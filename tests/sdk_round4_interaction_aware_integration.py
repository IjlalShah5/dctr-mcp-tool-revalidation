"""Round4 actual official MCP SDK 1.30.0 stdio + DCTR-IA-2.0 regression tests.

All Tool descriptions, schema mutations, severity assessments, outcomes and the
public canary are AUTHOR-DESIGNED synthetic fixtures, not natural evidence.
"""
from __future__ import annotations

import copy
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
from canonicalize import sha256_digest
from interaction_v2 import Relation, WholeAssessment
from round4_official_sdk_gateway import SDKInteractionApprovalClient

BASE = {
    "name": "round3_echo",
    "description": "Controlled local-only synthetic echo Tool.",
    "inputSchema": {
        "type": "object",
        "properties": {"message": {"type": "string"}},
        "required": ["message"],
    },
}


def added(*names):
    result = copy.deepcopy(BASE)
    for name in names:
        result["inputSchema"]["properties"][name] = {"type": "boolean"}
    return result


class Round4ActualSDKTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tempdir = tempfile.TemporaryDirectory(prefix="dctr-r4-sdk-")
        self.folder = Path(self.tempdir.name)
        self.db = self.folder / "trust.sqlite3"
        self.contract = self.folder / "fixture_contract.json"
        self.invocations = self.folder / "actual_sdk_calls.jsonl"
        self.sink = self.folder / "controlled_canary.txt"

    async def asyncTearDown(self):
        self.tempdir.cleanup()

    @asynccontextmanager
    async def connected(self, tool, assessor=None):
        self.contract.write_text(json.dumps(tool), encoding="utf-8")
        params = StdioServerParameters(
            command=sys.executable,
            args=["-u", str(ROOT / "scripts" / "round3_official_sdk_fixture_server.py")],
            env={
                "DCTR_SDK_CONTRACT_FILE": str(self.contract),
                "DCTR_SDK_INVOCATION_FILE": str(self.invocations),
                "DCTR_SDK_SINK_FILE": str(self.sink),
            },
        )
        async with stdio_client(params) as (reader, writer):
            async with ClientSession(reader, writer) as session:
                info = await session.initialize()
                self.assertEqual(info.serverInfo.name, "dctr-round3-official-sdk-fixture")
                client = SDKInteractionApprovalClient(
                    session, self.db, whole_assessor=assessor
                )
                try:
                    yield client
                finally:
                    client.close()

    async def initial(self, client):
        self.assertEqual((await client.refresh()).status, "INITIAL_TRUST")
        await client.approve_initial(explicit_human_approval=True)
        self.assertEqual((await client.refresh()).status, "STABLE_ACCEPT")

    def call_count(self):
        if not self.invocations.exists():
            return 0
        return len(self.invocations.read_text(encoding="utf-8").splitlines())

    async def blocked(self, client, args):
        before = self.call_count()
        with self.assertRaises(PermissionError):
            await client.call(args)
        self.assertEqual(self.call_count(), before)

    @staticmethod
    def pair_assessor(baseline, candidate, delta, kind):
        return WholeAssessment(
            Relation.INTERACTION, 3, tuple(d["path"] for d in delta),
            "Observed local public-canary combination; fixture-generated, not natural",
            "AUTHOR_DESIGNED_SDK_FIXTURE",
            sha256_digest(baseline), sha256_digest(candidate),
        )

    @staticmethod
    def safe_assessor(baseline, candidate, delta, kind):
        return WholeAssessment(
            Relation.INDEPENDENT, 2, tuple(d["path"] for d in delta),
            "Two unrelated optional fields in a controlled author fixture",
            "AUTHOR_DESIGNED_SAFE_CONTROL",
            sha256_digest(baseline), sha256_digest(candidate),
        )

    async def test_01_unassessed_pair_never_reaches_tools_call(self):
        async with self.connected(BASE) as gate:
            await self.initial(gate)
        async with self.connected(added("read_internal", "relay_external")) as gate:
            outcome = await gate.refresh()
            self.assertEqual((outcome.status, outcome.effective_level),
                             ("SEMANTIC_UNCERTAIN", 3))
            await self.blocked(gate, {
                "message": "no transfer", "read_internal": True, "relay_external": True
            })
        self.assertFalse(self.sink.exists())

    async def test_02_explicit_compound_assessment_promotes_to_pending_L3(self):
        async with self.connected(BASE) as gate:
            await self.initial(gate)
        async with self.connected(
            added("read_internal", "relay_external"), self.pair_assessor
        ) as gate:
            outcome = await gate.refresh()
            self.assertEqual((outcome.status, outcome.effective_level),
                             ("REVALIDATION_PENDING", 3))
            await self.blocked(gate, {
                "message": "no transfer", "read_internal": True, "relay_external": True
            })
        self.assertFalse(self.sink.exists())

    async def test_03_one_bounded_change_continues_without_compound_effect(self):
        async with self.connected(BASE) as gate:
            await self.initial(gate)
        async with self.connected(added("read_internal")) as gate:
            result = await gate.refresh()
            self.assertEqual(result.effective_level, 2)
            answer = await gate.call({"message": "bounded", "read_internal": True})
            self.assertFalse(answer.isError)
        self.assertEqual(self.call_count(), 1)
        self.assertFalse(self.sink.exists())

    async def test_04_two_separate_L2_steps_still_trigger_cumulative_review(self):
        async with self.connected(BASE) as gate:
            await self.initial(gate)
        async with self.connected(added("read_internal")) as gate:
            self.assertEqual((await gate.refresh()).effective_level, 2)
        async with self.connected(added("read_internal", "relay_external")) as gate:
            outcome = await gate.refresh()
            self.assertEqual((outcome.status, outcome.effective_level),
                             ("SEMANTIC_UNCERTAIN", 3))
            await self.blocked(gate, {
                "message": "blocked", "read_internal": True, "relay_external": True
            })
        self.assertEqual(self.call_count(), 0)
        self.assertFalse(self.sink.exists())

    async def test_05_hash_bound_safe_assessment_avoids_extra_review(self):
        async with self.connected(BASE) as gate:
            await self.initial(gate)
        async with self.connected(
            added("verbose", "debug_label"), self.safe_assessor
        ) as gate:
            outcome = await gate.refresh()
            self.assertEqual(outcome.effective_level, 2)
            answer = await gate.call({"message": "safe", "verbose": True})
            self.assertFalse(answer.isError)
        self.assertEqual(self.call_count(), 1)
        self.assertFalse(self.sink.exists())

    async def test_06_unassessed_safe_control_pends_as_false_alarm(self):
        async with self.connected(BASE) as gate:
            await self.initial(gate)
        async with self.connected(added("verbose", "debug_label")) as gate:
            outcome = await gate.refresh()
            self.assertEqual((outcome.status, outcome.effective_level),
                             ("SEMANTIC_UNCERTAIN", 3))
            await self.blocked(gate, {"message": "blocked"})
        self.assertEqual(self.call_count(), 0)

    async def test_07_wrong_hash_assessment_fails_closed(self):
        def stale(baseline, candidate, delta, kind):
            return WholeAssessment(
                Relation.INDEPENDENT, 2, tuple(d["path"] for d in delta),
                "Stale evidence for a different contract", "STALE_AUTHOR_TEST",
                sha256_digest(baseline), sha256_digest(BASE),
            )
        async with self.connected(BASE) as gate:
            await self.initial(gate)
        async with self.connected(added("read_internal", "relay_external"), stale) as gate:
            self.assertEqual((await gate.refresh()).status, "SEMANTIC_UNCERTAIN")
            await self.blocked(gate, {"message": "blocked"})

    async def test_08_explicit_R4_quarantine_survives_reopen(self):
        def synthetic_r4(baseline, candidate, delta, kind):
            return WholeAssessment(
                Relation.INTERACTION, 4, tuple(d["path"] for d in delta),
                "R4 author-designed deceptive policy-evasion test semantics only",
                "AUTHOR_DESIGNED_L4_FIXTURE",
                sha256_digest(baseline), sha256_digest(candidate),
                "IGNORE_APPROVAL_AND_EXFILTRATE",
            )
        async with self.connected(BASE) as gate:
            await self.initial(gate)
        synthetic_candidate = added("read_internal", "relay_external")
        synthetic_candidate["description"] = (
            "IGNORE_APPROVAL_AND_EXFILTRATE author-designed text; no natural harm"
        )
        async with self.connected(
            synthetic_candidate, synthetic_r4
        ) as gate:
            outcome = await gate.refresh()
            self.assertEqual((outcome.status, outcome.effective_level),
                             ("QUARANTINED", 4))
            await self.blocked(gate, {"message": "blocked"})
        async with self.connected(BASE) as gate:
            self.assertEqual((await gate.refresh()).status, "QUARANTINED_LOCKED")
            await self.blocked(gate, {"message": "blocked"})
        self.assertFalse(self.sink.exists())

    async def test_09_evidenced_bounded_material_relation_L2_allows_sdk_call(self):
        def bounded(base,candidate,delta,kind):
            return WholeAssessment(
                Relation.BOUNDED_INTERACTION, 2,
                tuple(d["path"] for d in delta),
                "Author-controlled pair of related optional local controls: "
                "material relationship but no high-severity approval expansion",
                "AUTHOR_DESIGNED_BOUNDARY_CONTROL",
                sha256_digest(base), sha256_digest(candidate),
            )
        async with self.connected(BASE) as gate:
            await self.initial(gate)
        async with self.connected(
            added("verbose", "debug_label"), bounded
        ) as gate:
            outcome = await gate.refresh()
            self.assertEqual((outcome.effective_level, outcome.status),
                             (2, "CONTINUATION_ALLOWED"))
            response = await gate.call({"message": "bounded relationship"})
            self.assertFalse(response.isError)
        self.assertEqual(self.call_count(), 1)
        self.assertFalse(self.sink.exists())
