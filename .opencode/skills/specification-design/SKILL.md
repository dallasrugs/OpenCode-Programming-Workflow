---
name: specification-design
description: Transform approved requirements and architectural findings into an implementation-ready technical specification with acceptance criteria, dependencies, and verification strategy.
---

# Specification Design

Adapted from Matt Pocock's to-spec and
wildwasser's writing-plans.

## Purpose

Produce an accurate, implementation-ready specification
without prematurely modifying the codebase.

Use after requirements clarification and architecture
investigation are complete.

## 1. Gather established context

Review:
- Confirmed requirements and user decisions
- Existing repository documentation
- Domain terminology and invariants
- Relevant architecture and implementation
- Existing interfaces and test conventions
- Constraints and explicit exclusions

Do not repeat completed requirements interviews.

If a critical decision remains unresolved, return to
requirements-grilling before finalizing the specification.

## 2. Define the problem and solution

Document:

### Problem Statement
Explain the actual problem from the user's perspective.

### Desired Outcome
Describe the intended observable behavior.

### User Stories
Identify relevant actors, capabilities, and benefits.

### Scope
Explicitly distinguish included and excluded behavior.

## 3. Technical design

Define:
- Affected components and their responsibilities
- Interfaces and API contracts
- Data model implications
- State transitions and invariants
- Error handling and recovery
- Security and authorization requirements
- Compatibility and migration considerations
- Dependencies and integration boundaries

Prefer existing repository patterns.

Do not invent file paths, schemas, endpoints, or services.

Reference verified implementation locations when useful.

## 4. Architecture decisions

For significant design choices document:
- Selected approach
- Why it was chosen
- Alternatives considered
- Consequences and tradeoffs
- Risks requiring mitigation

Avoid speculative abstractions.

Prefer the simplest solution satisfying the requirements.

## 5. Testing strategy

Identify meaningful public interfaces and testing seams.

Prefer behavioral tests over implementation-coupled tests.

Define:
- Expected successful behavior
- Relevant failure conditions
- Regression scenarios
- Integration requirements
- Data consistency checks
- Observable acceptance criteria

Reuse existing testing conventions.

Do not claim that tests have run during planning.

## 6. Implementation roadmap

Describe logical implementation milestones.

For each milestone include:
- Objective
- Expected deliverable
- Relevant dependencies
- Acceptance conditions
- Verification approach

Do not over-decompose into individual coding actions.

Detailed task decomposition belongs to the Supervisor.

Prefer independently verifiable vertical slices.

For broad mechanical refactors, consider an
expand-migrate-contract sequence where appropriate.

## 7. Final specification

Present these sections:

1. Problem Statement
2. Desired Outcome
3. Confirmed Requirements
4. Current Architecture
5. Proposed Technical Design
6. Architectural Decisions
7. Implementation Milestones
8. Testing and Verification Strategy
9. Acceptance Criteria
10. Risks and Mitigations
11. Out of Scope
12. Open Questions, if any

Separate verified facts from proposed decisions.

## 8. Approval gate

Present the completed specification to the user.

Do not initiate implementation until the user explicitly
approves the technical plan.

Approval must apply to the specific proposed scope.

Do not infer approval from general positive feedback.

## 9. Supervisor handoff

After explicit approval, provide the Supervisor with:
- Approved specification
- Confirmed architectural decisions
- Constraints and exclusions
- Relevant repository references
- Acceptance criteria
- Milestones and dependencies
- Testing expectations

The Supervisor owns detailed task decomposition and
execution coordination.

The Coder owns implementation and verification.

The Planner retains final review responsibility.

## Product ownership and acceptance design

Adapted from Agile Product Owner practices.

For user-facing capabilities, establish:

- Who benefits from the change
- What capability they require
- Why that capability matters
- Which outcomes are essential versus optional

Use concise user stories where helpful:

As a [persona], I want [capability],
so that [business or user benefit].

Define acceptance criteria using observable behavior:

Given [relevant precondition],
When [action or event],
Then [expected outcome].

Cover relevant success, validation, failure,
authorization, and data consistency scenarios.

Do not invent arbitrary performance thresholds.

Prioritize requirements by business value, user impact,
risk, and implementation dependencies.

Do not require story points, sprint planning, velocity
tracking, or fixed acceptance-criterion counts.

Acceptance criteria must be confirmed before
implementation authorization.

## Restrictions

Never modify application code.
Never silently change approved requirements.
Never deploy, merge, push, or commit.
Never delegate implementation before approval.
Never claim unperformed verification.
