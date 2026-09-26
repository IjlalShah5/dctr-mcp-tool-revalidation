# Held-out independent annotation results

## Design

P01-P04 are development data because they were visible during iterative codebook development and are excluded from the primary reliability statistic.

The held-out evaluation used the separate supplementary set: **32 natural mutations, 34 path-level units, and 10 maintainer clusters**. Two security-knowledgeable non-author annotators independently applied `DCTR-CB-1.0-FROZEN` to randomized forms containing Tool identity, changed path, operation, and exact before/after evidence. Author labels, mutation/cluster/family identifiers, and comparator outputs were withheld.

## Pre-adjudication reliability

Pre-adjudication metrics were frozen before either annotator saw the other's labels:

- exact L0-L4 agreement: **82.4% (28/34)**;
- linear-weighted Cohen's kappa: **0.720**;
- ordinal Krippendorff alpha: **0.764**;
- cluster-macro exact agreement: **94.5%**;
- predefined pattern-deduplicated exact agreement: **96.4%**;
- uncertain held-out labels: **0** for each annotator.

Six L0-L4 disagreements occurred, all within the coordinated Playwright filename/path-description cluster `SPLW01`. Annotator A treated six workspace-root filename-description changes as R1/L1 clarification; Annotator B treated them as R2a/L2 bounded resource-scope semantics.

## Precision diagnostics

The frozen protocol did not predeclare confidence intervals. To avoid hiding sampling
uncertainty, a later transparent precision analysis reports percentile bootstrap intervals
with 50,000 resamples and seed `20260926`:

- unit-resampled 95% interval for linear-weighted kappa: **0.472-0.905**;
- cluster-resampled 95% interval: **0.146-1.000** (49,727/50,000 resamples had defined kappa).

The intervals are wide because the held-out study contains only 34 path units and 10
clusters. They are precision diagnostics rather than hypothesis tests or additional
independent evidence.

A post hoc localization diagnostic excluding the coordinated `SPLW01` cluster leaves
23 path units and yields kappa **1.000**. This is not a replacement reliability estimate;
it identifies where the observed disagreement is concentrated.

## Adjudication

After the independent metrics were frozen, the six disagreements were reviewed by Annotators A and B. All six were resolved by documented A+B consensus to **R2a/L2**: the newly explicit workspace-root resolution sentence changes client-visible file-location semantics in a bounded ordinary way without evidencing a security-boundary expansion.

Adjudicated held-out path-level distribution:
- L0: 1
- L1: 13
- L2: 19
- L3: 1
- L4: 0

After max-path composition to the 32 mutation-level outputs:
- L1: 13
- L2: 18
- L3: 1
- L0/L4: 0

These are reference-policy outputs, not calibrated attack probabilities, runtime-harm scores, or ecosystem prevalence estimates.

## Codebook insight from disagreement

The disagreement is informative rather than merely noise. The eleven coordinated
Playwright edits share a rollout pattern but are not textually identical: some only add
the workspace-root resolution clause, while others also restate default output location
or broaden "markdown file" to "a file". The six disagreements isolate a fragile codebook
boundary: when previously implicit behavior becomes explicit, is that R1 maintenance or
R2a bounded semantics? The adjudication selected R2a for these file-location clauses,
but the result is not retroactively generalized into a new rule for unrelated prose.

This boundary also clarifies why P01 remains different. R3c is reserved for a newly
explicit **material risk** that changes the informational basis of approval; ordinary
implicit-to-explicit operational detail does not become L3 merely because it is newly
stated. A future codebook revision should include dedicated boundary examples for
implicit-to-explicit disclosures before any new evaluation.

## Protocol audit note

The returned workbooks preserved the held-out evidence, frozen codebook, and calibration materials. An administrative deviation was recorded because each annotator edited the `START HERE` instruction by removing the sentence prohibiting AI/other-person assistance. The administrator subsequently reconfirmed with both annotators that the actual annotation start date was 2026-09-25, each annotator personally made that instruction-sheet edit, neither used generative AI or another person to decide labels, and neither saw the other annotator's answers before completion.

Original returned workbooks and pre-adjudication metrics are retained separately from adjudicated outputs.
