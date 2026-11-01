import { execFile, spawn } from 'node:child_process'
import { readFileSync } from 'node:fs'
import { fileURLToPath } from 'node:url'
import { promisify } from 'node:util'
import { randomUUID } from 'node:crypto'

const defaults = JSON.parse(readFileSync(new URL('./config.json', import.meta.url)))
const exec = promisify(execFile)
export const metricProvider = async (pids, timeout = defaults.metricTimeoutMs) => {
  const { stdout } = await exec('python3', [fileURLToPath(new URL('./sample.py', import.meta.url)), ...pids.map(String)],
    { timeout, maxBuffer: 65536 })
  return JSON.parse(stdout)
}
export function configuration(overrides = {}) {
  for (const key of Object.keys(overrides)) if (!(key in defaults)) throw Error('Unknown governor configuration')
  const c = { ...defaults, ...overrides }
  for (const [k, v] of Object.entries(c)) {
    if (k === 'thresholds') continue
    if (!Number.isFinite(v) || v <= 0) throw Error(`Invalid governor setting: ${k}`)
  }
  for (const k of ['maxAgents','maxTools','maxShells','maxDepth','maxQueue','historySize','recoverySamples','leakSamples','outputBytes']) {
    if (!Number.isInteger(c[k])) throw Error(`Expected integer: ${k}`)
  }
  if (!Array.isArray(c.thresholds) || c.thresholds.length !== 4 || c.thresholds.some((v, i, a) =>
    !Number.isFinite(v) || v <= 0 || v >= 1 || (i && v <= a[i-1])) ||
    c.fdSoft >= c.fdHard || c.workloadFDSoft >= c.workloadFDHard ||
    c.workloadRssSoftFraction >= c.workloadRssHardFraction || c.workloadRssHardFraction >= 1 || c.rssSoftFraction >= c.rssHardFraction || c.rssHardFraction >= 1 ||
    c.hysteresis >= c.thresholds[0] || c.leakSamples < 3 || c.maxShells > 63) throw Error('Invalid governor budgets')
  return Object.freeze({ ...c, thresholds: Object.freeze([...c.thresholds]) })
}

export class Governor {
  #config
  constructor({ config = {}, provider = metricProvider, now = Date.now } = {}) {
    this.#config = configuration(config)
    this.provider = provider; this.now = now
    this.state = 'CRITICAL'; this.level = 3; this.healthy = 0; this.valid = false
    this.queue = []; this.active = new Map(); this.processes = new Map()
    this.history = []; this.growth = new Map(); this.resources = new Set()
    this.warningCount = 0; this.closed = false; this.lastSample = 0
    this.id = randomUUID(); this.metrics = null
  }
  get config() { return this.#config }
  event(type, detail = {}) {
    // Callers supply numeric/identifier metadata only; never commands, output, prompts or env.
    this.history.push({ time: this.now(), type, ...detail })
    this.history.splice(0, Math.max(0, this.history.length - this.config.historySize))
    if (type.includes('warning') || type.includes('suspected') || type === 'monitor-failed') this.warningCount++
  }
  start() {
    if (this.started || this.closed) return
    this.started = true
    const tick = async () => {
      await this.sample()
      if (!this.closed) {
        this.timer = setTimeout(tick, (this.active.size || this.queue.length) ? this.config.activeSampleMs : this.config.idleSampleMs)
        this.timer.unref?.()
      }
    }
    void tick()
  }
  sample() {
    if (this.closed) return this.sampling ?? Promise.resolve()
    if (this.sampling) return this.sampling
    this.sampling = this.#sample().finally(() => { this.sampling = null })
    return this.sampling
  }
  async #sample() {
    try {
      const m = await this.provider([process.pid, ...this.processes.keys()], this.config.metricTimeoutMs)
      if (![m.systemFD, m.systemLimit, m.physicalMemory].every(Number.isFinite) || m.systemFD < 0 ||
          m.systemLimit <= 0 || m.physicalMemory <= 0 || !Array.isArray(m.processes)) throw Error('Invalid metrics')
      this.metrics = m; this.valid = true; this.lastSample = this.now()
      const ratio = m.systemFD / m.systemLimit
      let level = this.config.thresholds.filter(t => ratio >= t).length
      const managed = m.processes.filter(p => this.processes.has(p.pid) || this.processes.has(p.group))
      for (const p of m.processes) if (![p.pid, p.rss].every(Number.isFinite) || p.rss < 0 ||
          (p.fd !== null && (!Number.isFinite(p.fd) || p.fd < 0))) throw Error('Invalid process metrics')
      const measured = m.processes.filter(p => p.pid === process.pid || managed.includes(p))
      const rss = measured.reduce((s, p) => s + p.rss, 0)
      const live = new Set(managed.map(p => p.pid))
      for (const pid of this.growth.keys()) if (!live.has(pid)) this.growth.delete(pid)
      const groups = [...this.processes.keys()].map(group => managed.filter(p => p.pid === group || p.group === group))
      const workloadSoft = groups.some(group => group.reduce((s,p) => s + p.rss, 0) >= m.physicalMemory * this.config.workloadRssSoftFraction ||
        group.reduce((s,p) => s + (p.fd ?? 0), 0) >= this.config.workloadFDSoft)
      const workloadHard = groups.some(group => group.reduce((s,p) => s + p.rss, 0) >= m.physicalMemory * this.config.workloadRssHardFraction ||
        group.reduce((s,p) => s + (p.fd ?? 0), 0) >= this.config.workloadFDHard)
      const soft = workloadSoft || measured.some(p => p.fd >= this.config.fdSoft) || rss >= m.physicalMemory * this.config.rssSoftFraction
      const hard = workloadHard || measured.some(p => p.fd >= this.config.fdHard) || rss >= m.physicalMemory * this.config.rssHardFraction
      if (soft) level = Math.max(level, 2)
      if (hard) level = Math.max(level, 4)
      for (const p of managed) {
        if (p.fd === null) { level = Math.max(level, 3); this.event('fd-warning', { pid: p.pid }) }
        if (p.zombie) this.event('unreaped-warning', { pid: p.pid })
        const window = this.growth.get(p.pid) ?? []
        if (Number.isFinite(p.fd)) window.push({ fd: p.fd, time: this.now(), active: this.active.size })
        if (window.length > this.config.leakSamples) window.shift()
        this.growth.set(p.pid, window)
        if (window.length === this.config.leakSamples && window.every((v,i) => v.active === window[0].active && (!i || v.fd > window[i-1].fd)) &&
            window.at(-1).fd - window[0].fd >= this.config.leakGrowth) this.event('leak-suspected', {
          pid: p.pid, samples: window.length, fdGrowth: window.at(-1).fd - window[0].fd, durationMs: window.at(-1).time - window[0].time, activeWorkloads: this.active.size })
      }
      if (!this.initialized) { this.level = level; this.state = ['NORMAL','WARNING','THROTTLED','CRITICAL','CRITICAL'][level]; this.everHealthy = true; this.initialized = true }
      const previous = this.state
      if (level >= this.level && level > 0) {
        this.level = level; this.healthy = 0
        this.state = ['NORMAL','WARNING','THROTTLED','CRITICAL','CRITICAL'][level]
      } else if (level < this.level || this.state === 'RECOVERING' || !this.everHealthy) {
        const boundary = this.config.thresholds[Math.max(0, Math.min(this.level, 4) - 1)] - this.config.hysteresis
        if (!soft && ratio < boundary) {
          this.state = 'RECOVERING'
          if (++this.healthy >= this.config.recoverySamples) {
            this.level = Math.max(level, this.level - 1); this.healthy = 0; this.everHealthy = true
            this.state = ['NORMAL','WARNING','THROTTLED','CRITICAL','CRITICAL'][this.level]
          }
        } else this.healthy = 0
      }
      if (previous !== this.state) this.event('state', { state: this.state, systemFD: m.systemFD, systemLimit: m.systemLimit })
      if (level >= 4) for (const work of this.active.values()) if (work.cancelEligible && work.kind !== 'control') work.controller.abort(Error('Resource emergency'))
    } catch {
      this.valid = false; this.state = 'CRITICAL'; this.level = 3; this.healthy = 0
      this.event('monitor-failed')
    }
    this.drain()
  }
  capacity(kind) {
    if (kind === 'control') return this.closed ? 0 : 1
    if (!this.valid || this.closed || this.now() - this.lastSample > this.config.activeSampleMs || this.state === 'CRITICAL' || this.state === 'RECOVERING') return 0
    const max = kind === 'agent' ? this.config.maxAgents : kind === 'shell' ? Math.min(this.config.maxShells, this.config.maxTools) : this.config.maxTools
    return this.state === 'NORMAL' ? max : this.state === 'WARNING' ? Math.max(1, max - 1) : 1
  }
  drain() {
    // FIFO within each lane. A bounded interactive preference ages out after 5 seconds.
    const ordered = [...this.queue].sort((a,b) =>
      (a.created - (a.interactive ? 5000 : 0)) - (b.created - (b.interactive ? 5000 : 0)))
    for (const item of ordered) {
      const running = [...this.active.values()]
      const count = running.filter(w => w.kind === item.kind).length
      const tools = running.filter(w => w.kind !== 'agent' && w.kind !== 'control').length
      if (count >= this.capacity(item.kind) || (!['agent','control'].includes(item.kind) && tools >= this.capacity('tool'))) continue
      this.queue.splice(this.queue.indexOf(item), 1); item.detach()
      this.active.set(item.id, item); item.resolve(item)
    }
  }
  async run(kind, operation, { signal, sessionID = 'local', agentID = 'unknown', taskID = randomUUID(), depth = 0,
    interactive = false, cancelEligible = true } = {}) {
    if (!['agent','tool','shell','control'].includes(kind)) throw Error('Unknown workload kind')
    if (this.closed || signal?.aborted) throw Error('Governor stopped or workload cancelled')
    if (kind === 'agent' && depth >= this.config.maxDepth) throw Error('Nested agent depth exceeded')
    // Parent agents have a separate lane and never hold a heavy-tool slot while awaiting children.
    // Reject nested admission rather than queue behind ancestors occupying every agent slot.
    if (kind === 'agent' && depth > 0 && [...this.active.values()].filter(w => w.kind === 'agent').length >= this.capacity('agent')) throw Error('Nested agent backpressure: retry after parent releases')
    if (this.queue.filter(w => kind === 'control' ? w.kind === 'control' : w.kind !== 'control').length >= (kind === 'control' ? 4 : this.config.maxQueue)) throw Error('Resource queue full')
    const controller = new AbortController()
    const item = { id: randomUUID(), kind, sessionID, agentID, taskID, controller, cancelEligible, interactive, created: this.now() }
    const relay = () => controller.abort(signal.reason)
    signal?.addEventListener('abort', relay, { once: true })
    try {
      await new Promise((resolve, reject) => {
        item.resolve = resolve
        const cancel = () => {
          const i = this.queue.indexOf(item); if (i >= 0) this.queue.splice(i,1)
          item.detach(); reject(Error('Queued workload cancelled or expired'))
        }
        const timer = setTimeout(cancel, this.config.queueTimeoutMs)
        item.detach = () => { clearTimeout(timer); controller.signal.removeEventListener('abort', cancel) }
        controller.signal.addEventListener('abort', cancel, { once: true })
        this.queue.push(item); this.drain()
        if (!this.valid || this.now() - this.lastSample > this.config.activeSampleMs) void this.sample()
      })
      const timer = setTimeout(() => controller.abort(Error('Workload timeout')), this.config.workTimeoutMs)
      try { return await operation(controller.signal, item) } finally { clearTimeout(timer) }
    } finally {
      signal?.removeEventListener('abort', relay)
      this.active.delete(item.id); this.drain()
    }
  }
  own(close) {
    if (this.closed) throw Error('Governor stopped')
    this.resources.add(close)
    return async () => { if (this.resources.delete(close)) await close() }
  }
  cancelSession(sessionID) {
    for (const w of [...this.queue, ...this.active.values()]) if (w.sessionID === sessionID && w.kind !== 'control') w.controller.abort(Error('Session ended'))
  }
  async execute(argv, { signal, input, sessionID = 'local', agentID = 'unknown', taskID = randomUUID(),
    timeoutMs = this.config.workTimeoutMs, progress, cleanup = false } = {}) {
    const launch = async (workSignal) => new Promise((resolve, reject) => {
      if (workSignal?.aborted) return reject(Error('Workload cancelled'))
      const child = spawn(argv[0], argv.slice(1), { detached: process.platform !== 'win32', stdio: ['pipe','pipe','pipe'] })
      const record = { pid: child.pid, parentPID: process.pid, sessionID, agentID, taskID, startTime: this.now(),
        ownership: this.id, status: 'running', cancellation: false, timeoutMs, cleanup: 'pending' }
      if (child.pid) this.processes.set(child.pid, record)
      const buffers = [Buffer.alloc(0), Buffer.alloc(0)], sizes = [0,0]
      let force, failure, settled = false
      const kill = (sig) => {
        // Only this newly created process group; never a discovered descendant or another session.
        try { if (process.platform === 'win32') child.kill(sig); else process.kill(-child.pid, sig) }
        catch (e) { if (e.code !== 'ESRCH') this.event('cleanup-warning', { pid: child.pid }) }
      }
      const abort = () => {
        if (record.cancellation) return
        record.cancellation = true; kill('SIGTERM')
        force = setTimeout(() => kill('SIGKILL'), this.config.graceMs)
      }
      workSignal?.addEventListener('abort', abort, { once: true })
      const timeout = setTimeout(abort, timeoutMs)
      child.stdout.on('data', chunk => consume(0, chunk))
      child.stderr.on('data', chunk => consume(1, chunk))
      function consume(i, chunk) {
        sizes[i] += chunk.length
        buffers[i] = Buffer.concat([buffers[i], chunk]).subarray(-governor.config.outputBytes)
        if (progress) { try { progress(i, chunk) } catch { governor.event('progress-warning') } }
      }
      const governor = this
      child.on('error', e => { failure = e })
      child.stdin.on('error', () => {})
      child.stdin.end(input)
      child.on('exit', (code, sig) => {
        record.status = 'exited'; record.exitCode = code; record.exitSignal = sig
        // Even successful commands must not leave background children holding pipes open.
        kill('SIGTERM')
        if (!force) force = setTimeout(() => kill('SIGKILL'), this.config.graceMs)
      })
      child.on('close', (code, sig) => {
        if (settled) return; settled = true
        clearTimeout(timeout); clearTimeout(force); workSignal?.removeEventListener('abort', abort)
        // Catch owned children that closed their inherited pipes but remain in our group.
        kill('SIGKILL')
        record.cleanup = 'complete'; this.processes.delete(child.pid); this.growth.delete(child.pid)
        this.event('cleanup', { pid: child.pid, exitCode: code, cancelled: record.cancellation })
        void this.sample()
        if (failure || record.cancellation) reject(failure ?? Error('Managed process cancelled or timed out'))
        else resolve({ code, signal: sig, stdout: buffers[0].toString(), stderr: buffers[1].toString(),
          truncated: sizes.map((n,i) => n > buffers[i].length), bytes: sizes })
      })
      void this.sample()
    })
    // Cleanup is always allowed during pressure; callers cannot select this via tool input.
    return this.run(cleanup ? 'control' : 'shell', launch, { signal, sessionID, agentID, taskID })
  }
  report() {
    return { version: 1, platform: process.platform, node: process.version, governorState: this.state,
      monitoringValid: this.valid, config: this.config, metrics: this.metrics, managedProcesses: [...this.processes.values()],
      activeAgents: [...this.active.values()].filter(w => w.kind === 'agent').length,
      activeToolCalls: [...this.active.values()].filter(w => w.kind !== 'agent' && w.kind !== 'control').length,
      managedFD: this.metrics?.processes.filter(p => this.processes.has(p.pid) || this.processes.has(p.group)).reduce((s,p) => s + (p.fd ?? 0), 0) ?? null,
      estimatedManagedRSS: this.metrics?.processes.filter(p => this.processes.has(p.pid) || this.processes.has(p.group)).reduce((s,p) => s + p.rss, 0) ?? null,
      queuedWorkloads: this.queue.length, warningCount: this.warningCount, recentEvents: this.history,
      self: { rss: process.memoryUsage().rss, cpu: process.cpuUsage() } }
  }
  async close() {
    this.closed = true; clearTimeout(this.timer)
    for (const w of [...this.queue, ...this.active.values()]) w.controller.abort(Error('Governor shutdown'))
    await Promise.allSettled([...this.resources].map(close => close()))
    this.resources.clear()
    // Execute promises retain their slots until their child has actually closed/reaped.
    const deadline = Date.now() + this.config.graceMs + 3000
    while (this.processes.size && Date.now() < deadline) await new Promise(r => setTimeout(r, 25))
    if (this.sampling) await this.sampling
  }
}
