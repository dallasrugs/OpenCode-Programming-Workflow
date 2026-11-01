# Current integration note — November 1, 2026

Team Lead now owns orchestration. The resource governor's one-worker/one-heavy-tool defaults remain. [Agent contracts](AGENT_CONTRACTS.md) add per-turn admission/step/runtime/output limits and bounded local search. New guards reuse a registered global legacy workspace tool rather than duplicating sandbox hooks/monitors; installation-specific plugin IDs avoid a duplicate-ID rejection. Research control operations have a reserved finalization slot. No whole-host FD/memory stability claim follows from short fixture runs.

# Resource governance and troubleshooting

The governor is installed with the existing workspace plugin. It adds no dependencies
beyond Node-compatible JavaScript, Python 3.10+, and the OS. Restart OpenCode after
updating the bundle. Existing installers copy new files but never overwrite old ones;
use the repository migration/compare-install workflow when upgrading an installation.
Do not combine a new plugin with missing or stale governor files.

The implementation files are `runtime/resource-governor/{governor.mjs,config.json,
sample.py,cli.mjs,benchmark.mjs}`, relative to `.opencode/`. Integration changes are in
`plugins/poseidon-workspace/index.js`, `runtime/{runtime,workspace,sandbox}.py`, and
`opencode.json`; tests are in `test_resource_governor.mjs`, `test_workspace_plugin.mjs`,
`test_runtime.py`, and `test_sandbox.py`. No role/model/provider changes were made for
this task. See [the inspected architecture](RESOURCE_BASELINE.md).

## Configuration

Edit `runtime/resource-governor/config.json` as a trusted operator and restart the
runtime. Configuration is validated and deeply frozen for thresholds. There is no
agent-facing API for changing budgets or disabling monitoring. Existing native
control-plane edit denials protect these files. Host shell remains a documented
bypass of those filesystem permissions; this is not an OS security boundary.

| Setting | Default and behavior |
| --- | --- |
| `maxAgents` | 1 admitted native subagent call; the primary coordinator is not counted |
| `maxTools` | 1 heavy/tool call, including shell and MCP tools |
| `maxShells` | 1 managed shell limit, also subject to the stricter heavy-call limit |
| `maxDepth` | 1 in the governor; existing worker delegation denials remain. OpenCode v2.2.5 ignores the legacy `subagent_depth` setting, so it was removed |
| `maxQueue` / `queueTimeoutMs` | 4 pending heavy/agent jobs, 60 seconds maximum wait |
| `workTimeoutMs` / `graceMs` | 15 minute cooperative timeout; managed processes get TERM then KILL after 2 seconds |
| `activeSampleMs` / `idleSampleMs` | 7.5 seconds active or queued, 30 seconds idle; extra coalesced spawn/exit samples |
| `thresholds` | System FD fractions 50%, 65%, 80%, 90% |
| `hysteresis` / `recoverySamples` | 5 percentage points; 3 healthy samples for each step of recovery |
| `fdSoft` / `fdHard` | 1,024 / 2,048 numeric descriptors per measured process |
| `workloadFDSoft` / `workloadFDHard` | 2,048 / 4,096 descriptors summed across an owned process group |
| `rssSoftFraction` / `rssHardFraction` | 20% / 30% of actual physical RAM across the runtime and managed groups |
| `workloadRssSoftFraction` / `workloadRssHardFraction` | 10% / 20% of physical RAM per owned group |
| `metricTimeoutMs` | 3 seconds per OS sampler; one sampler in flight |
| `outputBytes` / `historySize` | 1 MiB per helper stream; 64 diagnostic events |
| `leakSamples` / `leakGrowth` | 6 increasing FD samples, growth of at least 64, with stable workload count |

All thresholds are heuristics. Memory budgets track RSS, not virtual memory. Shared
RSS pages can be double-counted. Allocator memory and system memory pressure are
reported as unavailable, not inferred from VSZ or free-page counts. Docker VM/container
memory is not included in host group RSS; existing Docker limits remain necessary.

## Admission and recovery

`NORMAL` uses configured capacity. `WARNING` reduces capacity by one (minimum one).
`THROTTLED` admits one job in each lane. `CRITICAL` stops new heavy/agent work.
At 90% system FD usage or a hard process/workload budget, eligible active work is
cancelled. `RECOVERING` admits no new heavy work while validating recovery; capacity
returns one pressure level at a time. Queued work can expire during a long recovery;
retry after resources stabilize. No kernel limits or reboot settings are changed.

Queues are FIFO within lanes. Explicit trusted interactive scheduling has at most
five seconds of preference, so older work cannot starve. Parent agents occupy an
agent slot, not a tool slot. Nested agent requests at saturation fail with backpressure
rather than waiting behind their ancestors. Callers must release/retry such work.
The Code Mode `execute` dispatcher is exempt to avoid parents holding a tool permit
while waiting for nested tools; registered underlying tool executors remain wrapped.
Direct Code Mode computation itself is not resource scheduled. Helpers used for safe observation are separately bounded. Python command capture is capped at 16 MiB per stream and explicitly rejects oversized required results; streaming test evidence retains its existing bounded tails.

Observation and cleanup have a separate single-slot lane, with four queue places;
they work during pressure/monitor failure and cannot launch unbounded helper counts.
Invalid/unavailable critical OS metrics fail closed for heavy work. Cancelling native
operations is cooperative: an executor that ignores its signal keeps its permit until
it settles. It cannot free a slot and keep growing unseen through that permit.

## Monitoring and ownership

On macOS `sysctlbyname` reads `kern.num_files`, `kern.maxfiles`, and `hw.memsize`.
`libproc` enumerates only known owned process groups, capped at 64 sampled PIDs, and
`PROC_PIDLISTFDS` counts numeric descriptors without counting `cwd`, text mappings,
or mapped libraries as descriptors. One targeted `ps` reads PID, PPID, group, RSS,
VSZ and zombie state. Unavailable per-process FD counts pause admission. Sampling
over the PID bound fails closed. No periodic full-system `lsof` is used.
Linux uses `/proc` for system/known-process FD counts; group expansion is currently
macOS-only. Unsupported OS metrics fail closed; Windows process-tree cleanup is not
claimed. The sampler is timeout-bounded and reaped; monitoring uses one self-scheduling
timer rather than overlapping intervals. It stops on plugin disposal or CLI exit.

The registry records PID, PPID, owning session/agent/task, start time, ownership UUID,
status, timeout, cancellation and cleanup. Workspace helpers start isolated process
groups. Only those created groups receive TERM/KILL, never discovered unrelated
OpenCode descendants. Child `close` captures exit status and releases permits after
pipes close. Even successful group leaders cannot leave background children behind
in their group. Completed registry entries and rolling PID windows are removed;
only bounded cleanup events remain. The Python helper has an orphan watchdog when
it is an isolated group leader, so a dead plugin/server parent triggers cancellation.

Docker exec cancellation, exceptions, and timeouts remove only the verified
session-labelled container. Session archive/delete cancels that root's admitted
work and removes its sandbox. Deleting a child does not cancel its root. Plugin
shutdown attempts cached-session sandbox cleanup within a total ten-second deadline,
then aborts remaining helpers and closes the monitor. Docker daemon failure or a
hard kill can require a later `/poseidon-end`; no guarantee is made that daemon-owned
containers disappear after a host SIGKILL. The existing persisted sandbox registry
and ownership labels support safe retry. Groups that deliberately call `setsid` or
change groups can escape group cleanup and are outside this boundary.

There are no local/remote MCP servers configured in this bundle. Registered MCP tool
executors use the heavy-tool queue, deadlines and cancellation signals, including
catalog refreshes. OpenCode owns MCP transports, connection reuse and server lifecycle;
this change neither duplicates them nor kills shared servers. `Governor.own()` is an
idempotent disposal registry for future harness-owned transports/watchers, tested with
simulated handles. Actual MCP transport idle expiry/reuse is not implemented here
because there is no harness-owned transport. Native LSPs, watchers and global MCPs
remain OpenCode's responsibility. Recursive generated-directory watcher exclusions
are in `opencode.json`; project source files remain watched. No watcher-to-FD ratio
is assumed.

## Diagnostics and future ENFILE events

In OpenCode, use `poseidon_workspace` with `action: "status"` for a resource report in
the tool result, or `/poseidon-resources` for a synthetic diagnostic context message.
That report belongs to the live plugin; the standalone CLI reports its own process
and any work it supervises, not another OpenCode server's in-memory registry.

```sh
node .opencode/runtime/resource-governor/cli.mjs doctor
node .opencode/runtime/resource-governor/cli.mjs resources --json > resources.json
node .opencode/runtime/resource-governor/cli.mjs resources --watch --json
node .opencode/runtime/resource-governor/cli.mjs run -- executable argument
node .opencode/runtime/resource-governor/benchmark.mjs
```

The watch stops on Ctrl-C/SIGTERM or after 480 samples (about one hour). JSON includes
system FD usage/limit, process metrics, estimated managed RSS, counts of admitted
agents/tools and queued jobs, state, warnings, bounded recent cleanup events,
configuration, Node/platform and governor format version. Record `opencode --version`
separately. History is an in-memory ring; it rotates at 64 events and writes no logs.
Export a snapshot manually for issue reports. There is no unbounded on-disk diagnostic
history. Reports omit argv, tool outputs, prompts, environment, and file contents;
review session identifiers before sharing. Existing operation evidence/logs are
separate and can contain task output; do not attach them without review.

For a future incident:

1. Stop admitting new work. Capture live workspace status plus a standalone `doctor`
   report, time, OpenCode version, macOS version and whether pressure recovers when
   managed tasks finish. Do not attribute all system growth to this harness.
2. Compare `kern.num_files / kern.maxfiles` over multiple observations. `ENFILE`
   means system-wide exhaustion. `EMFILE` means one process hit its own descriptor
   limit; inspect that process's limits and numeric descriptors instead.
3. Inspect the report's known PID/group RSS and FD trends and `leak-suspected`
   evidence (sample count, duration, growth, stable admitted workload count). A high
   reading alone does not establish a leak. Legitimate within-task expansion can
   still produce a heuristic warning. Zombie warnings identify unreaped processes,
   not descriptor ownership; a zombie generally has already released descriptors.
4. If needed, run **one targeted** `lsof -nP -p PID` on an identified process.
   Separate numeric FD rows from cwd/txt/mem entries. Avoid repeated system scans
   while under pressure. Watcher exhaustion has different OS limits and needs
   watcher/LSP diagnostics; do not assume every watcher is one FD.
5. Cancel through the session or `/poseidon-end`. Check cleanup events and retry
   owned sandbox cleanup if Docker was unavailable. Never kill broad process names
   or processes merely because they descend from OpenCode. Investigate unsupported
   raw shell/direct CLI/LSP/MCP paths if managed counts remain flat.

## Verification and limits

Run `node --test tests/test_resource_governor.mjs tests/test_workspace_plugin.mjs`,
`python3 -m unittest discover -s tests -v`, Python compilation, `node --check` on the
JS modules, `bash -n install.sh`, and `runtime/skillctl.py validate`.
Native sampling tests require macOS process/sysctl read access; a sandbox that blocks
those calls should cause a monitoring failure, never silently bypass admission.
Tests simulate emergency pressure rather than exhausting the machine. Integration
uses eight temporary file handles and twelve short simulated agent workloads.

A ten-sample macOS benchmark measured **31.8 ms/sample**, **15.0 ms supervisor CPU**
total, **1.44 MB RSS increase**, unchanged **15 numeric FDs**, and zero remaining
managed children. CPU/RSS figures cover the supervisor; elapsed time includes the
Python/ps helper cost. This is a bounded smoke measurement, not a long-duration proof
of leak freedom or a model/browser workload benchmark. At 7.5-second intervals the
measured sampler wall time is about 0.42% of one interval.

Native tool transforms were accepted by a real disposable OpenCode v2.2.5 server;
no paid/provider/model requests were made. Permission tests passed against that
server. Automated tests cover native executor wrapping with faithful test doubles,
not full LLM-driven native subagent or remote MCP execution. Real Docker cancellation,
forced server-crash recovery, long-session behavior, and Windows/Linux tree handling
remain unverified. Existing Docker execution is simulated in the Python suite.

**Enforcement boundary:** native registered tool calls inside this plugin's location,
workspace helpers launched by this plugin, and optional supervisor-owned groups.
Each OpenCode location/server or CLI supervisor has its own governor; these are not
a machine-wide shared scheduler. Host shells can launch arbitrary background work,
modify controls or kill other sessions under the same OS user. Direct Python CLI
calls, raw SDK shell/API requests and other plugins may bypass these wrappers.
File edit permissions do not constrain shell syscalls. Root/Team Lead cannot bypass
governor admission through its configuration API, but OS-level confinement requires
a separate restricted OS account/container and removing unrestricted host shell.
No claim is made that this identifies the original crash's root cause or prevents
all system-wide ENFILE incidents.

Final validation on October 31, 2026: 23 Node tests passed, including real macOS
numeric-FD and owned-group enumeration; 61 Python tests ran successfully (56 passed,
5 live-server cases skipped in discovery). The five opt-in live permission cases
also passed separately against the disposable v2.2.5 server. Skill/provenance
validation, Python compilation, JavaScript syntax checks, shell syntax and
`git diff --check` passed. Native sampling was run with approved access outside the
execution sandbox after its `sysctl` denial was observed; simulated tests never
triggered actual ENFILE or high memory pressure.

The October 31 agent-efficiency update deliberately makes default admission serial on the 8 GiB development host. Parallel-capacity stress tests now request their own explicit test configuration; plugin tests verify serial admission with production defaults. These limits apply per governor, not across independent servers or unrestricted shell descendants. See [agent evaluation](AGENT_EVALUATION.md).
