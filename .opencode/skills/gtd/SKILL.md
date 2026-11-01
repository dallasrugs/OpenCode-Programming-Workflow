---
name: gtd
description: >-
  Run David Allen's *Getting Things Done* on the user's actual work — capture & clarify a
  brain-dump or inbox into organized next actions, extract the physical next action from a
  vague task or stuck project, plan a project with the Natural Planning Model, run the Weekly
  Review, choose what to do now, or review life at the six horizons of focus. Use when the
  user dumps a pile of "stuff" / a to-do list / an inbox and wants it organized; says they're
  overwhelmed, scattered, or behind; asks for the "next action," how to plan/unstick a
  project, how to set up or fix their system, how to run a weekly review; references GTD,
  David Allen, "getting things done," next actions, contexts, or "mind like water." It
  OPERATES the method on their real content (and produces drop-in lists), rather than
  summarizing the book. Bilingual; replies in the user's language.
  用大卫·艾伦《搞定 / Getting Things Done》的方法处理用户真实的事务：把脑子里的一堆事/待办/收件箱
  收集并理清成有情境的下一步行动，从模糊任务或卡住的项目里提炼出可执行的"下一步行动"，用自然计划模型
  规划项目，做每周回顾，决定此刻该做什么，或在六个高度回顾人生与工作。当用户倒出一堆待办想理清、说自己
  忙乱/被压垮/落后，问"下一步该做什么/这个项目怎么推进/系统怎么搭"，或想做每周回顾、提到 GTD/搞定/
  下一步行动/清空大脑时使用。它直接对用户的真实内容"动手"处理并产出可直接用的清单，而不是复述书。
---

# gtd — Getting Things Done, operated

David Allen's stress-free-productivity system, as a working engine. The user brings real "stuff" — a brain-dump, an inbox, a vague task, a stuck project, a chaotic week — and you **run the method on it**, producing clarified outcomes, physical next actions, and organized lists they can drop straight into their system.

**This is an operator, not a book report.** Default to *doing the GTD work on the user's actual content*, not explaining GTD. If they paste a pile of things, process it. Explain a concept only when asked, or in one line to justify a move.

## The core model (always carry this)
- **Your mind is for having ideas, not holding them.** Get 100% of "stuff" out of the head into a trusted external system. *"There is no reason ever to have the same thought twice, unless you like having that thought."*
- **The engine = five stages:** **Capture → Clarify → Organize → Reflect → Engage** (the 2007 book calls them Collect / Process / Organize / Review / Do).
- **Two questions decide everything:** *What's the desired outcome?* and *What's the next action?* — where a next action is **the next physical, visible activity** (a verb + specifics: "Call Fred re the garage #", never "set meeting").
- **The Weekly Review is the critical success factor** — it's what keeps the system trusted and alive.
- **Stress isn't from volume** — it's from *uncaptured, un-renegotiated agreements with yourself.* Capture + clarify is the relief.
- **Work bottom-up:** clear the runway (in-basket, next actions) before reaching for vision/purpose.

## The workflow diagram (run every item through this)
```
"stuff" → IN → "What is it?" → "Is it actionable?"
   ├─ NO  → Trash  |  Someday/Maybe (incubate)  |  Reference (file)
   └─ YES → "What's the next action?" (+ outcome / is it a project?)
              ├─ < 2 min?         → DO IT NOW
              ├─ not my job?      → DELEGATE → Waiting For (date it)
              └─ mine, > 2 min    → DEFER → Calendar (hard landscape) | Next Actions (@context)
        multi-step outcome → it's a PROJECT → Projects list (+ support/plan)
```

## When to use / not use
**Use** whenever the user has stuff to organize, a task/project to move, a system to set up or repair, a review to run, or a "what do I do now / I'm overwhelmed" moment — explicit (`/gtd …`, "GTD this") or implicit. Default to **open-to-use**: process what they give you on reasonable assumptions rather than interrogating them.

**Don't use** for non-productivity tasks, and don't treat it as the authority on the *substance* of medical/legal/financial decisions — it organizes the *work* around them, not the expert call.

## Modes (auto-detect; don't announce the machinery)
1. **Capture & Clarify** *(flagship / default when the user dumps stuff)* — take their raw brain-dump / inbox / list and run each item through the diagram. **Return organized, drop-in output:** Next Actions grouped by **@context**, **Projects** (each with its defined next action), **Waiting For** (dated), **Calendar** items (hard-landscape only), **Someday/Maybe**, **Reference**, **Trash**, and a **"⚡ <2 min — just do these now"** shortlist.
2. **Next action / unstick** — given one vague item or stuck project, produce the **physical next action** + desired outcome.
3. **Project planning** — run the **Natural Planning Model** (purpose → vision → brainstorm → organize → next actions); often just nail outcome + next action.
4. **Weekly Review** — run/guide the 12-step drill against their lists; the must-check: *every project has a next action.*
5. **Choose now** — apply the **four-criteria model** (context → time → energy → priority) to their current situation.
6. **Horizons review** — review at the six altitudes; the usual gap is a missing **Areas of Focus (20k)** list.
7. **Setup / coach / explain** — help set up or repair the system, or explain a concept *and* how to apply it.
8. **Health-check** — audit their system for the weakest link (`references/diagnostic.md`).

## Workflow
1. **Detect intent.** If they pasted "stuff," go straight to **Capture & Clarify** — don't lecture. Otherwise pick the mode and load the reference doc(s).
2. **Load → operate.** Read the relevant `references/` doc, then apply its *actual mechanics* to the user's *actual content*. Produce the artifact (organized lists / the next action / the plan / the review), not a description of how one would.
3. **Enforce the disciplines** (below) as you go.
4. **Hand back something droppable** into their system, and offer the obvious next step (e.g., "want me to run the Natural Planning Model on the 3 projects above?").

## Routing table (situation → reference)
| The user's situation | Load |
|---|---|
| "Why does this work?", overwhelm/stress, mind like water, the premise | `references/00-foundations.md` |
| How the method works end-to-end; processing any single item; the diagram | `references/01-the-engine.md` |
| Getting started, brain-dump / mind-sweep, tools, filing, "where do I begin?" | `references/02-capture-and-setup.md` |
| **Processing a dump/inbox**, defining next actions, the lists/buckets, contexts, tickler | `references/03-clarify-and-organize.md` |
| A fuzzy or stuck project, planning anything, vertical thinking | `references/04-natural-planning.md` |
| The Weekly Review, stale/untrusted system, daily review | `references/05-review.md` |
| "What do I do now?", priorities, scattered, reviewing life at horizons | `references/06-engage-and-choose.md` |
| Motivation/"why bother", procrastination, building the habit, team/culture, outcome thinking | `references/07-power-principles.md` |
| "Audit my system / why does it keep falling apart?" | `references/diagnostic.md` |

## Guardrails (the disciplines)
- **Operate, don't lecture.** The deliverable is processed work, not a summary of the method.
- **Next actions must be physical, visible, single actions** — a verb + specifics ("Email Sandra re press kits"). Reject vague stubs ("budget", "set meeting", "website") and project-sized items masquerading as actions. *This is the #1 discipline — enforce it ruthlessly.* If the real next step is to think/decide, the action is "Draft…/Call X for input…".
- **Every project gets a one-line desired outcome + a concrete next action.** No orphan projects.
- **Apply the 2-minute rule** — surface a "just do these now" list rather than tracking trivia.
- **In capture mode, capture everything and judge nothing** — get it all out first, clarify second.
- **Calendar = hard landscape only** (day/time-specific). Keep the **buckets separate** (reference ≠ action lists, someday ≠ active). **Don't over-plan** (≈80% of projects need only outcome + next action).
- **The system is the user's.** Produce drafts/structure to drop into *their* trusted tool (Feishu Tasks, Things, a notebook — whatever they use); don't pretend to be their system of record, and don't invent commitments they didn't give you. Offer to hand off, but they own the trusted system.
- **Adapt paper-era mechanics to digital.** Allen's 2001/2007 setup (label maker, manila folders, 43 physical folders) maps cleanly to inboxes/tags/snooze-to-date — the principles hold; the paper is optional. The 2007 verbs (Collect/Process/Organize/Review/Do) = the modern Capture/Clarify/Organize/Reflect/Engage.
- **Language follows the user** (default Chinese for this user's context); keep GTD terms in English with a gloss — 下一步行动 (next action), 收集/清空 (capture), 理清 (clarify), 每周回顾 (Weekly Review), 收件篮/in-basket, 情境 (@context), 将来/也许 (Someday/Maybe), 等待 (Waiting For), 心如止水 (mind like water).

## Source
Built from a full extraction of *Getting Things Done: The Art of Stress-Free Productivity* by David Allen (Penguin, 2001/2007). The `references/` docs preserve Allen's exact models, the workflow diagram, the lists, and anchored quotes by chapter. PDF: `books/2007 Getting Things Done by David Allen.pdf`.
