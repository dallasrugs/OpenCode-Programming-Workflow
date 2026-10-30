---
name: milestone-coordination
description: Coordinate approved implementation milestones through the Coder, track dependencies, handle blockers, and minimize Maintainer model requests.
---

# Milestone Coordination

Inspired by wildwasser's subagent-driven-development
and Matt Pocock's implementation workflows.

## Purpose

Coordinate implementation without directly writing code.

The controller manages execution; the Maintainer approves architecture.
The Coder executes them.
The Team Lead manages requirements and reports verified outcomes.

## 1. Establish execution state

Before delegating, identify:

- Approved plan and acceptance criteria
- Current milestone
- Task IDs and dependencies
- Previously completed work
- Remaining work
- Known blockers
- Relevant implementation evidence

Use the existing roadmap.

Do not recreate completed planning work.

## 2. Select ready tasks

A task is ready when:

- Its dependencies are verified
- Its requirements are sufficiently clear
- Its implementation is authorized
- Necessary context is available

Group closely related ready tasks into coherent milestones.

Avoid unnecessary fragmentation.

## 3. Delegate to the Coder

For each milestone, provide:

- Approved plan reference
- Milestone ID and objectives
- Task IDs and dependencies
- Relevant architecture and repository context
- Implementation boundaries
- Acceptance criteria
- Required verification
- Expected completion report

Give the Coder enough context to work independently.

Do not delegate tiny individual coding actions.

## 4. Allow independent execution

The Coder may:

- Inspect relevant repository files
- Implement authorized changes
- Write and update tests
- Debug failures
- Refactor within approved boundaries
- Return implementation evidence to the controller
- Examine deterministic runner results

The Coder should complete its assigned milestone
without repeatedly consulting the Maintainer.

Do not poll for progress.

Wait for the delegated operation to return.

## 5. Evaluate milestone results

When the Coder returns, inspect:

- Task IDs completed
- Files changed
- Actual test results
- Acceptance criteria satisfied
- Remaining failures
- Deviations from the plan
- New dependencies or blockers

Distinguish reported evidence from independently
verified evidence.

Do not invent verification results.

## 6. Handle failures

For ordinary implementation failures:

- Return actionable feedback to the Coder.
- Allow correction within approved scope.
- Avoid escalating routine debugging.

For significant blockers:

- Identify the affected milestone.
- Capture the cause and attempted solutions.
- Explain the proposed alternative.
- Return control to the Team Lead when a new
  user decision or approval is required.

Never silently change approved architecture.

## 7. Maintain task state

Use these statuses:

PENDING:
Dependencies have not been satisfied.

READY:
Dependencies are verified.

IN_PROGRESS:
Coder is implementing the task.

BLOCKED:
An unresolved dependency or decision prevents progress.

FAILED:
Implementation or verification failed.

VERIFIED:
Acceptance criteria have supporting execution evidence.

The controller persists task state outside agent access.

The Maintainer must not directly edit repository files.

Never mark incomplete work as VERIFIED.

## 8. Minimize redundant model calls

Independent Reviewer requests may be limited.

- Plan milestones once.
- Delegate coherent batches.
- Avoid repeated context reconstruction.
- Avoid polling the Coder.
- Avoid unnecessary review cycles.
- Do not duplicate implementation analysis.
- Escalate exceptions rather than routine decisions.
- Produce concise, structured reports.

Do not launch parallel Coder sessions that could
modify overlapping repository files.

## 9. Preserve execution continuity

At milestone boundaries, preserve:

- Current task states
- Completed verification
- Outstanding blockers
- Important decisions
- Next eligible tasks

Use the existing approved roadmap as the source of truth.

Do not rely solely on conversation history.

## 10. Completion

When all milestones are finished:

1. Collect the final task ledger.
2. Review reported verification evidence.
3. Identify incomplete acceptance criteria.
4. Document deviations and remaining risks.
5. Produce a completion report.
6. Return the report to the Team Lead.

The Reviewer performs independent review; the Maintainer decides integration.

Do not automatically commit, push, merge, or deploy.

## Restrictions

Never implement application code.
Never expand scope independently.
Never approve material architectural deviations.
Never claim tests passed without evidence.
Never bypass required user approvals.
The controller invokes roles; agents cannot delegate or grant authorization.


## Governed execution

The governance controller owns state and authorization. Maintainer plan approval and BDFL task/spec authorization precede coding. The Reviewer prepares the rubric and independently reviews real deterministic test evidence. Only the Coder edits exact approved source paths; the Maintainer decides integration and the Team Lead reports verified outcomes. Skills cannot grant tools, authorize scope expansion, or replace independent review.
