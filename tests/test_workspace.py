"""Native workspace tools do not authorize or orchestrate agents."""
import json
import contextlib
import io
import subprocess
import tempfile
import unittest
from unittest.mock import patch

import test_sandbox as fixtures
import workspace
import sandbox
import runtime


class WorkspaceTests(unittest.TestCase):
    setUp = fixtures.SandboxTests.setUp
    tearDown = fixtures.SandboxTests.tearDown

    def call(self, action, **values):
        return workspace.dispatch(self.root, {'action': action, 'session_id': 'opencode-session', **values})

    def test_configuration_requires_only_test_and_sandbox_settings(self):
        self.call('configure', tests=self.policy['tests'], sandbox={})
        saved = sandbox.load(self.root)
        self.assertEqual(saved['version'], 2)
        self.assertEqual(set(saved['policy']), {'tests'})
        self.assertNotIn('authorization', saved)
        self.assertEqual(runtime.git(self.root, 'status', '--porcelain'), b'')

    def test_actual_evidence_is_saved_without_a_controller_run(self):
        with patch.object(runtime, 'run_logged', return_value=subprocess.CompletedProcess([], 0, b'PASS', b'')):
            result = self.call('test', operation_id='a' * 32)
        self.assertTrue(result['passed'])
        self.assertTrue((sandbox.home(self.root) / 'evidence' / ('a' * 32 + '.json')).exists())
        self.assertFalse((sandbox.home(self.root) / 'runs').exists())
        self.assertEqual(self.call('status')['latest_test']['candidate'], result['candidate'])

    def test_source_changes_make_evidence_stale(self):
        def run(argv, timeout):
            (self.root / 'app.py').write_text('changed during tests\n')
            return subprocess.CompletedProcess(argv, 0, b'PASS', b'')
        with patch.object(runtime, 'run_logged', side_effect=run):
            result = self.call('test')
        self.assertTrue(result['stale'])
        self.assertFalse(result['passed'])

    def test_controller_submission_is_not_a_workspace_capability(self):
        for action in ('submit', 'authorize', 'resume'):
            with self.subTest(action=action), self.assertRaisesRegex(runtime.SandboxError, 'Unknown workspace action'):
                self.call(action)
        self.assertFalse((sandbox.home(self.root) / 'runs').exists())

    def test_non_git_startup_and_inspection_are_nonfatal_and_do_not_write(self):
        with tempfile.TemporaryDirectory() as directory:
            for action in ('session_start', 'settings', 'status', 'end_sandbox'):
                output = io.StringIO()
                with self.subTest(action=action), patch.object(workspace.sys, 'stdin', io.StringIO(json.dumps({'action': action}))), contextlib.redirect_stdout(output):
                    self.assertEqual(workspace.main(['--repo', directory, 'call']), 0)
                result = json.loads(output.getvalue())
                self.assertEqual(result['reason'], 'not_git_repository')
                self.assertEqual(result['status'], 'unavailable')
            self.assertEqual(list(workspace.Path(directory).iterdir()), [])

    def test_non_git_tests_still_report_failure_instead_of_claiming_verification(self):
        with tempfile.TemporaryDirectory() as directory:
            output = io.StringIO()
            with patch.object(workspace.sys, 'stdin', io.StringIO('{"action":"test"}')), contextlib.redirect_stdout(output):
                self.assertEqual(workspace.main(['--repo', directory, 'call']), 1)
            self.assertIn('Cannot use workspace', json.loads(output.getvalue())['error'])


if __name__ == '__main__':
    unittest.main()
