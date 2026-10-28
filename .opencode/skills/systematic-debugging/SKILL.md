---
name: systematic-debugging
description: Investigate software failures through reproducible evidence, root-cause analysis, targeted corrections, and efficient regression verification.
---

# Systematic Debugging

Adapted from wildwasser's systematic-debugging
and Matt Pocock's diagnosing-bugs approaches.

## Purpose

Find and correct the underlying cause of a failure.

Do not rely on random changes, speculative fixes,
or repeated test execution without new information.

## 1. Establish the problem

Before changing code, determine:

- Expected behavior
- Actual behavior
- Relevant error messages
- Reproduction conditions
- Affected components
- Recent relevant changes
- Available logs and test results

Separate observations from assumptions.

If the problem cannot be reproduced, inspect existing
evidence and identify what is still unknown.

## 2. Investigate the execution path

Trace the failing behavior through relevant boundaries.

Examples:

- User interface to API
- API to application logic
- Application logic to database
- Queue producer to worker
- External service request to response

Inspect actual implementation and repository conventions.

Use logs, stack traces, existing tests, and source code.

Do not assume the reported failing component
is necessarily the root cause.

## 3. Form a focused hypothesis

Identify the most plausible explanation supported
by the available evidence.

State:

- Suspected root cause
- Evidence supporting it
- Evidence that could disprove it
- Smallest useful verification

Prefer targeted investigation over broad exploration.

Do not generate a large list of speculative fixes.

## 4. Confirm the cause

When feasible:

- Reproduce the failure.
- Establish a focused failing test.
- Inspect the relevant state or data.
- Compare expected and actual execution.
- Confirm the suspected failure mechanism.

If the cause remains uncertain, report that uncertainty.

Do not present a hypothesis as a confirmed fact.

## 5. Implement the correction

Once the cause is sufficiently established:

- Apply the smallest correct fix.
- Preserve established architecture.
- Respect existing public contracts.
- Address the cause rather than masking symptoms.
- Avoid unrelated refactoring.
- Stay within the approved milestone.

If the fix requires a material architectural change,
return the decision to the Supervisor.

## 6. Verify efficiently

After the correction:

1. Run the focused reproduction or regression test.
2. Confirm the original failure is resolved.
3. Check relevant neighboring behavior.
4. Run broader tests when risk or milestone policy
   requires them.

Avoid repeatedly running identical successful checks.

If a fix fails, analyze the new evidence before
attempting another change.

Never weaken assertions or silence errors
merely to obtain a passing test.

## 7. Handle environmental failures

Distinguish code defects from failures caused by:

- Missing dependencies
- Configuration differences
- Database or network availability
- Resource exhaustion
- Permissions
- External services
- Test infrastructure

Do not modify application code to compensate for
an unrelated environmental problem.

Report unavailable verification explicitly.

## 8. Escalation

Escalate when:

- Evidence contradicts the current diagnosis.
- A required decision changes approved scope.
- An unexpected data migration is necessary.
- The fix affects security or authorization policy.
- Multiple focused attempts reveal a deeper issue.
- Required external access is unavailable.

Provide the Supervisor with the evidence gathered,
not merely a statement that debugging failed.

## 9. Completion report

Report:

### Symptom
What failed.

### Root Cause
Confirmed cause, or remaining uncertainty.

### Correction
What changed and why.

### Evidence
Reproduction and verification performed.

### Regression Results
Actual tests and outcomes.

### Remaining Risks
Unresolved issues or missing checks.

## Efficiency rules

- Investigate before editing.
- Prefer one evidence-supported correction.
- Avoid speculative multi-fix patches.
- Avoid unnecessary agent consultations.
- Do not poll or repeatedly rerun identical checks.
- Batch related verification where appropriate.
- Never sacrifice correctness for fewer iterations.

## Restrictions

Follow the approved implementation scope.
Never fabricate reproduction or test evidence.
Never hide unresolved failures.
Never modify production data during debugging
without explicit authorization.
Never automatically commit, push, merge, or deploy.
