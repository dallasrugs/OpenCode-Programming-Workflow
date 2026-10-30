# Install — human-writing skill for Claude Code

Three ways. Pick one.

The distributed file is `human-writing.skill` — that's just a zip archive with a `.skill` extension (the convention used by agentskills.io and Anthropic's skill ecosystem). If your OS doesn't recognize the extension, either rename it to `.zip` or point your unzip tool at it directly — the commands below do.

---

## Option 1 — macOS / Linux (fastest)

Open a terminal and paste this:

```bash
mkdir -p ~/.claude/skills && unzip -o ~/Downloads/human-writing.skill -d ~/.claude/skills/
```

Adjust the path if you downloaded the file somewhere other than `~/Downloads`.

Then restart your Claude Code session. Done.

---

## Option 2 — Windows

1. Open File Explorer
2. Type `%USERPROFILE%\.claude\skills` in the address bar and press Enter
   - If the `.claude\skills` folder doesn't exist, create it
3. Either rename `human-writing.skill` → `human-writing.zip`, or right-click it → Open With → 7-Zip / WinRAR / File Explorer
4. Extract into the `.claude\skills` folder
5. Confirm the result looks like:

   ```
   C:\Users\<you>\.claude\skills\human-writing\SKILL.md
   C:\Users\<you>\.claude\skills\human-writing\references\...
   ```

   Not nested an extra level deep. If it is, move the inner `human-writing` folder up one.
6. Restart Claude Code.

---

## Option 3 — Project-scoped (skill only active in one repo)

Pick project-scoped when the whole team should get the skill automatically via `git pull`. Pick user-scoped (Options 1 or 2) when it's for your personal workflow across all projects.

```bash
cd /path/to/your/project
mkdir -p .claude/skills && unzip -o ~/Downloads/human-writing.skill -d .claude/skills/
```

Then commit `.claude/skills/human-writing/` if you want the whole team to get it.

---

## Verify it worked

Start a new Claude Code session and check two things.

**1. Files are in place:**

```bash
ls ~/.claude/skills/human-writing/
```

You should see:

```
SKILL.md
references/
```

**2. Claude Code registered the skill.** Ask Claude "what skills do you have available?" (or run `/skills` if your version supports it). Confirm `human-writing` appears in the list. If the files are there but the skill doesn't show up, the most common cause is a folder-nesting problem — see "Common install mistakes" below.

Once it's loaded, invoke it explicitly with:

```
/human-writing rewrite this: <paste AI text>
```

Or just paste AI-sounding text and ask "make this sound human" — Claude Code should auto-load the skill based on the trigger phrases in the description.

---

## Common install mistakes

- **Double-nested folder.** If you see `~/.claude/skills/human-writing/human-writing/SKILL.md`, move the inner folder up one level.
- **Wrong directory.** Skills go in `~/.claude/skills/`, not `~/.claude/` directly and not `~/.claude/commands/`.
- **Forgot to restart.** Claude Code only scans skills at session start. New terminal, new session.
- **`.skill` extension not recognized.** Rename to `.zip` or use a tool that doesn't care about the extension (7-Zip on Windows, `unzip` on macOS/Linux).

---

## Alternative distribution

- **agentskills.io** — the canonical skill registry. If this skill is published there, you can install via its standard tooling instead of the manual zip extract above.
- **Claude Code plugins** — skills can ship inside a plugin for unified install of multiple skills at once. Out of scope for a single-file skill, but worth knowing if you're building a suite.

---

## Uninstall

```bash
rm -rf ~/.claude/skills/human-writing
```

Or rename to disable temporarily:

```bash
mv ~/.claude/skills/human-writing ~/.claude/skills/_human-writing
```
