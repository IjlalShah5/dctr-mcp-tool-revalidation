# DCTR Independent Annotation Codebook
Version: **DCTR-CB-1.0-FROZEN**

## Development disclosure

This codebook was iteratively developed using the four primary mutations P01–P04 and
controlled policy examples. Those four transitions are therefore treated as a development
set and excluded from the primary independent-reliability statistic. The held-out
evaluation population is the separate 32-mutation supplementary corpus.

Annotators must code only the client-visible before→after evidence supplied in the held-out
packet. Do not infer undocumented runtime behavior, maintainer intent, maliciousness,
popularity, or provenance.

## TSV vocabulary

For `capability_side_effect`, `resource_scope`, `privacy_default`,
`schema_constraint`, and `annotation_trust_hint`, use one:

- `NONE`
- `BOUNDED`
- `DECREASE`
- `INCREASE`
- `AMBIGUOUS`
- `UNCERTAIN`

For `model_visible_semantics`, use one:

- `NONE`
- `BENIGN`
- `BOUNDED`
- `MATERIAL`
- `DECREASE`
- `DECEPTIVE`
- `UNCERTAIN`

For `deception_concealment`, use one:

- `NONE`
- `PRESENT`
- `UNCERTAIN`

## Minimum-action rules

Select the strongest rule directly supported by the shown path.

- `R0 → L0`: representation/evidence change with invariant semantic projection.
- `R1 → L1`: benign clarification/maintenance with no material approval-basis change.
- `R2a → L2`: bounded functional/schema evolution with no evidenced security-boundary expansion.
- `R2b → L2`: security-relevant change whose direction is clearly risk-decreasing.
- `R3a → L3`: capability, side effect, or resource scope expands materially.
- `R3b → L3`: security-sensitive default, requiredness, approval, constraint, or trust hint weakens or becomes materially ambiguous.
- `R3c → L3`: newly explicit material risk changes the informational basis of prior approval.
- `R4 → L4`: deceptive, concealed, cross-tool policy-evasive, or adversarial model-visible semantics.
- `UNCERTAIN`: evidence/codebook is insufficient for a confident assignment.

`minimum_level` must match `primary_rule`.

## Boundary rules

1. Structural direction is not automatically security direction.
2. MCP annotations are client-visible hints, not runtime proof.
3. A new serious risk disclosure can support R3c without runtime capability expansion.
4. Ordinary prose changes are not automatically L3.
5. R4 requires positive evidence of deception/evasion in the shown transition.
6. Uncertainty is allowed and must not be forced into a level.

## Confidence

Use an integer from 1 (very low) to 5 (very high). Confidence does not override the
categorical label.

## Transition composition

Annotators label path units. Transition output is composed later as the maximum
path-level minimum action. If unresolved uncertainty prevents a unique minimum action, the
transition remains `UNCERTAIN`.
