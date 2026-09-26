# Held-out Independent Annotation Protocol

## Objective

Measure whether two independent security-knowledgeable non-author annotators can apply `DCTR-CB-1.0-FROZEN` consistently to unseen natural mutation evidence.

## Data split

**Development set**
- P01-P04;
- 4 transitions;
- 12 path units;
- used during codebook development;
- excluded from the primary reliability statistic.

**Held-out evaluation set**
- 32 supplementary natural mutations;
- 34 path units;
- 10 maintainer mutation clusters.

The held-out unit index is stored in `data/heldout_annotation_unit_index.csv`.

## Blinding and procedure

Annotators received Tool identity, contract surface, exact path, operation, and before/after evidence. They did not receive author DCTR labels, mutation IDs, cluster IDs, family IDs, or comparison-baseline outputs.

The codebook and forms were frozen before scoring. Annotators worked independently. Completed forms were validated and the pre-adjudication metrics were archived before either annotator saw the other's answers. Only then were the six disagreements revealed for A+B consensus adjudication.

## Predeclared outcomes

Primary:
- linear-weighted Cohen's kappa for held-out path-level L0-L4 labels;
- raw exact L0-L4 agreement.

Sensitivity:
- ordinal Krippendorff alpha;
- cluster-macro raw agreement, weighting the 10 maintainer clusters equally;
- pattern-deduplicated agreement, where the coordinated 10-Tool Terraform annotation update and 11-Tool Playwright filename-guidance update each contribute as one predefined change pattern.

Uncertainty and confidence were also retained.

## Completed results

- raw exact L0-L4 agreement: **82.4% (28/34)**;
- linear-weighted Cohen's kappa: **0.720**;
- ordinal Krippendorff alpha: **0.764**;
- cluster-macro exact agreement: **94.5%**;
- pattern-deduplicated exact agreement: **96.4%**;
- six disagreements, all in the coordinated Playwright filename/path-description cluster;
- all six disagreements were adjudicated by A+B consensus to R2a/L2 after pre-adjudication metrics were frozen.

Agreement measures reproducibility of the frozen reference policy, not calibrated attack probability, runtime harm, or ecosystem prevalence.

## Audit trail

The held-out evidence, codebook, and calibration materials in the returned forms match the frozen versions. An instruction-sheet edit and a start-date clerical correction were recorded in the administrative audit. The administrator reconfirmed independence and no AI/other-person assistance with both annotators. Original returned files and pre-adjudication statistics remain archived separately from consensus outputs.
