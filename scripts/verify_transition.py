#!/usr/bin/env python3
"""Verify reconstructed Tool contracts using DCTR evidence rules."""

from __future__ import annotations

import argparse
import json

from canonicalize import load_json, sha256_digest
from recursive_diff import recursive_diff


class DifferencingInconsistency(RuntimeError):
    """Fail-closed condition: digests differ but no exact delta was produced."""


def verify_objects(before, after) -> dict:
    h0 = sha256_digest(before)
    h1 = sha256_digest(after)

    if h0 == h1:
        return {
            "type": "STABLE",
            "before_hash": h0,
            "after_hash": h1,
            "delta": [],
        }

    delta = recursive_diff(before, after)
    if not delta:
        raise DifferencingInconsistency(
            "JCS canonical digests differ but recursive differencing produced no delta."
        )

    return {
        "type": "MUTATION",
        "before_hash": h0,
        "after_hash": h1,
        "delta": delta,
    }


def verify(before_path: str, after_path: str) -> dict:
    return verify_objects(load_json(before_path), load_json(after_path))


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
