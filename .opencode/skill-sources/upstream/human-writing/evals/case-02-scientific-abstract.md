# Eval Case 02: Scientific abstract (light touch)

Tests the "when not to humanize aggressively" guidance. The agent should recognize this is a formal register where full seven-moves rewriting would break the register and make the text more suspicious, not less.

## Input

> This study delves into the multifaceted relationship between sleep quality and cognitive performance in older adults. Leveraging a comprehensive dataset of 1,200 participants recruited over three years, we underscore the pivotal role of REM sleep in memory consolidation. Our findings foster a nuanced understanding of the intricate mechanisms underlying age-related cognitive decline and pave the way for novel therapeutic interventions. We argue that interventions targeting REM latency could bolster long-term memory retention in clinical populations.

## Trigger phrase

"make this sound human — it's for a journal submission"

(The register hint is critical. The agent should recognize formal-register context.)

## Expected properties (pass when all present)

- [ ] Cuts: delves, multifaceted, leveraging, comprehensive, underscore, pivotal, foster, nuanced, intricate, pave the way, bolster
- [ ] Replaces with plain verbs (examines, uses, shows, contributes, suggests, or similar)
- [ ] Preserves formal register: no contractions, no fragments, no "honestly," no slang
- [ ] Preserves the sample size (1,200 participants) and timeframe (three years)
- [ ] Preserves the scientific claims (REM sleep role, therapeutic interventions)
- [ ] Reads like a publishable abstract, not a blog post
- [ ] Third-person throughout (no "I think," "in my view")
- [ ] Total length within ±20% of original

## Failure properties (fail if any present)

- [ ] Uses fragments or sentence-fragment paragraphs
- [ ] Adds colloquialisms ("basically," "honestly," "look,")
- [ ] Adds first-person editorializing
- [ ] Opens with a framing phrase ("Let's face it," "Here's the thing about aging brains")
- [ ] Drops the original specifics (sample size, timeframe)
- [ ] Reads as casual blog prose
- [ ] Keeps any of: delves, multifaceted, leveraging, comprehensive, underscore, pivotal, foster, nuanced, intricate, pave the way, bolster

## Grading rubric

Score 0–10, pass at 8+:

| Check | Points |
|---|---|
| All AI-vocab from input replaced | 3 |
| Register preserved (no fragments, no colloquial, no first-person) | 3 |
| All original specifics preserved | 2 |
| Prose reads as a reviewer-credible abstract | 2 |

## Baseline (what RED — no skill — typically produces)

Agents without the skill often over-humanize scientific text, adding fragments and casual phrasing that destroy the register. Or they keep the formal register but also keep all the AI vocabulary. Baseline typically scores 3-5 points.

## Notes for grader

This case fails if the agent applied the seven moves aggressively. The skill's "When not to humanize aggressively" section and Example 13 in examples.md exist for this case — the agent must recognize the register cue and apply light touch only.
