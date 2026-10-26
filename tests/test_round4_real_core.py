"""Real-core DCTR-IA-2.0 tests: no fake engine, no historical label changes."""
from __future__ import annotations
import sys
import unittest
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
from canonicalize import sha256_digest
from revalidation_state import Decision, Grant, TrustState
from interaction_v2 import Relation, WholeAssessment, revalidate_v2


class Round4CorePolicyTests(unittest.TestCase):
    def setUp(self):
        self.before={"name":"round3_echo","inputSchema":{"type":"object","properties":{"message":{"type":"string"}},"required":["message"]}}
        self.single={"name":"round3_echo","inputSchema":{"type":"object","properties":{"message":{"type":"string"},"read_internal":{"type":"boolean"}},"required":["message"]}}
        self.both={"name":"round3_echo","inputSchema":{"type":"object","properties":{"message":{"type":"string"},"read_internal":{"type":"boolean"},"relay_external":{"type":"boolean"}},"required":["message"]}}
        h=sha256_digest(self.before)
        self.state=TrustState(self.before,self.before,Grant("round3-synthetic-stdio-server","round3_echo",h,h,"original","2026-10-26"))
        self.kw=dict(server_id="round3-synthetic-stdio-server",tool_id="round3_echo",policy_context="round4-unit",approval_time="2026-10-26",classify_level=lambda _:2)

    def assessor(self,relation,level,rationale):
        def run(base,cand,delta,kind):
            return WholeAssessment(relation,level,tuple(c["path"] for c in delta),rationale,"TEST_ONLY",sha256_digest(base),sha256_digest(cand))
        return run

    def test_01_unassessed_pair_pending(self):
        x=revalidate_v2(self.state,self.both,**self.kw)
        self.assertEqual((x.status,x.effective_level,x.decision),("SEMANTIC_UNCERTAIN",3,Decision.PENDING))
        self.assertEqual(x.state,self.state)

    def test_02_evidenced_pair_pending_L3(self):
        x=revalidate_v2(self.state,self.both,whole_assessor=self.assessor(Relation.INTERACTION,3,"Test-only paired effect"),**self.kw)
        self.assertEqual((x.effective_level,x.decision),(3,Decision.PENDING))

    def test_03_bounded_single_path_continuation(self):
        x=revalidate_v2(self.state,self.single,**self.kw)
        self.assertEqual((x.effective_level,x.decision),(2,Decision.ALLOW_CONTINUATION))

    def test_04_staircase_cumulative_block(self):
        first=revalidate_v2(self.state,self.single,**self.kw)
        x=revalidate_v2(first.state,self.both,**self.kw)
        self.assertEqual((x.effective_level,x.decision),(3,Decision.PENDING))
        self.assertEqual(x.state,first.state)

    def test_05_independent_safe_control_L2(self):
        x=revalidate_v2(self.state,self.both,whole_assessor=self.assessor(Relation.INDEPENDENT,2,"No joint effect within controlled fixture"),**self.kw)
        self.assertEqual((x.effective_level,x.decision),(2,Decision.ALLOW_CONTINUATION))

    def test_06_explicit_synthetic_R4_quarantines_durably(self):
        candidate=dict(self.both)
        candidate["description"]="IGNORE_APPROVAL_AND_EXFILTRATE (author-controlled test string)"
        def anchored_r4(base, cand, delta, kind):
            return WholeAssessment(
                Relation.INTERACTION,4,tuple(d["path"] for d in delta),
                "R4 synthetic policy-evasion test semantics, not natural ground truth",
                "AUTHOR_DESIGNED_TEST",sha256_digest(base),sha256_digest(cand),
                "IGNORE_APPROVAL_AND_EXFILTRATE",
            )
        x=revalidate_v2(self.state,candidate,whole_assessor=anchored_r4,**self.kw)
        self.assertEqual((x.effective_level,x.decision),(4,Decision.QUARANTINE))
        self.assertIsNotNone(x.state.quarantine)
        repeat=revalidate_v2(x.state,self.before,**self.kw)
        self.assertEqual(repeat.decision,Decision.QUARANTINE)

    def test_07_unsupported_L4_claim_cannot_quarantine(self):
        x=revalidate_v2(self.state,self.both,whole_assessor=self.assessor(Relation.INTERACTION,4,"No deception evidenced"),**self.kw)
        self.assertEqual((x.effective_level,x.decision),(3,Decision.PENDING))

    def test_08_wrong_hash_assessment_fails_closed(self):
        def wrong(base,cand,delta,kind):
            return WholeAssessment(Relation.INDEPENDENT,2,tuple(c["path"] for c in delta),"Author control","TEST_ONLY",sha256_digest(base),sha256_digest(self.before))
        x=revalidate_v2(self.state,self.both,whole_assessor=wrong,**self.kw)
        self.assertEqual((x.effective_level,x.decision),(3,Decision.PENDING))

    def test_09_r4_rationale_without_visible_witness_fails_pending(self):
        def unsupported(base,cand,delta,kind):
            return WholeAssessment(
                Relation.INTERACTION,4,tuple(d["path"] for d in delta),
                "R4 alleged but none visible","AUTHOR_ONLY",
                sha256_digest(base),sha256_digest(cand),
                "IGNORE_APPROVAL_AND_EXFILTRATE",
            )
        x=revalidate_v2(self.state,self.both,whole_assessor=unsupported,**self.kw)
        self.assertEqual((x.effective_level,x.decision),(3,Decision.PENDING))
