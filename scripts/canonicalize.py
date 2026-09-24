#!/usr/bin/env python3
"""RFC 8785/JCS canonicalization and SHA-256 hashing for DCTR."""

from __future__ import annotations

import hashlib
import json
from pathlib import Path
from typing import Any

import rfc8785


def canonical_bytes(obj: Any) -> bytes:
    """Return RFC 8785/JCS canonical UTF-8 bytes.

    Consequences relevant to DCTR:
    * Boolean values remain distinct from JSON numbers.
    * 1 and 1.0 canonicalize to the same JSON number representation.
    * -0.0 and 0 canonicalize to the same JSON number representation.
    * object properties follow the deterministic RFC 8785 ordering.
    """
    return rfc8785.dumps(obj)


def sha256_digest(obj: Any) -> str:
    return hashlib.sha256(canonical_bytes(obj)).hexdigest()


def load_json(path: str | Path) -> Any:
    with open(path, "r", encoding="utf-8") as fh:
        return json.load(fh)
