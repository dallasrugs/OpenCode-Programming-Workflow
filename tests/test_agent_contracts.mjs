import { test } from 'node:test'
import assert from 'node:assert/strict'
import { mkdtemp, mkdir, writeFile, symlink, rm } from 'node:fs/promises'
import { tmpdir } from 'node:os'
import path from 'node:path'
import { assignment,validateBrief,handoff,fallback,spend,scopedPath,editPaths } from '../.opencode/runtime/agent-contracts.mjs'
const budget={tools:8,steps:8,searches:3,pages:4,words:300,seconds:120}
const task=()=>assignment({id:'r1',to:'researcher',objective:'Check evidence',question:'What is supported?',purpose:'Decide',scope:['src'],exclusions:[],sourceTypes:['local'],skills:[],acceptance:['Cited support'],nextAction:'Report',design:false},budget)
const state=()=>({started:0,calls:0,sources:[{id:'S1',excerpt:'The foreground is green.'}]})
const result=()=>({taskID:'r1',from:'researcher',to:'poseidon',objective:'Check evidence',scope:['src'],exclusions:[],briefVersion:null,status:'PARTIAL',summary:'Only the foreground is established.',claims:[{id:'C1',type:'VERIFIED_FACT',text:'The foreground is green.',sourceIDs:['S1'],quote:'The foreground is green.'}],verification:[],uncertainty:['User taste unknown.'],nextAction:'Ask Poseidon to clarify intent.'})
test('admission prevents overruns including concurrent reservations and failed attempts',()=>{
 const s=state();for(let i=0;i<8;i++)spend(s,'read',budget,1)
 assert.throws(()=>spend(s,'read',budget,2),/Tool budget/);assert.equal(s.calls,8)
 const q=state();for(let i=0;i<3;i++)spend(q,'websearch',budget,1)
 assert.throws(()=>spend(q,'websearch',budget,1),/Search budget/)
 const p=state();for(let i=0;i<4;i++)spend(p,'webfetch',budget,1)
 assert.throws(()=>spend(p,'webfetch',budget,1),/Page budget/)
 assert.throws(()=>spend(state(),'read',budget,120000),/Runtime budget/)
})
test('unapproved skills and budget escalation rejected',()=>{
 const t=task();assert.throws(()=>assignment({...t,skills:['frontend-design']},budget),/Unauthorized/)
 assert.throws(()=>assignment({...t,budget:{tools:9}},budget),/operator/)
 assert.throws(()=>assignment({...t,scope:['../outside']},budget),/Unsafe/)
})
test('handoffs reject unsupported citations, fabricated quotations, expanded scope and excessive prose',()=>{
 assert.equal(handoff(result(),task(),state(),300).status,'PARTIAL')
 for(const change of [h=>h.claims[0].sourceIDs=['fake'],h=>h.claims[0].quote='Users require red.',h=>h.scope=['.'],h=>h.from='poseidon',h=>h.summary='word '.repeat(301)]) {
  const h=result();change(h);assert.throws(()=>handoff(h,task(),state(),300))
 }
})
test('review verdicts require calibrated findings; partial fallback is inconclusive',()=>{
 const t={...task(),to:'reviewer'},h={...result(),from:'reviewer',claims:[],verdict:'PASS',findings:[]}
 assert.equal(handoff(h,t,state(),300).verdict,'PASS')
 assert.throws(()=>handoff({...h,verdict:'FAIL',findings:[]},t,state(),300),/Preferences/)
 const f={severity:'P0',location:'src/a',problem:'Bug',evidence:'Observed',impact:'Failure',confidence:'high',remediation:'Fix'}
 assert.throws(()=>handoff({...h,verdict:'FAIL',findings:[f]},t,state(),300),/immediate danger/)
 assert.equal(fallback(t,state(),'Deadline').verdict,'INCONCLUSIVE')
})
test('briefs preserve revision provenance and cannot self-confirm',()=>{
 const b={id:'design',version:1,goals:['Read'],preferences:['Green'],prohibitions:['No shop'],functional:[],technical:[],accessibility:[],acceptance:['Readable'],openQuestions:[],decisions:[{id:'d1',text:'Green',kind:'USER_STATEMENT',provenance:'User message 1'}],confirmed:true}
 const first=validateBrief(b);assert.equal(first.confirmed,false)
 assert.throws(()=>validateBrief({...b,version:2},first),/revision reason/)
 assert.ok(validateBrief({...b,version:2,reason:'User changed spacing'},first).previousHash)
})
test('file scope, secret/control-plane paths, shell patch escapes and external symlinks rejected',async()=>{
 const root=await mkdtemp(path.join(tmpdir(),'contract-scope-'));const outside=await mkdtemp(path.join(tmpdir(),'contract-out-'))
 try {
  await mkdir(path.join(root,'src'));await writeFile(path.join(root,'src/a.txt'),'a');await symlink(outside,path.join(root,'src/escape'))
  const t={...task(),to:'coder'}
  await scopedPath(root,'src/a.txt',t,true)
  for(const p of ['src/escape/new.txt','../outside','.opencode/agents/poseidon.md','src/.env','src/customer.credentials.json','docs/other.md'])await assert.rejects(scopedPath(root,p,t,true))
  await assert.rejects(scopedPath(root,'src/a.txt',task(),true),/Only Coder/)
  assert.deepEqual(editPaths({patchText:'*** Update File: src/a\n*** Move to: src/b'}),['src/a','src/b'])
  assert.throws(()=>editPaths({command:'write anything'}),/Unknown/)
 }finally{await rm(root,{recursive:true,force:true});await rm(outside,{recursive:true,force:true})}
})
test('bounded local search excludes credentials, explicit exclusions and symlinked directories',async()=>{
 const {searchProject}=await import('../.opencode/runtime/agent-contracts.mjs')
 const root=await mkdtemp(path.join(tmpdir(),'search-scope-')),out=await mkdtemp(path.join(tmpdir(),'search-out-'))
 try{await writeFile(path.join(root,'a.md'),'green source');await writeFile(path.join(root,'.env'),'green secret');await writeFile(path.join(out,'leak.md'),'green outside');await symlink(out,path.join(root,'link'))
 const result=await searchProject(root,{...task(),scope:['.']},'green');assert.deepEqual(result.matches.map(x=>x.path),['a.md'])
 const excluded=await searchProject(root,{...task(),scope:['.'],exclusions:['a.md']},'green');assert.equal(excluded.matches.length,0)
 }finally{await rm(root,{recursive:true,force:true});await rm(out,{recursive:true,force:true})}
})
test('brief revision cannot silently drop prior prohibitions or confirmed decisions',()=>{
 const b={id:'journal',version:1,goals:['Read'],preferences:['Green'],prohibitions:['No shop'],functional:[],technical:[],accessibility:[],acceptance:['Readable'],openQuestions:[],decisions:[]}
 const previous=validateBrief(b)
 assert.throws(()=>validateBrief({...b,version:2,reason:'Spacing update',prohibitions:[]},previous),/explicit change provenance/)
 assert.equal(validateBrief({...b,version:2,reason:'User changed scope',prohibitions:[],changes:[{field:'prohibitions',previous:'No shop',reason:'User now requested commerce',provenance:'User correction message 2'}]},previous).version,2)
})
test('project root can be read without weakening scope or external path checks',async()=>{
 const {mkdtemp,mkdir,rm}=await import('node:fs/promises')
 const {tmpdir}=await import('node:os')
 const root=await mkdtemp(path.join(tmpdir(),'root-read-'))
 try{
  const task={...result(),to:'researcher',scope:['.'],exclusions:[]}
  assert.equal(await scopedPath(root,'.',task),root)
  assert.equal(await scopedPath(root,root,task),root)
  await mkdir(path.join(root,'src'))
  await assert.rejects(scopedPath(root,'.',{...task,scope:['src']}),/outside task scope/)
  await assert.rejects(scopedPath(root,'..',task),/escapes project/)
 }finally{await rm(root,{recursive:true,force:true})}
})
