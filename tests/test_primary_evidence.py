"""Regression tests for primary contract-annotation completeness."""
from __future__ import annotations

import csv
import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from verify_primary_evidence import verify_primary_evidence


class PrimaryEvidenceTests(unittest.TestCase):
    def test_all_primary_evidence_is_complete_and_composes(self):
        result = verify_primary_evidence()
        self.assertEqual(result["transitions"], 4)
        self.assertEqual(result["path_units"], 12)
        self.assertEqual({k: v["level"] for k, v in result["by_transition"].items()},
                         {"P01":"L3","P02":"L2","P03":"L2","P04":"L2"})

    def test_required_set_changes_are_retained(self):
        result = verify_primary_evidence()["by_transition"]
        self.assertIn("/inputSchema/required", result["P02"]["paths"])
        self.assertIn("/inputSchema/required", result["P03"]["paths"])
        self.assertEqual(len(result["P02"]["paths"]), 2)
        self.assertEqual(len(result["P03"]["paths"]), 5)


if __name__ == "__main__":
    unittest.main(verbosity=2)
