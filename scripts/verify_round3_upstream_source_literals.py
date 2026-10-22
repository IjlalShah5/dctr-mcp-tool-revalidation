#!/usr/bin/env python3
"""Reproduce source-literal MCP change audit at seven upstream immutable commits.

--offline validates registered study scope, commitments, and one source-derived
Tool projection. --online additionally retrieves 14 immutable upstream blobs,
verifies their Git SHA-1 and source-context markers. No L0--L4 labels, live
tools/list captures, or production behavior claims are generated.
"""
from __future__ import annotations

import argparse
import hashlib
import json
import re
import urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DATA = ROOT / "data" / "round3_screening"


def get_data(name: str) -> dict:
    return json.loads((DATA / name).read_text(encoding="utf-8"))


def jcs_digest_simple_contract(value: dict) -> str:
    """JCS-equivalent encoding for the controlled ASCII-only, number-free FS03 Tool."""
    if not isinstance(value, dict):
        raise TypeError("Tool must be a JSON object")
    serialized = json.dumps(value, ensure_ascii=False, sort_keys=True,
                            separators=(",", ":"), allow_nan=False)
    return hashlib.sha256(serialized.encode("utf-8")).hexdigest()


def extract_region(source: str, row: dict) -> str:
    case = row["id"]
    if case in {"FC01", "FC02"}:
        phrase = ("scrapeOptions fetches web pages, never Alexandria provider tools."
                  if case == "FC01"
                  else "can discover providers for the same fields across several pages; a matching provider")
        lines = [line for line in source.splitlines() if phrase in line]
        if len(lines) != 1:
            raise AssertionError(f"{case}: expected one pinned declaration line, got {len(lines)}")
        return lines[0]
    start, end = row["anchor"], row["end_anchor"]
    index = source.find(start)
    if index < 0 or source.find(start, index + 1) != -1:
        raise AssertionError(f"{case}: missing or duplicate Tool anchor")
    next_pos = source.find(end, index + len(start))
    if next_pos < 0:
        raise AssertionError(f"{case}: Tool declaration terminator missing")
    return source[index:next_pos]


def verify_markers(before: str, after: str, row: dict) -> None:
    case = row["id"]
    x, y = extract_region(before, row), extract_region(after, row)
    if x == y:
        raise AssertionError(f"{case}: source declaration did not change")
    if row["old_marker"] not in x or row["new_marker"] not in y:
        raise AssertionError(f"{case}: recorded before/after string not present")
    if row["new_marker"] in x:
        raise AssertionError(f"{case}: new marker already in old source")
    if case not in {"CD03", "FC02"} and row["old_marker"] in y:
        raise AssertionError(f"{case}: old marker remains in new source")
    if case == "CD01":
        for p in ("requestFilePath: zod", "responseFilePath: zod"):
            if p in x or p not in y:
                raise AssertionError("CD01: advertised source fields not added")


def upstream_blob(record: dict, stage: str) -> str:
    owner_repo = record["repository"]
    path = record["path"]
    commit = record[stage]
    url = f"https://raw.githubusercontent.com/{owner_repo}/{commit}/{path}"
    request = urllib.request.Request(
        url, headers={"User-Agent": "dctr-reproducibility-research/1.0",
                      "Accept": "text/plain"}
    )
    with urllib.request.urlopen(request, timeout=25) as response:
        raw = response.read(1_000_001)
    if len(raw) > 1_000_000:
        raise AssertionError(f"{record['id']}: unexpected large upstream source")
    sha = hashlib.sha1(f"blob {len(raw)}\0".encode("ascii") + raw).hexdigest()
    if sha != record[f"{stage}_blob_sha"]:
        raise AssertionError(f"{record['id']} {stage}: Git blob hash mismatch")
    return raw.decode("utf-8")


def validate_registered_data() -> tuple[list, dict]:
    payload = get_data("verified_upstream_literal_transitions.json")
    rows = payload["records"]
    if len(rows) != 7 or len({r["id"] for r in rows}) != 7:
        raise AssertionError("expected exactly 7 unique independent maintainer events")
    if len({r["repository"] for r in rows}) != 3:
        raise AssertionError("expected exactly 3 upstream repositories")
    if len({r["cluster_id"] for r in rows}) != 7:
        raise AssertionError("maintainer event identity collision")
    for row in rows:
        for k in ("before", "after", "before_blob_sha", "after_blob_sha"):
            if not re.fullmatch(r"[0-9a-f]{40}", row[k]):
                raise AssertionError(f"{row['id']}: invalid {k}")
        if row["severity_label"] is not None or row["source_level"] != "VERIFIED_SOURCE_LITERAL_ONLY":
            raise AssertionError("unverified human judgment or wire capture claim")

    fs = get_data("FS03_source_reconstructed_not_wire.json")
    if fs["source_case_id"] != "FS03" or "NOT_RUNTIME_WIRE" not in fs["derivation"]:
        raise AssertionError("FS03 projection incorrectly represented as wire capture")
    for stage in ("before", "after"):
        d = fs[f"{stage}_tool"]
        if sorted(d) != ["description", "inputSchema", "name"]:
            raise AssertionError("FS03 reconstructed Tool fields changed")
        if d["name"] != "list_allowed_directories":
            raise AssertionError("FS03 Tool identity changed")
        if d["inputSchema"] != {"type": "object", "properties": {}, "required": []}:
            raise AssertionError("FS03 input schema changed")
        if jcs_digest_simple_contract(d) != fs[f"{stage}_jcs_sha256"]:
            raise AssertionError("FS03 canonical source-projection hash does not match")
    if fs["changed_paths"] != ["/description"]:
        raise AssertionError("FS03 source-derived difference no longer one path")
    return rows, fs


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--online", action="store_true",
                        help="verify upstream contents from pinned Git commits")
    args = parser.parse_args()
    records, fs = validate_registered_data()
    print("Offline provenance audit PASSED: 7 maintainer events / 3 repositories; FS03 source projection JCS hashes")
    if not args.online:
        print("NOTE: upstream blobs not fetched; evidence is source-derived, no live tools/list capture")
        return
    for row in records:
        before = upstream_blob(row, "before")
        after = upstream_blob(row, "after")
        verify_markers(before, after, row)
        if row["id"] == "FS03":
            # Join the statically concatenated quoted description parts at each SHA.
            for stage, source in (("before", before), ("after", after)):
                excerpt = extract_region(source, row)
                declaration = excerpt.split("description:", 1)[1]
                raw_lits = re.findall(r'"(?:[^"\\]|\\.)*"', declaration)
                text = "".join(json.loads(part) for part in raw_lits)
                if text != fs[f"{stage}_tool"]["description"]:
                    raise AssertionError(f"FS03 {stage}: source-derived description mismatch")
        print(f"  {row['id']}: immutable before/after Git blob and change marker confirmed")
    print("Online upstream source-literal audit PASSED; still no human labels or MCP runtime wire observations")


if __name__ == "__main__":
    main()
