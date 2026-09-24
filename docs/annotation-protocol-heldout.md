# Held-out Independent Annotation Protocol

## Objective

Measure whether two independent security-knowledgeable non-author annotators can apply
`DCTR-CB-1.0-FROZEN` consistently to unseen natural mutation evidence.

## Data split

**Development set**
- P01–P04
- 4 transitions
- 12 path units
- used during codebook development
- excluded from the primary reliability statistic

**Held-out evaluation set**
- 32 supplementary natural mutations
- 34 path units
- 10 maintainer mutation clusters

The held-out unit index is stored in `data/heldout_annotation_unit_index.csv`.

## Blinding

Annotators should receive Tool identity, contract surface, exact path, operation, and
before/after evidence. They should not receive author DCTR labels, mutation IDs, cluster
IDs, family IDs, or comparison-baseline outputs.

## Procedure

1. Confirm the applicable institutional ethics determination before recruitment.
2. Freeze the exact codebook and annotator forms with a SHA-256 manifest.
3. Annotators A/B work independently.
4. Validate the completed forms.
5. Archive pre-adjudication agreement.
6. Only then reveal disagreements and adjudicate.
7. Preserve the original pre-adjudication metrics in the manuscript.

## Predeclared outcomes

Primary:
- linear-weighted Cohen's kappa for held-out path-level L0–L4 labels;
- raw exact L0–L4 agreement.

Sensitivity:
- ordinal Krippendorff alpha;
- cluster-macro raw agreement, weighting the 10 maintainer clusters equally;
- pattern-deduplicated agreement, where the coordinated 10-Tool Terraform annotation
  update and 11-Tool Playwright filename-guidance update each contribute as one predefined
  change pattern.

Also report uncertainty and confidence distributions.

## Interpretation

Agreement measures reproducibility of the frozen reference policy, not calibrated attack
probability, runtime harm, or ecosystem prevalence.
