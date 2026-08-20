# Reconstruction Status

This file tracks the public-source reconstruction of the empirical corpus reported in the manuscript. Counts are promoted to **verified** only when the relevant Tool-level event can be tied to an immutable source boundary and, where a family has additional qualifying history, the corpus-selection rule is reproducible.

## Target reported by the manuscript

| Family | Reported transitions | Reported composition inferred from the four primary mutations |
|---|---:|---:|
| CXWorld/CapFrameX | 42 | 42 introductions |
| Shortcut | 18 | 17 introductions + 1 in-place mutation |
| Terraform MCP | 12 | 12 introductions |
| Playwright MCP | 10 | 7 introductions + 3 in-place mutations |
| **Total** | **82** | **78 introductions + 4 mutations** |

## Verified so far

### CXWorld/CapFrameX — 42/42 Tool introductions reconstructed

The family-level count is independently reproduced from four immutable source commits:

1. `10847c37903113bbddd66246236dba4733f1473d` — initial MCP implementation: **13 Tool introductions**.
2. `d5f9e3eddf70d65ca278a1707af750ce72d6bda2` — sensor and overlay configuration: **2 Tool introductions**.
3. `5a1aead8f33400297600c01e27580915e18306d4` — additional capture/config/analysis/sensor tools: **25 Tool introductions**.
4. `3bc6acae92a84db7f50542665226e1df3c6451d7` — PMD analysis: **2 Tool introductions**.

The exact 42 Tool identities and their absent→present boundaries are recorded in `data/capframex_introductions.csv`.

### Primary in-place mutations — 4/4 source boundaries verified

The four primary mutation cases have source-level before/after boundaries recorded in `data/primary_mutations.csv` and projections under `contracts/primary/`.

- Playwright run-code rename / RCE-equivalent warning — verified.
- Playwright screenshot scale semantics — verified at source level.
- Playwright screenshot WebP/default semantics — verified at source level.
- Shortcut documents-create HTML→Markdown semantics — verified.

A key correction emerged during reconstruction: the Shortcut mutation occurred at source commit `c0bf3cda72e4db3fba8f4b007644f9e907951574` on 2026-01-20. The later 2026-02-09 commit previously used as a candidate changes README wording only and is retained as secondary documentation evidence.

### Shortcut — 17 Tool introductions reconstructed at immutable source boundaries

The manuscript-implied Shortcut composition is 17 introductions plus the verified `documents-create` mutation. The 17 introduction rows have now been reconstructed and recorded in `data/shortcut_introductions.csv`.

The reconstruction resolves into two same-day source clusters on 2025-03-10:

1. `78607f0b67814873e03da1772271851fd0466baf` relative to parent `8bbd6224f3874f223a974c1b7f23214e8352dc8c`: **10 Tool introductions** (`get-current-user`, Story/Iteration/Epic/Objective read/search Tools). The commit creates the MCP server's initial Tool surface.
2. `02599fbde607890315031debbe04c1f9901589df` relative to parent `ecbe7af97d6570dfeb50de988e475b04eba773d6`: **7 Tool introductions** (`create-story`, owner assignment/unassignment, Team read/list, Workflow read/list). The source diff explicitly adds Team and Workflow Tool registries and expands Story Tools.

The 17 rows are independently source-verified as absent→present transitions. They are currently marked `manuscript-consistent-family-boundary`: unlike CapFrameX, the public Shortcut history contains many later Tool additions, so the artifact still needs to document the original corpus observation rule explaining why these 17 introductions plus the later `documents-create` mutation constitute the manuscript's 18 Shortcut transitions. The Tool events themselves are verified; the exact family-level sampling rule remains to be reconstructed.

### Terraform MCP — 12 source-verified introduction candidates, corpus boundary not yet reproducible

Twelve absent→present Tool introductions that match the manuscript's reported family count have now been reconstructed and recorded in `data/terraform_introductions.csv`:

- `attach_policy_set_to_workspaces`
- `get_token_permissions`
- `list_stacks`
- `get_stack_details`
- `list_workspace_policy_sets`
- `get_plan_json_output`
- `get_plan_details`
- `get_plan_logs`
- `get_apply_details`
- `get_apply_logs`
- `get_sentinel_mock`
- `force_unlock_workspace`

Each row is tied to a direct maintainer commit that adds and registers the Tool. However, these rows are currently marked `provisional-boundary-match`, not final corpus rows, because the public repository contains additional Tool introductions after `force_unlock_workspace`, including `list_state_versions`, `get_state_version`, and `get_run_comments`, followed by further August 2026 additions. Therefore the manuscript's exact Terraform count of 12 cannot be independently reproduced from repository history alone until the original observation-window/release-selection rule is identified and shown to exclude those later introductions.

This is an important reproducibility finding: source evidence verifies the 12 candidate transitions themselves, but not yet the rule that makes exactly those 12—and no later additions—the empirical Terraform corpus.

### Playwright MCP — 7 source-verified introduction candidates, corpus boundary not yet reproducible

Seven absent→present Tool introductions that match the manuscript-implied Playwright composition have now been reconstructed from the authoritative upstream `microsoft/playwright` Tool source and recorded in `data/playwright_introductions.csv`:

- `browser_show_tracing`
- `browser_network_state_set`
- `browser_drop`
- `browser_annotate`
- `browser_video_show_actions`
- `browser_video_hide_actions`
- `browser_find`

The corresponding immutable source commits are `8d4588c85ce362f9bf43108e5cd0ee5eb7e3f9a9`, `6fd3cb4c45cbc4fc4ef2fde36624f91bfc3abd81`, `f9f8fff0e09276062e3ace017b4c01d145de63e8`, `b19250e9c6456939b551b222d14bb8e343de2949`, `20e51e78570f3a09e16888b20eb5aea10e725d36` (two Tool introductions), and `9725152dac40ed511098664fcd253b545f67e7f0`.

Each commit directly adds a Tool schema to the MCP Tool registry, so the individual introduction events are source-verified. They remain marked `provisional-boundary-match` because the upstream repository contains other MCP Tool introductions outside this seven-event set. The downstream `microsoft/playwright-mcp` repository is primarily a packaging/synchronization layer for upstream Tool definitions and therefore cannot by itself explain why these seven introductions—and no other upstream Tool additions—constitute the manuscript's reported Playwright introduction subset.

The three Playwright in-place mutations are separately source-verified, so the reported family arithmetic of **7 introductions + 3 mutations = 10 transitions** can now be reproduced at the event-identity level. What remains unresolved is the exact observation/release-selection rule that makes this ten-event set the intended empirical Playwright corpus.

## Verified transition coverage

At the **Tool-event identity and immutable-boundary level**, source evidence now exists for all **82 events implied by the manuscript's family arithmetic**:

- 42 CapFrameX introductions;
- 17 Shortcut introductions;
- 12 Terraform introduction candidates;
- 7 Playwright introduction candidates;
- 4 primary in-place mutations.

This reproduces the reported arithmetic **78 introductions + 4 mutations = 82 Tool events** without inventing event identities or commit boundaries.

However, this does **not** yet establish that the manuscript's exact 82-row selected corpus is independently reproducible. The distinction is important:

- **CapFrameX**: family count and source boundaries are independently reproduced.
- **Shortcut**: all 17 introductions and the mutation are source-verified, but the family observation/selection rule is not yet explicit enough to explain exclusion of later Tool additions.
- **Terraform**: all 12 candidate introductions are source-verified, but the selection cutoff is unresolved.
- **Playwright**: all seven candidate introductions and three mutations are source-verified, but the selection cutoff is unresolved.

Therefore the current artifact supports the statement that **82 source-backed Tool events matching the manuscript's reported composition have been reconstructed**, while the stronger statement **“the exact 82-row corpus has been independently reproduced under a fully specified sampling rule”** remains pending.

## Important serializer caveat

For code-defined Tool schemas, source changes can establish field names, enums, defaults, descriptions, and optional/default semantics directly. Exact JSON-Schema `required` arrays can depend on the serializer/library revision. Therefore the repository does not infer serialized required-list changes solely from Zod syntax. See `docs/projection-notes.md`.

This caveat means the manuscript wording that currently states exact screenshot `required`-list transitions must be checked against an actual serialized Tool object before final submission. If that wire-level effect cannot be reproduced, the manuscript will be revised to state the source-verified default/optionality change instead.

## Next reconstruction work

1. Reconstruct the corpus-selection rule by identifying the observation/release cutoffs used for Shortcut, Terraform, and Playwright. If no defensible common or family-specific rule can be recovered, flag the affected manuscript family totals as a provenance limitation rather than forcing a retrospective rule.
2. Reconcile the reconstructed source/release boundaries against the manuscript's reported **20 release clusters**.
3. Build a unified machine-readable manifest that assigns each reconstructed event a source boundary, family, transition type, cluster identifier, and membership status.
4. Generate a machine-checkable `verification_report.md` summarizing event counts, unresolved boundaries, and any manuscript corrections required.
5. Update the manuscript corpus-provenance table and Data Availability Statement from the final public artifact.
