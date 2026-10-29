"""Unlabeled natural maintainer snapshot replay of the V2 *mechanism*.

The 20 paired Tool snapshots are not independently rated high-severity events,
nor observed MCP wire traffic. A hypothetical all-L2 fixture mapper is used
only to isolate policy behavior; these outputs are NOT human annotations.
"""
from __future__ import annotations

import json
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from canonicalize import sha256_digest
from recursive_diff import recursive_diff
from revalidation_state import Decision,Grant,TrustState
from interaction_v2 import needs_whole_assessment,revalidate_v2

DATA=ROOT/"data"/"round3_stage3_natural_candidates"


class Round4NaturalSnapshotReplay(unittest.TestCase):
    def cases(self):
        for n in range(1,5):
            for line in (DATA/f"batch{n}_full_contracts.jsonl").read_text(encoding="utf-8").splitlines():
                if line.strip():
                    yield json.loads(line)

    def test_01_all_twenty_maintainer_snapshot_pairs_pass_through_whole_gate(self):
        n=0
        clusters=set()
        multi=0
        single=0
        path_count=0
        for item in self.cases():
            n+=1
            clusters.add(item["cluster_id"])
            before,after=item["before_tool"],item["after_tool"]
            delta=recursive_diff(before,after)
            self.assertTrue(delta,item["case_id"])
            path_count+=len(delta)
            digest=sha256_digest(before)
            state=TrustState(before,before,Grant("natural-replay",item["tool"],digest,digest,"hypothetical-test","2026-10-26"))
            out=revalidate_v2(
                state,after,server_id="natural-replay",tool_id=item["tool"],
                policy_context="UNLABELED-NATURAL-SNAPSHOT-REPLAY",
                approval_time="2026-10-26",classify_level=lambda _:2,
            )
            if needs_whole_assessment(delta):
                multi+=1
                self.assertEqual((out.status,out.decision),("SEMANTIC_UNCERTAIN",Decision.PENDING),item["case_id"])
                self.assertEqual(out.state,state,item["case_id"])
            else:
                single+=1
                self.assertEqual(out.decision,Decision.ALLOW_CONTINUATION,item["case_id"])
        self.assertEqual((n,len(clusters),path_count),(20,14,43))
        self.assertGreater(multi,0)
        self.assertGreater(single,0)

    def test_02_replay_does_not_manufacture_L4_quarantine_labels(self):
        for item in self.cases():
            before,after=item["before_tool"],item["after_tool"]
            h=sha256_digest(before)
            state=TrustState(before,before,Grant("natural-replay",item["tool"],h,h,"hypothetical-test","2026-10-26"))
            out=revalidate_v2(
                state,after,server_id="natural-replay",tool_id=item["tool"],
                policy_context="UNLABELED",approval_time="2026-10-26",
                classify_level=lambda _:2,
            )
            self.assertNotEqual(out.decision,Decision.QUARANTINE,item["case_id"])
