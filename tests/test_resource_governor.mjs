import { test } from 'node:test'
import assert from 'node:assert/strict'
import { Governor, configuration, metricProvider } from '../.opencode/runtime/resource-governor/governor.mjs'
import { setTimeout as delay } from 'node:timers/promises'
import { open, mkdtemp, rm } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import path from 'node:path'

const metrics = (ratio = .2, processes = []) => ({ systemFD: ratio * 10000, systemLimit: 10000, physicalMemory: 16e9, processes })
async function fixture(config = {}) {
  let reading = metrics()
  const g = new Governor({ config, provider: async () => reading })
  await g.sample()
  return { g, set(value) { reading = value } }
}
async function waitFor(predicate) {
  for (let i = 0; i < 200; i++) { if (predicate()) return; await delay(10) }
  assert.fail('Condition timed out')
}

test('normal, warning, throttled, critical and emergency FD thresholds', async () => {
  const f = await fixture({maxAgents:3})
  assert.equal(f.g.state, 'NORMAL'); assert.equal(f.g.capacity('agent'), 3)
  for (const [ratio,state,capacity] of [[.5,'WARNING',2],[.65,'THROTTLED',1],[.8,'CRITICAL',0],[.9,'CRITICAL',0]]) {
    f.set(metrics(ratio)); await f.g.sample()
    assert.equal(f.g.state, state); assert.equal(f.g.capacity('agent'), capacity)
  }
  await f.g.close()
})

test('hysteresis requires sustained recovery and restores capacity gradually', async () => {
  const { g, set } = await fixture({ recoverySamples: 2 })
  set(metrics(.81)); await g.sample()
  set(metrics(.78)); await g.sample(); assert.equal(g.state,'CRITICAL')
  set(metrics(.2)); await g.sample(); assert.equal(g.state,'RECOVERING')
  await g.sample(); assert.equal(g.state,'THROTTLED')
  for (let i=0;i<4;i++) await g.sample()
  assert.equal(g.state,'NORMAL'); await g.close()
})

test('monitor failure and invalid metrics fail closed; cleanup remains possible', async () => {
  const { g } = await fixture()
  g.provider = async () => { throw Error('secret token must not be logged') }
  await g.sample(); assert.equal(g.capacity('shell'),0)
  assert.equal(g.state,'CRITICAL'); assert.equal(g.valid,false)
  const result = await g.execute([process.execPath,'-e','process.stdout.write("cleanup")'], { cleanup:true })
  assert.equal(result.stdout,'cleanup')
  assert.ok(!JSON.stringify(g.report()).includes('secret token'))
  await g.close()
})

test('memory budget uses resident memory and physical hardware, not virtual space', async () => {
  const { g,set } = await fixture({workloadRssSoftFraction:.4,workloadRssHardFraction:.5})
  g.processes.set(123,{ sessionID:'a' })
  set(metrics(.2,[{pid:123,fd:10,rss:1e6,virtual:1e15}]))
  await g.sample(); assert.equal(g.state,'NORMAL')
  set(metrics(.2,[{pid:123,fd:10,rss:4e9,virtual:1e15}]))
  await g.sample(); assert.equal(g.state,'THROTTLED')
  set(metrics(.2,[{pid:123,fd:10,rss:5e9}]))
  await g.sample(); assert.equal(g.state,'CRITICAL')
  g.processes.clear(); await g.close()
})

test('per-process FD budgets and unavailable descriptor measurements', async () => {
  const {g,set}=await fixture()
  g.processes.set(123,{})
  set(metrics(.2,[{pid:123,fd:1024,rss:1}]))
  await g.sample(); assert.equal(g.state,'THROTTLED')
  set(metrics(.2,[{pid:123,fd:2048,rss:1}]))
  await g.sample(); assert.equal(g.state,'CRITICAL')
  set(metrics(.2,[{pid:123,fd:null,rss:1}]))
  await g.sample(); assert.ok(g.history.some(e=>e.type==='fd-warning'))
  g.processes.clear(); await g.close()
})

test('FIFO saturation, bounded backpressure, queue cancellation and timeouts', async () => {
  const {g}=await fixture({maxTools:1,maxQueue:2,queueTimeoutMs:100})
  let release
  const first=g.run('tool',()=>new Promise(r=>{release=r}))
  await waitFor(()=>release)
  const order=[]
  const a=g.run('tool',async()=>order.push('a'))
  const b=g.run('tool',async()=>order.push('b'))
  await assert.rejects(g.run('tool',async()=>{}),/queue full/)
  release(); await Promise.all([first,a,b]); assert.deepEqual(order,['a','b'])
  const cancel=new AbortController()
  g.state='CRITICAL'
  const queued=g.run('tool',async()=>assert.fail(),{signal:cancel.signal})
  cancel.abort(); await assert.rejects(queued,/cancelled/)
  await assert.rejects(g.run('tool',async()=>assert.fail()),/expired/)
  assert.equal(g.queue.length,0); await g.close()
})

test('nested agent saturation rejects without deadlock; shell uses a separate lane', async()=>{
  const {g}=await fixture({maxAgents:1,maxDepth:2})
  await g.run('agent',async()=>{
    await g.run('shell',async()=>{})
    await assert.rejects(g.run('agent',async()=>{},{depth:1}),/Nested agent backpressure/)
    await assert.rejects(g.run('agent',async()=>{},{depth:2}),/depth exceeded/)
  })
  await g.close()
})

test('session cancellation cannot cancel another session',async()=>{
  const {g}=await fixture({maxTools:2})
  const observed=[]
  const operation=id=>g.run('tool',signal=>new Promise(resolve=>{
    signal.addEventListener('abort',()=>{observed.push(id);resolve()},{once:true})
  }),{sessionID:id})
  const a=operation('a'), b=operation('b')
  await waitFor(()=>g.active.size===2)
  g.cancelSession('a'); await a; assert.deepEqual(observed,['a']); assert.equal(g.active.size,1)
  g.cancelSession('b'); await b; await g.close()
})

test('emergency cancels eligible work; one high FD reading does not declare a leak',async()=>{
  const {g,set}=await fixture()
  const running=g.run('tool',signal=>new Promise(resolve=>signal.addEventListener('abort',resolve,{once:true})))
  await waitFor(()=>g.active.size===1)
  set(metrics(.95)); await g.sample(); await running
  assert.ok(!g.history.some(e=>e.type==='leak-suspected')); await g.close()
})

test('rolling leak evidence and unreaped children warnings are bounded',async()=>{
  const {g,set}=await fixture({leakSamples:3,leakGrowth:10,historySize:4})
  g.processes.set(123,{})
  for (const fd of [10,20,30,40,50]) {
    set(metrics(.2,[{pid:123,fd,rss:1,zombie:true}]))
    await g.sample()
  }
  assert.ok(g.history.some(e=>e.type==='unreaped-warning'))
  assert.ok(g.history.some(e=>e.type==='leak-suspected' && e.fdGrowth===20))
  assert.equal(g.history.length,4); assert.equal(g.growth.get(123).length,3)
  g.processes.clear(); await g.close()
})

test('trusted configuration is frozen and invalid/unknown budgets rejected',()=>{
  const g=new Governor()
  assert.throws(()=>{g.config.maxTools=999},TypeError)
  assert.throws(()=>{g.config={maxTools:999}},TypeError)
  assert.throws(()=>configuration({thresholds:[.8,.2,.3,.4]}))
  assert.throws(()=>configuration({disableMonitoring:true}))
  assert.throws(()=>configuration({maxQueue:Infinity}))
  assert.throws(()=>configuration({fdSoft:3000}))
})

test('managed subprocess timeout/cancel reaps child and bounds output',async()=>{
  const {g}=await fixture({graceMs:40,outputBytes:100})
  const r=await g.execute([process.execPath,'-e','process.stdout.write("x".repeat(10000))'])
  assert.equal(r.stdout.length,100); assert.equal(r.truncated[0],true)
  await assert.rejects(g.execute([process.execPath,'-e','setInterval(()=>{},1000)'],{timeoutMs:50}),/timed out/)
  const cancel=new AbortController()
  const pending=g.execute([process.execPath,'-e','setInterval(()=>{},1000)'],{signal:cancel.signal})
  await waitFor(()=>g.processes.size===1)
  cancel.abort(); await assert.rejects(pending,/cancelled/)
  assert.equal(g.processes.size,0); assert.equal(g.active.size,0); await g.close()
})

test('owned background child is cleaned even after successful parent exit',async()=>{
  const {g}=await fixture({graceMs:50})
  const result=await g.execute([process.execPath,'-e',`
    const {spawn}=require('node:child_process');
    const c=spawn(process.execPath,['-e','setInterval(()=>{},1000)'],{stdio:'ignore'});
    console.log(c.pid); c.unref();
  `])
  const pid=Number(result.stdout.trim())
  await waitFor(()=>{try{process.kill(pid,0);return false}catch{return true}})
  await g.close()
})

test('MCP transports and watchers close exactly once; monitoring stops',async()=>{
  const {g}=await fixture({activeSampleMs:20,idleSampleMs:30})
  let mcp=0, watcher=0, samples=0
  const release=g.own(async()=>{mcp++})
  g.own(()=>{watcher++})
  g.provider=async()=>{samples++;return metrics()}
  g.start(); await delay(70)
  await release(); await release(); await g.close()
  const n=samples; await delay(70)
  assert.equal(samples,n); assert.equal(mcp,1); assert.equal(watcher,1)
})

test('integration: bounded real file handles and simulated agent activity',async()=>{
  // Explicit stress-test capacity; production defaults intentionally stay serial.
  const {g}=await fixture({maxAgents:3,maxTools:2,maxShells:4,maxQueue:32})
  const dir=await mkdtemp(path.join(tmpdir(),'governor-fds-'))
  const files=[]
  try {
    for(let i=0;i<8;i++) files.push(await open(path.join(dir,String(i)),'w'))
    let peak=0, active=0
    await Promise.all(Array.from({length:12},()=>g.run('agent',async()=>{
      active++;peak=Math.max(peak,active)
      try { await g.execute([process.execPath,'-e','process.stdout.write("done")']) }
      finally { active-- }
    })))
    assert.equal(peak,3); assert.equal(g.queue.length,0); assert.equal(g.processes.size,0)
  } finally {
    await Promise.all(files.map(f=>f.close())); await rm(dir,{recursive:true,force:true}); await g.close()
  }
})

test('native read-only sampling reports actual hardware and self numeric FDs',async()=>{
  if(!['darwin','linux'].includes(process.platform))return
  const m=await metricProvider([process.pid])
  assert.ok(m.systemLimit>m.systemFD); assert.ok(m.physicalMemory>0)
  assert.ok(m.processes[0].fd>0); assert.ok(m.processes[0].rss>0)
})


test('same-group children contribute to per-workload RSS and FD budgets', async () => {
  const {g,set}=await fixture({workloadFDSoft:100,workloadFDHard:150})
  g.processes.set(123,{})
  set(metrics(.2,[{pid:123,group:123,fd:60,rss:1},{pid:124,group:123,fd:60,rss:1}]))
  await g.sample(); assert.equal(g.state,'THROTTLED'); assert.equal(g.report().managedFD,120)
  set(metrics(.2,[{pid:123,group:123,fd:80,rss:1},{pid:124,group:123,fd:80,rss:1}]))
  await g.sample(); assert.equal(g.state,'CRITICAL')
  g.processes.clear(); await g.close()
})

test('macOS sampler includes only owned same-group children', async () => {
  if (process.platform !== 'darwin') return
  const g = new Governor({ config: { graceMs: 50 } })
  await g.sample()
  const cancelled = new AbortController()
  let ready = false
  const running = g.execute([process.execPath, '-e', `
    const {spawn}=require('node:child_process');
    spawn(process.execPath,['-e','setInterval(()=>{},1000)'],{stdio:'ignore'});
    console.log('ready'); setInterval(()=>{},1000);
  `], { signal: cancelled.signal, progress: () => { ready = true } })
  running.catch(() => {})
  try {
    await waitFor(() => ready)
    await g.sample() // Finish any coalesced spawn sample taken before the child started.
    await g.sample()
    const root = [...g.processes.keys()][0]
    const owned = g.metrics.processes.filter(p => p.group === root)
    assert.ok(owned.length >= 2)
    assert.ok(owned.every(p => p.fd !== null && p.rss > 0))
  } finally {
    cancelled.abort(); await assert.rejects(running); await g.close()
  }
})


test('default budgets serialize work and reject nested agent dispatch', async () => {
  const {g}=await fixture()
  try {
    assert.equal(g.config.maxAgents,1)
    assert.equal(g.config.maxTools,1)
    assert.equal(g.config.maxShells,1)
    assert.equal(g.config.maxDepth,1)
    assert.equal(g.config.maxQueue,4)
    assert.equal(g.config.workTimeoutMs,900000)
    let active=0, peak=0
    await Promise.all(Array.from({length:4},()=>g.run('tool',async()=>{
      active++; peak=Math.max(peak,active)
      try { await delay(5) } finally { active-- }
    })))
    assert.equal(peak,1)
    await assert.rejects(g.run('agent',async()=>{},{depth:1}),/depth exceeded/)
  } finally { await g.close() }
})
