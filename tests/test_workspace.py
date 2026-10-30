"""Native workspace tools do not authorize or orchestrate agents."""
import json
import subprocess
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


if __name__ == '__main__':
    unittest.main()
