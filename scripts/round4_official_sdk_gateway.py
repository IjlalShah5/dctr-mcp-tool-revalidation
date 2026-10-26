#!/usr/bin/env python3
"""DCTR-IA-2.0 experimental real-MCP-SDK approval client (not a production host).

The SDK ClientSession performs real tools/list and tools/call over stdio. All
before/after Tools are author-controlled synthetic fixtures; observed canary
transfer cannot be interpreted as natural threat evidence.
"""
from __future__ import annotations

from pathlib import Path
from typing import Any, Callable

from canonicalize import sha256_digest
from revalidation_state import ABSENT
from round3_mcp_stdio_harness import SERVER_ID, TOOL_ID, test_only_classifier
from round3_official_sdk_gateway import SDKApprovalClient
from interaction_v2 import WholeAssessment, revalidate_v2


class SDKInteractionApprovalClient(SDKApprovalClient):
    """Persist interaction-aware decisions and gate every invocation."""

    def __init__(
        self, session: Any, database_path: str | Path, *,
        whole_assessor: Callable[..., WholeAssessment] | None = None,
        classify_level: Callable[..., int] = test_only_classifier,
    ):
        super().__init__(session, database_path)
        self.whole_assessor = whole_assessor
        self.classify_level = classify_level

    async def refresh(self, *, explicit_human_approval: bool | None = None):
        result = revalidate_v2(
            self.store.load(), await self.discover(),
            server_id=SERVER_ID, tool_id=TOOL_ID,
            policy_context="DCTR-IA-2.0-experimental",
            approval_time="round4-fixture",
            classify_level=self.classify_level,
            whole_assessor=self.whole_assessor,
            explicit_human_approval=explicit_human_approval,
        )
        self.store.save(result.state)
        return result

    async def call(self, arguments: dict[str, Any]):
        state = self.store.load()
        if state.quarantine is not None:
            raise PermissionError("QUARANTINED_LOCKED")
        grant = state.grant
        if (grant is None or state.operational_baseline is None
                or state.human_reviewed_baseline is None):
            raise PermissionError("NO_ACTIVE_COMPLETE_GRANT")
        if (grant.server_id, grant.tool_id) != (SERVER_ID, TOOL_ID):
            raise PermissionError("IDENTITY_MISMATCH")
        try:
            if sha256_digest(state.operational_baseline) != grant.approved_hash:
                raise PermissionError("OPERATIONAL_HASH_MISMATCH")
            if sha256_digest(state.human_reviewed_baseline) != grant.human_reviewed_hash:
                raise PermissionError("HUMAN_HASH_MISMATCH")
        except (TypeError, ValueError, OverflowError) as exc:
            raise PermissionError("CORRUPT_GRANT") from exc
        live = await self.discover()
        if live is ABSENT or sha256_digest(live) != grant.approved_hash:
            raise PermissionError("UNAPPROVED_LIVE_CONTRACT")
        if not isinstance(arguments, dict):
            raise TypeError("arguments must be a dictionary")
        # TOCTOU gap remains: a hostile server may change after tools/list.
        return await self.session.call_tool(TOOL_ID, arguments=arguments)
