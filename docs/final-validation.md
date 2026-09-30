# Final revision validation checkpoint

Date: 2026-09-28

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
- post-protocol unit-bootstrap kappa 95% interval: 0.472-0.905;
- post-protocol cluster-bootstrap kappa 95% interval: 0.146-1.000;
- post hoc SPLW01-excluded localization diagnostic: kappa 1.000 on 23 units;
- six disagreements, all in the coordinated Playwright filename/path-description cluster;
- all six adjudicated by A+B consensus to R2a/L2 after independent metrics were frozen.

The natural held-out set contains one L3 path unit and no L4 path unit. This is retained as an explicit limitation: the observed reliability statistic primarily informs L1/L2 distinctions and is not generalized to every L2/L3/L4 policy boundary. Appendix-D controlled fixtures remain author-defined conformance checks rather than independent natural-label evidence.

Both annotators consented to participation and to publication of anonymized annotation outputs and broad professional-background descriptors.

## Reference implementation

A branch-equivalent offline reconstruction was executed with the vendored RFC 8785 fallback and the current state-model/tests.

Result: **25/25 unit and artefact-integrity tests passed**.

Coverage includes:
- `true != 1`;
- `1 == 1.0`;
- `-0 == 0`;
- JSON Pointer escaping;
- reviewer Boolean-to-number regression;
- no stability laundering;
- cumulative staircase escalation;
- separate digest integrity for the operational baseline and human-reviewed anchor;
- automatic L2 continuation preserving the human anchor;
- explicit L2 human approval advancing both baselines/digests;
- withdrawal revocation and reintroduction as initial trust;
- grant identity mismatch fail-closed;
- semantic uncertainty -> L3 revalidation;
- unsupported JCS numeric domain fail-closed;
- policy-engine exception fail-closed;
- L4 quarantine not overridden by an approval flag;
- supplementary corpus counts;
- all-36 comparison completion and DCTR/Microsoft cross-tab;
- runtime subset counts;
- held-out index counts;
- final path/mutation annotation distributions;
- frozen reliability and precision-diagnostic fields.

## Claim boundary

The tests establish conformance of the reference implementation and integrity of retained artefacts. They do not establish general MCP runtime security, attack prevalence, calibrated L0-L4 risk, automatic semantic-classifier accuracy, or end-to-end reviewer-workload reduction.

The staircase property is also scoped: max-over-path composition does not by itself guarantee detection of emergent security interactions among multiple individually bounded path changes.

## Phase-12 reviewer hardening

The final Phase-12 branch adds:

- independent integrity binding/checking for the human-reviewed anchor digest;
- explicit control-flow tests for automatic continuation versus explicit human approval;
- a scope caveat for cross-path semantic interactions in the staircase lemma;
- bootstrap precision diagnostics for annotation reliability;
- a DCTR/Microsoft decision cross-tab and P01 granularity example;
- explicit documentation that held-out DCTR comparison labels are human-adjudicated reference-policy outputs, not automatic-classifier predictions;
- a deployment-semantic-stage note and clearer artefact index;
- explicit consent/governance wording for the two non-author annotators.

No additional annotation experiment is claimed in the current revision.
