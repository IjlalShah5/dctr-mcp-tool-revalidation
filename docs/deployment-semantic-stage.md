# Deployment Semantic Stage

DCTR separates deterministic evidence/state handling from semantic policy application.

## What the reference implementation automates

The repository code deterministically handles:

- JCS canonicalisation and digest identity;
- typed recursive path deltas;
- operational-baseline and human-anchor integrity checks;
- local and cumulative delta construction;
- maximum-level composition once path levels are supplied;
- approval-state transitions, withdrawal, quarantine, and fail-closed states.

## What is not claimed to be automated

The current empirical evaluation does **not** demonstrate an automatic semantic classifier
for arbitrary Tool prose. The held-out DCTR labels used in the manuscript are independent
human codebook labels followed by documented adjudication. Therefore the DCTR column in the
all-36 comparison is a reference-policy output, not the prediction of a learned or fully
automatic detector.

This distinction matters operationally: DCTR can reduce repeated whole-contract review by
presenting exact changed evidence and by allowing local policy to auto-authorise bounded
cases, but the manuscript does not measure end-to-end human-workload reduction.

## Conservative deployment pattern

A deployment can use a staged router without changing the reference policy:

1. deterministic evidence extraction;
2. narrow, auditable local rules for cases the operator is willing to auto-classify;
3. a separately validated semantic classifier if available;
4. human review for free-text, ambiguous, unsupported, or uncertain cases;
5. minimum L3 explicit revalidation whenever semantic uncertainty remains.

The default-safe fallback is therefore **escalate**, not guess. A classifier used in step 3
must be evaluated separately for under-escalation before its outputs are allowed to advance
an approval baseline.

## Research boundary

Building and validating a classifier that preserves DCTR's no-under-escalation intent is a
separate empirical problem. Any future benchmark should report automation coverage,
under-escalation relative to an independently defined reference set, false escalation, and
human-review workload. The present paper does not convert the held-out human labels into an
automatic-classifier accuracy claim.
