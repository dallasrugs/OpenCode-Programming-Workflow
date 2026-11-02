import { reserveNvidia } from './provider-budget.mjs'
import { readFileSync } from 'node:fs'
import { realpath, mkdir, writeFile } from 'node:fs/promises'
import { fileURLToPath } from 'node:url'
import path from 'node:path'
import { createHash } from 'node:crypto'
import { assignment, validateBrief, handoff, fallback, spend, scopedPath, editPaths, searchProject, roles, need, digest } from './agent-contracts.mjs'
const matrix = JSON.parse(readFileSync(new URL('../skills/SOURCES.json', import.meta.url))).agents
const limits = JSON.parse(readFileSync(new URL('./agent-limits.json', import.meta.url)))
const readTools = new Set(['read','glob','grep','webfetch','websearch','skill','opencode_list_mcp_resources','opencode_read_mcp_resource'])
const writes = new Set(['edit','write','patch','apply_patch'])
const native = new Set([...readTools,...writes,'question','subagent','agent_contracts','project_search','poseidon_workspace'])
const unwrap = r => r?.data ?? r
const sourceText = r => Array.isArray(r?.content) ? r.content.filter(x=>x.type==='text').map(x=>x.text).join('\n') : typeof r?.content === 'string' ? r.content : JSON.stringify(r?.content ?? r)

export default {
 id:'agent-reliability',
 async setup(ctx) {
  const locks=new Map(), timers=new Map(), audit=new Map()
  const rootOf=async id=>{const seen=new Set();while(id&&!seen.has(id)&&seen.size<16){seen.add(id);const s=unwrap(await ctx.session.get({sessionID:id}));if(!s.parentID)return id;id=s.parentID}throw Error('Invalid session ancestry')}
  const transact=async(root,fn)=>{
   const prior=locks.get(root)??Promise.resolve();const next=prior.catch(()=>{}).then(async()=>{
    const key='root/'+root;const d=await ctx.storage.get(key)??{tasks:{},briefs:{},sessions:{},events:[]};const before=structuredClone(d)
    let result
    try{result=await fn(d)}catch(error){
     // Roll back task/brief mutations, while failed admitted calls still consume budget.
     for(const [id,s]of Object.entries(d.sessions)){
      before.sessions[id]??={role:s.role,taskID:s.taskID,started:s.started,calls:0,searches:0,pages:0,denied:0,modelSteps:0,sources:[],closed:false}
      for(const k of ['calls','searches','pages','denied','modelSteps'])before.sessions[id][k]=Math.max(before.sessions[id][k]??0,s[k]??0)
     }
     await ctx.storage.set(key,before);throw error
    }
    d.events=d.events.slice(-128);await ctx.storage.set(key,d);return result
   });locks.set(root,next);try{return await next}finally{if(locks.get(root)===next)locks.delete(root)}
  }
  const getState=(d,id,role)=>{
   need(roles.includes(role),'Unknown agent')
   if(!d.sessions[id]) {
    need(Object.keys(d.sessions).length<64,'Session record limit reached; start a new root task')
    const t=Object.values(d.tasks).find(t=>t.to===role&&t.status==='RUNNING')
    d.sessions[id]={role,taskID:t?.id??null,started:Date.now(),calls:0,searches:0,pages:0,sources:[],denied:0,modelSteps:0,closed:false}
   }
   need(d.sessions[id].role===role,'Session role changed; use a new session');return d.sessions[id]
  }
  const taskFor=(d,s)=>d.tasks[s.taskID]??{id:'direct-'+s.role,from:'poseidon',to:s.role,objective:'Direct bounded investigation',question:'Answer the current user request',purpose:'Direct session',scope:['.'],exclusions:[],sourceTypes:['local','web'],skills:matrix[s.role],acceptance:['Return evidence within scope'],design:false,budget:limits.roles[s.role]}
  const stopTimer=id=>{clearTimeout(timers.get(id));timers.delete(id)}
  const arm=(root,id,s,t)=>{
   if(timers.has(id)||s.closed)return
   const timer=setTimeout(async()=>{
    timers.delete(id)
    try {await transact(root,d=>{const state=d.sessions[id];if(!state||state.closed)return;state.closed=true;state.reason='Runtime budget exhausted';const task=taskFor(d,state);if(d.tasks[task.id]){d.tasks[task.id].handoff=fallback(task,state,state.reason);d.tasks[task.id].status='PARTIAL'}});await ctx.session.interrupt({sessionID:id,resume:false})}catch{}
   },Math.max(1,t.budget.seconds*1000-(Date.now()-s.started)));timer.unref?.();timers.set(id,timer)
  }
  const execute=async(input,context)=>{
   const root=await rootOf(context.sessionID),role=context.agent??unwrap(await ctx.session.get({sessionID:context.sessionID})).agent
   return transact(root,async d=>{
    const s=getState(d,context.sessionID,role),task=taskFor(d,s)
    if(s.calls>=task.budget.tools-1)need(input.action==='submit','Final tool slot is reserved for submit')
    spend(s,'agent_contracts',task.budget,Date.now())
    if(input.action==='status')return {task,state:s,briefs:d.briefs,tasks:role==='poseidon'?d.tasks:undefined,reviewTarget:task.reviewOf?d.tasks[task.reviewOf]?.handoff:undefined}
    if(input.action==='assign') {
     need(role==='poseidon','Only Poseidon assigns work');need(Object.keys(d.tasks).length<128,'Task record limit reached')
     const t=assignment(input.value,limits.roles[input.value?.to]);need(!d.tasks[t.id],'Task ID already exists')
     need(!Object.values(d.tasks).some(x=>x.to===t.to&&['ASSIGNED','RUNNING'].includes(x.status)),'Recipient already owns active work')
     if(t.design&&t.to==='coder'){const b=d.briefs[t.briefID]?.find(x=>x.version===t.briefVersion);need(b?.confirmed,'User-confirmed brief required');t.briefHash=digest(b)}
     if(t.researchTaskID){const r=d.tasks[t.researchTaskID];need(r?.critique?.verdict==='PASS','Material research needs independent critique')}
     if(t.to==='coder')need(!Object.values(d.tasks).some(x=>x.to==='coder'&&['ASSIGNED','RUNNING'].includes(x.status)),'One implementation owner at a time')
     d.tasks[t.id]=t;d.events.push({type:'assigned',taskID:t.id,to:t.to});return t
    }
    if(input.action==='propose_brief') {
     need(role==='poseidon','Only Poseidon proposes design briefs');const history=d.briefs[input.value?.id]??[];need(history.length<32,'Brief revision limit reached')
     const b=validateBrief(input.value,history.at(-1));history.push(b);d.briefs[b.id]=history
     return {brief:b,hash:digest(b),confirmationCommand:`/confirm-brief ${b.id} ${b.version} ${digest(b)}`}
    }
    if(input.action==='submit') {
     need(!s.closed,'Task is closed');const h=handoff(input.value,task,s,task.budget.words)
     if(d.tasks[task.id]){d.tasks[task.id].handoff={...h,sources:s.sources};d.tasks[task.id].status=h.status}
     s.closed=true;s.modelHandoff=true;s.handoff={...h,sources:s.sources};stopTimer(context.sessionID);return s.handoff
    }
    if(input.action==='critique') {
     need(role==='reviewer'&&task.reviewOf===input.value?.taskID,'Only assigned independent Reviewer critiques research')
     const t=d.tasks[input.value.taskID];need(t?.handoff?.from==='researcher','Research handoff missing')
     need(['PASS','FAIL','INCONCLUSIVE'].includes(input.value.verdict),'Critique verdict required')
     need(Array.isArray(input.value.checkedClaims)&&t.handoff.claims.every(c=>input.value.checkedClaims.includes(c.id)),'Every claim must be checked')
     need(typeof input.value.summary==='string'&&input.value.summary.length<=4000,'Bounded critique required')
     t.critique=structuredClone(input.value);return t.critique
    }
    throw Error('Unknown contract action')
   })
  }
  await ctx.tool.transform(editor=>editor.add({name:'agent_contracts',description:'Trusted assignments, read-only evidence ledger, Poseidon brief proposals, and validated handoffs. Actions: status; assign(value=task contract, Poseidon only); propose_brief(value=brief, Poseidon only); submit(value=handoff); critique(value=research critique, assigned Reviewer only). No action can confirm a brief.',options:{permission:'agent_contracts',codemode:false},input:{type:'object',properties:{action:{type:'string',enum:['status','assign','propose_brief','submit','critique']},value:{type:'object',additionalProperties:true}},required:['action'],additionalProperties:false},execute:async(input,c)=>({content:JSON.stringify(await execute(input,c))})}))
  await ctx.tool.transform(editor=>editor.add({name:'project_search',description:'Bounded literal search of assigned local source paths. Does not follow symlinks or search protected files.',options:{permission:'project_search',codemode:false},input:{type:'object',properties:{query:{type:'string'}},required:['query'],additionalProperties:false},execute:async(input,c)=>{const root=await rootOf(c.sessionID);const task=await transact(root,d=>taskFor(d,getState(d,c.sessionID,c.agent)));return {content:JSON.stringify(await searchProject(ctx.location.directory,task,input.query,c.signal))}}}))
  await ctx.command.transform(editor=>{
   editor.add({name:'confirm-brief',description:'Confirm an inspected proposal: ID VERSION HASH. This operator command is never an agent tool.',execute:async({sessionID,prompt})=>{
    const [id,version,hash,...extra]=prompt.text.trim().split(/\s+/);need(!extra.length,'Expected ID VERSION HASH');const root=await rootOf(sessionID)
    const result=await transact(root,d=>{const b=d.briefs[id]?.at(-1);need(b&&b.version===Number(version)&&digest(b)===hash,'Stale or changed brief proposal');need(!b.openQuestions.length,'Resolve open questions before confirmation');b.confirmed=true;b.confirmedBy='USER_COMMAND';b.confirmedAt=new Date().toISOString();return b})
    await ctx.session.synthetic({sessionID,text:JSON.stringify(result),resume:false})
   }})
   editor.add({name:'agent-audit',description:'Inspect registered tools and bounded session telemetry, without provider secrets.',execute:async({sessionID})=>{
    await ctx.tool.list?.()
    const root=await rootOf(sessionID);const data=await transact(root,d=>({toolAudit:[...audit.values()],sessions:Object.fromEntries(Object.entries(d.sessions).map(([id,s])=>[id,{role:s.role,calls:s.calls,denied:s.denied,searches:s.searches,pages:s.pages,closed:s.closed}]))}))
    console.info('agent-reliability-tool-audit',JSON.stringify(data.toolAudit))
    await ctx.session.synthetic({sessionID,text:JSON.stringify(data),resume:false})
   }})
   editor.add({name:'agent-export',description:'Operator-only export of bounded evaluation evidence into Git-local storage.',execute:async({sessionID})=>{
    const root=await rootOf(sessionID);const record=await transact(root,d=>{const s=d.sessions[sessionID];need(s,'No execution evidence');const t=taskFor(d,s);const accepted=s.handoff??d.tasks[t.id]?.handoff;
     const h=accepted??fallback(t,s,'No accepted model handoff before completion');s.closed=true;stopTimer(sessionID);return {sessionID,task:t,state:s,handoff:h,modelHandoff:Boolean(s.modelHandoff),fallback:!s.modelHandoff}
    });const directory=path.join(ctx.location.directory,'.git/bdfl/agent-evals');await mkdir(directory,{recursive:true});await writeFile(path.join(directory,digest(sessionID)+'.json'),JSON.stringify(record,null,2));await ctx.session.synthetic({sessionID,text:'Evaluation evidence exported to Git-local storage.',resume:false})
   }})
   editor.add({name:'agent-evaluate',description:'Operator-only disposable evaluation assignment, JSON task contract; no model request.',execute:async({sessionID,prompt})=>{
    const root=await rootOf(sessionID);const info=unwrap(await ctx.session.get({sessionID}));const t=assignment(JSON.parse(prompt.text),limits.roles[info.agent]);need(t.to===info.agent&&root===sessionID,'Evaluation role/location mismatch')
    await transact(root,d=>{need(!d.tasks[t.id],'Task already initialized');t.status='RUNNING';d.tasks[t.id]=t;const s=getState(d,sessionID,t.to);s.taskID=t.id});await ctx.session.synthetic({sessionID,text:'Evaluation assignment initialized.',resume:false})
   }})
  })
  await ctx.session.hook('prompt',async event=>{
   const root=await rootOf(event.sessionID),info=unwrap(await ctx.session.get({sessionID:event.sessionID}))
   stopTimer(event.sessionID)
   await transact(root,d=>{const old=d.sessions[event.sessionID];const active=Object.values(d.tasks).find(t=>t.to===info.agent&&t.status==='RUNNING');
    d.sessions[event.sessionID]={role:info.agent,taskID:active?.id??old?.taskID??null,started:Date.now(),calls:0,searches:0,pages:0,sources:old?.sources??[],denied:0,modelSteps:0,closed:false}
   })
  })
  await ctx.session.hook('context',async event=>{
   const root=await rootOf(event.sessionID)
   const info=await transact(root,d=>{const s=getState(d,event.sessionID,event.agent);const t=taskFor(d,s);s.modelSteps=(s.modelSteps??0)+1;return {s:structuredClone(s),t:structuredClone(t)}})
   const {s,t}=info;arm(root,event.sessionID,s,t)
   event.options??={};event.options.maxTokens=event.agent==='researcher'||event.agent==='reviewer'?1800:4000
   const exhausted=s.closed||s.modelSteps>=t.budget.steps-1||s.calls>=t.budget.tools-1||Date.now()-s.started>=t.budget.seconds*1000
   if(event.tools)for(const name of Object.keys(event.tools))if(!native.has(name)||(exhausted&&name!=='agent_contracts'))delete event.tools[name]
   event.system.push({type:'text',text:'Trusted task contract: '+JSON.stringify(t)+'. Budget includes skill loads. Read agent_contracts status for actual sources and counters. Submit the handoff through agent_contracts submit; a raw final response is not a validated handoff. '+(exhausted?'Tools exhausted: submit existing evidence as PARTIAL or INSUFFICIENT; do not retry.':'')})
  })
  await ctx.session.hook('retry',event=>{if(event.attempt>=1)event.decision={retry:false}})
  await ctx.session.hook('model.request',async event=>{
   const model=event.model?.id??''
   if(event.model?.providerID==='nvidia'||model.startsWith('nvidia/')||model.includes('nemotron'))await reserveNvidia(limits.providerLimits.nvidia)
  })
  await ctx.tool.transform(editor=>{
   for(const info of editor.list()){
    if(info.id==='agent_contracts')continue
    editor.update(info.id,tool=>{
     // Keep permitted tools on the native list when execute/Code Mode is denied.
     if(native.has(info.id))tool.options={...tool.options,codemode:false}
     const original=tool.execute;audit.set(info.id,{id:info.id,executor:typeof original==='function',recognized:native.has(info.id)})
     if(typeof original!=='function')return
     tool.execute=async(input,c)=>{
      const root=await rootOf(c.sessionID),role=c.agent??unwrap(await ctx.session.get({sessionID:c.sessionID})).agent
      let delegate
      const state=await transact(root,async d=>{
       const s=getState(d,c.sessionID,role),t=taskFor(d,s)
       try{
        need(!s.closed,'Task closed');need(info.id!=='grep','Native grep cannot enforce file exclusions; use project_search');need(s.calls<t.budget.tools-1,'Final tool slot reserved for handoff');need(native.has(info.id),'Unclassified tool denied: '+info.id)
        if(info.id==='subagent'){
         need(role==='poseidon','Only Poseidon delegates');need(roles.includes(input.agent)&&input.agent!=='poseidon','Invalid delegation target')
         delegate=Object.values(d.tasks).find(x=>x.to===input.agent&&x.status==='ASSIGNED');need(delegate,'Validated assignment required before delegation');delegate.status='RUNNING'
         need(typeof input.prompt==='string','Unsupported subagent prompt schema');input={...input,prompt:input.prompt+'\nTrusted assignment: '+JSON.stringify(delegate)}
        }
        if(writes.has(info.id)){
         need(s.taskID&&t.to==='coder','Implementation requires assigned Coder task')
         for(const p of editPaths(input)){
          await scopedPath(ctx.location.directory,p,t,true)
          if(t.design||/\.(css|scss|sass|less|html?|tsx|jsx|vue|svelte)$/i.test(p)){
           const current=d.briefs[t.briefID]?.filter(b=>b.confirmed).at(-1)
           need(t.design&&current?.version===t.briefVersion&&digest(current)===t.briefHash,'Current confirmed design brief required for UI writes')
          }
         }
        }
        if(info.id==='read'){need(t.sourceTypes.includes('local'),'Local sources not approved');const p=input.path??input.filePath??input.file_path;let support=false;for(const skill of t.skills){try{const base=await realpath(fileURLToPath(new URL('../skills/'+skill+'/',import.meta.url)));const target=await realpath(path.resolve(ctx.location.directory,p));if(target.startsWith(base+path.sep))support=true}catch{}}if(!support)await scopedPath(ctx.location.directory,p,t)}
        if(info.id==='glob'||info.id==='grep'){need(t.sourceTypes.includes('local')&&t.scope.includes('.'),'Discovery requires explicit project-wide source scope; read named files instead')}
        if(info.id==='skill')need(t.skills.includes(input.id??input.name),'Skill not authorized by assignment')
        if(info.id==='websearch'||info.id==='webfetch')need(t.sourceTypes.includes('web'),'Web sources not approved')
        if(info.id.startsWith('opencode_'))need(t.sourceTypes.includes('mcp'),'MCP sources not approved')
        if(info.id==='question')need(role==='poseidon'||role==='team-lead','Only coordinator/design owner asks user questions')
        if(info.id==='poseidon_workspace')need(['settings','status','test'].includes(input.action)||(role==='poseidon'&&input.action==='end_sandbox'),'Operator configures sandbox; workers cannot configure it')
        spend(s,info.id,t.budget,Date.now());arm(root,c.sessionID,s,t)
        d.events.push({type:'admitted',tool:info.id,role,taskID:t.id});return {task:t,remaining:Math.max(1,t.budget.seconds*1000-(Date.now()-s.started))}
       }catch(e){d.events.push({type:'denied',tool:info.id,role});throw e}
      }).catch(async error=>{await transact(root,d=>{getState(d,c.sessionID,role).denied++});throw error})
      const timeout=AbortSignal.timeout(state.remaining);const signal=c.signal?AbortSignal.any([c.signal,timeout]):timeout
      let result
      try{result=await original(input,{...c,signal})}catch(e){if(!delegate)throw e;result={content:'Worker stopped: '+e.message}}
      return transact(root,d=>{
       const s=getState(d,c.sessionID,role)
       if(delegate){
        const t=d.tasks[delegate.id];const worker=Object.values(d.sessions).find(x=>x.taskID===t.id)
        t.handoff??=fallback(t,worker??{sources:[]},'Worker returned no validated handoff');t.status=t.handoff.status
        for(const [id,state]of Object.entries(d.sessions))if(state.taskID===t.id){state.closed=true;stopTimer(id)}
        return {...result,content:JSON.stringify(t.handoff)}
       }
       if(['read','project_search','webfetch','opencode_read_mcp_resource'].includes(info.id)&&s.sources.length<16){
        const content=sourceText(result),ref=input.url??(info.id==='project_search'?'Local bounded search: '+input.query:undefined)??input.path??input.filePath??input.uri??'MCP resource';s.sources.push({id:'S'+(s.sources.length+1),ref,type:info.id==='read'?'LOCAL':'RETRIEVED',retrievedAt:new Date().toISOString(),sha256:createHash('sha256').update(content).digest('hex'),excerpt:content.slice(0,16000),truncated:content.length>16000})
       }
       return result
      })
     }
    })
   }
  })
  const lifecycle=new AbortController()
  const subscription=ctx.event?.subscribe ? (async()=>{
   for await(const event of ctx.event.subscribe({types:['session.execution.succeeded','session.execution.failed','session.execution.interrupted','session.deleted','session.archived'],signal:lifecycle.signal})){
    const id=event.data?.sessionID??event.sessionID
    if(!id||!timers.has(id))continue
    stopTimer(id)
    try{const root=await rootOf(id);await transact(root,d=>{const s=d.sessions[id];if(!s||s.closed)return;const t=taskFor(d,s);s.closed=true;s.handoff??=fallback(t,s,event.type);if(d.tasks[t.id]){d.tasks[t.id].handoff??=s.handoff;d.tasks[t.id].status=d.tasks[t.id].handoff.status}})}catch{}
   }
  })().catch(()=>{}) : Promise.resolve()
  return async()=>{lifecycle.abort();for(const id of timers.keys())stopTimer(id);await subscription;await Promise.allSettled([...locks.values()]);locks.clear();audit.clear()}
 }
}
