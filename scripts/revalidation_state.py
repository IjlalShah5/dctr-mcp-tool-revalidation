#!/usr/bin/env python3
"""DCTR approval continuity with operational + human-reviewed baselines."""

from __future__ import annotations

from dataclasses import dataclass, replace
from enum import Enum
from typing import Any, Callable, Optional

from canonicalize import sha256_digest
from recursive_diff import recursive_diff


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


@dataclass(frozen=True)
class Grant:
    server_id: str
    tool_id: str
    approved_hash: str
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
        return Decision.QUARANTINE
    return Decision.BLOCK


def _level(value: int) -> int:
    value = int(value)
    if value not in (0, 1, 2, 3, 4):
        raise ValueError("classify_level must return 0..4")
    return value


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

    if operational is None or anchor is None or grant is None:
        return RevalidationResult("INITIAL_TRUST", None, None, None, None, None, (), (), state, sha256_digest(advertised))

    if sha256_digest(operational) != grant.approved_hash:
        return RevalidationResult("BASELINE_INTEGRITY_FAILURE", None, None, None, ReferenceAction.FAIL_CLOSED, Decision.BLOCK, (), (), state, sha256_digest(advertised))

    candidate_hash = sha256_digest(advertised)
    if candidate_hash == grant.approved_hash:
        return RevalidationResult("STABLE_ACCEPT", 0, 0, 0, ReferenceAction.ACCEPT_LOG, Decision.ALLOW_CONTINUATION, (), (), state, candidate_hash)

    local_delta = recursive_diff(operational, advertised)
    if not local_delta:
        return RevalidationResult("DIFFERENCING_INCONSISTENCY", None, None, None, ReferenceAction.FAIL_CLOSED, Decision.BLOCK, (), (), state, candidate_hash)

    cumulative_delta = recursive_diff(anchor, advertised)
    if sha256_digest(anchor) != candidate_hash and not cumulative_delta:
        return RevalidationResult("DIFFERENCING_INCONSISTENCY", None, None, None, ReferenceAction.FAIL_CLOSED, Decision.BLOCK, tuple(local_delta), (), state, candidate_hash)

    local_level = _level(classify_level(local_delta))
    cumulative_level = 0 if not cumulative_delta else _level(classify_level(cumulative_delta))
    effective_level = max(local_level, cumulative_level)
    action = reference_action(effective_level)
    decision = enforce(action, explicit_human_approval)

    if decision == Decision.ALLOW_CONTINUATION:
        new_grant = replace(grant, approved_hash=candidate_hash, policy_context=policy_context, approval_time=approval_time)
        new_anchor = advertised if explicit_human_approval is True else anchor
        new_state = TrustState(advertised, new_anchor, new_grant)
        status = "HUMAN_APPROVED_CONTINUATION" if explicit_human_approval is True else "POLICY_AUTHORISED_CONTINUATION"
    else:
        new_state = state
        status = {
            Decision.PENDING: "REVALIDATION_PENDING",
            Decision.DENY: "REVALIDATION_DENIED",
            Decision.QUARANTINE: "QUARANTINED",
            Decision.BLOCK: "FAIL_CLOSED",
        }[decision]

    return RevalidationResult(
        status, local_level, cumulative_level, effective_level, action, decision,
        tuple(local_delta), tuple(cumulative_delta), new_state, candidate_hash
    )
