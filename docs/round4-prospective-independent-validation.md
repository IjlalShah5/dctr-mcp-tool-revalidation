# Round 4 prospective scientific validation — PROTOCOL ONLY

**Created:** 23 October 2026. **Status:** engineering tests/protocol drafted; no new independent judgments obtained. Not a completed experiment, ethics approval or public preregistration.

## Target questions

1. Can two consenting qualified non-author annotators independently reproduce L0–L4 path-level decisions, especially L2/L3 and L3/L4? Report untouched pre-adjudication labels, number of independent clusters with each boundary and uncertainty. Agreement is not proof of security correctness.
2. Can explicitly specified whole-delta guards prevent interaction outcomes from individual L0–L2 changes? Count unnecessary escalations and missed higher-order interactions. Safe author-defined fixtures are not external security ground truth.
3. Can state persistence and invocation gating under pinned official MCP Python SDK clients block an actual test-only Tool call, including after SQLite reopen? Existing tests support controlled client integration but not production deployment, TOCTOU elimination or real risk reduction.

## Mandatory disjoint denominators

- Historical 82 Tool events / 20 maintainer clusters (mostly introductions).
- Earlier held-out: 34 paths / 10 clusters, one L3, zero L4; 6 disagreements in coordinated Playwright changes.
- Separate natural pilot: 21 paths / 4 clusters, four L3 paths **in a single cluster** and zero L4.
- Pending Stage3N: 20 natural Tool mutations / 43 paths / 14 clusters, all within github/github-mcp-server. Maintainer-generated snapshots, NOT recorded tools/list traffic. Current independent A/B packets UNFILLED. Do not publish labels not obtained.
- Pending 3-other-repo source audit: seven verified source-literal events, NOT complete observed Tool-contract transitions, no severity labels. Require pinned SDK/feature-flag reconstruction, exact before/after client-visible objects, JCS canonical hashes and typed deltas. Exclude implementation-only events.
- Previously staged 24-case/45-path controlled study (independent raw results frozen, seven consensus questions open) and 16-pair/32-path study (new consent and Stage 1 returns pending) are separate synthetic arms. Do not pool with natural data.

## Steps for a real independent study

1. Obtain two qualified NON-AUTHOR human annotators and new informed consent; consult institutional ethics requirements, keep identity and signed forms private.
2. Freeze the existing DCTR-CB-1.0-FROZEN codebook, immutable source hashes and eligibility manifest. Supply complete BEFORE and AFTER client-visible Tool contracts, exact paths, operations, source and configuration qualifications. Randomize each annotator's packet order; hide author reference labels and the other person's decisions.
3. Independently record each path L0–L4, rule, uncertainty and rationale. Separately rate whole-contract interactions with full context. Freeze original A/B records and hashes before discussion.
4. After both independent stages, adjudicate disagreements in an audit trail WITHOUT overwriting original ratings. Never treat consensus as an independently correct ground truth or fabricate a missing natural L4.
5. Report exact and cluster-macro agreement, linear-weighted Cohen kappa, 5x5 cross-tab, L2/L3 and L3/L4 disagreements, separate L3/L4 independent cluster coverage and exploratory cluster-bootstrap 95% interval. Report undefined kappa and bootstrap replicates explicitly. If zero natural L4, state zero.

## Analyzer and CI

The input to scripts/round4_independent_boundary_analysis.py is a CSV with columns:

    unit_id,cluster_id,repository,rater_a_level,rater_b_level

Use only real, separately frozen PRE-ADJUDICATION A/B judgments. Run:

    python -m unittest discover -s tests -p 'test_round4*.py' -v
    python scripts/round4_independent_boundary_analysis.py --input FROZEN_AB.csv --output round4_agreement.json --bootstrap 5000 --seed 20261023

The analyzer does not fabricate ratings. Blank, non-L0–L4, duplicate or missing data fail loudly. Bootstrap resamples repository-qualified maintainer clusters with replacement, not individual paths. Reporting agreement does NOT demonstrate safety.

## Synthetic compound-change experiment — FIRST VERIFIED ENGINEERING RESULT

The separate safe author-designed test script (scripts/round4_interaction_stress.py) enumerates 16 switch configurations over three families: a known pair, an unknown triple interaction, and a benign pair. Every individual change is stipulated L2. The oracle is purely local and symbolic: no real MCP Tool execution, data exfiltration or human severity labels. Of the 13 configurations representing a change, 2 have an intentionally encoded compound effect.

| Toy policy | Compound outcomes not blocked | Benign configurations escalated |
|---|---:|---:|
| Maximum of isolated L2 paths | 2 | 0 |
| One known pairwise guard | 1 | 0 |
| Conservative review of any two or more changed fields | 0 | 4 |

This is a falsifiable *coverage vs. interruption* trade-off in an author-defined model. It is not a calibrated cross-path classifier, general security advantage or proof for real servers. Existing official MCP SDK integration cases test different, narrower client enforcement properties.

## Scientific decision gates

Do NOT add planned human work to the manuscript's finished results. Only report new boundary reliability after genuine independent coding with consent and frozen original returns. Cross-repository claims require eligible complete Tool contracts from more than one repository; source diffs alone do not count. Report zero L4 if no independently identified natural L4 exists. Separately report controlled policy stress evidence, production integration gaps and residual time-of-check/time-of-use uncertainty. Editor acceptance cannot be guaranteed.
