# 36-Case External Baseline Comparison

The revised comparison is extended from four primary mutations to all 36 natural
present-to-present mutations.

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

P01–P04 are retained as development-set author-reference outputs. The supplementary
32 transitions remain `PENDING_HELD_OUT_INDEPENDENT_ANNOTATION` until the real Phase 6
study is complete.

Any later under-/over-escalation count must be described as relative to the adjudicated
reference-policy labels, not as absolute security truth.
