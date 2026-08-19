# Contract Projection Notes

The files under `contracts/primary/` are **source-derived projections** of the client-visible Tool contract fields relevant to each verified mutation. They are reconstructed from immutable upstream source boundaries and are deliberately narrower than a claim of captured MCP wire traffic.

## Why projections are used

The upstream implementations define Tool schemas through code-level builders such as Zod and `defineTabTool`. The source therefore establishes Tool name, title, description, field enumerations, defaults, and schema descriptions directly, but an exact serialized MCP `tools/list` object can depend on the library serializer used at that revision.

Accordingly:

- source-visible fields are recorded as verified;
- canonical hashes in this repository hash the **stored projection**, not an unobserved network response;
- required-list effects are not asserted merely from Zod `.default()`/`.optional()` syntax unless an exact serialized Tool object is independently captured;
- a future serialized-contract capture may add fields without changing the already verified source-level transition.

## Primary evidence boundaries

### P01 — `browser_run_code` → `browser_run_code_unsafe`

The Playwright PR changes the Tool name, title, and description and explicitly identifies the behavior as arbitrary JavaScript execution in the Playwright server process and RCE-equivalent. The source-level Tool schema is directly available on both sides of the PR boundary.

### P02 — screenshot `scale`

The Playwright PR adds `scale` with the values `css` and `device`, a default of `css`, and changes execution from a hard-coded CSS scale to the supplied parameter. Whether a particular generated JSON Schema serializer places a defaulted field in `required` is treated separately from the source-level fact that the field and default were added.

### P03 — screenshot WebP and type inference

The Playwright PR expands screenshot type from `png|jpeg` to `png|jpeg|webp`, changes `type` from a defaulted field to an optional field, and documents filename-extension inference with png fallback. This is a direction-sensitive schema/default change even before considering serializer-specific `required` output.

### P04 — Shortcut HTML → Markdown authoring semantics

The Shortcut source boundary changes both the Tool description and `content` property description from HTML guidance to Markdown guidance and sets `content_format: "markdown"` in the implementation. A later README-only synchronization commit is retained as secondary evidence, not as the primary contract mutation boundary.

## Interpretation boundary

The evidence layer and DCTR policy layer remain separate. The source establishes **what changed**. The L0–L4 assignment records **how DCTR interprets that change** under the coding rules in `docs/coding-rules.md`.
