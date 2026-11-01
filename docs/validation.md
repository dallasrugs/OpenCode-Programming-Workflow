# Researcher validation — October 30, 2026

The former `ui-designer` is now `researcher`. The model is unchanged. Verified:

- Offline Python discovery: 54 passed, 5 opt-in live tests skipped (59 total).
- All 5 opt-in tests then passed against a disposable OpenCode v2 localhost server
  with temporary XDG state and no model requests. Native discovery found researcher;
  permission checks allowed project read/glob/grep, webfetch/websearch and MCP
  resource reads, while rejecting edits, shell, code execution, workspace actions,
  arbitrary MCP tools, credentials and worker delegation.
- All 4 Node plugin tests passed. Skill/provenance validation passed (25 native
  skills, 19 verified imports, 6 preserved adaptations, 173 imported files).
- Fresh project/global installer behavior is covered by the Python suite.

Web search/fetch and MCP resource permissions were evaluated, not actual provider
or MCP calls. Availability depends on configured services. No model generation,
visual inspection, live Docker execution or global installation update was performed.
Restart with a new chat after activating the updated bundle; see
[migration](MIGRATION.md#researcher-rename) for removing the old agent file.

## Earlier implementation record

> Historical record of the earlier UI Designer implementation and smoke tests.
> The current role is `researcher`, with project read/search, webfetch/websearch and
> read-only MCP resource access. Historical sanitized-only restrictions and model
> smoke-test results below do not describe or validate the new role. See
> [AUTHORITY.md](AUTHORITY.md) for the current permission contract.

# Validation notes

Inkling Designer/hierarchy change checked October 30, 2026, on macOS with
**OpenCode v2.2.4**. The installed bundle was compared read-only and differs from
the repository; it was not upgraded or overwritten. No commit, push or publication.

## Automated results

- **59 Python tests passed, 0 failures, 0 skips** with the five opt-in real
  OpenCode permission tests enabled. Command:
  `python3 -m unittest discover -s tests -v`, with `OPENCODE_TEST_URL` pointing at
  a disposable local v2 server and its temporary password supplied through the
  environment. Default discovery without that server runs **54 passed / 5 skipped**.
- **4 Node plugin tests passed, 0 failures** using
  `node --test tests/test_workspace_plugin.mjs`. They exercise the actual plugin
  with API/permission doubles, including rejection before helper execution.
- `python3 .opencode/runtime/skillctl.py validate` passed: **25 native skills,
  19 verified imports, 6 unchanged unverified adaptations, 173 imported files**.
- `bash -n install.sh`, `node --check` on the workspace plugin, and
  `git diff --check` passed. Published schema field/structure checks passed;
  native CLI agent discovery parsed the actual v2 configuration/frontmatter.
- Fresh project/global Bash installations in temporary directories validate and
  include the sixth agent, skill, license and source snapshot. Existing config,
  JSONC, symlinks and customized Designer definitions remain preserved.

Static negative tests cover role/model promotion, worker delegation grants,
Designer shell/Code Mode/MCP/workspace expansion, unknown agent/role catalogs,
missing hard policies, restricted skills, license/source identity, skill/license/
notice tampering and read-only migration comparison. Existing sandbox lifecycle,
source fingerprint/staleness and provenance synchronization tests still pass.

## Real OpenCode permission evaluation

`tests/test_live_permissions.py` uses the actual v2 REST permission evaluator,
not `skillctl.permission`, against copied synthetic fixtures. It verifies all
worker/target pairs (including self, Poseidon, unknown and disabled built-ins),
Poseidon delegation allows, Designer read allowlist and denials, skill restrictions,
workspace actions, native editing limits and sole visible primary discovery.
It deliberately adds a Coder grant to edit Poseidon's definition; the hard
`tool.use` policy still returns **deny**.

Endpoints inspected from the running server's OpenAPI document:
`GET /api/agent`, `POST /api/session`,
`POST /api/session/{sessionID}/permission`. A matching permission request is
runtime evaluated and rejected; these tests do **not** execute a forbidden edit
or force a model to emit a forbidden native subagent call. Allowed host shell
checks remain allowed and are explicitly documented as residual risk.
The malicious README fixture demonstrates that plain file text does not alter
configuration; it is not an adversarial model/prompt-injection benchmark.

To repeat against a disposable server, keep all server state in temporary XDG
config/data/cache/state directories, run `opencode serve --hostname 127.0.0.1
--port PORT`, then supply its printed local URL/password through
`OPENCODE_TEST_URL`/`OPENCODE_TEST_PASSWORD`. Do not use a production server for
this suite. It creates synthetic sessions and no model requests. Stop the server
and discard its state afterwards. No provider credentials are needed.

## Actual provider/model smoke tests

The existing local OpenRouter provider's **real model catalog** resolved exactly
`openrouter/thinkingmachines/inkling:free`. The public OpenRouter catalog also
listed that exact ID, image input and tool support; structured response formatting
was not assumed. The existing provider and model assignments were unchanged.

Using only a synthetic community-garden volunteer dashboard brief in a temporary
project and the existing configured connection:

1. A real `ui-designer` session called native `skill` for `frontend-design` and
   native `read` for `design-context/brief.md`; both completed.
2. Inkling returned a completed Markdown handoff with the required headings,
   tokens, layout/wireframe, responsive behavior, states, accessibility and criteria.
3. A real Poseidon session on `openai/gpt-6-sol` invoked the native `subagent` tool
   with `agent: ui-designer`. The tool completed and returned a design direction.
4. The delegated child's assistant messages independently recorded
   `providerID: openrouter`, `id: thinkingmachines/inkling:free`, with a terminal
   `stop` finish. This confirms provider execution, not just the parent's claim.

The first root-session attempt failed before creating any model messages because
the temporary project had no Git repository for the installed workspace prompt
hook. Initializing **only that temporary repository** resolved it; the retry and
native delegation completed. No models were substituted. No provider credentials
were read/printed or included in prompts; only local server authentication and
the already-connected provider handled authentication.

## Remaining validation limits

No visual browser/screenshot inspection was performed. The generated specification
is smoke-test evidence, not a validated production design or accessibility audit.
No real Docker container was started for this change: sandbox tests use deterministic
Docker doubles. Native Windows/PowerShell execution was unavailable.

Host shell remains outside file-edit permission confinement. Coder/Reviewer can
bypass native file protections using a host process; Reviewer is not OS-enforced
read-only. Review-iteration and privacy/scope gates are documented instructions,
not runtime counters or automatic sensitive-data classifiers. See
[authority boundaries](AUTHORITY.md) for precise limitations and
[migration](MIGRATION.md) before updating any installed bundle.

The v2 schema and APIs were checked against the installed CLI and official
[v2 permissions](https://opencode.ai/v2/docs/permissions),
[policies](https://opencode.ai/v2/docs/policies), and
[plugin permission assertions](https://opencode.ai/v2/docs/build/plugins/server).
V1 `permission`/`bash`/`task` configuration was not introduced.

## November 1, 2026 — user vision and GTD integration

- `python3 -m unittest discover -s tests -v`: 69 tests ran, 64 passed, five opt-in
  live-server permission tests skipped. Includes shared interview access and
  dependencies, Researcher restrictions, Poseidon-only GTD access, complete GTD
  reference/license installation and root-level source update round-trip.
- `python3 .opencode/runtime/skillctl.py validate`: passed; 27 native skills,
  21 verified imports, six preserved unverified inputs, 187 imported files.
- `bash -n install.sh` and `git diff --check`: passed.
- Bounded live behavior evidence and failed attempts are recorded in
  `AGENT_EVALUATION.md`. These do not constitute broad design-quality or runtime
  approval enforcement claims. No existing user installation was migrated or
  globally reloaded; the live exercises used a disposable installed bundle.

## November 1, 2026 — non-Git session startup repair

The real startup log showed HTTP 500 from the global workspace prompt hook because
`git rev-parse --show-toplevel` failed in `experimental/notepad++`, a non-Git folder.
The repository and installed global workspace helper now return a successful
`unavailable/not_git_repository` result for startup, inspection and cleanup there.
Actual configuration/test actions still fail explicitly; no Git repository or
workspace state is created. No agent definitions/providers were migrated.

Six focused workspace tests passed, including non-Git startup without writes and
non-Git tests remaining a failure. The installed plugin prompt/context hooks were
exercised against that actual folder with stub session/model APIs and the real
helper; startup succeeded and surfaced sandbox-unavailable context. No model call
was made. UI retry remains to be observed. The pasted later log contains SIGTERM
shutdown after about 25 seconds but does not establish who requested termination.
The prior installed helper is backed up at
`/private/tmp/opencode-startup-fix-ewtqpdan/workspace.py.before`. The broader agent
evaluation/tuning task remains paused.

## Publication checks — 2026-11-01

Before publishing the accumulated reliability and discovery changes:

- Python suite: 89 tests run, 84 passed and five opt-in tests skipped.
- Node contracts, reliability, workspace, resource-governor and provider-budget suites: 45 passed, zero failures.
- Skill manifest validation: 27 native skills, 21 verified imports, six preserved unverified legacy entries.
- `bash -n install.sh` and authored-file whitespace checks passed. Staged full-diff checks also report pre-existing whitespace in the two byte-preserved upstream frontend-design notices; those licensed source bytes were intentionally retained.
- README local links and coverage of all 27 catalog skill IDs were checked.

No live agent evaluation or provider request was part of these checks. README
project evidence distinguishes the Poseidon-led installation that produced
PocketCalc from this repository's Team Lead-led contract bundle. Existing
configuration was not migrated as part of publication.
