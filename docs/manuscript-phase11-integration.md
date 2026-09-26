# Phase 11 manuscript integration map

## Positioning

Preferred revised title:

**Directional Contract-Transition Revalidation for Model Context Protocol Tools: An Approval-Continuity Framework for Evolving Agent Capabilities**

DCTR is an approval-continuity reference design, not a calibrated risk model or runtime detector.

## Core state model

- operational baseline `O_t`;
- last human-reviewed anchor `H_t`;
- active grant bound to `h(O_t)`;
- local delta `D_local = Delta(O_t,C)`;
- cumulative delta `D_cum = Delta(H_t,C)`;
- effective reference-policy level `L_eff = max(L(D_local), L(D_cum))`.

Automatic L0-L2 continuation may advance `O_t`; only explicit human approval advances `H_t`.

## Canonical identity

RFC 8785/JCS is used for canonical identity:
- `true != 1`;
- `1 == 1.0` for canonical JSON-number identity;
- `-0 == 0`;
- unsupported/non-I-JSON forms fail closed;
- digest mismatch with an empty exact delta fails closed.

## Empirical evidence

- original historical corpus: 82 Tool-level transitions / 20 clusters;
- supplementary validation corpus: 32 natural mutations / 10 clusters;
- combined mutation-focused evidence: 36 natural mutations / 14 clusters.

The original denominator is not replaced by the targeted supplementary mutation set.

## Completed independent annotation

P01-P04 remain development examples and are excluded from the primary reliability statistic.

Held-out evaluation:
- 32 supplementary natural mutations;
- 34 path units;
- 10 maintainer clusters;
- exact L0-L4 agreement: 82.4% (28/34);
- linear-weighted Cohen's kappa: 0.720;
- ordinal Krippendorff alpha: 0.764;
- cluster-macro exact agreement: 94.5%;
- pattern-deduplicated exact agreement: 96.4%;
- six disagreements, all in the coordinated Playwright filename/path-description cluster;
- six disagreements adjudicated by A+B consensus to R2a/L2 after pre-adjudication metrics were frozen.

Final held-out mutation-level distribution after max-path composition:
- L1: 13;
- L2: 18;
- L3: 1;
- L0/L4: 0.

## Comparison / runtime boundaries

The all-36 comparison reports ETDI-style explicit reapproval for all changed definitions, Microsoft documented specific drift/rug-pull coverage, and final DCTR reference-policy outputs. Unsupported Microsoft surfaces remain `NOT_COVERED`.

The three-case runtime triangulation remains scoped corroboration only.

## Claims discipline

- L0-L4 is an ordinal reference policy, not calibrated risk.
- Coordinated edits are not statistically independent prevalence evidence.
- The controlled R0-R4 suite is policy-conformance coverage, not natural prevalence data.
- Contract semantics do not prove hidden implementation behavior.
- Reliability metrics measure codebook reproducibility, not detector accuracy or attack probability.
