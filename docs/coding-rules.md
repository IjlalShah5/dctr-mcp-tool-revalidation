# Frozen DCTR Coding Rules

These rules define the reference minimum action for a path-level contract change. They are a design codebook, not independently adjudicated ground truth.

| Rule | Path-level condition | Minimum level |
|---|---|---|
| R0 | Canonical representation differs but semantic projection is invariant. | L0 |
| R1 | Text/metadata clarification with no material capability, scope, default, constraint, approval, or risk change. | L1 |
| R2a | Bounded functional/schema evolution with no evidenced security-boundary expansion. | L2 |
| R2b | Security-relevant change whose direction is clearly risk-decreasing, such as `public → private`. | L2 |
| R3a | Capability or side-effect expands toward write, destructive, external, secret-bearing, or broader-scope behavior. | L3 |
| R3b | Security-sensitive default, requiredness, approval, or trust hint weakens or becomes materially ambiguous. | L3 |
| R3c | Newly explicit material risk information changes the informational basis of the prior approval. | L3 |
| R4 | Deceptive, concealed, cross-tool policy-evasive, or adversarial model-visible semantics. | L4 |
| RC | For a multi-path mutation, transition level is the maximum of all applicable path-level levels. | max |

## Reference actions

- L0: accept and retain evidence;
- L1: accept with audit note;
- L2: surface a notice / low-friction review;
- L3: require explicit revalidation;
- L4: quarantine or block pending investigation.

## Validation boundary

A future annotation study should freeze this codebook before labeling, allow uncertainty labels, use at least two independent annotators, and report inter-rater agreement before training or evaluating an automated semantic classifier.
