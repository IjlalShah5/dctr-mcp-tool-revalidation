#!/usr/bin/env python3
"""Verify blinded Round 3 Stage3N independent blank coding packets.

No severity reference outputs or independently completed ratings are supplied.
"""
from __future__ import annotations
import csv
from pathlib import Path

DATA = Path(__file__).resolve().parents[1] / "data" / "round3_stage3_natural_candidates"
FIXED_FIELDS = [
    "Match_Key","Tool_Name","Exact_JSON_Pointer","Operation","Before_JSON",
    "After_JSON","Full_Before_Tool_JSON","Full_After_Tool_JSON","Evidence_Origin",
]
RESPONSE_FIELDS = [
    "TSV_Capability","TSV_Resource_Scope","TSV_Privacy","TSV_Schema",
    "TSV_Annotations","TSV_Model_Semantics","TSV_Deception","Strongest_R",
    "Minimum_L","Confidence_1to5","Evidence_Rationale","Uncertainty",
]

def sheet(who):
    f = DATA / f"Stage3N_Annotator_{who}_UNFILLED_43_Paths.csv"
    with f.open("r", encoding="utf-8", newline="") as h:
        return list(csv.DictReader(h))

def main():
    a, b = sheet("A"), sheet("B")
    assert len(a) == len(b) == 43
    assert all(r["Blinded_ID"].startswith("AN") for r in a)
    assert all(r["Blinded_ID"].startswith("BN") for r in b)
    for rows in (a, b):
        assert len(set(r["Match_Key"] for r in rows)) == 43
        assert all(all(not r[col] for col in RESPONSE_FIELDS) for r in rows)
        assert all(r["Evidence_Origin"] == "SOURCE_SNAPSHOT_NOT_MCP_WIRE" for r in rows)
        assert all(r["Full_Before_Tool_JSON"] and r["Full_After_Tool_JSON"] for r in rows)
    keys_a = [r["Match_Key"] for r in a]
    keys_b = [r["Match_Key"] for r in b]
    assert set(keys_a) == set(keys_b)
    assert keys_a != keys_b, "Must be independently ordered to reduce order cues"
    pair = {r["Match_Key"]: r for r in b}
    for r in a:
        match = pair[r["Match_Key"]]
        assert all(r[k] == match[k] for k in FIXED_FIELDS)
    print("Round 3 Stage3N A/B blind coding packets verified: 43 each, 22 columns")
    print("  Same source evidence; different orders; all 12 response cells blank")
    print("  0 severity labels, 0 independent classification claims")

if __name__ == "__main__":
    main()
