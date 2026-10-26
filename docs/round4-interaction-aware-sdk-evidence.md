# DCTR-IA-2.0 — Reviewer 1 algorithmic follow-up (research branch)

**Status:** Prospective experimental policy, 26 October 2026. Not merged into main, not a production MCP enforcement or security-risk classifier. Historical DCTR-CB-1.0, the 34-path held-out study, 21-path natural pilot, comparator data and original author labels remain unchanged.

## Why the change exists

The frozen reference engine composes local and cumulative path-level minimum actions. Two individually L2 changes can introduce an effect that is not inferred from either path in isolation. DCTR-IA-2.0 therefore adds an explicit **whole-contract interaction assessment** at both operational and cumulative comparison points.

For interaction-sensitive changes, the engine receives a separately sourced whole-contract assessment bound to RFC 8785/JCS before/after digests. If the assessment is missing, stale, insufficient or uncertain, the candidate does **not** get automatic continuation; the reference engine returns a *pending L3 human review action*. That action is a conservative policy decision, **not** a human-validated semantic L3 ground-truth label.

A supported material interaction may escalate to L3. L4 is reserved for an explicit R4 deception/evasion rationale, subject to the same canonical hash binding; neither a hash match nor a rationale string alone independently validates the expert's correctness. Single bounded changes retain normal L0–L2 treatment unless they involve relational/opaque schema edits. Existing confirmed path-level L4 is never downgraded.

### Authoritative implementation path in this research branch

- \`scripts/interaction_v2.py\`: prospective \`revalidate_v2\` entry point. It wraps the unmodified historical \`revalidation_state.revalidate\` for audit reproducibility.
- \`scripts/round4_official_sdk_gateway.py\`: real official MCP SDK \`ClientSession\` stdio adapter using \`revalidate_v2\` at refresh and SQLite trust-state persistence before invocation. Prior to \`tools/call\`, it rechecks the live \`tools/list\` contract digest and the stored operational/human baselines.
- \`tests/test_round4_real_core.py\`: eight direct nonstubbed original-engine interaction tests.
- \`tests/sdk_round4_interaction_aware_integration.py\`: eight real official MCP SDK 1.30.0 stdio tests. Controlled server, controlled Tool definitions and synthetic public canary; no real network exfiltration or production host.
- \`tests/test_round4_natural_snapshot_replay.py\`: two tests replaying 20 natural-source Tool-snapshot before/after pairs (43 changed paths; 14 maintainer clusters) under a **hypothetical all-L2 fixture rule**. This exercises policy mechanics only and does not label or validate natural severity.

## Evidence and key negative controls

Official SDK tests cover: previously approved baseline; an unassessed two-path change pending before call dispatch; an explicitly author-assessed L3 interaction pending; single L2 bounded continuation; two sequential individually bounded changes caught by the **cumulative** whole-contract gate; author-assessed benign paired change allowed; a benign unassessed pair generating an **extra review**; stale hash-bound assessment rejected; author-defined R4 quarantine persisted across SQLite client/server reopen.

The important **negative result** is extra human review for multi-path *safe* controls when no independent whole-contract assessment is supplied. Fail-closed policy is not the same as accurate high-risk classification or reduced review burden.

Snapshot replay consumes actual version-pinned maintainer-generated Tool-definition fixtures. It does **not** replay tools/list traffic, invent independent R3/R4 labels or provide evidence that human adjudicators agree on the L2/L3/L4 boundaries.

### Reproducibility

Both CI jobs are triggered by pushing this branch (\`round3/**\`) under \`.github/workflows/reproducibility.yml\`:

\`\`\`sh
python -m unittest discover -s tests -v                  # mcp==1.28.0 pinned
python -m unittest discover -s tests -p 'sdk_*.py' -v   # mcp==1.30.0 pinned
python scripts/verify_round3_public_pilot.py
python scripts/verify_round3_natural_candidates.py
python scripts/verify_round3_natural_packets.py
python scripts/verify_primary_evidence.py
\`\`\`

Use the latest successful run of this branch, not a previous main-branch CI count, when reporting technical results. Unit, SDK and snapshot replays are **not independent natural research observations**.

## Four Round-4 reviewer comments: allowable claims

1. **Two individually L2 changes:** the prospective policy now assesses joint contract effects and conservatively prevents automatic continuation if unresolved; real SDK tests exercise this enforcement.
2. **Guard scope and multiple scenarios:** whole assessment is a versioned policy entry point rather than the prior one-off literal-path guard; several positive/negative/cumulative controlled cases and source-derived snapshots exercise it. This still does **not** establish sensitivity/specificity or natural interaction detection accuracy.
3. **Independent natural L3/L4 evidence:** remains open. Four previously adjudicated natural L3 paths share one maintainer cluster, and no independently annotated natural L4 is available. The unlabeled 43-path Stage3N cohort and seven cross-repository source events are not substitutes for independent human judgments and pinned actual tools/list captures.
4. **ETDI and Microsoft comparisons:** keep Table 7 explicitly scoped to **policy-design/decision-structure differences**. Synthetic fixture outcomes may be shown separately as measured local gate behavior, never as real-world security benefit, fewer false positives, or better detection than independently implemented production comparators.

## Remaining work before revised MDPI submission

Independent consented natural labels and cross-cluster reliability; diverse real full contract before/after captures where feasible; stronger author-independent whole-contract assessments, including safe/unsafe cases and uncertainty; source and reviewer response synchronized with the **exact** latest journal-submitted manuscript; explicit ethics/coauthor/declaration checks; code review before a possible main-branch merge. Review acceptance cannot be guaranteed.

**Security limits:** not a general automatic interaction-risk detector; no SDK v2, hostile remote transport, per-invocation server-enforced digest precondition, authenticated remediation service, multi-worker concurrency transaction, or security-harm ground truth. The \`tools/list\`→\`tools/call\` TOCTOU gap remains.
