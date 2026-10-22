# Round 3 continued: official MCP Python SDK integration and controlled compound-outcome test

**Date:** 22 October 2026  
**Frozen baseline for this extension:** `main` commit `8c69bd79f02c5b8ddb1d11bc9de32b59ebdd728b`  
**Verified CI:** [GitHub Actions run 39708525779](https://github.com/IjlalShah5/dctr-mcp-tool-revalidation/actions/runs/39708525779), **71/71 passing tests**: 38 original, 18 Round-3 raw stdio integration, **15 official SDK-based integration**. Public 21-path pilot reliability and primary evidence also verified in the same run.

## Motivation

Reviewer 1 objected that the three earlier runtime checks were not a real MCP-client integration and that persistent quarantine was only a reference-state abstraction. Our first Round-3 fixture exchanged JSON-RPC-shaped lines with a custom Python server. This follow-up exercises an **actual supported MCP Python SDK** client and server: pinned `mcp==1.28.0` (v1 maintenance line), `StdioServerParameters`, `stdio_client`, `ClientSession.initialize()`, `ClientSession.list_tools()` and `ClientSession.call_tool()` across a separate stdio subprocess.

Do not present this as the SDK v2 protocol, Streamable HTTP integration, a production MCP host, or behavior testing of real third-party MCP servers. We intentionally pin v1 so results are reproducible despite the v2 protocol transition.

## Implementation

- `scripts/round3_official_sdk_fixture_server.py`: official MCP SDK low-level server; serves one controlled Tool contract from a mutable local JSON fixture, records actual `tools/call` arrival, and optionally writes a **public synthetic canary string** to a local temporary sink.
- `tests/test_round3_official_mcp_sdk.py`: official SDK `ClientSession` adapter plus SQLite `TrustState` storage and invocation-time gate. Reuses **unchanged** DCTR `revalidate()` / `recover_quarantine()`.
- `.github/workflows/reproducibility.yml`: installs the exact published `mcp==1.28.0` dependency, then runs all repository tests and existing public evidence verifiers.

## Fifteen controlled end-to-end observations

| ID | SDK-path observation |
|---|---|
| 01–02 | Initialize, discover and invoke only after an explicit first approval; no implicit grant |
| 03–04 | L3 pending/repeat cannot advance anchors; explicit L3 review rebinds both |
| 05–07 | Author-defined L4 marker triggers quarantine; invocation gate blocks it; SQLite reopening and old-contract rediscovery do not unlock it |
| 08 | Separate recovery needs both remediation confirmation and explicit human reapproval |
| 09 | Live unapproved Tool definition change blocks invocation before explicit refresh |
| 10 | **Controlled outcome:** two new optional boolean schema properties each receive L2 under a deliberately narrow fixture classifier. Together, with both arguments true, an SDK `tools/call` is continued under the original max-path policy and the public test canary reaches a **local temporary sink** |
| 11 | **Experimental whole-delta guard:** detecting the two property paths together triggers `SemanticUncertainty` → pending L3, preserving the prior anchors and preventing the SDK call/canary transfer |
| 12–13 | Matched controls adding only one of the two optional flags do **not** transfer the canary |
| 14 | Tampered operational hash fails closed and persists quarantine |
| 15 | Withdrawal revokes active grant and rediscovery requires initial approval |

**Important epistemic boundary:** The classifier in this test is a **test-only, author-defined rule** mapping optional additions to L2 and literal test messages to L3/L4. The compound example is a designed stress/counterexample; a fully qualified human expert could instead rate an individual path more strongly. The canary is intentionally public, and the 'external' sink is a local file. Its transfer demonstrates a **controlled behavioral difference** between two gating policies under one mocked implementation, not a real compromise, production data theft, independent severity ground truth or general mitigation of composite attack chains.

## What is now supported

- Official SDK v1 protocol messages traverse an SDK-managed transport and real Tool handler.
- Persisting the reference quarantine flag in a local SQLite record and enforcing it at an MCP-client invocation gate survives a state-store reopening.
- A controlled composite setup can produce a concrete oracle (canary sink observed/not observed) under a fixed test-only policy, supporting the need for additional whole-contract review.
- A narrow experimental guard can prevent that exact controlled outcome before the Tool handler executes.

## Remaining reviewer-relevant gaps

1. No independent **natural L4 annotation** was obtained; neither author-defined L4 tests nor the new synthetic challenge stimuli can be counted as one.
2. No **production** MCP client, v2 SDK, hostile network server, cross-process coordinated race, authenticated admin UI, machine compromise, crash durability, or full Streamable HTTP integration has been validated.
3. A list→call time-of-check/time-of-use gap remains. Server behavior can change after the client verifies `tools/list`, and the protocol fixture does not provide a server-enforced expected-digest precondition.
4. The new compound guard is specific to two known fixture paths, and has no field-data sensitivity/specificity evidence. It is **not** part of the frozen DCTR-CB-1.0 reference policy.
5. Additional blind, consented expert coding with difficult independent L3/L4 examples and whole-contract judgments must occur **before** new independent reliability statistics can legitimately be claimed.

## Exact reproduction

```sh
python -m pip install 'mcp==1.28.0'
python -m unittest discover -s tests -v
python scripts/verify_round3_public_pilot.py
python scripts/verify_primary_evidence.py
```

Retain the previously published 34 held-out and 21 new natural-pilot results unchanged and separately denominated.
