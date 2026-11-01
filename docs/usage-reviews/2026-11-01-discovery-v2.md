# Discovery prompt update v2

Installed in the six repository agent definitions and six local global OpenCode definitions on 2026-11-01. The global configuration still uses Poseidon as primary; the repository's staged configuration still uses Team Lead as primary. Models, permissions, modes, steps, runtime, plugins and upstream skill files were preserved. The paused broader reliability migration was not installed.

## Intended behavior

For materially ambiguous product work, redesigns and broad usability audits:

1. Poseidon identifies the intended outcome, primary journey and observable success before choosing a solution. It distinguishes confirmed constraints, observations, assumptions and proposals. Existing implementation behavior is open to examination unless the user requires its preservation.
2. It uses relevant grilling with concise, dependency-aware rounds. Questions uncover user intent and consequential choices; they do not merely seek approval for an agent-selected repair.
3. Required questions default to numbered ordinary chat. Poseidon ends the turn for an actual response and retains unanswered questions across interruptions. A widget failure, unrelated response, tool completion or silence cannot authorize dependent changes. Explicit delegation of a decision is accepted.
4. The coordinator obtains a bounded independent Researcher challenge of the original request, confirmed answers and proposed scope before dependent implementation. Researcher identifies evidence, unsupported assumptions, overlooked steps and material questions. It does not decide user preferences. In the repository hierarchy this is routed through Team Lead; in the active global hierarchy Poseidon invokes Researcher.
5. A compact shared brief carries the original request, actual answers, journeys, acceptance checks and material unknowns into planning, implementation and review. Reviewer assesses both patch correctness and overall requirement coverage, with evidence and confidence separated from severity.

Precise authorized fixes with settled intent do not require an interview or redundant Researcher dispatch. Relevant accepted findings can be reused. Discovery ends when material decisions are answered or explicitly delegated; no additional confirmation ritual is added.

## Method sources and adaptation

The independently written prompt protocol applies the outcome/assumption/constraint method described by [First Principles Thinking](https://github.com/awesome-skills/first-principles-skill/blob/main/SKILL.md) and progressive clarification described by [Socrates](https://github.com/bevibing/socrates-skill/blob/main/SKILL.md). These are conceptual references, not new unchanged upstream imports. In particular, Socrates' tutor-only refusal to give direct answers was not adopted. The essential method is embedded in agent prompts so loading an optional skill is not its sole trigger. Existing native `grilling` content remains unchanged.

## Question-interface limitation

The inspected session contains an interrupted native question call and the user's report that the questions did not appear. Its cause was not established. The installed workspace plugin wraps tools in resource governance, but that fact alone does not demonstrate that it caused the question failure. No speculative plugin/runtime repair was made. The ordinary-chat default and widget-to-chat fallback address answerability at the prompt level; the native widget itself is not claimed fixed.

## Validation and deployment evidence

- All six updated global prompt bodies were found in the read-only `/api/agent` response for a fresh temporary project directory. No session or generation was started.
- Every agent's frontmatter was preserved byte-for-byte. The installation manifest records before/after hashes and active models/modes: [installation record](2026-11-01-discovery-v2-installation.json).
- `python3 .opencode/runtime/skillctl.py validate` passed (27 native skills, 21 verified imports, six preserved unverified entries).
- `python3 -m unittest discover -s tests -p 'test_*.py'` passed: 89 tests run, five opt-in tests skipped. Expected test-fixture output includes a deliberately rejected source-changing validation; the suite's final result is OK.
- No live model evaluation was run; no effectiveness improvement or new agent grade is claimed. No provider quota was consumed by this update's validation.

Global before copies are under `/private/tmp/opencode-discovery-v2-n8y6zlna/global-before`; local benchmark snapshots also retain both variants' complete prompt definitions. The temporary backup is for immediate recovery, not durable storage.

## Next mini-project test

The benchmark now includes ten cases, adding clarification recovery, a precise fix that should avoid unnecessary interviewing, and a generic mini-project development case. The inventory case also checks independent discovery, actual answers and their propagation. Existing snapshots and historical scores were not rewritten.

Local frozen variants `discovery-v2-before` and `discovery-v2` use the same v2 cases, rubric, scorer, harness and non-prompt configuration. Only their prompt bodies differ. No runs have been prepared or scored for these variants. The earlier `current-baseline` remains historical; its v1 cases are not a controlled counterpart to these v2 snapshots.

Before starting the user's mini project, save its exact original request in a text file and prepare the run with the real project directory and environment:

```sh
python3 benchmarks/prompt_effectiveness/benchmark.py prepare discovery-v2 mini-project-discovery \
  --workspace /absolute/path/to/mini-project \
  --environment 'Actual OS, runtime, browser and available test setup' \
  --request /absolute/path/to/original-request.txt
```

Use a fresh OpenCode session in that project. Keep the complete questions and answers, corrections, resulting changes and validation evidence. Do not give the agent the assessor-only checklist. Supply outcomes after actual use; installed prompts and passing infrastructure tests are not proof of product effectiveness. For a controlled comparison, replay the same initial artifact, original request, environment and predeclared user decisions with the other frozen variant; preserve failed attempts.
