import { test } from "node:test"
import assert from "node:assert/strict"
import plugin from "../.opencode/plugins/bdfl-chat/index.js"
import { fileURLToPath } from "node:url"

test("V2 registration calls the real Python bridge without granting shell access", async () => {
  let tool
  const assertions = []
  await plugin.setup({
    location: { directory: fileURLToPath(new URL("..", import.meta.url)) },
    tool: { transform: async (register) => register({ add: (definition) => { tool = definition } }) },
    permission: { assert: async (input) => { assertions.push(input) } },
  })
  assert.equal(tool.name, "bdfl_controller")
  await assert.rejects(tool.execute({ action: "defaults" }, { agent: "coder" }), /interactive Team Lead/)
  const result = await tool.execute({ action: "defaults" }, {
    agent: "team-lead", sessionID: "session-test", messageID: "message-test", id: "call-test",
    signal: new AbortController().signal,
  })
  const defaults = JSON.parse(result.content)
  assert.deepEqual(Object.keys(defaults.policy_template.models).sort(), ["coder", "maintainer", "reviewer", "team-lead"])
  assert.equal(assertions.length, 1)
  assert.equal(assertions[0].action, "bdfl_controller")
})
