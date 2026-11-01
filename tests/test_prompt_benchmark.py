import importlib.util
import json
from pathlib import Path
import tempfile
import unittest

SCRIPT=Path(__file__).resolve().parents[1]/'benchmarks/prompt_effectiveness/benchmark.py'
spec=importlib.util.spec_from_file_location('prompt_benchmark',SCRIPT)
b=importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)

class PromptBenchmarkTests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory();self.addCleanup(self.temp.cleanup)
        self.root=Path(self.temp.name);self.store=self.root/'store';self.agents=self.root/'bundle/agents';self.agents.mkdir(parents=True)
        for role in b.ROLES:
            (self.agents/(role+'.md')).write_text('---\n'+json.dumps({'model':'same-model','mode':'subagent','permissions':[]})+'\n---\nBaseline instructions.\n')
        self.workspace=self.root/'app';self.workspace.mkdir();(self.workspace/'app.txt').write_text('starting state')
        b.snapshot(self.store,'before',self.agents)
        for p in self.agents.glob('*.md'):p.write_text(p.read_text().replace('Baseline instructions.','Candidate outcome instructions.'))
        b.snapshot(self.store,'after',self.agents)

    def prepare(self,variant,repeat=1,environment='same-browser-runtime',request=None):
        return b.prepare(self.store,variant,'editor-obvious-problems',repeat,self.workspace,environment,request)

    def review(self,run,rating=5,status='PASS'):
        directory=self.store/'runs'/run['run_id'];r=b.read(directory/'review.template.json')
        r.update(assessor='Fixture assessor',outcome='COMPLETED',rubric_ratings=dict.fromkeys(b.grader.WEIGHTS,rating),snapshot_used={'status':'CONFIRMED','evidence':'Fixture: checked loaded snapshot identity'})
        for c in r['critical_checks']:c.update(status=status,evidence='Fixture observed action/result')
        (directory/'transcript.txt').write_text('Synthetic test evidence, not a live model evaluation.')
        r['evidence_files']=['transcript.txt'];path=directory/'review.json';b.write_new(path,r)
        return path

    def test_snapshot_is_immutable_and_tampering_is_detected(self):
        with self.assertRaises(ValueError):b.snapshot(self.store,'before',self.agents)
        (self.store/'snapshots/before/coder.md').write_text('changed')
        with self.assertRaises(ValueError):b.load_variant(self.store,'before')

    def test_prepared_run_is_unscored_and_freezes_actual_request(self):
        req=self.root/'request.txt';req.write_text('My actual wording.')
        r=self.prepare('before',request=req);d=self.store/'runs'/r['run_id']
        self.assertEqual((d/'request.txt').read_text(),'My actual wording.')
        self.assertFalse((d/'assessment.json').exists())
        with self.assertRaises(ValueError):self.prepare('before',request=req)

    def test_frozen_criteria_cannot_be_deleted_or_marked_not_applicable(self):
        r=self.prepare('before');path=self.review(r);review=b.read(path)
        review['critical_checks'].pop();path.write_text(json.dumps(review))
        with self.assertRaises(ValueError):b.score(self.store,r['run_id'],path)
        review=b.read(path.parent/'review.template.json');review.update(assessor='A',outcome='COMPLETED',evidence_files=['transcript.txt']);review['critical_checks'][0]['status']='NOT_APPLICABLE';path.write_text(json.dumps(review))
        with self.assertRaises(ValueError):b.score(self.store,r['run_id'],path)

    def test_pending_or_unsupported_reviews_do_not_receive_scores(self):
        r=self.prepare('before');d=self.store/'runs'/r['run_id']
        with self.assertRaises(ValueError):b.score(self.store,r['run_id'],d/'review.template.json')
        path=self.review(r);review=b.read(path);review['evidence_files']=['missing.txt'];path.write_text(json.dumps(review))
        with self.assertRaises(OSError):b.score(self.store,r['run_id'],path)

    def test_critical_failure_blocks_even_high_scored_presentation(self):
        r=self.prepare('before');result=b.score(self.store,r['run_id'],self.review(r,10,'FAIL'))
        self.assertEqual(result['weighted_score'],10);self.assertEqual(result['readiness'],'BLOCKED')

    def test_comparable_prompt_only_pair_has_delta_without_claiming_significance(self):
        for variant,rating in [('before',4),('after',7)]:
            r=self.prepare(variant);b.score(self.store,r['run_id'],self.review(r,rating))
        result=b.compare(self.store,'before','after')
        self.assertEqual(result['paired_runs'],1);self.assertEqual(result['mean_task_score_delta'],3)
        self.assertEqual(result['distinct_scored_tasks'],1);self.assertIsNone(result['two_sided_sign_test_p'])

    def test_environment_source_and_requirements_changes_are_excluded(self):
        a=self.prepare('before');b.score(self.store,a['run_id'],self.review(a))
        (self.workspace/'app.txt').write_text('different initial artifact')
        request=self.root/'new-request.txt';request.write_text('Different requirements')
        c=self.prepare('after',environment='different-browser',request=request);b.score(self.store,c['run_id'],self.review(c))
        result=b.compare(self.store,'before','after');self.assertEqual(result['paired_runs'],0)
        why=result['excluded_pairs'][0]['reasons'];self.assertIn('Starting workspace differs',why);self.assertIn('environment differs',why);self.assertIn('requestHash differs',why)

    def test_model_permission_or_runtime_changes_are_not_prompt_only(self):
        a=self.prepare('before');b.score(self.store,a['run_id'],self.review(a))
        p=self.agents/'coder.md';p.write_text(p.read_text().replace('same-model','different-model'));b.snapshot(self.store,'confounded',self.agents)
        c=self.prepare('confounded');b.score(self.store,c['run_id'],self.review(c))
        result=b.compare(self.store,'before','confounded');self.assertEqual(result['paired_runs'],0);self.assertIn('nonPromptHash differs',result['excluded_pairs'][0]['reasons'])

    def test_run_and_scored_packet_integrity_and_no_overwrite(self):
        r=self.prepare('before');path=self.review(r);b.score(self.store,r['run_id'],path)
        with self.assertRaises(FileExistsError):b.score(self.store,r['run_id'],path)
        packet=path.parent/'assessment.json';v=b.read(packet);v['result']['weighted_score']=10;packet.write_text(json.dumps(v))
        with self.assertRaises(ValueError):b.compare(self.store,'before','after')

    def test_missing_counterpart_is_visible_not_a_zero_score(self):
        r=self.prepare('before');b.score(self.store,r['run_id'],self.review(r))
        result=b.compare(self.store,'before','after');self.assertEqual(result['paired_runs'],0);self.assertEqual(result['excluded_pairs'][0]['reasons'],['Missing scored counterpart'])

    def test_infrastructure_failure_does_not_become_a_prompt_regression(self):
        a=self.prepare('before');b.score(self.store,a['run_id'],self.review(a,8))
        c=self.prepare('after');path=self.review(c,0);r=b.read(path);r['outcome']='INFRASTRUCTURE_FAILURE';path.write_text(json.dumps(r));b.score(self.store,c['run_id'],path)
        result=b.compare(self.store,'before','after');self.assertEqual(result['paired_runs'],0);self.assertIn('Infrastructure failure; no prompt-effect attribution',result['excluded_pairs'][0]['reasons'])

    def test_evidence_is_archived_and_independent_of_mutable_original_file(self):
        for variant in ('before','after'):
            r=self.prepare(variant);path=self.review(r);b.score(self.store,r['run_id'],path)
            (path.parent/'transcript.txt').unlink()
        self.assertEqual(b.compare(self.store,'before','after')['paired_runs'],1)
        directory=self.store/'runs'/'before--editor-obvious-problems--1'
        packet=b.read(directory/'assessment.json');archived=directory/next(iter(packet['archivedEvidence'].values()));archived.write_text('changed')
        with self.assertRaises(ValueError):b.compare(self.store,'before','after')
