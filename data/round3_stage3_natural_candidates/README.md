# Round 3: unlabelled natural candidate-pool reconstruction (not results)

**Status:** Source evidence verified; **no new independent labels or action-boundary reliability outcomes have been collected from this set.** Do not substitute these cases for a completed independent severity evaluation in the manuscript or response letter.

This supplementary targeted candidate pool includes **20 present-to-present Tool-level mutations, 43 changed JSON Pointer path units, and 14 distinct maintainer commit clusters** within **one repository**, `github/github-mcp-server`. Changes are represented by complete retained JSON Tool-definition snapshots (`pkg/github/__toolsnaps__/*.snap`) at immutable commit/parent pairs and their exact direction-preserving deltas. These are maintainer-generated fixture snapshots, **not recorded MCP `tools/list` wire traffic or verified runtime behavior**.

## Selection boundary

Purposive retrospective screen of individual 2026 maintainer commits whose `.snap` files were modified, covering symlink semantics, cross-repository parent issues, input validation, destructive annotations, pagination, pull-request requiredness, and response guidance. This is **not** a random sample, exhaustive time-window survey, claim about representative severity prevalence, or cross-repository generalizability. Coordinated updates within one commit are one maintainer cluster. Earlier Round 3 N01–N10 cases and the original 34-path held-out population remain entirely separate.

The Oct 6, 2026 broad SDK/typed-output migration was not included in this targeted sample; it would otherwise dominate with repeated schema additions. This selective exclusion is disclosed, rather than being described as a preregistered filter. Events were chosen for reconstructible changes and diversity of change surfaces, *not* to manufacture specific L3/L4 labels. **We do not know whether any will independently receive L3 or L4.**

## Contents

- `batch1_path_units.csv` ... `batch4_path_units.csv`: exact before/after path deltas, immutable parent and child commits, Git blob SHA identifiers and source URLs. No severity levels.
- `batch1_full_contracts.jsonl` ... `batch4_full_contracts.jsonl`: complete source Tool-definition projections associated with each Tool transition.
- `scripts/verify_round3_natural_candidates.py`: verifies 20/43/14, before/after JSON and exact delta coverage using the DCTR reference differencer.

Run `python scripts/verify_round3_natural_candidates.py`.

**No L4 claim:** The earlier new natural pilot has four L3 paths from one cluster and zero natural L4. The present extra 43 paths remain UNLABELLED and cannot remedy that evidentiary gap until separate independent coding has occurred. Controlled synthetic L4 stress fixtures must also remain separately denominated.
