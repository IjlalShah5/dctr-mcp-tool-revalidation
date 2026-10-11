#!/usr/bin/env python3
"""Verify primary contract hashes, complete path/TSV evidence and composition."""
from __future__ import annotations

import csv
import json
from collections import Counter
from pathlib import Path

from canonicalize import load_json, sha256_digest
from recursive_diff import recursive_diff, json_exact_equal

ROOT = Path(__file__).resolve().parents[1]
LEVEL = {"R0": "L0", "R1": "L1", "R2a": "L2", "R2b": "L2",
         "R3a": "L3", "R3b": "L3", "R3c": "L3", "R4": "L4"}
TSV_CATEGORICAL = (
    "capability_side_effect", "resource_scope", "privacy_default",
    "schema_constraint", "annotation_trust_hint",
)
TSV_SEMANTICS = "model_visible_semantics"
TSV_DECEPTION = "deception_concealment"


def read_csv(root: Path, filename: str):
    with (root / "data" / filename).open(encoding="utf-8", newline="") as handle:
        return list(csv.DictReader(handle))


def require(condition, message: str):
    if not condition:
        raise AssertionError(message)


def verify_primary_evidence(root: Path = ROOT) -> dict:
    transitions = read_csv(root, "transitions.csv")
    primaries = {r["mutation_id"]: r for r in read_csv(root, "primary_mutations.csv")}
    semantic_rows = read_csv(root, "primary_path_evidence.csv")
    semantic = {}
    for record in semantic_rows:
        key = (record["transition_id"], record["path"])
        require(key not in semantic, f"Duplicate author path label: {key}")
        semantic[key] = record

    observed = set()
    summary = {}
    require({r["transition_id"] for r in transitions} == {"P01","P02","P03","P04"},
            "Expected exactly four primary transitions")
    for event in transitions:
        tid = event["transition_id"]
        before = load_json(str(root / event["before_contract_path"]))
        after = load_json(str(root / event["after_contract_path"]))
        bh, ah = sha256_digest(before), sha256_digest(after)
        require(event["before_hash"] == bh and event["after_hash"] == ah,
                f"{tid}: stale canonical hash(es)")
        delta = recursive_diff(before, after)
        require(delta, f"{tid}: missing exact paths")
        paths = [d["path"] for d in delta]
        declared = [p.strip() for p in event["delta_path"].split(";") if p.strip()]
        require(set(paths) == set(declared) and len(paths) == len(declared),
                f"{tid}: transitions.csv path coverage mismatch")
        levels = []
        for d in delta:
            key = (tid, d["path"])
            require(key in semantic, f"{tid}: no TSV/rule/rationale for {d['path']}")
            record = semantic[key]
            observed.add(key)
            require(record["operation"] == d["operation"], f"{key}: operation mismatch")
            require(json_exact_equal(json.loads(record["before_json"]), d["before"]),
                    f"{key}: wrong before value")
            require(json_exact_equal(json.loads(record["after_json"]), d["after"]),
                    f"{key}: wrong after value")
            require(record["coding_status"] == "AUTHOR_DEVELOPMENT_REFERENCE",
                    f"{key}: development-set provenance missing")
            for dimension in TSV_CATEGORICAL:
                require(record[dimension] in {"NONE","BOUNDED","DECREASE","INCREASE","AMBIGUOUS","UNCERTAIN"},
                        f"{key}: bad TSV category {dimension}")
            require(record[TSV_SEMANTICS] in {"NONE","BENIGN","BOUNDED","MATERIAL","DECREASE","DECEPTIVE","UNCERTAIN"},
                    f"{key}: bad model-visible TSV category")
            require(record[TSV_DECEPTION] in {"NONE","PRESENT","UNCERTAIN"},
                    f"{key}: bad deception TSV category")
            require(record["primary_rule"] in LEVEL and
                    LEVEL[record["primary_rule"]] == record["minimum_level"],
                    f"{key}: rule/level mismatch")
            require(bool(record["rationale"].strip()), f"{key}: missing rationale")
            levels.append(int(record["minimum_level"][1:]))
        effective = "L" + str(max(levels))
        require(primaries[tid]["dctr_level"] == effective,
                f"{tid}: maximum path-level composition mismatch")
        summary[tid] = {"paths": paths, "level": effective, "before_hash": bh, "after_hash": ah}
    require(observed == set(semantic), f"Unmatched TSV rows: {set(semantic) - observed}")
    require(summary["P02"]["after_hash"] == summary["P03"]["before_hash"],
            "P02 after must match P03 before")
    return {"transitions": len(summary), "path_units": len(observed), "by_transition": summary}


if __name__ == "__main__":
    outcome = verify_primary_evidence()
    print(f"Verified {outcome['transitions']} primary transitions and "
          f"{outcome['path_units']} exact path/TSV/rule/rationale records.")
