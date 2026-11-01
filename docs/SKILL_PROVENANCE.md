# Current role integration — November 1, 2026

The historical catalog/restoration notes below are retained. Current role assignments live in skills/SOURCES.json: Team Lead coordinates, Poseidon owns design and can load frontend-design/grilling/documented interview/GTD, Researcher can load only task-approved karpathy-guidelines. Imported skill bodies, support files and licenses were compared with the pre-assignment hashes and are unchanged. Microsoft and five K-Dense workflows were studied as references; no new collection/scripts/providers were installed. [Agent contracts](AGENT_CONTRACTS.md) supersede older role/delegation descriptions below.

# Skill provenance and native OpenCode integration

The role matrix includes Poseidon plus five native worker agents. Agent Markdown
files define capabilities; the README describes the current workflow. Upstream
source hashes, licenses and imported bodies are unchanged.

Audit date: October 30, 2026. Development CLI: **OpenCode v2.2.3**.

All 17 pre-restoration skills were inspected along with the three local history
commits, their attribution statements, the cited upstream repositories and relevant
upstream history. The initial engineering files entered at
`0872f9a8e739730b99a1ccb657b61a7b8afefbbc`; the writing/SEO/commerce files entered at
`2998647261d058ce324b810810929abe110ea54d`. Those commits contain adaptations, not
pinned original sources. There is no historical upstream lockfile from which to
recover the authors' exact revisions at adaptation time.

The evidence establishes **named source identities**, not an undocumented history
of exactly which paragraphs were copied. Explicitly named composite sources are
restored separately; their procedures are never merged into a new synthetic skill.
Repository-level inspirations without a unique file are not treated as proof.
Current author-maintained source is pinned at the inspected Git commits below.

11 old skill entries now resolve to 16 original native skills. Two additional
original skills (`codebase-design` and `superpowers-test-driven-development`) are
included because restored skills explicitly depend on them. Six existing local
adaptations remain byte-for-byte unchanged and carry `SOURCE_UNVERIFIED` status.
That restoration produced **24 IDs**, including **18 verified upstream imports**.
The subsequent original frontend-design import brings the current catalog to
**25 IDs / 19 verified imports**; see its Apache-2.0 record below. All pre-restoration
inputs are archived outside discovery.

## Audit of every existing skill

| Previous local ID | Outcome / native originals | Evidence or blocker |
|---|---|---|
| `code-quality` | `SOURCE_UNVERIFIED`; preserved unchanged | The header names Uncle Bob’s UB Mode, but no redistribution license exists in the inspected master history. Preserve the local adaptation; do not import UB Mode. |
| `codebase-understanding` | `how` | Explicit named-source attribution; pinned original(s) and MIT notice verified. |
| `completion-audit` | `code-review`, `verification-before-completion` | Explicit named-source attribution; pinned original(s) and MIT notice verified. The wildwasser component traces to Jesse Vincent through the import commit and matching Git blobs. |
| `domain-modeling` | `domain-modeling` | Explicit named-source attribution; pinned original(s) and MIT notice verified. |
| `ecommerce-brand-voice` | `SOURCE_UNVERIFIED`; preserved unchanged | Only a repository-level inspiration is named; ecommerce-brand-guide is a candidate, not a verified file-level derivation. No license file exists at the inspected revision. |
| `ecommerce-copywriting` | `SOURCE_UNVERIFIED`; preserved unchanged | A matching named skill exists in the cited repository, but redistribution permission is unverified. No license file exists at the inspected revision. Preserve the local adaptation. |
| `ecommerce-product-pages` | `SOURCE_UNVERIFIED`; preserved unchanged | Composite repository-level inspirations do not identify a unique original file. The eCommerce source lacks a license; do not substitute seo-ecommerce or ecommerce-pdp based on name/function. |
| `milestone-coordination` | `SOURCE_UNVERIFIED`; preserved unchanged | The header identifies subagent-driven-development plus unspecified Matt Pocock implementation workflows. A unique original for the combined skill cannot be established; preserve the composite. |
| `natural-writing` | `humanizer`, `human-writing` | Explicit named-source attribution; pinned original(s) and MIT notice verified. |
| `requirements-grilling` | `grilling`, `grill-with-docs` | Explicit named-source attribution; pinned original(s) and MIT notice verified. |
| `seo-content` | `seo-content` | Explicit named-source attribution; pinned original(s) and MIT notice verified. |
| `seo-technical` | `seo-technical` | Explicit named-source attribution; pinned original(s) and MIT notice verified. |
| `specification-design` | `to-spec`, `writing-plans` | Explicit named-source attribution; pinned original(s) and MIT notice verified. The wildwasser component traces to Jesse Vincent through the import commit and matching Git blobs. |
| `systematic-debugging` | `systematic-debugging`, `diagnosing-bugs` | Explicit named-source attribution; pinned original(s) and MIT notice verified. The wildwasser component traces to Jesse Vincent through the import commit and matching Git blobs. |
| `task-decomposition` | `to-tickets` | Explicit named-source attribution; pinned original(s) and MIT notice verified. |
| `test-driven-development` | `tdd` | Explicit named-source attribution; pinned original(s) and MIT notice verified. |
| `verification` | `SOURCE_UNVERIFIED`; preserved unchanged | The header names verification-before-completion but identifies no author/repository for this file. Related completion-audit attribution is corroborating context, not proof of a unique source. The verified Jesse Vincent skill is separately restored through completion-audit. |

`SOURCE_UNVERIFIED` means the restoration gate is unresolved; reasons distinguish
ambiguous provenance from identified source with unclear redistribution permission.
For example, UB Mode's source exists, but its inspected history has no license.
The eCommerce repository likewise has no license file at the inspected revision;
a README heading alone does not supply the missing notice/terms. No upstream text
from those repositories was imported. Their existing local adaptations remain
provisional, not re-certified as original or cleared for redistribution.

`verification` names a methodology without identifying an author in that file.
We preserve it rather than guessing. The separate, verified
`verification-before-completion` import is established through the explicit
`completion-audit` attribution. `milestone-coordination` mixes a named wildwasser
skill with unspecified Matt Pocock implementation workflows; no unique original
for that combination is asserted. Alireza Rezvani's repository is broadly credited
in the old root attribution, but no local entry establishes a unique original
Alireza skill. Its MIT license is verified; no replacement is invented from it.

## Original authors and pinned sources

All imports below carry their original MIT copyright and permission notice in the
native directory and in the preserved snapshot. Full per-file upstream paths,
original Git modes and SHA-256 hashes are recorded in `skills/SOURCES.json`.

| Native ID | Original author | Immutable source |
|---|---|---|
| `how` | Lauren Tan | [skills/how/SKILL.md](https://github.com/poteto/how/blob/b1ef42969ea7a2bb50aa26c2480274828a0385e7/skills/how/SKILL.md) |
| `domain-modeling` | Matt Pocock | [skills/engineering/domain-modeling/SKILL.md](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/domain-modeling/SKILL.md) |
| `tdd` | Matt Pocock | [skills/engineering/tdd/SKILL.md](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/tdd/SKILL.md) |
| `codebase-design` | Matt Pocock | [skills/engineering/codebase-design/SKILL.md](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/codebase-design/SKILL.md) |
| `grilling` | Matt Pocock | [skills/productivity/grilling/SKILL.md](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/productivity/grilling/SKILL.md) |
| `grill-with-docs` | Matt Pocock | [skills/engineering/grill-with-docs/SKILL.md](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/grill-with-docs/SKILL.md) |
| `to-spec` | Matt Pocock | [skills/engineering/to-spec/SKILL.md](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/to-spec/SKILL.md) |
| `to-tickets` | Matt Pocock | [skills/engineering/to-tickets/SKILL.md](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/to-tickets/SKILL.md) |
| `code-review` | Matt Pocock | [skills/engineering/code-review/SKILL.md](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/code-review/SKILL.md) |
| `diagnosing-bugs` | Matt Pocock | [skills/engineering/diagnosing-bugs/SKILL.md](https://github.com/mattpocock/skills/blob/a496f5513d4a4cf889bc48e189e579f4b0bdf6aa/skills/engineering/diagnosing-bugs/SKILL.md) |
| `systematic-debugging` | Jesse Vincent | [skills/systematic-debugging/SKILL.md](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/systematic-debugging/SKILL.md) |
| `verification-before-completion` | Jesse Vincent | [skills/verification-before-completion/SKILL.md](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/verification-before-completion/SKILL.md) |
| `writing-plans` | Jesse Vincent | [skills/writing-plans/SKILL.md](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/writing-plans/SKILL.md) |
| `superpowers-test-driven-development` | Jesse Vincent | [skills/test-driven-development/SKILL.md](https://github.com/obra/superpowers/blob/2ce8aa15d05bd57213e6f746f953aafb7ded7a8b/skills/test-driven-development/SKILL.md) |
| `humanizer` | Siqi Chen | [SKILL.md](https://github.com/blader/humanizer/blob/0ef9fe5bc3572734fd3ae6c448fe00a30cd5dcf0/SKILL.md) |
| `human-writing` | amineall | [human-writing/SKILL.md](https://github.com/amineall/human-writing-skills/blob/dba7f72f2d45ab53bf5b8466219d75e8fa8e7b89/human-writing/SKILL.md) |
| `seo-content` | AgriciDaniel | [skills/seo-content/SKILL.md](https://github.com/AgriciDaniel/claude-seo/blob/6be93f45064ffbadced572b5d5c95f55fd263af0/skills/seo-content/SKILL.md) |
| `seo-technical` | AgriciDaniel | [skills/seo-technical/SKILL.md](https://github.com/AgriciDaniel/claude-seo/blob/6be93f45064ffbadced572b5d5c95f55fd263af0/skills/seo-technical/SKILL.md) |

The original-author chain for the Superpowers material is not a name-based guess:
wildwasser's commit `96bd036cb468deade32a496aabf20cbca025c489` explicitly names
`obra/superpowers`. Its skill blobs also occur in that repository's history. The
manifest records the matching blob IDs and historical commits. The imported
revisions come directly from Jesse Vincent's licensed original repository rather
than treating wildwasser's unverified root license as sufficient.

## Exact source and compatibility changes

The **16 non-SEO skill bodies are byte-identical to their pinned originals**.
Both SEO skills have only the documented path substitution
`${CLAUDE_PLUGIN_ROOT}` → `.opencode/skill-resources/claude-seo`; no procedure,
example, warning, scoring rule or conceptual step is rewritten. Exact replacement
counts and reasons live in the two JSON patches. All other imported supporting
file contents are unchanged.

`superpowers-test-driven-development` uses a namespaced directory ID so Jesse
Vincent's dependency cannot be mistaken for the former Matt Pocock-derived
`test-driven-development` alias. Its upstream display name and body are unchanged;
Matt's original is independently available as `tdd`. The two TDD methodologies
remain distinct. Namespaced references map only to the actual author's native
skill, never to the other author's similarly named procedure.

Upstream program files are installed with mode **0644** and are not enabled.
Original Git modes and every such local mode change are recorded in the manifest.
`SCRIPT_INSPECTION.json` is a static inventory of imports, operation indicators and
source hashes at restoration time. It is not an authorization or complete security
audit. Dependency metadata (including the SEO requirements/lockfile) is preserved;
no dependencies, hooks, installers, browser tools or upstream programs were run.
The SEO launcher can create a managed environment and install packages: it remains
inert. Future source updates list changed scripts for renewed inspection.

The patched SEO resource root remains project-relative. Project-local installations
include those resources. With a global-only installation, use an explicit global
resource path or install into the project when a skill expects project-local
supporting files. The removed controller no longer creates source mirrors for
agent conversations. Readable global references are limited by native permissions.

The copied `agents/openai.yaml` files are inert upstream harness metadata inside
skills, not new OpenCode agents. Source snapshots and legacy inputs live outside
`.opencode/skills`, so OpenCode cannot discover duplicate snapshots as live skills.

```text
.opencode/
  skills/SOURCES.json                       # authoritative audit, pins, hashes, roles
  skills/<native-id>/SKILL.md               # native, lazy-loaded author instructions
  skills/<native-id>/LICENSE                # original MIT notice
  skills/<native-id>/<original-support>     # references/templates/examples
  skill-sources/upstream/<id>/              # unmodified source bytes
  skill-sources/legacy/<previous-id>/        # all 17 exact pre-restoration inputs
  skill-sources/patches/<id>.json            # minimal compatibility replacements
  skill-sources/SCRIPT_INSPECTION.json       # static, source-only inspection record
  skill-resources/claude-seo/                # original shared tree and inert programs
  runtime/skillctl.py                    # local validator / updater
```

## Native execution and role assignment

November 1, 2026: Poseidon and Researcher now load the existing, unchanged Matt
Pocock `grilling` skill proactively for material product/design ambiguity. User
phrases “grill me”, “grill-me” and “grill” route to this native ID; no duplicate
skill is invented. Both roles also have `grill-with-docs` (explicit requests only)
and its `domain-modeling` dependency. Researcher drafts questions and documentation
through Poseidon, with no write/question-tool/delegation grant. Role definitions
limit rounds to three material questions, reuse answers and honor explicit user
delegation. Imported source bodies, hashes and manual-invocation flags are intact.

Poseidon alone can load `gtd`, imported byte-for-byte from
[zrwang/gtd](https://github.com/zrwang/gtd/tree/e192366199ba543505ff8d5caf88d31c40a4ae90)
at commit `e192366199ba543505ff8d5caf88d31c40a4ae90`. The root skill, README,
LICENSE, `.gitignore` and all nine references are retained and hashed in
`skills/SOURCES.json` with matching source snapshots. Root-level update selectors
preserve reference paths. Zerui Wang's MIT license includes a separate copyright
caveat for David Allen excerpts; that full notice is retained. No book PDF is
bundled or required; the skill's `books/...pdf` string is an upstream source
citation. The user's language and confirmed vision take precedence over the
skill author's personal defaults. GTD grants no new authority for external actions.

Skills load through OpenCode's native skill tool. Their source text and licenses
remain unchanged; loading a skill does not grant additional permissions. Manual-only
invocation flags remain intact. OpenCode is responsible for the full YAML parser;
the local validator checks the discovery fields used by the pinned sources.

The six agent definitions and `skills/SOURCES.json` contain matching allowlists:

| Agent | Skill responsibilities |
|---|---|
| Poseidon | Coordination, planning and verification |
| Team Lead | Requirements, decomposition and content planning |
| Maintainer | Architecture, compatibility and code review |
| Researcher | Read-only source/web research; frontend-design methodology for UI specifications |
| Coder | Implementation, TDD, debugging and code/content quality |
| Reviewer | Independent review, test strategy and verification |

Poseidon delegates to the five worker agents. Worker agents do not recursively delegate.
Coder uses native edit/shell tools. Reviewer has native shell access for inspection and tests, while its instructions
prohibit application source edits. It can also run the configured sandbox tests. A skill requiring unsupported delegation,
external publication or other unavailable tools must report that limitation; an
agent must not claim to have completed those steps.

## Validate and inspect

```sh
python3 .opencode/runtime/skillctl.py validate
python3 -m unittest discover -s tests -v
node --test tests/test_workspace_plugin.mjs
```

Validation checks source hashes, original inputs, licenses, patch application,
resource references, native discovery fields and role allowlists. It does not invoke
models or execute imported programs. The removed live controller verifier and its
historical output are not part of the native workflow.

## Safe updates

```sh
# Read-only HTTPS Git inspection; produces a diff and report, changes no installed files.
python3 .opencode/runtime/skillctl.py check tdd --ref main --report /tmp/tdd-update.json
# Read the full diff, pins, changed-program list and any blockedReasons in that report.
python3 .opencode/runtime/skillctl.py apply /tmp/tdd-update.json --reviewed REPORT_SHA256
```

The displayed fingerprint binds application to the exact reviewed report. Updating
one skill checks all imported units from that repository together, keeping shared
resources and license copies pinned consistently. The utility fetches only public
canonical GitHub HTTPS sources into temporary bare Git repositories. No checkout,
hooks, filters, installers or upstream programs execute. New supporting files are
detected, regular-file modes are checked and symlinks/submodules are rejected.

Application refuses unknown local additions, deletions or edits, changed source
snapshots, changed compatibility patches, a changed manifest, license/notice
changes or replacement-count conflicts. A changed license needs separate review
and an explicit provenance revision; a report flag cannot bypass the apply-time
license check. Source patches are preserved, not regenerated with an LLM. The
proposed complete bundle is validated before writes; a lock serializes application
and caught write failures restore already-applied files without discarding detected
concurrent user edits. Imported programs remain non-executable. A crash/power loss
can leave a lock or partial transaction: restore from Git/backup and validate before
continuing; the updater does not claim filesystem-wide atomicity across power loss.

Save intentional local work separately before synchronizing. For a compatibility
patch that genuinely needs rebasing, inspect the new raw snapshot, edit only the
necessary literal replacement with a reason and exact count, materialize the
corresponding native file, update its snapshot/installed/patch hashes and pin, then
run the full validator and tests. Do not simply change a hash to conceal a body
rewrite. Preserve a diff against the author source for review.

## Add a verified source

1. Find an authoritative source and corroborate its relationship to the local
   skill; do not infer authorship from a name match. If uncertain, preserve and
   record `SOURCE_UNVERIFIED` instead of importing.
2. Resolve an immutable Git commit, inspect applicable license and notices, and
   retrieve the exact skill directory plus necessary dependencies without executing
   programs. Copy original notices and retain file-level source paths/modes/hashes.
3. Keep an unmodified snapshot outside discovery, place the native skill under its
   author's stable ID (document unavoidable naming collisions), and record any
   minimal literal compatibility patch separately. Never regenerate the body.
4. Add a manifest entry, selectors, role grants, missing-capability notes and any
   justified project-link exceptions. Source bytes and installed bytes must match
   after applying only that patch.
5. Update attribution, test the complete recursive installer inventory, validate,
   and perform native skill-loading probes. Upstream program execution is a separate
   decision requiring dependency, permission and license review.

Both installers carry complete skills, support trees, notices, source snapshots,
patches and runtime utilities while preserving existing files. For an existing
installation, back up and inspect obsolete adapted directories before removing
them; the installer never deletes user files or silently merges local changes.
Old Task #1 runs should be restarted because the canonical skill IDs and catalog
have changed. No commits, pushes or deployments were made by the restoration.

## Approved Apache-2.0 frontend-design import

Added October 30, 2026 from the original [Anthropic skill directory](https://github.com/anthropics/skills/tree/ca45fc496a3436251f191354091d557da31c15b5/skills/frontend-design),
pinned at **`ca45fc496a3436251f191354091d557da31c15b5`**. This adds one verified
native ID to the earlier restoration: **25 native skills, 19 verified imports,
6 unchanged unverified adaptations, 173 imported files including shared resources**.
The original methodology is not rewritten or compatibility-patched.

`SKILL.md`, original `LICENSE.txt` (Apache License 2.0) and repository
`THIRD_PARTY_NOTICES.md` are copied byte-for-byte to both
`skill-sources/upstream/frontend-design/` and `skills/frontend-design/`.
The complete root third-party notice is retained conservatively; this import
contains no third-party programs, fonts or dependencies from those notices.
Each path, immutable SHA, file hash and installed hash/mode is recorded in SOURCES.
The author frontmatter's relative `LICENSE.txt` link remains valid.

The validator permits Apache-2.0 only for the explicitly approved
`frontend-design` identity at `https://github.com/anthropics/skills`, source path
`skills/frontend-design`, and original license path. It additionally pins the
approved Apache license's exact SHA-256 in validator code. Existing imports
still require MIT and their original notices; unknown licenses/sources fail
closed. Snapshot/installed equality, hashes, complete file inventory and sync-time
license-change blocking apply unchanged. The selector preserves LICENSE.txt
rather than renaming it to LICENSE during future synchronization. License or
notice changes require separate review, not a bypass flag.

Researcher alone has native `skill:frontend-design allow`. Other roles receive
the bounded handoff and retain their existing skill allowlists. The native skill
loader supplies the document on demand; it is not injected into every agent.
Build/code instructions in the original are advisory methodology and confer no
editing, shell, screenshot or delegation permission. Researcher's tool restrictions
and the application brief take precedence. The updated development CLI used to
verify discovery, skill loading and permissions is **OpenCode v2.2.4**.

## Karpathy guidelines (November 1, 2026)

All six agents load `karpathy-guidelines` before substantive coding, planning, research or review work, within existing authority, role, test ownership and work limits. Project and global installations include the skill and narrowly scoped global read permissions.

Imported unchanged from `multica-ai/andrej-karpathy-skills` at commit `2c606141936f1eeef17fa3043a72095b4765b9c2`. The skill and source snapshot are byte-identical. Upstream declares MIT in the skill frontmatter and [README](https://github.com/multica-ai/andrej-karpathy-skills/blob/2c606141936f1eeef17fa3043a72095b4765b9c2/README.md#license), without a separate LICENSE file; none has been invented. The validator accepts only this exact source hash and declaration for this import; source updates require review of that exception.
