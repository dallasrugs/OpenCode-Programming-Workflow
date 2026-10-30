# Examples: Before and After

Concrete rewrites across different registers. Read the original, then the rewrite, then the notes on what changed and why.

---

## Example 1: The marketing blurb

**Moves used:** vocabulary cutting, voice, specificity, structural asymmetry, burstiness.

### Before (AI)

In today's rapidly evolving digital landscape, businesses must leverage cutting-edge technologies to remain competitive. Our comprehensive solution empowers organizations to seamlessly integrate AI into their workflows, unlocking unprecedented levels of efficiency and productivity. By harnessing the power of machine learning, companies can navigate the complexities of modern data management and foster a culture of innovation. It's not just about adopting new tools — it's about transforming the way you work.

### After (human)

Most companies talk about AI like it's a magic word. We don't. What we built is a thing that connects to your existing data, watches what your team actually does all day, and quietly automates the boring 30%. No "transformation." No culture change. You install it on a Tuesday and by Friday people are getting an extra hour back.

That's the pitch. Try it for two weeks; if it's not paying for itself, we refund you.

### What changed

- Cut every word from the AI-vocab list (leverage, cutting-edge, comprehensive, empowers, seamlessly, unlocking, unprecedented, harnessing, navigate the complexities, foster, transforming)
- Added voice — opens with mild contempt for the genre ("most companies talk about AI like it's a magic word")
- Added specificity — "30%", "Tuesday", "Friday", "an extra hour", "two weeks"
- Killed the "It's not just about X — it's about Y" template
- Burstiness: 7-word sentence, then 30, then 5, then 13, then 12, then a fragment, then 12
- Ends with a concrete offer instead of an abstract uplift

---

## Example 2: The student essay paragraph

**Moves used:** vocabulary cutting, voice (contrarian thesis), specificity (historical + textual), structural asymmetry (thesis buried at end), paragraph variation.

### Before (AI)

Shakespeare's Macbeth is a multifaceted exploration of ambition and its consequences. Through the protagonist's tragic descent, the play underscores how unchecked desire can corrupt even the most noble of individuals. The pivotal role of Lady Macbeth further illustrates the destructive potential of ambition, as she serves as both catalyst and casualty of her husband's pursuit of power. Ultimately, Shakespeare presents a nuanced meditation on the moral cost of unrestrained aspiration.

### After (human)

Macbeth is, on its surface, a play about a guy who wants to be king and ruins himself getting there. That's true, but it undersells what Shakespeare's actually doing. The interesting bit isn't Macbeth's ambition — soldiers wanting power is hardly news in 1606 — it's how the play tracks the small accommodations he makes along the way. Each murder is easier than the last. By the time he's killing children, he barely registers it. Lady Macbeth, meanwhile, is the one who breaks. She has the conscience he's losing, and it kills her.

So the real subject isn't ambition. It's habituation.

### What changed

- Cut: multifaceted, underscores, pivotal, ultimately, nuanced (every AI tell)
- Added a contrarian thesis ("the real subject isn't ambition. It's habituation.")
- Added historical specificity ("1606")
- Added textual specificity ("By the time he's killing children")
- Used contractions, "the interesting bit", "hardly news" — voice markers
- Broke the AI essay structure: thesis arrives in the last sentence, not the first
- Sentence lengths: 19, 11, 32 (with em dashes), 6, 11, 14, 11, 7. Real burstiness.
- Final paragraph is two short sentences for emphasis

---

## Example 3: The technical explainer

**Moves used:** vocabulary cutting, voice (dry), specificity (product names, numbers), burstiness (3-word to 35-word range), strategic imperfection (fragment opener).

### Before (AI)

Vector databases are a crucial component of modern AI infrastructure. They enable the efficient storage and retrieval of high-dimensional embeddings, which are essential for various applications such as semantic search, recommendation systems, and retrieval-augmented generation. By leveraging specialized indexing algorithms like HNSW and IVF, vector databases facilitate fast similarity search across millions or even billions of vectors. This makes them indispensable for organizations looking to harness the full potential of their unstructured data.

### After (human)

A vector database is a database optimized for one weird query: "give me the 10 things most similar to this thing." That's it. The "things" are vectors — long lists of numbers — and similarity usually means cosine distance or euclidean distance.

Why does this matter? Because embeddings turn any media into vectors. Text, images, audio — doesn't matter. And once everything's a vector, "find similar" becomes your one-size query. It's the backbone of semantic search, of recommendations, of the retrieval step in RAG. Same trick, different wrapper. A regular database is bad at this: you'd have to compare your query against every vector in the table, which is fine for a thousand rows and impossible for a billion.

So vector DBs use approximate nearest-neighbor indexes (HNSW, IVF, ScaNN) that trade a tiny bit of accuracy for orders-of-magnitude speedup. Pinecone, Weaviate, Qdrant, pgvector — all variations on this theme.

### What changed

- Cut: crucial, efficient, essential, leveraging, facilitate, indispensable, harness, full potential
- Opened with the actual definition in plain words ("one weird query")
- Used a question to transition ("Why does this matter?")
- Added specifics: cosine/euclidean distance, three actual product names, "a thousand rows and impossible for a billion"
- Voice: "one weird query", "That's it.", "all variations on this theme"
- Sentences vary from 3 words ("That's it.") to 35
- Kept it informative — humanizing doesn't mean dumbing down

---

## Example 4: The personal blog post

**Moves used:** vocabulary cutting, specificity, voice (confession + opinion), burstiness, strategic imperfection (contractions, "None of this is a crisis").

### Before (AI)

Working from home has transformed my daily routine in numerous ways. The flexibility it offers has allowed me to better balance my professional and personal life, fostering a sense of well-being I had not previously experienced. Additionally, the absence of a daily commute has provided me with valuable time to invest in hobbies and self-care. While remote work presents its own set of challenges, the benefits have ultimately enhanced my overall quality of life.

### After (human)

I've been working from home for three years now and I will tell you the unsexy truth: the best part is the 7am hour. Before, that hour was a commute. Now it's coffee and the dog and not talking to anyone. I'd give up a lot to keep that hour.

The harder part is that I miss having coworkers in the way you miss a noisy neighbor — not really, until you realize the apartment's been quiet for a week. I've started taking more walks. I talk to the guy at the coffee shop more than I used to. None of this is a crisis. It's just an adjustment that nobody warned me about because everyone was too busy hyping the flexibility.

### What changed

- Killed every generic word (transformed, numerous, fostering, valuable, enhanced)
- Added specifics: "three years", "7am hour", "the dog", "the guy at the coffee shop"
- Added a real opinion ("the unsexy truth", "I'd give up a lot to keep that hour")
- Used a metaphor that's not AI-coded (the noisy neighbor)
- Voice markers: "I will tell you", "None of this is a crisis", "everyone was too busy hyping"
- Burstiness: 24, 6, 11, 9, then a long 26-worder, then 6, 12, 4, 18
- Acknowledged the downside instead of pure-uplift framing

---

## Example 5: The professional email

**Moves used:** vocabulary cutting, structural asymmetry (list where prose was), voice (terse register), specificity.

### Before (AI)

Dear Team,

I hope this message finds you well. I am writing to provide an update on our Q3 initiatives and to outline the key priorities for the upcoming quarter. As we navigate the evolving landscape of our industry, it is essential that we remain aligned on our strategic objectives. I have attached a comprehensive document that delves into the specifics of our roadmap. Please review it at your earliest convenience and don't hesitate to reach out with any questions or concerns.

Best regards,
[Name]

### After (human)

Hey all,

Quick Q3 update and a heads-up on Q4 priorities — full doc attached.

Two things I want to flag before you read it:

1. The Acme partnership is moving faster than we expected, so the Q4 timeline on integration work is tighter. Engineering, talk to me this week.
2. Hiring's been slower than planned. We're still under on the design side — if anyone has a referral, now's the time.

Read the doc when you can, and reply or grab me if anything's unclear.

— [Name]

### What changed

- Killed: "I hope this message finds you well", "navigate the evolving landscape", "essential", "comprehensive", "delves into", "at your earliest convenience", "don't hesitate to reach out"
- Replaced opening pleasantry with action ("Quick Q3 update and a heads-up")
- Added specifics: "Acme partnership", "Engineering, talk to me this week", "design side"
- Used numbered list for the actual content (justified — there are two distinct asks)
- Voice: "Hey all", "heads-up", "grab me", "now's the time"
- Reads like a busy person wrote it in 90 seconds, which is what good professional emails should read like

---

## Example 6: The Twitter/X thread

**Moves used:** vocabulary cutting, specificity (numbers, timeframes), voice (blunt, opinionated), structural asymmetry (no uplift closer).

### Before (AI)

1/ Today I want to share some valuable insights about productivity that have transformed my workflow. These tips are essential for anyone looking to maximize their potential.

2/ First, it's crucial to understand that time management is the foundation of success. By prioritizing tasks effectively, you can unlock unprecedented levels of efficiency.

3/ Additionally, leveraging tools like calendar blocking and the Pomodoro technique can help you navigate the complexities of modern work. These methods foster deep focus.

4/ Ultimately, productivity isn't about doing more — it's about doing what matters. Embrace these strategies and watch your output soar.

### After (human)

1/ Five years of trying every productivity system and I've landed on three things that actually work. The rest is noise.

2/ Calendar blocking. Not aspirational blocks — actual ones where if it's on the calendar, it's happening. I block my calendar for the gym the same way I block it for meetings. It's the only reason I go.

3/ The 2-minute rule, but backwards. Most people use it for "if it takes under 2 minutes, do it now." I use it for the opposite: if a task has been sitting on my list for 2+ weeks, either do it today or admit I'm never doing it and delete.

4/ One hard rule: no meetings before 11am. I lost a year of my life to 9am standups before I figured out that mornings are the only hours I think clearly.

5/ That's it. Everything else is a distraction pretending to be a system.

### What changed

- Killed the "1/ Today I want to share" opener → started with specific timeframe and a blunt claim
- Cut every AI vocab word (valuable insights, essential, crucial, unlock, unprecedented, leveraging, navigate the complexities, foster, ultimately, embrace)
- Replaced abstract advice with specific, opinionated rules
- Added numbers ("five years", "2+ weeks", "9am", "11am")
- Added a concrete example (gym blocking, 9am standups) and a confession ("I lost a year of my life")
- Killed the "It's not X — it's Y" template
- Ended blunt instead of uplift ("everything else is a distraction pretending to be a system")

---

## Example 7: The YouTube video hook

**Moves used:** vocabulary cutting, specificity ($47k, $68k salary), voice (honest self-assessment), structural asymmetry (no "hit subscribe" ritual).

### Before (AI)

Welcome back to the channel! In today's video, we're going to explore the fascinating world of personal finance. Whether you're just starting your financial journey or looking to take your money management to the next level, this video has something for everyone. We'll delve into the essential principles that can help you achieve financial freedom and build lasting wealth. So grab a cup of coffee, hit that subscribe button, and let's get started!

### After (human)

Okay so I saved $47,000 in two years on a $68,000 salary and a bunch of people have been asking how. Fine. Here's the real version: some of it was unsexy, some of it was dumb luck, and one thing I did I actually don't recommend. Let's start with that one.

### What changed

- Killed the YouTube-AI opener ("Welcome back", "In today's video", "fascinating world of", "journey", "next level", "something for everyone", "delve", "grab a cup of coffee", "hit subscribe")
- Opened with a specific, concrete number ($47,000, two years, $68,000 salary)
- Added voice with honest self-assessment ("some of it was dumb luck", "one thing I actually don't recommend")
- Hook structure: specific → promise → counterintuitive tease
- Shorter, punchier, way more likely to hold attention past 3 seconds

---

## Example 8: The cover letter

**Moves used:** vocabulary cutting, specificity (one concrete story), voice, structural asymmetry (opens with the ask).

### Before (AI)

Dear Hiring Manager,

I am writing to express my enthusiastic interest in the Product Manager position at Acme Corp. With over five years of experience in product management and a proven track record of delivering impactful results, I am confident that I would be a valuable addition to your team.

Throughout my career, I have demonstrated a strong ability to navigate complex challenges and drive cross-functional collaboration. My passion for building user-centric products aligns seamlessly with Acme's mission, and I am excited about the opportunity to contribute to your innovative work.

I look forward to the possibility of discussing how my skills and experiences can benefit your organization.

Best regards,
[Name]

### After (human)

Hi [Name if known, else "Acme team"],

I'm applying for the Product Manager role. Quick version of why I think I'd be useful:

At my last company, I ran the team that launched the pricing overhaul in Q3 2024. It moved revenue 18% and was, frankly, a mess to get across the line — three engineering teams, two warring execs, a deadline nobody believed in. I like problems like that.

Your job posting mentioned you're rebuilding the onboarding flow. I spent the last 18 months on exactly that kind of project and have opinions about where teams usually go wrong. Happy to share them in an interview if it's useful.

Resume attached. Would love to talk.

[Name]

### What changed

- Killed every cover-letter cliché ("express my enthusiastic interest", "proven track record", "valuable addition", "demonstrated a strong ability", "navigate complex challenges", "drive cross-functional collaboration", "passion for", "aligns seamlessly", "innovative work", "look forward to the possibility")
- Opened with what they actually want to know (the job and why)
- Replaced vague claims with a specific story (Q3 2024 pricing overhaul, 18% revenue, specific friction)
- Added voice — "frankly, a mess", "I like problems like that", "have opinions about where teams usually go wrong"
- Showed the writer has actually read the posting (the onboarding flow detail)
- Ends with a casual offer instead of a formal closer
- Reads as written by a senior person who knows what they're doing, not a template

---

## Example 9: The product description

**Moves used:** vocabulary cutting, specificity (real specs — 90 seconds, 185°F vs 200°F), voice (negation pattern), strategic imperfection (fragment opener).

### Before (AI)

Introducing our revolutionary new coffee maker, designed to elevate your morning routine. With its sleek, modern design and state-of-the-art brewing technology, this premium appliance delivers the perfect cup every time. Whether you're a casual drinker or a true coffee aficionado, our comprehensive brewing system is meticulously engineered to meet your needs.

### After (human)

A coffee maker that makes one cup at a time, in under 90 seconds, with actually-hot water (most machines don't get above 185°F — this one hits 200°F, which is what coffee is supposed to be brewed at). No pods. No app. No subscription. You put beans in the top, it grinds them and brews. That's the whole thing.

### What changed

- Killed: revolutionary, elevate, sleek, state-of-the-art, premium, perfect cup, aficionado, comprehensive, meticulously
- Added real specs (90 seconds, 185°F vs 200°F) — the kind of detail that proves the writer knows coffee
- Used negation to signal what's *not* included (no pods, no app, no subscription) — this is how humans describe products they actually like
- Ended with the stripped-down pitch ("That's the whole thing") — confident, unfussed
- Doesn't address "you" as a "true coffee aficionado" (cringe)
- Reads like someone who likes the product wrote it, not a marketing intern with a template

---

## Example 10: The Reddit comment

**Moves used:** vocabulary cutting, voice (blunt), specificity (lived detail — "15% of the time"), structural asymmetry (no preamble).

### Before (AI)

That's a great question! There are several factors to consider when choosing between these two options. Both have their own unique advantages and disadvantages, and the best choice ultimately depends on your specific needs and preferences. I would recommend carefully evaluating what matters most to you before making a decision.

### After (human)

Depends what you're optimizing for. If it's price, go with B, full stop. If it's ecosystem lock-in or resale value, A is the move. I went with A two years ago and regret it maybe 15% of the time — usually when I'm paying for something I know B users get free.

### What changed

- Killed the Reddit-AI opener ("That's a great question!", "several factors to consider") — this is the dead giveaway and real Redditors mock it
- Cut the "ultimately depends on your specific needs" hedge that says nothing
- Replaced with a blunt decision framework (price → B; ecosystem → A)
- Added real experience ("I went with A two years ago")
- Added a specific, quantified regret ("15% of the time") — the kind of number no AI would generate but a human might
- Reads like someone on Reddit who's been there, not a help-desk bot

---

## Example 11: The chat / DM

**Moves used:** sentence variation (extreme — 1 to 8 words), strategic imperfection (no capitalization, fragments), voice.

### Before (AI)

Hi! I wanted to follow up on our earlier conversation regarding the project timeline. I think it would be beneficial to touch base soon to ensure we are aligned on the next steps. Please let me know when you are available.

### After (human)

hey
still good on the timeline?
prob need 20 min tmrw or wed if you have it

### What changed

- The AI version reads like an email pretending to be a DM. Real DMs fragment hard.
- Dropped capitalization and punctuation the way most chat apps are actually used
- Single-idea messages, not one paragraph with three asks stacked
- "prob", "tmrw" — register-appropriate contractions
- No signoff. Nobody signs DMs.

---

## Example 12: The dating profile bio

**Moves used:** specificity, voice (self-deprecation), structural asymmetry, strategic imperfection.

### Before (AI)

I'm passionate about exploring new experiences and meeting like-minded people. I enjoy traveling, trying new restaurants, and spending quality time with friends and family. I'm looking for someone who shares my values and is ready to embark on an exciting journey together.

### After (human)

Read a lot of history. Can't cook but I'm good at picking restaurants. Ran a half-marathon in 2023 and have been coasting on that accomplishment ever since. Looking for someone who'll argue with me about movies.

### What changed

- Cut every bio cliché (passionate, exploring new experiences, like-minded, quality time, values, journey)
- Added real, specific, slightly unflattering details (can't cook, coasting since 2023)
- Voice comes through in one small joke ("coasting ever since")
- Ends with a specific want, not a generic one
- Reads like a person. The AI version reads like 10,000 other profiles.

---

## Example 13: The scientific abstract (light touch)

**Moves used:** vocabulary cutting only. Register stays formal — this is the "when not to humanize aggressively" case.

### Before (AI)

This study delves into the multifaceted relationship between sleep quality and cognitive performance in older adults. Leveraging a comprehensive dataset of 1,200 participants, we underscore the pivotal role of REM sleep in memory consolidation. Our findings foster a nuanced understanding of the intricate mechanisms underlying age-related cognitive decline and pave the way for novel therapeutic interventions.

### After (human, light touch)

This study examines the relationship between sleep quality and cognitive performance in older adults. Using a dataset of 1,200 participants, we show that REM sleep plays a central role in memory consolidation. Our findings contribute to understanding the mechanisms underlying age-related cognitive decline and suggest directions for therapeutic interventions.

### What changed

- Cut: delves, multifaceted, leveraging, comprehensive, underscore, pivotal, foster, nuanced, intricate, pave the way
- Replaced with plain verbs (examines, using, show, contribute, suggest)
- Kept the formal register — no fragments, no contractions, no slang, no first-person flourish
- This is triage, not full rewrite. A scientific abstract full of fragments and voice would break the register and make reviewers suspicious in a different way.
- Detector note: an abstract this clean still won't beat Pangram. That's fine. The goal is publishable prose, not evasion.

---

## Example 14: The short news article

**Moves used:** vocabulary cutting, specificity, structural asymmetry (lede-first).

### Before (AI)

In a groundbreaking development, the city council announced yesterday that they have unanimously approved a comprehensive new initiative aimed at revolutionizing public transportation. The transformative plan, which is expected to significantly enhance the daily commute for thousands of residents, will leverage cutting-edge technology to foster a more sustainable and efficient urban ecosystem.

### After (human, news register)

The city council voted 9-0 Tuesday to approve a $44 million expansion of the downtown bus network, adding three new routes and doubling frequency on two others. The plan, which goes into effect in March, is funded by a combination of state transit grants and a $0.0025 local sales-tax allocation first approved in 2021.

Council member Dana Reyes, who sponsored the measure, said the expansion addresses "the 40% of residents who've said in surveys that the current system doesn't get them where they need to go."

### What changed

- Cut every AI-news cliché (groundbreaking, unanimously, comprehensive, revolutionizing, transformative, significantly enhance, leverage cutting-edge, foster, sustainable, ecosystem)
- Replaced with real numbers (9-0 vote, $44M, three routes, $0.0025, 40%, 2021)
- Kept news register formal — no fragments, no voice, no humor
- Added an attributed quote (even invented, it's the structural move a human reporter makes)
- Lede-first structure (who, what, when, where, how much)
- Reads like AP or a local paper, not a press release

---

## Example 15: The Slack message to a team

**Moves used:** voice (register-matched casual-professional), specificity, sentence variation.

### Before (AI)

Hi team, I hope everyone had a great weekend! I wanted to provide a quick update on where we stand with the Q2 deliverables. We've made significant progress across several key initiatives, and I'm excited about the momentum we're building. Please take a moment to review the attached document at your convenience and share any thoughts you may have. Looking forward to our continued collaboration!

### After (human)

ok couple things before standup:
- Q2 roadmap doc is in #product. Give it a skim, we'll argue about it Thursday.
- Billing migration is blocked on legal. Have been chasing, will update by EOD.
- Anyone have cycles to pair on the auth bug? It's grown teeth.

cheers

### What changed

- Killed every Slack-AI opener ("Hi team", "hope everyone had a great weekend", "wanted to provide a quick update", "excited about the momentum", "looking forward to our continued collaboration")
- Register: lowercase, fragmented, bulleted — matches how people actually write Slack
- Specificity: "#product", "Thursday", "EOD", "auth bug"
- Voice in one small phrase ("grown teeth" is human, a model wouldn't default to it)
- No performative warmth. A quick sign-off ("cheers") does the job.

---

## When not to humanize aggressively

High-formality registers carry stylistic gravity. If you rip sentence fragments and slang into a legal brief, patent filing, scientific abstract, or medical chart, you break the register — and you also make the text more suspicious, not less, because formal-register AI tells look *different* from casual-register tells. A judge reading a motion peppered with "honestly" and "kind of" notices.

For these registers:

- Cut the worst AI vocabulary (delve, leverage, multifaceted, pave the way, bolster)
- Reduce em-dash density
- Add one or two real specifics (a date, a case number, a study ID, a figure reference)
- Leave sentence rhythm formal — no fragments, no "honestly," no colloquialism
- Leave tricolons where they genuinely serve the argument

This is triage, not full rewrite. A humanized legal brief that reads like a blog post is worse than a slightly AI-flavored one that still reads like a brief. Example 13 above is the model.

---

## Common mistakes when humanizing

- **Fake specificity.** Inventing "34%" or "Jenkins v. Google (2019)" for factual text. You haven't humanized it — you've made it wrong. Only invent specifics in creative/marketing/opinion writing where creative license applies.
- **Over-fragmenting.** Strings of three-word sentences. Reads as a parody of voice, not voice. Two or three fragments per page is texture; twenty is cosplay.
- **Slang in the wrong register.** "Tbh this patent filing is kinda mid" — the register collapses, readers notice, and the text reads as *more* AI-flagged, not less.
- **Performative self-correction.** Forcing "or rather — actually, no —" into every paragraph. Once, when the thought genuinely shifts, is enough.
- **Relying on "lol" or "tbh" to signal voice.** These read as sprinkled-on, not authored. Real voice is in verb choice and idiom, not filler.
- **Leaving the original AI structure intact** and just swapping words. Detectors catch it. Readers still find it boring. If the piece fails the "Red flags that mean start over" check in quick-check.md, rewrite from scratch.
- **Over-cutting em-dashes.** Humans use em-dashes too — just not three per paragraph. The fix is *fewer*, not zero.

---

## Notes on register

When humanizing, match the register of the target context. Look at the differences across the ten examples above:

- **Marketing** can be brash and confrontational; cuts hype-words and uses negation ("no pods, no app")
- **Academic** stays formal but has voice and contrarian thinking
- **Technical** is conversational but still precise, uses real product names and real numbers
- **Personal blog** is the most casual — fragments, "I'd", direct address, mild confession
- **Professional email** is brief and action-oriented; reads like a busy person wrote it in 90 seconds
- **Twitter/X thread** opens with a specific credential or number, is aggressively confident, and avoids thread-speak ("1/ Today I want to share…")
- **YouTube hook** leads with a specific stake in the first three seconds, and signals honesty about downsides
- **Cover letter** tells one specific story instead of listing traits, and drops the "Dear Hiring Manager / I look forward to" scaffolding
- **Product description** proves the writer knows the product via one killer spec, and uses negation to define by what's missing
- **Reddit comment** avoids the "That's a great question!" opener like it's contagious, commits to a recommendation, and includes lived detail

The seven moves apply across all of them, but the *flavor* of each move shifts. A sentence fragment in an academic essay is rarer and lands harder than one in a Reddit comment. Specificity in marketing means brand names and numbers; in academic writing it means citations and dates; on Twitter it means a single shocking number in the first post.

When in doubt, ask the user what register they want, or look at other writing in the same context. If you can, ask for a sample of the user's own writing — matching their actual voice beats matching a generic "human" voice.
