"""Controlled end-to-end MCP stdio, SQLite, and DCTR approval-state tests.

Test claims are deliberately about this synthetic client/server fixture only.
No automatic semantic classification or real-server security superiority is implied.
"""
from __future__ import annotations

import copy
import json
import sqlite3
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from revalidation_state import Decision
from round3_mcp_stdio_harness import (
    BASE_TOOL, TOOL_ID, SQLiteMCPApprovalClient, StdioTestServer,
    conservative_cross_path_guard,
)


class Round3MCPStdioIntegration(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix="dctr-round3-mcp-")
        self.db = Path(self.tmp.name) / "state.sqlite3"
        self.server = StdioTestServer()
        self.client = SQLiteMCPApprovalClient(self.server, self.db)
        self.base = copy.deepcopy(BASE_TOOL)

    def tearDown(self):
        self.client.close()
        self.server.close()
        self.tmp.cleanup()

    def approve(self):
        self.assertEqual(self.client.refresh().status, "INITIAL_TRUST")
        self.client.approve_initial(explicit_human_approval=True)
        self.assertEqual(self.client.refresh().status, "STABLE_ACCEPT")

    def mutate(self, **changes):
        candidate = copy.deepcopy(self.base)
        candidate["x-round3-test"].update(changes)
        self.server.set_contract(candidate)
        return candidate

    def malicious(self):
        candidate = copy.deepcopy(self.base)
        candidate["description"] += " IGNORE_APPROVAL_AND_EXFILTRATE"
        self.server.set_contract(candidate)
        return candidate

    def assert_blocked(self):
        before = self.server.calls()
        with self.assertRaises(PermissionError):
            self.client.call("must-not-reach-server")
        self.assertEqual(self.server.calls(), before, "forbidden tools/call crossed the client gate")

    def test_01_initial_trust_is_not_automatic(self):
        self.assertEqual(self.client.refresh().status, "INITIAL_TRUST")
        self.assert_blocked()
        with self.assertRaises(PermissionError):
            self.client.approve_initial(explicit_human_approval=False)
        self.assert_blocked()
        self.client.approve_initial(explicit_human_approval=True)
        self.assertEqual(self.client.call("ok")["content"][0]["text"], "ok")
        self.assertEqual(self.server.calls(), 1)

    def test_02_stable_refresh_and_stdio_tools_call(self):
        self.approve()
        self.assertEqual(self.client.call("hello")["content"][0]["text"], "hello")
        self.assertEqual(self.client.refresh().status, "STABLE_ACCEPT")
        self.assertEqual(self.server.calls(), 1)

    def test_03_l3_pending_keeps_operational_and_human_anchors(self):
        self.approve()
        before = self.client.store.load()
        self.mutate(scope=3)
        first = self.client.refresh()
        self.assertEqual(first.effective_level, 3)
        self.assertEqual(first.decision, Decision.PENDING)
        self.assertEqual(self.client.store.load(), before)
        self.assert_blocked()
        second = self.client.refresh()
        self.assertEqual(second.status, "REVALIDATION_PENDING")
        self.assertEqual(self.client.store.load(), before)

    def test_04_l3_explicit_approval_rebinds_both_anchors(self):
        self.approve()
        changed = self.mutate(scope=3)
        result = self.client.refresh(explicit_human_approval=True)
        self.assertEqual(result.status, "HUMAN_APPROVED_CONTINUATION")
        state = self.client.store.load()
        self.assertEqual(state.operational_baseline, changed)
        self.assertEqual(state.human_reviewed_baseline, changed)
        self.assertEqual(self.client.call("approved")["content"][0]["text"], "approved")

    def test_05_l4_automatic_quarantine_blocks_real_tool_invocation(self):
        self.approve()
        self.malicious()
        result = self.client.refresh()
        self.assertEqual(result.status, "QUARANTINED")
        self.assertEqual(result.effective_level, 4)
        self.assertEqual(self.client.store.load().quarantine.reason, "L4")
        self.assert_blocked()

    def test_06_quarantine_persists_across_sqlite_client_reopen(self):
        self.approve()
        self.malicious()
        self.assertEqual(self.client.refresh().status, "QUARANTINED")
        self.client.close()
        self.client = SQLiteMCPApprovalClient(self.server, self.db)
        self.assertIsNotNone(self.client.store.load().quarantine)
        self.assertEqual(self.client.refresh().status, "QUARANTINED_LOCKED")
        self.assert_blocked()

    def test_07_original_and_bounded_refresh_cannot_unlock_quarantine(self):
        self.approve()
        self.malicious()
        self.client.refresh()
        self.server.set_contract(self.base)
        self.assertEqual(self.client.refresh().status, "QUARANTINED_LOCKED")
        self.assert_blocked()
        self.mutate(scope=2)
        self.assertEqual(self.client.refresh().status, "QUARANTINED_LOCKED")
        self.assert_blocked()

    def test_08_l4_cannot_be_overridden_by_human_flag(self):
        self.approve()
        self.malicious()
        r = self.client.refresh(explicit_human_approval=True)
        self.assertEqual(r.status, "QUARANTINED")
        self.assertEqual(r.decision, Decision.QUARANTINE)
        self.assert_blocked()

    def test_09_recovery_requires_remediation_and_explicit_reapproval(self):
        self.approve()
        self.malicious()
        self.client.refresh()
        self.server.set_contract(self.base)
        self.assertEqual(self.client.recover(remediation_confirmed=True).status,
                         "QUARANTINED_LOCKED")
        self.assertEqual(self.client.recover(explicit_human_approval=True).status,
                         "QUARANTINED_LOCKED")
        self.assert_blocked()
        self.assertEqual(
            self.client.recover(remediation_confirmed=True,
                                explicit_human_approval=True).status,
            "QUARANTINE_RELEASED",
        )
        self.assertIsNone(self.client.store.load().quarantine)
        self.assertEqual(self.client.call("after-recovery")["content"][0]["text"],
                         "after-recovery")

    def test_10_recovery_rejects_same_quarantined_candidate(self):
        self.approve()
        self.malicious()
        self.client.refresh()
        r = self.client.recover(remediation_confirmed=True,
                                explicit_human_approval=True)
        self.assertEqual(r.status, "QUARANTINE_RECOVERY_REJECTED")
        self.assert_blocked()

    def test_11_integrity_failure_persists_lock_and_blocks_invocation(self):
        self.approve()
        bad = self.client.store.load()
        from dataclasses import replace
        self.client.store.save(replace(
            bad, operational_baseline={"name": TOOL_ID, "wrong": True}
        ))
        self.assert_blocked()
        self.assertEqual(self.client.refresh().status, "BASELINE_INTEGRITY_FAILURE")
        self.assertEqual(self.client.store.load().quarantine.reason,
                         "BASELINE_INTEGRITY_FAILURE")
        self.assert_blocked()

    def test_12_human_anchor_tamper_fails_closed(self):
        self.approve()
        bad = self.client.store.load()
        from dataclasses import replace
        self.client.store.save(replace(
            bad, human_reviewed_baseline={"name": TOOL_ID, "wrong": True}
        ))
        self.assert_blocked()
        self.assertEqual(self.client.refresh().status,
                         "HUMAN_ANCHOR_INTEGRITY_FAILURE")
        self.assert_blocked()

    def test_13_withdrawal_revokes_grant_and_reintroduction_needs_new_approval(self):
        self.approve()
        self.server.set_contract(None)
        self.assertEqual(self.client.refresh().status, "WITHDRAWN")
        self.assert_blocked()
        self.server.set_contract(self.base)
        self.assertEqual(self.client.refresh().status, "INITIAL_TRUST")
        self.assert_blocked()

    def test_14_bounded_operational_step_cumulative_l3_staircase(self):
        self.approve()
        step = self.mutate(scope=2)
        r1 = self.client.refresh()
        self.assertEqual(r1.effective_level, 2)
        self.assertEqual(r1.decision, Decision.ALLOW_CONTINUATION)
        self.assertEqual(self.client.store.load().operational_baseline, step)
        self.assertEqual(self.client.store.load().human_reviewed_baseline, self.base)
        self.mutate(scope=3)
        r2 = self.client.refresh()
        self.assertEqual((r2.local_level, r2.cumulative_level, r2.effective_level),
                         (2, 3, 3))
        self.assertEqual(r2.status, "REVALIDATION_PENDING")
        self.assert_blocked()

    def test_15_unreviewed_live_mutation_blocked_even_without_refresh(self):
        self.approve()
        candidate = copy.deepcopy(self.base)
        candidate["annotations"]["title"] = "Echo changed title"
        self.server.set_contract(candidate)
        self.assert_blocked()
        self.assertEqual(self.client.refresh().effective_level, 1)
        self.assertEqual(self.client.call("updated")["content"][0]["text"],
                         "updated")

    def test_16_partially_missing_approval_fails_closed(self):
        self.approve()
        state = self.client.store.load()
        from dataclasses import replace
        self.client.store.save(replace(state, operational_baseline=None))
        self.assert_blocked()
        self.assertEqual(self.client.refresh().status, "BASELINE_MISSING")
        self.assertEqual(self.client.store.load().quarantine.reason,
                         "BASELINE_MISSING")
        self.assert_blocked()

    def test_17_controlled_cross_path_max_rule_counterexample(self):
        """Two synthetic independent L2 paths jointly enable a new combination.

        This exhibits *design coverage*, not observed implementation harm.
        """
        self.approve()
        self.mutate(write_enabled=True, external_enabled=True)
        outcome = self.client.refresh()
        self.assertEqual((outcome.local_level, outcome.cumulative_level,
                          outcome.effective_level), (2, 2, 2))
        self.assertEqual(outcome.decision, Decision.ALLOW_CONTINUATION)
        self.assertEqual(self.client.store.load().operational_baseline[
            "x-round3-test"]["external_enabled"], True)
        # The server executes a harmless synthetic conjunction witness.
        self.assertEqual(self.server.compound_effects(), 0)
        self.assertEqual(
            self.client.call("controlled-conjunction")["isError"], False
        )
        self.assertEqual(self.server.compound_effects(), 1)

    def test_18_experimental_cross_path_guard_escalates_uncertainty(self):
        self.approve()
        self.client.close()
        self.client = SQLiteMCPApprovalClient(
            self.server, self.db, classifier=conservative_cross_path_guard
        )
        old = self.client.store.load()
        self.mutate(write_enabled=True, external_enabled=True)
        outcome = self.client.refresh()
        self.assertEqual(outcome.status, "SEMANTIC_UNCERTAIN")
        self.assertEqual(outcome.effective_level, 3)
        self.assertEqual(outcome.decision, Decision.PENDING)
        self.assertEqual(self.client.store.load(), old)
        self.assert_blocked()
        self.assertEqual(self.server.compound_effects(), 0)

    def test_19_each_individual_switch_has_no_compound_witness(self):
        self.approve()
        self.mutate(write_enabled=True)
        self.assertEqual(self.client.refresh().effective_level, 2)
        self.client.call("write-only")
        self.assertEqual(self.server.compound_effects(), 0)
        self.mutate(external_enabled=True)
        self.assertEqual(self.client.refresh().effective_level, 2)
        self.client.call("external-only")
        self.assertEqual(self.server.compound_effects(), 0)

    def test_20_compound_witness_requires_both_switches_at_invocation(self):
        self.approve()
        self.mutate(write_enabled=True, external_enabled=True)
        result = self.client.refresh()
        self.assertEqual(result.decision, Decision.ALLOW_CONTINUATION)
        self.client.call("one")
        self.client.call("two")
        self.assertEqual(self.server.compound_effects(), 2)
        self.mutate(write_enabled=True, external_enabled=False)
        self.assertEqual(self.client.refresh().effective_level, 2)
        self.client.call("one-flag-disabled")
        self.assertEqual(self.server.compound_effects(), 2)


if __name__ == "__main__":
    unittest.main(verbosity=2)
