# Current validation: author skill restoration

October 30, 2026; macOS, OpenCode v2.2.3.

- **49 automated tests pass**, including the original governance/installer suite,
  all 17 audit inputs, source hashes, preserved unverified files, native metadata,
  resources, licenses, literal patch application/conflicts, recursive installers,
  role-specific allowlists, filtered lazy catalogs, safe update reports/application,
  changed-license refusal and inert program sources.
- Coder checkpoint tests cover red then green then mandatory independent final
  gates, bounded checkpoint budgets, scope rejection, infrastructure failure/resume,
  and rejection of a changed source catalog during an authorized run.
- All four configured models loaded a representative native original through real
  `skill` tool events: Team Lead → `grilling`; Maintainer → `codebase-design`;
  Coder → `tdd`; Reviewer → `verification-before-completion`. The Reviewer used
  `openrouter/nvidia/nemotron-3-ultra-550b-a55b:free`, without an override.
- The live Coder also loaded `tdd`, wrote one red-capable unittest in a disposable
  fixture, kept the implementation unchanged and returned `CHECKPOINT`. The runner
  honestly stopped because Docker is unavailable. No upstream program executed;
  this does not claim that a red or green test actually ran on this host.
- An actual HTTPS bare-Git update check against pinned Matt Pocock commit
  `a496f5513d4a4cf889bc48e189e579f4b0bdf6aa` produced no imported-file diff and
  no licensing blocks. It did not apply an update or execute upstream code.
- The CLI recognizes the four visible native agents and their exact skill
  allowlists. The experimental cold `api skill.list` catalog is empty in this
  installed version; it is recorded as a limitation, not a successful discovery
  count. Positive loading evidence comes from actual native tool events.
- `skillctl validate`, Bash syntax checks, recursive temporary installations,
  reinstall preservation and `git diff --check` pass.

The reproducible live verifier is
`python3 .opencode/governance/verify_skills.py --live`.
See [the machine-readable record](skill-validation.json) and
[the full source audit and limitations](SKILL_PROVENANCE.md).

Docker container execution, native Windows/PowerShell execution and a complete live
four-role implementation pipeline remain untested here. Some original skill
procedures need additional agents, writes, tracker publication or network tools;
those capabilities are explicitly unsupported rather than silently rewritten.

---

## Earlier Task #1 validation record

Checks performed on macOS on October 30, 2026:

- Installed CLI reports `opencode v2.2.3`.
- `opencode --standalone debug agents` loads exactly four visible roles:
  `team-lead` (primary), `maintainer`, `coder`, `reviewer` (all).
  Build, Plan, General and Explore are disabled. Hidden OpenCode housekeeping
  agents remain; they are not functional development roles.
- Effective permissions deny edits, shell, subagent delegation and Code Mode for
  direct invocation of each role. Native read/discovery/skills remain available.
  Only the controller's Coder session adds exact authorized edit paths.
- All 17 bundled skill files are preserved. The native Coder successfully loaded
  `code-quality`. The `api skill.list` endpoint returned an empty catalog on a cold
  private server, so that endpoint was not used as proof of skill registration.
- `debug config` confirms the project default is `team-lead` and the v2
  configuration is accepted without migration to v1 fields.
- A real `openai/gpt-6-sol` Team Lead call returned JSON successfully. Its actual
  `run --format json` event stream was accepted by the adapter's text-event parser.
- A real Coder adapter call used a disposable Git fixture, read `app.py`, changed
  only the approved greeting string using the native patch tool, and read it back.
  No tests were claimed by the Coder, and the original project checkout was not
  used as its edit workspace.
- That smoke check caught a v2 integration issue: subprocess `cwd` alone was
  insufficient because the inherited logical `PWD` selected the original project.
  The adapter now sets both; the offline adapter test asserts the logical path.
- All 29 Python unittest tests pass. The suite uses real temporary Git repositories,
  worktrees and patch generation with deterministic model/test doubles, and checks
  authorization binding, revisions, BDFL escalation, rubric ordering, failed tests,
  independent review, retry exhaustion, read-only violations, changed candidates,
  stale exported patches, scope enforcement, persistence, locks, source filtering,
  model event parsing, adapter permissions, bounded logs, test timeouts, container
  cleanup, missing Docker, and installer preservation behavior.
- `bash -n install.sh`, installer dry runs, clean temporary project installation,
  reinstall preservation, JSONC preservation, and existing symlink-file handling
  pass. `git diff --check` passes.

Not exercised here:

- Docker is not installed, so the test Dockerfile was not built and the actual
  isolated container runner was not executed. Runner command construction,
  failure, timeout and cleanup paths were tested with deterministic process doubles.
- No complete live four-role workflow was executed. The configured OpenRouter
  Reviewer model needs account-specific availability confirmation using
  `opencode models`; its model ID is configurable in the runner policy.
- PowerShell/native Windows execution and Linux-host execution were not available.
  The PowerShell installer was updated alongside Bash but still needs a native run.
- OpenCode compatibility is verified against the installed 2.2.3 configuration
  loader and native Coder tools, not every future v2 release. Managed system config
  can impose additional restrictions; those are intentionally not bypassed.

The original pasted request ended at `MA` in its lifecycle diagram. The completed
path implemented here is Maintainer integration decision followed by Team Lead's
verified report. Integration yields an uncommitted candidate and patch; automated
commits, merges, pushes and deployments remain outside this starter's authority.
