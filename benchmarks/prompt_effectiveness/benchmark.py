"""Offline prompt-variant benchmark. No model calls, application edits, or automatic grading."""
import argparse
import hashlib
import importlib.util
import json
import os
import re
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[2]
HOME = Path(__file__).resolve().parent
ROLES = ('poseidon', 'team-lead', 'researcher', 'maintainer', 'coder', 'reviewer')
GRADER = ROOT / 'tests/agent_evals/grade_usage_review.py'
spec = importlib.util.spec_from_file_location('usage_grader', GRADER)
grader = importlib.util.module_from_spec(spec)
spec.loader.exec_module(grader)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def file_hash(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def read(path):
    return json.loads(path.read_text())


def write_new(path, value):
    with path.open('x') as f:
        json.dump(value, f, indent=2, allow_nan=False)
        f.write('\n')


def name(value, maximum=64):
    if len(value)>maximum or not re.fullmatch(r'[A-Za-z0-9][A-Za-z0-9_-]*', value):
        raise ValueError('Use a short name containing letters, numbers, underscores or hyphens')
    return value


def workspace_hash(root):
    """Source identity only: no commands, no copied application data, no symlink traversal."""
    entries, size = {}, 0
    ignored = {'.git', '.opencode', '.codex', '.agents', 'node_modules', 'dist', 'build',
               '.venv', '__pycache__', '.cache', 'coverage', '.local'}
    for directory, dirs, files in os.walk(root, followlinks=False):
        dirs[:] = sorted(d for d in dirs if d not in ignored and not (Path(directory)/d).is_symlink())
        for filename in sorted(files):
            path = Path(directory)/filename
            if path.is_symlink() or filename.startswith('.env') or re.search(r'credentials|auth\.json|\.(pem|key|log)$', filename, re.I):
                continue
            size += path.stat().st_size
            if len(entries) >= 2000 or size > 16*1024*1024:
                raise ValueError('Workspace fingerprint exceeds 2,000 files / 16 MiB; use a smaller controlled fixture')
            entries[path.relative_to(root).as_posix()] = file_hash(path)
    return {'sha256': digest(entries), 'files': entries}


def snapshot(store, variant, agents):
    target = store/'snapshots'/name(variant)
    if target.exists():
        raise ValueError('Variant already exists; snapshots are immutable')
    payloads, metadata = {}, {}
    for role in ROLES:
        path = agents/(role+'.md')
        if path.is_symlink():
            raise ValueError('Snapshot regular agent files, not mutable symlinks')
        data = path.read_bytes()
        _, front, _ = data.decode().split('---', 2)
        metadata[role] = json.loads(front)
        payloads[path.name] = data
    for dest, source in [('cases.json', HOME/'cases.json'),
                         ('rubric.json', ROOT/'tests/usage_reviews/rubric-v1.json'),
                         ('grader.py', GRADER)]:
        payloads[dest] = source.read_bytes()
    runtime = {}
    for folder in ('runtime', 'plugins', 'skills', 'skill-resources'):
        for path in sorted((agents.parent/folder).rglob('*')):
            if path.is_file() and not path.is_symlink() and '__pycache__' not in path.parts and path.suffix != '.pyc':
                runtime[path.relative_to(agents.parent).as_posix()] = file_hash(path)
    for filename in ('opencode.json', 'opencode.jsonc'):
        path = agents.parent/filename
        if path.is_file():
            runtime[filename] = file_hash(path)  # Never copy provider credentials/config content.
    record = {'variant': variant, 'createdUTC': datetime.now(timezone.utc).isoformat(),
              'agentSource': str(agents.resolve()), 'harnessHash':file_hash(Path(__file__)),
              'files': {p: hashlib.sha256(b).hexdigest() for p,b in payloads.items()},
              'roles': metadata, 'nonPromptHash': digest({'runtime': runtime, 'metadata': metadata}),
              'nonPromptFiles': runtime}
    record['snapshotHash'] = digest(record)
    target.mkdir(parents=True)
    for filename, data in payloads.items():
        (target/filename).write_bytes(data)
    write_new(target/'manifest.json', record)
    return record


def load_variant(store, variant):
    directory = store/'snapshots'/name(variant)
    value = read(directory/'manifest.json')
    if digest({k:v for k,v in value.items() if k!='snapshotHash'}) != value['snapshotHash']:
        raise ValueError('Snapshot manifest changed')
    for filename, expected in value['files'].items():
        if Path(filename).name != filename or file_hash(directory/filename) != expected:
            raise ValueError('Frozen snapshot file changed: '+filename)
    if value['harnessHash'] != file_hash(Path(__file__)):
        raise ValueError('Benchmark harness changed; restore the matching harness before using this snapshot')
    if value['files']['grader.py'] != file_hash(GRADER):
        raise ValueError('Scorer changed; use a matching version before comparing scores')
    if read(directory/'rubric.json')['weights'] != grader.WEIGHTS:
        raise ValueError('Frozen rubric and scorer disagree')
    return directory, value


def prepare(store, variant, case_id, repeat, workspace, environment, request=None):
    if not workspace.is_dir():
        raise ValueError('Starting workspace directory does not exist')
    if not 1 <= repeat <= 10000 or not environment.strip():
        raise ValueError('Positive repeat and recorded environment required')
    frozen, manifest = load_variant(store, variant)
    cases = read(frozen/'cases.json')['cases']
    case = next((c for c in cases if c['id']==case_id), None)
    if case is None:
        raise ValueError('Unknown frozen case')
    run_id = name(variant)+'--'+name(case_id)+'--'+str(repeat)
    directory = store/'runs'/name(run_id,160)
    if directory.exists():
        raise ValueError('Run already exists; retain failed runs and use a new repeat')
    request_text = request.read_text() if request else case['request']
    record = {'run_id': run_id, 'task_id': case_id, 'variant': variant, 'repeat': repeat,
              'createdUTC': datetime.now(timezone.utc).isoformat(),
              'snapshotHash': manifest['snapshotHash'], 'requestHash': digest(request_text),
              'caseHash': digest(case), 'rubricHash': manifest['files']['rubric.json'],
              'graderHash': manifest['files']['grader.py'], 'harnessHash':manifest['harnessHash'], 'nonPromptHash': manifest['nonPromptHash'],
              'workspace': str(workspace.resolve()), 'startingSource': workspace_hash(workspace),
              'environment': environment}
    record['runHash'] = digest(record)
    directory.mkdir(parents=True)
    # Keep a replayable copy of the bounded, non-secret inputs, not just their hashes.
    for relative, expected in record['startingSource']['files'].items():
        source=workspace/relative
        if source.is_symlink() or file_hash(source)!=expected:
            raise ValueError('Starting workspace changed during capture')
        destination=directory/'starting-workspace'/relative
        destination.parent.mkdir(parents=True,exist_ok=True)
        destination.write_bytes(source.read_bytes())
        if file_hash(destination)!=expected:
            raise ValueError('Starting input copy changed during capture')
    if workspace_hash(workspace)!=record['startingSource']:
        raise ValueError('Starting workspace changed during capture')
    write_new(directory/'run.json', record)
    (directory/'request.txt').write_text(request_text)
    review = {'task_id': case_id, 'artifact_id': run_id, 'variant': variant, 'repeat': repeat,
              'assessor': '', 'outcome': 'NOT_RUN', 'snapshot_used': {'status':'UNVERIFIED','evidence':''},
              'rubric_ratings': {}, 'user_overall_rating': None,
              'critical_checks': [{'id': c['id'], 'status':'UNVERIFIED',
                                  'evidence':'Pending observed outcome; do not infer a pass from code or appearance.'}
                                 for c in case['critical_checks']],
              'evidence_files': [], 'notes': 'Keep original requirements and user clarifications with the transcript.'}
    write_new(directory/'review.template.json', review)
    return record


def score(store, run_id, review_path):
    directory = store/'runs'/name(run_id,160)
    if (directory/'assessment.json').exists():
        raise FileExistsError('Assessment already exists')
    record = read(directory/'run.json')
    if digest({k:v for k,v in record.items() if k!='runHash'}) != record['runHash']:
        raise ValueError('Run metadata changed')
    frozen, manifest = load_variant(store, record['variant'])
    if record['snapshotHash'] != manifest['snapshotHash'] or digest((directory/'request.txt').read_text()) != record['requestHash']:
        raise ValueError('Run snapshot or request changed')
    case = next(c for c in read(frozen/'cases.json')['cases'] if c['id']==record['task_id'])
    review = read(review_path)
    if not review.get('assessor', '').strip() or review.get('outcome') not in ('COMPLETED','PARTIAL','FAILED','INFRASTRUCTURE_FAILURE'):
        raise ValueError('Name an assessor and an actual run outcome; NOT_RUN is not scored')
    for key in ('task_id', 'variant', 'repeat'):
        if review[key] != record[key]:
            raise ValueError('Review changed run identity')
    if review['artifact_id'] != run_id:
        raise ValueError('Review changed artifact identity')
    expected = {c['id'] for c in case['critical_checks']}
    actual = {c['id'] for c in review['critical_checks']}
    if any(c['status']=='NOT_APPLICABLE' for c in review['critical_checks']):
        raise ValueError('Frozen critical criteria apply to this case; use UNVERIFIED for missing evidence')
    if expected != actual:
        raise ValueError('Cannot omit or add frozen critical criteria')
    if not review.get('evidence_files'):
        raise ValueError('Attach transcript/test/output evidence before scoring')
    evidence_hashes, evidence_data = {}, {}
    if len(review['evidence_files'])>32:
        raise ValueError('Attach at most 32 evidence files')
    for reference in review['evidence_files']:
        source = (review_path.parent/reference).resolve()
        if source.stat().st_size>32*1024*1024 or sum(len(x) for x in evidence_data.values())+source.stat().st_size>32*1024*1024:
            raise ValueError('Evidence exceeds 32 MiB; use focused excerpts')
        evidence_data[reference]=source.read_bytes()
        evidence_hashes[reference] = hashlib.sha256(evidence_data[reference]).hexdigest()
    result = grader.grade(review)
    used = review.get('snapshot_used', {})
    verified = used.get('status') == 'CONFIRMED' and bool(used.get('evidence','').strip())
    result.update(outcome=review['outcome'], configuration_verified=verified)
    if review['outcome'] != 'COMPLETED' and result['readiness']=='ELIGIBLE_FOR_ACCEPTANCE':
        result['readiness'] = 'INCONCLUSIVE'
    archived={}
    for index,(reference,data) in enumerate(evidence_data.items(),1):
        path=directory/'evidence'/(str(index).zfill(3)+'-'+Path(reference).name)
        path.parent.mkdir(exist_ok=True)
        with path.open('xb') as f: f.write(data)
        archived[reference]=path.relative_to(directory).as_posix()
    packet = {'archivedEvidence':archived, 'run': record, 'review': review, 'result': result, 'evidenceHashes': evidence_hashes}
    packet['assessmentHash'] = digest(packet)
    write_new(directory/'assessment.json', packet)
    return result


def compare(store, before, after):
    if before==after:
        raise ValueError('Choose two different prompt variants')
    for variant in (before, after):
        load_variant(store, variant)
    index = {}
    for path in (store/'runs').glob('*/assessment.json'):
        row = read(path)
        if digest({k:v for k,v in row.items() if k!='assessmentHash'}) != row['assessmentHash']:
            raise ValueError('Scored assessment changed')
        for reference,relative in row['archivedEvidence'].items():
            if file_hash(path.parent/relative)!=row['evidenceHashes'][reference]:
                raise ValueError('Archived evidence changed')
        r = row['run']
        if r['variant'] not in (before,after):
            continue
        key = (r['variant'],r['task_id'],r['repeat'])
        if key in index:
            raise ValueError('Duplicate pair; do not select the best run')
        index[key] = row
    left, right, excluded = [], [], []
    tasks = sorted({(k[1],k[2]) for k in index})
    for task_id, repeat in tasks:
        a, b = index.get((before,task_id,repeat)), index.get((after,task_id,repeat))
        why = []
        if a is None or b is None:
            why.append('Missing scored counterpart')
        else:
            if any(x['result']['outcome']=='INFRASTRUCTURE_FAILURE' for x in (a,b)):
                why.append('Infrastructure failure; no prompt-effect attribution')
            for k in ('requestHash','caseHash','rubricHash','graderHash','harnessHash','nonPromptHash','environment'):
                if a['run'][k] != b['run'][k]:
                    why.append(k+' differs')
            if a['run']['startingSource']['sha256'] != b['run']['startingSource']['sha256']:
                why.append('Starting workspace differs')
            if not all(x['result']['configuration_verified'] for x in (a,b)):
                why.append('Active prompt configuration not verified')
        if why:
            excluded.append({'task_id':task_id,'repeat':repeat,'reasons':why})
        else:
            left.append(a['result']);right.append(b['result'])
    result = grader.compare(left,right)
    result.update(before=before,after=after,excluded_pairs=excluded,
                  before_ready=sum(r['readiness']=='ELIGIBLE_FOR_ACCEPTANCE' for r in left),
                  after_ready=sum(r['readiness']=='ELIGIBLE_FOR_ACCEPTANCE' for r in right))
    return result


def main():
    parser=argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--store',type=Path,default=HOME/'.local')
    sub=parser.add_subparsers(dest='command',required=True)
    p=sub.add_parser('snapshot');p.add_argument('variant');p.add_argument('--agents',type=Path,default=Path.home()/'.config/opencode/agents')
    p=sub.add_parser('prepare');p.add_argument('variant');p.add_argument('case');p.add_argument('--repeat',type=int,default=1);p.add_argument('--workspace',type=Path,required=True);p.add_argument('--environment',required=True);p.add_argument('--request',type=Path)
    p=sub.add_parser('score');p.add_argument('run');p.add_argument('--review',type=Path,required=True)
    p=sub.add_parser('compare');p.add_argument('before');p.add_argument('after')
    p=sub.add_parser('status')
    a=parser.parse_args()
    try:
        if a.command=='snapshot': result=snapshot(a.store,a.variant,a.agents)
        elif a.command=='prepare': result=prepare(a.store,a.variant,a.case,a.repeat,a.workspace,a.environment,a.request)
        elif a.command=='score': result=score(a.store,a.run,a.review)
        elif a.command=='compare': result=compare(a.store,a.before,a.after)
        else:
            valid,invalid=[],{}
            for p in sorted((a.store/'snapshots').glob('*')):
                if not p.is_dir():continue
                try:load_variant(a.store,p.name);valid.append(p.name)
                except (ValueError,OSError,KeyError) as error:invalid[p.name]=str(error)
            result={'variants':valid,'incompatible_snapshots':invalid,
                    'prepared_runs':len(list((a.store/'runs').glob('*/run.json'))),
                    'scored_runs':len(list((a.store/'runs').glob('*/assessment.json'))),
                    'live_model_requests_made_by_benchmark':0}
        print(json.dumps(result,indent=2,allow_nan=False))
        return 0
    except (ValueError,KeyError,OSError,StopIteration) as error:
        print('Benchmark stopped: '+str(error))
        return 1

if __name__=='__main__':
    raise SystemExit(main())
