# Targeted L2/L3/L4 Boundary Challenge Protocol

## Rationale

The natural held-out validation set contains 34 path units but only one L3 path unit and
no L4 path unit. Its reliability statistic therefore primarily tests L1/L2 distinctions
and should not be over-generalized to the decision-critical L2/L3 or L3/L4 boundaries.

The controlled Appendix-D conformance fixtures are not suitable for a new blind test
because closely corresponding rule examples were already exposed in the annotators'
earlier calibration material. Reusing those examples as "blind" validation would
contaminate the exercise.

## Separate challenge set

A new, previously unseen synthetic challenge set contains **16 cases** designed to exercise
boundary conditions including:

- bounded optional functionality versus material capability/scope expansion;
- risk-decreasing versus risk-increasing privacy/default changes;
- ordinary requiredness changes versus weakened safety confirmation;
- narrowing versus expanding resource scope;
- security-sensitive annotation/trust-hint changes;
- ordinary implicit-to-explicit semantics versus newly explicit material risk;
- a benign wording control; and
- a deceptive/policy-evasive L4 case.

The cases are synthetic challenge stimuli, not ecosystem-prevalence evidence.

## Procedure

The same two non-author security-knowledgeable annotators receive separately randomized
forms containing only the case evidence, neutral context, and the already-frozen
DCTR-CB-1.0 rule definitions. They must:

1. work independently until both completed files are returned;
2. not use generative AI, another person, author labels, or expected answers;
3. classify the TSV dimensions, primary rule, minimum level, confidence, uncertainty,
   and rationale;
4. complete a declaration confirming independence and consent to publication of
   anonymized labels and broad professional-background descriptors from the DCTR
   held-out annotation study and this boundary exercise.

The administrator reference key is withheld until both forms are frozen.

## Analysis plan

The challenge is reported separately from the natural held-out reliability study.

Planned descriptive outputs:

- exact rule agreement and exact level agreement between annotators;
- weighted Cohen's kappa across the ordinal L0-L4 labels when mathematically defined;
- agreement with the prewritten author reference key, reported separately for each
  annotator and after any documented adjudication;
- an explicit count of L2 versus L3/L4 challenge cases;
- disagreement descriptions at the boundary level.

Because the challenge cases are author-constructed and purposefully balanced toward hard
boundaries, no prevalence, calibrated-risk, attack-probability, or general classifier
accuracy claim is permitted.

## Status

**Prepared; results pending.** No challenge-set outcome is claimed in the manuscript or
repository until both independent forms are completed and frozen.
