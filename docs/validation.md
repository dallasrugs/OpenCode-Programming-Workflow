# Validation notes

Repository cleanup checked on October 30, 2026, on macOS.

## Checks performed

- **44 Python tests passed.** Coverage includes the five agent definitions and
  permissions, source snapshots, secret/symlink filtering, test evidence and
  staleness, sandbox lifecycle, image caching, cancellation, logs, skill provenance
  and fresh project/global installation into temporary directories.
- **Three plugin tests passed.** These check native workspace permissions, shared
  parent/child sandbox ownership, parent-session cleanup and safe log commands.
- Skill validation passed for 24 native skills: 18 verified imports/dependencies
  and six preserved, explicitly unverified adaptations. Original source bytes,
  licenses and required supporting resources remain intact.
- Bash installer syntax, JavaScript plugin syntax, runtime imports, local
  documentation links and `git diff --check` passed.

## Limits of these checks

No model requests were made. No real Docker containers were started or stopped
for this cleanup; lifecycle tests use deterministic Docker doubles. Native Windows
and PowerShell execution were not available.

The user's installed OpenCode configuration was not updated. Checks used repository
files and disposable fixtures, not the running OpenCode installation. Existing
project settings, historical worktrees and saved task data were not removed.

## Subsequent agent configuration updates

The repository coordinator is now named Poseidon. Reviewer remains on Nemotron
and has native shell access. At the user's explicit request, the installed Reviewer
definition and its matching permission validator were also updated; the Poseidon
rename and repository cleanup were not applied to the installed setup. The 44
Python tests and three plugin tests pass after these changes. No model calls were
made.
