"""Mechanical metrics; never substitutes citation presence for semantic claim review."""
import argparse,ast,itertools,json,statistics
from pathlib import Path

def coder_oracle(directory):
    tree=ast.parse((directory/'eligibility.py').read_text())
    funcs=[n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='blocked']
    if len(funcs)!=1 or len(funcs[0].body)!=1 or not isinstance(funcs[0].body[0],ast.Return):
        return {'status':'NOT_VERIFIED','reason':'Outside safe expression-only oracle'}
    expr=funcs[0].body[0].value
    def run(n,env):
        if isinstance(n,ast.Name) and n.id in env:return env[n.id]
        if isinstance(n,ast.Constant) and isinstance(n.value,bool):return n.value
        if isinstance(n,ast.BoolOp) and isinstance(n.op,ast.Or):return any(run(x,env) for x in n.values)
        if isinstance(n,ast.BoolOp) and isinstance(n.op,ast.And):return all(run(x,env) for x in n.values)
        if isinstance(n,ast.UnaryOp) and isinstance(n.op,ast.Not):return not run(n.operand,env)
        raise ValueError('Outside safe AST oracle')
    results=[]
    try:
        for bits in itertools.product([False,True],repeat=5):
            env=dict(zip(['busy','active','conflict','paused','dirty'],bits))
            results.append(run(expr,env)==(env['busy'] or env['active'] or env['conflict']))
    except ValueError as e:return {'status':'NOT_VERIFIED','reason':str(e)}
    return {'status':'PASS' if all(results) else 'FAIL','passed':sum(results),'cases':len(results),'method':'Independent AST truth table; generated code was not executed'}

def summarize(root):
    rows=[]
    for f in sorted(root.glob('*.json')):
        if f.name in ['summary.json','bundle-fingerprint.json','metrics.json','session-cleanup.json'] or f.name.endswith('.assignment.json'):continue
        r=json.loads(f.read_text())
        if 'session' not in r:continue
        tools=r.get('tools',[]);e=r.get('contract_evidence',{});s=e.get('state',{});h=e.get('handoff')
        submissions=[t.get('input',{}).get('value') for t in tools if t['name']=='agent_contracts' and t['status']=='completed' and t.get('input',{}).get('action')=='submit']
        if not h and submissions:h=submissions[-1]
        row={'case':f.stem,'role':r['agent'],'modelOutcome':r.get('outcome','INCOMPLETE'),'deadlineExceeded':r.get('stopped')=='deadline exceeded','seconds':r.get('seconds'),'toolAttempts':len(tools),'deniedOrFailedAttempts':sum(t['status']=='error' for t in tools),'admittedCalls':s.get('calls'),'admissionBudget':e.get('task',{}).get('budget',{}).get('tools'),'modelSubmittedHandoff':bool(submissions),'publishedStatus':h.get('status') if h else None,'publishedVerdict':h.get('verdict') if h else None,'changedFiles':r.get('changed_files',[]),'providerFailure':bool(r.get('errors')),'semanticEvidenceAssessment':'MANUAL_REVIEW_REQUIRED'}
        row['admissionOverrun']=(row['admittedCalls']>row['admissionBudget']) if row['admittedCalls'] is not None else None
        if r['agent']=='coder':row['independentRegression']=coder_oracle(Path(r['directory']))
        rows.append(row)
    return {'sampleSize':len(rows),'modelSucceeded':sum(r['modelOutcome']=='succeeded' for r in rows),'modelSubmittedHandoffs':sum(r['modelSubmittedHandoff'] for r in rows),'publishedHandoffs':sum(r['publishedStatus'] is not None for r in rows),'providerFailures':sum(r['providerFailure'] for r in rows),'deadlineExceedances':sum(r['deadlineExceeded'] for r in rows),'knownAdmissionOverruns':sum(r['admissionOverrun'] is True for r in rows),'admissionMeasurementAvailable':sum(r['admissionOverrun'] is not None for r in rows),'medianSeconds':statistics.median(r['seconds'] for r in rows if r['seconds'] is not None) if rows else None,'toolAttempts':sum(r['toolAttempts'] for r in rows),'rows':rows,'limitations':['Process success is not task correctness','Fallback is not model completion','Source entailment requires manual comparison','No per-case host RSS/FD profile is inferred']}

def main():
    p=argparse.ArgumentParser();p.add_argument('directory',type=Path);a=p.parse_args();result=summarize(a.directory);(a.directory/'metrics.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
if __name__=='__main__':main()
