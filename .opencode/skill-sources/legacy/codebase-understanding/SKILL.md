---
name: codebase-understanding
description: Investigate and explain existing codebase architecture, runtime flows, component relationships, and implementation boundaries before planning changes.
---

# Codebase Understanding

Adapted from https://github.com/poteto/how

## Purpose

Understand how the existing system actually works before
proposing modifications.

Use this skill during architecture exploration, feature
planning, refactoring analysis, or subsystem explanations.

## 1. Discover repository context

Inspect relevant documentation before making assumptions.

Look for:
- AGENTS.md and repository instructions
- docs/ architecture and design documentation
- Existing specifications and ADRs
- Domain glossaries and terminology
- Relevant interfaces, schemas, and tests

Documentation provides context, but implementation and tests
are the evidence of current behavior.

When documentation contradicts code, report the discrepancy.

## 2. Assess complexity

For narrow questions involving one module:
- Explore directly.
- Avoid unnecessary subagents.

For cross-cutting questions involving several components:
- Identify independent exploration areas.
- Delegate focused, read-only exploration where useful.
- Avoid overlapping or redundant investigations.
- Synthesize results into one coherent explanation.

Prefer minimal delegation.

## 3. Trace the actual implementation

Follow the relevant path from entry point to outcome.

Identify:
- Entry points and triggers
- Public interfaces and API contracts
- Domain models and data structures
- Service boundaries and dependencies
- State changes and persistence
- External integrations
- Error handling and failure paths
- Tests that establish expected behavior

Read actual implementations rather than inferring behavior
from filenames or symbol names.

## 4. Explain the architecture

Produce the following sections when relevant:

### Overview
What the subsystem does and why it exists.

### Key Concepts
Important models, abstractions, and domain terminology.

### Runtime Flow
What happens from input to output, including interactions
between components.

### Where Things Live
Relevant files and directories with concise explanations.

### Important Constraints
Architectural decisions, compatibility requirements,
invariants, and non-obvious behavior.

### Gotchas
Potential failure points, surprising behavior, and known
limitations supported by actual evidence.

Reference specific files and symbols whenever possible.

## 5. Architectural critique

Only critique the architecture when requested or necessary
to evaluate a proposed change.

First explain the existing implementation.

Then identify:
- Structural weaknesses
- Coupling and complexity
- Missing boundaries
- Data consistency risks
- Performance or security concerns
- Opportunities to reuse existing functionality

Separate verified problems from possible improvements.

Do not recommend redesign merely because a different pattern
exists.

## 6. Planning handoff

Provide the Team Lead with:
- Verified current behavior
- Relevant components and contracts
- Existing patterns to preserve
- Constraints and potential regressions
- Unresolved questions requiring decisions

Do not implement changes during this investigation.

## Principles

- Source code and tests establish actual behavior.
- Never invent repository facts.
- Prefer existing architecture over unnecessary abstractions.
- Distinguish observation, inference, and recommendation.
- Do not access secrets or credentials.
- Do not modify repository files.
- Do not invoke expensive external models unnecessarily.


## Governed execution

The governance controller owns state and authorization. Maintainer plan approval and BDFL task/spec authorization precede coding. The Reviewer prepares the rubric and independently reviews real deterministic test evidence. Only the Coder edits exact approved source paths; the Maintainer decides integration and the Team Lead reports verified outcomes. Skills cannot grant tools, authorize scope expansion, or replace independent review.
