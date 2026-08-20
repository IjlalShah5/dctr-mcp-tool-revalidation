# Contract Projection Notes

The files under `contracts/primary/` are **source-derived projections** of the client-visible Tool contract fields relevant to each verified mutation. They are reconstructed from immutable upstream source boundaries and are deliberately narrower than a claim of captured MCP wire traffic.

## Why projections are used

The upstream implementations define Tool schemas through code-level builders such as Zod and `defineTabTool`. Source evidence directly establishes Tool name, title, description, field enumerations, defaults, optionality, and schema descriptions, but an exact serialized MCP `tools/list` object can depend on the serializer/library revision.

Accordingly:

- source-visible fields are recorded as verified;
- canonical hashes in this repository hash the **stored projection**, not an unobserved network response;
- serializer-specific required-list effects are not inferred from Zod `.default()`/`.optional()` syntax alone;
- where a generated downstream release listing is available, it is retained as additional contract-representation evidence without being described as captured MCP network traffic.

## Primary evidence boundaries

### P01 — `browser_run_code` → `browser_run_code_unsafe`

The Playwright source change renames the Tool, changes its title and description, and explicitly identifies arbitrary JavaScript execution in the Playwright server process as RCE-equivalent. The corresponding distributed v0.0.72 Tool listing exposes the renamed Tool and warning.

### P02 — screenshot `scale`

The Playwright source change adds `scale` with the values `css` and `device`, a default of `css`, and changes execution from a hard-coded CSS scale to the supplied parameter. The downstream v0.0.77 generated Tool listing exposes `scale` as a required string parameter with the same enum/default semantics. This release-level generated listing supports the requiredness statement used in the revised manuscript; it is not represented as a network capture.

### P03 — screenshot WebP and type inference

The Playwright source change expands screenshot type from `png|jpeg` to `png|jpeg|webp`, changes `type` from a defaulted field to an optional field, and documents filename-extension inference with png fallback. The downstream v0.0.79 generated Tool listing exposes `type` as optional while `scale` remains required. Relative to the prior generated listing, this supports the revised manuscript's direction-sensitive `[type, scale] -> [scale]` required-set statement.

### P04 — Shortcut HTML → Markdown authoring semantics

The Shortcut source boundary changes both the Tool description and `content` property description from HTML guidance to Markdown guidance and sets `content_format: "markdown"` in the implementation. A later README-only synchronization commit is retained as secondary documentation evidence, not as the primary contract mutation boundary.

## Interpretation boundary

The evidence layer and DCTR policy layer remain separate. Source and generated-release evidence establish **what changed**. The L0-L4 assignment records **how DCTR interprets that change** under the coding rules in `docs/coding-rules.md`.