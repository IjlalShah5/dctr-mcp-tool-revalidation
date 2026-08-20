# 20-Cluster Reconciliation

## Result

The manuscript's reported total of **20 maintainer change clusters** can be reconstructed from the source-backed 82-event set under an explicit grouping rule documented in `data/cluster_manifest.csv`.

This audit uses the term **maintainer change cluster** rather than assuming that every cluster is a formal tagged release. A cluster is one retained maintainer boundary or one tightly coupled retained rollout whose Tool-level events are decomposed into individual rows for analysis.

## Grouping rule

A cluster is formed using the following precedence:

1. **Single immutable source boundary:** all retained Tool events introduced or mutated by the same maintainer commit are one cluster.
2. **Downstream package release exposure (Playwright):** when the authoritative Tool source lives upstream but the distributed `playwright-mcp` package exposes multiple retained changes together, the downstream tagged/version-marked release is used as the cluster boundary.
3. **Contiguous initial rollout (Shortcut):** the initial Tool-surface commit and its same-day contiguous expansion are treated as one retained rollout cluster because they are on one ancestry path and constitute the study's initial retained Tool surface.
4. **Same unreleased changelog rollup (Terraform):** same-day Tool PRs that accumulate into the same unreleased CHANGELOG development surface are grouped as one change cluster.

The grouping rule affects only cluster accounting; it does not merge Tool-level transition rows.

## Family cluster counts

| Family | Tool events | Reconstructed clusters |
|---|---:|---:|
| CXWorld/CapFrameX | 42 | 4 |
| Shortcut | 18 | 2 |
| Terraform MCP | 12 | 6 |
| Playwright MCP | 10 | 8 |
| **Total** | **82** | **20** |

## Playwright release-level checks

The downstream generated Tool listings provide particularly strong release exposure evidence:

- v0.0.71 (`f27ff153...`) lists `browser_run_code` and does not list `browser_annotate`.
- v0.0.72 (`5ae9c9e...`) lists `browser_run_code_unsafe` with the RCE-equivalent warning and lists `browser_annotate`. Those two retained changes therefore share the v0.0.72 exposure cluster.
- v0.0.77 (`36ec986...`) lists screenshot `scale` as a non-optional parameter with `css|device` semantics and default `css`.
- v0.0.78 (`7d36e7c...`) contains the retained `browser_find` Tool.
- v0.0.79 (`4c507765...`) lists screenshot `type` as optional, adds WebP, keeps `scale` non-optional, and documents filename inference.

These generated listings also resolve the earlier serializer caveat for the two screenshot cases at the documentation/projection level used by the paper: the distributed Tool listing marks `scale` as required after its introduction, and marks `type` as required before the WebP change but optional after it. The manuscript's direction claim `[type, scale] -> [scale]` is therefore supported by the generated release-level Tool documentation, although the artifact still distinguishes generated Tool documentation from captured MCP wire traffic.

## Terminology correction recommended for the manuscript

Because several clusters are immutable commit/rollout boundaries rather than independently tagged releases, the paper should replace the phrase **"20 release clusters"** with **"20 maintainer change clusters"** (or "20 release/commit clusters") throughout. This retains the verified count while avoiding a stronger claim than the evidence supports.

## Scope limitation that remains

The 82 retained events and their 20-cluster grouping are now auditable from the reconstructed manifest. However, the original acquisition cutoff for Shortcut, Terraform, and Playwright is still not recoverable as a single pre-existing observation rule from the manuscript alone. The final paper should therefore distinguish:

- **reconstructed retained corpus:** 82 source-backed Tool events in 20 documented maintainer change clusters; and
- **historical sampling provenance:** exact original cutoff/selection rule could not be independently recovered for three families.

This limitation does not invalidate the retained-event analysis, but it should be stated in Methods/Limitations and the public manifest should be treated as the authoritative reproducibility record for the submitted version.
