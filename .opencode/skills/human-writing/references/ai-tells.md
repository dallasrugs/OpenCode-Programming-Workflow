# AI Tells: Words, Phrases, and Patterns to Cut

The checklist. When humanizing text, scan for these and either delete, replace, or restructure.

---

## Top-tier tell: em-dash saturation

Em-dashes are good — humans use them — but AI uses them as default rhythm glue, typically 2–4× the human rate. This has become **the** single most-cited AI signal of 2025, to the point where OpenAI shipped a GPT-5.1 preference toggle in November 2025 specifically to suppress it.

**Rule of thumb:** Cap at 1 em-dash per 4–5 sentences in casual/blog prose, 1 per 8+ in formal writing. If you have three in four sentences, replace most with commas, parens, full stops, or restructure.

Parenthetical em-dashes mid-clause ("the plan — a long one — was finally —") are particularly Claude 4.x-flavored.

---

## Words AI overuses

These words appear in human writing too. The issue is *frequency* and *register* — AI reaches for them when a plainer word would do.

**The classics (cut on sight in casual/conversational text):**
- delve, delving
- leverage (as a verb)
- underscore
- multifaceted
- robust
- seamless / seamlessly
- holistic
- foster (metaphorical)
- navigate (metaphorical, "navigate the complexities")
- realm
- landscape (metaphorical, "the current landscape")
- tapestry
- testament ("a testament to")
- pivotal
- paramount
- crucial
- vital (when "important" works)
- comprehensive
- nuanced (overused; sometimes right, often padding)
- intricate
- meticulous
- elevate (metaphorical)
- empower
- cutting-edge
- state-of-the-art
- bespoke (when not literally about tailoring)
- curated
- streamline
- optimize
- facilitate
- utilize (always replace with "use")
- myriad
- plethora
- ensure (in marketing contexts; "make sure" is more human)

**2025 additions (spiked >50% usage in AI output since ChatGPT launch per Max Planck corpus study):**
- bolster
- unpack (as in "let's unpack this")
- pave the way
- spearhead
- revolutionize
- transformative
- ecosystem (metaphorical)
- paradigm
- synergy (no longer just corporate-speak; now generic AI)
- vibrant
- shed light on
- harness

**Adjectives that signal AI hedging:**
- significant, significantly
- various
- numerous
- diverse (when used vaguely)
- key (as in "key insights")
- essential
- fundamental (when overused)

**Adverbs to thin out:**
- arguably
- notably
- importantly
- ultimately
- essentially
- fundamentally
- effectively
- particularly

---

## Phrases to cut entirely or rewrite

**Filler openings:**
- "In today's [fast-paced / digital / modern / interconnected] world…"
- "In recent years…"
- "Throughout history…"
- "Since the dawn of…"
- "It is widely known that…"
- "It goes without saying that…" (then proceeds to say it)

**Padding mid-sentence:**
- "It is important to note that…"
- "It's worth mentioning that…"
- "It should be noted that…"
- "One must consider…"
- "It is essential to understand…"
- "When it comes to…"
- "In terms of…"
- "With regard to…"
- "In the context of…"

**Closers:**
- "In conclusion,"
- "To sum up,"
- "All in all,"
- "Ultimately,"
- "In summary,"
- "By embracing [X], we can [Y]"
- "As we move forward,"
- "Only time will tell."

**The metaphor cluster:**
- "navigating the complexities of…"
- "unlock the potential of…"
- "harness the power of…"
- "shed light on…"
- "delve into…"
- "dive deep into…"
- "paint a picture of…"
- "weave together…"
- "a treasure trove of…"
- "the heart of the matter"
- "at the end of the day"
- "in the realm of…"
- "the world of…"
- "pave the way for…"

**The contrast template (LinkedIn-weaponized now — call out by name):**
- "Not X — Y" ("Not just a feature — a revolution")
- "Not only [X], but also [Y]"
- "[X] is not just about [Y], it's about [Z]"
- "It's not [X] — it's [Y]"

This pattern is so heavily AI-associated in 2025–2026 that readers actively roll their eyes at it. Cut unless the contrast genuinely needs the emphasis.

---

## Structural tics

**The rule of three (tricolons).** AI loves grouping things in threes:
- "fast, efficient, and reliable"
- "elegant, intuitive, and powerful"
- "we'll explore, examine, and analyze"

Humans use threes sometimes but break the pattern often. Cut one item, add a fourth, or restructure.

**The balanced "however" sentence.** "X is true. However, Y is also true." Endless balanced contrasts make text feel like a hedging model. Real writers commit.

**Topic sentence + 3 supports + summary.** Every paragraph following this template signals AI. Mix it up — bury the topic sentence, open with the supporting detail, open with a question.

**The "as an AI" relatives:**
- "While I can't [X], I can [Y]"
- "It's important to consider multiple perspectives"
- "There's no one-size-fits-all answer"

Model-speak even when "AI" isn't mentioned. Cut.

**Bullet point overuse.** AI converts everything into bullets. Often prose is better. Three flowing sentences > three bullets, most of the time.

**Headers for everything.** AI subdivides aggressively. A 400-word piece doesn't need 6 headers. Often it needs zero.

---

## Model-specific tells (2025–2026)

Different frontier models default to different tics. If you know which model produced the text, target the specific pattern.

### Claude 4.x (Sonnet / Opus)

- **Parenthetical em-dashes mid-clause:** "The plan — an ambitious one, honestly — ran into trouble."
- **Reflexive "Not X — Y" negative parallelisms.** Claude uses this more heavily than other models.
- **Rhythmic tricolons** that land on a beat: "fast, clean, and built to last."
- **"I should note" / "It's worth mentioning"** hedges, even when unprompted.
- **Slight over-warmth** — phrases like "happy to help," "great question," softening that reads as sycophantic once noticed.
- **Reveal-phrase openers** (very common in casual Claude output): "Here's the thing," "Here's the part nobody wants to say out loud," "Here's what people miss," "The truth is," "The real question is," "What people get wrong is." These frame a claim with a faux-insider meta move. Cut all of them on sight.
- **Instructional-essay imperatives at paragraph openers:** "Start with the boring truth about X." "Consider this." "Picture this." Reads as a self-help essay regardless of register.

### GPT-5.x (ChatGPT, API)

- **Scaffolding openers:** "Here's the thing:", "The short answer:", "TL;DR:", "Quick take:".
- **High function-word density** — lots of "this," "that," "which," "these" doing referential work.
- **Marketing-voice mimicry** when asked for casual prose — slides into LinkedIn cadence unprompted.
- **Bolded key phrases** in paragraphs that don't need them.
- **Frequent "let's" and "we"** creating false collaborative tone.

### Gemini 2-3 (Google)

- **Schematic paragraph scaffolding** — every paragraph topic-sentence-then-three-points, almost rigid.
- **Low vocabulary entropy** — the same term reused instead of varied (e.g., "the system" three times where a human would use pronouns or synonyms).
- **Over-formal register** even in casual prompts — defaults to a report voice.
- **Heavy hedging** — "could," "may," "might," "sometimes," "in some cases" stacked within single sentences.
- **Terminology reuse** with Capitalized Key Phrases repeated across paragraphs as if cross-referencing.

---

## Punctuation tells

- **Em-dashes everywhere.** See the top-tier section above. This is now the #1 punctuation signal.
- **Oxford commas on every list.** Humans are inconsistent. Sometimes drop one.
- **Colons introducing lists.** Overdone. Sometimes a sentence flows better without the colon-list structure.
- **Smart quotes vs straight quotes.** Some detectors look at this. Inconsistency is more human than perfect uniformity, but don't make this load-bearing.

---

## The corporate-LinkedIn cluster

Its own dialect of AI prose. Watch for:
- "passionate about"
- "thrilled to announce"
- "humbled and honored"
- "a journey"
- "this is just the beginning"
- "stay tuned"
- "game-changer"
- "synergy" (now also in generic AI output)
- "value-add"
- "circle back"
- "deep dive"
- "low-hanging fruit"
- "moving the needle"

If the target register is professional but not LinkedIn, cut all of these.

---

## Unicode / homoglyph / invisible-character tricks

**Don't use them.** Pangram, Originality.ai, and GPTZero all ship dedicated scanners for:
- Mixed-script characters (Cyrillic "а" in place of Latin "a," etc.)
- Zero-width spaces and non-breaking spaces in unusual positions
- Homoglyph substitutions at any density above background noise

Once detected, these are flagged as **tampering signals** — meaning the text gets treated as *more* suspicious than clean AI output, not less. Originality has a public homoglyph detector live at originality.ai. This was risky in 2024; in 2026 it's actively worse than doing nothing.

---

## What to add instead

Humans use language AI underuses:

- Contractions (don't, won't, can't, you're, it's)
- Specific numbers, dates, names, brands, places
- Slang and idioms appropriate to the register
- Sentence fragments. Like this.
- Conjunctions to start sentences. And questions.
- Self-correction ("or rather…", "actually, no —", "scratch that")
- Hedges that sound human ("I think", "probably", "kind of", "more or less", "honestly")
- Asides in parens or dashes (sparingly — see em-dash note)
- Rhetorical questions (sparingly)
- Mild profanity if the register allows
- Repetition for emphasis (the human kind — same word twice in a row, not AI-style restating the same idea three different ways)

---

## Quick scan checklist

Before delivering a rewrite:

1. Any word from the "classics" or "2025 additions" lists — replace or cut
2. Any phrase from "filler openings" or "padding" — cut
3. Em-dash density above 1 per 4 sentences — cut or restructure
4. More than two tricolons in the piece — break one
5. "Not X — Y" contrast template — probably cut
6. Every paragraph the same length — vary
7. Every sentence 15–25 words — add shorts and longs
8. No contractions — add some if register allows
9. No specific names, numbers, or examples — add if possible
10. Headers on a piece under 500 words — probably remove
11. Model-specific tics (Claude/GPT/Gemini) if you know the source — target them
