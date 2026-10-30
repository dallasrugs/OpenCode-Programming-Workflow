---
name: test-driven-development
description: Implement features and bug fixes using behavioral tests, red-green development cycles, and independently verifiable results.
---

# Test-Driven Development

Adapted from Matt Pocock's TDD skill.

## Purpose

Implement approved requirements through small,
testable increments.

Use for feature implementation, bug fixes,
and changes to existing behavior.

## 1. Understand the testing boundaries

Before writing tests:

- Read the approved specification.
- Identify the public interfaces involved.
- Inspect existing tests and conventions.
- Identify appropriate testing seams.
- Reuse existing testing infrastructure.

Prefer testing behavior through public interfaces.

Do not invent new testing architecture unnecessarily.

Testing seams should follow the approved plan.
Escalate significant deviations to the Maintainer.

## 2. Write meaningful tests

Good tests:

- Describe observable behavior.
- Verify real requirements.
- Use independently established expectations.
- Survive internal refactoring.
- Exercise relevant failure conditions.
- Clearly communicate what broke.

Avoid:

- Testing private implementation details.
- Excessive mocking of internal collaborators.
- Assertions that reproduce implementation logic.
- Tautological tests.
- Snapshot tests without meaningful assertions.
- Tests that always pass regardless of behavior.

## 3. Efficient red-green development

Use risk-adaptive TDD with coherent behavioral slices.

### Before implementation

- Understand all acceptance criteria for the assigned slice.
- Identify existing tests and relevant public interfaces.
- Group closely related assertions into focused tests.
- Avoid writing separate tests for every trivial code change.

### RED

1. Write the focused test or tests for the behavior.
2. Run them once to confirm the expected failure.
3. Ensure the failure actually represents missing behavior.

### GREEN

4. Implement the complete coherent behavior.
5. Run the focused tests.
6. Correct any failures before declaring the slice complete.

### REFACTOR

7. Refactor only when it materially improves the design.
8. Rerun affected tests after refactoring.

### Efficiency rules

- Do not create microscopic red-green loops.
- Prefer one cohesive implementation pass per behavior.
- Avoid repeating identical successful test commands.
- Do not rerun the entire suite after every edit.
- Run focused tests during implementation.
- Run broader regression checks at milestone completion.
- If the same failure recurs, investigate the cause
  rather than blindly repeating changes.
- Never skip necessary verification to save requests.

### Risk adaptation

High risk:
Security, authorization, financial calculations,
concurrency, migrations, and critical business logic.
Use stronger regression and integration coverage.

Normal risk:
Features and ordinary bug fixes.
Use focused behavioral TDD and milestone verification.

Low risk:
Documentation, formatting, or purely mechanical edits.
Use appropriate static or structural verification.
Do not create artificial tests.

These categories guide verification effort, not permission
to leave changed behavior untested.

## 4. Work in vertical slices

Each slice should demonstrate a useful behavior.

Where relevant, verify the full path across:
- Public interface
- Application logic
- Persistence
- External boundaries
- Error handling

Avoid unnecessary test duplication across layers.

## 5. Refactoring

After behavior is verified:

- Improve clarity when justified.
- Remove unnecessary duplication.
- Preserve public contracts.
- Avoid speculative abstractions.
- Rerun affected tests.

Do not expand the approved scope.

## 6. Regression testing

For bug fixes:

1. Reproduce the actual reported problem.
2. Establish a failing verification.
3. Identify the root cause.
4. Apply the minimal correct fix.
5. Confirm the original failure disappears.
6. Run relevant regression tests.

A passing test that never detected the bug
does not prove the bug was fixed.

## 7. Verification

Before reporting completion:

- Run relevant focused tests.
- Run applicable integration tests.
- Execute required static checks.
- Run the broader regression suite when appropriate.
- Inspect failures rather than ignoring them.

Report actual results.

Distinguish:
- Passed
- Failed
- Skipped
- Not executed
- Blocked

Never claim success without execution evidence.

## 8. Exceptions

Test-first development may be impractical for certain
configuration, infrastructure, or exploratory changes.

When that happens:

- Explain why.
- Identify alternative verification.
- Preserve existing behavior where required.
- Report limitations to the Maintainer.

Do not write meaningless tests merely to satisfy TDD.

## Restrictions

- Follow approved scope and architecture.
- Never silently modify requirements.
- Never fabricate test results.
- Never suppress failing tests to claim success.
- Never automatically commit, push, merge, or deploy.


## Governed execution

The governance controller owns state and authorization. Maintainer plan approval and BDFL task/spec authorization precede coding. The Reviewer prepares the rubric and independently reviews real deterministic test evidence. Only the Coder edits exact approved source paths; the Maintainer decides integration and the Team Lead reports verified outcomes. Skills cannot grant tools, authorize scope expansion, or replace independent review.
