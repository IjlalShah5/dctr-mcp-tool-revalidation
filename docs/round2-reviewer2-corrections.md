# Round-2 Reviewer 2 — code/data correction register

All changes in this register were applied to the existing **main** branch.
They are corrections to the repository; the MDPI manuscript and SuSy response
must be updated/re-uploaded separately.

## Comment 1 — quarantine lifecycle

The former `QUARANTINED` response returned the original unchanged
`TrustState`, allowing the next original-contract refresh to hit
`STABLE_ACCEPT` and potentially a later L2 continuation. The updated
`scripts/revalidation_state.py` adds immutable `QuarantineRecord` to the
state, blocks ordinary refreshes when the marker is present, prevents an
injected enforcer from overriding L4, and provides explicit
`recover_quarantine`. Recovery requires **remediation_confirmed=True**
and **explicit_human_approval=True**, refuses the offending candidate
digest, verifies anchor integrity and L0–L4 classification, and atomically
rebinds both anchors in the returned state after a non-L4 recovery.
`tests/test_phase11_hardening.py` covers old-baseline refresh after L4,
L2-after-L4, malicious-candidate recovery, missing approval, custom
enforcer override, policy block, and withdrawal.

**Deployment qualifier:** The reference function does not itself store
state durably or block actual MCP invocations. Production clients must
persist the returned state and enforce the inactive quarantine marker.
Describe this conditional guarantee in Figure 2, Section 4.5, Algorithm 2,
deployment/limitations, and the response letter.

## Comment 2 — primary transition records and completeness

`data/transitions.csv` now derives hashes and path lists from the four
stored before/after contract pairs, including:

- P02: `/inputSchema/properties/scale` and `/inputSchema/required`.
- P03: `/inputSchema/properties/filename/description`,
  `/inputSchema/properties/type/default`,
  `/inputSchema/properties/type/description`,
  `/inputSchema/properties/type/enum`, and
  `/inputSchema/required`.

The P02 after digest equals the P03 before digest. The new file
`data/primary_path_evidence.csv` retains **all 12** exact
P01–P04 delta paths with before/after JSON, seven categorical TSV fields,
author-assigned development-set rule/level, and rationale. These are
**author references**, *not independent held-out annotation labels or
a validated automatic classifier*.

Run:

```bash
python scripts/verify_primary_evidence.py
python -m unittest discover -s tests -v
```

The verifier checks both digests for each primary record, exact delta
coverage/operations/values, seven TSV dimensions, rule-to-level mapping,
the maximum path-level composition, and P02→P03 hash continuity.

## Comment 3 — alpha distance bug

`scripts/agreement_analysis_heldout.py` formerly used
`((a-b)/4)**2`, an **interval** distance, under the function name
`ordinal_alpha`. The corrected implementation uses ordinal distances
from the pooled observed category frequencies:

`distance(i,j) = (0.5*n_i + sum(n_k for i<k<j) + 0.5*n_j)**2`

for i != j, and zero on the diagonal.

Computed on the same published 34 pre-adjudication label pairs:
- Correct ordinal Krippendorff alpha = **0.7081173067105337** (0.708).
- Previous mislabeled interval-distance alpha = **0.7635294117647059** (0.764).
- Linear-weighted Cohen kappa = **0.7197802197802198** (0.720).
- Exact agreement = **28/34 (82.4%)**.

These changes do **not** create new annotation evidence or improve precision
at the sparse natural L2/L3 and L3/L4 boundaries.

## Manuscript/response synchronization still necessary

Correct every occurrence of *ordinal alpha 0.764* in the manuscript
(Abstract, Section 5.9, Table 11, Section 6.6, Conclusion, as applicable)
to **0.708**, and explain the distance correction. Clarify lifecycle
persistence and the obligation of the integrating client in Figure 2,
Section 4.5, Algorithm 2, and the deployment discussion. Describe the
new public primary evidence table and completeness script in Section 4.11.
Retain the narrow approval-continuity framing and the limitation that only
one held-out natural L3 path and no L4 paths were observed.
