---
name: domain-modeling
description: Establish consistent domain terminology, investigate business rules, identify domain boundaries, and propose architectural decision records during software design.
---

# Domain Modeling

Adapted from Matt Pocock's domain-modeling skill.

## Purpose

Establish a precise shared understanding of the domain
before implementation.

Use when designing features, resolving ambiguous concepts,
modifying domain models, or evaluating architectural decisions.

## 1. Discover existing terminology

Inspect available sources:

- GLOSSARY.md
- AGENTS.md
- Existing ADRs
- Architecture documentation
- Domain models and schemas
- API contracts
- Relevant source code and tests

Prefer established repository terminology.

Do not invent new names for existing concepts.

## 2. Establish ubiquitous language

Identify:
- Domain entities and value objects
- Business processes and operations
- Important states and transitions
- Relationships and constraints
- Ownership and responsibility boundaries
- Terms with multiple meanings

Challenge vague or overloaded terminology.

When terminology conflicts with existing definitions,
identify the contradiction and ask for clarification.

## 3. Stress-test the domain model

Construct concrete scenarios involving:

- Normal operation
- Edge cases
- Invalid states
- Concurrent operations
- Partial failures
- Recovery and retries
- Data consistency
- Authorization boundaries

Determine whether the proposed domain model handles
these scenarios correctly.

Prefer designs that make invalid states difficult
or impossible to represent.

## 4. Validate against implementation

Compare proposed terminology and behavior against:
- Actual database structures
- Existing domain classes
- Public interfaces
- Business logic
- Existing tests

Distinguish:
- Current implementation
- Confirmed business requirements
- Proposed architectural changes

Never assume documentation is authoritative when
source code contradicts it.

## 5. Maintain glossary proposals

When a domain term is resolved, propose a glossary entry:

Term:
Canonical name

Definition:
Precise domain meaning

Distinguishing characteristics:
How it differs from similar concepts

Related terms:
Other relevant domain concepts

The Team Lead must not directly modify repository files.

Include proposed glossary changes in the approved
implementation handoff when necessary.

## 6. Architecture Decision Records

Propose an ADR only when the decision:

1. Is costly or difficult to reverse.
2. Would be surprising without historical context.
3. Involves a meaningful architectural tradeoff.

An ADR proposal should contain:

- Title
- Context
- Decision
- Alternatives considered
- Consequences
- Compatibility implications
- Status: Proposed

Do not create ADRs for trivial implementation choices.

## 7. Planning handoff

Provide the Team Lead with:

- Confirmed domain vocabulary
- Domain invariants
- Relevant business rules
- Current implementation discrepancies
- Proposed model changes
- Architectural decisions requiring approval

## Principles

- Model the business domain, not arbitrary code structure.
- Reuse established terminology.
- Avoid speculative abstractions.
- Prefer explicit invariants.
- Preserve existing architectural decisions unless
  there is a justified reason to reconsider them.
- Never modify source code or documentation directly.
- Never silently change agreed business rules.


## Governed execution

The governance controller owns state and authorization. Maintainer plan approval and BDFL task/spec authorization precede coding. The Reviewer prepares the rubric and independently reviews real deterministic test evidence. Only the Coder edits exact approved source paths; the Maintainer decides integration and the Team Lead reports verified outcomes. Skills cannot grant tools, authorize scope expansion, or replace independent review.
