#!/usr/bin/env python3
"""Verify two reconstructed Tool contracts using DCTR evidence rules."""

from __future__ import annotations

import argparse
import json

from canonicalize import load_json, sha256_digest
from recursive_diff import recursive_diff


def verify(before_path: str, after_path: str) -> dict:
    before = load_json(before_path)
    after = load_json(after_path)
    h0 = sha256_digest(before)
    h1 = sha256_digest(after)
    if h0 == h1:
        return {"type": "STABLE", "before_hash": h0, "after_hash": h1, "delta": []}
    return {
        "type": "MUTATION",
        "before_hash": h0,
        "after_hash": h1,
        "delta": recursive_diff(before, after),
    }


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("before")
    parser.add_argument("after")
    parser.add_argument("--output")
    args = parser.parse_args()
    result = verify(args.before, args.after)
    payload = json.dumps(result, ensure_ascii=False, indent=2)
    if args.output:
        with open(args.output, "w", encoding="utf-8") as fh:
            fh.write(payload + "\n")
    else:
        print(payload)


if __name__ == "__main__":
    main()
