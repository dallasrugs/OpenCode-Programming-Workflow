# Resource governance baseline

Inspected October 31, 2026 on Apple Silicon macOS. The working tree already contained
extensive uncommitted role/provenance/migration changes; these were preserved.

- Installed executable: `~/.opencode/bin/opencode`, **v2.2.5**. Version discovery
  used a disposable `XDG_DATA_HOME` because the execution sandbox cannot write the
  normal OpenCode log. No upstream runtime source was changed.
- `.opencode/opencode.json` is the repository configuration; no project root JSON
  or JSONC counterpart was present. Global configuration was inspected only for
  MCP/LSP/plugin counts, without displaying provider configuration or credentials.
- Primary coordinator: Poseidon. Native subagents: Team Lead, Maintainer, Coder,
  Reviewer, Researcher. There is **no currently configured UI Designer**. Existing
  models, provider settings, skill permissions, and authority relationships remain.
  Poseidon launches workers through native `subagent`; worker-to-worker delegation
  is denied. Coder and Reviewer retain host shell, as does Poseidon.
- The only custom plugin is `plugins/poseidon-workspace/index.js`. It uses the V2
  session hooks, tool/command transforms, permission assertions, and archive/delete
  event subscription. Previously it spawned one Python helper per operation, with
  unbounded stdout, a bounded stderr tail, and direct-child AbortSignal cancellation.
- Python `workspace.py` owns sandbox lifecycle, settings, and test evidence.
  `runtime.py` provides Git/snapshot commands and threaded output draining;
  `sandbox.py` runs session-labelled Docker containers. Tests/builds use Docker
  `exec`/`build`; containers already have memory, CPU, PID and tmpfs limits.
  Docker exec timeout already removed the session-owned sandbox. Ordinary host
  processes are launched with `subprocess.run`/`Popen`; `skillctl.py` also runs Git
  for trusted skill maintenance, outside interactive workspace execution.
- No repository-owned watcher registrations, background service, explicit LSP
  overrides, or MCP configurations were found. Global JSON configuration likewise
  contained zero MCP entries, zero explicit plugins, and no LSP overrides. OpenCode
  may still start built-in LSPs/watchers on demand. Those belong to the runtime.
- Existing agent admission had no resource scheduler. Native shell execution and
  direct invocation of the Python CLI were intentional approved paths; prompt text
  cannot make those OS-confined. Docker resources are not host child-process RSS.

The implemented boundary is the existing workspace plugin plus an optional process
supervisor, not invented global spawn/cancellation hooks. V2 executable tool transforms
were checked against the installed server using a temporary instrumented plugin copy:
20 tools wrapped, zero missing executors (before exempting the Code Mode dispatcher).
The plugin loaded as active and registered its diagnostic command without a model call.

API references: [V2 server transforms and cancellation](https://opencode.ai/v2/docs/build/plugins/server),
[plugin loading](https://opencode.ai/v2/docs/build/plugins/),
[configuration schema](https://opencode.ai/config.json),
[watcher ignore semantics](https://opencode.ai/docs/config/#watcher),
[Apple libproc implementation](https://github.com/apple-oss-distributions/xnu/blob/main/libsyscall/wrappers/libproc/libproc.c).
