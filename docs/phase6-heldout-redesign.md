# Phase 6 Redesign: Development vs Held-Out Evaluation

The four primary mutations P01–P04 were visible during iterative codebook development.
They therefore become a **development set** and are excluded from the primary
inter-rater reliability statistic.

The separate supplementary natural corpus becomes the **held-out evaluation set**:

- 32 natural mutations;
- 34 path-level units after multi-path transitions are decomposed;
- 10 maintainer mutation clusters.

Before annotators begin:

1. expose the paper-facing codebook as `DCTR-CB-1.0-FROZEN`;
2. disclose that earlier codebook revisions used P01–P04 and synthetic examples;
3. freeze the held-out forms and SHA-256 manifest;
4. use linear-weighted Cohen's kappa plus exact raw agreement as primary outcomes;
5. predeclare ordinal Krippendorff alpha as a sensitivity statistic;
6. report cluster-macro agreement so the coordinated Terraform/Playwright clusters do not
   dominate the result;
7. report a predefined pattern-deduplicated sensitivity analysis in which the repeated
   10-Tool Terraform annotation change and 11-Tool Playwright path-guidance change each
   contribute one coordinated change pattern.

No independent annotation result is claimed until real non-author annotators complete
the frozen held-out forms.
