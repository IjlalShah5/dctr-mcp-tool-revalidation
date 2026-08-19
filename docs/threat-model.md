# DCTR Threat Model and Trust Assumptions

DCTR is designed for an MCP client that has already established a trusted local baseline for a Tool and later observes a new version of the same advertised capability.

## Security objective

The objective is to prevent silent transfer of an earlier approval when the client-visible trust proposition has materially changed, while avoiding unnecessary reapproval for stable or clearly bounded evolution.

## Assumptions

A1. The MCP client, local approval record, stored canonical baseline, and canonicalization/differencing implementation are part of the trusted computing base.

A2. Provenance or publisher-origin validation, where deployed, occurs before DCTR. Updates that fail origin or integrity checks should be rejected upstream rather than semantically revalidated.

A3. DCTR analyzes the advertised client-visible Tool contract. It does not prove that runtime implementation behavior matches that contract.

A4. An authentic maintainer update can still be security-relevant. DCTR therefore does not equate authenticity with semantic approval continuity.

A5. A same-name Tool is not assumed to preserve approval when its canonical contract changes.

A6. Tool introduction and reintroduction require an initial-trust path; only present-to-present mutation is revalidation evidence.

## Relevant transition causes

A changed contract can result from benign maintenance, intentional capability expansion, changed defaults or constraints, newly explicit risk disclosure, a compromised maintainer account, or malicious semantic manipulation. DCTR does not infer which cause is true. It evaluates whether the prior approval remains transferable across the observed change.

## Out of scope

The current framework does not claim to solve:

- compromise of the local client or stored approval database;
- runtime behavior that changes without a client-visible contract change;
- publisher identity/provenance verification itself;
- invocation-time authorization or sandbox enforcement;
- probabilistic maliciousness detection;
- independently validated human semantic labels.

These layers are complementary to contract-transition revalidation.
