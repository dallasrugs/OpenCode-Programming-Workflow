---
name: code-quality
description: Produce simple, maintainable, well-structured software using pragmatic Clean Code principles, clear domain boundaries, and restrained refactoring.
---

# Code Quality

Adapted from Uncle Bob's UB Mode and pragmatic
software engineering practices.

## Purpose

Produce understandable, reliable code that follows
the existing architecture and approved requirements.

Prefer clarity over cleverness.

Avoid unnecessary abstractions and speculative design.

## 1. Make it work, then make it right

First:
- Understand the required behavior.
- Identify the relevant existing implementation.
- Implement the smallest coherent solution.
- Verify the behavior.

Then:
- Inspect the resulting design.
- Remove unnecessary complexity.
- Improve clarity where justified.
- Preserve passing behavior.

Do not create excessive development iterations.

## 2. Follow existing architecture

Before introducing new structures:

- Inspect repository conventions.
- Reuse established patterns.
- Respect existing module boundaries.
- Preserve public interfaces where required.
- Keep domain behavior in the appropriate layer.

Do not introduce new frameworks, infrastructure,
or architectural layers without justification.

Material deviations require Maintainer escalation.

## 3. Clear responsibilities

Functions and modules should have understandable
responsibilities.

Prefer:
- Cohesive behavior
- Explicit dependencies
- Clear control flow
- Meaningful names
- Predictable side effects
- Well-defined interfaces

Avoid:
- Unrelated responsibilities in one component
- Hidden global state
- Excessive parameter passing
- Deep unnecessary nesting
- Clever but unreadable expressions

Do not split functions merely to make them shorter.

## 4. Domain clarity

Use consistent terminology from the approved
domain model and existing repository.

Distinguish concepts that have different business
meanings even when their data looks similar.

Keep important domain invariants explicit.

Do not invent generalized domain abstractions
without a real requirement.

## 5. Minimize duplication intelligently

Remove duplication when multiple implementations
represent the same underlying business rule.

Do not abstract coincidentally similar code
that may evolve independently.

Prefer straightforward code over premature DRY.

Avoid premature generalization.

## 6. Error handling

Handle failures deliberately.

- Preserve meaningful error information.
- Do not swallow exceptions silently.
- Use consistent error contracts.
- Validate inputs at appropriate boundaries.
- Consider partial failures and retries.
- Preserve data consistency.
- Avoid unsafe fallback behavior.

Do not hide defects behind broad exception handlers.

## 7. State and concurrency

When applicable:

- Identify state ownership.
- Preserve transaction boundaries.
- Consider idempotency.
- Respect locking and concurrency rules.
- Avoid inconsistent intermediate states.
- Preserve retry safety.
- Make state transitions understandable.

Prefer existing infrastructure and safeguards.

## 8. Compatibility

Before modifying shared contracts, consider:

- Existing callers
- API consumers
- Database compatibility
- Background workers
- External integrations
- Serialization formats
- Existing tests

Do not introduce breaking changes unintentionally.

## 9. Refactoring discipline

Refactor when it provides measurable value:

- Reduces actual complexity
- Removes harmful duplication
- Improves readability
- Corrects misplaced responsibilities
- Makes required behavior easier to test
- Reduces known maintenance risks

Do not refactor unrelated modules.

Do not chase arbitrary code-quality metrics.

Avoid broad rewrites when targeted corrections suffice.

## 10. Testing and verification

Use the test-driven-development skill when
implementing behavior.

Use systematic-debugging when investigating failures.

Favor meaningful behavioral verification.

Do not add superficial tests merely to increase
coverage numbers.

Run appropriate tests after changes.

Never claim verification that was not performed.

## 11. Efficient implementation

For each approved milestone:

1. Inspect the relevant code and conventions.
2. Establish the required behavior.
3. Choose the simplest viable design.
4. Implement a coherent slice.
5. Verify the slice.
6. Perform one focused quality review.
7. Correct meaningful defects.
8. Report results and remaining risks.

Avoid repeated cosmetic passes.

Avoid introducing abstractions for hypothetical
future requirements.

Do not request additional agent reviews unless
there is a substantive unresolved issue.

## 12. Completion checklist

Before reporting completion, check:

- Required behavior is implemented.
- Approved architecture is respected.
- Domain terminology is consistent.
- Error handling is appropriate.
- No unnecessary complexity was introduced.
- Relevant compatibility is preserved.
- Required verification has been performed.
- Remaining limitations are disclosed.

## Restrictions

Follow the approved implementation plan.
Do not silently expand scope.
Do not perform unrelated refactoring.
Do not introduce dependencies without justification.
Do not fabricate quality or test results.
Do not automatically commit, push, merge, or deploy.


## Governed execution

The governance controller owns state and authorization. Maintainer plan approval and BDFL task/spec authorization precede coding. The Reviewer prepares the rubric and independently reviews real deterministic test evidence. Only the Coder edits exact approved source paths; the Maintainer decides integration and the Team Lead reports verified outcomes. Skills cannot grant tools, authorize scope expansion, or replace independent review.
