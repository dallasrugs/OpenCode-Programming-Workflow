# Evals for the `human-writing` skill

Four test cases used to verify the skill works as designed. Each case file contains:

- **Input** — an AI-flavored passage the agent is asked to rewrite
- **Trigger phrase** — what the user says (the same prompt used for every case: "make this sound human")
- **Expected properties** — what the rewrite should have (moves applied, red flags cleared)
- **Failure properties** — what the rewrite should NOT have
- **Grading rubric** — a checklist for a grader (human or LLM) to score pass/fail

## How to run

Two ways:

**1. Manual (fastest).** Paste the Input into a fresh Claude Code session that has the skill installed. Run:

```
make this sound human: <paste input>
```

Compare the output against the expected/failure properties. Score against the rubric.

**2. Subagent pressure test (more rigorous).** Dispatch a subagent with the skill loaded and the input as its task. Run the same case a second time *without* the skill to get a baseline. Compare.

## Pass criteria

A case passes when:

- All items in "expected properties" are satisfied
- Zero items in "failure properties" are triggered
- Rubric score is 80% or higher

Three of four cases passing = skill ships. Two or fewer = rewrite the weak sections.

## Cross-model testing

Run each case on three models (Haiku, Sonnet, Opus) per Anthropic's skill-authoring guide. A case that passes on Opus but fails on Haiku means the skill relies too heavily on model intelligence rather than clear instruction — revise toward more explicit guidance.

## Cases

- `case-01-marketing-blurb.md` — full seven-moves humanization of a hype-vocabulary marketing paragraph
- `case-02-scientific-abstract.md` — light-touch test; formal register must be preserved
- `case-03-chat-dm.md` — extreme-register test; output must drop capitalization and use fragments
- `case-04-voice-match.md` — voice-matching test; user supplies a writing sample plus target text
