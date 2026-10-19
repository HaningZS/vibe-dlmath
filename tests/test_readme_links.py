import json
import hashlib
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT=Path(__file__).resolve().parents[1]


class ReadmeLinksTests(unittest.TestCase):
    def paper_fixture(self,root):
        (root/'catalog').mkdir()
        paper=root/'proof_ref/paper'
        paper.mkdir(parents=True)
        (paper/'README.md').write_text('# Paper\n')
        row={'arxiv_id':'2105.04026v2','title':'Example','topic':'test','path':'proof_ref/paper','templates':['T01']}
        (root/'catalog/test.json').write_text(json.dumps({'schema_version':1,'papers':[row]}))
        cards=root/'proofs/test'
        cards.mkdir(parents=True)
        (cards/'T01-test.md').write_text('# Test\n\n## 复用契约\nContract\n\n## 实例化时必须完成\n- [ ] Check\n')
        template={'id':'T01','path':'proofs/test/T01-test.md','topic':'test','kind':'proof-template',
                  'related':[],'sources':['2105.04026']}
        (root/'proofs/registry.json').write_text(json.dumps({'schema_version':1,'topics':{'test':'Test'},'templates':[template]}))
        return paper

    def check(self,root):
        result=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/check_library.py'),'--root',str(root)],capture_output=True,text=True)
        return result.returncode,json.loads(result.stdout)

    def test_versioned_manifest_retains_base_id_template_sources(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            self.paper_fixture(root)
            code,data=self.check(root)
            self.assertEqual(code,0)
            self.assertEqual(data['template_routes'],1)

    def test_library_check_detects_metadata_identity_and_cached_byte_drift(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            paper=self.paper_fixture(root)
            content=b'%PDF-1.4\nfixture\n%%EOF\n'
            (paper/'paper.pdf').write_bytes(content)
            meta={'identifier':'2105.04026','resolved_id':'2105.04026v2',
                  'artifacts':{'pdf':{'sha256':hashlib.sha256(content).hexdigest()}}}
            (paper/'metadata.json').write_text(json.dumps(meta))
            self.assertEqual(self.check(root)[0],0)
            (paper/'paper.pdf').write_bytes(content.replace(b'fixture',b'changed'))
            code,data=self.check(root)
            self.assertEqual(code,1)
            self.assertIn('SHA-256','\n'.join(data['errors']))
            (paper/'paper.pdf').write_bytes(content)
            meta['resolved_id']='1705.07809v1'
            (paper/'metadata.json').write_text(json.dumps(meta))
            code,data=self.check(root)
            self.assertEqual(code,1)
            self.assertIn('Metadata identity','\n'.join(data['errors']))

    def test_html_navigation_and_banner_are_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'catalog').mkdir()
            (root/'README.md').write_text('<img src="hero.svg" alt="banner">\n<a href="guide.md#proof">Guide</a>\n')
            (root/'guide.md').write_text('# Wrong heading\n')
            def run():
                result=subprocess.run([sys.executable,'-B',str(ROOT/'scripts/check_library.py'),'--root',str(root)],capture_output=True,text=True)
                return result.returncode,json.loads(result.stdout)
            code,data=run()
            self.assertEqual(code,1)
            self.assertEqual(len(data['errors']),2)
            (root/'hero.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
            (root/'guide.md').write_text('# Proof\n')
            code,data=run()
            self.assertEqual(code,0)
            self.assertEqual(data['errors'],[])

    def test_root_local_archive_is_not_checked(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'catalog').mkdir()
            (root/'README.md').write_text('# Public library\n')
            archive=root/'.local-archive/old-release'
            archive.mkdir(parents=True)
            (archive/'notes.md').write_text('[[Obsolete wiki link]]\n[Old location](missing.md)\n')
            code,data=self.check(root)
            self.assertEqual(code,0)
            self.assertEqual(data['markdown_files'],1)
            self.assertEqual(data['errors'],[])

    def test_public_links_cannot_depend_on_local_archive(self):
        for target_exists in (False,True):
            with self.subTest(target_exists=target_exists),tempfile.TemporaryDirectory() as directory:
                root=Path(directory)
                (root/'catalog').mkdir()
                (root/'README.md').write_text(
                    '[Old notes](.local-archive/notes.md)\n'
                    '<a href=".local-archive/notes.md">Old notes</a>\n'
                    '<img src=".local-archive/hero.svg" alt="Old banner">\n'
                )
                if target_exists:
                    archive=root/'.local-archive'
                    archive.mkdir()
                    (archive/'notes.md').write_text('# Notes\n')
                    (archive/'hero.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg"/>')
                code,data=self.check(root)
                self.assertEqual(code,1)
                self.assertEqual(len(data['errors']),3)
                self.assertTrue(all('Local-only archive link:' in error for error in data['errors']))

    def test_missing_live_link_is_still_checked_with_local_archive(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'catalog').mkdir()
            (root/'.local-archive').mkdir()
            (root/'README.md').write_text('[Missing live note](missing.md)\n')
            code,data=self.check(root)
            self.assertEqual(code,1)
            self.assertEqual(data['errors'],['Missing: README.md -> missing.md'])

    def test_archive_links_cannot_be_hidden_by_symlink_aliases(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'catalog').mkdir()
            archive=root/'.local-archive'
            archive.mkdir()
            (root/'guide.md').write_text('# Public guide\n')
            (archive/'notes.md').write_text('# Private notes\n')
            (archive/'nested').mkdir()
            (archive/'public-alias.md').symlink_to(root/'guide.md')
            (root/'private-alias.md').symlink_to(archive/'notes.md')
            (root/'nested-alias').symlink_to(archive/'nested', target_is_directory=True)
            (root/'README.md').write_text(
                '[Archived alias](.local-archive/public-alias.md)\n'
                '[Hidden archive](private-alias.md)\n'
                '[Parent after alias](nested-alias/../notes.md)\n'
            )
            code,data=self.check(root)
            self.assertEqual(code,1)
            self.assertEqual(len(data['errors']),3)
            self.assertTrue(all('Local-only archive link:' in error for error in data['errors']))

    def test_nested_directory_named_local_archive_remains_live(self):
        with tempfile.TemporaryDirectory() as directory:
            root=Path(directory)
            (root/'catalog').mkdir()
            nested=root/'examples/.local-archive'
            nested.mkdir(parents=True)
            (root/'README.md').write_text('[Live example](examples/.local-archive/notes.md#example)\n')
            (nested/'notes.md').write_text('# Example\n[Missing](missing.md)\n')
            code,data=self.check(root)
            self.assertEqual(code,1)
            self.assertEqual(data['markdown_files'],2)
            self.assertEqual(data['errors'],['Missing: examples/.local-archive/notes.md -> missing.md'])
            (nested/'notes.md').write_text('# Example\n')
            code,data=self.check(root)
            self.assertEqual(code,0)
            self.assertEqual(data['errors'],[])


if __name__=='__main__':
    unittest.main()
