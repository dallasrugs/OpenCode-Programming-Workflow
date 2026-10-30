#!/usr/bin/env python3
"""Narrow chat-to-controller bridge. JSON on stdin; no shell commands from chat."""
from __future__ import annotations

import argparse
import json
import os
from pathlib import Path
import subprocess
import sys
import uuid

import bdfl as b


def running(store):
    done = store.directory / 'worker-result.json'
    job = store.directory / 'worker.json'
    if not job.exists() or done.exists():
        return False
    try:
        os.kill(json.loads(job.read_text())['pid'], 0)
        return True
    except ProcessLookupError:
        return False


def launch(store, command='resume', spec=None, reason=None):
    # Serialize chat launches independently of the worker's controller lock.
    lock = store.home / 'chat-launch.lock'
    try:
        fd = os.open(lock, os.O_WRONLY | os.O_CREAT | os.O_EXCL, 0o600)
    except FileExistsError as error:
        raise b.GateError('Another chat launch is in progress; check status before retrying') from error
    try:
        os.close(fd)
        _launch(store, command, spec, reason)
    finally:
        lock.unlink()


def _launch(store, command, spec, reason):
    b.require(not running(store), 'Controller is already running; use status')
    b.require(not (store.home / 'controller.lock').exists(), 'Controller is locked; inspect status before resuming')
    result = store.directory / 'worker-result.json'
    result.unlink(missing_ok=True)
    argv = [sys.executable, str(Path(__file__).resolve()), '--repo', str(store.repo),
            'worker', store.directory.name, '--command', command]
    if spec is not None:
        argv += ['--spec', spec]
    if reason is not None:
        argv += ['--reason', reason]
    with (store.directory / 'controller.log').open('ab') as log:
        child = subprocess.Popen(argv, stdin=subprocess.DEVNULL, stdout=log, stderr=log,
                                 start_new_session=True, cwd=store.repo)
    b.atomic_json(store.directory / 'worker.json', {'pid': child.pid})


def status(store):
    state = store.read()
    result = store.directory / 'worker-result.json'
    log = store.directory / 'controller.log'
    return {'id': state['id'], 'phase': state['phase'], 'running': running(store),
            'spec_hash': state.get('spec_hash'), 'spec': state.get('spec'),
            'plan_decision': state.get('plan_decision'), 'feedback': state.get('feedback'),
            'report': state.get('report'), 'worktree': state['worktree'],
            'state': str(store.path), 'request_file': str(store.directory / 'request.txt'),
            'policy_file': str(store.directory / 'policy.json'), 'log': str(log),
            'worker_result': json.loads(result.read_text()) if result.exists() else None,
            'log_tail': log.read_bytes()[-8000:].decode(errors='replace') if log.exists() else '',
            'candidate_stale': bool(state.get('candidate') and
                                    b.fingerprint(Path(state['worktree'])) != state['candidate'])}


def dispatch(root, payload):
    action = payload.get('action')
    if action == 'defaults':
        policy = json.loads((b.BUNDLE / 'governance/policy.example.json').read_text())
        policy['models'] = {role: b.read_agent(role)[0]['model'] for role in b.ROLES}
        try:
            images = b.execute(['docker', 'image', 'ls', '--format', '{{.Repository}}:{{.Tag}}'], timeout=15).decode().splitlines()
        except b.GateError as error:
            images = []
            docker_error = str(error)
        else:
            docker_error = None
        return {'policy_template': policy, 'local_test_images': images, 'docker_error': docker_error,
                'note': 'Replace example tests/image with repository-specific validation. Dependencies must be preloaded.'}
    if action == 'submit':
        request, policy = payload.get('request'), payload.get('policy')
        b.require(isinstance(request, str) and request.strip(), 'A non-empty BDFL request is required')
        b.require(isinstance(policy, dict), 'A generated policy object is required')
        b.validate_policy(policy)
        store = b.Store(root, uuid.uuid4().hex[:12])
        with store.lock():
            b.atomic_json(store.directory / 'chat.json', {'session_id': payload.get('session_id')})
            b.start(store, request, policy, authorized=True)
        launch(store)
        return status(store)
    b.require(action in ('status', 'resume', 'authorize', 'reject'), 'Unknown chat controller action')
    store = b.Store(root, payload.get('run_id', ''))
    state = store.read()
    if action == 'reject':
        with store.lock():
            b.require(state['phase'] in ('AWAITING_BDFL', 'ESCALATED', 'EXHAUSTED'), 'No pending decision to reject')
            b.require(isinstance(payload.get('reason'), str) and payload['reason'].strip(), 'Rejection reason required')
            state.update(phase='REJECTED', rejection_reason=payload['reason'])
            store.save(state, 'bdfl_rejected')
    elif action == 'authorize':
        # Validate the exact decision before starting a background worker.
        b.require(isinstance(payload.get('spec'), str), 'Exact specification hash required')
        b.require(isinstance(payload.get('reason'), str) and payload['reason'].strip(), 'Approval reason required')
        b.require(state['phase'] == 'AWAITING_BDFL' and state['spec_hash'] == payload['spec'],
                  'Approval must match the pending specification fingerprint')
        launch(store, 'authorize', payload['spec'], payload['reason'])
    elif action == 'resume':
        b.require(state['phase'] not in ('REJECTED', 'EXHAUSTED', 'ESCALATED'), 'Start a new task with revised scope or policy')
        launch(store)
    return status(store)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--repo', required=True, type=Path)
    parser.add_argument('mode', choices=('call', 'worker'))
    parser.add_argument('run_id', nargs='?')
    parser.add_argument('--command', choices=('resume', 'authorize'), default='resume')
    parser.add_argument('--spec')
    parser.add_argument('--reason')
    args = parser.parse_args(argv)
    try:
        root = Path(b.git(args.repo.resolve(), 'rev-parse', '--show-toplevel').decode().strip())
        if args.mode == 'worker':
            store = b.Store(root, args.run_id)
            command = ['--repo', str(root), args.command, args.run_id]
            if args.command == 'authorize':
                command += ['--spec', args.spec, '--reason', args.reason]
            code = b.main(command)
            b.atomic_json(store.directory / 'worker-result.json', {'exit_code': code})
            return code
        print(json.dumps(dispatch(root, json.load(sys.stdin))))
        return 0
    except (b.GateError, b.skillctl.SkillError, OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({'error': str(error)}))
        return 1


if __name__ == '__main__':
    sys.exit(main())
