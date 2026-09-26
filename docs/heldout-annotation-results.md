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

## Protocol audit note

The returned workbooks preserved the held-out evidence, frozen codebook, and calibration materials. An administrative deviation was recorded because each annotator edited the `START HERE` instruction by removing the sentence prohibiting AI/other-person assistance. The administrator subsequently reconfirmed with both annotators that the actual annotation start date was 2026-09-25, each annotator personally made that instruction-sheet edit, neither used generative AI or another person to decide labels, and neither saw the other annotator's answers before completion.

Original returned workbooks and pre-adjudication metrics are retained separately from adjudicated outputs.
