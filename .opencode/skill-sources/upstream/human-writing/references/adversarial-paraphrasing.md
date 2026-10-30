# Adversarial paraphrasing

Detector-in-the-loop rewriting: use a paraphraser LLM to rewrite the text, score the rewrite against a live detector, feed the score back, and iterate until the detector stops flagging it. Use this **only** when the user has API access to a specific detector they need to beat, stakes are high enough to justify the per-iteration cost, and the seven moves in `SKILL.md` aren't cutting it on their own. Hinton et al. (arXiv 2506.07001, June 2025) report roughly 88% reduction in T@1%F across neural, watermark, and zero-shot detectors — that's the single strongest number in the open literature for any post-hoc technique.

## How it works

One LLM paraphrases. A second call (or API) scores the paraphrase with the target detector and returns a confidence-of-AI number. The paraphraser's next pass sees the previous text, the score, and instructions to reduce the score without breaking meaning. Gradient-free reinforcement — the detector is the reward, the LLM is the policy, and you're doing rollouts with prompting instead of weight updates. It works because modern detector classifiers have decision boundaries that are locally smooth under paraphrase, so nudging text across them is tractable.

## Prompt template

```text
SYSTEM:
You are a paraphraser. Your only job is to rewrite the user's text so that
an AI-text detector scores it as human. Preserve: meaning, factual claims,
named entities, numerical values, citations, quotations. Change: sentence
structure, rhythm, vocabulary, register, clause order. Do not add facts.
Do not remove facts. Do not add disclaimers. Output only the rewrite —
no preamble, no explanation.

USER (iteration 1):
Rewrite this text. Target: detector confidence-of-AI < 0.30.

<<<
{original_text}
>>>

USER (iteration 2..N):
Previous rewrite scored {score} on {detector_name} (0 = certainly human,
1 = certainly AI). Rewrite again, more aggressively vary sentence length,
register, and clause structure. Keep every fact and entity intact.

<<<
{previous_text}
>>>
```

**Stopping criteria (hard-coded, no negotiation):**

- **Success:** detector confidence < 0.30 for three consecutive iterations. Take the last rewrite.
- **Hard cap:** 8 iterations. Stop regardless.
- **Plateau abort:** if the rolling-three-iteration mean score stays above 0.5, stop and tell the user this detector isn't yielding. Don't burn another 20 API calls on a lost cause.

Log every score. Show the user the trajectory when you return the result — they need to see whether it converged or you just hit the cap.

## Limitations

- **Needs a detector API.** GPTZero, Originality, Winston all have paid APIs. Pangram offers one to enterprise only. Turnitin does not expose one. If the user doesn't have keys, this technique is unavailable — period.
- **Cost.** Every iteration is a paraphrase call plus a detector call. At 8 iterations on a 1,000-word passage you're looking at real money and 30–90 seconds of wall time. Per document.
- **Meaning drift.** The paraphraser will silently reword technical claims, soften hedges, and occasionally drop clauses it thinks are stylistic. Diff the output against the original before shipping.
- **Pangram on long passages.** The 2506.07001 paper did not meaningfully beat Pangram on passages over ~500 words, and Jabarian & Imas's 2025 evaluation confirms Pangram holds up against adversarial humanizers in general. Don't promise results there.
- **DAMAGE (arXiv 2501.03437).** Explicitly trains detectors on adversarially-paraphrased text. As detector vendors fold DAMAGE-style training data in (Pangram already has, Originality likely next), this technique's half-life shortens. Treat the 88% number as a 2025 snapshot, not a law.

## When NOT to use

- User just wants better prose. Use the seven moves in `SKILL.md`. Adversarial paraphrasing produces detector-evasive text, not good text — those are different goals.
- No detector API access. Skip.
- Text under ~100 words. Detectors are noisy on short passages and the paraphraser has nowhere to maneuver.
- Factual, legal, medical, academic, or contractual text where meaning drift is disqualifying. The risk of silently mangling a number or a hedge isn't worth the detector win. Tell the user no.

## Citation and further reading

- Primary: arXiv **2506.07001** (2025) — https://arxiv.org/abs/2506.07001
- Complementary — TH-Bench, a benchmark for humanizer evaluation across detectors: arXiv **2503.08708**
- Complementary — Jabarian & Imas, *Detecting AI-Generated Text: Evidence from Humans and Algorithms*, UChicago BFI Working Paper **2025-116**. The most rigorous independent detector evaluation to date.
