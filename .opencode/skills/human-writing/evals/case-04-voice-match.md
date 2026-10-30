# Eval Case 04: Voice matching from user samples

Tests `voice-matching.md`. The agent receives two samples of the user's own writing plus a target text to rewrite in that voice.

## Input

**Sample 1 (user's own writing, a Substack essay):**

> The thing about learning a language as an adult is the ceiling sneaks up on you. You can get to B1 — halting restaurant conversation, the headlines — in a year of real effort. B2 is another year. Fluent, actually fluent, is a decade if you ever get there, and most people don't. I have been told this is discouraging. It is not. Knowing the real price tag of something is useful.

**Sample 2 (user's own writing, a tweet):**

> My most reliable productivity hack is being aware that I'm stupid before 10am. No decisions, no coding, no meetings. Just coffee and the dog. If I break this rule I write bugs that take three days to find.

**Target text to rewrite in the user's voice (currently AI-flavored):**

> Learning to invest in index funds has been a transformative experience for me. By embracing a passive investment strategy and harnessing the power of compound interest, I have been able to build substantial wealth over time. I would encourage everyone to leverage this approach to achieve financial freedom.

## Trigger phrase

"rewrite this to sound like me — here are two samples of my writing"

## Expected properties (pass when all present)

- [ ] Cuts all AI vocab (transformative, embracing, harnessing, leverage)
- [ ] Mean sentence length matches the samples (roughly 15-22 words, with occasional shorter hits)
- [ ] Uses the sample's opener style (bare subject or "The thing about X is") — not "Let's talk about" or "Here's the thing"
- [ ] Reproduces the sample's dry / matter-of-fact tone; no added warmth or enthusiasm
- [ ] Uses "is" / "are" / full auxiliaries (the samples favor "I have been told" / "I'm aware" — contraction-mixed, not heavy)
- [ ] Includes at least one specific number or timeframe (the samples love "a decade," "10am," "three days")
- [ ] Paragraph feels of-a-piece with the samples — if pasted into the Substack, wouldn't stand out as written by someone else

## Failure properties (fail if any present)

- [ ] Adds warmth or enthusiasm absent from samples ("I love," "it's amazing")
- [ ] Uses "Let's be honest," "Here's the thing," or any other reveal-phrase opener the samples don't use
- [ ] Turns it into a five-paragraph mini-essay with intro/body/close
- [ ] Uses any of the original AI vocabulary
- [ ] Retains the original's exhortation ("I would encourage everyone")
- [ ] No specifics added (samples are specific; a voice-matched rewrite must match that)

## Grading rubric

Score 0–10, pass at 8+:

| Check | Points |
|---|---|
| Voice profile matches samples (sentence shape, tone, opener) | 4 |
| All AI vocab from original removed | 2 |
| Added at least one specific detail in the sample's style | 2 |
| Reads as of-a-piece with the Substack samples | 2 |

## Baseline (what RED — no skill — typically produces)

Agents without voice-matching guidance typically produce a generic "casual-human" rewrite that doesn't match the specific samples' dry register. They often add warmth, enthusiasm, or framing phrases the user would never use. Baseline typically scores 3-5 points.

## Notes for grader

The user's samples show a specific voice: dry, matter-of-fact, numerate, slightly deadpan, uses "The thing about X is" as an opener, mixes contractions moderately, specific time references ("a decade," "before 10am," "three days"). A rewrite that is generically humanized but doesn't hit these markers fails the case.
