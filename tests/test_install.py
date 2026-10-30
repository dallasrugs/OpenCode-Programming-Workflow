import json
from pathlib import Path
import subprocess
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]


class InstallerTests(unittest.TestCase):
    def install(self, target, *args):
        return subprocess.run(['bash', str(ROOT / 'install.sh'), '--project', str(target), *args],
                              check=True, capture_output=True, text=True)

    def test_dry_run_and_complete_install_and_no_overwrite(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            self.install(target, '--dry-run')
            self.assertFalse((target / '.opencode').exists())
            self.install(target)
            bundle = target / '.opencode'
            self.assertEqual(set(x.stem for x in (bundle / 'agents').glob('*.md')),
                             {'team-lead', 'maintainer', 'coder', 'reviewer'})
            self.assertTrue((bundle / 'governance/bdfl.py').is_file())
            self.assertTrue((bundle / 'governance/policy.example.json').is_file())
            self.assertEqual(len(list((bundle / 'skills').glob('*/SKILL.md'))), 24)
            self.assertTrue((bundle / 'skills/tdd/tests.md').is_file())
            self.assertTrue((bundle / 'skills/tdd/LICENSE').is_file())
            self.assertTrue((bundle / 'skill-sources/upstream/tdd/SKILL.md').is_file())
            self.assertTrue((bundle / 'skill-sources/patches/seo-content.json').is_file())
            self.assertTrue((bundle / 'skill-resources/claude-seo/scripts/url_safety.py').is_file())
            config = bundle / 'opencode.json'
            self.assertEqual(json.loads(config.read_text())['default_agent'], 'team-lead')
            config.write_text('preserve existing user config')
            self.install(target)
            self.assertEqual(config.read_text(), 'preserve existing user config')

    def test_jsonc_preserved_without_competing_json(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / '.opencode').mkdir()
            jsonc = target / '.opencode/opencode.jsonc'
            jsonc.write_text('// existing config\n{}')
            self.install(target)
            self.assertFalse((target / '.opencode/opencode.json').exists())
            self.assertEqual(jsonc.read_text(), '// existing config\n{}')

    def test_symlink_existing_file_preserved(self):
        with tempfile.TemporaryDirectory() as tmp:
            target = Path(tmp)
            (target / '.opencode').mkdir()
            config = target / '.opencode/opencode.json'
            config.symlink_to(target / 'absent.json')
            self.install(target)
            self.assertTrue(config.is_symlink())
            self.assertFalse((target / 'absent.json').exists())


if __name__ == '__main__':
    unittest.main()
