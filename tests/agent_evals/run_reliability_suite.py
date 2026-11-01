"""Serial, frozen-bundle evaluation. Records NOT_RUN rather than inventing provider results."""
import argparse,hashlib,json,shutil,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[2]
FIXTURE=Path(__file__).parent/'reliability'
def main():
 p=argparse.ArgumentParser();p.add_argument('--bundle',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--phase',choices=['before','after'],required=True);p.add_argument('--case');p.add_argument('--timeout',type=int,default=90);a=p.parse_args()
 cases=json.loads((FIXTURE/'cases.json').read_text());a.output.mkdir(parents=True,exist_ok=True)
 frozen=Path(tempfile.mkdtemp(prefix='reliability-frozen-',dir='/private/tmp'))/'.opencode';shutil.copytree(a.bundle,frozen,ignore=shutil.ignore_patterns('__pycache__'));a.bundle=frozen
 manifest={str(f.relative_to(a.bundle)):hashlib.sha256(f.read_bytes()).hexdigest() for f in a.bundle.rglob('*') if f.is_file() and '__pycache__' not in f.parts}
 (a.output/'bundle-fingerprint.json').write_text(json.dumps(manifest,indent=2))
 rows=[]
 for case in cases['baseline']+cases['regressions']+(cases['prepared'] if a.case else []):
  if a.case and case['id']!=a.case:continue
  directory=Path(tempfile.mkdtemp(prefix='reliability-'+a.phase+'-',dir='/private/tmp'))
  shutil.copytree(FIXTURE,directory,dirs_exist_ok=True);shutil.copytree(a.bundle,directory/'.opencode',ignore=shutil.ignore_patterns('__pycache__'));subprocess.run(['git','init','-q',str(directory)],check=True)
  prompt=a.output/(case['id']+'.prompt.txt');prompt.write_text(case['prompt']+'\nUse your role contract and submit a valid handoff if the installed bundle supports it. Keep the human summary under 300 words.\n')
  report=a.output/(case['id']+'.json');cmd=[sys.executable,str(Path(__file__).parent/'run_eval.py'),'--directory',str(directory),'--agent',case['role'],'--prompt',str(prompt),'--output',str(report),'--timeout',str(a.timeout),'--tools','12']
  if a.phase=='after':
   assignment={'id':case['id'],'to':case['role'],'objective':'Evaluate '+case['id'],'question':case['prompt'],'purpose':'Controlled role evaluation','scope':case.get('scope', [name for name in ['source.md','conflicting.md','injection.md','standards.md','eligibility.py','test_eligibility.py'] if name in case['prompt']] or ['source.md']),'exclusions':[],'sourceTypes':['local'],'skills':['karpathy-guidelines'] if case['role']=='researcher' else ['grilling','karpathy-guidelines'] if case['role']=='poseidon' else [],'acceptance':['Preserve requirements and scope','Return attributable evidence and explicit uncertainty'],'nextAction':'Return bounded handoff','design':False}
   if case['role']=='team-lead':
    # Team Lead is evaluated directly: its primary contract is a bounded plan, not a self-delegation.
    pass
   else:
    af=a.output/(case['id']+'.assignment.json');af.write_text(json.dumps(assignment));cmd+=['--assignment',str(af)]
  started=time.monotonic()
  try:
   run=subprocess.run(cmd,capture_output=True,text=True,timeout=a.timeout+60)
   (a.output/(case['id']+'.log')).write_text(run.stdout+'\n'+run.stderr)
   result=json.loads(report.read_text()) if report.exists() else {'status':'NOT_RUN','reason':run.stderr[-1500:]}
   row={'case':case['id'],'role':case['role'],'exitCode':run.returncode,'status':result.get('outcome',result.get('status','INCOMPLETE')),'seconds':round(time.monotonic()-started,2),'toolAttempts':len(result.get('tools',[])),'changedFiles':result.get('changed_files',[]),'errors':result.get('errors',[]),'behavioralGrade':'REQUIRES_SOURCE_AND_OUTPUT_REVIEW'}
  except subprocess.TimeoutExpired as e:
   row={'case':case['id'],'role':case['role'],'status':'NOT_RUN','reason':'Harness outer timeout; inspect cleanup before continuing'};rows.append(row);break
  rows.append(row);(a.output/'summary.json').write_text(json.dumps(rows,indent=2));print(json.dumps(row),flush=True)
 (a.output/'summary.json').write_text(json.dumps(rows,indent=2))
if __name__=='__main__':main()
