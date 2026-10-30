"""Chat intake persists real inputs and uses the existing authorization gates."""
import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / '.opencode/governance'))
import chat
import bdfl as b


class ChatTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)
        b.execute(['git', 'init', '-q', str(self.root)])
        b.git(self.root, 'config', 'user.email', 'test@example.invalid')
        b.git(self.root, 'config', 'user.name', 'Test')
        (self.root / 'app.py').write_text('original\n')
        b.git(self.root, 'add', '.')
        b.git(self.root, 'commit', '-qm', 'fixture')
        self.policy = json.loads((b.BUNDLE / 'governance/policy.example.json').read_text())

    def tearDown(self):
        self.tmp.cleanup()

    def submit(self):
        with patch.object(chat, 'launch') as launch:
            result = chat.dispatch(self.root, {'action': 'submit', 'request': 'Fix app\nPreserve API',
                                               'policy': self.policy, 'session_id': 'chat-session'})
        self.assertEqual(launch.call_count, 1)
        return result

    def test_submit_saves_inputs_authorizes_and_preserves_original_checkout(self):
        result = self.submit()
        self.assertEqual(Path(result['request_file']).read_text(), 'Fix app\nPreserve API')
        self.assertEqual(json.loads(Path(result['policy_file']).read_text()), self.policy)
        state = json.loads(Path(result['state']).read_text())
        self.assertTrue(state['task_authorized'])
        self.assertEqual(state['phase'], 'PLAN')
        self.assertEqual(b.git(self.root, 'status', '--porcelain'), b'')
        self.assertEqual((self.root / 'app.py').read_text(), 'original\n')
        self.assertNotEqual(Path(state['worktree']), self.root)

    def test_dirty_checkout_stops_before_launch(self):
        (self.root / 'app.py').write_text('user draft\n')
        with patch.object(chat, 'launch') as launch, self.assertRaisesRegex(b.GateError, 'clean checkout'):
            chat.dispatch(self.root, {'action': 'submit', 'request': 'Fix app', 'policy': self.policy})
        launch.assert_not_called()
        self.assertEqual((self.root / 'app.py').read_text(), 'user draft\n')

    def test_invalid_policy_never_launches(self):
        with patch.object(chat, 'launch') as launch, self.assertRaises(b.GateError):
            chat.dispatch(self.root, {'action': 'submit', 'request': 'Fix app', 'policy': {}})
        launch.assert_not_called()

    def test_escalation_requires_matching_hash(self):
        result = self.submit()
        store = b.Store(self.root, result['id'])
        state = store.read()
        state.update(phase='AWAITING_BDFL', spec_hash='exact-hash')
        store.save(state, 'test_escalation')
        with patch.object(chat, 'launch') as launch:
            with self.assertRaisesRegex(b.GateError, 'fingerprint'):
                chat.dispatch(self.root, {'action': 'authorize', 'run_id': result['id'],
                                         'spec': 'wrong-hash', 'reason': 'Approved'})
            launch.assert_not_called()
            chat.dispatch(self.root, {'action': 'authorize', 'run_id': result['id'],
                                     'spec': 'exact-hash', 'reason': 'Approve this migration'})
            self.assertEqual(launch.call_args.args[1:], ('authorize', 'exact-hash', 'Approve this migration'))

    def test_launch_uses_fixed_argv_and_background_process(self):
        result = self.submit()
        store = b.Store(self.root, result['id'])
        with patch.object(chat.subprocess, 'Popen') as popen:
            popen.return_value.pid = 12345
            chat.launch(store)
            args, options = popen.call_args
            self.assertEqual(args[0][0], sys.executable)
            self.assertEqual(args[0][-4:], ['worker', result['id'], '--command', 'resume'])
            self.assertTrue(options['start_new_session'])
            self.assertEqual(options['stdin'], subprocess.DEVNULL)
        with patch.object(chat.os, 'kill'), self.assertRaisesRegex(b.GateError, 'already running'):
            chat.launch(store)

    def test_worker_failure_is_visible_in_status(self):
        result = self.submit()
        with patch.object(b, 'main', return_value=1):
            self.assertEqual(chat.main(['--repo', str(self.root), 'worker', result['id']]), 1)
        result = chat.dispatch(self.root, {'action': 'status', 'run_id': result['id']})
        self.assertFalse(result['running'])
        self.assertEqual(result['worker_result'], {'exit_code': 1})


if __name__ == '__main__':
    unittest.main()
