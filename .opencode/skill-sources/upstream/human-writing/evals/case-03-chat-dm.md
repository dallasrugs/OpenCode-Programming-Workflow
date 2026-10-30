# Eval Case 03: Chat / DM (extreme register)

Tests register-matched humanization at the casual end of the spectrum. The agent should drop capitalization, break the paragraph into multiple messages, and use fragments — not produce one polished paragraph.

## Input

> Hi! I wanted to follow up on our earlier conversation regarding the project timeline. I think it would be beneficial to touch base soon to ensure we are aligned on the next steps. Please let me know when you are available this week. I am happy to work around your schedule. Looking forward to hearing from you.

## Trigger phrase

"make this sound human — it's going in a DM on Slack"

## Expected properties (pass when all present)

- [ ] Broken into 2+ shorter messages (one idea per message)
- [ ] Lowercase or inconsistent capitalization — no title-case prose
- [ ] At least one fragment or ultra-short sentence (≤ 4 words)
- [ ] No "Hi!" greeting, no "Looking forward to hearing from you" signoff
- [ ] At least one chat-register contraction or abbreviation (tmrw, thx, prob, lmk, ngl) where natural
- [ ] Total word count below half the original (chat is terse)

## Failure properties (fail if any present)

- [ ] One polished paragraph of 3+ complete sentences
- [ ] Formal capitalization throughout
- [ ] Any of: "touch base," "align on next steps," "happy to work around," "looking forward"
- [ ] Multiple sentences per message with conjunctions
- [ ] Any greeting more formal than "hey" / "heya" / bare opener
- [ ] Any signoff — DMs don't get signed
- [ ] Reads as an email pretending to be a chat

## Grading rubric

Score 0–10, pass at 8+:

| Check | Points |
|---|---|
| Message is broken into 2+ terse sends | 3 |
| Register-appropriate fragments and casings | 3 |
| No email-style scaffolding | 2 |
| Word count roughly halved from original | 2 |

## Baseline (what RED — no skill — typically produces)

Agents without the skill typically produce a polished paragraph that "sounds casual" but is still one continuous block of prose with full capitalization and a greeting/signoff. Baseline typically scores 2-4 points on this case — the register mismatch is the main failure.

## Notes for grader

Example 11 in examples.md is the model. If the agent's output looks like Example 11's "before," it failed; if it looks like Example 11's "after," it passed. Compare directly.
