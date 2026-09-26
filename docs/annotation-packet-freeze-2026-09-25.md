# Independent Annotation Packet Freeze — 2026-09-25

The held-out independent annotation packet was frozen before collection of any real
annotator labels.

## Evaluation population

- 32 natural supplementary mutations
- 34 path-level annotation units
- 10 maintainer mutation clusters
- P01–P04 remain development-set examples and are excluded from the primary held-out
  reliability statistic.

## Frozen paper-facing codebook

`DCTR-CB-1.0-FROZEN`

## Annotator packet hashes

Annotator A form:
`533c859add31b99b44d0f99acf5720cfb802df8627ef0c99c0e8c8ec4d0801a0`

Annotator B form:
`e0fa113d6bd15bd73aab8b52cb07dafaac3a368a73ddd84a254d0abc4a80c95c`

Shared guide/codebook DOCX:
`8e7e2e271f96b39fb372af8a2a33d9c9e9720caf87cdbfa4ad5e1f2a4c78bcb8`

Annotator A ZIP:
`44281f11bea214654041429d9888e4d75626b506828ebb71ca2f980bc716e761`

Annotator B ZIP:
`35f06476056201faa14b1428c3c8d282eda0e5358b509da95b958b4fa346e09d`

Administrator case-map workbook:
`12577452ec17ad046ad7d1bea5d65554ea60090c7012d9709829018b92374016`

## Blinding

The two annotator workbooks use different deterministic randomized row orders and
annotator-specific case IDs. Mutation IDs, cluster IDs, repository/family identifiers,
author DCTR labels, and comparison-baseline outputs are not included in annotator forms.

Tool identity, client-visible surface, exact path, operation, before/after evidence, and
neutral evidence-boundary notes remain visible because semantic interpretation depends on
the role of the changed field.

## Independence instructions

Annotators are instructed not to:
- discuss held-out cases with each other;
- use generative AI or another person to decide labels;
- browse source repositories/commit history;
- run code or MCP servers;
- infer undocumented runtime behavior or maintainer intent.

## Administration

The packet should be distributed only after the applicable institutional ethics
determination/permission has been obtained. Original completed workbooks must be locked
before pre-adjudication agreement is computed. Disagreements may be adjudicated only
after those independent metrics are archived.

No real annotator labels existed at the time of this freeze.
