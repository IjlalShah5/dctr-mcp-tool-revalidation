#!/usr/bin/env python3
"""Direction-preserving recursive JSON differencer for DCTR."""

from __future__ import annotations

from typing import Any

ABSENT = {"__dctr_absent__": True}


def _path_join(base: str, key: str | int) -> str:
    return f"{base}/{key}" if base else f"/{key}"


def recursive_diff(before: Any, after: Any, path: str = "") -> list[dict[str, Any]]:
    out: list[dict[str, Any]] = []

    if isinstance(before, dict) and isinstance(after, dict):
        keys = sorted(set(before) | set(after))
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
        # Arrays are order-preserving contract values. Record an exact replacement
        # when their ordered content differs rather than treating them as sets.
        if before != after:
            out.append({"path": path or "/", "operation": "REPLACE", "before": before, "after": after})
        return out

    if before != after:
        out.append({"path": path or "/", "operation": "REPLACE", "before": before, "after": after})

    return out
