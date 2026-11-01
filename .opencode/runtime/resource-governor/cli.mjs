#!/usr/bin/env node
import { Governor } from './governor.mjs'
import { setTimeout } from 'node:timers/promises'

const args = process.argv.slice(2)
const governor = new Governor()
const stopped = new AbortController()
const stop = () => stopped.abort()
process.once('SIGINT', stop); process.once('SIGTERM', stop)
try {
  const command = args.shift() ?? 'doctor'
  if (command === 'run') {
    if (args[0] === '--') args.shift()
    if (!args.length) throw Error('Usage: cli.mjs run -- executable [arguments]')
    governor.start()
    const result = await governor.execute(args, { signal: stopped.signal,
      progress: (index, chunk) => (index ? process.stderr : process.stdout).write(chunk) })
    process.exitCode = result.code ?? 1
  } else if (['doctor','resources'].includes(command)) {
    const watch = args.includes('--watch')
    // A watch is bounded to one hour; signals cancel the wait and close monitoring.
    for (let i = 0; i < (watch ? 480 : 1) && !stopped.signal.aborted; i++) {
      await governor.sample()
      console.log(JSON.stringify(governor.report(), null, args.includes('--json') || watch ? 0 : 2))
      if (watch) await setTimeout(governor.config.activeSampleMs, undefined, { signal: stopped.signal })
    }
    if (!governor.valid) process.exitCode = 1
  } else throw Error('Use doctor, resources [--json] [--watch], or run -- executable')
} catch (error) {
  if (!stopped.signal.aborted) { console.error(error.message); process.exitCode = 1 }
} finally {
  await governor.close()
  process.removeListener('SIGINT', stop); process.removeListener('SIGTERM', stop)
}
