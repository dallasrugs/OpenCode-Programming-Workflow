#!/usr/bin/env python3
"""Verify native OpenCode registration and optional real role skill-tool calls.

Live mode makes provider requests against a disposable fixture, never application
source. It checks native tool events rather than trusting model completion claims.
"""
import argparse
import json
import os
from pathlib import Path
import sys
import tempfile

import bdfl
import skillctl

PROBES = {'team-lead': 'grilling', 'maintainer': 'codebase-design',
          'coder': 'tdd', 'reviewer': 'verification-before-completion'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--live', action='store_true')
    parser.add_argument('--reviewer-model', help='Explicit test-only provider override, recorded in the report')
    parser.add_argument('--role', choices=tuple(PROBES), action='append')
    parser.add_argument('--report', type=Path)
    args = parser.parse_args()
    report = {'offlineValidation': skillctl.validate(), 'roles': [], 'executedUpstreamScripts': []}
    try:
        report['openCodeVersion'] = bdfl.execute(['opencode', '--version']).decode().strip()
        env = os.environ.copy()
        env['PWD'] = str(skillctl.BUNDLE.parent.resolve())
        agents = json.loads(bdfl.execute(['opencode', '--standalone', 'debug', 'agents'], cwd=skillctl.BUNDLE.parent, env=env))
        visible = {a['id'] for a in agents if not a.get('hidden')}
        bdfl.require(visible == set(PROBES), 'Unexpected visible agents: ' + str(visible))
        report['nativeAgents'] = sorted(visible)
        for agent in agents:
            if agent['id'] not in PROBES:
                continue
            for skill in skillctl.native_ids(skillctl.load_manifest()):
                expected = 'allow' if skill in skillctl.allowed_skills(agent['id']) else 'deny'
                bdfl.require(skillctl.permission(agent['permissions'], 'skill', skill) == expected,
                             'Installed native role skill permission mismatch')
        report['nativeAgentPermissions'] = 'PASS'
        # A cold v2.2.3 experimental catalog can be empty; never treat that as proof of registration.
        catalog = json.loads(bdfl.execute(['opencode', '--standalone', 'api', 'skill.list'], cwd=skillctl.BUNDLE.parent, env=env))
        report['coldApiSkillCatalogCount'] = len(catalog.get('data', []))
        if args.live:
            policy = json.loads((skillctl.BUNDLE / 'governance/policy.example.json').read_text())
            policy['agent_timeout_seconds'] = 180
            if args.reviewer_model:
                policy['models']['reviewer'] = args.reviewer_model
            backend = bdfl.OpenCode(policy)
            with tempfile.TemporaryDirectory(prefix='skill-native-fixture-') as tmp:
                root = Path(tmp)
                bdfl.execute(['git', 'init', '-q', str(root)])
                bdfl.git(root, 'config', 'user.name', 'Skill validation fixture')
                bdfl.git(root, 'config', 'user.email', 'fixture@example.invalid')
                (root / 'README.md').write_text('Disposable native skill discovery fixture.\n')
                bdfl.git(root, 'add', '.')
                bdfl.git(root, 'commit', '-qm', 'fixture')
                for role in args.role or PROBES:
                    skill = PROBES[role]
                    record = {'role': role, 'skill': skill, 'model': policy['models'][role]}
                    print(f'Checking native {role} skill {skill}', flush=True)
                    try:
                        result = backend.call(role, 'native-skill-discovery-check', {
                            'request': 'This is a metadata/loading check only. Call the native skill tool with ID ' + skill +
                                       ' once, to prove it resolves. Do not apply the workflow, ask interview questions, edit files, or run shell/tests. Then return the requested JSON object.',
                            'response_contract': {'loaded': skill}}, root)
                        calls = [e['part'] for e in backend.last_events if e.get('type') == 'tool_use'
                                 and e.get('part', {}).get('tool') == 'skill']
                        loaded = [c for c in calls if c.get('state', {}).get('status') == 'completed'
                                  and c.get('state', {}).get('input', {}).get('id') == skill]
                        bdfl.require(loaded, 'No successful native skill-tool event; model text is insufficient')
                        bdfl.require(result.get('loaded') == skill, 'Skill probe response did not match')
                        record['result'] = 'PASS'
                        record['nativeToolEvents'] = len(loaded)
                        record['sourceSha256'] = skillctl.sha((skillctl.BUNDLE / 'skills' / skill / 'SKILL.md').read_bytes())
                    except (bdfl.GateError, OSError, ValueError) as e:
                        record.update(result='FAIL', reason=str(e))
                    report['roles'].append(record)
    except (bdfl.GateError, skillctl.SkillError, OSError, ValueError) as e:
        report['error'] = str(e)
    data = json.dumps(report, indent=2) + '\n'
    if args.report:
        with args.report.open('x') as f:
            f.write(data)
    print(data)
    return 1 if report.get('error') or any(r['result'] != 'PASS' for r in report['roles']) else 0


if __name__ == '__main__':
    sys.exit(main())
