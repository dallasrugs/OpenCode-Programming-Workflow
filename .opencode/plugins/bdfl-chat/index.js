import { spawn } from "node:child_process"
import { fileURLToPath } from "node:url"

const bridge = fileURLToPath(new URL("../../governance/chat.py", import.meta.url))

export default {
  id: "bdfl-chat",
  async setup(ctx) {
    await ctx.tool.transform((editor) => {
      editor.add({
        name: "bdfl_controller",
        description: "Save a BDFL chat request and generated policy and start the governed controller. Also read defaults/status, resume, or convey an explicit BDFL escalation decision. Runs asynchronously; status contains verified results and errors.",
        input: {
          type: "object",
          properties: {
            action: { type: "string", enum: ["defaults", "submit", "status", "resume", "authorize", "reject"] },
            request: { type: "string", description: "Full user request, acceptance criteria, and agreed context. Required for submit." },
            policy: { type: "object", additionalProperties: true, description: "Complete repository-specific controller policy. Required for submit." },
            run_id: { type: "string", pattern: "^[a-f0-9]{12}$" },
            spec: { type: "string", description: "Exact pending specification hash, only after explicit BDFL approval." },
            reason: { type: "string" },
          },
          required: ["action"],
          additionalProperties: false,
        },
        execute: async (input, context) => {
          if (context.agent !== "team-lead") throw new Error("Only the interactive Team Lead may use the controller bridge")
          await ctx.permission.assert({
            sessionID: context.sessionID,
            agent: context.agent,
            source: { type: "tool", messageID: context.messageID, id: context.id },
            action: "bdfl_controller",
            resources: ["*"],
          })
          const output = await new Promise((resolve, reject) => {
            // Fixed executable/script and argv; request and policy are data, never shell text.
            const child = spawn("python3", [bridge, "--repo", ctx.location.directory, "call"], {
              stdio: ["pipe", "pipe", "pipe"], signal: context.signal,
            })
            let stdout = "", stderr = ""
            child.stdout.on("data", (chunk) => { stdout += chunk })
            child.stderr.on("data", (chunk) => { stderr += chunk })
            child.on("error", reject)
            child.on("close", (code) => code === 0 ? resolve(stdout) : reject(new Error(stdout || stderr || `Controller bridge exited ${code}`)))
            child.stdin.on("error", reject)
            child.stdin.end(JSON.stringify({ ...input, session_id: context.sessionID }))
          })
          return { content: output }
        },
      })
    })
  },
}
