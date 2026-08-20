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

## Verified transition coverage

At the Tool-event level, source evidence now exists for:

- 42 CapFrameX introductions;
- 17 Shortcut introductions;
- 4 primary in-place mutations;
- 12 Terraform introduction candidates.

That is **75 source-verified Tool events** associated with the reported corpus, of which **63** (42 CapFrameX + 17 Shortcut + 4 mutations) align with the manuscript-implied family composition without changing any Tool identity or event count. The remaining **12 Terraform events** are individually verified but await a reproducible family-selection cutoff before promotion to final corpus membership.

Remaining reconstruction work:

- Terraform MCP: resolve the selection rule for the 12 reconstructed candidates;
- Shortcut: document the family observation/selection rule that yields exactly the reconstructed 17 introductions plus the `documents-create` mutation;
- Playwright MCP: reconstruct the 7 introductions selected by the original corpus boundary;
- reconcile all reconstructed source clusters against the manuscript's reported 20 release clusters.

## Important serializer caveat

For code-defined Tool schemas, source changes can establish field names, enums, defaults, descriptions, and optional/default semantics directly. Exact JSON-Schema `required` arrays can depend on the serializer/library revision. Therefore the repository does not infer serialized required-list changes solely from Zod syntax. See `docs/projection-notes.md`.

This caveat means the manuscript wording that currently states exact screenshot `required`-list transitions must be checked against an actual serialized Tool object before final submission. If that wire-level effect cannot be reproduced, the manuscript will be revised to state the source-verified default/optionality change instead.

## Next reconstruction work

1. Reconstruct the 7 Playwright Tool introductions selected by the original corpus boundary.
2. Identify/document the observation or release-selection rules for Terraform and Shortcut; if they cannot be reproduced, flag the affected manuscript family totals for correction rather than forcing a match.
3. Reconcile the reconstructed cluster count against the manuscript's reported 20 release clusters.
4. Generate a machine-checkable final audit (`verification_report.md`) and update the manuscript Data Availability Statement.
