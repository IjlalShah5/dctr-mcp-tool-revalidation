"""Round4 measured SDK policy-outcome matrix, all AUTHOR-CONTROLLED fixtures.

An official MCP SDK ClientSession exchanges real tools/list and tools/call over
stdio. The public local-file marker is a controlled functional outcome, NOT a
real exfiltration, security harm or a natural Tool observation.

Two policies share the exact same SDK call gate and SQLite TrustState:
- historical DCTR revalidate() with deliberately narrow all-L2 TEST classifier;
- prospective revalidate_v2() with missing/explicit synthetic whole assessments.
This is a counterexample/mechanism comparison, not security-effectiveness ranking.
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

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from canonicalize import sha256_digest
from interaction_v2 import WholeAssessment,Relation
from revalidation_state import Decision, revalidate
from round4_official_sdk_gateway import SDKInteractionApprovalClient
from round3_mcp_stdio_harness import SERVER_ID,TOOL_ID


def fixture_classifier(delta):
    # Deliberately narrow AUTHOR-DEFINED path-level test fixture, NOT expert L2.
    return 2 if delta else 0


BASE = {
    "name": "round3_echo",
    "description": "Controlled local SDK outcome-oracle tool.",
    "inputSchema": {
        "type": "object",
        "properties": {"message": {"type": "string"}},
        "required": ["message"],
    },
}


def positive_cases():
    # Different schema mutations/trigger operations, all synthetic local outcomes.
    scenarios=[]
    t=copy.deepcopy(BASE)
    for name in ("read_internal","relay_external"):
        t["inputSchema"]["properties"][name]={"type":"boolean","default":False}
    scenarios.append(("P01-two-opt-in-switches",BASE,t,{"message":"test","read_internal":True,"relay_external":True},{"read_internal":True,"relay_external":True}))

    t=copy.deepcopy(BASE)
    for name in ("write_local","remote_sync"):
        t["inputSchema"]["properties"][name]={"type":"boolean","default":False}
    scenarios.append(("P02-write-plus-sync",BASE,t,{"message":"test","write_local":True,"remote_sync":True},{"write_local":True,"remote_sync":True}))

    b=copy.deepcopy(BASE)
    b["inputSchema"]["properties"]["operation"]={"type":"string","enum":["preview"]}
    t=copy.deepcopy(b)
    t["inputSchema"]["properties"]["operation"]["enum"]=["preview","publish"]
    t["inputSchema"]["properties"]["confirm_external"]={"type":"boolean","default":False}
    scenarios.append(("P03-enum-plus-confirmation",b,t,{"message":"test","operation":"publish","confirm_external":True},{"operation":"publish","confirm_external":True}))

    b=copy.deepcopy(BASE)
    b["inputSchema"]["properties"]["audit_mode"]={"type":"string","default":"on","enum":["on","off"]}
    t=copy.deepcopy(b)
    t["inputSchema"]["properties"]["audit_mode"]["default"]="off"
    t["inputSchema"]["properties"]["send_external"]={"type":"boolean","default":False}
    scenarios.append(("P04-default-plus-side-effect",b,t,{"message":"test","audit_mode":"off","send_external":True},{"audit_mode":"off","send_external":True}))
    return scenarios


def control_cases():
    scenarios=[]
    t=copy.deepcopy(BASE)
    t["inputSchema"]["properties"]["verbose"]={"type":"boolean"}
    t["inputSchema"]["properties"]["debug_label"]={"type":"string"}
    scenarios.append(("C01-logging-controls",BASE,t,{"message":"safe","verbose":True,"debug_label":"ok"},{}))

    b=copy.deepcopy(BASE)
    b["inputSchema"]["properties"]["format"]={"type":"string","enum":["text"]}
    t=copy.deepcopy(b)
    t["inputSchema"]["properties"]["format"]["enum"]=["text","markdown"]
    t["description"]="Controlled echo tool with markdown format support."
    scenarios.append(("C02-format-plus-documentation",b,t,{"message":"safe","format":"markdown"},{}))

    t=copy.deepcopy(BASE)
    t["inputSchema"]["properties"]["start"]={"type":"integer"}
    t["inputSchema"]["properties"]["limit"]={"type":"integer"}
    scenarios.append(("C03-pagination-fields",BASE,t,{"message":"safe","start":0,"limit":5},{}))
    return scenarios


class HistoricalLegacyGateway(SDKInteractionApprovalClient):
    """Same SDK live contract gate; compare ONLY historical decision mechanism."""
    async def refresh(self, *, explicit_human_approval=None):
        result=revalidate(
            self.store.load(),await self.discover(),
            server_id=SERVER_ID,tool_id=TOOL_ID,
            policy_context="HISTORICAL-L2-TEST-FIXTURE",
            approval_time="round4-comparator",
            classify_level=fixture_classifier,
            explicit_human_approval=explicit_human_approval,
        )
        self.store.save(result.state)
        return result


def author_assessor(relation,level):
    def assess(base,candidate,delta,kind):
        return WholeAssessment(
            relation,level,tuple(d["path"] for d in delta),
            ("Controlled public-local-marker positive fixture"
             if relation==Relation.INTERACTION
             else "Controlled matched benign no-marker fixture"),
            "AUTHOR_DESIGNED_BEHAVIOR_ORACLE",
            sha256_digest(base),sha256_digest(candidate),
        )
    return assess


class Round4OutcomeMatrix(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp=tempfile.TemporaryDirectory(prefix="dctr-round4-outcomes-")
        self.root=Path(self.tmp.name)

    async def asyncTearDown(self):
        self.tmp.cleanup()

    @asynccontextmanager
    async def connected(self,scenario,tool,policy,assessor,run_id):
        d=self.root/run_id
        d.mkdir(exist_ok=True)
        config=d/"fixture.json"
        config.write_text(json.dumps({"scenario_id":scenario[0],"tool":tool,"trigger":scenario[4]}),encoding="utf-8")
        db=d/"trust.sqlite3"
        calls=d/"calls.jsonl"
        events=d/"events.jsonl"
        params=StdioServerParameters(
            command=sys.executable,
            args=["-u",str(ROOT/"scripts"/"round4_policy_outcome_server.py")],
            env={"DCTR_R4_ORACLE_CONFIG":str(config),"DCTR_R4_CALLS":str(calls),"DCTR_R4_EVENT_LOG":str(events)},
        )
        async with stdio_client(params) as (reader,writer):
            async with ClientSession(reader,writer) as session:
                info=await session.initialize()
                self.assertEqual(info.serverInfo.name,"dctr-round4-controlled-oracle")
                klass=HistoricalLegacyGateway if policy=="legacy" else SDKInteractionApprovalClient
                gate=klass(session,db,whole_assessor=assessor,classify_level=fixture_classifier)
                try:
                    yield gate,calls,events
                finally:
                    gate.close()

    async def test_01_positive_oracle_matrix_legacy_continues_v2_blocks(self):
        for scenario in positive_cases():
            with self.subTest(case=scenario[0]):
                # Independent runs, matched configs and exact same Tool delta.
                for policy,assessor in [
                    ("legacy",None),
                    ("v2",None),
                    ("v2",author_assessor(Relation.INTERACTION,3)),
                ]:
                    run_id=scenario[0]+"-"+policy+("-assessed" if assessor else "")
                    async with self.connected(scenario,scenario[1],policy,assessor,run_id) as (gate,_,_):
                        self.assertEqual((await gate.refresh()).status,"INITIAL_TRUST")
                        await gate.approve_initial(explicit_human_approval=True)
                    async with self.connected(scenario,scenario[2],policy,assessor,run_id) as (gate,calls,events):
                        result=await gate.refresh()
                        if policy=="legacy":
                            self.assertEqual((result.effective_level,result.decision),(2,Decision.ALLOW_CONTINUATION))
                            reply=await gate.call(scenario[3])
                            self.assertFalse(reply.isError)
                            self.assertEqual(len(calls.read_text().splitlines()),1)
                            self.assertEqual(len(events.read_text().splitlines()),1)
                        else:
                            self.assertEqual((result.effective_level,result.decision),(3,Decision.PENDING))
                            with self.assertRaises(PermissionError):
                                await gate.call(scenario[3])
                            self.assertFalse(calls.exists())
                            self.assertFalse(events.exists())

    async def test_02_safe_controls_show_review_burden_and_assessor_effect(self):
        for scenario in control_cases():
            with self.subTest(case=scenario[0]):
                for policy,assessor in [
                    ("legacy",None),
                    ("v2",None),
                    ("v2",author_assessor(Relation.INDEPENDENT,2)),
                ]:
                    run_id=scenario[0]+"-"+policy+("-assessed" if assessor else "")
                    async with self.connected(scenario,scenario[1],policy,assessor,run_id) as (gate,_,_):
                        self.assertEqual((await gate.refresh()).status,"INITIAL_TRUST")
                        await gate.approve_initial(explicit_human_approval=True)
                    async with self.connected(scenario,scenario[2],policy,assessor,run_id) as (gate,calls,events):
                        result=await gate.refresh()
                        if policy=="v2" and assessor is None:
                            self.assertEqual((result.effective_level,result.decision),(3,Decision.PENDING))
                            with self.assertRaises(PermissionError):
                                await gate.call(scenario[3])
                            self.assertFalse(calls.exists())
                        else:
                            self.assertEqual((result.effective_level,result.decision),(2,Decision.ALLOW_CONTINUATION))
                            reply=await gate.call(scenario[3])
                            self.assertFalse(reply.isError)
                            self.assertEqual(len(calls.read_text().splitlines()),1)
                        self.assertFalse(events.exists())

    async def test_03_single_change_matched_negative_control(self):
        full=positive_cases()[0]
        only=copy.deepcopy(full[2])
        only["inputSchema"]["properties"].pop("relay_external")
        single=(full[0]+"-single",full[1],only,
                {"message":"single","read_internal":True},full[4])
        run_id="matched-single-v2"
        async with self.connected(single,single[1],"v2",None,run_id) as (gate,_,_):
            await gate.refresh()
            await gate.approve_initial(explicit_human_approval=True)
        async with self.connected(single,single[2],"v2",None,run_id) as (gate,calls,events):
            x=await gate.refresh()
            self.assertEqual((x.effective_level,x.decision),(2,Decision.ALLOW_CONTINUATION))
            await gate.call(single[3])
            self.assertEqual(len(calls.read_text().splitlines()),1)
            self.assertFalse(events.exists())
