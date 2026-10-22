#!/usr/bin/env python3
"""Verify NEW unlabeled natural candidate Tool-definition source snapshots.

These 20 cases / 43 paths / 14 maintainer clusters are RETROSPECTIVE,
PURPOSIVELY SCREENED, and NOT independently annotated severity outcomes.
"""
import csv
import json
from collections import Counter, defaultdict
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "round3_stage3_natural_candidates"
import sys
sys.path.insert(0, str(ROOT / "scripts"))

from recursive_diff import recursive_diff

def read_csv(filename):
    with (DATA / filename).open(newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

def main():
    rows, snapshots = [], []
    for i in range(1, 5):
        rows.extend(read_csv(f"batch{i}_path_units.csv"))
        with (DATA / f"batch{i}_full_contracts.jsonl").open(encoding="utf-8") as f:
            snapshots.extend(json.loads(line) for line in f if line.strip())

    assert (len(snapshots), len(rows)) == (20, 43), (
        "new candidate pool shape changed", len(snapshots), len(rows))
    assert len({r["unit_id"] for r in rows}) == 43
    assert len({r["case_id"] for r in rows}) == 20
    assert len({r["cluster_id"] for r in rows}) == 14
    assert {r["repo"] for r in rows} == {"github/github-mcp-server"}
    assert len({r["source_after_commit"] for r in rows}) == 14
    assert not any("level" in r or "rule" in r or "annotator" in r for r in rows), (
        "Candidate pool must remain UNLABELLED until independent returns are frozen"
    )
    by_case = defaultdict(list)
    for row in rows:
        by_case[row["case_id"]].append(row)

    case_counts = Counter()
    for s in snapshots:
        key = s["case_id"]
        assert key in by_case
        assert s["before_tool"]["name"] == s["tool"]
        assert s["after_tool"]["name"] == s["tool"]
        assert len(s["source_before_commit"]) == len(s["source_after_commit"]) == 40
        assert len(s["before_blob_sha"]) == len(s["after_blob_sha"]) == 40

        delta = recursive_diff(s["before_tool"], s["after_tool"])
        recorded = by_case[key]
        assert len(delta) == len(recorded), (key, len(delta), len(recorded))
        by_path = {d["path"]: d for d in delta}
        assert len(by_path) == len(delta), (key, "duplicate JSON Pointers")
        for row in recorded:
            path = row["path"]
            assert path in by_path and row["operation"] == by_path[path]["operation"], (
                key, path)
            calculated = by_path[path]
            for value_key, val in [
                ("before_json", calculated["before"]),
                ("after_json", calculated["after"]),
            ]:
                if row[value_key] == "ABSENT":
                    assert val == {"__dctr_absent__": True}, (key, path, value_key)
                else:
                    assert json.loads(row[value_key]) == val, (key, path, value_key)
            for field in (
                "case_id", "cluster_id", "repo", "tool", "snapshot_path",
                "source_before_commit", "source_after_commit",
                "before_blob_sha", "after_blob_sha", "source_url",
            ):
                assert row[field] == s[field], (key, field)
        case_counts[s["cluster_id"]] += 1

    assert len(case_counts) == 14
    assert sorted(case_counts.values()) == sorted([1] * 8 + [2] * 6), dict(case_counts)
    print("Round 3 new natural candidate source reconstruction: PASS")
    print("  20 Tool mutations, 43 exact changed paths, 14 maintainer clusters")
    print("  Single repository; 0 independent ratings; 0 natural L4 validation claims")
    print("  All changes reproduced against retained before/after .snap projections")

if __name__ == "__main__":
    main()
