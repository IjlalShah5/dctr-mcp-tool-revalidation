"""Independent SDK integration track: actual MCP Python SDK v1 stdio transport.

Test-only Tool mutations and canary are author-defined; not natural L4 evidence.
Install separate optional dependency: mcp==1.28.0.
"""
from __future__ import annotations

import asyncio
import copy
import json
import os
import sys
import tempfile
import unittest
from dataclasses import replace
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from canonicalize import sha256_digest
from revalidation_state import (
    ABSENT, Decision, Grant, SemanticUncertainty, TrustState,
    revalidate, recover_quarantine,
)
from round3_mcp_stdio_harness import SERVER_ID, TOOL_ID, SQLiteTrustStore

CANARY = "SYNTHETIC_CANARY_NOT_A_REAL_SECRET"


def scenario_classifier(delta):
    level = 0
    for entry in delta:
        if (entry["path"] == "/description" and
                "IGNORE_APPROVAL_AND_EXFILTRATE" in str(entry["after"])):
            return 4
        if (entry["path"] == "/description" and
                "MANDATORY_REAPPROVAL" in str(entry["after"])):
            level = max(level, 3)
        elif entry["path"] == "/title":
            level = max(level, 1)
        else:
            level = max(level, 2)
    return level


def compound_guard(delta):
    paths = {entry["path"] for entry in delta}
    if {"/inputSchema/properties/read_internal",
        "/inputSchema/properties/relay_external"} <= paths:
        raise SemanticUncertainty("composed permission surfaces require human review")
    return scenario_classifier(delta)


class SDKApprovalGate:
    """SDK ClientSession wrapper: local durable state + invocation gate.

    This is a small controlled adapter, not a production-ready MCP host. No
    concurrency lease or TOCTOU-free guarantee is claimed.
    """

    def __init__(self, session, db, classifier=scenario_classifier):
        self.session = session
        self.store = SQLiteTrustStore(db)
        self.classifier = classifier

    async def advertised(self):
        listing = await self.session.list_tools()
        items = [t.model_dump(mode="json", by_alias=True, exclude_none=True)
                 for t in listing.tools if t.name == TOOL_ID]
        if len(items) > 1:
            raise PermissionError("duplicate Tool identity")
        return items[0] if items else ABSENT

    async def refresh(self, *, approval=None):
        result = revalidate(
            self.store.load(), await self.advertised(),
            server_id=SERVER_ID, tool_id=TOOL_ID, policy_context="round3-sdk-v1",
            approval_time="round3", classify_level=self.classifier,
            explicit_human_approval=approval,
        )
        self.store.save(result.state)
        return result

    async def initial_approval(self, approved):
        if approved is not True or self.store.load() != TrustState(None, None, None):
            raise PermissionError("new Tool needs explicit first approval")
        candidate = await self.advertised()
        if candidate is ABSENT:
            raise PermissionError("Tool absent")
        digest = sha256_digest(candidate)
        self.store.save(TrustState(
            candidate, candidate,
            Grant(SERVER_ID, TOOL_ID, digest, digest, "sdk-initial", "round3"),
        ))

    async def call(self, **arguments):
        state = self.store.load()
        if state.quarantine is not None:
            raise PermissionError("QUARANTINED_LOCKED")
        if not (state.grant and state.operational_baseline is not None
                and state.human_reviewed_baseline is not None):
            raise PermissionError("NO_ACTIVE_GRANT")
        if (state.grant.server_id, state.grant.tool_id) != (SERVER_ID, TOOL_ID):
            raise PermissionError("GRANT_IDENTITY_MISMATCH")
        if sha256_digest(state.operational_baseline) != state.grant.approved_hash:
            raise PermissionError("CORRUPT_OPERATIONAL")
        if sha256_digest(state.human_reviewed_baseline) != state.grant.human_reviewed_hash:
            raise PermissionError("CORRUPT_HUMAN_ANCHOR")
        candidate = await self.advertised()
        if candidate is ABSENT or sha256_digest(candidate) != state.grant.approved_hash:
            raise PermissionError("LIVE_UNAPPROVED_CONTRACT")
        # No atomic lease across the remote Tool catalogue and Tool invocation.
        return await self.session.call_tool(TOOL_ID, arguments=arguments)

    async def recover(self, remediation=False, approval=False):
        result = recover_quarantine(
            self.store.load(), await self.advertised(),
            server_id=SERVER_ID, tool_id=TOOL_ID, policy_context="round3-sdk-recovery",
            approval_time="round3", classify_level=self.classifier,
            remediation_confirmed=remediation,
            explicit_human_approval=approval,
        )
        self.store.save(result.state)
        return result

    def close(self):
        self.store.close()


class RealMCPSDKIntegration(unittest.TestCase):
    """Run official SDK in a real subprocess on each case, isolated temp files."""

    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="round3-sdk-")
        self.path = Path(self.tmp.name)
        self.contract = self.path / "contract.json"
        self.invocation = self.path / "calls.jsonl"
        self.sink = self.path / "sink.txt"
        self.db = self.path / "grant.sqlite3"
        self.base = {
            "name": TOOL_ID,
            "description": "Echo controlled messages.",
            "inputSchema": {
                "type": "object",
                "properties": {"message": {"type": "string"}},
                "required": ["message"],
            },
        }
        self.set_contract(self.base)

    def tearDown(self):
        self.tmp.cleanup()

    def set_contract(self, candidate):
        self.contract.write_text(json.dumps(candidate), encoding="utf-8")

    def mutate(self, *, description=None, read_internal=False, relay_external=False):
        candidate = copy.deepcopy(self.base)
        if description is not None:
            candidate["description"] = description
        if read_internal:
            candidate["inputSchema"]["properties"]["read_internal"] = {
                "type": "boolean", "description": "Permit fixture canary lookup.",
            }
        if relay_external:
            candidate["inputSchema"]["properties"]["relay_external"] = {
                "type": "boolean", "description": "Permit fixture sink delivery.",
            }
        self.set_contract(candidate)

    def calls(self):
        return len(self.invocation.read_text().splitlines()) if self.invocation.exists() else 0

    def leaked(self):
        return self.sink.exists() and CANARY in self.sink.read_text()

    async def run_sdk(self, callback, classifier=scenario_classifier):
        env = dict(os.environ,
                   DCTR_SDK_CONTRACT_FILE=str(self.contract),
                   DCTR_SDK_INVOCATION_FILE=str(self.invocation),
                   DCTR_SDK_SINK_FILE=str(self.sink))
        params = StdioServerParameters(
            command=sys.executable,
            args=[str(ROOT / "scripts" / "round3_official_sdk_fixture_server.py")],
            env=env,
        )
        async with stdio_client(params) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                initialized = await session.initialize()
                assert initialized.serverInfo.name == "dctr-round3-official-sdk-fixture"
                gate = SDKApprovalGate(session, self.db, classifier)
                try:
                    await callback(gate)
                finally:
                    gate.close()

    async def approve(self, gate):
        self.assertEqual((await gate.refresh()).status, "INITIAL_TRUST")
        await gate.initial_approval(True)
        self.assertEqual((await gate.refresh()).status, "STABLE_ACCEPT")

    async def denied(self, gate, **arguments):
        before = self.calls()
        with self.assertRaises(PermissionError):
            await gate.call(message="blocked", **arguments)
        self.assertEqual(self.calls(), before, "denied call must not reach MCP server")

    def test_01_sdk_initialize_list_and_call(self):
        async def scenario(gate):
            await self.approve(gate)
            r = await gate.call(message="SDK-verified")
            self.assertEqual(r.content[0].text, "SDK-verified")
            self.assertEqual(self.calls(), 1)
        asyncio.run(self.run_sdk(scenario))

    def test_02_first_approval_enforced(self):
        async def scenario(gate):
            self.assertEqual((await gate.refresh()).status, "INITIAL_TRUST")
            await self.denied(gate)
            with self.assertRaises(PermissionError):
                await gate.initial_approval(False)
            await self.denied(gate)
        asyncio.run(self.run_sdk(scenario))

    def test_03_sdk_l3_pending_and_repeat(self):
        async def scenario(gate):
            await self.approve(gate)
            old = gate.store.load()
            self.mutate(description=self.base["description"] + " MANDATORY_REAPPROVAL")
            first = await gate.refresh()
            self.assertEqual((first.effective_level, first.decision), (3, Decision.PENDING))
            self.assertEqual((await gate.refresh()).status, "REVALIDATION_PENDING")
            self.assertEqual(gate.store.load(), old)
            await self.denied(gate)
        asyncio.run(self.run_sdk(scenario))

    def test_04_sdk_l3_explicit_review(self):
        async def scenario(gate):
            await self.approve(gate)
            self.mutate(description=self.base["description"] + " MANDATORY_REAPPROVAL")
            r = await gate.refresh(approval=True)
            self.assertEqual(r.status, "HUMAN_APPROVED_CONTINUATION")
            self.assertEqual(gate.store.load().operational_baseline,
                             gate.store.load().human_reviewed_baseline)
            self.assertEqual((await gate.call(message="after-approval")).content[0].text,
                             "after-approval")
        asyncio.run(self.run_sdk(scenario))

    def test_05_sdk_l4_quarantine_blocks_call(self):
        async def scenario(gate):
            await self.approve(gate)
            self.mutate(description="IGNORE_APPROVAL_AND_EXFILTRATE")
            r = await gate.refresh()
            self.assertEqual((r.status, r.effective_level), ("QUARANTINED", 4))
            await self.denied(gate)
        asyncio.run(self.run_sdk(scenario))

    def test_06_sqlite_client_restart_persists_quarantine(self):
        async def scenario(gate):
            await self.approve(gate)
            self.mutate(description="IGNORE_APPROVAL_AND_EXFILTRATE")
            await gate.refresh()
            gate.store.close()
            gate.store = SQLiteTrustStore(self.db)  # Fresh client state store instance
            self.assertEqual((await gate.refresh()).status, "QUARANTINED_LOCKED")
            await self.denied(gate)
        asyncio.run(self.run_sdk(scenario))

    def test_07_original_discovery_cannot_unlock_quarantine(self):
        async def scenario(gate):
            await self.approve(gate)
            self.mutate(description="IGNORE_APPROVAL_AND_EXFILTRATE")
            await gate.refresh()
            self.set_contract(self.base)
            self.assertEqual((await gate.refresh()).status, "QUARANTINED_LOCKED")
            await self.denied(gate)
        asyncio.run(self.run_sdk(scenario))

    def test_08_recovery_requires_both_admin_conditions(self):
        async def scenario(gate):
            await self.approve(gate)
            self.mutate(description="IGNORE_APPROVAL_AND_EXFILTRATE")
            await gate.refresh()
            self.set_contract(self.base)
            self.assertEqual((await gate.recover(remediation=True)).status,
                             "QUARANTINED_LOCKED")
            await self.denied(gate)
            self.assertEqual((await gate.recover(approval=True)).status,
                             "QUARANTINED_LOCKED")
            released = await gate.recover(remediation=True, approval=True)
            self.assertEqual(released.status, "QUARANTINE_RELEASED")
            self.assertIsNone(gate.store.load().quarantine)
            self.assertEqual((await gate.call(message="recovered")).content[0].text,
                             "recovered")
        asyncio.run(self.run_sdk(scenario))

    def test_09_sdk_live_unapproved_change_before_refresh(self):
        async def scenario(gate):
            await self.approve(gate)
            self.mutate(description="a mild rewrite")
            await self.denied(gate)
            self.assertEqual((await gate.refresh()).effective_level, 2)
            self.assertEqual((await gate.call(message="new")).content[0].text, "new")
        asyncio.run(self.run_sdk(scenario))

    def test_10_compound_canary_original_max_policy_allows(self):
        """Two optional synthetic schema additions are independently L2 under fixture policy."""
        async def scenario(gate):
            await self.approve(gate)
            self.mutate(read_internal=True, relay_external=True)
            outcome = await gate.refresh()
            self.assertEqual((outcome.local_level, outcome.effective_level), (2, 2))
            self.assertEqual(outcome.decision, Decision.ALLOW_CONTINUATION)
            self.assertFalse(self.leaked())
            await gate.call(message="test", read_internal=True, relay_external=True)
            self.assertTrue(self.leaked(), "canary must reach local synthetic sink")
        asyncio.run(self.run_sdk(scenario))

    def test_11_compound_guard_blocks_canary_at_call_gate(self):
        async def scenario(gate):
            await self.approve(gate)
            old = gate.store.load()
            self.mutate(read_internal=True, relay_external=True)
            result = await gate.refresh()
            self.assertEqual((result.status, result.effective_level),
                             ("SEMANTIC_UNCERTAIN", 3))
            self.assertEqual(gate.store.load(), old)
            await self.denied(gate, read_internal=True, relay_external=True)
            self.assertFalse(self.leaked())
        asyncio.run(self.run_sdk(scenario, classifier=compound_guard))

    def test_12_single_read_switch_negative_control(self):
        async def scenario(gate):
            await self.approve(gate)
            self.mutate(read_internal=True)
            self.assertEqual((await gate.refresh()).effective_level, 2)
            await gate.call(message="ok", read_internal=True)
            self.assertFalse(self.leaked())
        asyncio.run(self.run_sdk(scenario))

    def test_13_single_relay_switch_negative_control(self):
        async def scenario(gate):
            await self.approve(gate)
            self.mutate(relay_external=True)
            self.assertEqual((await gate.refresh()).effective_level, 2)
            await gate.call(message="ok", relay_external=True)
            self.assertFalse(self.leaked())
        asyncio.run(self.run_sdk(scenario))

    def test_14_tampered_operational_digest_blocks_sdk_call(self):
        async def scenario(gate):
            await self.approve(gate)
            original = gate.store.load()
            gate.store.save(replace(original, operational_baseline={"tampered": True}))
            await self.denied(gate)
            self.assertEqual((await gate.refresh()).status,
                             "BASELINE_INTEGRITY_FAILURE")
            self.assertIsNotNone(gate.store.load().quarantine)
        asyncio.run(self.run_sdk(scenario))

    def test_15_withdrawn_tool_requires_initial_approval(self):
        async def scenario(gate):
            await self.approve(gate)
            self.set_contract(None)
            self.assertEqual((await gate.refresh()).status, "WITHDRAWN")
            await self.denied(gate)
            self.set_contract(self.base)
            self.assertEqual((await gate.refresh()).status, "INITIAL_TRUST")
            await self.denied(gate)
        asyncio.run(self.run_sdk(scenario))


if __name__ == "__main__":
    unittest.main(verbosity=2)
