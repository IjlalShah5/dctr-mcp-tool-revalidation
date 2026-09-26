from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))

from canonicalize import canonical_bytes, sha256_digest
from recursive_diff import json_exact_equal, recursive_diff
from revalidation_state import (
    ABSENT,
    Decision,
    Grant,
    ReferenceAction,
    SemanticUncertainty,
    TrustState,
    revalidate,
)


def scope_classifier(delta):
    level = 0
    for d in delta:
        if d["path"] == "/scope" and d["operation"] == "REPLACE":
            increase = d["after"] - d["before"]
            level = max(level, 3 if increase >= 2 else 2)
        else:
            level = max(level, 2)
    return level


class JCSCanonicalizationTests(unittest.TestCase):
    def test_true_is_not_one(self):
        self.assertNotEqual(canonical_bytes(True), canonical_bytes(1))
        self.assertFalse(json_exact_equal(True, 1))

    def test_one_equals_one_point_zero(self):
        self.assertEqual(canonical_bytes(1), canonical_bytes(1.0))
        self.assertTrue(json_exact_equal(1, 1.0))
        self.assertEqual(recursive_diff({"x": 1}, {"x": 1.0}), [])

    def test_negative_zero_equals_zero(self):
        self.assertEqual(canonical_bytes(-0.0), b"0")
        self.assertEqual(canonical_bytes(-0.0), canonical_bytes(0))

    def test_reviewer_true_to_one_case_is_replace(self):
        delta = recursive_diff({"default": True}, {"default": 1})
        self.assertEqual(len(delta), 1)
        self.assertEqual(delta[0]["path"], "/default")
        self.assertEqual(delta[0]["operation"], "REPLACE")

    def test_json_pointer_escaping(self):
        delta = recursive_diff({"a/b": {"x~y": 1}}, {"a/b": {"x~y": 2}})
        self.assertEqual(delta[0]["path"], "/a~1b/x~0y")


class DualBaselineTests(unittest.TestCase):
    def setUp(self):
        self.A = {"scope": 1}
        self.grant = Grant("s", "t", sha256_digest(self.A), "p0", "t0")
        self.state = TrustState(self.A, self.A, self.grant)

    def call(self, state, candidate, approval=None, classifier=scope_classifier, server_id="s", tool_id="t"):
        return revalidate(
            state,
            candidate,
            server_id=server_id,
            tool_id=tool_id,
            policy_context="p",
            approval_time="now",
            classify_level=classifier,
            explicit_human_approval=approval,
        )

    def test_no_stability_laundering(self):
        candidate = {"scope": 3}
        first = self.call(self.state, candidate)
        self.assertEqual(first.effective_level, 3)
        self.assertEqual(first.decision, Decision.PENDING)
        self.assertEqual(first.state, self.state)

        repeated = self.call(first.state, candidate)
        self.assertEqual(repeated.status, "REVALIDATION_PENDING")
        self.assertEqual(repeated.state, self.state)

    def test_staircase_is_caught_by_cumulative_anchor(self):
        B = {"scope": 2}
        C = {"scope": 3}

        first = self.call(self.state, B)
        self.assertEqual(first.effective_level, 2)
        self.assertEqual(first.state.operational_baseline, B)
        self.assertEqual(first.state.human_reviewed_baseline, self.A)

        second = self.call(first.state, C)
        self.assertEqual(second.local_level, 2)
        self.assertEqual(second.cumulative_level, 3)
        self.assertEqual(second.effective_level, 3)
        self.assertEqual(second.action, ReferenceAction.REVALIDATE)
        self.assertEqual(second.decision, Decision.PENDING)

    def test_human_approval_resets_anchor(self):
        candidate = {"scope": 3}
        result = self.call(self.state, candidate, True)
        self.assertEqual(result.state.operational_baseline, candidate)
        self.assertEqual(result.state.human_reviewed_baseline, candidate)
        self.assertEqual(result.state.grant.approved_hash, sha256_digest(candidate))

    def test_withdrawal_revokes_and_reintroduction_requires_initial_trust(self):
        withdrawn = self.call(self.state, ABSENT)
        self.assertEqual(withdrawn.status, "WITHDRAWN")
        self.assertEqual(withdrawn.decision, Decision.REVOKE)
        self.assertEqual(withdrawn.state, TrustState(None, None, None))

        reintroduced = self.call(withdrawn.state, {"scope": 1})
        self.assertEqual(reintroduced.status, "INITIAL_TRUST")
        self.assertIsNone(reintroduced.state.grant)
        self.assertIsNone(reintroduced.state.operational_baseline)

    def test_grant_identity_mismatch_fails_closed(self):
        result = self.call(self.state, {"scope": 2}, server_id="different")
        self.assertEqual(result.status, "GRANT_IDENTITY_MISMATCH")
        self.assertEqual(result.decision, Decision.BLOCK)
        self.assertEqual(result.state, self.state)

    def test_semantic_uncertainty_requires_explicit_revalidation(self):
        def uncertain(_delta):
            raise SemanticUncertainty("meaning cannot be resolved")

        result = self.call(self.state, {"scope": 2}, classifier=uncertain)
        self.assertEqual(result.status, "SEMANTIC_UNCERTAIN")
        self.assertEqual(result.action, ReferenceAction.REVALIDATE)
        self.assertEqual(result.decision, Decision.PENDING)
        self.assertEqual(result.effective_level, 3)
        self.assertEqual(result.state, self.state)

    def test_unsupported_jcs_value_fails_closed(self):
        result = self.call(self.state, {"scope": 2**53})
        self.assertEqual(result.status, "CANONICALIZATION_FAILURE")
        self.assertEqual(result.decision, Decision.BLOCK)
        self.assertEqual(result.state, self.state)

    def test_policy_engine_exception_fails_closed(self):
        def broken(_delta):
            raise RuntimeError("boom")

        result = self.call(self.state, {"scope": 2}, classifier=broken)
        self.assertEqual(result.status, "POLICY_ENGINE_FAILURE")
        self.assertEqual(result.decision, Decision.BLOCK)
        self.assertEqual(result.state, self.state)

    def test_l4_quarantine_is_not_overridden_by_human_approval_flag(self):
        def l4(_delta):
            return 4

        result = self.call(self.state, {"scope": 2}, approval=True, classifier=l4)
        self.assertEqual(result.status, "QUARANTINED")
        self.assertEqual(result.action, ReferenceAction.QUARANTINE)
        self.assertEqual(result.decision, Decision.QUARANTINE)
        self.assertEqual(result.state, self.state)


if __name__ == "__main__":
    unittest.main(verbosity=2)
