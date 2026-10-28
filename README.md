# OpenCode Multi-Agent Starter

An approval-gated multi-agent software engineering workflow for OpenCode v2.

## Agents

| Agent | Default model | Responsibility |
|---|---|---|
| Planner | GPT-6 Sol | Requirements, architecture, planning and review |
| Consultant | Inkling (free) | Optional technical research |
| Supervisor | Nemotron 3 Ultra (free) | Milestone coordination and auditing |
| Coder | GPT-6 Sol | Implementation, debugging and verification |

Models are configurable. Users must supply their own provider credentials.

## Workflow

1. Describe the task to Planner.
2. Planner investigates the repository and clarifies requirements.
3. Consultant provides technical advice when needed.
4. Planner prepares an implementation specification.
5. The user explicitly approves the plan.
6. Supervisor decomposes approved work into milestones.
7. Coder implements and verifies the changes.
8. Supervisor audits the results.
9. Planner reviews the final implementation.

No implementation begins before explicit approval.

## Included

- Four agent definitions
- Eleven engineering skills
- Six writing, SEO, and eCommerce skills
- OpenCode v2 project configuration
- Approval-gated implementation
- Risk-adaptive TDD
- Root-cause debugging
- Evidence-based verification

## Requirements

- OpenCode v2 (tested with 2.2.0)
- Access to configured model providers
- Git

## Configuration

Agent definitions: .opencode/agents/

Engineering skills: .opencode/skills/

Default agent and delegation depth: .opencode/opencode.json

Change model IDs in the agent YAML frontmatter.

Check available models with: opencode models

## Installation

Clone the repository:

    git clone https://github.com/dallasrugs/opencode-multi-agent-starter.git
    cd opencode-multi-agent-starter

### Linux and macOS

Preview global installation:

    ./install.sh --global --dry-run

Install globally:

    ./install.sh --global

Install into an existing project:

    ./install.sh --project /path/to/project

The installer preserves existing configuration files.
Existing files must be updated or merged manually.

### Verification

    opencode debug agents
    opencode api skill.list

For native Windows setup, see the Windows installation section below.

## Security

Agent instructions prohibit automatic commits, pushes,
merges and deployments.

Use feature branches for implementation work.

Do not share credentials or confidential source code
with external providers without authorization.

Free models may be rate-limited.

Read-only orchestration smoke tests have passed.
Real implementation quality requires additional validation.

## Attribution

See ATTRIBUTION.md.

## Windows installation

The starter supports native Windows 10/11 through PowerShell.

### Prerequisites

1. Install OpenCode v2 for Windows.
2. Install Git if you want to clone the repository.
3. Configure access to your selected model providers.
4. Download or clone this repository.

Official OpenCode installation:
https://opencode.ai/v2/docs

### Global installation

Open PowerShell in the downloaded repository folder.

Preview installation:

    powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Global -DryRun

Install:

    powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Global

Installs the agent and skill files under:

    %USERPROFILE%\.config\opencode

No administrator privileges are required for this
per-user installation.

The execution policy override applies only to the
launched PowerShell process. Review the script before
running it.

### Project installation

Preview:

    powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Project "C:\Projects\MyApp" -DryRun

Install:

    powershell.exe -NoProfile -ExecutionPolicy Bypass -File .\install.ps1 -Project "C:\Projects\MyApp"

The project directory must already exist.

Files are installed under the project's .opencode
directory.

### Verification

Restart OpenCode, then run:

    opencode debug agents

To check skill registration:

    opencode api skill.list

### Model configuration

The four agent definitions contain default model IDs.

Edit the model field in the respective agent Markdown
file to select models available to your account.

Confirm model availability with:

    opencode models

### Existing configurations

The installer never overwrites existing files.

Existing JSONC configuration is also preserved.
If an existing configuration is skipped, manually merge
the required settings for the default Planner agent and
nested delegation.

### Windows Subsystem for Linux

WSL users can instead run install.sh inside their
Linux environment.

WSL and native Windows maintain separate user
configuration directories.

### Important

The native PowerShell installer is designed for Windows
PowerShell 5.1 and PowerShell 7. Windows execution tests
should be completed before the first public release.

> **Windows status:** The PowerShell installer is included but has not yet been tested on a Windows machine.
