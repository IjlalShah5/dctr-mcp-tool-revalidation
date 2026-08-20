# Corpus Selection-Boundary Audit

## Purpose

The manuscript reports 82 Tool-level transitions across 20 release clusters. Public-source reconstruction now identifies 82 Tool events whose family composition matches the reported arithmetic (78 introductions and four in-place mutations). This audit separates two claims that must not be conflated:

1. **Event verification:** an individual Tool event can be tied to an immutable maintainer-authored before/after boundary.
2. **Corpus-selection reproducibility:** an independent researcher can apply a stated observation/release rule and recover exactly the same event set and release-cluster grouping.

The first claim is now substantially supported for the reported 82-event composition. The second remains partially unresolved for Shortcut, Terraform, and Playwright because the manuscript does not currently state family-specific observation cutoffs with enough precision to explain why later qualifying Tool additions are excluded.

## Family-level status

| Family | Reported events | Reconstructed source-backed events | Selection-boundary status |
|---|---:|---:|---|
| CXWorld/CapFrameX | 42 | 42 | Reproduced at family level |
| Shortcut | 18 | 17 introductions + 1 mutation | Event identities reproduced; observation cutoff unresolved |
| Terraform MCP | 12 | 12 introductions | Event identities reproduced; observation cutoff unresolved |
| Playwright MCP | 10 | 7 introductions + 3 mutations | Event identities reproduced; observation cutoff unresolved |
| **Total** | **82** | **82** | Event arithmetic reproduced; exact sampling rule not yet fully reproduced |

## Why a cutoff is necessary

All three unresolved histories contain additional Tool additions outside the reconstructed manuscript-matching subset. A retrospective rule such as “take the first N additions” would be scientifically unacceptable unless that rule can be shown to have been part of the original acquisition design. Likewise, choosing a date solely because it yields the desired family count would constitute post-hoc count fitting.

A defensible rule must be independently motivated by evidence such as:

- a documented literature/data collection cutoff;
- a frozen release/tag boundary;
- an archived acquisition manifest;
- a common observation date applied consistently across repositories;
- or another rule stated before the family counts are considered.

## Current implication for the manuscript

Until the selection rule is recovered, the public artifact supports the following narrower statement:

> We reconstructed 82 immutable, source-backed Tool events whose family composition matches the retained study corpus: 78 introductions and four in-place mutations. Family-level event identities are auditable; however, the original observation cutoff for three histories could not yet be recovered with sufficient precision to claim independent reproduction of the corpus-selection rule.

The artifact does **not** yet support the stronger wording:

> An independent researcher can regenerate the exact 82-row corpus solely from the published acquisition procedure.

## Required next checks

1. Map every reconstructed event to downstream release/tag exposure where applicable.
2. Search retained manuscript/project artifacts for an explicit observation date, release whitelist, or acquisition manifest.
3. Test whether one non-post-hoc cutoff recovers the reported Shortcut, Terraform, and Playwright sets simultaneously.
4. Reconcile the resulting boundaries with the manuscript's reported 20 release clusters.
5. If no defensible rule is recoverable, revise the paper to state this as a provenance limitation and publish the reconstructed immutable event manifest as the authoritative dataset.

## Integrity rule

Counts will not be forced to match the manuscript by inventing a cutoff, silently excluding later events, or fabricating historical metadata. Where retained study metadata and public history disagree, the manuscript will be corrected or the limitation will be stated explicitly.
