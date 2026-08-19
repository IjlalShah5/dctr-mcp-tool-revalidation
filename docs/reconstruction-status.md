# Reconstruction Status

This file tracks the public-source reconstruction of the empirical corpus reported in the manuscript. Counts are promoted to **verified** only when the relevant Tool-level event can be tied to an immutable source boundary.

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

The family-level count is now independently reproduced from four immutable source commits:

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

## Verified transition coverage

At this stage the public artifact has source-level evidence for:

- 42 CapFrameX introductions;
- 4 primary in-place mutations.

That is **46 of the reported 82 Tool-level transitions**. The remaining reconstruction target is **36 introductions**:

- Shortcut: 17;
- Terraform MCP: 12;
- Playwright MCP: 7.

These numbers are reconstruction targets derived from the manuscript totals, not yet promoted to verified corpus rows.

## Important serializer caveat

For code-defined Tool schemas, source changes can establish field names, enums, defaults, descriptions, and optional/default semantics directly. Exact JSON-Schema `required` arrays can depend on the serializer/library revision. Therefore the repository does not infer serialized required-list changes solely from Zod syntax. See `docs/projection-notes.md`.

This caveat means the manuscript wording that currently states exact screenshot `required`-list transitions must be checked against an actual serialized Tool object before final submission. If that wire-level effect cannot be reproduced, the manuscript will be revised to state the source-verified default/optionality change instead.

## Next reconstruction work

1. Reconstruct the 12 Terraform Tool introductions and their release/commit clusters.
2. Reconstruct the 17 Shortcut Tool introductions selected by the original corpus boundary.
3. Reconstruct the 7 Playwright Tool introductions selected by the original corpus boundary.
4. Reconcile the reconstructed cluster count against the manuscript's reported 20 release clusters.
5. Generate a machine-checkable final audit (`verification_report.md`) and update the manuscript Data Availability Statement.
