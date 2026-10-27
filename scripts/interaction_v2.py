#!/usr/bin/env python3
"""DCTR-IA-2.0: prospective whole-contract approval-continuity policy.

Versioned extension of the frozen historical DCTR-CB-1.0 model; never alters
original path-level labels, denominators or the legacy revalidate() function.
Absent/uncertain whole assessment causes PENDING L3 *review action*, not a
claimed independently validated L3 semantic ground-truth classification.
"""
from __future__ import annotations

import re
from dataclasses import dataclass
from enum import Enum
from typing import Any, Callable, Mapping, Optional, Sequence

POLICY_VERSION = "DCTR-IA-2.0-EXPERIMENTAL"


class Relation(str, Enum):
    INDEPENDENT = "INDEPENDENT"
    BOUNDED_INTERACTION = "BOUNDED_INTERACTION"  # related effects, no higher approval action evidenced
    INTERACTION = "INTERACTION"  # material escalation requiring L3+
    UNCERTAIN = "UNCERTAIN"


@dataclass(frozen=True)
class WholeAssessment:
    relation: Relation
    level: Optional[int]
    evidence_paths: tuple[str, ...]
    rationale: str
    evidence_origin: str = "EXPERT_OR_CONTROLLED_OBSERVATION"
    baseline_jcs_sha256: str = ""
    candidate_jcs_sha256: str = ""
    r4_client_visible_witness: str = ""  # Exact substring in a changed after-value


class UnresolvedWholeContract(Exception):
    pass


def _paths(delta: Sequence[Mapping[str, Any]]) -> tuple[str, ...]:
    paths = []
    for change in delta:
        path = change.get("path")
        if not isinstance(path, str) or not path.startswith("/"):
            raise ValueError("All changed paths must be JSON pointers")
        paths.append(path)
    return tuple(sorted(set(paths)))


def _coupled_schema(value: Any) -> bool:
    """One ADD of a schema object can contain several coupled constraints."""
    if isinstance(value, dict):
        if set(value) & {
            "anyOf", "oneOf", "allOf", "dependentSchemas", "dependencies",
            "if", "then", "else",
        }:
            return True
        properties = value.get("properties")
        if isinstance(properties, dict) and len(properties) >= 2:
            return True
        return any(_coupled_schema(v) for v in value.values())
    if isinstance(value, list):
        return any(_coupled_schema(v) for v in value)
    return False


def needs_whole_assessment(delta: Sequence[Mapping[str, Any]]) -> bool:
    if len(_paths(delta)) >= 2:
        return True
    relational = {
        "anyOf", "oneOf", "allOf", "dependentSchemas", "dependencies",
        "if", "then", "else",
    }
    return any(
        bool(relational.intersection(change["path"].split("/")))
        or _coupled_schema(change.get("before"))
        or _coupled_schema(change.get("after"))
        for change in delta
    )


def evaluate_v2(
    delta: Sequence[Mapping[str, Any]], base_level: int, *,
    assessment: WholeAssessment | None,
) -> int:
    """Compute candidate minimum action; unresolved assessment raises.

    The resulting number is a policy action threshold, not a measured
    probability of harm or empirically calibrated risk score.
    """
    if type(base_level) is not int or base_level not in range(5):
        raise ValueError("Invalid path-level minimum action")
    exact_paths = set(_paths(delta))
    if base_level == 4 or not needs_whole_assessment(delta):
        return base_level
    if assessment is None:
        raise UnresolvedWholeContract("WHOLE_ASSESSMENT_MISSING")
    if not isinstance(assessment, WholeAssessment):
        raise ValueError("Whole assessor returned invalid type")
    try:
        relation = Relation(assessment.relation)
    except (TypeError, ValueError) as exc:
        raise ValueError("Invalid whole-contract relation") from exc
    if (not re.fullmatch(r"[0-9a-f]{64}", assessment.baseline_jcs_sha256)
            or not re.fullmatch(r"[0-9a-f]{64}", assessment.candidate_jcs_sha256)):
        raise UnresolvedWholeContract("MISSING_CONTRACT_HASH_BINDING")
    if not assessment.rationale.strip() or not assessment.evidence_origin.strip():
        raise ValueError("Evidence rationale/origin is required")
    witnessed_paths = set(assessment.evidence_paths)
    if not witnessed_paths or not witnessed_paths.issubset(exact_paths):
        raise ValueError("Assessment witness does not match exact changed paths")
    if relation is Relation.UNCERTAIN:
        if assessment.level is not None:
            raise ValueError("Uncertainty must not be mislabeled with severity")
        raise UnresolvedWholeContract("WHOLE_INTERACTION_UNCERTAIN")
    if relation is Relation.INDEPENDENT:
        if assessment.level not in (0, 1, 2):
            raise ValueError("INDEPENDENT assessment cannot claim L3/L4")
        return max(base_level, assessment.level)
    if relation is Relation.BOUNDED_INTERACTION:
        if assessment.level not in (0, 1, 2):
            raise ValueError("BOUNDED_INTERACTION cannot claim L3/L4")
        if len(witnessed_paths) < 2:
            raise ValueError("BOUNDED_INTERACTION requires multiple evidenced changed paths")
        return max(base_level, assessment.level)
    if assessment.level not in (3, 4):
        raise ValueError("INTERACTION requires L3 or explicit evidenced R4/L4")
    if assessment.level == 4:
        if "R4" not in assessment.rationale.upper():
            raise UnresolvedWholeContract("L4_NEEDS_EXPLICIT_R4_EVIDENCE")
        witness = assessment.r4_client_visible_witness
        # The witness is an evidence anchor, not a validated deception detector.
        if (not isinstance(witness, str) or len(witness.strip()) < 8
                or not any(
                    change.get("path") in witnessed_paths
                    and witness in str(change.get("after", ""))
                    for change in delta
                )):
            raise UnresolvedWholeContract("L4_CLIENT_VISIBLE_WITNESS_MISSING")
    return max(base_level, assessment.level)


def revalidate_v2(
    state: Any, advertised: Any, *,
    classify_level: Callable[[list[dict[str, Any]]], int],
    whole_assessor: Callable[..., WholeAssessment] | None = None,
    _engine: Callable[..., Any] | None = None,
    **kwargs: Any,
) -> Any:
    """Route both operational and cumulative deltas via the whole-contract gate.

    This is the prospective DCTR-IA-2.0 engine entry point. The legacy engine
    remains intact for reproduction. An independent reviewer can supply a
    digest-bound whole contract assessment; absent/uncertain assessment is
    translated to SemanticUncertainty, which the reference engine handles as
    a pending, non-continuing L3 review action.
    """
    from canonicalize import sha256_digest
    from revalidation_state import SemanticUncertainty
    if _engine is None:
        from revalidation_state import revalidate as _engine
    anchors = (
        ("operational", getattr(state, "operational_baseline", None)),
        ("human_reviewed", getattr(state, "human_reviewed_baseline", None)),
    )
    invocation = 0

    def classify(delta: list[dict[str, Any]]) -> int:
        nonlocal invocation
        if invocation >= 2:
            raise ValueError("Unexpected number of classifier invocations")
        anchor_type, baseline = anchors[invocation]
        invocation += 1
        level = classify_level(delta)
        if not needs_whole_assessment(delta) or level == 4:
            return level
        if whole_assessor is None:
            raise SemanticUncertainty("WHOLE_ASSESSMENT_MISSING")
        assessment = whole_assessor(baseline, advertised, tuple(delta), anchor_type)
        if not isinstance(assessment, WholeAssessment):
            raise ValueError("Invalid whole assessor output")
        try:
            if (assessment.baseline_jcs_sha256 != sha256_digest(baseline)
                    or assessment.candidate_jcs_sha256 != sha256_digest(advertised)):
                raise UnresolvedWholeContract("STALE_ASSESSMENT_HASH")
            return evaluate_v2(delta, level, assessment=assessment)
        except UnresolvedWholeContract as exc:
            raise SemanticUncertainty(str(exc)) from exc

    return _engine(state, advertised, classify_level=classify, **kwargs)
