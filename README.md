# DCTR: Directional Contract-Transition Revalidation

This repository is the reproducibility artefact for the revised DCTR manuscript on
approval continuity for evolving Model Context Protocol (MCP) Tools.

## Current revision branch

The active major-revision work is on:

`revision-phase11-hardening`

Draft PR: #1.

The default `main` branch is intentionally left untouched until the revision artefact is
fully audited.

## What DCTR evaluates

DCTR asks whether a prior approval remains transferable when an authenticated,
client-visible Tool contract changes. The reference artefact separates:

1. **deterministic change evidence** — RFC 8785/JCS canonical identity, SHA-256,
   direction-preserving recursive deltas, and fail-closed consistency checks;
2. **security-semantic interpretation** — explicit TSV/reference-policy coding;
3. **trust-renewal state** — an operational grant-bound baseline plus a last
   human-reviewed anchor used to detect cumulative staircase drift.

Runtime authorization, provenance, sandboxing, and hidden implementation behavior remain
separate controls.

## Evidence sets

The artefact keeps two empirical sets separate:

- **Original historical corpus:** 82 Tool-level transitions across 20 maintainer/release
  clusters and four server families. This remains the descriptive denominator.
- **Supplementary natural-mutation validation set:** 32 additional present-to-present
  mutations across 10 maintainer clusters.

Combined mutation-focused analysis therefore contains **36 natural mutations across
14 mutation clusters**, but the two datasets are not pooled into a prevalence denominator.

## Independent annotation design

The four primary mutations P01–P04 were visible during codebook development and are now
treated as a development set.

The held-out independent evaluation population is the supplementary set:
- 32 mutations;
- 34 path-level units;
- 10 maintainer clusters.

The frozen paper-facing codebook is `docs/DCTR-CB-1.0-FROZEN.md`. Real independent
annotator results are not present yet and must not be fabricated.

## External comparison

`data/baseline_comparison_36.csv` extends the decision-structure comparison to all
36 natural mutations using:
- an ETDI-style reapproval-on-any-change decision baseline;
- Microsoft MCP Security Gateway's documented specific schema-drift and rug-pull rules;
- DCTR, with supplementary outputs intentionally pending held-out independent annotation.

Unsupported Microsoft surfaces are recorded as `NOT_COVERED`; no severity is invented.

## Runtime triangulation

A three-case controlled subset is retained for:
- Playwright screenshot scale;
- Playwright WebP/type-selection behavior;
- Terraform `create_run` safe/destructive contract selection.

These checks corroborate selected behavior only; they do not make DCTR a runtime detector.

## Key layout

```text
contracts/primary/                  corrected primary before/after projections
data/
  transitions.csv                  original historical transition inventory
  primary_mutations.csv            original primary mutation manifest
  supplementary_natural_mutations.csv
  supplementary_mutation_clusters.csv
  baseline_comparison_36.csv
  runtime_alignment_matrix.csv
  heldout_annotation_unit_index.csv
  policy_conformance_suite.json
docs/
  methodology.md
  coding-rules.md
  DCTR-CB-1.0-FROZEN.md
  annotation-protocol-heldout.md
  supplementary-search-protocol.md
  baseline-comparison-36.md
  runtime-validation-report.md
  formal-properties-phase11.md
scripts/
  canonicalize.py
  recursive_diff.py
  verify_transition.py
  revalidation_state.py
  p03_filename_inference.js
  playwright_runtime_validation.py
  tfmx11_contract_selector.go
tests/
  test_phase11_hardening.py
  test_revision_artifacts.py
```

## Reproducibility discipline

No transition row, contract projection, source boundary, or semantic label should be
promoted into the artefact unless it can be traced to retained evidence. Coordinated
multi-Tool edits are reported at both event and cluster level to avoid pseudo-replication.

## Citation and release

A formal citation entry is provided in `CITATION.cff`. Before resubmission, merge the
audited revision PR, create an immutable revision tag/release, and cite that exact commit
SHA in the response letter.

## License

A repository license has not yet been selected by the authors. Until one is added, the
repository remains publicly readable but no additional reuse rights are granted beyond
those provided by applicable law.
