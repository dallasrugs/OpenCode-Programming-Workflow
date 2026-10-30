---
name: task-decomposition
description: Convert an approved implementation plan into dependency-aware, independently verifiable coding milestones for Maintainer coordination.
---

# Task Decomposition

Adapted from Matt Pocock's to-tickets.

## Purpose

Transform an explicitly approved technical specification
into an executable roadmap.

The controller coordinates execution; the Maintainer constrains the architecture.
The Coder implements.
The Team Lead owns requirements; the Maintainer decides integration after independent review.

## 1. Establish authority

Before decomposing work, confirm that the handoff contains:

- BDFL task/specification authorization and Maintainer approval
- Approved specification
- Scope and exclusions
- Acceptance criteria
- Architectural decisions
- Relevant repository references

If approval is missing, return control to the Team Lead.

Never treat an unapproved draft as authorization.

## 2. Identify implementation dependencies

Extract:

- Required functionality
- Affected components
- External dependencies
- Schema and API changes
- Compatibility constraints
- Testing requirements
- Migration or rollout considerations

Use facts supplied by the Team Lead.

Do not invent repository structure or implementation details.

## 3. Create vertical slices

Prefer tracer-bullet tasks.

Each task should deliver a narrow but complete,
independently verifiable capability.

Where appropriate, include:

- Data model changes
- Backend behavior
- API integration
- Frontend behavior
- Tests and verification

Avoid splitting work into artificial horizontal layers
when an end-to-end slice is feasible.

## 4. Handle broad refactors

For changes that cannot remain independently functional,
consider an expand-migrate-contract sequence:

1. Introduce compatible replacement behavior.
2. Migrate existing consumers incrementally.
3. Verify compatibility and correctness.
4. Remove obsolete behavior after verification.

Do not force vertical slicing onto mechanical refactors
when doing so would introduce unnecessary complexity.

## 5. Define each task

Use this structure:

Task ID:
Stable identifier such as T001.

Title:
Concise description.

Objective:
Observable functionality to deliver.

Dependencies:
Task IDs that must complete first.

Scope:
Relevant components and constraints.

Acceptance Criteria:
Specific, independently testable outcomes.

Verification:
Tests, checks, or observable evidence required.

Status:
PENDING | READY | IN_PROGRESS |
BLOCKED | FAILED | VERIFIED

A task is READY only when its dependencies are VERIFIED.

## 6. Build the dependency graph

Identify which tasks can begin immediately.

Do not begin tasks with unresolved dependencies.

Prefer a small number of coherent milestones.

A milestone may contain multiple related tasks.

Avoid unnecessary task fragmentation.

## 7. Define milestone handoffs

For each Coder delegation provide:

- Approved plan reference
- Milestone and task IDs
- Relevant implementation context
- Dependencies and constraints
- Acceptance criteria
- Required tests and checks
- Reporting requirements

Provide sufficient context for independent execution.

Do not repeatedly delegate trivial subtasks.

## 8. Maintain execution state

The Maintainer must maintain a logical task ledger.

The controller persists execution state outside agent access; the Maintainer returns structured evidence.

Do not confuse reported progress with verified completion.

Every completed task requires supporting evidence.

Preserve task IDs, dependencies, and acceptance criteria
throughout execution.

## 9. Minimize redundant model calls

The independent Reviewer may have limited provider capacity.

- Decompose the approved plan once.
- Batch related tasks into milestones.
- Avoid progress polling.
- Do not independently repeat Coder investigations.
- Review milestone summaries and evidence.
- Escalate only meaningful blockers or deviations.
- Prefer one coherent delegation per milestone.

Do not launch unnecessary agents.

## 10. Handle deviations

If the implementation requires a material change to:

- Approved functionality
- Architecture
- Data contracts
- Security behavior
- Scope
- Acceptance criteria

Stop affected work.

Return the proposed deviation and reasoning to the Team Lead.

Do not independently approve scope changes.

## 11. Completion conditions

A task is VERIFIED only when:

- Its acceptance criteria are satisfied.
- Required tests or checks have actually run.
- Relevant evidence is available.
- No unresolved blocking failures remain.

If verification is unavailable, report the limitation.

Never fabricate execution results.

## Product ownership and task quality

Apply INVEST principles pragmatically:

Independent:
Minimize unnecessary dependencies between tasks.

Negotiable:
Leave implementation flexibility within approved
architectural constraints.

Valuable:
Each task should deliver a meaningful capability or
enable a necessary part of the approved solution.

Estimable:
Scope must be sufficiently understood for execution.

Small:
Prefer coherent milestones the Coder can implement
and verify without excessive coordination.

Testable:
Every task must have observable acceptance criteria.

Preserve the Team Lead's Given-When-Then outcomes when
converting requirements into implementation tasks.

Do not invent additional acceptance requirements.

Do not require Scrum ceremonies, story points,
velocity estimates, or artificial task-size limits.

Prioritize high-risk prerequisites and useful vertical
slices while respecting the approved dependency graph.

## Deliverable

Produce an execution roadmap containing:

1. Approved plan reference
2. Implementation milestones
3. Task IDs and dependencies
4. Acceptance criteria
5. Required verification
6. Risks and potential blockers
7. Initial ready-task frontier

Do not implement code directly.
Do not commit, push, merge, or deploy.
Do not expand scope without a newly approved and BDFL-authorized specification.


## Governed execution

The governance controller owns state and authorization. Maintainer plan approval and BDFL task/spec authorization precede coding. The Reviewer prepares the rubric and independently reviews real deterministic test evidence. Only the Coder edits exact approved source paths; the Maintainer decides integration and the Team Lead reports verified outcomes. Skills cannot grant tools, authorize scope expansion, or replace independent review.
