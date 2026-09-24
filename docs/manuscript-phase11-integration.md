# Phase 11 manuscript integration map

This document records the manuscript-level integration corresponding to the revision artefact on this branch.

## Title / positioning

Preferred revised title:

**Directional Contract-Transition Revalidation for Model Context Protocol Tools: An Approval-Continuity Framework for Evolving Agent Capabilities**

DCTR is positioned as an approval-continuity reference design, not as a calibrated risk model or runtime detector.

## Introduction / contributions

- Narrow novelty relative to ETDI and existing schema-drift tooling.
- Preserve the exact approved operational baseline rather than the last observation.
- Add a distinct last-human-reviewed cumulative anchor.
- State non-claims: no ecosystem prevalence, calibrated L0-L4 risk, universal runtime equivalence, or demonstrated workload reduction.

## Methods

### State model

Use:
- operational baseline `O_t`;
- last human-reviewed anchor `H_t`;
- active grant bound to `h(O_t)`.

For candidate `C`:

`D_local = Δ(O_t, C)`

`D_cum = Δ(H_t, C)`

`L_eff = max(L(D_local), L(D_cum))`

Automatic L0-L2 continuation may advance `O_t`; only explicit human approval advances `H_t`.

### Canonical identity

Use RFC 8785 / JCS rather than Python-native serialization/equality.

Required consequences:
- `true != 1`;
- `1 == 1.0` for canonical JSON-number identity;
- `-0 == 0`;
- digest mismatch with an empty exact delta is fail-closed.

### Independent annotation

P01-P04 are development data and excluded from the primary reliability statistic.

Held-out evaluation:
- 32 supplementary natural mutations;
- 34 path units;
- 10 maintainer clusters.

Paper-facing frozen codebook: `DCTR-CB-1.0-FROZEN`.

Primary outcomes:
- exact raw agreement;
- linear-weighted Cohen kappa.

Sensitivity:
- ordinal Krippendorff alpha;
- cluster-macro agreement;
- predefined pattern-deduplicated agreement.

No independent reliability result is reported until real non-author annotation and the applicable institutional ethics determination are complete.

## Results

Keep original historical corpus as its own denominator:
- 82 Tool-level transitions / 20 clusters.

Supplementary validation corpus:
- 32 natural present-to-present mutations / 10 clusters.

Combined mutation-focused evidence:
- 36 natural mutations / 14 mutation clusters.

The all-36 comparison reports:
- ETDI-style explicit reapproval for all changed definitions;
- Microsoft documented specific drift/rug-pull coverage;
- unsupported Microsoft surfaces as `NOT_COVERED`;
- DCTR supplementary outputs as pending held-out independent annotation.

The three-case runtime triangulation remains scoped corroboration only.

## Discussion / limitations

- L0-L4 is an ordinal reference policy, not calibrated risk.
- Coordinated edits are not treated as statistically independent prevalence evidence.
- The controlled R0-R4 suite is policy-conformance coverage, not natural prevalence data.
- Contract security semantics do not prove hidden implementation behavior.
- Independent semantic reproducibility remains the external empirical gate.

## Submission gate

Before the revision is submitted:
1. obtain the applicable institutional ethics determination for expert annotation;
2. collect two real independent non-author annotation sets;
3. archive pre-adjudication agreement;
4. adjudicate only after that archive exists;
5. insert real results into the manuscript and response letter;
6. audit/merge this draft PR;
7. create an immutable revision tag/release and cite its merged commit SHA.

The current Phase 11 DOCX intentionally retains visible annotation/ethics placeholders so it cannot be mistaken for a submission-final file.
