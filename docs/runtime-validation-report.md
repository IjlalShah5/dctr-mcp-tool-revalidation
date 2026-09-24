# Controlled Contract/Implementation/Runtime Triangulation

## Aim

This validation subset triangulates three natural mutations across the advertised
client-visible contract, the corresponding maintainer implementation change, and an
executable behavioral check where the local environment permits it.

It is not presented as comprehensive runtime validation or attack-effectiveness
measurement.

## P02 — Screenshot scale

Historical source changes from a fixed `scale: 'css'` to a Tool parameter
`scale ∈ {css, device}` passed directly to the screenshot call.

Controlled execution used Playwright Python 1.57.0 with Chromium
144.0.7559.96 on Debian GNU/Linux 13 and a 400×300 viewport at device scale factor 2.

Observed:
- `scale=css` → 400×300 PNG;
- `scale=device` → 800×600 PNG.

Result: **aligned** with the advertised scale semantics.

## P03 — WebP and filename/type selection

The historical implementation expands the screenshot format to WebP, makes `type`
optional, introduces filename-extension inference, and selects:

`params.type ?? inferTypeFromFilename(params.filename) ?? 'png'`.

The source-derived selection logic was executed against eight cases. All **8/8 passed**,
including `.webp`, case-insensitive `.WEBP`, `.jpg/.jpeg`, `.png`, unknown
extension, missing filename, and explicit-type override.

The browser check used Chromium's DevTools screenshot command. Chromium produced valid
PNG, JPEG, and WebP byte signatures, including `RIFF....WEBP`.

Result: **aligned at the selection-logic and browser-encoding layers**. This is not a
replay of the complete historical MCP response/file-registration path.

## TFMX11 — Terraform safe/default `create_run`

The historical after boundary adds `ENABLE_TF_OPERATIONS`, defaulting to `false`.
When false, `registerTFETools()` selects `CreateRunSafe`; when true it selects
`CreateRun`. `CreateRunSafe` advertises `destructiveHint=false` and narrows
`run_type` by removing `auto_approve` and `is_destroy`.

A source-derived Go harness confirmed:
- environment unset/false → safe contract;
- `ENABLE_TF_OPERATIONS=true` → broader destructive variant.

The experiment deliberately did not invoke Terraform Cloud/Enterprise or execute a real
destructive run.

## Interpretation

For these three cases, the observed implementation/runtime evidence did not contradict
the advertised transition. The finding is narrow. It does not establish that DCTR detects
hidden implementation changes, that all advertised hints are truthful, or that a
contract-level L2/L3 classification equals runtime harm.

The intended claim is therefore:

> DCTR evaluates approval-relevant **contract security semantics**. A small controlled
> triangulation found implementation/runtime behavior consistent with three selected
> advertised transitions, but runtime equivalence remains outside the framework's general
> guarantee.
