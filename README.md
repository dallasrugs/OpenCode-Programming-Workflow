# OpenCode Programming Workflow

This project turns OpenCode into a small programming team. You describe what you
want to build or fix, and talk to **Poseidon**, the coordinating agent. Poseidon brings in
other agents to plan the work, write code, check the design and review the result.
You stay in one conversation and make the final decisions.

The agents do the reasoning. A few small Python helpers manage Docker test
sandboxes, project settings and test logs. There is no separate controller to
start and no request file or authorization token to prepare.

## Meet the team

| Agent | What it does | Model |
|---|---|---|
| **Poseidon** | Your main contact; coordinates the work and reports the result | OpenAI GPT-6 Sol |
| **Team Lead** | Turns requirements into a practical plan | OpenAI GPT-6 Sol |
| **Maintainer** | Checks architecture, compatibility and maintainability | OpenAI GPT-6 Sol |
| **Coder** | Makes the code changes and addresses feedback | OpenAI GPT-6 Sol |
| **Reviewer** | Independently reviews the changes and test evidence | NVIDIA Nemotron via OpenRouter |

Poseidon decides how much planning and review a task needs. A small fix can stay small;
a larger change can involve all four specialists. Delegation appears directly in
OpenCode, so you can see which agent is working.

The definitions live in [.opencode/agents](.opencode/agents). Poseidon is the default
agent. The first four use `openai/gpt-6-sol`; Reviewer uses
`openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`. To change a model, edit its
agent's `model` field. OpenCode uses your existing provider connections; this
project adds no login system and stores no model credentials.

## Set it up

You need:

- **OpenCode v2** and connections for the configured OpenAI/OpenRouter models.
- **Git** and **Python 3.10 or newer** for the workspace helpers.
- A running **Docker engine** for sandbox tests. On macOS, start Docker Desktop.

For a project installation, run these commands from this starter's directory:

```sh
./install.sh --project /path/to/your/project --dry-run
./install.sh --project /path/to/your/project
```

Or install globally, so the team is available in all your repositories:

```sh
./install.sh --global
```

On Windows, use `./install.ps1 -Project 'C:\Projects\MyApp'` or
`./install.ps1 -Global`. Add `-DryRun` to preview the changes.

Installers preserve existing files. They do not overwrite an older installation
or remove its files automatically. Review an existing installed bundle before
replacing it. Restart OpenCode after deliberately updating its configuration.

## Give it a task

Open a new OpenCode chat in your repository:

```sh
cd /path/to/your/project
opencode
```

Then send a normal request, for example:

> Refine the notebook layout for desktop and mobile. Preserve autosave and the
> existing API. Run the frontend and browser tests, then explain what changed.

Poseidon inspects the project, delegates the appropriate work, and brings back the
changes, actual test results and any unresolved issues. You do not need to switch
agents manually or supply a controller run ID. Agents should preserve unrelated
changes and commit or publish only when you ask them to.

## What Docker is for

Docker provides an isolated place to run your project's tests. The container image
contains the tools those tests need: for example Python, Node and a browser.
The image is specific to the project; it is not an AI agent.

On first use, Poseidon inspects the project and saves its test setup. It can reuse an
existing image or build one from a saved Dockerfile recipe. Once configured, the
sandbox starts when you send a request and is reused during that chat. Delegated
agents share their parent chat's sandbox.

For each test run, the helpers copy the current source into the container and run
the configured commands. Tests run without network access or host mounts; image
building can download dependencies. Results include real command output and a
source fingerprint. If the code changes during validation, the result is marked
stale instead of being reported as a pass.

The agents still edit your repository through native OpenCode tools. The Docker
sandbox isolates tests; it does not enclose every agent action. Standard OpenCode
permissions in the agent definitions control tool access. Coder has native edit
and shell access. Reviewer also has shell access for inspection and tests, with
instructions to leave application source unchanged.

## Logs, settings and cleanup

Ask Poseidon to show test output in OpenCode's shell. Structured workspace tool calls
also report progress. Full helper logs and test evidence are saved with the project:

```text
.git/bdfl/
  settings.json       # Docker setup and test commands
  image-cache.json    # Reusable image build information
  sessions/           # Which sandbox belongs to each chat
  operations/         # Setup and test logs
  evidence/           # Test results tied to the source that was tested
```

The `bdfl` storage-directory name is retained so existing project settings, logs
and sandbox ownership continue to work. These files are local to the project
and survive OpenCode restarts. They are
outside the application working tree, so saving settings does not create source
changes. Git worktrees share their Git common directory's settings.

Two commands are available in OpenCode:

- `/poseidon-logs LOG_ID` asks Poseidon to show a saved workspace operation's log.
- `/poseidon-end` removes the current chat's sandbox and keeps its settings and work.

Archiving or deleting the parent chat also removes its container. Deleting a
worker agent's session does not remove the parent's sandbox. A later request can
recreate the sandbox from the saved configuration. Closing the UI alone does not
end a saved chat. Docker must be reachable for container cleanup to succeed.

The [example settings](.opencode/runtime/settings.example.json) show the available
test and sandbox options. Poseidon can configure these through `poseidon_workspace`; you
do not have to write the file yourself. Existing version 1 project settings remain
readable, but their old model/retry fields do not control the native agents.

## What's in this repository

| Location | Purpose |
|---|---|
| `.opencode/agents/` | The five agents, their models, permissions and instructions |
| `.opencode/plugins/poseidon-workspace/` | OpenCode integration for sandbox lifecycle and workspace tools |
| `.opencode/runtime/` | Small sandbox, settings, logging and source-validation helpers |
| `.opencode/skills/` | Skills available to the agents |
| `.opencode/skill-sources/` | Pinned originals, licenses and audit records for those skills |
| `.opencode/skill-resources/` | Supporting material required by imported skills |
| `tests/` | Checks for the current agents, helpers, plugin and installers |

Skill source snapshots and original licenses are intentionally retained. They are
used to verify provenance, not loaded as duplicate agents or skills. See
[skill provenance](docs/SKILL_PROVENANCE.md) and [attribution](ATTRIBUTION.md).

## Check the starter

These checks do not invoke models or require model credits:

```sh
python3 -m unittest discover -s tests -v
node --test tests/test_workspace_plugin.mjs
python3 .opencode/runtime/skillctl.py validate
bash -n install.sh
```

[Validation notes](docs/validation.md) record what has actually been checked and
what still needs live-environment testing.
