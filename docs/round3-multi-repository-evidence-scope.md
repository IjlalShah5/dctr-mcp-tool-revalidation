# Round 3 evidence-scope note: multiple MCP repositories (22 October 2026)

**Do not interpret source-diff discovery as L3/L4 independent validation.**

## Three different units of evidence

| Cohort / purpose | Tool transitions | Changed paths | Maintainer clusters | Repositories | Independent A/B coding? | Evidential status |
|---|---:|---:|---:|---:|---|---|
| Existing Round 3 natural pilot | 10 | 21 | 4 | 1 (`github/github-mcp-server`) | Yes | 18/21 exact agreement, κ=0.877; final four L3 paths in same cluster, zero L4 |
| Existing Stage3N reconstructed natural candidate pool | 20 | 43 | 14 | 1 (`github/github-mcp-server`) | **No** | Reproducibly reconstructed full maintainer-generated .snap snapshots; not actual `tools/list` wire captures |
| **New external multi-repository source audit** | 7 source events | **Not yet counted as exact runtime contract paths** | 7 | 3 | **No** | Matched immutable source blobs, detected literal Tool declaration changes only; SDK projection/wire-traffic checks remain |

The seven external source events are FS01–FS03, CD01, CD03, FC01–FC02. They concern filesystem-server annotations/descriptions, Chrome DevTools MCP read-only hints/description and Firecrawl MCP descriptive/schema guidance. The audit is intentionally source-literal; configuration, schema factories, runtime versions and Tool discovery may affect the complete effective contract. The single FS03 object in `FS03_source_reconstructed_not_wire.json` is a statically reconstructed Tool object, explicitly *not* live captured traffic.

### Reproduce / verify

```bash
python scripts/verify_round3_natural_candidates.py
python scripts/verify_round3_natural_packets.py
python scripts/verify_round3_upstream_source_literals.py
python scripts/verify_round3_upstream_source_literals.py --online
```

The last command retrieves both source blobs at each of seven immutable upstream first-parent commit boundaries, re-hashes each blob using Git's own object-identity algorithm, and confirms the recorded Tool-definition source change in the relevant declaration. The published case registry includes exact Git blob hashes and changed-source markers, but **no severity labels**. Raw source owners retain their respective licences.

### Independent validation required before claims change

1. For the three new upstream repositories, obtain SDK-pinned and configuration-pinned *complete* before/after `tools/list` Tool objects; retain observed response JSON separately from manual source projection.
2. Compute JCS identity and direction-preserving exact JSON Pointer deltas for every eligible runtime listing. Exclude cases that changed implementation without changing the advertised Tool object.
3. Obtain separate affirmative consent for the new multi-repository cohort, supply two independently randomized evidence packets, and freeze both original sets of L0–L4 judgments. No author-generated reference labels.
4. Estimate ordinal agreement with cluster-aware sensitivity and transparent per-repository limits; report naturally occurring L4 cases as **zero if zero**.
5. Never pool the original 34-path held-out test, the separate 21-path natural pilot, the new 43-path unlabelled Stage3N pool, this seven-event source audit, or the separate synthetic controlled 24/16-case studies.

### Integration CI accounting (not human evidence)

At the current `main` CI, the `verification` job runs **73 automated tests**: 38 original regression tests, 20 controlled MCP-shaped subprocess tests, and 15 additional official MCP Python SDK 1.28.0 tests. The separate `official-mcp-sdk-integration` job runs **eight** tests under SDK 1.30.0. Thus **81 test executions across two pinned dependency environments**, not 81 independent empirical validation units. Those controlled engineering tests do not address the external L4-label scarcity or establish measured harm reduction.

### Annotation & privacy administration

The prospective, separate **16-pair / 32-path** all-minor-to-major controlled study awaits new consent and genuine independent Stage 1 returns; its Stage 2 remains escrowed. The earlier 24-case/45-path study has its raw independent responses frozen and seven human consensus questions still open. Source-screening files in this directory contain no identities, raw consent signatures, or private blinding maps. Never publish those confidential materials.
