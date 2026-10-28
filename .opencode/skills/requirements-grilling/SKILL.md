---
name: requirements-grilling
description: Interrogate software requirements through structured, dependency-aware questions, validate assumptions against repository evidence, and establish shared understanding before implementation.
---

# Requirements Grilling

Adapted from Matt Pocock's grilling and grill-with-docs.

## Objective

Turn an initially ambiguous feature request into a precise,
mutually understood set of requirements and decisions.

Be rigorous without asking unnecessary questions.

## 1. Understand the request

Identify:
- The problem being solved
- The desired user outcome
- Existing versus desired behavior
- Systems and users affected
- Constraints and exclusions
- What successful completion looks like

Distinguish facts, assumptions, proposals, and decisions.

## 2. Investigate before questioning

Use the codebase-understanding skill when repository
knowledge is necessary.

Read relevant documentation, source code, interfaces,
schemas, and tests.

Never ask the user for facts that can be established
from the available repository.

When documentation conflicts with implementation,
report the discrepancy.

## 3. Construct a decision tree

Represent requirements as connected decisions.

For each decision identify:
- The question being resolved
- Its prerequisites
- Available alternatives
- The recommended answer
- Consequences of each significant alternative

Identify the decision frontier: questions whose
prerequisites have already been resolved.

Do not ask questions that depend on unanswered decisions.

## 4. Interview in rounds

Present focused questions from the current frontier.

For each question provide:
- A clear explanation of the decision
- Relevant repository findings
- A recommended answer with reasoning
- Important alternatives when appropriate

Group closely related independent questions.

Avoid overwhelming the user with large questionnaires.

After receiving answers:
1. Record the decisions.
2. Update the decision tree.
3. Identify newly unlocked questions.
4. Continue until material ambiguity is resolved.

Do not reopen settled questions without new evidence.

## 5. Challenge assumptions

Consider:
- Missing use cases
- Edge cases and failure modes
- Data ownership and consistency
- API and compatibility implications
- Security and authorization
- Performance and scalability
- Error handling and recovery
- Observability and testing
- Scope creep and unnecessary complexity

Challenge weak assumptions respectfully and specifically.

Do not invent problems merely to prolong questioning.

## 6. Consult external expertise selectively

When standards, protocols, or architecture conventions
are uncertain, the Planner may consult Gemini.

Consult only when the answer could materially change
a design decision.

Provide minimal sanitized context.

Do not expose secrets, private source code, or sensitive
business data to external providers.

## 7. Maintain shared terminology

Identify ambiguous or overloaded domain terms.

Prefer existing repository terminology.

When a new term is necessary, propose a precise definition.

Record glossary additions and architectural decisions
as proposals.

The Planner must not modify repository documents directly.

## 8. Conclude the interview

The interview is complete when:
- The objective is unambiguous.
- Material decisions are resolved.
- Acceptance criteria are testable.
- Constraints and exclusions are explicit.
- Remaining assumptions are documented.

Present a concise requirements summary containing:
- Confirmed requirements
- Agreed technical decisions
- Acceptance criteria
- Out-of-scope items
- Remaining risks and assumptions

Ask the user to confirm shared understanding.

## 9. Approval boundary

Requirements confirmation is not implementation approval.

After confirmation, the Planner prepares the technical
implementation plan.

Implementation requires explicit user approval of
that plan before Supervisor delegation.

## Principles

- Discover facts; ask users for decisions.
- Ask dependent questions in the correct order.
- Recommend defaults rather than forcing guesswork.
- Preserve existing architecture where appropriate.
- Avoid redundant questions and repeated consultation.
- Never confuse assumptions with confirmed requirements.
- Never implement code during requirements discovery.
