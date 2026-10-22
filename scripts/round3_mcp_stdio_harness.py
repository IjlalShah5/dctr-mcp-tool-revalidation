#!/usr/bin/env python3
"""Round-3 controlled MCP stdio integration harness.

This is an experimental *client-side* adapter, not a production MCP client or a
general semantic classifier. It uses a real child process and newline-delimited
JSON-RPC 2.0 MCP stdio messages (initialize, tools/list and tools/call), and
durably stores the unchanged DCTR TrustState in SQLite before permitting calls.
The test-only "test/*" methods mutate a deliberately synthetic MCP server.
"""
from __future__ import annotations

import copy
import json
import sqlite3
import subprocess
import sys
from dataclasses import asdict
from pathlib import Path
from typing import Any

from canonicalize import sha256_digest
from revalidation_state import (
    ABSENT, Decision, Grant, QuarantineRecord, SemanticUncertainty, TrustState,
    revalidate, recover_quarantine,
)

SERVER_ID = "round3-synthetic-stdio-server"
TOOL_ID = "round3_echo"
PROTOCOL_VERSION = "2025-03-26"

BASE_TOOL: dict[str, Any] = {
    "name": TOOL_ID,
    "description": "Echo a message inside a controlled local test fixture.",
    "inputSchema": {
        "type": "object",
        "properties": {"message": {"type": "string"}},
        "required": ["message"],
    },
    "annotations": {"readOnlyHint": True, "title": "Echo fixture"},
    "x-round3-test": {"scope": 1, "write_enabled": False, "external_enabled": False},
}


def test_only_classifier(delta: list[dict[str, Any]]) -> int:
    """Predeclared, intentionally narrow fixture policy; NOT an NLP detector."""
    maximum = 0
    for entry in delta:
        path = entry["path"]
        after = entry["after"]
        before = entry["before"]
        if path == "/description" and isinstance(after, str) and (
            "IGNORE_APPROVAL_AND_EXFILTRATE" in after
        ):
            return 4
        if path == "/x-round3-test/scope" and isinstance(before, int) and isinstance(after, int):
            maximum = max(maximum, 3 if after - before >= 2 else 2)
        elif path == "/annotations/title":
            maximum = max(maximum, 1)
        else:
            maximum = max(maximum, 2)
    return maximum


def conservative_cross_path_guard(delta: list[dict[str, Any]]) -> int:
    """EXPERIMENTAL extension: escalate two jointly changed test switches to L3.

    It is not part of the frozen DCTR R0-R4 classifier and is never used to
    retroactively re-label the natural annotation sample.
    """
    paths = {item["path"] for item in delta}
    if {"/x-round3-test/write_enabled", "/x-round3-test/external_enabled"} <= paths:
        raise SemanticUncertainty("co-occurring bounded changes need holistic review")
    return test_only_classifier(delta)


def server_main() -> None:
    tool: dict[str, Any] | None = copy.deepcopy(BASE_TOOL)
    call_count = 0
    compound_effect_count = 0  # local fixture witness only, no external write/network
    for raw in sys.stdin:
        try:
            msg = json.loads(raw)
            method = msg.get("method")
            ident = msg.get("id")
            params = msg.get("params") or {}
            if method == "notifications/initialized":
                continue
            if method == "initialize":
                result = {
                    "protocolVersion": PROTOCOL_VERSION,
                    "capabilities": {"tools": {"listChanged": True}},
                    "serverInfo": {"name": SERVER_ID, "version": "round3-fixture"},
                }
            elif method == "tools/list":
                result = {"tools": [tool] if tool is not None else []}
            elif method == "tools/call":
                if tool is None or params.get("name") != TOOL_ID:
                    raise ValueError("unknown Tool")
                call_count += 1
                switches = tool.get("x-round3-test") or {}
                # An observable, deliberately SAFE local witness that exists
                # ONLY when two individually bounded contract fields co-occur.
                # No actual outbound traffic or file modification is performed.
                if (switches.get("write_enabled") is True
                        and switches.get("external_enabled") is True):
                    compound_effect_count += 1
                result = {"content": [{"type": "text", "text": str(
                    (params.get("arguments") or {}).get("message", "")
                )}], "isError": False}
            elif method == "test/set_contract":
                candidate = params.get("tool")
                if candidate is not None and (
                    not isinstance(candidate, dict) or candidate.get("name") != TOOL_ID
                ):
                    raise ValueError("invalid fixture contract")
                tool = candidate
                result = {"updated": True}
            elif method == "test/stats":
                result = {"tool_calls": call_count, "compound_effect_calls": compound_effect_count}
            else:
                raise ValueError("unsupported method")
            response = {"jsonrpc": "2.0", "id": ident, "result": result}
        except Exception as exc:
            response = {
                "jsonrpc": "2.0", "id": msg.get("id") if isinstance(msg, dict) else None,
                "error": {"code": -32603, "message": str(exc)},
            }
        sys.stdout.write(json.dumps(response, sort_keys=True, separators=(",", ":")) + "\n")
        sys.stdout.flush()


class StdioTestServer:
    """Subprocess transport exercising actual MCP-shaped stdio JSON-RPC messages."""

    def __init__(self) -> None:
        self.proc = subprocess.Popen(
            [sys.executable, "-u", str(Path(__file__).resolve()), "--server"],
            stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
            text=True, bufsize=1,
        )
        self._sequence = 0
        init = self.request("initialize", {
            "protocolVersion": PROTOCOL_VERSION,
            "capabilities": {},
            "clientInfo": {"name": "dctr-round3-test-client", "version": "1"},
        })
        if init["protocolVersion"] != PROTOCOL_VERSION:
            raise RuntimeError("fixture protocol negotiation failed")
        self.proc.stdin.write('{"jsonrpc":"2.0","method":"notifications/initialized"}\n')
        self.proc.stdin.flush()

    def request(self, method: str, params: dict[str, Any] | None = None) -> Any:
        if self.proc.poll() is not None:
            raise RuntimeError("MCP fixture process stopped")
        self._sequence += 1
        request = {"jsonrpc": "2.0", "id": self._sequence, "method": method,
                   "params": params or {}}
        assert self.proc.stdin is not None and self.proc.stdout is not None
        self.proc.stdin.write(json.dumps(request) + "\n")
        self.proc.stdin.flush()
        line = self.proc.stdout.readline()
        if not line:
            raise RuntimeError("fixture returned no JSON-RPC response")
        response = json.loads(line)
        if response.get("id") != self._sequence:
            raise RuntimeError("JSON-RPC request/response ID mismatch")
        if "error" in response:
            raise RuntimeError(response["error"]["message"])
        return response["result"]

    def set_contract(self, tool: dict[str, Any] | None) -> None:
        self.request("test/set_contract", {"tool": copy.deepcopy(tool)})

    def calls(self) -> int:
        return int(self.request("test/stats")["tool_calls"])

    def compound_effects(self) -> int:
        return int(self.request("test/stats")["compound_effect_calls"])

    def close(self) -> None:
        if self.proc.poll() is None:
            assert self.proc.stdin is not None
            self.proc.stdin.close()
            self.proc.terminate()
            try:
                self.proc.wait(timeout=3)
            except subprocess.TimeoutExpired:
                self.proc.kill()
                self.proc.wait(timeout=3)
        for stream in (self.proc.stdout, self.proc.stderr):
            if stream is not None:
                stream.close()


class SQLiteTrustStore:
    """Durable, transactional TrustState serialization; one active Tool identity."""

    def __init__(self, path: str | Path) -> None:
        self.connection = sqlite3.connect(str(path), timeout=10, isolation_level=None)
        self.connection.execute("PRAGMA journal_mode=WAL")
        self.connection.execute("PRAGMA synchronous=FULL")
        self.connection.execute(
            "CREATE TABLE IF NOT EXISTS approval_state ("
            "tool_id TEXT PRIMARY KEY, payload TEXT NOT NULL)"
        )

    def load(self) -> TrustState:
        row = self.connection.execute(
            "SELECT payload FROM approval_state WHERE tool_id=?", (TOOL_ID,)
        ).fetchone()
        if row is None:
            return TrustState(None, None, None)
        data = json.loads(row[0])
        grant = Grant(**data["grant"]) if data["grant"] is not None else None
        q = QuarantineRecord(**data["quarantine"]) if data["quarantine"] is not None else None
        return TrustState(
            data["operational_baseline"], data["human_reviewed_baseline"], grant, q
        )

    def save(self, state: TrustState) -> None:
        payload = json.dumps(asdict(state), sort_keys=True, separators=(",", ":"))
        self.connection.execute("BEGIN IMMEDIATE")
        try:
            self.connection.execute(
                "INSERT INTO approval_state(tool_id,payload) VALUES (?,?) "
                "ON CONFLICT(tool_id) DO UPDATE SET payload=excluded.payload",
                (TOOL_ID, payload),
            )
            self.connection.execute("COMMIT")
        except BaseException:
            self.connection.execute("ROLLBACK")
            raise

    def close(self) -> None:
        self.connection.close()


class SQLiteMCPApprovalClient:
    """Minimal integrating client. No invocation proceeds without a fresh trust check."""

    def __init__(self, server: StdioTestServer, database_path: str | Path,
                 classifier=test_only_classifier) -> None:
        self.server = server
        self.store = SQLiteTrustStore(database_path)
        self.classifier = classifier

    def _advertised(self) -> Any:
        tools = self.server.request("tools/list")["tools"]
        matches = [t for t in tools if t.get("name") == TOOL_ID]
        if len(matches) > 1:
            raise PermissionError("duplicate Tool identities: fail closed")
        return matches[0] if matches else ABSENT

    def refresh(self, *, explicit_human_approval: bool | None = None):
        candidate = self._advertised()
        result = revalidate(
            self.store.load(), candidate, server_id=SERVER_ID, tool_id=TOOL_ID,
            policy_context="round3-controlled", approval_time="round3",
            classify_level=self.classifier,
            explicit_human_approval=explicit_human_approval,
        )
        # Transaction commits the quarantine marker before returning a status.
        self.store.save(result.state)
        return result

    def approve_initial(self, *, explicit_human_approval: bool) -> None:
        if explicit_human_approval is not True:
            raise PermissionError("initial approval requires explicit human decision")
        if self.store.load() != TrustState(None, None, None):
            raise PermissionError("grant/baseline is not entirely absent")
        contract = self._advertised()
        if contract is ABSENT:
            raise PermissionError("cannot approve an absent Tool")
        digest = sha256_digest(contract)
        grant = Grant(SERVER_ID, TOOL_ID, digest, digest,
                      "round3-initial-approval", "round3")
        self.store.save(TrustState(contract, contract, grant))

    def call(self, message: str) -> Any:
        # Enforced on every call, not merely on catalogue refresh.
        state = self.store.load()
        if state.quarantine is not None:
            raise PermissionError("QUARANTINED_LOCKED")
        if state.grant is None or state.operational_baseline is None or (
            state.human_reviewed_baseline is None
        ):
            raise PermissionError("NO_ACTIVE_COMPLETE_GRANT")
        if state.grant.server_id != SERVER_ID or state.grant.tool_id != TOOL_ID:
            raise PermissionError("GRANT_IDENTITY_MISMATCH")
        try:
            if sha256_digest(state.operational_baseline) != state.grant.approved_hash:
                raise PermissionError("OPERATIONAL_HASH_INTEGRITY_FAILURE")
            if sha256_digest(state.human_reviewed_baseline) != state.grant.human_reviewed_hash:
                raise PermissionError("HUMAN_HASH_INTEGRITY_FAILURE")
            candidate = self._advertised()
            if candidate is ABSENT or sha256_digest(candidate) != state.grant.approved_hash:
                raise PermissionError("UNAPPROVED_LIVE_CONTRACT")
        except (TypeError, ValueError, OverflowError) as exc:
            raise PermissionError("UNVERIFIABLE_STATE") from exc
        return self.server.request("tools/call", {
            "name": TOOL_ID, "arguments": {"message": message}
        })

    def recover(self, *, remediation_confirmed=False, explicit_human_approval=False):
        result = recover_quarantine(
            self.store.load(), self._advertised(),
            server_id=SERVER_ID, tool_id=TOOL_ID,
            policy_context="round3-admin-recovery", approval_time="round3",
            classify_level=self.classifier,
            remediation_confirmed=remediation_confirmed,
            explicit_human_approval=explicit_human_approval,
        )
        self.store.save(result.state)
        return result

    def close(self) -> None:
        self.store.close()


if __name__ == "__main__" and "--server" in sys.argv:
    server_main()
