# Humanization Techniques vs AI Detectors

## What this is

A working best-estimate of which humanization techniques beat which detectors, current as of April 2026. The ratings below synthesize three main sources: Pangram's August 2025 humanizer evaluation (which caught all 19 commercial tools tested at 90–100%), Jabarian & Imas (UChicago BFI Working Paper 2025-116, September 2025), and TH-Bench (arXiv 2503.08708). Detector models get retrained on a monthly-ish cadence, so treat this as a snapshot, not a permanent map. Sanity-check against fresh evals before you bet anything important on a cell in this table.

## The matrix

✓ = reliable (>80% success in published evals) · ~ = partial · ✗ = fails · ? = unknown

| Technique | Pangram | Turnitin | GPTZero Pro (3.x) | Originality.ai 3 | Copyleaks | Winston | ZeroGPT | GPTZero free |
|---|---|---|---|---|---|---|---|---|
| Real humanization (seven moves) | ~ length-dependent | ~ mostly | ✓ works | ✓ works | ✓ works | ✓ works | ✓ works | ✓ works |
| Synonym swap / light paraphrase | ✗ caught | ✗ caught | ✗ caught | ✗ caught | ✗ caught | ✗ caught | ✗ caught | ✗ caught |
| Burstiness tuning only | ✗ caught | ✗ caught | ✗ caught | ✗ caught | ✗ caught | ✗ caught | ~ sometimes | ~ sometimes |
| Commercial humanizers | ✗ caught | ~ partial | ~ partial | ~ partial | ✓ slips | ✓ slips | ✓ slips | ✓ slips |
| Adversarial paraphrasing | ~ reduced | ✓ works | ✓ works | ✓ works | ✓ works | ✓ works | ✓ works | ✓ works |
| Homoglyph / zero-width | ✗ tampering | ✗ tampering | ✗ tampering | ✗ tampering | ✗ flagged | ✗ flagged | ✗ flagged | ✗ flagged |
| Typo injection | ✗ caught | ✗ caught | ✗ caught | ✗ caught | ✗ caught | ~ noisy | ~ noisy | ~ noisy |
| Register shift (casual↔formal) | ~ moderate | ~ moderate | ~ moderate | ~ moderate | ~ moderate | ~ moderate | ~ moderate | ~ moderate |

Note on homoglyphs and zero-width tricks: Pangram, Turnitin, GPTZero, and Originality all flag these as tampering signals, which is worse than leaving the text clean. Don't use them.

## Per-detector notes

**Pangram.** Strongest detector on the market as of April 2026. Uses a fine-tuned transformer classifier trained on synthetic-humanized corpora, including outputs from every major commercial humanizer. Jabarian & Imas confirmed near-zero false positives and false negatives against adversarial humanizers on passages over 250 words. Strength: catches structural AI shape even after aggressive rewriting. Weakness: shorter passages (under 100 words) and heavily domain-specific text (legal, medical, technical specs) leak more. Recent update: February 2026 model refresh added stronger Claude 4.x and Gemini 3 detection; em-dash density is now a weighted feature rather than a hard rule.

**Turnitin.** Designed for academic submissions, so optimized for long-form essay structure and citation patterns. Retrained in late 2025 on humanized training data, which closed the synonym-swap and commercial-humanizer loopholes that worked in 2024. Strength: very high true-positive rate on untouched LLM output in academic register. Weakness: inherits institutional conservatism on false positives, so it's tuned to under-flag, which means heavy real humanization usually gets through. Register-shifted casual prose confuses it more than the other enterprise detectors.

**GPTZero Pro (v3.x).** Transformer-based classifier plus burstiness and perplexity features kept as secondary signals. Middle of the pack against adversarial paraphrasing, behind Pangram but ahead of Originality. Strength: consistent performance across lengths from ~150 words up. Weakness: register shifts and genuine voice injection move the needle noticeably; still over-relies on em-dash frequency as a feature despite claims otherwise. Recent update: v3.2 in January 2026 added a multi-model ensemble head. Free tier (non-Pro) is a much weaker model and shouldn't be conflated with Pro.

## Caveats

- **Length matters a lot.** Most detectors get much stronger past 250 words and much weaker under 100. Results above assume medium-length passages (roughly 300–800 words).
- **Domain matters.** Academic, legal, and technical writing have narrower human baselines, so detectors flag more aggressively. Casual and creative prose gives humanization more room to work.
- **Source LLM matters.** Claude 4.x and GPT-5.x outputs are caught more reliably than Gemini 2.x; newer frontier models may evade detectors trained on older corpora for a few weeks after release.
- **Training cutoff matters.** A detector trained before a given humanizer existed will miss it until the next retrain cycle (typically 4–8 weeks behind).
- ✓ means >80% success in published evals, not 100%. Any individual passage can still get flagged.

## Decision rule

- If the detector is Pangram and stakes are high, don't promise defeat. Use adversarial paraphrasing if the user has API access, and warn them it still isn't bulletproof.
- If the detector is Turnitin, Originality.ai 3, or GPTZero Pro and the passage is under 600 words, real humanization (the seven moves) is usually enough. Lean on specifics and structural irregularity hardest.
- If the detector is a free-tier or older consumer tool (GPTZero free, ZeroGPT, Copyleaks, Winston), almost any genuine rewrite works. Don't overthink it.
- Never reach for homoglyphs, zero-width characters, or typo injection. They now hurt more than they help against any detector worth worrying about.
- Synonym swaps and burstiness-only tuning are wasted effort on every modern detector. Skip them.
- If the user won't name the detector, assume Pangram or Turnitin and plan accordingly — over-preparing is cheaper than under-preparing.
