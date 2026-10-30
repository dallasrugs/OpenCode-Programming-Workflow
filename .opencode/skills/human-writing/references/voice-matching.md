# Voice Matching: Rewriting in the User's Own Voice

When the user's own writing is being falsely AI-flagged, or when they want rewrites to sound like *them* instead of a generic "human," voice-matching beats generic humanization. It's also the single most effective defense against detectors, since a user's actual voice is by definition not in the AI distribution.

Use when:

- The user provides their own writing samples (emails, blog posts, tweets, Slack messages).
- The user says "match my voice," "sound like me," "rewrite this the way I'd write it."
- The user has public writing (blog, Substack, Twitter archive) they're willing to point to.
- The user's own text is being flagged as AI and they want it tuned back toward their actual style.

## What to extract from samples

A 10-point diagnostic checklist. Read at least 300–500 words of the user's writing. Build a voice profile by scoring each:

1. **Sentence length distribution.** Mean, min, max. Are they a short-burst writer (6–12 words average) or a long-winder (25+)? Note the range.
2. **Opener patterns.** Do they start with "So," / "Look," / "Honestly," / "OK —" / a bare subject / a question? Note the top two or three.
3. **Contraction density.** "Don't" vs "do not," "it's" vs "it is." Fraction of contracted possibles.
4. **Em-dash and parens frequency.** Count per 200 words. Heavy, medium, or rare?
5. **Idiom set.** Pick 2–3 specific phrases the user reuses. ("Back-of-envelope," "the short version is," "for what it's worth.")
6. **Concrete-reference density.** Do they name brands, people, years, places? How many per paragraph?
7. **Emotional register.** Pick one: dry, warm, sardonic, enthusiastic, deadpan, earnest, combative. Be specific.
8. **Filler words.** "Basically," "I mean," "sort of," "kind of," "like." Which do they use, how often?
9. **Verb choice.** Active vs passive. Punchy Anglo-Saxon ("use," "run," "break") vs Latinate ("utilize," "facilitate," "elucidate"). Users almost always lean one way.
10. **Paragraph length preference.** Count sentences per paragraph across 5+ paragraphs. Do they write 2-sentence paragraphs or 8-sentence ones?

## How to apply the profile

Three steps:

1. **Summarize the voice in one paragraph.** Example: *"Mean sentence length 18 words, range 4–42. Opens paragraphs with bare subjects or 'So,'. Heavy contraction use. One em-dash per 8 sentences. Idioms: 'back of the envelope,' 'not a million miles from.' Names specific products and years. Dry, slightly sardonic. Uses 'basically' roughly once per 200 words. Anglo-Saxon verbs. Paragraphs run 3–7 sentences, uneven."*

2. **Rewrite to hit those distributions.** Not the user's *words* — the user's *shape*. If they average 18 words per sentence, your rewrite should too, with a similar range. If they're dry, don't add warmth. If they don't use "Not X — Y," neither should you.

3. **Read it and ask:** would a reader who knows this person assume *they* wrote this? If no, revise. If you're uncertain, tell the user and let them calibrate.

## Prompt template for a second LLM call

If the user wants to run voice-matching in a second pass or in their own tooling:

```
You are going to rewrite a piece of text to match a specific writer's voice.

First, read these samples of the target writer's work:

SAMPLE 1:
{sample1}

SAMPLE 2:
{sample2}

Build a profile covering:
- sentence length distribution (mean, range)
- opener patterns (top 2-3)
- contraction density
- em-dash / parens frequency
- 2-3 idioms they reuse
- emotional register (one word)
- filler words they favor
- active vs passive, Anglo-Saxon vs Latinate
- paragraph length

Then rewrite the following text to match that profile. Do not copy the samples' content — only their shape. Preserve all meaning from the target text.

TEXT TO REWRITE:
{text_to_rewrite}
```

## Failure modes

- **Too few samples.** Under ~200 words total and the voice profile is noise. Fall back to the seven moves in SKILL.md and tell the user.
- **AI-contaminated samples.** If the user used AI when writing the samples, matching that voice just reproduces AI cadence. Ask: "Are these fully your own writing, or did an assistant help draft them?" If contaminated, use the original human samples they have or switch to generic humanization.
- **Wanting to match someone else's voice.** If the user wants to sound like a specific famous writer or colleague without providing samples, refuse or use public corpus (with attribution). Don't generate style-impersonation from model training alone — it's usually a flat caricature.
- **Voice-matching isn't humanization.** The output will sound like the user. If the user's natural voice is itself detector-triggering (some academic or corporate registers are statistically close to AI), voice-matching alone won't save them. Pair with light seven-moves application.
