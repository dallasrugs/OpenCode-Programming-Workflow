---
name: completion-audit
description: Audit completed coding milestones against approved requirements, execution evidence, test results, and architectural constraints before final Planner review.
---

# Completion Audit

Adapted from wildwasser's verification-before-completion
and Matt Pocock's code-review.

## Purpose

Determine whether implementation actually satisfies the
approved plan.

Evidence before completion claims.

The Supervisor performs coordination and auditing.
The Coder supplies implementation and test evidence.
The Planner owns final acceptance.

## 1. Establish the baseline

Retrieve from the approved handoff:

- Original specification
- Confirmed requirements
- Acceptance criteria
- Implementation task IDs
- Architectural decisions
- Explicit exclusions
- Required verification

Do not substitute a Coder summary for the original plan.

## 2. Collect implementation evidence

Require the Coder to report:

- Changed files
- Actual implementation details
- Git diff summary
- Tests executed
- Test commands and outcomes
- Static analysis results
- Build results where applicable
- Unresolved failures
- Deviations from the plan

Distinguish directly observed evidence from
unverified agent assertions.

If evidence is missing, request targeted verification.

## 3. Specification compliance review

For every acceptance criterion determine:

VERIFIED:
Evidence demonstrates the expected behavior.

PARTIAL:
Some requirements are satisfied.

FAILED:
Evidence demonstrates incorrect behavior.

UNVERIFIED:
Insufficient evidence exists.

NOT_APPLICABLE:
The criterion does not apply.

Never mark a criterion VERIFIED merely because
the Coder claims that implementation is complete.

## 4. Code quality review

Evaluate reported implementation against:

- Repository coding standards
- Established architectural boundaries
- Domain terminology and invariants
- Backward compatibility
- Error handling
- Security and authorization
- Data consistency
- Unnecessary complexity
- Duplication and maintainability

Separate confirmed violations from possible concerns.

Do not invent findings without supporting evidence.

## 5. Verification gate

Before approving completion, confirm evidence for:

- Relevant tests passing
- Existing functionality preserved
- New behavior tested
- Reported regressions resolved
- Required integration checks completed
- Acceptance criteria satisfied

For missing evidence, delegate targeted checks
to the Coder when permitted.

Do not repeatedly run identical checks without reason.

If verification cannot be performed, report UNVERIFIED.

## 6. Handle deficiencies

For ordinary defects within approved scope:

- Return specific findings to the Coder.
- Request focused corrections.
- Require fresh verification evidence.
- Reassess affected acceptance criteria.

For significant architectural or scope deviations:

- Stop affected work.
- Report the decision required to the Planner.
- Do not authorize unapproved changes.

Avoid unnecessary review loops.

## 7. Final task reconciliation

Check every task ID against the original roadmap.

Report:

- Verified tasks
- Partial tasks
- Failed tasks
- Unverified tasks
- Blocked tasks
- Outstanding dependencies

No task may disappear from the final report.

Do not silently drop failed or deferred work.

## 8. Produce the audit report

Use this structure:

### Approved Plan
Reference the original specification.

### Implementation Summary
Describe delivered functionality.

### Task Reconciliation
Report each task ID and its verified status.

### Verification Evidence
List actual checks and results.

### Specification Compliance
Identify satisfied and missing requirements.

### Code Quality Findings
Record confirmed issues and relevant concerns.

### Deviations
Explain changes from the approved plan.

### Outstanding Risks
List unresolved issues or missing evidence.

### Final Recommendation
One of:

READY_FOR_PLANNER_REVIEW
NEEDS_CORRECTION
BLOCKED
INCOMPLETE

Only recommend READY_FOR_PLANNER_REVIEW when all
required acceptance criteria are verified.

This recommendation is not final user acceptance.

## 9. Return to Planner

Send the final audit report and the reference
to the original approved plan.

The Planner compares the report with the original
requirements and makes the final recommendation.

The Supervisor must not independently declare
the feature accepted by the user.

## Efficiency

- Audit once per completed milestone where useful.
- Perform a comprehensive final audit.
- Avoid repeating successful checks unnecessarily.
- Request narrowly scoped corrections.
- Minimize Nemotron inference requests.
- Keep audit reports concise and evidence-based.

## Restrictions

Never edit application code directly.
Never fabricate test results.
Never treat claims as verification.
Never expand implementation scope.
Never push, merge, deploy, or commit.
Never bypass required user approval.
