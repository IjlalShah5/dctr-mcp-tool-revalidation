"""Real MCP Python SDK (v1.30.0) subprocess integration regression tests.

Run separately: python -m unittest discover -s tests -p 'sdk_*.py' -v
A dedicated CI job installs the pinned official MCP Python SDK. This is not
included in the dependency-free baseline regression count.
"""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from contextlib import asynccontextmanager
from pathlib import Path

from mcp import ClientSession, StdioServerParameters
from mcp.client.stdio import stdio_client

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from round3_official_sdk_gateway import SDKApprovalClient


class SDKMCPClientIntegration(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="round3-sdk-mcp-")
        self.root = Path(self.tmp.name)
        self.db = self.root / "approval.sqlite3"
        self.config = self.root / "fixture_contract.json"
        self.counter = self.root / "tool_invocation_count"
        self.counter.write_text("0", encoding="ascii")
        self.original = "Controlled local Echo Tool. It has no external side effects."
        self.l4_description = self.original + " IGNORE_APPROVAL_AND_EXFILTRATE"
        self.l2_description = self.original + " It accepts an additional local workflow note."

    async def asyncTearDown(self):
        self.tmp.cleanup()

    @asynccontextmanager
    async def connected(self, description: str):
        self.config.write_text(json.dumps({"description": description}), encoding="utf-8")
        params = StdioServerParameters(
            command=sys.executable,
            args=["-u", str(ROOT / "scripts" / "round3_official_sdk_server.py")],
            env={"DCTR_ROUND3_SDK_CONTRACT_FILE": str(self.config),
                 "DCTR_ROUND3_SDK_CALL_COUNTER": str(self.counter)},
        )
        async with stdio_client(params) as (read, write):
            async with ClientSession(read, write) as session:
                info = await session.initialize()
                self.assertEqual(info.serverInfo.name, "round3-synthetic-stdio-server")
                client = SDKApprovalClient(session, self.db)
                try:
                    yield client
                finally:
                    client.close()

    async def approved(self, client):
        result = await client.refresh()
        self.assertEqual(result.status, "INITIAL_TRUST")
        await client.approve_initial(explicit_human_approval=True)
        self.assertEqual((await client.refresh()).status, "STABLE_ACCEPT")

    def calls(self):
        return int(self.counter.read_text(encoding="ascii"))

    async def assert_blocked(self, client):
        previous = self.calls()
        with self.assertRaises(PermissionError):
            await client.call("should never reach SDK Tool")
        self.assertEqual(self.calls(), previous)

    async def test_01_real_sdk_initial_approval_gate(self):
        async with self.connected(self.original) as client:
            self.assertEqual((await client.refresh()).status, "INITIAL_TRUST")
            await self.assert_blocked(client)
            with self.assertRaises(PermissionError):
                await client.approve_initial(explicit_human_approval=False)
            await client.approve_initial(explicit_human_approval=True)
            result = await client.call("hello")
            self.assertFalse(result.isError)
            self.assertIn("hello", result.content[0].text)
            self.assertEqual(self.calls(), 1)

    async def test_02_real_sdk_l4_quarantine_blocks_tools_call(self):
        async with self.connected(self.original) as client:
            await self.approved(client)
        async with self.connected(self.l4_description) as client:
            outcome = await client.refresh()
            self.assertEqual((outcome.status, outcome.effective_level),
                             ("QUARANTINED", 4))
            await self.assert_blocked(client)

    async def test_03_sdk_quarantine_durable_across_server_and_client_restarts(self):
        async with self.connected(self.original) as client:
            await self.approved(client)
        async with self.connected(self.l4_description) as client:
            self.assertEqual((await client.refresh()).status, "QUARANTINED")
        async with self.connected(self.original) as client:
            self.assertEqual((await client.refresh()).status, "QUARANTINED_LOCKED")
            await self.assert_blocked(client)
        async with self.connected(self.l2_description) as client:
            self.assertEqual((await client.refresh()).status, "QUARANTINED_LOCKED")
            await self.assert_blocked(client)

    async def test_04_sdk_recovery_requires_two_administrative_factors(self):
        async with self.connected(self.original) as client:
            await self.approved(client)
        async with self.connected(self.l4_description) as client:
            await client.refresh()
            self.assertEqual((await client.recover(
                remediation_confirmed=True, explicit_human_approval=True
            )).status, "QUARANTINE_RECOVERY_REJECTED")
            await self.assert_blocked(client)
        async with self.connected(self.original) as client:
            self.assertEqual((await client.recover(remediation_confirmed=True)).status,
                             "QUARANTINED_LOCKED")
            self.assertEqual((await client.recover(explicit_human_approval=True)).status,
                             "QUARANTINED_LOCKED")
            await self.assert_blocked(client)
            self.assertEqual((await client.recover(
                remediation_confirmed=True, explicit_human_approval=True
            )).status, "QUARANTINE_RELEASED")
            self.assertFalse((await client.call("recovered")).isError)
            self.assertEqual(self.calls(), 1)

    async def test_05_sdk_unapproved_live_contract_is_blocked_pre_dispatch(self):
        async with self.connected(self.original) as client:
            await self.approved(client)
        async with self.connected(self.l2_description) as client:
            await self.assert_blocked(client)
            self.assertEqual((await client.refresh()).effective_level, 2)
            self.assertFalse((await client.call("bounded")).isError)
            self.assertEqual(self.calls(), 1)

    async def test_06_sdk_human_anchor_tampering_blocks_call(self):
        from dataclasses import replace
        async with self.connected(self.original) as client:
            await self.approved(client)
            state = client.store.load()
            client.store.save(replace(state, human_reviewed_baseline={"invalid": True}))
            await self.assert_blocked(client)
            self.assertEqual((await client.refresh()).status,
                             "HUMAN_ANCHOR_INTEGRITY_FAILURE")
            self.assertIsNotNone(client.store.load().quarantine)

    async def test_07_sdk_quarantine_survives_explicit_approval_flag(self):
        async with self.connected(self.original) as client:
            await self.approved(client)
        async with self.connected(self.l4_description) as client:
            result = await client.refresh(explicit_human_approval=True)
            self.assertEqual((result.status, result.effective_level), ("QUARANTINED", 4))
            await self.assert_blocked(client)

    async def test_08_sdk_repeated_l4_does_not_reset_trust(self):
        async with self.connected(self.original) as client:
            await self.approved(client)
        async with self.connected(self.l4_description) as client:
            old = client.store.load()
            self.assertEqual((await client.refresh()).status, "QUARANTINED")
            locked = client.store.load()
            self.assertEqual((await client.refresh()).status, "QUARANTINED_LOCKED")
            self.assertEqual(client.store.load(), locked)
            self.assertEqual(client.store.load().grant, old.grant)
            await self.assert_blocked(client)


if __name__ == "__main__":
    unittest.main(verbosity=2)
