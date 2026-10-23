"""Synthetic model regression tests, not independent risk measurements."""
import sys
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from round4_interaction_stress import run

class InteractionStressTests(unittest.TestCase):
    def test_exhaustive_case_counts(self):
        result=run()
        self.assertEqual(result["total_combinations"],16)
        self.assertEqual(result["changed_contract_combinations"],13)

    def test_guard_vs_per_path_and_over_escalation(self):
        s=run()["summary"]
        self.assertEqual(s["per_path_max"]["unblocked_compound_effect_cases"],2)
        self.assertEqual(s["known_pairwise_guard"]["unblocked_compound_effect_cases"],1)
        self.assertEqual(s["conservative_two_or_more"]["unblocked_compound_effect_cases"],0)
        self.assertEqual(s["conservative_two_or_more"]["benign_combinations_escalated"],4)

    def test_single_path_never_triggers_compound_or_extra_review(self):
        for case in run()["cases"]:
            if len(case["active"])==1:
                self.assertFalse(case["test_only_compound_effect"])
                self.assertTrue(all(level<=2 for level in case["policy_levels"].values()))
