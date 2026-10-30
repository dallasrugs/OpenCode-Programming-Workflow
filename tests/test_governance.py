"""Offline integration tests: real Git, deterministic fake LLMs, no provider calls."""
import importlib.util
import json
import os
from pathlib import Path
import subprocess
import tempfile
import unittest
from unittest.mock import patch

MODULE = Path(__file__).resolve().parents[1] / '.opencode/governance/bdfl.py'
spec = importlib.util.spec_from_file_location('bdfl', MODULE)
b = importlib.util.module_from_spec(spec)
spec.loader.exec_module(b)


def specification(**changes):
    return dict(objective='Correct greeting', design='Change greeting, preserve interface; test behavior',
                migration='Not needed', acceptance=['Greeting is hello'], constraints=['No new dependencies'],
                allowed_paths=['app.py', 'new.py'], breaking_change=False, major_architecture=False,
                skills=['code-quality'], **changes)


class Backend:
    def __init__(self, plan_decisions=None, reviews=None, integrations=None):
        self.calls = []
        self.plan_decisions = list(plan_decisions or ['APPROVE'])
        self.reviews = list(reviews or ['PASS'])
        self.integrations = list(integrations or ['APPROVE'])
        self.mutate_review = False
        self.missed_breaking = False

    def call(self, role, stage, context, root, allowed):
        self.calls.append((role, stage))
        if stage == 'plan':
            return {'spec': specification()}
        if stage == 'plan-review':
            return dict(decision=self.plan_decisions.pop(0), rationale='Architecture assessed', constraints=[],
                        breaking_change=self.missed_breaking, major_architecture=False,
                        memory={'map': 'app.py owns greeting', 'invariants': ['stable interface'], 'adrs': ['no framework']})
        if stage == 'rubric':
            return {'rubric': ['Greeting is hello; execute behavior test; preserve API']}
        if stage == 'implement':
            assert 'app.py' in allowed
            (root / 'app.py').write_text('greeting = "hello"\n')
            (root / 'new.py').write_text('# approved addition\n')
            return {'decision': 'SUBMIT', 'rationale': 'Greeting corrected'}
        if stage == 'review':
            if self.mutate_review:
                (root / 'app.py').write_text('# illicit change\n')
            d = self.reviews.pop(0)
            return {'decision': d, 'rationale': 'Independent review', 'findings': [] if d == 'PASS' else [
                {'severity': 'high', 'file': 'app.py', 'line': 1, 'message': 'Fix greeting'}]}
        if stage == 'integration':
            return {'decision': self.integrations.pop(0), 'rationale': 'Integration assessed'}
        if stage == 'report':
            return {'summary': 'Greeting fixed, tests passed; candidate awaits user integration.'}
        raise AssertionError(stage)


class Runner:
    def __init__(self, results=None):
        self.results = list(results or [True])
        self.calls = 0

    def run(self, root, policy):
        self.calls += 1
        passed = self.results.pop(0)
        return {'passed': passed, 'records': [{'argv': ['test'], 'exit_code': 0 if passed else 1,
                                            'stdout': 'actual deterministic fixture', 'stderr': ''}]}


class WorkflowTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        b.execute(['git', 'init', '-q', str(self.root)])
        b.git(self.root, 'config', 'user.email', 'test@example.invalid')
        b.git(self.root, 'config', 'user.name', 'Test')
        (self.root / 'app.py').write_text('greeting = "hi"\n')
        (self.root / 'untouched.txt').write_text('keep\n')
        b.git(self.root, 'add', '.')
        b.git(self.root, 'commit', '-qm', 'fixture')
        self.store = b.Store(self.root, 'a123456789ab')
        self.policy = json.loads((b.BUNDLE / 'governance/policy.example.json').read_text())

    def tearDown(self):
        self.tmp.cleanup()

    def start(self, authorized=True):
        return b.start(self.store, 'Correct greeting', self.policy, authorized)

    def test_full_workflow_and_real_patch_with_new_files(self):
        state, backend, runner = self.start(), Backend(), Runner()
        c = b.Controller(self.store, backend, runner)
        c.advance(state)
        self.assertEqual(state['phase'], 'READY')
        self.assertEqual(runner.calls, 1)
        self.assertEqual([s for _, s in backend.calls], ['plan', 'plan-review', 'rubric', 'implement', 'review', 'integration', 'report'])
        self.assertLess(backend.calls.index(('reviewer', 'rubric')), backend.calls.index(('coder', 'implement')))
        patch_text = (self.store.directory / 'candidate.patch').read_text()
        self.assertIn('new file mode', patch_text)
        self.assertIn('hello', patch_text)
        self.assertEqual((self.root / 'app.py').read_text(), 'greeting = "hi"\n')
        self.assertEqual(b.git(state['worktree'], 'diff', '--cached'), b'')
        self.assertTrue((self.store.home / 'architecture.json').exists())

    def test_authorization_bound_to_exact_specification(self):
        state, backend = self.start(False), Backend()
        c = b.Controller(self.store, backend, Runner())
        c.advance(state)
        self.assertEqual(state['phase'], 'AWAITING_BDFL')
        self.assertNotIn(('coder', 'implement'), backend.calls)
        with self.assertRaises(b.GateError):
            b.authorize(self.store, state, 'stale', 'approved')
        b.authorize(self.store, state, state['spec_hash'], 'BDFL approves this exact design')
        c.advance(state)
        self.assertEqual(state['phase'], 'READY')

    def test_maintainer_detected_breaking_change_requires_bdfl(self):
        state, backend = self.start(), Backend()
        backend.missed_breaking = True
        b.Controller(self.store, backend, Runner()).advance(state)
        self.assertEqual(state['phase'], 'AWAITING_BDFL')
        self.assertTrue(state['spec']['breaking_change'])
        self.assertNotIn(('coder', 'implement'), backend.calls)

    def test_revise_then_approve(self):
        state, backend = self.start(), Backend(['REVISE', 'APPROVE'])
        b.Controller(self.store, backend, Runner()).advance(state)
        self.assertEqual(state['phase'], 'READY')
        self.assertEqual(state['plan_round'], 2)

    def test_escalation_never_implicitly_authorizes(self):
        state, backend = self.start(), Backend(['ESCALATE'])
        b.Controller(self.store, backend, Runner()).advance(state)
        self.assertEqual(state['phase'], 'AWAITING_BDFL')
        self.assertFalse(b.auth_valid(state))

    def test_failures_return_to_coder_with_original_rubric(self):
        state, backend, runner = self.start(), Backend(reviews=['FAIL', 'PASS']), Runner([False, True])
        b.Controller(self.store, backend, runner).advance(state)
        self.assertEqual(state['phase'], 'READY')
        self.assertEqual(state['implementation_round'], 2)
        self.assertEqual(sum(s == 'rubric' for _, s in backend.calls), 1)
        self.assertEqual(runner.calls, 2)

    def test_reviewer_pass_cannot_hide_failed_tests(self):
        state, backend = self.start(), Backend(reviews=['PASS', 'PASS', 'PASS'])
        b.Controller(self.store, backend, Runner([False, False, False])).advance(state)
        self.assertEqual(state['phase'], 'EXHAUSTED')
        self.assertNotIn(('maintainer', 'integration'), backend.calls)

    def test_maintainer_revision_requires_new_tests_and_review(self):
        state, backend, runner = self.start(), Backend(reviews=['PASS', 'PASS'], integrations=['REVISE', 'APPROVE']), Runner([True, True])
        b.Controller(self.store, backend, runner).advance(state)
        self.assertEqual(state['phase'], 'READY')
        self.assertEqual(runner.calls, 2)

    def test_post_review_edit_invalidates_all_approvals(self):
        state, backend, runner = self.start(), Backend(reviews=['PASS', 'PASS'], integrations=['APPROVE', 'APPROVE']), Runner([True, True])
        c = b.Controller(self.store, backend, runner)
        c.advance(state)
        (Path(state['worktree']) / 'app.py').write_text('greeting = "changed after review"\n')
        c.advance(state)
        self.assertEqual(state['phase'], 'READY')
        self.assertEqual(runner.calls, 2)
        self.assertTrue(any(e['event'] == 'candidate_changed_approvals_invalidated' for e in state['events']))

    def test_out_of_scope_changes_block_integration(self):
        state = self.start()
        c = b.Controller(self.store, Backend(), Runner())
        c.advance(state)
        (Path(state['worktree']) / 'untouched.txt').write_text('unauthorized\n')
        with self.assertRaises(b.GateError):
            c.advance(state)

    def test_read_only_role_mutation_is_rejected(self):
        state, backend = self.start(), Backend()
        backend.mutate_review = True
        with self.assertRaisesRegex(b.GateError, 'Read-only role'):
            b.Controller(self.store, backend, Runner()).advance(state)
        self.assertNotEqual(state['phase'], 'READY')

    def test_policy_and_spec_tampering_rejected(self):
        state = self.start(False)
        c = b.Controller(self.store, Backend(), Runner())
        c.advance(state)
        b.authorize(self.store, state, state['spec_hash'], 'approved')
        state['spec']['allowed_paths'].append('untouched.txt')
        self.assertFalse(b.auth_valid(state))
        with self.assertRaises(b.GateError):
            c.advance(state)
        state['policy']['tests']['commands'] = [['true']]
        with self.assertRaisesRegex(b.GateError, 'Policy changed'):
            c.advance(state)

    def test_repository_wide_lock_and_persistent_resume(self):
        with self.store.lock():
            with self.assertRaises(b.GateError):
                with b.Store(self.root, 'b123456789ab').lock():
                    pass
        state = self.start(False)
        b.Controller(self.store, Backend(), Runner()).advance(state)
        restored = self.store.read()
        b.authorize(self.store, restored, restored['spec_hash'], 'approved')
        b.Controller(self.store, Backend(), Runner()).advance(restored)
        self.assertEqual(self.store.read()['phase'], 'READY')

    def test_symlink_and_secret_context_excluded(self):
        (self.root / '.env').write_text('SECRET=never\n')
        with b.mirror(self.root) as mirror:
            self.assertFalse((mirror / '.env').exists())
        (self.root / 'link').symlink_to('/etc/passwd')
        with self.assertRaisesRegex(b.GateError, 'Symlink'):
            b.source_files(self.root)

    def test_exhaustion_cannot_be_revived_by_editing_candidate(self):
        state = self.start()
        c = b.Controller(self.store, Backend(reviews=['FAIL'] * 3), Runner([False] * 3))
        c.advance(state)
        self.assertEqual(state['phase'], 'EXHAUSTED')
        (Path(state['worktree']) / 'app.py').write_text('new mutation\n')
        c.advance(state)
        self.assertEqual(state['phase'], 'EXHAUSTED')

    def test_ready_resume_checks_exported_patch(self):
        state = self.start()
        c = b.Controller(self.store, Backend(), Runner())
        c.advance(state)
        (self.store.directory / 'candidate.patch').write_text('tampered')
        with self.assertRaisesRegex(b.GateError, 'Exported patch changed'):
            c.advance(state)

    def test_adapter_grants_only_approved_paths_and_syncs_submission(self):
        adapter = object.__new__(b.OpenCode)
        adapter.policy = self.policy
        real_execute = b.execute
        def fake_execute(argv, cwd=None, **kwargs):
            if argv[0] != 'opencode':
                return real_execute(argv, cwd=cwd, **kwargs)
            config = json.loads((cwd / '.opencode/opencode.json').read_text())
            rules = config['agents']['coder']['permissions']
            grants = [r['resource'] for r in rules if r['action'] == 'edit' and r['effect'] == 'allow']
            self.assertEqual(grants, ['app.py'])
            self.assertEqual(config['agents']['coder']['mode'], 'primary')
            self.assertIn('--standalone', argv)
            self.assertFalse((cwd / '.git').exists())
            self.assertEqual(kwargs['env']['XDG_CONFIG_HOME'].startswith('/'), True)
            self.assertEqual(kwargs['env']['PWD'], str(cwd.resolve()))
            (cwd / 'app.py').write_text('greeting = "hello"\n')
            return json.dumps({'type': 'text', 'part': {'text': json.dumps({'decision': 'SUBMIT', 'rationale': 'fixed'})}}).encode()
        with patch.object(b, 'execute', side_effect=fake_execute):
            adapter.call('coder', 'implement', {}, self.root, ['app.py'])
        self.assertIn('hello', (self.root / 'app.py').read_text())

    def test_adapter_rejects_readonly_write_and_out_of_scope_coder_output(self):
        adapter = object.__new__(b.OpenCode)
        adapter.policy = self.policy
        real_execute = b.execute
        for role in ('reviewer', 'coder'):
            def fake_execute(argv, cwd=None, **kwargs):
                if argv[0] != 'opencode':
                    return real_execute(argv, cwd=cwd, **kwargs)
                (cwd / 'untouched.txt').write_text('illicit')
                return json.dumps({'type': 'text', 'part': {'text': '{"decision":"SUBMIT"}'}}).encode()
            with self.subTest(role=role), patch.object(b, 'execute', side_effect=fake_execute):
                with self.assertRaisesRegex(b.GateError, 'outside its authority'):
                    adapter.call(role, 'review', {}, self.root, ['app.py'] if role == 'coder' else [])
            self.assertEqual((self.root / 'untouched.txt').read_text(), 'keep\n')

    def test_red_green_checkpoints_then_independent_final_gates(self):
        state = self.start()
        class TDDBackend(Backend):
            turns = 0
            def call(inner, role, stage, context, root, allowed):
                if stage != 'implement':
                    return super(TDDBackend, inner).call(role, stage, context, root, allowed)
                inner.calls.append((role, stage))
                inner.turns += 1
                if inner.turns == 1:
                    self.assertIsNone(context['latest_checkpoint'])
                    (root / 'new.py').write_text('# red test fixture\n')
                    return {'decision': 'CHECKPOINT', 'rationale': 'Run the failing behavior test before implementation'}
                if inner.turns == 2:
                    self.assertFalse(context['latest_checkpoint']['passed'])
                    (root / 'app.py').write_text('greeting = "hello"\n')
                    return {'decision': 'CHECKPOINT', 'rationale': 'Check green after the minimal fix'}
                self.assertTrue(context['latest_checkpoint']['passed'])
                return {'decision': 'SUBMIT', 'rationale': 'Red and green observed; ready for independent review'}
        runner = Runner([False, True, True])
        backend = TDDBackend()
        b.Controller(self.store, backend, runner).advance(state)
        self.assertEqual(state['phase'], 'READY')
        self.assertEqual(state['implementation_round'], 1)
        self.assertEqual(state['coder_turns'], 3)
        self.assertEqual([h['passed'] for h in state['test_checkpoints']], [False, True])
        self.assertEqual(runner.calls, 3)
        self.assertEqual(sum(stage == 'review' for _, stage in backend.calls), 1)

    def test_checkpoint_cannot_expand_source_scope(self):
        state = self.start()
        class ScopeBackend(Backend):
            def call(inner, role, stage, context, root, allowed):
                if stage != 'implement':
                    return super(ScopeBackend, inner).call(role, stage, context, root, allowed)
                (root / 'untouched.txt').write_text('unauthorized')
                return {'decision': 'CHECKPOINT', 'rationale': 'Attempt unauthorized mutation'}
        runner = Runner()
        with self.assertRaisesRegex(b.GateError, 'scope'):
            b.Controller(self.store, ScopeBackend(), runner).advance(state)
        self.assertEqual(runner.calls, 0)

    def test_checkpoint_budget_stops_without_bypassing_review(self):
        self.policy['max_test_checkpoints'] = 1
        state = self.start()
        class RepeatedCheckpoint(Backend):
            def call(inner, role, stage, context, root, allowed):
                if stage != 'implement':
                    return super(RepeatedCheckpoint, inner).call(role, stage, context, root, allowed)
                (root / 'app.py').write_text('greeting = "hello"\n')
                return {'decision': 'CHECKPOINT', 'rationale': 'Request fixed tests'}
        runner = Runner([False])
        b.Controller(self.store, RepeatedCheckpoint(), runner).advance(state)
        self.assertEqual(state['phase'], 'EXHAUSTED')
        self.assertEqual(runner.calls, 1)
        self.assertNotIn('review', state)

    def test_pending_checkpoint_resumes_after_runner_infrastructure_failure(self):
        state = self.start()
        class OneCheckpoint(Backend):
            turns = 0
            def call(inner, role, stage, context, root, allowed):
                if stage != 'implement':
                    return super(OneCheckpoint, inner).call(role, stage, context, root, allowed)
                inner.turns += 1
                (root / 'app.py').write_text('greeting = "hello"\n')
                return {'decision': 'CHECKPOINT' if inner.turns == 1 else 'SUBMIT', 'rationale': 'Fixed-policy validation'}
        class Unavailable:
            def run(inner, root, policy):
                raise b.GateError('Docker unavailable')
        backend = OneCheckpoint()
        with self.assertRaisesRegex(b.GateError, 'Docker unavailable'):
            b.Controller(self.store, backend, Unavailable()).advance(state)
        state = self.store.read()
        self.assertEqual(state['phase'], 'CHECKPOINT_TEST')
        self.assertNotIn('review', state)
        b.Controller(self.store, backend, Runner([True, True])).advance(state)
        self.assertEqual(state['phase'], 'READY')
        self.assertEqual(state['implementation_round'], 1)

    def test_catalog_update_requires_new_authorized_run(self):
        state = self.start()
        with patch.object(b.skillctl, 'sha', return_value='catalog-updated'):
            with self.assertRaisesRegex(b.GateError, 'Skill catalog/provenance changed'):
                b.Controller(self.store, Backend(), Runner()).advance(state)

    def test_plan_retries_bounded(self):
        state = self.start()
        b.Controller(self.store, Backend(['REVISE'] * 3), Runner()).advance(state)
        self.assertEqual(state['phase'], 'EXHAUSTED')
        self.assertEqual(state['plan_round'], 3)


class BoundaryTests(unittest.TestCase):
    def test_invalid_scope(self):
        for path in ('../escape', '/absolute', '.git/config', '.opencode/opencode.json',
                     'nested/opencode.json', '.env', 'secret.key', 'src/*.py', 'C:/escape'):
            with self.subTest(path=path), self.assertRaises(b.GateError):
                b.safe_path(path)

    def test_native_agents_deny_mutations_and_delegation(self):
        for role in b.ROLES:
            front, _ = b.read_agent(role)
            def resolve(action, resource='*'):
                effect = 'ask'
                for rule in front['permissions']:
                    if b.fnmatch.fnmatchcase(action, rule['action']) and b.fnmatch.fnmatchcase(resource, rule['resource']):
                        effect = rule['effect']
                return effect
            for action in ('edit', 'shell', 'subagent', 'execute', 'some_mcp_tool', 'external_directory'):
                self.assertEqual(resolve(action), 'deny', (role, action))
        self.assertEqual(set(p.stem for p in (b.BUNDLE / 'agents').glob('*.md')), set(b.ROLES))

    def test_parser_never_trusts_tool_json(self):
        with self.assertRaises(b.GateError):
            b.parse_response(json.dumps({'type': 'tool_result', 'text': '{"decision":"PASS"}'}))
        self.assertEqual(b.parse_response(json.dumps({'type': 'text', 'part': {'text': '{"decision":"PASS"}'}})), {'decision': 'PASS'})
        with self.assertRaises(b.GateError):
            b.parse_response(json.dumps({'type': 'error', 'error': 'provider failed'}))

    def test_docker_command_is_isolated_and_uses_argv(self):
        policy = json.loads((b.BUNDLE / 'governance/policy.example.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(b, 'mirror') as mirror, patch.object(b, 'run_logged') as run, patch.object(b.subprocess, 'run') as cleanup:
                mirror.return_value.__enter__.return_value = Path(tmp)
                run.return_value = subprocess.CompletedProcess([], 0, b'PASS', b'')
                result = b.DockerTests().run(Path(tmp), policy)
                argv = run.call_args_list[0].args[0]
                for flag in ('--network=none', '--read-only', '--cap-drop=ALL', '--pull=never', '--user=65534:65534'):
                    self.assertIn(flag, argv)
                self.assertIn('readonly', ' '.join(argv))
                self.assertTrue(result['passed'])
                self.assertEqual(cleanup.call_args.args[0][:3], ['docker', 'rm', '-f'])

    def test_log_capture_is_bounded(self):
        r = b.run_logged([b.sys.executable, '-c', 'import sys; print("x"*200000); print("y"*200000,file=sys.stderr)'], 10, limit=4096)
        self.assertEqual(r.returncode, 0)
        self.assertEqual(len(r.stdout), 4096)
        self.assertEqual(len(r.stderr), 4096)

    def test_test_timeout_fails_and_cleans_up_container(self):
        policy = json.loads((b.BUNDLE / 'governance/policy.example.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(b, 'mirror') as mirror, patch.object(b, 'run_logged', side_effect=subprocess.TimeoutExpired('docker', 1)), patch.object(b.subprocess, 'run') as cleanup:
                mirror.return_value.__enter__.return_value = Path(tmp)
                result = b.DockerTests().run(Path(tmp), policy)
                self.assertFalse(result['passed'])
                self.assertEqual(result['records'][0]['exit_code'], 124)
                self.assertEqual(cleanup.call_args.args[0][:3], ['docker', 'rm', '-f'])

    def test_docker_unavailable_never_executes_host_test(self):
        policy = json.loads((b.BUNDLE / 'governance/policy.example.json').read_text())
        with tempfile.TemporaryDirectory() as tmp:
            with patch.object(b, 'mirror') as mirror, patch.object(b, 'run_logged', side_effect=FileNotFoundError), patch.object(b.subprocess, 'run'):
                mirror.return_value.__enter__.return_value = Path(tmp)
                with self.assertRaisesRegex(b.GateError, 'no host fallback'):
                    b.DockerTests().run(Path(tmp), policy)


if __name__ == '__main__':
    unittest.main()
