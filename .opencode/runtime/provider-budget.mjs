/** Shared rolling quota for requests admitted by these plugins. Stores no credentials. */
import { mkdir, readFile, writeFile, rename, rm, lstat } from 'node:fs/promises'
import path from 'node:path'
import { homedir } from 'node:os'
import { randomUUID } from 'node:crypto'
export const defaultQuotaFile = () => path.join(process.env.XDG_STATE_HOME || path.join(homedir(),'.local/state'), 'opencode-agent-reliability/nvidia-requests.json')
export async function reserveNvidia({file=defaultQuotaFile(),now=Date.now(),requestsPerMinute=20,requestsPerDay=1000}={}) {
  if(![now,requestsPerMinute,requestsPerDay].every(Number.isSafeInteger)||now<0||requestsPerMinute<1||requestsPerMinute>20||requestsPerDay<1||requestsPerDay>1000)throw Error('Invalid NVIDIA quota configuration')
  await mkdir(path.dirname(file),{recursive:true,mode:0o700})
  const lock=file+'.lock';let owned=false;const temp=file+'.'+randomUUID()+'.tmp'
  try {
    try{await mkdir(lock,{mode:0o700});owned=true}catch(e){if(e.code==='EEXIST')throw Error('NVIDIA quota state busy; no request admitted');throw e}
    let entries=[]
    try {
      if((await lstat(file)).isSymbolicLink())throw Error('NVIDIA quota file cannot be a symlink')
      const state=JSON.parse(await readFile(file,'utf8'))
      if(state.version!==1||!Array.isArray(state.requests)||state.requests.length>1000||!state.requests.every(t=>Number.isSafeInteger(t)&&t>=0))throw Error('Invalid NVIDIA quota state; no request admitted')
      entries=state.requests.filter(t=>t>now-86400000)
    }catch(e){if(e.code!=='ENOENT')throw e}
    // Rolling windows are conservative across calendar reset boundaries. Future stamps
    // remain charged if the system clock moves backwards.
    const recent=entries.filter(t=>t>now-60000)
    if(recent.length>=requestsPerMinute)throw Error('NVIDIA 20 requests/minute limit reached; stop and retry in a later minute')
    if(entries.length>=requestsPerDay)throw Error('NVIDIA 1000 requests/day limit reached; no further requests admitted')
    entries.push(now)
    await writeFile(temp,JSON.stringify({version:1,requests:entries}),{mode:0o600,flag:'wx'})
    await rename(temp,file)
    return {minute:recent.length+1,day:entries.length}
  }finally{await rm(temp,{force:true});if(owned)await rm(lock,{recursive:true})}
}
