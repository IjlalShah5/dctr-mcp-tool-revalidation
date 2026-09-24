# Runtime-validation source evidence

## P02 — Playwright `browser_take_screenshot` scale

Repository: `microsoft/playwright`  
Before: `224ed087809eca8db731cd1cb4c63d71d1efad3b`  
After: `33c0cb1437b3bb90a9666b7953474558dbbe91b7`  
Path: `packages/playwright-core/src/tools/backend/screenshot.ts`

Before, screenshot options force `scale: 'css'`. After, the Tool schema adds
`scale: enum('css','device').default('css')`, and the handler passes
`scale: params.scale`.

## P03 — Playwright WebP/type inference

Repository: `microsoft/playwright`  
Before: `32e8fd98462d9f274c4b6368613731f1a12a482f`  
After: `5e8ecb32a6b0c321a3464609cf726a1f419348a6`  
Path: `packages/playwright-core/src/tools/backend/screenshot.ts`

The after boundary expands image type to `png | jpeg | webp`, makes `type` optional,
adds `inferTypeFromFilename`, chooses
`params.type ?? inferTypeFromFilename(params.filename) ?? 'png'`, and passes the
resulting type to the screenshot call.

## TFMX11 — Terraform `create_run`

Repository: `hashicorp/terraform-mcp-server`  
Before: `0be75284be74d0e7f6b186c884db692bc582f06e`  
After: `ff39cb85341698e904e876be635a15706c0ead7e`

Relevant paths:
- `pkg/tools/dynamic_tool.go`
- `pkg/tools/tfe/create_run.go`

The after boundary adds `isTerraformOperationsEnabled()`; the environment variable
defaults to false. False selects `CreateRunSafe`; true selects `CreateRun`.
`CreateRunSafe` advertises `destructiveHint=false` and omits
`auto_approve`/`is_destroy`.

## Evidence boundary

The browser experiment corroborates delegated browser behavior rather than replaying the
historical TypeScript MCP package. The filename-inference and Terraform checks execute
source-derived pure selection logic, not the complete MCP transport/server stack or an
external Terraform Cloud action.
