#!/usr/bin/env python3
"""Deterministic JSON canonicalization and SHA-256 hashing for DCTR."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any


def canonical_bytes(obj: Any) -> bytes:
    """Return deterministic UTF-8 JSON bytes.

    Object keys are recursively sorted by ``json.dumps`` while array order is
    preserved. Compact separators remove insignificant whitespace.
    """
    return json.dumps(
        obj,
        sort_keys=True,
        separators=(",", ":"),
        ensure_ascii=False,
        allow_nan=False,
    ).encode("utf-8")


def sha256_digest(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def load_json(path: str | Path) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)


def main() -> None:
    import argparse

    parser = argparse.ArgumentParser()
    parser.add_argument("json_file")
    args = parser.parse_args()
    obj = load_json(args.json_file)
    print(sha256_digest(obj))


if __name__ == "__main__":
    main()
