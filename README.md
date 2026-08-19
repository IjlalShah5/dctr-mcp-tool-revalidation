# DCTR: Directional Contract-Transition Revalidation

This repository contains the reproducibility package for the manuscript **“Directional Contract-Transition Revalidation for Model Context Protocol Tools: A Risk-Aware Framework for Evolving Agent Capabilities.”**

## Purpose

DCTR studies whether a previously granted approval should remain transferable after an authenticated, client-visible MCP Tool contract changes. The repository is intended to retain the evidence required to reproduce the structural comparison and audit the resulting trust-renewal decision.

## Evidence model

For each verified Tool transition, the artifact is designed to retain:

- source repository and immutable before/after boundary;
- Tool identity before and after the transition;
- reconstructed client-visible contract before and after the transition;
- canonical SHA-256 digest for each present contract;
- exact recursive path-level delta with `ADD`, `REMOVE`, and `REPLACE` operations;
- before and after values for every changed path;
- DCTR Transition Security Vector (TSV) labels and rationale where semantic coding is applied;
- transition-level L0–L4 result and reference action;
- analysis-code version.

## Repository status

The repository is being reconstructed from public maintainer histories. **No transition row, commit SHA, contract snapshot, or semantic label is inserted unless it can be traced to public source evidence.** The manuscript reports 82 verified Tool-level transitions across 20 release clusters and four server families; the public artifact will be treated as the authoritative audit of those numbers. If reconstruction reveals a discrepancy, the manuscript will be corrected rather than forcing the repository to match a pre-existing count.

## Source families

The reconstruction targets these public maintainer repositories:

1. `CXWorld/CapFrameX`
2. `useshortcut/mcp-server-shortcut`
3. `hashicorp/terraform-mcp-server`
4. `microsoft/playwright-mcp`

## Directory layout

```text
.
├── README.md
├── CITATION.cff
├── requirements.txt
├── data/
│   ├── repository_boundaries.csv
│   ├── transitions.csv
│   └── primary_mutations.csv
├── docs/
│   ├── methodology.md
│   ├── threat-model.md
│   └── coding-rules.md
└── scripts/
    ├── canonicalize.py
    ├── recursive_diff.py
    └── verify_transition.py
```

## Reproducibility principle

The package separates three layers that should not be conflated:

1. **Change evidence** — canonical equality and exact recursive deltas.
2. **Security interpretation** — direction-aware semantic coding of changed paths.
3. **Trust-renewal action** — L0–L4 policy composition and the resulting client action.

Hashing proves only whether the canonical contract changed. Provenance establishes origin continuity. Runtime policy controls concrete execution. DCTR addresses the intermediate trust-continuity question: whether the approval bound to the earlier contract should transfer to the revised contract.

## Citation

A formal citation entry is provided in `CITATION.cff`. Update the manuscript DOI and archival dataset DOI after publication/deposit.

## License

A repository license has not yet been selected by the authors. Until a license is added, the repository remains publicly readable but no additional reuse rights are granted beyond those provided by applicable law.
