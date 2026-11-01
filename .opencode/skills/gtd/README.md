# gtd — Getting Things Done, operated

A [Claude Code](https://claude.com/claude-code) skill that runs David Allen's *Getting Things Done* on your **actual work**. Where most "GTD tools" make you do the method, this one *operates* it: you paste a brain-dump, an inbox, or a vague task, and it hands back clarified outcomes, physical next actions, and organized lists you can drop straight into your task manager.

> **An operator, not a book report.** Its default move is to *do the GTD work on your content* — not explain GTD. Paste a pile of "stuff" and it processes every item through the workflow diagram for you.

## What it does

Its flagship move — **Capture & Clarify**: give it a messy list / inbox / "everything on my mind," and it returns drop-in output:

- **Next Actions** grouped by **`@context`** (`@calls`, `@computer`, `@errands`, `@agendas`…)
- **Projects** — each with a defined desired outcome *and* a concrete next action
- **Waiting For** (dated), **Calendar** items (hard-landscape only), **Someday/Maybe**, **Reference**, **Trash**
- a **⚡ "<2 min — just do these now"** shortlist

Plus seven more auto-detected modes: extract the **next action** from a stuck task, plan a project with the **Natural Planning Model**, run the **Weekly Review**, choose **what to do now** (four-criteria model), review your life at the **six horizons of focus**, set up or repair your system, or **audit** it for the weakest link.

The hard discipline it enforces everywhere: **a next action must be a physical, visible, single action** (a verb + specifics — "Email Sandra re press kits", never "set meeting" or "budget").

## Coverage — all 13 chapters, 9 reference docs

| When you need… | It loads |
|---|---|
| Why it works / overwhelm / "mind like water" | `references/00-foundations.md` |
| The five-stage engine + the full workflow decision tree | `references/01-the-engine.md` |
| Brain-dump / mind-sweep / tools / filing / getting started | `references/02-capture-and-setup.md` |
| **Processing a dump → next actions, and the lists/buckets** | `references/03-clarify-and-organize.md` |
| A fuzzy or stuck project / planning anything | `references/04-natural-planning.md` |
| The Weekly Review / a stale, untrusted system | `references/05-review.md` |
| "What do I do now?" / priorities / the six horizons | `references/06-engage-and-choose.md` |
| Procrastination / motivation / building the habit / team culture | `references/07-power-principles.md` |
| "Audit my system / why does it keep falling apart?" | `references/diagnostic.md` |

## Install

The repository **is** the skill, so clone it straight into your Claude Code skills directory:

```bash
git clone https://github.com/zrwang/gtd.git ~/.claude/skills/gtd
```

Restart Claude Code (or start a new session) and the `gtd` skill is available.

## Use

Just dump your stuff or ask:

```
/gtd here's everything on my mind: <paste your pile>
/gtd what's the next action on <stuck project>?
/gtd run my weekly review
/gtd what should I do now? I have 20 minutes and low energy
/gtd audit my system
```

## How it works

`SKILL.md` is the always-loaded brain: the core model, the workflow diagram, eight modes, a situation→reference routing table, and the disciplines (physical next actions, the 2-minute rule, calendar = hard landscape, keep the buckets separate, capture-everything-judge-nothing). The `references/` docs hold the detailed mechanics and load **on demand**.

It was built by extracting the entire book in a structured pass, so the reference docs preserve Allen's exact models, the workflow diagram, the lists, and quotes cited by chapter. It also maps Allen's 2001/2007 paper-era mechanics (label maker, 43 physical folders) to digital tools, and notes the 2007 stage names (Collect/Process/Organize/Review/Do) alongside the modern ones (Capture/Clarify/Organize/Reflect/Engage).

## Attribution & fair use

This skill is an independent, transformative tool based on **_Getting Things Done: The Art of Stress-Free Productivity_ by David Allen** (Penguin, 2001/2007). It contains short verbatim excerpts quoted for commentary and education, attributed by chapter — believed to be fair use. It does **not** include the book's text and is **not** affiliated with, authorized, or endorsed by David Allen or the publisher. If the method helps you, **read the book** — and consider the official GTD® resources.

## License

The skill's original text (routing, model distillations, structure) is released under the [MIT License](./LICENSE). Quoted excerpts from *Getting Things Done* remain © David Allen and are used under fair use; the MIT grant does not extend to them. "Getting Things Done" and "GTD" are trademarks of the David Allen Company; this project is unofficial and uses them only descriptively.
