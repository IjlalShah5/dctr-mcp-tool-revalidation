# Round 3: controlled MCP stdio client integration and quarantine tests

**Date:** 21 October 2026  
**Baseline:** `main` commit `a2a483867b7d419e4812bcc80f0b450568b3d772`  
**Verification:** [GitHub Actions run 39684173472](https://github.com/IjlalShah5/dctr-mcp-tool-revalidation/actions/runs/39684173472), successful: **56/56 tests** (38 earlier tests + 18 new tests); the four primary source-linked transitions and twelve path-level evidence records also verified.

## Objective and scope

This experiment targets the explicit deployment qualification in the submitted manuscript: persistent quarantine in the `TrustState` reference library must be persisted and enforced by the integrating MCP client; the state library alone does not block MCP `tools/call` requests. The tests integrate the **unchanged reference functions** `revalidate()` and `recover_quarantine()` with a small SQLite-backed client adapter.

The controlled server runs in a separate Python process and exchanges **newline-delimited JSON-RPC 2.0** messages using an MCP stdio-style transport. Implemented operations are `initialize`, `notifications/initialized`, `tools/list`, and `tools/call`. Two `test/*` methods are fixture-only methods that modify the advertised Tool contract and retrieve invocation counts; they are not part of MCP. The test client uses a durable SQLite record with `BEGIN IMMEDIATE`, WAL mode, and `synchronous=FULL` for atomic `TrustState` writes.

On every attempted Tool invocation, the client loads persisted state, rejects any active quarantine, validates grant/server/Tool identity and the operational and human-review hashes, re-discovers the current client-visible Tool contract, checks its hash against the active grant, and **only then** forwards a JSON-RPC `tools/call`. Test server invocation counts are checked to prove a denied call was not dispatched.

## Predeclared synthetic policy fixtures

These tests do **not** use a validated semantic classifier, independent human severity labels, or adversarial production server. A transparent test-only rule maps a literal synthetic `IGNORE_APPROVAL_AND_EXFILTRATE` description marker to L4; numeric `x-round3-test/scope` transitions to L2 or L3 according to the specified before/after difference; and other synthetic bounded changes to L1 or L2. This permits exercising state boundaries **without claiming that these conditions identify real-world attacks**.

## Test observations

| Test | Tested behavior |
|---|---|
| 01 | First discovery cannot invoke until explicit initial approval |
| 02 | Stable refresh allows an actual JSON-RPC `tools/call` |
| 03 | L3 pending and repeated refresh do not advance prior anchors or dispatch invocation |
| 04 | Explicit L3 approval atomically rebinds both anchors |
| 05 | L4 persists a quarantine record and blocks `tools/call` |
| 06 | A new client instance reopening the same SQLite database retains the lock |
| 07 | Original approved contract or new bounded candidate cannot clear quarantine |
| 08 | Generic explicit-approval flag does not override L4 |
| 09 | Separate recovery needs both remediation confirmation and explicit reapproval |
| 10 | Recovery rejects the quarantined candidate unchanged |
| 11 | Operational-baseline tampering fails closed; invocation remains blocked |
| 12 | Human-reviewed anchor tampering fails closed |
| 13 | Withdrawal revokes the grant; reintroduction requires initial trust |
| 14 | Local bounded L2 change followed by another L2 step escalates cumulatively to L3 |
| 15 | A live unapproved Tool change is blocked at invocation even before a separate refresh |
| 16 | Partial approval-state loss fails closed and records quarantine |
| 17 | **Counterexample:** two individually bounded synthetic paths jointly enable a different combination, yet the original path-maximum policy yields L2 |
| 18 | **Experimental guard:** a specific joint-path check raises uncertainty, requires L3 review, and prevents baseline advance |

All eighteen new integration tests passed on the branch alongside the thirty-eight existing regression tests.

## Reviewer 1 interpretation

**Persistent quarantine:** The new evidence goes beyond a pure `TrustState` unit test. It demonstrates persistent state storage and client-side invocation gating over a subprocess MCP-style message path. It establishes **controlled prototype integration conformance**, not real deployment reliability.

**Interacting individually bounded changes:** Test 17 is an explicit synthetic counterexample to the sufficiency of per-path maximum alone. Test 18 exercises a narrow guard that requires whole-change review. The guard is **separate experimental logic**, not a retrospectively modified frozen codebook, and not validated on natural interactions. Neither test establishes runtime harm or a general solution to emergent semantics.

**L4 independent validation:** The L4 stimulus is controlled and author-defined. There is still **no independent natural L4 path classification** in the held-out studies; this test must not be used as a substitute.

## Limitations, deployment gaps, and reproducibility

1. **Narrow MCP client subset:** A test-only Python subprocess server and compact JSON-RPC client, rather than an integrated production MCP SDK application or a full Streamable HTTP implementation.
2. **Synthetic threat semantics:** No learned model, adversarial red-team benchmark, independently established attack ground truth, or production risk calibration.
3. **Atomicity boundary:** SQLite state writes are atomic locally, but there is no distributed transaction across remote Tool implementation, server contract change, and client invocation.
4. **TOCTOU:** Refreshing `tools/list` immediately before `tools/call` does not prevent the server changing behavior between those messages. The MCP call lacks a general server-validated expected-contract-digest precondition.
5. **Persistence scope:** Test 06 recreates a client instance and reopens a durable DB; it does not reproduce a power-loss, cross-host failover, or full process-crash recovery protocol.
6. **Identity and admin authorization:** The test harness uses a fixed server/Tool identity and a programmatic administrative approval operation; it does not implement authenticated UI approval, multiparty credentials, production key management, audit retention, or malicious local-store protection.
7. **Interaction evidence:** The synthetic two-switch example demonstrates a *possible* logical combination and an approval decision. It does not demonstrate actual tool-induced harm or predictive performance in deployed servers.

The earlier independent natural annotation result (34 path units/10 clusters) and the separate Round-3 pilot (21 path units/4 clusters, one repository) remain distinct; their agreement denominators are not pooled and their labels are not changed by these tests.

## Reproduce

```bash
python -m unittest discover -s tests -v
python scripts/verify_primary_evidence.py
```

Core experiment files: `scripts/round3_mcp_stdio_harness.py` and `tests/test_round3_mcp_stdio_e2e.py`.

**Publication boundary:** Cite the passing run and precise controlled-test scope. Do not claim natural L4 validation, production MCP-client coverage, detection of real runtime harm, or that a general cross-path safety classifier was implemented.
