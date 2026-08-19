# Reproducibility Methodology

## Unit of analysis

The primary unit is one client-visible MCP Tool transition at an immutable maintainer-authored version boundary. A transition is represented as

`<repository, before_boundary, after_boundary, tool_identity_before, tool_identity_after, contract_before, contract_after>`.

A release note is not counted as an additional Tool transition after its individual Tool events have been reconstructed.

## Inclusion rules

A candidate event is retained only when:

1. the before and after states can be tied to immutable public commits or tags;
2. the client-visible Tool object can be reconstructed with sufficient fidelity to compare the relevant contract surfaces;
3. the event is a Tool introduction, present-to-present mutation, or withdrawal rather than an implementation-only edit with an unchanged advertised contract;
4. the evidence source is maintainer-authored repository history rather than a secondary summary alone.

## Contract surface

The reconstruction attempts to preserve the complete client-visible Tool definition, including, where present:

- `name` and human-facing title;
- model-visible description;
- input schema;
- output schema;
- annotations / trust hints;
- standardized visible extensions.

## Canonicalization

Present Tool contracts are canonicalized recursively before hashing. Object keys are sorted, array order is preserved, compact JSON separators are used, and UTF-8 encoding is fixed. The resulting bytes are hashed with SHA-256.

The hash is an equality gate only. A mismatch proves that the canonical object differs; it does not classify risk.

## Transition classes

The observed state includes an explicit absence value:

- absent → present: Tool introduction;
- present → present with equal canonical digest: stable refresh;
- present → present with different digest: in-place mutation;
- present → absent: withdrawal;
- absent → absent: continued absence.

Initial trust and revalidation are therefore not conflated.

## Directional recursive delta

For each in-place mutation, recursive differencing records a set of path-level changes. Every row retains:

- JSON-style path;
- operation: `ADD`, `REMOVE`, or `REPLACE`;
- exact before value;
- exact after value.

This permits inverse transitions such as `private → public` and `public → private` to remain distinguishable.

## Semantic coding

Path-level deltas may subsequently be coded under the DCTR Transition Security Vector (TSV): capability/side effect, resource scope, privacy/default behavior, schema constraint, annotations, model-visible semantics, and deception/concealment.

Structural extraction is deterministic once source boundaries and reconstruction rules are fixed. Natural-language semantic coding is rule-governed and auditable but is not claimed to be independently validated ground truth in the current manuscript.

## Verification rule

No row is added to the public corpus solely because it appears in the manuscript. A row must be independently traceable to public source evidence. If the reproducible reconstruction disagrees with a manuscript count or interpretation, the manuscript should be corrected.
