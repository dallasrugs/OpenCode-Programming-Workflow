// Bounded local measurement; no workload or system-limit changes.
import { Governor, metricProvider } from './governor.mjs'
import { performance } from 'node:perf_hooks'
const g = new Governor()
const before = await metricProvider([process.pid])
const rss = process.memoryUsage().rss, cpu = process.cpuUsage(), start = performance.now()
for (let i = 0; i < 10; i++) await g.sample()
const elapsed = performance.now() - start
const after = await metricProvider([process.pid])
console.log(JSON.stringify({ samples: 10, elapsedMs: elapsed, averageMs: elapsed / 10,
  cpuMicros: process.cpuUsage(cpu), rssDeltaBytes: process.memoryUsage().rss - rss,
  fdBefore: before.processes.find(p => p.pid === process.pid)?.fd,
  fdAfter: after.processes.find(p => p.pid === process.pid)?.fd,
  eventsRetained: g.history.length, activeChildrenAfter: g.processes.size,
  note: 'CPU/RSS are supervisor-only; elapsed includes bounded Python/ps helper cost.' }, null, 2))
await g.close()
