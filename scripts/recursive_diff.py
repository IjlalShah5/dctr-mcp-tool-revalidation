#!/usr/bin/env python3
"""JCS-consistent, direction-preserving recursive JSON differencer for DCTR."""

from __future__ import annotations

from typing import Any

from canonicalize import canonical_bytes

ABSENT = {"__dctr_absent__": True}


def _escape_json_pointer_segment(segment: str | int) -> str:
    return str(segment).replace("~", "~0").replace("/", "~1")


def _path_join(base: str, key: str | int) -> str:
    seg = _escape_json_pointer_segment(key)
    return f"{base}/{seg}" if base else f"/{seg}"


def _is_number(value: Any) -> bool:
    # bool is deliberately excluded even though Python bool subclasses int.
    return isinstance(value, (int, float)) and not isinstance(value, bool)


def json_exact_equal(before: Any, after: Any) -> bool:
    """Equality aligned with the canonical JSON data model used by JCS."""
    if _is_number(before) and _is_number(after):
        return canonical_bytes(before) == canonical_bytes(after)

    if type(before) is not type(after):
        return False

    if isinstance(before, dict):
        return (
            set(before.keys()) == set(after.keys())
            and all(json_exact_equal(before[k], after[k]) for k in before)
        )

    if isinstance(before, list):
        return (
            len(before) == len(after)
            and all(json_exact_equal(b, a) for b, a in zip(before, after))
        )

    return before == after


def recursive_diff(before: Any, after: Any, path: str = "") -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    if isinstance(before, dict) and isinstance(after, dict):
        keys = sorted(set(before) | set(after), key=lambda x: str(x))
        for key in keys:
            p = _path_join(path, key)
            if key not in before:
                out.append({"path": p, "operation": "ADD", "before": ABSENT, "after": after[key]})
            elif key not in after:
                out.append({"path": p, "operation": "REMOVE", "before": before[key], "after": ABSENT})
            else:
                out.extend(recursive_diff(before[key], after[key], p))
        return out

    if isinstance(before, list) and isinstance(after, list):
        if not json_exact_equal(before, after):
            out.append({"path": path or "/", "operation": "REPLACE", "before": before, "after": after})
        return out

    if not json_exact_equal(before, after):
        out.append({"path": path or "/", "operation": "REPLACE", "before": before, "after": after})

    return out
