"""Engineering tests only: mock ratings are NOT independent expert data."""
import csv
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/"scripts"))
from round4_independent_boundary_analysis import analyze,read_frozen_ratings

def row(uid,cluster,a,b,repo="synthetic"):
    return {"unit_id":uid,"cluster_id":cluster,"repository":repo,"rater_a_level":a,"rater_b_level":b}

class BoundaryAnalyzerTests(unittest.TestCase):
    def test_perfect_agreement(self):
        report=analyze([row("a","c1","L0","L0"),row("b","c2","L4","L4")],reps=30)
        self.assertEqual(report["linear_weighted_cohen_kappa"],1.0)
        self.assertEqual(report["l4_jointly_labeled_clusters"],1)

    def test_undefined_kappa_stays_undefined(self):
        report=analyze([row("a","c1","L2","L2"),row("b","c2","L2","L2")],reps=30)
        self.assertIsNone(report["linear_weighted_cohen_kappa"])
        self.assertIsNone(report["cluster_bootstrap_kappa"]["interval_95"])

    def test_adjacent_boundary_disagreement_and_cluster_counts(self):
        r=analyze([row("a","c1","L3","L4"),row("b","c1","L2","L3"),
                   row("c","c2","L4","L4"),row("d","c3","L3","L3")],reps=100)
        self.assertEqual(r["critical_boundary_disagreements"]["L3/L4"],1)
        self.assertEqual(r["critical_boundary_disagreements"]["L2/L3"],1)
        self.assertEqual(r["repository_cluster_count"],3)
        self.assertEqual(r["l4_jointly_labeled_clusters"],1)

    def test_one_cluster_never_gives_precision_interval(self):
        r=analyze([row("a","c1","L1","L2")],reps=30)
        self.assertIsNone(r["cluster_bootstrap_kappa"]["interval_95"])

    def test_incomplete_and_duplicate_ratings_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            p=Path(directory)/"mock.csv"
            fields=["unit_id","cluster_id","repository","rater_a_level","rater_b_level"]
            with p.open("w",newline="",encoding="utf-8") as f:
                w=csv.DictWriter(f,fieldnames=fields)
                w.writeheader()
                w.writerow(row("a","c1","L2",""))
            with self.assertRaisesRegex(ValueError,"both frozen"):
                read_frozen_ratings(p)
            with p.open("w",newline="",encoding="utf-8") as f:
                w=csv.DictWriter(f,fieldnames=fields)
                w.writeheader()
                w.writerow(row("a","c1","L2","L2"))
                w.writerow(row("a","c1","L2","L2"))
            with self.assertRaisesRegex(ValueError,"duplicate"):
                read_frozen_ratings(p)

if __name__=="__main__":
    unittest.main()
