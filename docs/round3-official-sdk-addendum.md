# Round 3 extension: official MCP Python SDK and observable compound-change test

**Date:** 22 October 2026  
**Status:** Controlled engineering validation; no new human judgments collected.  
**Baseline:** Round-3 published main snapshot `8c69bd79f02c5b8ddb1d11bc9de32b59ebdd728b`.  
**Verified branch CI:** [Actions run 39713630108](https://github.com/IjlalShah5/dctr-mcp-tool-revalidation/actions/runs/39713630108), two successful jobs.

## Research aim

Reviewer 1 raised two practical limitations: the original three runtime triangulations were not a full MCP client test, and persistent L4 quarantine existed only as a state-machine claim until actually enforced around MCP invocations. A further concern was that a maximum over path levels cannot necessarily detect interactions of individually bounded changes.

This extension tests those issues **without claiming production security outcomes or independently validated L4 semantic classification**.

## Native SDK client/server test

The `official-mcp-sdk-integration` CI job installs **`mcp==1.30.0`**, pins Python 3.11, and runs eight cases using official Python SDK `ClientSession`, `stdio_client`, `StdioServerParameters`, and a separately launched `FastMCP` subprocess. The SDK exchanges real initialization, `tools/list`, and `tools/call` protocol messages. The experimental integrating client loads and atomically persists DCTR `TrustState` in SQLite, checks canonical identity against the live advertised Tool before call dispatch, and enforces the quarantine lock.

| SDK test | Observed assertion |
|---|---|
| 1 | Initial trust is not automatic; initial approval gates a real SDK Tool call |
| 2 | An author-defined L4 fixture sets quarantine and blocks SDK Tool calls |
| 3 | Quarantine remains across **both server-process and client/database reopen**, including rediscovery of original/bounded contracts |
| 4 | Recovery refuses unchanged offending definition and requires both remediation and explicit reapproval |
| 5 | Contract changed since approval cannot be invoked until revalidated, including bounded L2 changes |
| 6 | Corrupt human-reviewed anchor blocks actual Tool call and persists lock |
| 7 | Ordinary approval flag cannot override L4 |
| 8 | Repeated advertisement of L4 candidate cannot reset the original grant |

**Result: 8/8 official SDK tests passed.** The earlier hand-written stdio JSON-RPC fixture remains independently exercised and does not share the SDK test's dependencies. The SDK is the supported **1.x SDK branch**; it is not a demonstration of the newer MCP Python SDK v2 protocol's server/discover or Streamable HTTP behavior. The test server is synthetic, not an upstream deployed production server.

## Experimental compound-effect witness

The existing subprocess fixture previously exposed two individually bounded synthetic fields, `x-round3-test.write_enabled` and `x-round3-test.external_enabled`, but did not perform a distinct combined effect. This extension adds a **purely local, observable counter**, `compound_effect_calls`, incremented **only** when both switches are true during an actual dispatched `tools/call`. It performs no external network traffic, file modification, credential use, or real attack.

- With either single switch active, a Tool call occurs, but compound count remains zero (negative controls).
- Under the **unchanged** reference max-per-path policy both individually L2-rated fields together still result in **L2 automatic continuation**. An actual Tool invocation increments the compound count, verifying a new joint behavior in the controlled fixture.
- Under a distinct **experimental** pairwise guard, the combined change raises `SemanticUncertainty` and requires L3 review with no grant advance. The same client-side Tool gate blocks the invocation, so the compound-effect counter remains zero.
- When either switch is later disabled, future Tool calls do not increase the compound count.

This demonstrates a **counterexample to the sufficiency of max-path composition for arbitrary interacting semantics**, not a real exploit, validated production harm, calibrated detector advantage, or general interaction-aware classification algorithm. The synthetic conjunction is a proof-of-principle; applicability to any real Tool must be independently evaluated.

## Reproducibility

Two separate CI jobs at the same tested branch snapshot:

1. `verification`: **58/58** repository tests (38 historical + 20 controlled MCP-shaped stdio tests, including two new compound-effect controls), the anonymous natural-pilot recomputation, and the four-primary-transition/twelve-path verification.
2. `official-mcp-sdk-integration`: **8/8** native SDK tests.

**Total: 66 tests passed across two declared environments.** Reproduce with:

```bash
python -m unittest discover -s tests -v
python scripts/verify_round3_public_pilot.py
python scripts/verify_primary_evidence.py
python -m pip install 'mcp==1.30.0'
python -m unittest discover -s tests -p 'sdk_*.py' -v
```

The SDK test files do not match the default `test_*.py` discovery pattern; the dedicated SDK CI job deliberately collects them.

## Remaining scientific boundaries

There is no independent natural L4 annotation, no probabilistic sample of maintainer clusters, no security-harm ground truth, no production client authenticated-approval UX, no guarantees against server time-of-check/time-of-use behavior change, and no full remote Streamable HTTP/SDK v2 deployment assessment. A real integrating client must still address identity/provenance, per-request authorization, authenticated admin workflow and concurrency.

The prospective 24-fixture / 45-path controlled boundary study is still awaiting distinct consent and independent Stage-1 and Stage-2 annotations. **Do not report its author-authored fixtures as completed validation data**. The separate natural source-candidate screening under `data/round3_screening/` is not an annotated corpus and must not be pooled into any earlier denominators.
