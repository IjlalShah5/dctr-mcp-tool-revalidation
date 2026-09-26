# Final revision validation checkpoint

Date: 2026-09-26

## Annotation

Held-out semantic reproducibility is complete:
- 32 natural mutations;
- 34 path units;
- 10 maintainer clusters;
- exact pre-adjudication L0-L4 agreement: 82.4% (28/34);
- linear-weighted Cohen's kappa: 0.720;
- ordinal Krippendorff alpha: 0.764;
- cluster-macro exact agreement: 94.5%;
- pattern-deduplicated exact agreement: 96.4%;
- six disagreements, all in the coordinated Playwright filename/path-description cluster;
- all six adjudicated by A+B consensus to R2a/L2 after independent metrics were frozen.

## Reference implementation

A branch-equivalent offline reconstruction was executed with the vendored RFC 8785 fallback and the current state-model/tests.

Result: **21/21 unit and artefact-integrity tests passed**.

Coverage includes:
- `true != 1`;
- `1 == 1.0`;
- `-0 == 0`;
- JSON Pointer escaping;
- reviewer Boolean-to-number regression;
- no stability laundering;
- cumulative staircase escalation;
- explicit human-anchor reset;
- withdrawal revocation and reintroduction as initial trust;
- grant identity mismatch fail-closed;
- semantic uncertainty -> L3 revalidation;
- unsupported JCS numeric domain fail-closed;
- policy-engine exception fail-closed;
- L4 quarantine not overridden by an approval flag;
- supplementary corpus counts;
- all-36 comparison completion;
- runtime subset counts;
- held-out index counts;
- final path/mutation annotation distributions;
- frozen reliability metrics.

## Claim boundary

The tests establish conformance of the reference implementation and integrity of retained artefacts. They do not establish general MCP runtime security, attack prevalence, or calibrated L0-L4 risk.
