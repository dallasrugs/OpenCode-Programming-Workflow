import { spawn } from "node:child_process"
import { fileURLToPath } from "node:url"
import { randomUUID } from "node:crypto"

const bridge = fileURLToPath(new URL("../../runtime/workspace.py", import.meta.url))

export default {
  id: "poseidon-workspace",
  async setup(ctx) {
    const quote = (value) => "'" + value.replaceAll("'", process.platform === "win32" ? "''" : "'\\''") + "'"
    const rootSession = async (sessionID) => {
      const seen = new Set()
      while (!seen.has(sessionID) && seen.size < 32) {
        seen.add(sessionID)
        const response = await ctx.session.get({ sessionID })
        const session = response.data ?? response
        if (!session.parentID) return sessionID
        sessionID = session.parentID
      }
      throw new Error("Cannot resolve the owning OpenCode session")
    }
    const logCommand = (identifier) => {
      if (!/^[a-f0-9]{32}$/.test(identifier)) throw new Error("Invalid log ID")
      // Fixed read-only command: never accepts arbitrary shell input or starts implementation.
      return ["python3", "-u", quote(bridge), "--repo", quote(ctx.location.directory), "follow-operation", identifier].join(" ")
    }
    const invoke = (input, signal, progress) => {
      const recorded = ["session_start", "configure", "test"].includes(input.action)
      const payload = recorded ? { ...input, operation_id: randomUUID().replaceAll("-", "") } : input
      return new Promise((resolve, reject) => {
        const child = spawn("python3", ["-u", bridge, "--repo", ctx.location.directory, "call"], {
          stdio: ["pipe", "pipe", "pipe"], signal,
        })
        let stdout = "", stderr = ""
        child.stdout.on("data", (chunk) => { stdout += chunk })
        let progressQueue = Promise.resolve(), publishing = false, dirty = false
        const publish = () => {
          if (!progress || publishing) return
          publishing = true
          progressQueue = (async () => {
            while (dirty) {
              dirty = false
              await progress({ output: stderr })
            }
          })().catch(() => {}).finally(() => { publishing = false })
        }
        child.stderr.on("data", (chunk) => {
          stderr = (stderr + chunk).slice(-65536)
          dirty = true
          publish()
        })
        child.on("error", reject)
        child.on("close", async (code) => {
          await progressQueue
          code === 0 ? resolve(stdout) : reject(new Error(stdout || stderr || `Workspace operation exited ${code}`))
        })
        child.stdin.on("error", reject)
        child.stdin.end(JSON.stringify(payload))
      })
    }
    const preparation = new Map()
    await ctx.session.hook("prompt", async (event) => {
      const owner = await rootSession(event.sessionID)
      if (owner !== event.sessionID) return // Delegated agents share the parent's sandbox.
      preparation.set(owner, JSON.parse(await invoke({ action: "session_start", session_id: owner })))
    })
    await ctx.session.hook("context", async (event) => {
      const owner = await rootSession(event.sessionID)
      const status = preparation.get(owner)
      if (status) event.system.push({ type: "text", text: "Project sandbox status: " + JSON.stringify(status) + ". Use poseidon_workspace for settings and tests; orchestration uses native agents, not a controller." })
    })
    await ctx.command.transform((editor) => {
      editor.add({
        name: "poseidon-logs",
        description: "Show a saved workspace operation: /poseidon-logs LOG_ID",
        execute: async ({ sessionID, prompt }) => {
          const owner = await rootSession(sessionID)
          const command = logCommand(prompt.text.trim())
          await ctx.session.prompt({ sessionID: owner, text: "Use your native shell tool to run this read-only log follower. Do not start or resume implementation:\n" + command })
        },
      })
      editor.add({
        name: "poseidon-end",
        description: "Remove this chat's sandbox while preserving settings and project work",
        execute: async ({ sessionID }) => {
          const owner = await rootSession(sessionID)
          const output = await invoke({ action: "end_sandbox", session_id: owner })
          preparation.delete(owner)
          await ctx.session.synthetic({ sessionID: owner, text: "Session sandbox ended. " + output, resume: false })
        },
      })
    })
    const events = new AbortController()
    const subscription = (async () => {
      for await (const event of ctx.event.subscribe({ types: ["session.archived", "session.deleted"], signal: events.signal })) {
        const sessionID = event.data?.sessionID ?? event.sessionID
        if (!sessionID) continue
        try {
          // Do not resolve child IDs to parents here: deleting a subagent must not
          // terminate the user chat's sandbox.
          await invoke({ action: "end_sandbox", session_id: sessionID })
          preparation.delete(sessionID)
        } catch (error) { console.error("Session sandbox cleanup failed", error) }
      }
    })().catch((error) => { if (!events.signal.aborted) console.error("Sandbox lifecycle subscription failed", error) })
    await ctx.tool.transform((editor) => editor.add({
      name: "poseidon_workspace",
      description: "Sandbox infrastructure only: read settings/status, configure a Docker image/build recipe and tests, run tests, or end the sandbox. No controller, approval token, rubric phase or model authentication. Returns a runtime path for use through the native shell tool; structured tool calls also forward live progress.",
      options: { permission: "poseidon_workspace", codemode: false },
      input: {
        type: "object",
        properties: {
          action: { type: "string", enum: ["settings", "configure", "test", "status", "end_sandbox"] },
          tests: { type: "object", additionalProperties: true, description: "For configure: image, commands (argv arrays), timeout_seconds." },
          sandbox: { type: "object", additionalProperties: true, description: "For configure: Docker executable/context or host; optional build {dockerfile: Dockerfile text, timeout_seconds}; environment, prepare_commands and resource limits. Omit to reuse persisted settings." },
        },
        required: ["action"], additionalProperties: false,
      },
      execute: async (input, context) => {
        const owner = await rootSession(context.sessionID)
        const output = await invoke({ ...input, session_id: owner }, context.signal,
          typeof context.progress === "function" ? (update) => context.progress(update) : undefined)
        const result = JSON.parse(output)
        if (result.sandbox) preparation.set(owner, result.sandbox)
        if (input.action === "end_sandbox") preparation.set(owner, result)
        return { content: output }
      },
    }))
    return () => { events.abort(); void subscription }
  },
}
