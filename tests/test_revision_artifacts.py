import csv
import unittest
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

def read_csv(name):
    with (ROOT / "data" / name).open(encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))

class RevisionArtifactTests(unittest.TestCase):
    def test_supplementary_counts(self):
        rows = read_csv("supplementary_natural_mutations.csv")
        clusters = read_csv("supplementary_mutation_clusters.csv")
        self.assertEqual(len(rows), 32)
        self.assertEqual(len(clusters), 10)
        self.assertEqual(len({r["mutation_id"] for r in rows}), 32)
        counts = Counter(r["cluster_id"] for r in rows)
        for c in clusters:
            self.assertEqual(counts[c["cluster_id"]], int(c["event_count"]))

    def test_all_36_comparison(self):
        rows = read_csv("baseline_comparison_36.csv")
        self.assertEqual(len(rows), 36)
        self.assertTrue(all(r["etdi_style"] == "EXPLICIT_REAPPROVAL" for r in rows))

    def test_runtime_subset(self):
        rows = read_csv("runtime_alignment_matrix.csv")
        self.assertEqual(len(rows), 3)
        self.assertTrue(all(r["alignment"] == "aligned" for r in rows))

    def test_heldout_index(self):
        rows = read_csv("heldout_annotation_unit_index.csv")
        self.assertEqual(len(rows), 34)
        self.assertEqual(len({r["mutation_id"] for r in rows}), 32)
        self.assertEqual(len({r["cluster_id"] for r in rows}), 10)
        self.assertEqual(len({r["pattern_group"] for r in rows}), 15)

if __name__ == "__main__":
    unittest.main(verbosity=2)
