#!/usr/bin/env python3
"""Reference integrating client using the official MCP Python SDK v1.30.0.

An actual SDK ClientSession is used for tools/list and tools/call over stdio.
All trust decisions use the existing DCTR revalidate/recover_quarantine and
SQLiteTrustStore from the previously CI-tested controlled harness.
This adapter is an experimental fixture, not a production authorization service.
"""
from __future__ import annotations

from dataclasses import replace
from pathlib import Path
from typing import Any

from canonicalize import sha256_digest
from revalidation_state import ABSENT, Grant, TrustState, revalidate, recover_quarantine
from round3_mcp_stdio_harness import (
    SERVER_ID, TOOL_ID, SQLiteTrustStore, test_only_classifier
)


class SDKApprovalClient:
    def __init__(self, session: Any, database_path: str | Path) -> None:
        self.session = session
        self.store = SQLiteTrustStore(database_path)

    async def discover(self) -> Any:
        response = await self.session.list_tools()
        matches = [tool for tool in response.tools if tool.name == TOOL_ID]
        if len(matches) > 1:
            raise PermissionError("duplicate Tool IDs: fail closed")
        if not matches:
            return ABSENT
        # by_alias preserves protocol-defined client-visible JSON field spellings.
        return matches[0].model_dump(mode="json", by_alias=True, exclude_none=True)

    async def refresh(self, *, explicit_human_approval: bool | None = None):
        candidate = await self.discover()
        result = revalidate(
            self.store.load(), candidate,
            server_id=SERVER_ID, tool_id=TOOL_ID,
            policy_context="round3-mcp-python-sdk", approval_time="round3-sdk",
            classify_level=test_only_classifier,
            explicit_human_approval=explicit_human_approval,
        )
        self.store.save(result.state)
        return result

    async def approve_initial(self, *, explicit_human_approval: bool) -> None:
        if explicit_human_approval is not True:
            raise PermissionError("requires explicit initial approval")
        if self.store.load() != TrustState(None, None, None):
            raise PermissionError("initial trust requires entirely empty state")
        candidate = await self.discover()
        if candidate is ABSENT:
            raise PermissionError("absent Tool")
        digest = sha256_digest(candidate)
        grant = Grant(SERVER_ID, TOOL_ID, digest, digest, "round3-sdk", "initial")
        self.store.save(TrustState(candidate, candidate, grant))

    async def call(self, text: str):
        state = self.store.load()
        if state.quarantine is not None:
            raise PermissionError("QUARANTINED_LOCKED")
        grant = state.grant
        if grant is None or state.operational_baseline is None or state.human_reviewed_baseline is None:
            raise PermissionError("NO_ACTIVE_COMPLETE_GRANT")
        if grant.server_id != SERVER_ID or grant.tool_id != TOOL_ID:
            raise PermissionError("IDENTITY_MISMATCH")
        try:
            if sha256_digest(state.operational_baseline) != grant.approved_hash:
                raise PermissionError("OPERATIONAL_HASH_MISMATCH")
            if sha256_digest(state.human_reviewed_baseline) != grant.human_reviewed_hash:
                raise PermissionError("HUMAN_HASH_MISMATCH")
        except (ValueError, OverflowError, TypeError) as exc:
            raise PermissionError("CORRUPT_GRANT") from exc
        live = await self.discover()
        if live is ABSENT or sha256_digest(live) != grant.approved_hash:
            raise PermissionError("UNAPPROVED_LIVE_CONTRACT")
        # The SDK performs the real tools/call. The pre-call contract check is
        # client-side; a malicious server can still change its behavior afterward.
        return await self.session.call_tool(TOOL_ID, arguments={"message": text})

    async def recover(self, *, remediation_confirmed=False, explicit_human_approval=False):
        result = recover_quarantine(
            self.store.load(), await self.discover(),
            server_id=SERVER_ID, tool_id=TOOL_ID,
            policy_context="round3-sdk-remediation", approval_time="round3-sdk",
            classify_level=test_only_classifier,
            remediation_confirmed=remediation_confirmed,
            explicit_human_approval=explicit_human_approval,
        )
        self.store.save(result.state)
        return result

    def close(self):
        self.store.close()
