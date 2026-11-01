import { test } from 'node:test'
import assert from 'node:assert/strict'
import { mkdtemp,writeFile,readFile,rm } from 'node:fs/promises'
import path from 'node:path'
import { tmpdir } from 'node:os'
import { reserveNvidia } from '../.opencode/runtime/provider-budget.mjs'
async function fixture(fn){const root=await mkdtemp(path.join(tmpdir(),'nvidia-quota-'));try{await fn(path.join(root,'quota.json'))}finally{await rm(root,{recursive:true,force:true})}}
test('21st minute request is denied before dispatch; window later reopens',()=>fixture(async file=>{
 const now=100000000
 for(let i=0;i<20;i++)await reserveNvidia({file,now})
 await assert.rejects(reserveNvidia({file,now:now+1}),/requests\/minute/)
 assert.equal((await reserveNvidia({file,now:now+60001})).day,21)
}))
test('1001st rolling-day request denied even with empty minute window',()=>fixture(async file=>{
 const now=100000000;await writeFile(file,JSON.stringify({version:1,requests:Array(1000).fill(now-120000)}))
 await assert.rejects(reserveNvidia({file,now}),/requests\/day/)
 assert.equal((await reserveNvidia({file,now:now+86400001})).day,1)
}))
test('atomic shared reservations fail closed under contention',()=>fixture(async file=>{
 const outcomes=await Promise.allSettled(Array.from({length:25},()=>reserveNvidia({file,now:100000000})))
 const count=outcomes.filter(x=>x.status==='fulfilled').length;assert.ok(count>=1&&count<=20)
 const state=JSON.parse(await readFile(file));assert.equal(state.requests.length,count)
}))
test('corruption and backward clock do not reset consumed quota',()=>fixture(async file=>{
 await writeFile(file,'not json');await assert.rejects(reserveNvidia({file,now:100000000}))
 await writeFile(file,JSON.stringify({version:1,requests:Array(20).fill(100000000)}))
 await assert.rejects(reserveNvidia({file,now:99999999}),/requests\/minute/)
}))
