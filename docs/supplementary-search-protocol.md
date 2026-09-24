# Supplementary natural-mutation validation corpus — search protocol

## Purpose

The original empirical corpus contained 82 Tool-level transitions but only four present-to-present mutations. This supplementary corpus increases the number and structural diversity of **natural maintainer-authored Tool mutations** without rewriting the original 82-event sampling frame. It is a validation-extension corpus, not an ecosystem-prevalence sample.

## Discovery and inclusion

Repository-history scans were performed over Tool-definition directories in `CXWorld/CapFrameX`, `hashicorp/terraform-mcp-server`, and `microsoft/playwright`. Candidate commits were retained only when the Tool existed on both sides of an immutable maintainer boundary and at least one client-visible contract surface changed. Implementation-only edits, introductions, and withdrawals were excluded. Within each retained mutation cluster, all qualifying Tool-level contract mutations were kept.

The supplementary set contains **32 verified Tool-level present-to-present mutation events across 10 maintainer clusters and three server families**. Combined with the four original natural mutations, the revised evidence base contains **36 natural mutation events across 14 mutation clusters**, with at least one natural mutation from each of the four original server families.

## Counting discipline

Tool-level events and maintainer clusters are reported separately. Coordinated commits can mutate many Tools at once; event rows are therefore not treated as statistically independent observations. In particular, STFM01 contains ten annotation changes in one Terraform commit and SPLW01 contains eleven coordinated filename/path-description changes in one Playwright commit.

## Non-claims

This extension is not a probability sample and is not claimed to be an exhaustive census of all mutation history. It is used to improve mutation diversity and provide a larger natural set for subsequent independent annotation. Phase 5 does not assign validated L0-L4 ground truth to the supplementary rows.
