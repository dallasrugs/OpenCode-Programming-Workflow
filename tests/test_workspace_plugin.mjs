import { test } from "node:test"
import assert from "node:assert/strict"
import plugin from "../.opencode/plugins/poseidon-workspace/index.js"
import { createHash } from "node:crypto"
import { mkdtemp, readFile, rm, access, mkdir, writeFile, readdir } from "node:fs/promises"
import { tmpdir } from "node:os"
import path from "node:path"
import { execFileSync, execFile } from "node:child_process"
import { promisify } from "node:util"
import { setTimeout } from "node:timers/promises"

async function fixture(prefix = "poseidon-native-") {
  const directory = await mkdtemp(path.join(tmpdir(), prefix))
  execFileSync("git", ["init", "-q", directory])
  const hooks = new Map(), commands = new Map(), prompts = [], queue = []
  let tool, stopped = false
  const cleanup = await plugin.setup({
    location: { directory },
    session: {
      get: async ({ sessionID }) => ({ data: { id: sessionID, ...(sessionID === "child" ? { parentID: "parent" } : {}) } }),
      hook: async (name, handler) => hooks.set(name, handler),
      synthetic: async (value) => { assert.equal(value.resume, false) },
      prompt: async (value) => { prompts.push(value) },
    },
    command: { transform: async (register) => register({ add: (command) => commands.set(command.name, command) }) },
    tool: { transform: async (register) => register({ add: (definition) => { tool = definition } }) },
    event: { async *subscribe({ signal }) {
      while (!signal.aborted) {
        if (queue.length) yield queue.shift()
        else await setTimeout(10)
      }
      stopped = true
    } },
  })
  const marker = (id) => path.join(directory, ".git/bdfl/sessions", createHash("sha256").update(JSON.stringify(id)).digest("hex").slice(0, 24), "ended")
  const waitForMarker = async (id) => {
    for (let attempt = 0; attempt < 200; attempt++) {
      try { await access(marker(id)); return } catch { await setTimeout(10) }
    }
    assert.fail("Cleanup did not complete: " + id)
  }
  return { directory, hooks, commands, tool, prompts, queue, marker, waitForMarker, async cleanup() {
    cleanup()
    for (let attempt = 0; !stopped && attempt < 50; attempt++) await setTimeout(10)
    await rm(directory, { recursive: true, force: true })
  } }
}

test("workspace tool uses native permissions and root session ownership, without custom authorization or controller submission", async () => {
  const f = await fixture()
  try {
    assert.equal(f.tool.name, "poseidon_workspace")
    assert.equal(f.tool.options.permission, "poseidon_workspace")
    assert.equal(f.tool.options.codemode, false)
    assert.deepEqual(f.tool.input.properties.action.enum, ["settings", "configure", "test", "status", "end_sandbox"])
    const result = await f.tool.execute({ action: "settings" }, { sessionID: "child" })
    const settings = JSON.parse(result.content)
    assert.equal(settings.settings, null)
    assert.ok(settings.tests_template.commands.length)
    await assert.rejects(access(path.join(f.directory, ".git/bdfl/runs")))
  } finally { await f.cleanup() }
})

test("delegated agents share the user sandbox; deleting a child does not end its parent", async () => {
  const f = await fixture()
  try {
    await f.hooks.get("prompt")({ sessionID: "parent" })
    const operations = path.join(f.directory, ".git/bdfl/operations")
    const count = (await readdir(operations)).length
    await f.hooks.get("prompt")({ sessionID: "child" })
    assert.equal((await readdir(operations)).length, count)
    const context = { sessionID: "child", system: [] }
    await f.hooks.get("context")(context)
    assert.match(context.system[0].text, /needs_configuration/)
    f.queue.push({ type: "session.deleted", data: { sessionID: "child" } })
    await f.waitForMarker("child")
    await assert.rejects(access(f.marker("parent")))
    f.queue.push({ type: "session.archived", data: { sessionID: "parent" } })
    await f.waitForMarker("parent")
    await f.commands.get("poseidon-end").execute({ sessionID: "child" })
  } finally { await f.cleanup() }
})

test("log command follows native operation output with quoted paths and rejects shell injection", async () => {
  const f = await fixture("poseidon-'logs-")
  try {
    const id = "a".repeat(32)
    const directory = path.join(f.directory, ".git/bdfl/operations", id)
    await mkdir(directory, { recursive: true })
    await writeFile(path.join(directory, "state.json"), JSON.stringify({ finished: true, failed: false }))
    await writeFile(path.join(directory, "output.log"), "NATIVE_LOG_MARKER\n")
    await f.commands.get("poseidon-logs").execute({ sessionID: "child", prompt: { text: id } })
    const viewer = f.prompts.at(-1)
    assert.equal(viewer.sessionID, "parent")
    const output = await promisify(execFile)("/bin/sh", ["-c", viewer.text.split("\n").at(-1)])
    assert.match(output.stdout, /NATIVE_LOG_MARKER/)
    await assert.rejects(f.commands.get("poseidon-logs").execute({ sessionID: "parent", prompt: { text: id + "; echo injected" } }), /Invalid log ID/)
  } finally { await f.cleanup() }
})
