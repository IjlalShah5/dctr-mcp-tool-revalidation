#!/usr/bin/env python3
"""Recompute Round-3 public pilot label agreement; no external dependencies."""
from __future__ import annotations

import csv
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "round3_pilot"


def load(name):
    with (DATA / name).open("r", encoding="utf-8-sig", newline="") as f:
        return list(csv.DictReader(f))


def weighted_kappa(a, b):
    n = len(a)
    weight = lambda i, j: 1 - abs(i - j) / 4
    po = sum(weight(i, j) for i, j in zip(a, b)) / n
    ca, cb = Counter(a), Counter(b)
    pe = sum(ca[i] * cb[j] * weight(i, j)
             for i in range(5) for j in range(5)) / (n * n)
    return (po - pe) / (1 - pe)


def ordinal_alpha(a, b):
    # True Krippendorff ordinal distance, using pooled category frequencies.
    pool = Counter(a + b)
    n = 2 * len(a)

    def distance(i, j):
        if i == j:
            return 0
        low, high = sorted((i, j))
        return (.5 * pool[low] + sum(pool[k] for k in range(low + 1, high))
                + .5 * pool[high]) ** 2

    observed = sum(distance(i, j) for i, j in zip(a, b)) / len(a)
    expected = sum(pool[i] * pool[j] * distance(i, j)
                   for i in range(5) for j in range(5)) / (n * (n - 1))
    return 1 - observed / expected


def main():
    rows = load("DCTR_Round3_Adjudicated_21_Path_Units_ANONYMIZED.csv")
    consensus = load("DCTR_Round3_Three_Joint_Consensus_Decisions_ANONYMIZED.csv")
    screens = load("DCTR_Round3_Stage2_Exploratory_Interaction_Responses_ANONYMIZED.csv")
    source = load("upstream_immutable_snapshot_manifest.csv")
    assert (len(rows), len(consensus), len(screens), len(source)) == (21, 3, 3, 10)
    assert len({r["unit_key"] for r in rows}) == 21
    assert len({r["case_id"] for r in rows}) == 10
    assert len({r["cluster_id"] for r in rows}) == 4
    assert {r["repository"] for r in rows} == {"github/github-mcp-server"}
    a = [int(r["a_level"][1:]) for r in rows]
    b = [int(r["b_level"][1:]) for r in rows]
    agreement = sum(i == j for i, j in zip(a, b))
    assert agreement == 18
    kappa, alpha = weighted_kappa(a, b), ordinal_alpha(a, b)
    assert abs(kappa - 0.8767123287671234) < 1e-12
    assert abs(alpha - 0.9027133260592357) < 1e-12
    dist = Counter(r["final_level"] for r in rows)
    assert dist == {"L0": 5, "L1": 2, "L2": 10, "L3": 4}
    disagreements = {r["unit_key"] for r in rows if r["a_level"] != r["b_level"]}
    assert disagreements == {r["unit_key"] for r in consensus}
    lookup = {r["unit_key"]: r for r in rows}
    for c in consensus:
        x = lookup[c["unit_key"]]
        assert (x["final_rule"], x["final_level"]) == (c["consensus_rule"], c["consensus_level"])
    assert {r["cluster_id"] for r in rows if r["final_level"] == "L3"} == {"GHC-20260812"}
    maximum = {}
    for r in rows:
        maximum[r["case_id"]] = max(maximum.get(r["case_id"], 0),
                                    int(r["final_level"][1:]))
    assert Counter(maximum.values()) == {0: 5, 1: 1, 2: 1, 3: 3}
    for r in screens:
        assert r["annotator_a_interaction"] == "YES"
        assert r["annotator_b_interaction"] == "YES"
        assert r["supporting_path_set_equal"] == "YES"
        assert r["case_id"] in {"N07", "N08", "N09"}
    print("Round 3 anonymized public pilot: all checks PASSED")
    print(f"  21 paths, 10 mutations, 4 change clusters; {agreement}/21 raw agreement")
    print(f"  Weighted kappa={kappa:.6f}; ordinal alpha={alpha:.6f}")
    print("  Final path levels:", dict(sorted(dist.items())))
    print("  3 independent disagreements resolved; 3/3 interaction screens YES")
    print("  Scope: one repository, all L3 in one cluster, no natural L4")


if __name__ == "__main__":
    main()
