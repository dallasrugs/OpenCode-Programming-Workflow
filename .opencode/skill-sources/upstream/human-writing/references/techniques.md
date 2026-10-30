# Techniques: The Why Behind the Moves

Read this when you need to understand *why* a particular technique works, or when standard rewrites aren't getting the result you want and you need to diagnose what's still off.

> **A 2026 note before you read.** The explanations below are correct *as theory*. Early detectors (DetectGPT-era, 2023) keyed primarily on perplexity and burstiness. Modern detectors — Pangram, retrained Turnitin, GPTZero v3.x, Originality.ai 3 — use fine-tuned transformer classifiers trained on humanized corpora, so burstiness and perplexity tuning alone will not defeat a current-gen detector like Pangram. Apply the techniques below to make the prose actually better. Don't rely on them alone to defeat detection. See SKILL.md "The 2026 reality" section for the detector landscape.

## Perplexity, in plain terms

Perplexity measures how predictable a word is given the words before it. A language model assigns a probability to each possible next word. When that probability is high, perplexity is low — the word was expected. When the probability is low, perplexity is high — the word was a surprise.

Detectors essentially run text through their own language model and ask: "How surprised would I have been by these word choices?" Low surprise across the board → looks like AI. Spiky, uneven surprise → looks human.

Why humans have higher perplexity:
- We have personal vocabularies. Some people say "obnoxious" where others say "annoying" where others say "a pain in the ass."
- We use idioms specific to a region, generation, or subculture.
- We make associative leaps. We start a sentence one way and finish it another.
- We pull in unusual references — a Simpsons quote, a half-remembered line of poetry, the name of a coworker.

To raise perplexity in practice:
- Replace a generic word with a more specific or more colloquial one ("a problem" → "a headache" or "a slog" or "a nightmare")
- Use one unusual word per paragraph that the reader has to register — not show-off vocabulary, just a word the model wouldn't have picked
- Use idioms ("on the back foot", "phoning it in", "the wheels came off")
- Pull in a specific reference — a brand name, a year, a person, a place

What *not* to do: don't reach for thesaurus-weird words. Replacing "use" with "utilize" or "good" with "salubrious" raises perplexity in the wrong way and reads as artificial.

## Burstiness, in plain terms

Burstiness measures variation in sentence length and complexity. AI tends to produce a flat distribution — most sentences are 15–25 words. Humans cluster their sentences in bursts: a run of short snappy ones, then a long winding one, then a fragment, then medium, then medium, then very short.

Look at this paragraph. The first sentence is 9 words. The second is 24 words and has two clauses joined by "and." This one is 6 words. And then a really long one that runs on and on, building momentum, adding clauses, dropping in an aside (like this one), before finally arriving at its main point near the end. Bam. See?

That's the rhythm. Practice it.

To raise burstiness:
- Within each paragraph, deliberately write at least one sentence under 8 words and at least one over 30
- Use fragments. Strategically.
- Combine sentences that didn't need to be separate using em dashes or semicolons
- Split sentences that were doing too much

## Voice and register

"Voice" is the felt presence of a person behind the prose. AI text reads voiceless because it's averaged across millions of writers — no single perspective, no quirks, no preferences. To add voice:

**Have an opinion and let it show.** Even in nominally neutral writing, choose your verbs. "X claimed" is different from "X argued" is different from "X conceded." Those choices reveal what you think.

**Use first person where appropriate.** Even academic writing increasingly accepts "I argue" or "I think." For casual writing, refusing to use "I" when the topic is personal reads as evasive.

**Show the thinking, not just the conclusion.** Humans say things like "I used to think X, but then…" or "the obvious answer is Y, but I'm not sure that's right because…" That visible reasoning marks the text as authored by someone with an actual mind.

**Pick a register and stay in it, mostly.** Register is the level of formality. AI text often slides between registers — using "delve" in a sentence next to "stuff" — because it has no consistent persona. Pick one. Stick to it. Break it once, deliberately, for effect.

## Specificity

Specificity is probably the single most powerful humanizing technique, and the most underused.

AI generalizes because it has to — it doesn't know which specific example you'd choose. Compare:

- Generic (AI): "Many tech companies have faced antitrust scrutiny in recent years."
- Specific (human): "The FTC's been chewing on Amazon for the better part of three years now, and Lina Khan keeps signaling she's not done."

The specific version has names, an institution, a rough timeframe, and a hint of attitude. It reads as written by someone who actually pays attention to this stuff.

When humanizing, look at every general claim and ask: can I make this specific? If yes, do it. If you don't have the specifics yourself, the user might — flag it.

When you can't get a specific, sometimes you can fake the *feel* of specificity: "back around 2019 or so" reads more human than "in recent years," even though it's still vague.

## Structural irregularity

AI essay structure is famously predictable: introduction, three body paragraphs, conclusion. Each body paragraph: topic sentence, supporting evidence, mini-conclusion. Detectors notice this. So do bored readers.

To break it:
- Open with the conclusion. Then explain why.
- Open with a question. Don't answer it for a paragraph or two.
- Open with a specific scene or anecdote. Build the abstract point out of it.
- Bury the thesis in paragraph 3.
- End with a question, an admission of uncertainty, or a tangent that loops back.
- Have one paragraph that's a single sentence. Have another that's twelve.
- Skip the conclusion entirely. Just stop when you've made the point.

## Strategic imperfection

Real writing is not flawless. Editors smooth most things out, but the rhythm of speech leaves traces:

- Conjunctions starting sentences. (And, But, So, Because.)
- Sentence fragments for emphasis.
- Comma splices in casual writing — "I went, I saw, I left."
- Mid-sentence corrections — "the answer is X, or actually, sometimes Y"
- Repetition for effect. Real repetition. Not the AI kind where the same idea gets restated three different ways, but the kind where one word lands twice in a row because it needs to.

Don't overdo this. Two or three small "imperfections" per page reads as voice. Twenty reads as a parody of voice.

## Why simple paraphrase fails

A common misunderstanding: people think humanizing = replacing words with synonyms. Run AI text through a synonym swapper and ship it. This fails because:

- The sentence structure is unchanged, so burstiness stays low
- The word choices are still in the same statistical neighborhood (synonyms cluster)
- The structural template (intro → 3 points → conclusion) is preserved
- No voice or specificity has been added

Detectors trained after about 2023 catch synonym-swap output reliably. Real humanization requires structural and voice changes, not just lexical swaps.

## Diagnosing a stubborn piece

If you've applied the seven moves and the piece still feels AI-flavored, check these:

1. **Is there a single specific name, number, or date in the whole thing?** If no, you have a specificity problem.
2. **Does the longest sentence in any paragraph differ from the shortest by at least 15 words?** If no, burstiness problem.
3. **Could a reader infer anything about who wrote this — opinions, tastes, background?** If no, voice problem.
4. **Does the piece have an obvious structural template (intro/body/conclusion)?** If yes, structural problem.
5. **Are there any moments of self-correction, hedging that sounds human, or admitted uncertainty?** If no, the piece reads as too confident in the AI-pundit way.
6. **Does it still read machine-smooth after every other fix?** The sentence *transitions* may be the issue. Humans repeat words across sentences, fumble transitions, pick up a thread two paragraphs later. Models glide cleanly from one sentence to the next. Break one of those seams on purpose.

Address whichever diagnostic fails. Usually one of these is the real problem and fixing it transforms the piece.
