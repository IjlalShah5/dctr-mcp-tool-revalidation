# DCTR: Directional Contract-Transition Revalidation

This repository is the reproducibility artefact for the revised DCTR manuscript on approval continuity for evolving Model Context Protocol (MCP) Tools.

## Revision status

The major-revision work was developed on `revision-phase11-hardening` in PR #1. The branch now includes the completed held-out annotation results and adjudicated outputs in addition to the state-model, corpus, comparison, runtime, and conformance revisions.

## What DCTR evaluates

DCTR asks whether a prior approval remains transferable when an authenticated, client-visible Tool contract changes. The artefact separates:

1. deterministic change evidence — RFC 8785/JCS canonical identity, SHA-256, direction-preserving recursive deltas, and fail-closed consistency checks;
2. security-semantic interpretation — explicit TSV/reference-policy coding;
3. trust-renewal state — an operational grant-bound baseline plus a last human-reviewed anchor used to detect cumulative staircase drift.

Runtime authorization, provenance, sandboxing, and hidden implementation behavior remain separate controls.

## Evidence sets

- **Original historical corpus:** 82 Tool-level transitions across 20 maintainer/release clusters and four server families. This remains the descriptive denominator.
- **Supplementary natural-mutation validation set:** 32 additional present-to-present mutations across 10 maintainer clusters.

Combined mutation-focused analysis contains **36 natural mutations across 14 mutation clusters**, but the two datasets are not pooled into a prevalence denominator.

## Independent annotation results

P01-P04 are development data and are excluded from the primary reliability statistic.

The held-out evaluation covers 32 supplementary mutations / 34 path units / 10 clusters. Two security-knowledgeable non-author annotators independently applied `DCTR-CB-1.0-FROZEN`.

Pre-adjudication:
- exact L0-L4 agreement: **82.4% (28/34)**;
- linear-weighted Cohen's kappa: **0.720**;
- ordinal Krippendorff alpha: **0.764**;
- cluster-macro exact agreement: **94.5%**;
- pattern-deduplicated exact agreement: **96.4%**.

Post-protocol precision diagnostics (50,000 percentile-bootstrap resamples; seed 20260926)
give a unit-resampled kappa 95% interval of **0.472-0.905** and a cluster-resampled
interval of **0.146-1.000**. These intervals were added after the frozen protocol and are
reported as transparency diagnostics, not pre-specified inference.

Six disagreements were localized to the coordinated Playwright filename/path-description cluster and were adjudicated by A+B consensus to R2a/L2 after the independent metrics were frozen.

See `docs/heldout-annotation-results.md` and the final annotation data files under `data/`.

## External comparison

`data/baseline_comparison_36.csv` covers all 36 natural mutations using:
- an ETDI-style reapproval-on-any-change decision baseline;
- Microsoft MCP Security Gateway documented specific schema-drift and rug-pull rules;
- DCTR development-set reference outputs for P01-P04 and held-out consensus outputs for the supplementary 32.

Unsupported Microsoft surfaces are recorded as `NOT_COVERED`; no severity is invented.

## Runtime triangulation

A three-case controlled subset is retained for Playwright screenshot scale, Playwright WebP/type-selection behavior, and Terraform `create_run` contract selection. These checks corroborate selected behavior only; they do not make DCTR a runtime detector.

## Artefact map

**Core reproducibility documents**
- `docs/DCTR-CB-1.0-FROZEN.md` — frozen semantic codebook used for held-out coding.
- `docs/annotation-protocol-heldout.md` — held-out design, blinding, outcomes, and later precision diagnostics.
- `docs/heldout-annotation-results.md` — pre-adjudication reliability, adjudication, and disagreement analysis.
- `docs/formal-properties-phase11.md` — state properties and scope conditions.
- `docs/deployment-semantic-stage.md` — explicit boundary between automated evidence/state handling and semantic classification.
- `docs/baseline-comparison-36.md` — ETDI/Microsoft/DCTR decision-structure comparison.
- `docs/runtime-validation-report.md` — controlled runtime-alignment subset.

**Core data**
- `data/heldout_annotation_unit_index.csv`
- `data/heldout_annotation_final_path_units.csv`
- `data/heldout_annotation_final_mutations.csv`
- `data/heldout_annotation_metrics.json`
- `data/baseline_comparison_36.csv`
- `data/baseline_crosstab_36.csv`
- `data/policy_conformance_suite.json`

**Process/audit documents**
- `docs/phase6-heldout-redesign.md`, `docs/phase11-hardening.md`, and
  `docs/manuscript-phase11-integration.md` preserve the revision audit trail. They are
  not presented as preregistration documents and should be read alongside the frozen
  codebook/protocol above.

## Phase-12 validation status

A branch-equivalent offline run passes **25/25** unit and artefact-integrity tests,
including the new human-anchor integrity and comparison/precision artefact checks.

## Reproducibility discipline

No transition row, contract projection, source boundary, or semantic label is promoted into the artefact without retained evidence. Coordinated multi-Tool edits are reported at event and cluster level to avoid pseudo-replication. Pre-adjudication reliability remains distinct from post-consensus labels.

## Citation and release

A formal citation entry is provided in `CITATION.cff`. Commit
`0a95678737d3e79fbbf991710352b39241ee4156` is the immutable merged major-revision
snapshot. Phase-12 post-review hardening is developed separately on
`revision-phase12-postreview-hardening`.

No archival GitHub release/Zenodo DOI is claimed until the authors explicitly create one.

## License

A repository license has not yet been selected by the authors. Until one is added, the repository remains publicly readable but no additional reuse rights are granted beyond those provided by applicable law.
