"""Supervisor checks without model requests or an OpenCode server."""
import contextlib
import importlib.util
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

spec = importlib.util.spec_from_file_location('agent_eval_runner', Path(__file__).parent / 'agent_evals/run_eval.py')
runner = importlib.util.module_from_spec(spec)
spec.loader.exec_module(runner)


class AgentEvalRunnerTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name) / 'fixture'
        self.root.mkdir()
        (self.root / 'source.py').write_text('value = 1\n')
        self.prompt = Path(self.temp.name) / 'prompt.txt'
        self.prompt.write_text('Read only; stop after diagnosis.')
        self.output = Path(self.temp.name) / 'result.json'
        self.argv = ['run_eval', '--directory', str(self.root), '--agent', 'reviewer',
                     '--prompt', str(self.prompt), '--output', str(self.output)]

    def info(self, idle, outcome=None):
        return {'data': {'id': 'prior', 'location': {'directory': str(self.root)},
                         'agent': 'reviewer', 'time': {'idle': idle}, 'outcome': outcome}}

    def invoke(self, fake, extra=(), clock=None):
        with patch('sys.argv', self.argv + list(extra)), patch.object(runner, 'api', side_effect=fake), \
             patch.object(runner.time, 'sleep'), contextlib.redirect_stdout(io.StringIO()):
            if clock is not None:
                with patch.object(runner.time, 'monotonic', side_effect=clock):
                    return runner.main()
            return runner.main()

    def test_reused_session_waits_for_new_idle_instead_of_old_outcome(self):
        replies = iter([self.info(5, 'interrupted'), self.info(5, 'interrupted'),
                        self.info(6, 'succeeded')])
        calls = []

        def fake(method, path, payload=None):
            calls.append((method, path))
            if method == 'GET' and path == '/api/session/prior':
                return next(replies)
            if '/message?' in path:
                return {'data': []}
            return {'data': {}}

        self.assertEqual(self.invoke(fake, ['--session', 'prior']), 0)
        self.assertEqual(calls.count(('GET', '/api/session/prior')), 3)
        result = json.loads(self.output.read_text())
        self.assertEqual(result['outcome'], 'succeeded')
        self.assertEqual(result['changed_files'], [])

    def test_deadline_interrupts_server_side_generation(self):
        calls = []

        def fake(method, path, payload=None):
            calls.append((method, path))
            if path == '/api/session' or (method == 'GET' and path == '/api/session/prior'):
                return self.info(0)
            if '/message?' in path:
                return {'data': []}
            return {'data': {}}

        self.assertEqual(self.invoke(fake, ['--timeout', '1'], [0, 3, 4]), 1)
        self.assertEqual(calls.count(('POST', '/api/session/prior/interrupt')), 1)
        self.assertEqual(json.loads(self.output.read_text())['stopped'], 'deadline exceeded')

    def test_wrong_location_does_not_send_prompt(self):
        calls = []

        def fake(method, path, payload=None):
            calls.append((method, path))
            result = self.info(0)
            result['data']['location']['directory'] = str(self.root.parent)
            return result

        with self.assertRaisesRegex(RuntimeError, 'location mismatch'):
            self.invoke(fake)
        self.assertFalse(any(path.endswith('/prompt') for _, path in calls))


if __name__ == '__main__':
    unittest.main()
