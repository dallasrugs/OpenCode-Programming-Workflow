---
name: verification
description: Verify implemented software against approved acceptance criteria using risk-based tests, build checks, regression evidence, and concise completion reports.
---

# Verification

Adapted from verification-before-completion and
pragmatic evidence-based engineering practices.

## Purpose

Establish trustworthy evidence that implemented
behavior satisfies the approved requirements.

Avoid redundant execution, unnecessary test cycles,
and unsupported completion claims.

## 1. Establish verification scope

Read the approved milestone and identify:

- Acceptance criteria
- Changed behavior
- Affected components
- Relevant existing tests
- Integration boundaries
- Required static and build checks
- Important regression risks

Do not invent requirements or success criteria.

## 2. Use risk-based verification

High-risk changes:

- Authentication and authorization
- Financial or commercial calculations
- Data migrations
- Concurrency and locking
- Transactions and data integrity
- External synchronization
- Destructive operations

Require focused tests and appropriate integration
or regression evidence.

Normal-risk changes:

- Features
- UI workflows
- API behavior
- Ordinary bug fixes

Use focused behavioral tests and relevant regression
checks at milestone completion.

Low-risk changes:

- Documentation
- Formatting
- Mechanical changes without behavior changes

Use appropriate structural or static checks.

Never classify behavioral changes as low risk
merely to avoid testing.

## 3. Run checks efficiently

During implementation:

- Execute targeted tests when behavior changes.
- Investigate failures before rerunning.
- Avoid repeated identical successful test commands.
- Avoid full-suite runs after every small edit.

At milestone completion:

1. Run affected focused tests.
2. Run relevant integration tests where feasible.
3. Run required linting, typing, or static checks.
4. Run broader regression tests when warranted.
5. Confirm acceptance criteria using actual evidence.

Batch compatible checks where practical.

Do not sacrifice correctness to minimize iterations.

## 4. Inspect results accurately

For every check distinguish:

PASS:
Executed and completed successfully.

FAIL:
Executed and produced a failure.

SKIP:
Executed but intentionally skipped.

NOT_RUN:
Not executed.

BLOCKED:
Unable to execute due to an external constraint.

Do not report NOT_RUN or BLOCKED checks as PASS.

A previously passing result may need revalidation
after subsequent changes affecting that behavior.

## 5. Environmental limitations

When verification is blocked by:

- Missing dependencies
- Unavailable databases
- Missing credentials
- External service outages
- Inaccessible test infrastructure
- Permission restrictions

Report the exact limitation.

Do not silently replace missing integration tests
with weaker checks and call verification complete.

Do not modify production services or data solely
to satisfy verification requirements.

## 6. Acceptance criteria reconciliation

For each acceptance criterion record:

- Criterion or task ID
- Evidence supporting the outcome
- Current verification status
- Remaining uncertainty, if any

Use these statuses:

VERIFIED
PARTIAL
FAILED
UNVERIFIED
NOT_APPLICABLE

Do not claim VERIFIED without relevant evidence.

## 7. Final evidence report

Return to the Maintainer:

### Milestone
Approved milestone and task IDs.

### Changes
Files and components changed.

### Implementation
Concise description of delivered behavior.

### Tests
Actual commands, outcomes, and relevant counts.

### Static and Build Checks
Executed checks and outcomes.

### Acceptance Criteria
Status of each required criterion.

### Remaining Issues
Known defects, skipped checks, and limitations.

### Deviations
Any differences from the approved plan.

### Recommendation
READY_FOR_AUDIT
NEEDS_CORRECTION
BLOCKED

The Maintainer performs the completion audit.
The Maintainer decides integration; the Team Lead reports the verified outcome.

## Efficiency rules

- Verify coherent milestones rather than every edit.
- Use focused tests during development.
- Avoid redundant full-suite execution.
- Reuse valid evidence when changes cannot affect it.
- Investigate failures before repeating checks.
- Keep completion reports concise and factual.
- Never fabricate verification evidence.

## Restrictions

Never claim tests passed without execution.
Never suppress test failures to report success.
Never change approved acceptance criteria.
Never modify production data without authorization.
Never automatically commit, push, merge, or deploy.


## Governed execution

The governance controller owns state and authorization. Maintainer plan approval and BDFL task/spec authorization precede coding. The Reviewer prepares the rubric and independently reviews real deterministic test evidence. Only the Coder edits exact approved source paths; the Maintainer decides integration and the Team Lead reports verified outcomes. Skills cannot grant tools, authorize scope expansion, or replace independent review.
