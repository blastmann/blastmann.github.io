import contextlib
import importlib.util
import os
from pathlib import Path
import subprocess
import tempfile
import unittest

spec = importlib.util.spec_from_file_location('daily', Path(__file__).with_name('daily.py'))
daily = importlib.util.module_from_spec(spec)
spec.loader.exec_module(daily)
DATE = '2026-10-22'
ARTICLE = '---\nlayout: page\ntitle: Daily 2026-10-22\ndate: 2026-10-22\n---\n<h2>News</h2><p><a href="https://example.com">Source</a></p>'

class ImportTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.previous = Path.cwd()
        os.chdir(self.temp.name)
        subprocess.run(['git', 'init', '-q', '--bare', 'remote'], check=True)
        subprocess.run(['git', 'init', '-q', '-b', 'source', 'repo'], check=True)
        os.chdir('repo')
        daily.git('config', 'user.name', 'Test')
        daily.git('config', 'user.email', 'test@example.com')
        daily.ROOT.mkdir(parents=True)
        (daily.ROOT / 'index.html').write_text('---\nlayout: page\n---\n<ul>\n</ul>')
        daily.git('add', '.')
        daily.git('commit', '-qm', 'Base')
        daily.git('remote', 'add', 'origin', '../remote')
        daily.git('push', '-q', 'origin', 'source')
        self.base = daily.git('rev-parse', 'HEAD')

    def tearDown(self):
        os.chdir(self.previous)
        self.temp.cleanup()

    def candidate(self, content=ARTICLE, extra=None):
        path = daily.article_path(DATE)
        path.parent.mkdir(parents=True)
        path.write_text(content)
        if extra:
            Path(extra).write_text('untrusted code')
        daily.git('add', '.')
        daily.git('commit', '-qm', 'Candidate')
        sha = daily.git('rev-parse', 'HEAD')
        daily.git('push', '-q', 'origin', f'{sha}:refs/heads/candidate')
        daily.git('reset', '--hard', self.base)
        return sha

    def test_import_updates_source_archive_and_is_idempotent(self):
        sha = self.candidate()
        daily.import_candidate(sha, DATE)
        self.assertEqual(daily.article_path(DATE).read_text(), ARTICLE)
        self.assertIn('2026/10/2026-10-22.html', (daily.ROOT / 'index.html').read_text())
        published = daily.git('rev-parse', 'HEAD')
        daily.import_candidate(sha, DATE)
        self.assertEqual(published, daily.git('rev-parse', 'HEAD'))
        self.assertEqual(published, daily.git('ls-remote', 'origin', 'source').split()[0])

    def test_rejects_candidate_code_changes(self):
        sha = self.candidate(extra='payload.py')
        with self.assertRaisesRegex(ValueError, 'outside'):
            daily.import_candidate(sha, DATE)
        self.assertEqual(self.base, daily.git('rev-parse', 'HEAD'))
        self.assertFalse(daily.article_path(DATE).exists())

    def test_rejects_active_content(self):
        sha = self.candidate(ARTICLE + '<script>alert(1)</script>')
        with self.assertRaisesRegex(ValueError, 'Active content'):
            daily.import_candidate(sha, DATE)

    def test_rejects_overwrite(self):
        sha = self.candidate()
        path = daily.article_path(DATE)
        path.parent.mkdir(parents=True)
        path.write_text(ARTICLE + '<p>Editorial correction</p>')
        with self.assertRaisesRegex(ValueError, 'differs'):
            daily.import_candidate(sha, DATE)

    def test_rejects_path_traversal(self):
        with self.assertRaises(ValueError):
            daily.article_path('../../2026-10-22')

if __name__ == '__main__':
    unittest.main()
