# BDFL-Governed OpenCode Coding Team

Four functional roles backed by a persistent controller, scoped edit permissions,
isolated Git worktrees, independent review, and a deterministic container test runner.
The user is the BDFL. Team Lead is the default OpenCode contact.

| Role | Model | Authority |
|---|---|---|
| Team Lead | `openai/gpt-6-sol` | Requirements, specification negotiations, final report |
| Maintainer | `openai/gpt-6-sol` | Architecture, invariants, ADRs, integration decision |
| Coder | `openai/gpt-6-sol` | Edits only explicitly approved file paths |
| Reviewer & Tester | `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free` | Read-only rubric and independent review |

There is no fifth LLM agent. Python controls transitions; Docker executes tests.
All 17 previous skills were audited. The native catalog now contains 18 verified
upstream originals/dependencies plus six unchanged, explicitly unverified local
adaptations. See [skill provenance](docs/SKILL_PROVENANCE.md) for authors, exact
restorations, licensing blockers and compatibility limits.

## Requirements

- OpenCode **v2**, configuration loading verified with installed **v2.2.3**.
- Python 3.10+, Git, and credentials for the configured providers.
- Docker Engine or Docker Desktop for governed test execution; a preloaded Linux
  image containing the project's test dependencies and `/bin/sh`.
- A clean Git checkout. Agent-visible source must contain no symlinks or submodules.

Model availability depends on the provider/account. Run `opencode models`, then
set `models.reviewer` in your runner policy to the actual provider/model ID.
Set the other three models there as needed. For interactive sessions, also edit
`model` in the corresponding `.opencode/agents/*.md`. The controller passes an
explicit `--model` on each call so session defaults cannot select a different model.

## Install

macOS/Linux:

```sh
./install.sh --project /path/to/project --dry-run
./install.sh --project /path/to/project
# Or install the bundle globally:
./install.sh --global
```

Windows PowerShell 5.1 or 7:

```powershell
.\install.ps1 -Project 'C:\Projects\MyApp' -DryRun
.\install.ps1 -Project 'C:\Projects\MyApp'
# Or:
.\install.ps1 -Global
```

Both installers preserve existing files. They install agents, skills, configuration,
and the Python controller, example policy and test-image Dockerfile. Complete
reference trees, original licenses, preserved source snapshots, compatibility patches
and the provenance/synchronization utilities are installed together. Existing JSONC prevents creation of
competing JSON. The native Windows installer has not been executed on Windows;
WSL can use the Linux installation.

For global installation, invoke the controller at
`~/.config/opencode/governance/bdfl.py --repo /path/to/project ...` instead of the
project-local path below. No Python packages need installation.

## Run an authorized task

Copy `policy.example.json` to a BDFL-controlled location **outside the target
repository**. Set its test image, fixed argv commands, timeouts and retry limits.
The example policy runs this starter's own unittest suite; replace it for other
projects. Build the supplied image with Python, Git and Bash before running it:

```sh
docker build -t bdfl-python-tests:local -f .opencode/governance/Dockerfile.tests .opencode/governance
```

Use an image pinned by digest for reproducible dependencies. Runs cannot pull images,
install dependencies over the network, or fall back to executing candidate tests on
the host.

```sh
python3 .opencode/governance/bdfl.py start \
  --request 'Fix the timeout regression while preserving the public API' \
  --policy /absolute/path/to/my-policy.json \
  --authorize-task
```

`--authorize-task` is the BDFL's authorization for ordinary implementation within
this task. After Maintainer approval, the controller prepares the rubric, invokes
the Coder, runs tests, gets independent review, handles fixes, obtains the
Maintainer's integration decision, and asks Team Lead to report the result. No
manual agent switching is needed. The Reviewer prepares its rubric before coding.

Omit `--authorize-task` to inspect the specification before any implementation.
Breaking changes, major architectural decisions and Maintainer `ESCALATE` always
pause at `AWAITING_BDFL`, even when the task was authorized. Inspect `state.json`,
including the specification, rationale, migration and risks, then use the displayed
run ID and exact specification hash:

```sh
python3 .opencode/governance/bdfl.py authorize RUN_ID \
  --spec SPEC_SHA256 --reason 'Approve the migration and compatibility tradeoff'
python3 .opencode/governance/bdfl.py status RUN_ID
python3 .opencode/governance/bdfl.py resume RUN_ID
python3 .opencode/governance/bdfl.py reject RUN_ID --reason 'Choose a different approach'
```

The CLI is the supported autonomous execution entrypoint. The default interactive
Team Lead can discuss requirements and explain these commands; its shell, source
writes and direct subagent launches are denied. Typing an implementation request in
the TUI alone does not grant execution authority. The controller calls each role
in a fresh private OpenCode session, without relying on recursive agent delegation.

## Outcomes and recovery

State lives under the repository's Git common directory:

```text
.git/bdfl/
  architecture.json            # Maintainer map, invariants, ADRs across runs
  controller.lock             # repository-wide exclusive lock
  runs/RUN_ID/state.json      # spec, decisions, authorization, rubric, test logs, events
  runs/RUN_ID/candidate.patch # includes additions and deletions; no commit required
  worktrees/RUN_ID/           # isolated bdfl/RUN_ID branch, candidate remains uncommitted
```

`READY` means tests and independent review passed and the Maintainer approved the
exact candidate for integration. The controller does **not** commit, merge, push or
deploy. Review the patch and integrate it yourself. The original checkout and its
index stay untouched. Run `resume RUN_ID` before integration: any subsequent source
or executable-bit change invalidates tests, review, integration approval and report.
`status` reports staleness but does not execute anything.

Provider errors, malformed responses and missing Docker stop with no approval.
Use `resume` after restoring infrastructure. Interrupted planning/coding attempts
consume the persisted retry budget; tests and review can be safely rerun. Plan and
implementation retries default to three each. `EXHAUSTED` and implementation/final
`ESCALATED` need a new task with revised scope or policy, rather than an implicit
retry-budget or scope override. A BDFL plan escalation can be explicitly authorized
by its hash. Rejected runs cannot resume.

After a killed controller, inspect the PID in `controller.lock`; remove it only when
that process has exited. Worktrees are retained for investigation. Never remove a
worktree containing wanted changes. Architecture memory is advisory and is checked
against source on demand; it is not an approval or authorization token.

## Enforcement and limitations

- Only the controller grants exact file edit permissions after authorization.
  A directly invoked Coder has no write tools. All roles deny unrestricted shell,
  subagents, Code Mode, MCP and external directories. Reviewer has only native
  read/discovery/skill tools; it cannot execute tests or delegate mutations.
- Every model call sees a disposable source mirror, without Git metadata, secrets,
  project OpenCode configs/plugins, or other agent configuration. Global user
  configuration is isolated via `XDG_CONFIG_HOME`; provider authentication remains
  in OpenCode's normal data location. Managed system policy still applies.
- Source scope is a list of exact relative files. Secret files, symlinks, Git and
  agent-control paths are prohibited. Changing `.opencode` or root/nested
  `opencode.json(c)` through this workflow is deliberately unsupported. Review such
  infrastructure changes separately. Ignored/untracked local files are not supplied
  unless Git tracks them. Agent snapshots cannot use host dependency directories.
- The test runner mounts source read-only, executes a copy under `/tmp`, disables
  networking, drops capabilities, uses a non-root UID and limits CPU, memory, PIDs
  and runtime. It receives no provider keys, Docker socket or host credentials.
  Build test dependencies into the preloaded image. This is container isolation,
  not a promise to withstand a hostile kernel/container-runtime exploit.
- The BDFL controls the CLI, runner policy, state directory and trusted installation.
  A host user able to rewrite those files can change governance. Permissions and
  fingerprints protect against model tool misuse, not a malicious host owner.
- Sending a task authorizes the configured providers to process the eligible
  source context. Use only providers approved for that repository's confidentiality
  requirements; configure all four roles accordingly.

## Native author skills

Skills load lazily through OpenCode's native `skill` tool. Agent frontmatter has
explicit ID allowlists; the controller copies only that role's permitted skill
directories into its mirror. Bodies and supporting references are not preloaded.
The original author text is kept separate from the execution compatibility notes.

The two minimal SEO compatibility patches replace the Claude plugin-root path.
Other imported skill bodies are unchanged. Some original procedures require
extra agents, tracker publication, inline writes or network tools; these remain
explicitly unsupported where the four-role permissions cannot provide them. A
loaded skill never grants new permissions or makes an unsupported procedure valid.

For TDD/debugging, the Coder can return `CHECKPOINT` to yield its current approved
patch to the existing deterministic runner. The controller resumes that same role
with actual results. `max_test_checkpoints` defaults to 24 per run; implementation
retry limits still apply. Checkpoints support real red/green evidence and never
replace final tests, independent review or integration approval. No extra LLM or
unrestricted shell is used. Docker must be available for any checkpoint to run.

Validate or update original sources without silently rewriting them:

```sh
python3 .opencode/governance/skillctl.py validate
python3 .opencode/governance/skillctl.py check tdd --ref main --report /tmp/tdd-update.json
# Inspect the diff, source pins, licensing status and changed-program list first:
python3 .opencode/governance/skillctl.py apply /tmp/tdd-update.json --reviewed REPORT_SHA256
# Optional actual native skill-load checks using the configured providers:
python3 .opencode/governance/verify_skills.py --live --report /tmp/native-skills.json
```

Update checks use temporary bare HTTPS Git fetches and never execute upstream
programs. Local edits, license changes and compatibility-patch conflicts block
application. Imported scripts remain source-only and non-executable. Every run
pins its skill manifest; start a new authorized run after a catalog update.
Read [SKILL_PROVENANCE.md](docs/SKILL_PROVENANCE.md) for the complete audit, safe
update/add-source procedure, role matrix and unsupported upstream capabilities.

## Migration and validation

Previous Planner, Consultant and Supervisor agent files are removed from this
repository. Installers never delete existing user files: remove obsolete copies
from an existing installation yourself, merge the new configuration, and start a
new session. Existing sessions retain their selected agent. Old adapted skill directories must
be backed up and reviewed before removal; installers never delete them. Task #1
runs need a fresh start after the skill-ID/catalog migration. Keep unrelated local
agents only if you deliberately want them; the bundled coding lifecycle has four.

```sh
opencode --version
opencode --standalone debug agents
opencode --standalone debug config
python3 .opencode/governance/skillctl.py validate
python3 -m unittest discover -s tests -v
bash -n install.sh
```

The offline suite uses real temporary Git repositories and deterministic model and
runner doubles. It covers authorization, negotiations, escalation, retries, scope,
read-only enforcement, failure handling, review invalidation, persistence, locks,
new-file patches and container invocation. See [validation notes](docs/validation.md)
for checks performed here and remaining live-environment coverage.

Configuration follows the current [v2 agents](https://opencode.ai/v2/docs/agents),
[v2 permissions](https://opencode.ai/v2/docs/permissions),
[v2 config](https://opencode.ai/v2/docs/config), and
[v2 tools](https://opencode.ai/v2/docs/tools) documentation. V1 field names and
permission syntax are not interchangeable with v2.

See [ATTRIBUTION.md](ATTRIBUTION.md) for skill provenance.
