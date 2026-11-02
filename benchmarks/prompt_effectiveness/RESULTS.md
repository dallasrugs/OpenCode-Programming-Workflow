# Benchmark baseline — November 1, 2026

Current candidate: **grilling-default-v4**, baseline **evidence-v3**. This prompt-only
update makes Poseidon load grilling automatically for product/UI discovery,
including repairs. No trigger phrase is needed. No scored outcomes exist yet.

Latest prompt-only candidate: **evidence-v3**, with **discovery-v2** as baseline.
Cases, rubric, scorer, harness, metadata and non-prompt configuration match.
No v3 task outcomes have been scored; improved accuracy or efficiency is not yet
measured. See the [v3 tuning report](../../docs/usage-reviews/2026-11-01-evidence-v3.md).

Later prompt-only update: **discovery-v2** is installed locally, with matching
**discovery-v2-before** retained for comparisons using the same expanded v2 cases.
Both have zero prepared/scored runs. No improvement is measured. The record below
describes the earlier initial setup; see the [v2 installation report](../../docs/usage-reviews/2026-11-01-discovery-v2.md).

Active starting variant: **current-baseline**, captured from the six installed
global OpenCode agent definitions. Its exact prompt/configuration hashes are in
`.local/snapshots/current-baseline/manifest.json`.

| Measure | Current evidence |
|---|---|
| Scored repair trials | 0 — NOT_RUN |
| Scored transfer trials | 0 — NOT_RUN |
| Measured prompt-effect delta | Unavailable |
| Historical editor-building user review | 4/10, retained separately |
| Historical interface / usability review | 8/10 / 4/10 |
| Historical internal-save / identity-choice review | 0/10 / 0/10 |
| Provider requests from benchmark setup/tooling | 0 |

The historical creation task and the next repair task have different starting
conditions/objectives. Do not subtract their ratings and call the result a prompt
improvement. Snapshot subsequent variants and compare matched tasks/repeats from
the same inputs using the frozen rubric.

The editor repair case and six cross-task transfer cases are prepared. No live
benchmark was executed, no current agent grade was raised, and no zero score was
assigned to a missing result. The setup snapshot `outcome-v1` predates the final
harness guards, has no runs/scores, and is retained as incompatible history; use
`current-baseline` for new runs.

This file records initial setup, not a continuously refreshed scoreboard. The CLI
`status` and `compare` commands report subsequent recorded runs. See README.md for
capturing the exact user request, review evidence, configuration verification and
statistical limitations.
