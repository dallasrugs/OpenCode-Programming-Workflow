import base64
import importlib.util
import io
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import unittest
from unittest.mock import patch

GOVERNANCE = Path(__file__).resolve().parents[1] / '.opencode/governance'
sys.path.insert(0, str(GOVERNANCE))
import skillctl as s
import bdfl


class ProvenanceTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.bundle = Path(self.tmp.name) / '.opencode'
        shutil.copytree(s.BUNDLE, self.bundle, ignore=shutil.ignore_patterns('__pycache__'))
        self.manifest = s.load_manifest(self.bundle)

    def tearDown(self):
        self.tmp.cleanup()

    def fetcher(self, mutate=None):
        def fetch(repository, ref):
            source = {}
            for u in s.units(self.manifest):
                if u['upstreamRepository'] == repository:
                    for f in u['files']:
                        source[f['upstreamPath']] = (self.bundle / u['snapshot'] / f['path']).read_bytes()
            if mutate:
                mutate(source)
            yield 'a' * 40, dict.fromkeys(source, ('100644', 'blob', 'unused')), source.__getitem__
        return fetch

    def test_complete_catalog_and_all_seventeen_audit_inputs(self):
        result = s.validate(self.bundle)
        self.assertEqual(result['verifiedImports'], 18)
        self.assertEqual(result['unverifiedPreserved'], 6)
        self.assertEqual(result['nativeSkills'], 24)
        self.assertEqual(len(self.manifest['audit']), 17)
        for u in self.manifest['skills']:
            self.assertEqual(s.inventory(self.bundle / u['destination']),
                             s.patched(s.inventory(self.bundle / u['snapshot']), s.patches_for(u, self.bundle)))

    def test_methodologies_are_not_generic_rewrites(self):
        tdd = (self.bundle / 'skills/tdd/SKILL.md').read_text()
        self.assertIn('**One slice at a time.** One seam, one test, one minimal implementation per cycle.', tdd)
        self.assertIn('**Refactoring is not part of the loop.**', tdd)
        debugging = (self.bundle / 'skills/systematic-debugging/SKILL.md').read_text()
        self.assertIn('NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST', debugging)
        self.assertIn('### Phase 1: Root Cause Investigation', debugging)
        self.assertNotIn('## Governed execution', debugging)
        self.assertTrue((self.bundle / 'skills/systematic-debugging/root-cause-tracing.md').is_file())

    def test_unverified_inputs_remain_byte_identical(self):
        for a in self.manifest['audit']:
            if a['status'] == 'SOURCE_UNVERIFIED':
                self.assertEqual((self.bundle / a['preservedInput']).read_bytes(),
                                 (self.bundle / a['originalLocalPath']).read_bytes())
                self.assertEqual(a['license'], 'UNVERIFIED')

    def test_source_tampering_and_local_changes_fail_closed(self):
        for relative in ('skills/tdd/SKILL.md', 'skill-sources/upstream/tdd/SKILL.md',
                         'skill-sources/patches/seo-content.json'):
            p = self.bundle / relative
            original = p.read_bytes()
            p.write_bytes(original + b'\nlocal edit\n')
            with self.subTest(path=relative), self.assertRaises(s.SkillError):
                s.validate(self.bundle)
            p.write_bytes(original)

    def test_missing_resource_license_or_support_file_fails(self):
        for relative in ('skills/tdd/LICENSE', 'skills/tdd/tests.md',
                         'skill-resources/claude-seo/skills/seo/references/eeat-framework.md'):
            p = self.bundle / relative
            original = p.read_bytes()
            p.unlink()
            with self.subTest(path=relative), self.assertRaises(s.SkillError):
                s.validate(self.bundle)
            p.write_bytes(original)

    def test_unknown_local_support_file_is_not_silently_overwritten(self):
        p = self.bundle / 'skills/tdd/local-notes.md'
        p.write_text('unresolved local notes')
        with self.assertRaises(s.SkillError):
            s.plan_update(self.bundle, 'tdd', 'main', self.fetcher())
        self.assertEqual(p.read_text(), 'unresolved local notes')

    def test_native_ids_frontmatter_and_manual_discovery_flags(self):
        for u in self.manifest['skills']:
            f = s.frontmatter((self.bundle / u['destination'] / 'SKILL.md').read_bytes())
            self.assertTrue(f['description'])
        self.assertEqual(s.frontmatter((self.bundle / 'skills/to-spec/SKILL.md').read_bytes())['disable-model-invocation'], 'true')
        for bad in (b'no frontmatter', b'---\nname: x\n---\nbody', b'---\nname: x\nname: y\ndescription: z\n---'):
            with self.assertRaises(s.SkillError):
                s.frontmatter(bad)

    def test_roles_only_have_appropriate_native_skill_permissions(self):
        for role in s.ROLES:
            front, body = s.read_agent(self.bundle, role)
            for skill in s.native_ids(self.manifest):
                self.assertEqual(s.permission(front['permissions'], 'skill', skill),
                                 'allow' if skill in self.manifest['agents'][role] else 'deny')
            for action in ('edit', 'shell', 'subagent', 'execute', 'bdfl_tests_run_tests', 'random_mcp_tool'):
                self.assertEqual(s.permission(front['permissions'], action, '*'), 'deny')
            # Definitions explain integration, not embedded author methodologies.
            self.assertNotIn('NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST', body)
        self.assertNotIn('grilling', self.manifest['agents']['reviewer'])
        self.assertNotIn('tdd', self.manifest['agents']['team-lead'])
        self.assertIn('code-review', self.manifest['agents']['reviewer'])

    def test_update_is_diff_first_and_preserves_compatibility_patch(self):
        before = (self.bundle / 'skills/seo-content/SKILL.md').read_bytes()
        patch_path = self.bundle / 'skill-sources/patches/seo-content.json'
        patch_before = patch_path.read_bytes()
        def mutate(source):
            source['skills/seo-content/SKILL.md'] += b'\nUpstream release note.\n'
        report = s.plan_update(self.bundle, 'seo-content', 'main', self.fetcher(mutate))
        self.assertIn('+Upstream release note.', report['diff'])
        self.assertEqual((self.bundle / 'skills/seo-content/SKILL.md').read_bytes(), before)
        data = s.encoded(report)
        with self.assertRaises(s.SkillError):
            s.apply_update(self.bundle, data, 'unreviewed')
        result = s.apply_update(self.bundle, data, s.sha(data))
        self.assertEqual(result['updatedUnits'], 3)  # Both skills plus shared resources stay pinned together.
        self.assertEqual(result['executedScripts'], [])
        self.assertIn(b'Upstream release note.', (self.bundle / 'skills/seo-content/SKILL.md').read_bytes())
        self.assertEqual(patch_path.read_bytes(), patch_before)
        self.assertIn(b'.opencode/skill-resources/claude-seo', (self.bundle / 'skills/seo-content/SKILL.md').read_bytes())
        self.assertNotIn(b'${CLAUDE_PLUGIN_ROOT}', (self.bundle / 'skills/seo-content/SKILL.md').read_bytes())
        s.validate(self.bundle)

    def test_changed_license_blocks_update_and_apply_rechecks_it(self):
        def mutate(source):
            source['LICENSE'] += b'\nChanged redistribution terms.\n'
        report = s.plan_update(self.bundle, 'tdd', 'main', self.fetcher(mutate))
        self.assertTrue(any('LICENSE_CHANGED' in b for b in report['blockedReasons']))
        data = s.encoded(report)
        with self.assertRaises(s.SkillError):
            s.apply_update(self.bundle, data, s.sha(data))
        # Even a modified report cannot bypass the independent apply-time licensing check.
        report['blockedReasons'] = []
        data = s.encoded(report)
        with self.assertRaisesRegex(s.SkillError, 'License changed'):
            s.apply_update(self.bundle, data, s.sha(data))

    def test_patch_conflict_is_reported_without_modifying_source(self):
        before = (self.bundle / 'skills/seo-content/SKILL.md').read_bytes()
        def mutate(source):
            source['skills/seo-content/SKILL.md'] += b'\n${CLAUDE_PLUGIN_ROOT}/new-reference\n'
        report = s.plan_update(self.bundle, 'seo-content', 'main', self.fetcher(mutate))
        self.assertTrue(any('Compatibility patch conflict' in v for v in report['blockedReasons']))
        self.assertEqual((self.bundle / 'skills/seo-content/SKILL.md').read_bytes(), before)

    def test_local_modification_after_diff_blocks_apply(self):
        report = s.plan_update(self.bundle, 'tdd', 'main', self.fetcher())
        p = self.bundle / 'skills/tdd/tests.md'
        p.write_bytes(p.read_bytes() + b'local change')
        data = s.encoded(report)
        with self.assertRaises(s.SkillError):
            s.apply_update(self.bundle, data, s.sha(data))
        self.assertTrue(p.read_bytes().endswith(b'local change'))

    def test_changed_scripts_are_reported_and_never_executed(self):
        def mutate(source):
            source['scripts/content_humanize.py'] += b'\n# update inspection fixture\n'
        report = s.plan_update(self.bundle, 'seo-content', 'main', self.fetcher(mutate))
        self.assertTrue(any('scripts/content_humanize.py' in u['changedScripts'] for u in report['units']))
        with patch.object(s.subprocess, 'run', side_effect=AssertionError('No execution allowed')):
            data = s.encoded(report)
            s.apply_update(self.bundle, data, s.sha(data))
        self.assertFalse((self.bundle / 'skill-resources/claude-seo/scripts/content_humanize.py').stat().st_mode & 0o111)

    def test_source_snapshots_not_in_discovery_and_installer_is_recursive(self):
        self.assertNotIn('skill-sources', (self.bundle / 'opencode.json').read_text())
        files = s.installation_files(self.bundle)
        for name in ('skills/tdd/tests.md', 'skills/tdd/LICENSE', 'skills/SOURCES.json',
                     'skill-sources/upstream/tdd/SKILL.md', 'skill-sources/patches/seo-content.json',
                     'skill-resources/claude-seo/scripts/content_humanize.py', 'governance/skillctl.py'):
            self.assertIn(name, files)
        self.assertFalse(any('__pycache__' in f for f in files))

    def test_role_snapshots_are_filtered_and_skill_bodies_not_preloaded(self):
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            bdfl.execute(['git', 'init', '-q', str(root)])
            bdfl.git(root, 'config', 'user.name', 'Fixture')
            bdfl.git(root, 'config', 'user.email', 'fixture@example.invalid')
            (root / 'app.py').write_text('value = 1\n')
            bdfl.git(root, 'add', '.')
            bdfl.git(root, 'commit', '-qm', 'fixture')
            adapter = object.__new__(bdfl.OpenCode)
            adapter.policy = json.loads((s.BUNDLE / 'governance/policy.example.json').read_text())
            real_execute = bdfl.execute
            for role in s.ROLES:
                def fake_execute(argv, cwd=None, **kwargs):
                    if argv[0] != 'opencode':
                        return real_execute(argv, cwd=cwd, **kwargs)
                    native = {p.parent.name for p in (cwd / '.opencode/skills').glob('*/SKILL.md')}
                    self.assertEqual(native, set(self.manifest['agents'][role]))
                    self.assertNotIn('NO FIXES WITHOUT ROOT CAUSE INVESTIGATION FIRST', argv[-1])
                    self.assertNotIn('One seam, one test, one minimal implementation', argv[-1])
                    config = json.loads((cwd / '.opencode/opencode.json').read_text())
                    self.assertNotIn('mcp', config)  # No checkpoint for read-only or unauthorized sessions.
                    return json.dumps({'type': 'text', 'part': {'text': '{"checked":true}'}}).encode()
                with self.subTest(role=role), patch.object(bdfl, 'execute', side_effect=fake_execute):
                    adapter.call(role, 'metadata-check', {}, root)


if __name__ == '__main__':
    unittest.main()
