> Historical record of the earlier UI Designer implementation and smoke tests.
> The current role is `researcher`, with project read/search, webfetch/websearch and
> read-only MCP resource access. Historical sanitized-only restrictions and model
> smoke-test results below do not describe or validate the new role. See
> [AUTHORITY.md](AUTHORITY.md) for the current permission contract.

# Inkling Designer implementation report

Implemented in the repository only; no commit, push, publication, global install
change or model reassignment. See [validation](validation.md) for actual evidence,
[authority](AUTHORITY.md) for full boundaries, and [migration](MIGRATION.md) for
exact backup/staging/merge/activation/restart instructions.

## Designer and workflow

`ui-designer` is a subagent using exactly
`openrouter/thinkingmachines/inkling:free`. It creates bounded Markdown design
handoffs and critiques from approved sanitized briefs/references. It specifies
layout, color/type/spacing, components, states, responsive behavior, accessibility
and acceptance criteria; it returns no implementation code by default.

Poseidon remains the sole visible primary/default and sole delegator. Substantial
UI work follows requirements/planning → Designer → Maintainer → Poseidon
consolidation → Coder → independent Reviewer → Poseidon fidelity check. Small
backend/maintenance/CSS tasks stay lightweight. Review limit defaults to 3 cycles
and is configurable by a positive integer in the human's task request; exhaustion
produces a blocker report. No Visual Reviewer was added.

## Effective tool permissions

| Role | Native editing | Host shell | Subagent tool | Workspace tool |
|---|---|---|---|---|
| Poseidon | Application only; protected edits denied | Allowed | Five named workers | Existing actions |
| Team Lead | Denied | Denied | Denied | Denied |
| Maintainer | Denied | Denied | Denied | Denied |
| UI Designer | Denied | Denied | Denied | Denied |
| Coder | Application only; protected edits denied | Allowed | Denied | Settings/status/test |
| Reviewer | Denied | Allowed | Denied | Settings/status/test |

Designer can only `read` the staged `design-context` tree and load `frontend-design`;
it has no grep/glob, external-directory, MCP or Code Mode grant. Other agents keep
their prior skill matrices. Filename-based secret denials remain in effect.
Only assigned global skill trees have external-directory exceptions for other roles.

All worker definitions end with a deny for every `subagent` target. Control-plane
native edit/write/patch is additionally hard-denied by `tool.use` policies, including
for Poseidon. The workspace plugin checks the real calling agent and action before
running a helper; workers cannot configure/end through that tool. Static validation
rejects authority/model changes, rogue agents, unauthorized grants and missing policies.

**Remaining risk:** Coder, Reviewer and Poseidon retain host shell. They can use host
programs or APIs to bypass native file, delegation, credential and scope restrictions.
Reviewer is not OS-enforced read-only. Docker isolates tests, not all agent actions.
No complete shell confinement or prompt-injection immunity is claimed. Privacy gates
and review-cycle limits are procedural. Strong isolation requires a separate OS/container
boundary with protected mounts/credentials and no host/orchestrator access.

## Original skill identity

- Repository: https://github.com/anthropics/skills
- Immutable commit: `ca45fc496a3436251f191354091d557da31c15b5`
- Original directory: `skills/frontend-design`
- License: **Apache License 2.0**, original `LICENSE.txt` retained unchanged.
- Original SKILL and repository third-party notices copied without rewriting;
  source paths, source hashes, installed hashes and modes recorded in SOURCES.
- Snapshot: `.opencode/skill-sources/upstream/frontend-design/`
- Native installation: `.opencode/skills/frontend-design/`
- Apache approval is restricted to this source identity and exact license digest;
  existing MIT/provenance/tampering/sync checks remain fail-closed.

## Actual verification

- **59/59 Python tests passed, 0 failures, 0 skips** with live evaluator enabled
  (default offline discovery: 54 passed, 5 opt-in tests skipped).
- **4/4 Node plugin tests passed, 0 failures.** Plugin permission APIs are doubled.
- Provenance: **25 native skills, 19 verified imports, 6 preserved unverified
  adaptations, 173 imported files**. Original imports/hashes/licenses preserved.
- Bash/JavaScript syntax, published schema field checks and diff whitespace passed;
  OpenCode **v2.2.4** actually parsed/discovered the six agents.
- Real native permission API rejected worker delegation, forbidden Designer actions,
  restricted skills and protected edits, including a conflicting Coder grant.
  These are runtime permission checks, not forced executions of forbidden tools.
- Exact Inkling ID resolved from the existing local OpenRouter catalog. Actual
  Inkling skill/read calls and a completed synthetic dashboard handoff succeeded.
  Actual native Poseidon → Designer delegation completed; child model metadata
  independently confirmed Inkling. No model substitution or provider availability issue.
- No visual inspection, live Docker execution or native Windows execution performed.
- The installed bundle differs: read-only comparison found **9 different, 7 missing,
  372 identical** managed files. It was left untouched. Follow the migration guide;
  installing missing files over old config alone is not a validated upgrade.

## Example request

> Poseidon, design a community garden volunteer dashboard from this sanitized mock
> brief. Keep routes/API unchanged, use UI Designer for desktop/tablet/mobile design,
> have Maintainer assess compatibility, then delegate implementation and independent
> review. Review iteration limit: 2. Report any missing visual checks.

## Complete changed-file inventory

- `.opencode/agents/coder.md`
- `.opencode/agents/maintainer.md`
- `.opencode/agents/poseidon.md`
- `.opencode/agents/reviewer.md`
- `.opencode/agents/team-lead.md`
- `.opencode/agents/ui-designer.md`
- `.opencode/opencode.json`
- `.opencode/plugins/poseidon-workspace/index.js`
- `.opencode/runtime/skillctl.py`
- `.opencode/skill-sources/upstream/frontend-design/LICENSE.txt`
- `.opencode/skill-sources/upstream/frontend-design/SKILL.md`
- `.opencode/skill-sources/upstream/frontend-design/THIRD_PARTY_NOTICES.md`
- `.opencode/skills/SOURCES.json`
- `.opencode/skills/frontend-design/LICENSE.txt`
- `.opencode/skills/frontend-design/SKILL.md`
- `.opencode/skills/frontend-design/THIRD_PARTY_NOTICES.md`
- `ATTRIBUTION.md`
- `README.md`
- `docs/AUTHORITY.md`
- `docs/IMPLEMENTATION_REPORT.md`
- `docs/MIGRATION.md`
- `docs/SKILL_PROVENANCE.md`
- `docs/validation.md`
- `install.ps1`
- `install.sh`
- `tests/test_hierarchy.py`
- `tests/test_install.py`
- `tests/test_live_permissions.py`
- `tests/test_native_agents.py`
- `tests/test_skills.py`
- `tests/test_workspace_plugin.mjs`
