# Bounded agent evaluation

Shared agents contain general methods. Project-specific execution/recovery lessons
belong in that project's `AGENTS.md`, linked workflow notes and task prompts.
Updating prompts and evaluating behavior is not model-weight training.

## Run a small exercise

Copy a fixture from `tests/agent_evals/` into a disposable directory outside the
starter and application repositories, then `git init -q` that directory. Keep the
output report outside the fixture. The workspace plugin requires Git even for a
read-only task. No Docker setup is needed when that disposable repo has no saved
sandbox configuration. Never point the repair exercise at an owner workspace.

Use the existing connected OpenCode service and configured role/model:

```sh
python3 tests/agent_evals/run_eval.py \
  --directory /absolute/path/to/disposable-fixture \
  --agent coder --prompt tests/agent_evals/repair-prompt.txt \
  --output /absolute/path/to/repair-result.json --timeout 180 --tools 10
```

The runner creates a session with an explicit location, verifies it before sending
the prompt, polls a bounded message page, enforces a deadline/tool-call budget,
interrupts server-side generation on exit, records source fingerprints and stores
only visible text/tool evidence. It excludes internal model metadata. It does not
change agent models, permissions or providers. It is an evaluation utility, not
an application orchestrator or OS sandbox. Operator access to the local OpenCode
CLI/service and configured providers is required. Do not use multiple runners at
once. API calls have separate 20-second deadlines, so timeout/cleanup may extend
the nominal task deadline. Source snapshots cap at 2,000 files/16 MiB and exclude
Git metadata, dependencies and generated test/build directories. Shell descendants
and unrelated sessions remain outside this utility's confinement.

A successful agent turn is not a passing behavioral grade. Inspect its actual
trace, diff and outcomes using the criteria below. Fixtures intentionally include
incorrect code/tests; do not include them in application regression discovery.
Default starter `unittest discover -s tests` does not descend into these directories.
Never install these fixture files into a user application.

## Curriculum and grading

| Exercise | Roles | Required evidence |
| --- | --- | --- |
| `diagnose` | Poseidon, Team Lead, Researcher | Output is intermediate; receipt settlement permits leaving; cite source; preserve pending guard; no edits/execution/delegation |
| `repair` | Coder | Paused regression fails before repair, passes afterward; idle/dirty remains allowed; busy/active/conflict still block; only two scoped files change |
| `review` | Reviewer | Reject unconditional `False` despite a passing paused test; identify missing idle/dirty coverage; no edits/tests; calibrate severity |
| Project audit | Maintainer | Read-only scoped source trace, concrete causal evidence, facts separated from hypotheses; no milestone completion claim |
| Project repair | Coder then Reviewer | Deterministic red/green regression in isolated snapshot; narrow implementation; review source and logs before applying to application |

For `repair`, independently check all 32 combinations of busy/active/conflict/
paused/dirty. Expected result: no blocking flag is set; dirty does not affect
eligibility because the caller saves before submission. Do not accept an agent's
summary in place of those independent checks. Passing these small cases does not
qualify a role for unrestricted tasks or prove long-session resource stability.

## Observed results — October 31, 2026

The original Europa session dispatched parallel planning/research/architecture,
used multiple full browser runs across roles and included background test commands
with timeout zero. Its last recorded failures included DNS/authentication after
restart. This does not establish a root cause for the machine's resource exhaustion.
The 8 GiB host's initial standalone governor report showed NORMAL and 5,863/30,720
system descriptors. That report covered its own process, not another server's
complete workload or Docker VM memory.

- Poseidon diagnosis: three reads; preserved the guard; correct deterministic fix.
- Coder toy repair: 31.59 seconds, eight tool calls, exactly two allowed files;
  one failing regression before repair, six passing tests afterward. Independent
  32-case eligibility matrix passed.
- Reviewer adversarial candidate: 34.81 seconds, four reads, no changes; caught
  unconditional execution blocking and missing positive coverage. It overstated
  severity as Critical; subsequent review instructions explicitly require impact
  calibration. This is a remaining quality caveat, not a functional review pass
  for arbitrary future tasks.
- Maintainer Europa snapshot audit: 41.93 seconds, seven reads, no changes; found
  the pending-receipt notebook-switch gap. A proposed render-boundary execution
  race remains a hypothesis requiring its own discriminating check.
- Coder bounded Europa repair: 67.16 seconds, ten tool calls, two scoped files;
  focused hook tests changed from ten passed/one failed to eleven passed. The
  actual notebook-switch defect was reproduced; the broader race was not patched.

The first CLI-only fixture attempt resolved to the application directory despite
its subprocess cwd; no fixture diagnosis was possible. A second attempt failed
because the fixture was not a Git repo. Neither counts as a behavioral pass/fail.
Explicit session location verification and fixture Git initialization corrected
these harness issues before the scored runs.

Configuration now admits one agent and one heavy tool/shell at a time per governor,
with four queued jobs, one delegation level and a 15-minute cooperative timeout.
Worker delegation denials and existing models/permissions are preserved.
`subagent_depth` was removed because OpenCode v2.2.5 logs it as unsupported;
resource governance and worker policies provide the actual controls. Existing
servers may retain imported defaults until restarted; file edits alone are not
proof that a running server adopted the new limits. No broad service restart was
performed while evaluation workers were active.

Governor/plugin checks: 24 passed after correcting test fixtures to request
explicit parallel stress capacity instead of assuming production defaults.
The initial run failed on those assumptions and left pending simulated tasks;
only that identified owned Node run was terminated. Tests now verify serial
production admission while retaining parallel-capacity coverage.
Final Python discovery: 64 tests ran, 59 passed and five opt-in live-server cases skipped. Three additional mocked runner tests verify location mismatch, deadline interruption and waiting for a new idle outcome when reusing a session.
Skipped cases were not live permission validation in this run. Skill/provenance
validation, shell syntax and diff whitespace checks passed. No long-duration,
full browser/Docker, crash-recovery or machine-wide resource guarantee is claimed.
There is no controlled before/after model-performance benchmark.

## Follow-up evidence

The Team Lead passed the local planning exercise in 11 seconds with three reads.
Researcher returned the correct cause in 17.66 seconds/five reads, but its proposed
regression only asserted a flag. First feedback corrected the causal gap; a second
correction fixed its nonexistent module-level unittest API. It then produced a
runnable standard-library test, independently executed with exit 0. The shared
Researcher instructions now require assertions on the actual action, both rejected
and allowed behavior, and a distinction between pseudocode and runnable code.
This role needs review of test proposals; it did not pass the full exercise on its
first attempt.

The real repair review reached its 120-second deadline after five reads without a
verdict and was interrupted. A narrower follow-up reused that exact session and
required no more tools; it returned no blocking finding in 26.04 seconds. The first
follow-up attempt exposed a runner bug: it read the prior interrupted outcome too
early. The corrected supervisor waits for a newly recorded idle timestamp, covered
by the new mocked regression. These failed attempts are not counted as approvals.

After all evaluation work was idle, `opencode reload` succeeded. A new live
Poseidon status call actually reported maxAgents=1, maxTools=1 and maxDepth=1.
One native Poseidon-to-Maintainer delegation then passed in 30.52 seconds with
three coordinator tool calls and no changes. This verifies the loaded limits in
that tested location, not every independent server or arbitrary shell descendant.

The reviewed one-line pending-switch repair and its regression were then applied
to Europa's preserved working tree. Node 24.19 passed all 43 frontend tests and the
production TypeScript/Vite build. A command environment that selected Node 20.17
failed to start seven jsdom test files (ERR_REQUIRE_ESM); explicit runtime selection
resolved that mismatch without changing dependencies or permissions. Complete
Chrome/Python application/Go milestone validation was not run in this training
checkpoint, so Phase 3F-D remains incomplete and uncommitted.

## Vision and GTD exercises (November 1, 2026)

Copy `tests/agent_evals/vision/` to a disposable Git repository and install the
current `.opencode` bundle there. Do not run these against an application or swap
model providers. Use the existing runner with the prompt files below; keep JSON
reports outside the fixture. Run sequentially. The first-turn Poseidon exercise
uses plain-text questions so an unattended run does not stall at interactive UI.
Use fresh sessions for independent cases; a successful process exit alone is not
a behavioral pass.

| Prompt | Role | Passing observations |
| --- | --- | --- |
| `vision-prompt.txt` | Poseidon | Loads `grilling`, reads the actual site, asks no more than three material questions about intent/references; no settled aesthetic or implementation, no source changes |
| `vision-research-prompt.txt` | Researcher | Loads `grilling`, cites local facts, separates unknowns and proposals, returns at most three questions through Poseidon; no final design tokens, code, edits, shell, user contact or delegation |
| `vision-correction-prompt.txt` | Poseidon/Researcher | Keeps the confirmed journal purpose, white/green/Georgia, no commerce/dark theme/animation; acknowledges correction and scopes only hierarchy/mobile spacing; does not repeat settled questions |
| `vision-delegated-prompt.txt` | Poseidon/Researcher | Honors explicit creative delegation within the supplied bounds; does not request a second approval, invent features or replace protected content/colors/navigation |
| `vision-gtd-prompt.txt` | Poseidon | Loads `gtd` and natural-planning reference; produces outcome and concrete next action/owner; photographs in Waiting For without invented deadline; newsletter deferred; preserves accepted visual direction; no external action or edits |

Check file fingerprints and tool traces as well as answers. These are behavioral
exercises and grading criteria, not automated proof that prompts enforce a runtime
approval lock, and do not establish broad design quality or long-session behavior.

Observed first-turn Poseidon result: 28.39 seconds, eight tools; loaded `grilling`
and `karpathy-guidelines`, read README and HTML, asked three questions about purpose,
the meaning of premium and references, and changed no files. No design direction
was silently selected. This exercise ran in a disposable installed bundle; it did
not reload or migrate the user's existing installations.

Initial Researcher discovery attempt was interrupted after 82.62 seconds when it
exceeded its eight-tool budget (nine calls). It loaded `grilling`, read the relevant
README/HTML and changed no files, but also loaded frontend-design early and reread
source without returning a handoff. This is not a behavioral pass. Its instructions
now count skill loads in the budget, defer design methodology until a direction is
agreed unless needed for a specific question, and stop discovery once enough facts
exist to ask the user. Any subsequent result is recorded separately.

Poseidon's GTD exercise completed in 28.32 seconds/seven tools. It loaded `gtd`,
`karpathy-guidelines` and `references/04-natural-planning.md`; preserved the confirmed
journal outcome, returned a concrete mobile-inspection action with an owner, dated
Waiting For without inventing a photo deadline, and deferred the newsletter. Its
trace contains no edit or external-action tool; the HTML fingerprint stayed equal.
The report also records an operator-made Researcher definition update during that
run, so this result is not presented as an unchanged-fixture fingerprint pass.
Future comparisons must keep the entire disposable bundle frozen during a run.

A second Researcher attempt in the same disposable project also exceeded eight
tools (nine calls, 39.72 seconds), returned no handoff and changed no files. It
searched for grading documentation mentioned by the fixture README and loaded
frontend-design before vision confirmation. Cached configuration was not ruled
out. The fixture's dangling grading-document reference was removed, and the
research brief now names its complete two-file source scope, matching the agent
brief protocol. The final check uses a new disposable project with a frozen current
bundle. The earlier attempts remain failures, not evidence of reliable behavior.

The fresh, explicitly scoped Researcher exercise completed in 66.50 seconds with
seven recorded tools and no changed files. It loaded `grilling`, read the two named
files, returned three questions about vision/references/audience through Poseidon,
and deferred implementation until answers. This verifies skill access and the
basic discovery handoff on that fixture. It is a partial behavioral pass: the
handoff exceeded 300 words, still loaded frontend-design before confirmation,
miscounted its calls, and described subjective non-premium quality as a fact. Its
claims that style alternatives are mutually exclusive and that source had no
hierarchy were unsupported. Researcher instructions now explicitly reject those
claims and require honoring the handoff limit; Poseidon must screen findings for
agent taste masquerading as source facts. These final wording corrections were
statically validated but not rerun against a model. The correction and explicit
creative-delegation exercises are provided for further evaluation, not claimed as
live passes. This model still requires scoped briefs and coordinator review.
