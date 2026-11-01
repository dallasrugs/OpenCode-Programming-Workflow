"""Shared filesystem, source snapshots and process output for sandbox utilities."""
from __future__ import annotations

import codecs
from contextlib import contextmanager
import fnmatch
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import shlex
import shutil
import subprocess
import sys
import tempfile
import threading
import time
import uuid

BUNDLE = Path(__file__).resolve().parent.parent
CONTROL = {'.git', '.opencode', '.codex', '.agents', 'opencode.json', 'opencode.jsonc'}


class SandboxError(RuntimeError):
    pass


def require(condition, message):
    if not condition:
        raise SandboxError(message)


def digest(value):
    return hashlib.sha256(json.dumps(value, sort_keys=True, separators=(',', ':')).encode()).hexdigest()


def atomic_json(path, value):
    path = Path(path)
    tmp = path.with_name(path.name + '.' + uuid.uuid4().hex + '.tmp')
    try:
        with tmp.open('x', encoding='utf-8') as f:
            json.dump(value, f, indent=2, sort_keys=True)
            f.write('\n')
            f.flush()
            os.fsync(f.fileno())
        os.replace(tmp, path)
    finally:
        tmp.unlink(missing_ok=True)


def capture(argv, cwd=None, timeout=60, env=None, stdin=None, limit=16 * 1024 * 1024):
    """Drain both pipes with bounded buffers; reject oversized required results explicitly."""
    process = subprocess.Popen(argv, cwd=cwd, env=env, stdin=stdin,
                               stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    buffers, truncated = [bytearray(), bytearray()], [False, False]
    def drain(index, stream):
        try:
            while chunk := stream.read(8192):
                room = max(0, limit - len(buffers[index]))
                buffers[index].extend(chunk[:room])
                if len(chunk) > room:
                    truncated[index] = True
        finally:
            stream.close()
    threads = [threading.Thread(target=drain, args=(i, stream), daemon=True)
               for i, stream in enumerate((process.stdout, process.stderr))]
    for thread in threads:
        thread.start()
    try:
        process.wait(timeout=timeout)
    except BaseException:
        process.kill()
        process.wait()
        raise
    finally:
        for thread in threads:
            thread.join(timeout=2)
    require(not any(thread.is_alive() for thread in threads), 'Command left inherited output streams open')
    require(not any(truncated), 'Command output exceeded capture budget; required result was not silently truncated')
    return subprocess.CompletedProcess(argv, process.returncode, bytes(buffers[0]), bytes(buffers[1]))


def execute(argv, cwd=None, timeout=60, env=None):
    try:
        result = capture(argv, cwd=cwd, env=env, timeout=timeout)
    except (OSError, subprocess.TimeoutExpired) as e:
        raise SandboxError(f'Command unavailable or timed out: {argv[0]}: {e}') from e
    require(result.returncode == 0, f'Command failed: {argv[0]}: {result.stderr.decode(errors="replace")[-4000:]}')
    return result.stdout


def git(root, *args, env=None):
    return execute(['git', '-C', str(root), *args], env=env)


def secret(name):
    return any(fnmatch.fnmatch(x.lower(), pat) for x in PurePosixPath(name).parts
               for pat in ('.env', '.env.*', '*.pem', '*.key', '.ssh', '.aws', 'credentials', 'auth.json'))


def source_files(root):
    """Tracked plus non-ignored untracked files; symlinks are rejected, never dereferenced."""
    require(not any(line.startswith(b'160000 ') for line in git(root, 'ls-files', '--stage').splitlines()),
            'Git submodules are unsupported in agent-visible source')
    names = git(root, 'ls-files', '-z', '--cached', '--others', '--exclude-standard').decode().split('\0')
    out = {}
    for name in sorted(set(names) - {''}):
        p = root / name
        require(not any((root.joinpath(*PurePosixPath(name).parts[:i])).is_symlink()
                        for i in range(1, len(PurePosixPath(name).parts) + 1)),
                f'Symlink in candidate source is unsupported: {name}')
        if p.is_file():
            out[name] = {'sha256': hashlib.sha256(p.read_bytes()).hexdigest(),
                         'executable': bool(p.stat().st_mode & 0o111)}
    return out


def fingerprint(root):
    return digest({'head': git(root, 'rev-parse', 'HEAD').decode().strip(), 'files': source_files(root)})


def validate_tests(tests):
    require(isinstance(tests, dict), 'Test configuration must be an object')
    require(isinstance(tests.get('image'), str) and tests['image'] and not tests['image'].startswith('-'), 'Test image required')
    require(type(tests.get('timeout_seconds')) is int and 0 < tests['timeout_seconds'] <= 3600, 'Invalid test timeout')
    require(isinstance(tests.get('commands'), list) and tests['commands'], 'At least one test command is required')
    for cmd in tests['commands']:
        require(isinstance(cmd, list) and cmd and all(isinstance(x, str) and x and '\x00' not in x for x in cmd),
                'Test commands must be non-empty argv arrays')
    return tests


@contextmanager
def mirror(root, agent=True):
    with tempfile.TemporaryDirectory(prefix='poseidon-source-') as tmp:
        dest = Path(tmp)
        for name in source_files(root):
            parts = PurePosixPath(name).parts
            if secret(name) or '.git' in parts or (agent and any(x in CONTROL for x in parts)):
                continue
            target = dest / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copyfile(root / name, target)
            target.chmod(0o755 if (root / name).stat().st_mode & 0o111 else 0o644)
        yield dest


def run_logged(argv, timeout, limit=100000, cancelled=None):
    """Tee live command output to the terminal/log, retaining bounded evidence tails."""
    print('$ ' + shlex.join(argv), file=sys.stderr, flush=True)
    process = subprocess.Popen(argv, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    buffers = [bytearray(), bytearray()]
    output_lock = threading.Lock()

    def drain(stream, buffer):
        decoder = codecs.getincrementaldecoder('utf-8')(errors='replace')
        try:
            while True:
                chunk = stream.read1(8192)
                if not chunk:
                    break
                buffer.extend(chunk)
                if len(buffer) > limit:
                    del buffer[:-limit]
                with output_lock:
                    try:
                        sys.stderr.write(decoder.decode(chunk))
                        sys.stderr.flush()
                    except (OSError, ValueError):
                        pass  # Keep draining and retaining evidence if a log viewer disconnects.
        finally:
            stream.close()

    threads = [threading.Thread(target=drain, args=(stream, buffer), daemon=True)
               for stream, buffer in zip((process.stdout, process.stderr), buffers)]
    for thread in threads:
        thread.start()
    try:
        if cancelled is None:
            process.wait(timeout=timeout)
        else:
            deadline = time.monotonic() + timeout
            while process.poll() is None:
                if cancelled():
                    raise SandboxError('Session ended; sandbox image preparation cancelled')
                remaining = deadline - time.monotonic()
                if remaining <= 0:
                    raise subprocess.TimeoutExpired(argv, timeout)
                try:
                    process.wait(timeout=min(0.2, remaining))
                except subprocess.TimeoutExpired:
                    pass
    except subprocess.TimeoutExpired:
        process.kill()
        process.wait()
        for thread in threads:
            thread.join(timeout=2)
        print(f'Command timed out after {timeout}s', file=sys.stderr, flush=True)
        raise subprocess.TimeoutExpired(argv, timeout, output=bytes(buffers[0]), stderr=bytes(buffers[1]))
    except BaseException:
        # Tool cancellation/interrupts must also terminate an in-flight image build.
        process.terminate()
        try:
            process.wait(timeout=2)
        except subprocess.TimeoutExpired:
            process.kill()
            process.wait()
        for thread in threads:
            thread.join(timeout=2)
        raise
    for thread in threads:
        thread.join(timeout=2)
    print(f'\nCommand exited: {process.returncode}', file=sys.stderr, flush=True)
    return subprocess.CompletedProcess(argv, process.returncode, bytes(buffers[0]), bytes(buffers[1]))
