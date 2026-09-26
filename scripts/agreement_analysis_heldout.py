#!/usr/bin/env python3
from __future__ import annotations

import argparse
import csv
import math
from collections import defaultdict

LEVELS = ["L0", "L1", "L2", "L3", "L4"]
LEVEL_NUM = {level: i for i, level in enumerate(LEVELS)}

def read_csv(path):
    with open(path, encoding="utf-8", newline="") as fh:
        return list(csv.DictReader(fh))

def weighted_kappa(values):
    values = [(LEVEL_NUM[a], LEVEL_NUM[b]) for a, b in values if a in LEVEL_NUM and b in LEVEL_NUM]
    if not values:
        return float("nan")
    k = len(LEVELS)
    n = len(values)
    observed = [[0.0] * k for _ in range(k)]
    row = [0] * k
    col = [0] * k
    for a, b in values:
        observed[a][b] += 1 / n
        row[a] += 1
        col[b] += 1
    expected = [[(row[i] / n) * (col[j] / n) for j in range(k)] for i in range(k)]
    def weight(i, j):
        return abs(i - j) / (k - 1)
    num = sum(weight(i,j) * observed[i][j] for i in range(k) for j in range(k))
    den = sum(weight(i,j) * expected[i][j] for i in range(k) for j in range(k))
    return float("nan") if math.isclose(den, 0) else 1 - num / den

def ordinal_alpha(values):
    values = [(LEVEL_NUM[a], LEVEL_NUM[b]) for a, b in values if a in LEVEL_NUM and b in LEVEL_NUM]
    if not values:
        return float("nan")
    k = len(LEVELS)
    observed = sum(((a-b)/(k-1))**2 for a,b in values) / len(values)
    pooled = [x for pair in values for x in pair]
    n = len(pooled)
    if n < 2:
        return float("nan")
    expected = 0.0
    for i, a in enumerate(pooled):
        for j, b in enumerate(pooled):
            if i != j:
                expected += ((a-b)/(k-1))**2
    expected /= n * (n - 1)
    return float("nan") if math.isclose(expected, 0) else 1 - observed / expected

def raw_agreement(values):
    return sum(a == b for a,b in values) / len(values) if values else float("nan")

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("annotator_a")
    ap.add_argument("annotator_b")
    ap.add_argument("--mapping", default="data/heldout_annotation_unit_index.csv")
    args = ap.parse_args()

    A = {r["unit_id"]: r for r in read_csv(args.annotator_a)}
    B = {r["unit_id"]: r for r in read_csv(args.annotator_b)}
    M = {r["unit_id"]: r for r in read_csv(args.mapping)}
    ids = sorted(set(A) & set(B) & set(M))

    usable = [
        (A[u].get("minimum_level",""), B[u].get("minimum_level",""))
        for u in ids
        if A[u].get("minimum_level") not in {"", "UNCERTAIN"}
        and B[u].get("minimum_level") not in {"", "UNCERTAIN"}
    ]

    by_cluster = defaultdict(list)
    by_pattern = defaultdict(list)
    for u in ids:
        a = A[u].get("minimum_level","")
        b = B[u].get("minimum_level","")
        if a and b:
            by_cluster[M[u]["cluster_id"]].append((a,b))
            by_pattern[M[u]["pattern_group"]].append((a,b))

    cluster_macro = sum(raw_agreement(v) for v in by_cluster.values()) / len(by_cluster)
    pattern_macro = sum(raw_agreement(v) for v in by_pattern.values()) / len(by_pattern)

    print(f"heldout_units={len(ids)}")
    print(f"raw_agreement={raw_agreement(usable):.6f}")
    print(f"linear_weighted_cohen_kappa={weighted_kappa(usable):.6f}")
    print(f"ordinal_krippendorff_alpha={ordinal_alpha(usable):.6f}")
    print(f"cluster_macro_raw_agreement={cluster_macro:.6f}")
    print(f"pattern_macro_raw_agreement={pattern_macro:.6f}")
    print(f"clusters={len(by_cluster)}")
    print(f"patterns={len(by_pattern)}")

if __name__ == "__main__":
    main()
