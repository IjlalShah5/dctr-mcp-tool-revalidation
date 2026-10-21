# DCTR Round 3 independent natural Tool-definition pilot: anonymized evidence

**Scope.** Ten natural Tool-level before/after mutations, 21 path units, four maintainer change clusters, from **one repository** (`github/github-mcp-server`). All changed evidence was reconstructed from maintainer-generated Tool snapshots at immutable commit pairs, **not captured MCP `tools/list` traffic**. N10 was configuration/feature-flag qualified. No representative prevalence or security-outcome claims are made.

The previous held-out evaluation of 34 path units across ten maintainer clusters (kappa 0.720; true ordinal alpha 0.708) is a distinct study. Denominators, reliability outcomes, and cohorts are not pooled.

## Files

- `DCTR_Round3_Adjudicated_21_Path_Units_ANONYMIZED.csv`: exact before/after changed-path values, operations, anonymized original A/B rules and levels, final consensus rules and levels, and source references. `ABSENT` is a deliberately explicit missing-value marker.
- `DCTR_Round3_Three_Joint_Consensus_Decisions_ANONYMIZED.csv`: the three disputed paths resolved **after** independent ratings were frozen.
- `DCTR_Round3_Stage2_Exploratory_Interaction_Responses_ANONYMIZED.csv`: independent, **delta-only** interaction screening on three multi-path Tool changes, all in one maintainer cluster.
- `upstream_immutable_snapshot_manifest.csv`: immutable source commit pairs and snapshot paths for all ten cases. Git blob identifiers are **not** JCS/SHA-256 contract digests.
- `scripts/verify_round3_public_pilot.py` at repository root: compute public reliability/consistency checks.

## Findings and reproducibility limits

**Independent pre-adjudication:** 18/21 (85.7%) exact level agreement, linear-weighted Cohen's kappa **0.876712** (0.877), genuine ordinal Krippendorff alpha **0.902713** (0.903); three disagreements (two L2/L3, one L1/L2). The exploratory cluster-bootstrap kappa 95% interval ~0.615–1.000 remains wide and is a post-protocol precision diagnostic.

**Final adjudication:** 21 levels: L0=5, L1=2, L2=10, L3=4, L4=0. **All four L3 path units come from the same change cluster.** At Tool-mutation level: 5 L0, 1 L1, 1 L2, 3 L3, 0 L4. The three original disagreements were jointly resolved without editing pre-adjudication ratings; consensus is **not** counted as perfect independent agreement.

**Exploratory Stage 2:** Both annotators answered YES for each of three Tool mutations and cited identical changed-path sets. Cohen's kappa is mathematically undefined here (all labels YES). All three cases share one change cluster **and already include individually L3-rated paths**; they do not establish a severe interaction arising solely from individually L0–L2 paths. Annotators saw exact changed-path evidence but **not full unchanged contracts**.

**No natural L4:** This pilot provides **zero independently annotated natural L4 cases**. Synthetic L4/SQLite-client experiments in `docs/round3-client-e2e-report.md` are controlled engineering validation, **not** independent natural severity evidence. There is no measured security-harm accuracy or general cross-path-classifier validation.

**Ethics and identity protection:** Anonymized individual coding and aggregate outcomes are released under the two annotators' recorded affirmative consent. Signed/private participation records, identities, unpublished identifier mappings, and administrator workbooks remain separately retained by the authors. No personal identifiers are included here. Original upstream files remain subject to their source licences; publication of these research files does not itself assert a new global reuse licence.

## Reproduce

```bash
python scripts/verify_round3_public_pilot.py
python -m unittest discover -s tests -v
python scripts/verify_primary_evidence.py
```

Do not conflate the 82-transition historical corpus, 36-mutation comparison, older 34-path held-out annotation, and this separate 21-path pilot. For client integration scope and remaining deployment gaps, see `docs/round3-client-e2e-report.md`.
