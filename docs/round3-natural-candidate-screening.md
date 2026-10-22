# DCTR Round 3 — natural multi-repository candidate screening (22 October 2026)

**Status: upstream commit-diff screening only. NOT independently annotated. NOT a validated natural L3/L4 sample.**

## Evidential scope

Fourteen source-linked screening rows across three new upstream repositories: 11 *candidate maintainer events/tool surfaces*, two excluded/conditional controls and one further hold. Nine screened rows are single-Tool or multi-Tool changes with source-hunk evidence; all require **full before/after client-visible Tool-contract reconstruction and JCS-consistent path comparison** before inclusion in a journal evidence cohort. Exact path names marked '(provisional)' are hypotheses about SDK serialization, NOT independently verified JSON Pointer deltas.

The current CSV contains: 11 candidates, 1 explicit implementation-only exclusion, 1 configuration hold, and 1 implementation-only exclusion pending proof. The total of 14 rows is a **screening register**, not 14 eligible mutations/clusters.

## Source evidence

Every register row records repository, immutable commit and first-parent SHA, source file, Tool names, diff summary and conservative screening status. To inspect: `https://github.com/<repo>/commit/<after_commit>`. Candidate evidence includes:

- Filesystem `move_file`: `destructiveHint` false→true, and distinct older `search_files` and `list_allowed_directories` description changes; one later coordinated openWorldHint change affects many Tools but **counts as one cluster**.
- Chrome DevTools `get_network_request`: readOnlyHint true→false with two optional body-saving file path parameters; separate enum removal and model-visible description changes; factory-dependent `pageId` case flagged for full-contract projection.
- Firecrawl `firecrawl_search` scrapeOptions billing disclosure and `firecrawl_scrape` authenticated-session wording; some descriptions are conditioned by deployment configuration.

## Screening and next scientific gate

1. Reconstruct **complete** Tool listing on both immutable boundaries, preserving SDK version, feature flags, and source reconstruction procedure.
2. Retain full before/after client-visible JSON, JCS/SHA256 hashes, exact operation/paths and clustered provenance.
3. Mark absent/generated-only/version-conditional cases explicitly; exclude implementation-only cases. Do not assign L3/L4 reference labels to candidates.
4. Blind, randomize, collect **new consent** and independent labels from two qualified non-author annotators under DCTR-CB-1.0-FROZEN. Freeze originals before adjudication.
5. Pre-adjudication report by repository and maintainer cluster. No pooling with 34-unit old held-out or 21-unit pilot. Natural L4 may remain absent.

This screening was curated by the researcher/assistant and is NOT an independent, probability-based sample. The screening is purposive for material contract surfaces and must not be used for ecosystem prevalence or validated attack detection claims.

## Reviewer interpretation

Finding credible natural candidates across distinct upstream codebases addresses the **availability of future sampling material**, but **does not itself close** the reliability/L4 evidence objections. The previously CI-verified 21-path cohort remains the only new independently coded natural pilot.