# DCTR: Directional Contract-Transition Revalidation

This repository is the reproducibility artefact for the revised DCTR manuscript on approval continuity for evolving Model Context Protocol (MCP) Tools.

## Current Round-4 reproducibility status (29 October 2026)

DCTR-IA-2.0 is now implemented on **`main`** following [merged PR #8](https://github.com/IjlalShah5/dctr-mcp-tool-revalidation/pull/8). The initial merge commit `ce25966a67c92638c64bcdca780022bfd0fe8534` passed [main-branch CI #40960388584](https://github.com/IjlalShah5/dctr-mcp-tool-revalidation/actions/runs/40960388584): **87 primary tests and 20 official MCP SDK tests passed**, and the upstream immutable-source audit succeeded. Later documentation-only commits must be checked against their own CI before treating their heads as tested. The version identifier in `scripts/interaction_v2.py` is explicitly experimental; no `v2.0` Git tag or production guarantee is asserted. See [Round-4 interaction-aware evidence](docs/round4-interaction-aware-sdk-evidence.md).

**Evidence scope:** the N2 natural 20-contract/43-path replay establishes structural triggering only; independently frozen N3 and Study B annotator returns were verified by the authors off-repository and are not part of the 87+20 engineering CI; the S1 synthetic human-rating totals were withdrawn from the revised paper. Neither controlled test outcomes nor the source-snapshot replay establish real-world harmful-interaction detection, natural L4 prevalence or reduced unnecessary approvals. Keep participant records private pending ethics/consent approval.

## Revision status

The major-revision work was developed in PR #1 and the final post-review hardening in PR #2. Both revision sets are now merged into the default `main` branch so reviewers opening the repository see the complete submission artefact, including the dual-baseline integrity hardening, reliability precision diagnostics, and DCTR/Microsoft cross-tabulation.

## Round-3 extension — official MCP SDK integration (22 October 2026)

A second controlled integration step uses the **official MCP Python SDK `mcp==1.30.0`** with a real `ClientSession`, separate stdio subprocess server, `tools/list`/`tools/call`, SQLite grant persistence and per-invocation DCTR approval gating. Its **8 SDK-specific tests** pass in a dedicated CI job. The original dependency-free suite also adds two safe controlled tests for a *measurable local compound-effect witness*: two individually bounded test fields create a new combined action while max-path remains L2, and an experimental guard escalates uncertainty to L3 and prevents invocation. The former 58-test checkpoint remains historically valid; the then-current Round-3 verification job additionally collected **15 separate official SDK 1.28.0 tests**, making **73** in that job (38 original + 20 controlled stdio + 15 SDK 1.28.0) and **8** under SDK 1.30.0 in its own job: **81 test executions across two dependency environments**. These are overlapping controlled engineering checks, not 81 independent research cases. See [the official-SDK addendum](docs/round3-official-sdk-addendum.md) for test design and limitations.

The [immutable-source provenance audit](docs/round3-multi-repository-evidence-scope.md) additionally verifies seven source-literal maintainer events from three repositories. These are not complete runtime Tool captures and have no human L0–L4 labels. The distinct 20-Tool, 43-path, 14-cluster Stage3N source-snapshot cohort is also UNLABELLED and remains one repository. Neither cohort should be silently pooled with the completed human-rated natural pilot.

Separately, a [multi-repository natural-change screening register](data/round3_screening/natural_candidate_screening_20261022.csv) records source-linked *candidate* commits across filesystem, Chrome DevTools and Firecrawl MCP servers. **These are not yet eligible fully reconstructed Tool-contract transitions and have no independent human severity labels.** Do not add them to the historical, supplementary, or independent pilot denominators. The next separate 24-fixture controlled boundary study has prepared blinded materials but **no human ratings yet**.

## Round-2 reviewer corrections on main

The current `main` code includes round-2 corrections without creating a separate branch:

- **Missing-baseline fail-closed handling (14 October 2026):** A genuinely new Tool has no grant and neither anchor; only this fully absent state takes `INITIAL_TRUST`. A partially missing approval state instead returns `BASELINE_MISSING` / `BLOCK` with a persisted quarantine marker. Five additional regression tests verify this distinction.
- **Persistent quarantine:** `TrustState.quarantine` preserves an L4/policy-block lifecycle lock. Normal refreshes cannot resume a blocked grant; `recover_quarantine()` requires remediation confirmation and explicit human approval. Integrators must durably persist this state and deny Tool execution during quarantine.
- **Primary evidence synchronization:** `data/transitions.csv` hashes and all P01-P04 delta paths are reconciled with the stored contracts. `data/primary_path_evidence.csv` supplies 12 exact path/TSV/rule/rationale records marked as author-coded development references.
- **Corrected reliability statistic:** The true ordinal-distance Krippendorff alpha is **0.708117** (reported as 0.708), not 0.764. The prior result was interval-distance alpha. Primary linear-weighted kappa remains 0.720.
- **Regression verification:** `python -m unittest discover -s tests -v` and `python scripts/verify_primary_evidence.py`. The GitHub workflow `.github/workflows/reproducibility.yml` is configured to run them on main commits.

See `docs/round2-reviewer2-corrections.md`. **The journal manuscript PDF and reviewer response uploaded to SuSy must still be revised separately; repository changes do not automatically change those submissions.**

## What DCTR evaluates

DCTR asks whether a prior approval remains transferable when an authenticated, client-visible Tool contract changes. The artefact separates:

1. deterministic change evidence — RFC 8785/JCS canonical identity, SHA-256, direction-preserving recursive deltas, and fail-closed consistency checks;
2. security-semantic interpretation — explicit TSV/reference-policy coding;
3. trust-renewal state — an operational grant-bound baseline plus a separately digest-bound last human-reviewed anchor used to detect cumulative staircase drift.

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
- ordinal Krippendorff alpha: **0.708**;
- cluster-macro exact agreement: **94.5%**;
- pattern-deduplicated exact agreement: **96.4%**.

Post-protocol precision diagnostics (50,000 percentile-bootstrap resamples; seed 20260926)
give a unit-resampled kappa 95% interval of **0.472-0.905** and a cluster-resampled
interval of **0.146-1.000**. These intervals were added after the frozen protocol and are
reported as transparency diagnostics, not pre-specified inference.

Six disagreements were localized to the coordinated Playwright filename/path-description cluster and were adjudicated by A+B consensus to R2a/L2 after the independent metrics were frozen.

The natural held-out set contains only one L3 path unit and no L4 path unit. The manuscript therefore treats reliability at L2/L3 and L3/L4 as a limitation rather than implying that the natural sample validates every policy boundary. The controlled conformance fixtures cover those rules only as author-defined design tests, not as independent natural-label evidence.

The two annotators consented to participation and to publication of anonymized annotation outputs and broad professional-background descriptors. No direct identifiers or sensitive personal data are published.

See `docs/heldout-annotation-results.md` and the final annotation data files under `data/`.

## External comparison

`data/baseline_comparison_36.csv` covers all 36 natural mutations using:
- an ETDI-style reapproval-on-any-change decision baseline;
- Microsoft MCP Security Gateway documented specific schema-drift and rug-pull rules;
- DCTR development-set reference outputs for P01-P04 and held-out consensus outputs for the supplementary 32.

Unsupported Microsoft surfaces are recorded as `NOT_COVERED`; no severity is invented. `data/baseline_crosstab_36.csv` summarizes the DCTR/Microsoft decision structure without converting unlike scales into an accuracy ranking.

## Runtime triangulation

A three-case controlled subset is retained for Playwright screenshot scale, Playwright WebP/type-selection behavior, and Terraform `create_run` contract selection. These checks corroborate selected behavior only; they do not make DCTR a runtime detector.

## Artefact map

**Core reproducibility documents**
- `docs/DCTR-CB-1.0-FROZEN.md` — frozen semantic codebook used for held-out coding.
- `docs/annotation-protocol-heldout.md` — held-out design, blinding, outcomes, and later precision diagnostics.
- `docs/heldout-annotation-results.md` — pre-adjudication reliability, adjudication, disagreement analysis, and boundary limitation.
- `docs/formal-properties-phase11.md` — state properties, digest-integrity conditions, and scope conditions.
- `docs/deployment-semantic-stage.md` — explicit boundary between automated evidence/state handling and semantic classification.
- `docs/baseline-comparison-36.md` — ETDI/Microsoft/DCTR decision-structure comparison.
- `docs/runtime-validation-report.md` — controlled runtime-alignment subset.
- `docs/ethics-checkpoint.md` — anonymized expert-annotation governance and consent record.

**Core data**
- `data/primary_path_evidence.csv` — per-path P01–P04 evidence/TSV/rule/rationale, verified against contract JSON.
- `data/transitions.csv` — synchronized primary hashes and exact directional path lists.
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

## Validation status

The earlier Phase-12 checkpoint recorded a **25/25** offline run. The expanded Round-2 workflow subsequently passed **38/38 tests** and verified **4 primary transitions / 12 exact path-level semantic records** on 2026-10-14. [GitHub Actions verification run](https://github.com/IjlalShah5/dctr-mcp-tool-revalidation/actions/runs/38502489325). The workflow under `.github/workflows/reproducibility.yml` rechecks future main commits; check the latest run before citing a newer snapshot.

## Reproducibility discipline

No transition row, contract projection, source boundary, or semantic label is promoted into the artefact without retained evidence. Coordinated multi-Tool edits are reported at event and cluster level to avoid pseudo-replication. Pre-adjudication reliability remains distinct from post-consensus labels.

## Citation and release

A formal citation entry is provided in `CITATION.cff`. The reference code, controlled fixtures and historical verification artefacts are now on the default `main` branch; author-held N3/B expert returns and private study evidence are not automatically deposited. The manuscript and reviewer response should cite the exact tested `main` commit, acknowledging that private data permissions and author sign-off remain separate.

No archival GitHub release/Zenodo DOI is claimed until the authors explicitly create one.

## License

A repository license has not yet been selected by the authors. Until one is added, the repository remains publicly readable but no additional reuse rights are granted beyond those provided by applicable law.
