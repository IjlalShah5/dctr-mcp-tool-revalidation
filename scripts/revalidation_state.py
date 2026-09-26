#!/usr/bin/env python3
"""DCTR approval continuity with operational + human-reviewed baselines."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Any, Callable, Optional

from canonicalize import sha256_digest
from recursive_diff import recursive_diff


class _AbsentTool:
    """Sentinel for an advertised Tool that is no longer present."""

    def __repr__(self) -> str:
        return "ABSENT"


ABSENT = _AbsentTool()


class SemanticUncertainty(Exception):
    """Classifier signal that exact evidence exists but semantic meaning is uncertain."""


class ReferenceAction(str, Enum):
    ACCEPT_LOG = "ACCEPT_LOG"
    AUDIT_NOTE = "AUDIT_NOTE"
    NOTICE = "NOTICE"
    REVALIDATE = "REVALIDATE"
    QUARANTINE = "QUARANTINE"
    FAIL_CLOSED = "FAIL_CLOSED"


class Decision(str, Enum):
    ALLOW_CONTINUATION = "ALLOW_CONTINUATION"
    PENDING = "PENDING"
    DENY = "DENY"
    QUARANTINE = "QUARANTINE"
    BLOCK = "BLOCK"
    REVOKE = "REVOKE"


@dataclass(frozen=True)
class Grant:
    server_id: str
    tool_id: str
    approved_hash: str
    human_reviewed_hash: str
    policy_context: str
    approval_time: str


@dataclass(frozen=True)
class TrustState:
    operational_baseline: Any | None
    human_reviewed_baseline: Any | None
    grant: Grant | None


@dataclass(frozen=True)
class RevalidationResult:
    status: str
    local_level: int | None
    cumulative_level: int | None
    effective_level: int | None
    action: ReferenceAction | None
    decision: Decision | None
    local_delta: tuple[dict[str, Any], ...]
    cumulative_delta: tuple[dict[str, Any], ...]
    state: TrustState
    candidate_hash: str | None = None


def reference_action(level: int) -> ReferenceAction:
    return {
        0: ReferenceAction.ACCEPT_LOG,
        1: ReferenceAction.AUDIT_NOTE,
        2: ReferenceAction.NOTICE,
        3: ReferenceAction.REVALIDATE,
        4: ReferenceAction.QUARANTINE,
    }[level]


def default_enforcer(action, explicit_human_approval):
    if action in {ReferenceAction.ACCEPT_LOG, ReferenceAction.AUDIT_NOTE, ReferenceAction.NOTICE}:
        return Decision.ALLOW_CONTINUATION
    if action == ReferenceAction.REVALIDATE:
        if explicit_human_approval is True:
            return Decision.ALLOW_CONTINUATION
        if explicit_human_approval is False:
            return Decision.DENY
        return Decision.PENDING
    if action == ReferenceAction.QUARANTINE:
        # L4 is a remediation/quarantine state, not an ordinary approval override.
        return Decision.QUARANTINE
    return Decision.BLOCK


def _level(value: int) -> int:
    value = int(value)
    if value not in (0, 1, 2, 3, 4):
        raise ValueError("classify_level must return 0..4")
    return value


def _canonical_hash_or_none(value: Any) -> str | None:
    try:
        return sha256_digest(value)
    except Exception:
        return None


def revalidate(
    state: TrustState,
    advertised: Any,
    *,
    server_id: str,
    tool_id: str,
    policy_context: str,
    approval_time: str,
    classify_level: Callable[[list[dict[str, Any]]], int],
    explicit_human_approval: Optional[bool] = None,
    enforce=default_enforcer,
) -> RevalidationResult:
    operational = state.operational_baseline
    anchor = state.human_reviewed_baseline
    grant = state.grant

    # Withdrawal is an explicit lifecycle event. It revokes the active grant and both
    # approval baselines so a later reintroduction cannot inherit prior approval.
    if advertised is ABSENT:
        if operational is None and anchor is None and grant is None:
            return RevalidationResult(
                "ABSENT_UNTRUSTED", None, None, None, None, Decision.REVOKE,
                (), (), state, None
            )
        revoked = TrustState(None, None, None)
        return RevalidationResult(
            "WITHDRAWN", None, None, None, None, Decision.REVOKE,
            (), (), revoked, None
        )

    candidate_hash = _canonical_hash_or_none(advertised)
    if candidate_hash is None:
        return RevalidationResult(
            "CANONICALIZATION_FAILURE", None, None, None,
            ReferenceAction.FAIL_CLOSED, Decision.BLOCK,
            (), (), state, None
        )

    # Initial trust is intentionally separate from revalidation; this function does not
    # silently establish a grant for a newly observed or reintroduced Tool.
    if operational is None or anchor is None or grant is None:
        return RevalidationResult(
            "INITIAL_TRUST", None, None, None, None, None,
            (), (), state, candidate_hash
        )

    if grant.server_id != server_id or grant.tool_id != tool_id:
        return RevalidationResult(
            "GRANT_IDENTITY_MISMATCH", None, None, None,
            ReferenceAction.FAIL_CLOSED, Decision.BLOCK,
            (), (), state, candidate_hash
        )

    operational_hash = _canonical_hash_or_none(operational)
    anchor_hash = _canonical_hash_or_none(anchor)
    if operational_hash is None or anchor_hash is None:
        return RevalidationResult(
            "CANONICALIZATION_FAILURE", None, None, None,
            ReferenceAction.FAIL_CLOSED, Decision.BLOCK,
            (), (), state, candidate_hash
        )

    if operational_hash != grant.approved_hash:
        return RevalidationResult(
            "BASELINE_INTEGRITY_FAILURE", None, None, None,
            ReferenceAction.FAIL_CLOSED, Decision.BLOCK,
            (), (), state, candidate_hash
        )

    # The cumulative human-reviewed anchor is also integrity-bound. Otherwise a
    # corrupted or tampered stored anchor could silently change the cumulative
    # comparison that underpins staircase-drift escalation.
    if anchor_hash != grant.human_reviewed_hash:
        return RevalidationResult(
            "HUMAN_ANCHOR_INTEGRITY_FAILURE", None, None, None,
            ReferenceAction.FAIL_CLOSED, Decision.BLOCK,
            (), (), state, candidate_hash
        )

    if candidate_hash == grant.approved_hash:
        return RevalidationResult(
            "STABLE_ACCEPT", 0, 0, 0,
            ReferenceAction.ACCEPT_LOG, Decision.ALLOW_CONTINUATION,
            (), (), state, candidate_hash
        )

    try:
        local_delta = recursive_diff(operational, advertised)
        cumulative_delta = recursive_diff(anchor, advertised)
    except Exception:
        return RevalidationResult(
            "DIFFERENCING_FAILURE", None, None, None,
            ReferenceAction.FAIL_CLOSED, Decision.BLOCK,
            (), (), state, candidate_hash
        )

    if not local_delta:
        return RevalidationResult(
            "DIFFERENCING_INCONSISTENCY", None, None, None,
            ReferenceAction.FAIL_CLOSED, Decision.BLOCK,
            (), (), state, candidate_hash
        )

    if anchor_hash != candidate_hash and not cumulative_delta:
        return RevalidationResult(
            "DIFFERENCING_INCONSISTENCY", None, None, None,
            ReferenceAction.FAIL_CLOSED, Decision.BLOCK,
            tuple(local_delta), (), state, candidate_hash
        )

    try:
        local_level = _level(classify_level(local_delta))
        cumulative_level = 0 if not cumulative_delta else _level(classify_level(cumulative_delta))
    except SemanticUncertainty:
        return RevalidationResult(
            "SEMANTIC_UNCERTAIN", None, None, 3,
            ReferenceAction.REVALIDATE, Decision.PENDING,
            tuple(local_delta), tuple(cumulative_delta), state, candidate_hash
        )
    except Exception:
        return RevalidationResult(
            "POLICY_ENGINE_FAILURE", None, None, None,
            ReferenceAction.FAIL_CLOSED, Decision.BLOCK,
            tuple(local_delta), tuple(cumulative_delta), state, candidate_hash
        )

    effective_level = max(local_level, cumulative_level)
    action = reference_action(effective_level)
    try:
        decision = enforce(action, explicit_human_approval)
    except Exception:
        return RevalidationResult(
            "POLICY_ENGINE_FAILURE", local_level, cumulative_level, effective_level,
            ReferenceAction.FAIL_CLOSED, Decision.BLOCK,
            tuple(local_delta), tuple(cumulative_delta), state, candidate_hash
        )

    if decision == Decision.ALLOW_CONTINUATION:
        if explicit_human_approval is True:
            new_anchor = advertised
            new_human_reviewed_hash = candidate_hash
            status = "HUMAN_APPROVED_CONTINUATION"
        else:
            new_anchor = anchor
            new_human_reviewed_hash = grant.human_reviewed_hash
            status = "POLICY_AUTHORISED_CONTINUATION"

        new_grant = replace(
            grant,
            approved_hash=candidate_hash,
            human_reviewed_hash=new_human_reviewed_hash,
            policy_context=policy_context,
            approval_time=approval_time,
        )
        new_state = TrustState(advertised, new_anchor, new_grant)
    else:
        new_state = state
        status = {
            Decision.PENDING: "REVALIDATION_PENDING",
            Decision.DENY: "REVALIDATION_DENIED",
            Decision.QUARANTINE: "QUARANTINED",
            Decision.BLOCK: "FAIL_CLOSED",
            Decision.REVOKE: "WITHDRAWN",
        }[decision]

    return RevalidationResult(
        status,
        local_level,
        cumulative_level,
        effective_level,
        action,
        decision,
        tuple(local_delta),
        tuple(cumulative_delta),
        new_state,
        candidate_hash,
    )
