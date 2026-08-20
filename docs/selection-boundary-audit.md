# Corpus Selection-Boundary Audit

## Purpose

The manuscript's retained empirical corpus contains 82 Tool-level events grouped into **20 maintainer change clusters**. Public-source reconstruction now identifies all 82 events (78 introductions and four in-place mutations) and maps them to the 20 retained clusters in `data/cluster_manifest.csv`.

This audit separates three claims that must not be conflated:

1. **Event verification:** an individual Tool event can be tied to immutable maintainer-authored evidence.
2. **Cluster reconstruction:** the 82 retained events can be assigned to the 20 maintainer change clusters used by the revised manuscript.
3. **Historical selection-rule reproducibility:** an independent researcher can recover the same retained event set solely by replaying the original observation/release cutoff that was used during acquisition.

The first two claims are now supported by the public artifact. The third remains partially unresolved for Shortcut, Terraform, and Playwright because the original historical observation cutoff was not retained with enough precision to explain every exclusion of later qualifying Tool additions.

## Family-level status

| Family | Retained events | Retained change clusters | Reconstruction status |
|---|---:|---:|---|
| CXWorld/CapFrameX | 42 | 4 | Event identities and family grouping reproduced |
| Shortcut | 18 | 2 | Event identities and retained grouping reproduced; historical cutoff unresolved |
| Terraform MCP | 12 | 6 | Event identities and retained grouping reproduced; historical cutoff unresolved |
| Playwright MCP | 10 | 8 | Event identities and retained grouping reproduced; historical cutoff unresolved |
| **Total** | **82** | **20** | Authoritative retained manifest reconstructed |

The machine-readable cluster record is `data/cluster_manifest.csv`. It is the authoritative manifest for the revised manuscript and should be used when reproducing the reported family and cluster arithmetic.

## Why the historical cutoff still matters

Shortcut, Terraform, and Playwright contain additional Tool additions outside the retained set. A retrospective rule such as “take the first N additions” would be scientifically unacceptable unless that rule can be shown to have been part of the original acquisition design. Likewise, choosing a date solely because it yields the reported family count would constitute post-hoc count fitting.

A historically reproducible selection rule would require independently motivated evidence such as a documented collection cutoff, frozen release/tag boundary, archived acquisition manifest, common observation date, or another rule fixed before the family counts were considered. That original selection metadata has not yet been recovered for all three histories.

## Current implication for the manuscript

The public artifact supports the following statement:

> We reconstructed 82 immutable, source-backed Tool events matching the retained study corpus and reconciled them into 20 maintainer change clusters documented in the authoritative public manifest. The event identities and retained cluster grouping are auditable; however, the original historical observation cutoff for three project histories could not be recovered with sufficient precision to claim that the same 82-event selection can be regenerated solely from the original unstated acquisition rule.

The artifact does **not** support the stronger statement:

> An independent researcher can regenerate the exact 82-event selection solely by replaying a fully specified original observation cutoff.

## Remaining checks

1. Continue searching retained project artifacts for an explicit historical observation date, release whitelist, or acquisition manifest.
2. Preserve `data/cluster_manifest.csv` as the authoritative retained corpus grouping unless stronger original acquisition metadata is recovered.
3. Keep the historical-cutoff limitation explicit in the manuscript and Data Availability materials.
4. Do not silently add later qualifying events to the retained corpus without defining a new prospective sampling protocol and reporting it as a separate dataset.

## Integrity rule

Counts are not forced by inventing a cutoff, silently excluding inconvenient history, or fabricating metadata. Event verification and retained-cluster reconstruction are reported separately from historical selection-rule reproducibility.