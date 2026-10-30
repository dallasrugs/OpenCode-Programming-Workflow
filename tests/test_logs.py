"""Live forwarding is verified before the producer completes, using real processes."""
from contextlib import redirect_stderr
import io
import json
from pathlib import Path
import sys
import tempfile
import threading
import unittest

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / '.opencode/runtime'))
import runtime as b
import logs


class LoggingTests(unittest.TestCase):
    def test_process_output_is_forwarded_before_exit(self):
        ready = threading.Event()
        finished = threading.Event()
        captured = []
        results = []
        errors = []
        class Output:
            def write(self, text):
                captured.append(text)
                if text == 'LIVE_MARKER\n':
                    ready.set()
            def flush(self):
                pass
        with tempfile.TemporaryDirectory() as tmp:
            release = Path(tmp) / 'release'
            program = 'import pathlib,time; print("LIVE_MARKER",flush=True); p=pathlib.Path(' + repr(str(release)) + ')\nwhile not p.exists(): time.sleep(.01)\nprint("finished",flush=True)'
            def run():
                try:
                    results.append(b.run_logged([sys.executable, '-u', '-c', program], timeout=5))
                except BaseException as error:
                    errors.append(error)
                finally:
                    finished.set()
            with redirect_stderr(Output()):
                thread = threading.Thread(target=run)
                thread.start()
                try:
                    self.assertTrue(ready.wait(3), 'Short live output was buffered until process exit')
                    self.assertFalse(finished.is_set())
                finally:
                    release.touch()
                    thread.join(timeout=6)
        self.assertEqual(errors, [])
        self.assertEqual(results[0].stdout, b'LIVE_MARKER\nfinished\n')
        self.assertIn('Command exited: 0', ''.join(captured))

    def test_operation_log_follower_is_live_and_preserves_json_protocol(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            b.execute(['git', 'init', '-q', str(root)])
            operation_id = 'a' * 32
            output = io.BytesIO()
            errors = []
            def follow():
                try:
                    logs.follow(root, operation_id, output=output, poll_seconds=.01)
                except BaseException as error:
                    errors.append(error)
            with redirect_stderr(io.StringIO()), logs.operation(root, {'action': 'configure', 'operation_id': operation_id}):
                thread = threading.Thread(target=follow)
                thread.start()
                print('image layer output', file=sys.stderr, flush=True)
            thread.join(timeout=5)
            self.assertFalse(thread.is_alive())
            self.assertEqual(errors, [])
            self.assertIn(b'image layer output', output.getvalue())
            directory = logs.operation_directory(root, operation_id)
            self.assertTrue(json.loads((directory / 'state.json').read_text())['finished'])
            self.assertIn('image layer output', (directory / 'output.log').read_text())

    def test_log_identifiers_cannot_select_arbitrary_paths(self):
        for identifier in ('../escape', '/etc/passwd', 'a' * 31, 'x' * 32):
            with self.subTest(identifier=identifier), self.assertRaises(b.SandboxError):
                logs.operation_directory(Path.cwd(), identifier)


if __name__ == '__main__':
    unittest.main()
