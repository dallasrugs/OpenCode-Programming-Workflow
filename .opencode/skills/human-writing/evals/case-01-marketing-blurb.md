# Eval Case 01: Marketing blurb (full seven moves)

Tests the core skill: can the agent humanize a hype-vocabulary marketing paragraph applying all seven moves, not just cosmetic ones.

## Input

> Introducing our revolutionary new productivity platform, meticulously engineered to elevate the way your team collaborates. In today's fast-paced world, leveraging cutting-edge AI technology has never been more crucial. Our comprehensive solution seamlessly integrates with your existing workflows, unlocking unprecedented levels of efficiency and fostering a culture of innovation. Whether you're a small startup or a Fortune 500 enterprise, our platform empowers your team to navigate the complexities of modern work with confidence. Join thousands of organizations who have already transformed their operations. Start your journey today.

## Trigger phrase

"make this sound human"

## Expected properties (pass when all present)

- [ ] Opens with a specific claim, not "In today's" or "Introducing"
- [ ] At least one proper noun, number, date, or lived specific
- [ ] At least one sentence under 8 words
- [ ] At least one sentence over 25 words
- [ ] Paragraph lengths vary (at least one paragraph differs from the others by 2+ sentences)
- [ ] At least one visible opinion or stance
- [ ] No tricolons, or one tricolon maximum
- [ ] Em-dash count ≤ 2 for the whole rewrite
- [ ] The "Not X — Y" contrast pattern appears ≤ 1 time
- [ ] Contractions used where natural ("don't," "it's," "you're")
- [ ] Ends on something concrete (a price, a timeframe, a specific offer) or a blunt claim — not "start your journey"

## Failure properties (fail if any present)

- [ ] Contains: revolutionary, meticulously, elevate, leveraging, cutting-edge, comprehensive, seamlessly, unlocking, unprecedented, fostering, empowers, navigate the complexities, transformed, journey
- [ ] Opens with "Let's be honest," "Here's the thing," "The truth is," "The real question is"
- [ ] Structure is still intro → 3 bullets → close
- [ ] Zero specific numbers, names, or dates
- [ ] Every paragraph is the same length (within 1 sentence of each other)
- [ ] Contains "unlock the potential of," "harness the power of," "shed light on," "pave the way for"

## Grading rubric

Score 0–10 points, pass at 8+:

| Check | Points |
|---|---|
| At least 8/11 "Expected" items present | 4 |
| Zero "Failure" items present | 3 |
| Prose reads aloud as something a real founder/marketer would say | 2 |
| One surprising/specific detail that wasn't in the input | 1 |

## Baseline (what RED — no skill — typically produces)

Agents without the skill usually keep the same intro-body-close structure, swap 2-3 vocab words, add one contraction, and leak "Let's be honest" or "Here's the thing" while calling it done. Baseline typically scores 3-5 points.

## Notes for grader

The rewrite does not need to be shorter than the input — marketing prose can run long if the voice carries. Length-matching is not a pass criterion. Specificity and structural break are.
