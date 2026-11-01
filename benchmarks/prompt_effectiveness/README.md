# Prompt effectiveness benchmark

This is the durable benchmark for future prompt changes. It measures **task
outcomes**, using a frozen prompt variant, requirements, starting artifact,
environment and evidence-backed rubric. It makes **no model/API requests** and
never changes the application or installs a prompt variant automatically.

The existing `tests/agent_evals` live runner remains separate and opt-in. Live
model runs, if later authorized, must be serial and bounded and obey Nvidia's
20 requests/minute and 1,000/day limits, including other account usage. Merely
creating, scoring or comparing these benchmark records consumes no provider quota.

## What is frozen

A variant snapshot saves all six agent definitions, their metadata, the rubric,
cases, scorer identity and benchmark identity. It fingerprints non-prompt runtime,
plugins, skills and config without copying provider config contents. The default
source is the **installed global** agents, matching the user's active setup.
Project-local agents can be selected explicitly with `--agents .opencode/agents`.
Do not compare different hierarchies/models/permissions as a prompt-only experiment.

Each prepared run saves the exact request, prompt snapshot hash, input source hashes,
a bounded replayable input copy, repeat number and environment. Runtime controls,
models, permissions, input source or request changes cause pairs to be excluded
from the prompt-only comparison, with a reason. This catches confounding; it does
not prove all environmental factors were captured.

Snapshots/runs are local in `.local/`, ignored by Git. No dependencies, Git internals,
agent configuration, symlink trees, known credential files or build output are
copied into application input fixtures. Capture is bounded to 2,000 files/16 MiB.
Keep an immutable fixture or restore the captured starting code for each repeat.
Do not use this benchmark's output directory as an agent working directory; it
contains grader criteria. Copy only `starting-workspace` to a separate disposable
project when replaying a task, preserving the same effective agent configuration.

## Start a variant and task run

The current installed prompt candidate is **discovery-v2**. Its matching baseline
is **discovery-v2-before**; both have frozen v2 cases and identical non-prompt
configuration. Earlier snapshots are preserved as history. See the
[discovery update and mini-project instructions](../../docs/usage-reviews/2026-11-01-discovery-v2.md).
No effectiveness results have been recorded for this candidate yet.

Run from the starter repository:

```sh
python3 benchmarks/prompt_effectiveness/benchmark.py prepare discovery-v2 editor-obvious-problems \
  --workspace '/Users/vjaiwantx/experimental/notepad++' \
  --environment 'Record exact OS, Node, browser and test setup here'
```

A fresh mini project can use the `mini-project-discovery` case with
`--request` pointing to its exact original user request and variant `discovery-v2`.
Capture before the agent changes the project. The `clarification-recovery` case
tests a reported invisible question followed by a chat fallback; it does not
reproduce the native widget failure. `precise-fix-no-interview` checks that the
discovery protocol does not create unnecessary interviews for settled work.

A current snapshot may already exist: `status` lists it. Snapshots never overwrite;
choose a new name after changing prompts.

`prepare` creates:

```text
.local/runs/discovery-v2--editor-obvious-problems--1/
  run.json                 # frozen starting conditions and hashes
  request.txt              # send only this to the agent
  starting-workspace/      # replayable bounded application inputs
  review.template.json     # assessor only; initially NOT_RUN / UNVERIFIED
```

For different natural wording, provide `--request /path/to/exact-request.txt` before
running. Use `--repeat 2` for another attempt. Retain failed attempts. A run ID can
be written in full by the CLI and should be reused when scoring.

Use a fresh OpenCode session with the selected variant actually installed. Record
which prompts/config were active, the complete conversation including user answers,
source diff, actual test results, screenshots and hands-on review as applicable.
Do not show the agent the rubric/expected checks as an answer key. Do not grade
against a hidden preference it had no chance to clarify. For interactive cases,
predeclare the same user facts and retain actual clarification exchanges. New
requirements belong to a new case/version, not a retroactively changed rubric.

## Record a review

Copy `review.template.json` to `review.json`, then fill in:

- Named assessor and actual outcome (COMPLETED, PARTIAL, FAILED or
  INFRASTRUCTURE_FAILURE). Infrastructure failures stay visible and are excluded from prompt-effect attribution.
- Evidence that the selected prompt variant was used; unverified config excludes
  the pair from controlled comparisons.
- Ratings for the five rubric dimensions, using observed evidence. Missing ratings
  remain missing; they are not imputed as zero.
- Every frozen critical criterion as PASS, FAIL or UNVERIFIED with supporting
  evidence. Criteria cannot be deleted or waived as NOT_APPLICABLE after the run.
- Paths to actual evidence files, relative to the review or absolute. The scorer
  archives and fingerprints up to 32 MiB of supplied evidence; it cannot decide whether they support a claim.

```sh
python3 benchmarks/prompt_effectiveness/benchmark.py score \
  discovery-v2--editor-obvious-problems--1 \
  --review benchmarks/prompt_effectiveness/.local/runs/discovery-v2--editor-obvious-problems--1/review.json
```

Scoring creates an immutable `assessment.json`. It rejects missing evidence,
NOT_RUN, tampered inputs, changed critical criteria and overwriting a prior score.
A failed critical journey blocks readiness even if visual ratings are high.
Unverified critical behavior stays inconclusive. The separate overall user rating
is preserved; it is not replaced by the weighted assessor score.

## Compare prompt versions

After another prompt variant and matching runs have been scored:

```sh
python3 benchmarks/prompt_effectiveness/benchmark.py compare discovery-v2 candidate-v2
python3 benchmarks/prompt_effectiveness/benchmark.py status
```

Comparison reports paired runs, distinct task clusters, per-task score changes,
readiness counts and excluded/unmatched pairs. Repeats are averaged within task
before tasks receive equal weight. An exact two-sided sign test is exposed only
with at least five non-tied scored task clusters; its independence/preselection
assumptions still apply. One app, multiple screenshots, many unit assertions or
several revisions do not establish general improvement. A passing process is not
an automatically passing product.

`cases.json` includes the editor repair case plus six transfer tasks covering
product discovery, web workflows, automation, migration, research and APIs. The
shared prompts remain task-agnostic; only assessor cases contain specific expected
outcomes. Keep development and transfer results separate when interpreting them.

The historical Emberpad **4/10** review is retained under `tests/usage_reviews/`.
It measures the original editor-building trajectory. The new “find and fix obvious
problems” task measures repair, so the two numbers are useful user feedback but
are **not a controlled prompt-only pair**. No after-tuning benchmark score exists
until an actual artifact and its evidence have been assessed.

## Offline checks

```sh
python3 -m unittest discover -s tests -p test_prompt_benchmark.py -v
python3 -m unittest discover -s tests -p test_usage_review.py -v
```

These validate the harness and scoring rules, not agent effectiveness. Native
installation hashes identify files, not the truthfulness of supplied evidence or
causal attribution. All benchmark snapshots and ratings remain inspectable.
