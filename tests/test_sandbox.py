"""Lifecycle integration with real Git/source snapshots and a deterministic Docker double."""
import json
from pathlib import Path
import subprocess
import sys
import tarfile
import tempfile
import unittest
from unittest.mock import patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.opencode/runtime'))
import runtime as b
import sandbox as s


class Docker:
    def __init__(self, session):
        self.session = session
        self.exists = False
        self.image = True
        self.calls = []
        self.execute_real = b.execute
        self.run_real = subprocess.run
        self.labels = {'runtime.project': session.project, 'runtime.session': session.key}
        self.copied = []

    def execute(self, argv, **kwargs):
        if argv[0] != 'docker':
            return self.execute_real(argv, **kwargs)
        self.calls.append(argv)
        if argv[1:3] == ['container', 'inspect']:
            if not self.exists:
                raise b.SandboxError('No such container')
            return json.dumps([{'State': {'Running': True}, 'Config': {'Labels': self.labels}}]).encode()
        if argv[1:3] == ['image', 'inspect']:
            if not self.image:
                raise b.SandboxError('No such image')
            return b'sha256:fixture-image\n'
        if argv[1] == 'run':
            self.exists = True
            return b'container-id\n'
        if argv[1] == 'rm':
            self.exists = False
        return b''

    def run(self, argv, **kwargs):
        if argv[0] != 'docker':
            return self.run_real(argv, **kwargs)
        self.calls.append(argv)
        if 'stdin' in kwargs:
            with tarfile.open(fileobj=kwargs['stdin'], mode='r') as archive:
                self.copied.append(archive.getnames())
        return subprocess.CompletedProcess(argv, 0, b'', b'')


class SandboxTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        b.execute(['git', 'init', '-q', str(self.root)])
        b.git(self.root, 'config', 'user.email', 'test@example.invalid')
        b.git(self.root, 'config', 'user.name', 'Test')
        (self.root / 'app.py').write_text('print("hello")\n')
        (self.root / '.gitignore').write_text('.env\nnode_modules/\n')
        b.git(self.root, 'add', '.')
        b.git(self.root, 'commit', '-qm', 'fixture')
        self.policy = json.loads((b.BUNDLE / 'runtime/settings.example.json').read_text())['policy']
        self.settings = s.save(self.root, self.policy, {})
        self.session = s.SessionSandbox(self.root, 'opencode-session')
        self.docker = Docker(self.session)
        for target, method, fake in ((b, 'execute', self.docker.execute), (s.subprocess, 'run', self.docker.run)):
            patcher = patch.object(target, method, side_effect=fake)
            patcher.start()
            self.addCleanup(patcher.stop)

    def tearDown(self):
        self.tmp.cleanup()

    def test_settings_persist_without_dirtying_source(self):
        self.assertEqual(s.load(self.root), self.settings)
        self.assertEqual(b.git(self.root, 'status', '--porcelain'), b'')
        self.assertTrue(str(s.settings_path(self.root)).endswith('.git/bdfl/settings.json'))

    def test_request_reuses_container_end_removes_and_resume_recreates(self):
        first = self.session.ensure()
        self.assertEqual(self.session.ensure(), first)
        self.assertEqual(len([cmd for cmd in self.docker.calls if cmd[1] == 'run']), 1)
        self.session.end()
        self.assertFalse(self.docker.exists)
        self.assertTrue(s.settings_path(self.root).exists())
        with self.assertRaisesRegex(b.SandboxError, 'ended'):
            self.session.active(self.settings)
        self.session.ensure()
        self.assertEqual(len([cmd for cmd in self.docker.calls if cmd[1] == 'run']), 2)
        run = next(cmd for cmd in self.docker.calls if cmd[1] == 'run')
        for flag in ('--network=none', '--read-only', '--cap-drop=ALL', '--user=65534:65534', '--pull=never'):
            self.assertIn(flag, run)
        self.assertNotIn('--mount', run)

    def test_concurrent_sessions_have_separate_names_and_cleanup(self):
        other = s.SessionSandbox(self.root, 'another-session')
        self.assertNotEqual(other.name, self.session.name)
        self.session.ensure()
        self.session.end()
        removed = next(cmd for cmd in self.docker.calls if cmd[1] == 'rm')
        self.assertEqual(removed[-1], self.session.name)

    def test_missing_image_is_built_from_sanitized_snapshot_and_recipe(self):
        self.docker.image = False
        self.settings = s.save(self.root, self.policy, {'build': {'dockerfile': 'FROM python:3.13-slim\n'}})
        (self.root / '.env').write_text('private')
        def build(argv, timeout, **kwargs):
            self.assertEqual(argv[:2], ['docker', 'build'])
            context = Path(argv[-1])
            self.assertTrue((context / 'app.py').exists())
            self.assertFalse((context / '.env').exists())
            self.assertFalse((context / '.git').exists())
            self.assertEqual((context / '.bdfl-sandbox.Dockerfile').read_text(), 'FROM python:3.13-slim\n')
            self.docker.image = True
            return subprocess.CompletedProcess(argv, 0, b'built', b'')
        with patch.object(b, 'run_logged', side_effect=build) as run:
            self.session.ensure()
            self.session.end()
            self.session.ensure()
        self.assertEqual(run.call_count, 1)

    def test_archive_during_image_build_prevents_container_start(self):
        self.docker.image = False
        s.save(self.root, self.policy, {'build': {'dockerfile': 'FROM python:3.13-slim\n'}})
        def build(argv, timeout, **kwargs):
            self.session.end()
            self.docker.image = True
            return subprocess.CompletedProcess(argv, 0, b'', b'')
        with patch.object(b, 'run_logged', side_effect=build), self.assertRaisesRegex(b.SandboxError, 'ended during'):
            self.session.ensure()
        self.assertFalse(any(cmd[1] == 'run' for cmd in self.docker.calls))

    def test_cleanup_refuses_unowned_containers(self):
        self.session.ensure()
        self.docker.labels = {'runtime.project': 'another-project', 'runtime.session': self.session.key}
        with self.assertRaisesRegex(b.SandboxError, 'not owned'):
            self.session.end()
        self.assertFalse(any(cmd[1] == 'rm' for cmd in self.docker.calls))

    def test_checkpoints_copy_fresh_source_and_execute_inside_session_container(self):
        self.session.ensure()
        (self.root / '.env').write_text('secret')
        runner = s.SessionDockerTests(self.root, 'opencode-session', self.settings)
        with patch.object(b, 'run_logged', return_value=subprocess.CompletedProcess([], 0, b'PASS', b'')) as run:
            self.assertTrue(runner.run(self.root, self.policy)['passed'])
            self.assertTrue(runner.run(self.root, self.policy)['passed'])
        self.assertEqual(len(self.docker.copied), 2)
        for names in self.docker.copied:
            self.assertIn('app.py', names)
            self.assertNotIn('.env', names)
            self.assertFalse(any(name.startswith('.git/') for name in names))
        for call in run.call_args_list:
            self.assertEqual(call.args[0][:5], ['docker', 'exec', '--workdir', '/tmp/project', self.session.name])
        self.assertEqual(len([cmd for cmd in self.docker.calls if cmd[1] == 'run']), 1)

    def test_timeout_removes_container_and_ended_runner_cannot_restart_it(self):
        self.session.ensure()
        runner = s.SessionDockerTests(self.root, 'opencode-session', self.settings)
        with patch.object(b, 'run_logged', side_effect=subprocess.TimeoutExpired(['docker', 'exec'], 1)):
            result = runner.run(self.root, self.policy)
        self.assertFalse(result['passed'])
        self.assertEqual(result['records'][-1]['exit_code'], 124)
        self.assertFalse(self.docker.exists)
        with self.assertRaisesRegex(b.SandboxError, 'ended'):
            runner.run(self.root, self.policy)

    def test_active_settings_cannot_silently_change(self):
        self.session.ensure()
        changed = s.save(self.root, self.policy, {'memory': '4g'})
        with self.assertRaisesRegex(b.SandboxError, 'configuration changed'):
            self.session.ensure(changed)
        self.session.end()
        self.assertEqual(self.session.ensure()['config']['memory'], '4g')

    def test_first_request_without_settings_reports_configuration_needed(self):
        s.settings_path(self.root).unlink()
        self.assertEqual(s.SessionSandbox(self.root, 'new').ensure()['status'], 'needs_configuration')

    def test_invalid_host_executable_and_resource_settings_are_rejected(self):
        for config in ({'docker': '/tmp/docker'}, {'memory': 'unlimited'}, {'context': 'x', 'host': 'y'}, {'cpus': 0}):
            with self.subTest(config=config), self.assertRaises(b.SandboxError):
                s.save(self.root, self.policy, config)


    def test_repeated_end_does_not_require_docker_after_verified_removal(self):
        self.session.ensure()
        self.session.end()
        with patch.object(b, 'execute', side_effect=AssertionError('No Docker call needed')):
            self.assertEqual(self.session.end()['status'], 'removed')

    def test_cancelled_image_process_is_terminated_without_waiting_for_timeout(self):
        with self.assertRaisesRegex(b.SandboxError, 'preparation cancelled'):
            b.run_logged([sys.executable, '-c', 'import time; time.sleep(60)'], timeout=60, cancelled=lambda: True)


if __name__ == '__main__':
    unittest.main()
