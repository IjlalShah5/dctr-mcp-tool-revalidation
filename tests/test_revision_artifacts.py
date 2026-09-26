import csv
import json
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
        supplementary = [r for r in rows if not r["mutation_id"].startswith("P0")]
        self.assertEqual(len(supplementary), 32)
        self.assertTrue(all(r["dctr_status"].startswith("HELD_OUT_CONSENSUS_") for r in supplementary))
        self.assertFalse(any("PENDING" in r["dctr_status"] for r in rows))

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

    def test_final_heldout_path_units(self):
        rows = read_csv("heldout_annotation_final_path_units.csv")
        self.assertEqual(len(rows), 34)
        self.assertEqual(len({r["mutation_id"] for r in rows}), 32)
        self.assertEqual(Counter(r["final_level"] for r in rows), Counter({"L2": 19, "L1": 13, "L3": 1, "L0": 1}))
        self.assertEqual(sum(r["resolution"] == "A+B consensus" for r in rows), 6)

    def test_final_heldout_mutations(self):
        rows = read_csv("heldout_annotation_final_mutations.csv")
        self.assertEqual(len(rows), 32)
        self.assertEqual(Counter(r["final_level"] for r in rows), Counter({"L2": 18, "L1": 13, "L3": 1}))

    def test_annotation_metrics(self):
        with (ROOT / "data" / "heldout_annotation_metrics.json").open(encoding="utf-8") as fh:
            metrics = json.load(fh)
        self.assertEqual(metrics["heldout_path_units"], 34)
        self.assertEqual(metrics["pre_adjudication_agreed_units"], 28)
        self.assertEqual(metrics["pre_adjudication_disagreements"], 6)
        self.assertAlmostEqual(metrics["pre_adjudication_exact_agreement"], 28 / 34)
        self.assertAlmostEqual(metrics["linear_weighted_cohen_kappa"], 0.7197802197802198)
        self.assertAlmostEqual(metrics["ordinal_krippendorff_alpha"], 0.7635294117647059)


if __name__ == "__main__":
    unittest.main(verbosity=2)
