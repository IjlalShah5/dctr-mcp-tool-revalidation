# Stage3N: launch instructions for two independent annotators

**Status:** original evidence packets ready; NO completed new annotations yet. The researcher has confirmed two prospective annotators are available, but consent and actual unassisted returns have not been received or verified.

**Pinned public evidence commit:** `217a553738bc9552d6cae6ad5d5b1f088ee1a180`.

## Send separately (after affirmative, study-specific consent)

- Annotator A ONLY: https://raw.githubusercontent.com/IjlalShah5/dctr-mcp-tool-revalidation/217a553738bc9552d6cae6ad5d5b1f088ee1a180/data/round3_stage3_natural_candidates/Stage3N_Annotator_A_UNFILLED_43_Paths.csv
- Annotator B ONLY: https://raw.githubusercontent.com/IjlalShah5/dctr-mcp-tool-revalidation/217a553738bc9552d6cae6ad5d5b1f088ee1a180/data/round3_stage3_natural_candidates/Stage3N_Annotator_B_UNFILLED_43_Paths.csv
- BOTH: https://raw.githubusercontent.com/IjlalShah5/dctr-mcp-tool-revalidation/217a553738bc9552d6cae6ad5d5b1f088ee1a180/docs/DCTR-CB-1.0-FROZEN.md

The prebuilt packets contain the *same 43 exact changed path units* in separate randomized orders, including exact path value and complete before/after Tool JSON. Each has 12 BLANK response fields and no author severity labels. The underlying cohort is 20 mutations/14 maintainer clusters in ONE repository. Snapshots come from immutable maintainer-generated source artefacts, NOT observed MCP wire captures.

## Human study administration

1. Check institution-specific ethics requirements and obtain new affirmative consent covering this 43-path cohort; obtain separate permission before publishing anonymous outputs. Keep signed consent private.
2. Confirm two qualified non-author raters, relevant prior DCTR roles and conflicts. Use independently randomized A/B forms and the identical frozen codebook.
3. Annotators fill TSV dimensions, primary R rule, minimum L action, confidence, rationale and uncertainty. Codebook explicitly permits UNCERTAIN; do not force an L0-L4 guess or use AI judgments.
4. They work without collaborating, sharing case labels, browsing author answer keys or receiving supervisor feedback about individual severity until original responses are both frozen.
5. Collect each completed CSV privately and hash both original returns (SHA-256) BEFORE comparing labels; validate no evidence/identifier modifications and no inconsistent R/L mapping. Preserve originals; separately retain adjudication.
6. Report all 43 units including UNCERTAIN counts. Weighted kappa based on both-ordinal rows is *conditional* and must list its smaller denominator; report raw disagreements and repository-cluster bootstrap limitations.
7. Do not pool old 34-path, Round3 natural pilot 21-path, new Stage3N 43-path, source-level multi-repo screening or synthetic test fixtures. Do not infer security correctness from inter-rater agreement; no natural L4 is guaranteed.

A separate local consent-and-freeze kit has been generated for administration; do not publish participant names, original signatures or raw confidential identifiers in this repository.

**This file records a prospective procedure, not completed independent validation.**
