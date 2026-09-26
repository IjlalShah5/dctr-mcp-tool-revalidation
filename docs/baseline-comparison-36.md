# 36-Case External Baseline Comparison

The revised comparison covers all 36 natural present-to-present mutations.

## ETDI-style decision baseline

Every changed approved Tool definition is assigned explicit reapproval. This isolates the
change-triggered decision relevant to the DCTR comparison and does not claim to reproduce
ETDI's full signature, OAuth, identity, or authorization architecture.

## Microsoft MCP Security Gateway

Two documented behaviors are kept separate:

1. **Specific schema-drift severity**
   - Tool description changed -> INFO
   - optional parameter added -> WARNING
   - required parameter added -> CRITICAL
   - parameter removed -> CRITICAL
   - type changed -> CRITICAL
   - required fields removed -> CRITICAL
   - required fields only added -> WARNING

2. **Rug-pull fingerprint behavior**
   - a stored Tool description or schema fingerprint change -> CRITICAL rug-pull threat

The published ToolSchema/fingerprint surface does not include MCP annotations.
Annotation-only mutations are therefore marked `NOT_COVERED`; the comparison does not
invent an external severity.

## DCTR outputs

P01-P04 remain development-set author-reference outputs: P01=L3 and P02-P04=L2.

The separate held-out supplementary set now has independently coded and adjudicated DCTR
outputs. After max-path composition across the 32 mutations:
- L1: 13;
- L2: 18;
- L3: 1;
- L0/L4: 0.

Across all 36 natural mutations, combining the four development examples with the 32
held-out consensus outputs gives L1=13, L2=21, and L3=2. This mixed all-36 view is a
decision-structure comparison, not a single held-out performance sample.

Any under-/over-escalation count must be described as relative to the adjudicated
reference-policy labels, not as absolute security truth.
