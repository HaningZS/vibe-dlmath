import io
import json
import sys
import tarfile
import tempfile
import unittest
from pathlib import Path
from unittest.mock import Mock, patch

sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "scripts"))
import download_papers as dp
from import_vault import convert_links

PDF = b"%PDF-1.4\nminimal fixture\n%%EOF\n"


def archive_at(path, name="main.tex", content=b"\\documentclass{article}"):
    with tarfile.open(path, "w:gz") as archive:
        member = tarfile.TarInfo(name)
        member.size = len(content)
        archive.addfile(member, io.BytesIO(content))


class DownloaderTests(unittest.TestCase):
    def setUp(self):
        self.tmp = tempfile.TemporaryDirectory()
        self.root = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def record(self):
        return {"arxiv_id":"1405.4980", "title":"Convex Optimization Algorithms and Complexity",
                "topic":"optimization", "collection":"test", "path":"proof_ref/test/convex-1405.4980"}

    def test_id_urls_and_legacy(self):
        for text in ("1405.4980v2", "https://arxiv.org/abs/1405.4980v2", "https://arxiv.org/pdf/1405.4980v2.pdf"):
            self.assertEqual(dp.normalize_id(text), "1405.4980v2")
        self.assertEqual(dp.normalize_id("arXiv:math/0309135"), "math/0309135")

    def test_reject_lookalike_domain(self):
        for value in ("https://notarxiv.org/abs/1405.4980", "../../data", "blah 1405.4980"):
            with self.assertRaises(ValueError):
                dp.normalize_id(value)

    def test_slug_is_title_first(self):
        self.assertEqual(dp.safe_slug("Convex Optimization", "1405.4980"), "convex-optimization-1405.4980")

    def test_manifest_duplicate_fails(self):
        dp.write_json(self.root / "catalog/a.json", {"schema_version":1, "papers":[self.record()]})
        version = {**self.record(), "arxiv_id":"1405.4980v2"}
        dp.write_json(self.root / "catalog/b.json", {"schema_version":1, "papers":[version]})
        with self.assertRaisesRegex(ValueError, "Duplicate"):
            dp.load_catalog(self.root)

    def test_manifest_path_escape_fails(self):
        for relative in ("../elsewhere", "/absolute/path"):
            with self.assertRaises(ValueError):
                dp.repo_path(self.root, relative)

    def test_pdf_magic_and_eof(self):
        path = self.root / "paper.pdf"
        for data in (b"<html>429</html>", b"%PDF-1.4\ntruncated"):
            path.write_bytes(data)
            with self.assertRaises(ValueError):
                dp.validate_artifact(path, "pdf")
        path.write_bytes(PDF)
        dp.validate_artifact(path, "pdf")

    def test_hash_detects_corrupt_cache(self):
        path = self.root / "paper.pdf"
        path.write_bytes(PDF)
        metadata = {"artifacts":{"pdf":{"sha256":dp.sha256(path)}}}
        self.assertTrue(dp.cached_ok(path, "pdf", metadata))
        path.write_bytes(PDF.replace(b"minimal", b"changed"))
        self.assertFalse(dp.cached_ok(path, "pdf", metadata))

    def test_tar_traversal_and_absolute_rejected(self):
        for name in ("../outside.tex", "/outside.tex", "folder/../../outside.tex", "C:/outside.tex"):
            archive_at(self.root / "source.tar.gz", name)
            with self.assertRaises(ValueError):
                dp.extract_source(self.root / "source.tar.gz", self.root / "source")
            self.assertFalse((self.root / "source").exists())

    def test_symlink_and_device_rejected(self):
        for kind in (tarfile.SYMTYPE, tarfile.LNKTYPE, tarfile.CHRTYPE):
            member = tarfile.TarInfo("unsafe")
            member.type = kind
            with self.assertRaises(ValueError):
                dp.check_members([member])

    def test_expanded_size_limit(self):
        member = tarfile.TarInfo("large.tex")
        member.size = dp.MAX_EXTRACT + 1
        with self.assertRaises(ValueError):
            dp.check_members([member])

    def test_tar_root_directory_is_allowed_but_empty_file_is_not(self):
        member = tarfile.TarInfo(".")
        member.type = tarfile.DIRTYPE
        dp.check_members([member])
        member.type = tarfile.REGTYPE
        with self.assertRaises(ValueError):
            dp.check_members([member])

    def test_extract_preserves_existing_content(self):
        archive_at(self.root / "source.tar.gz")
        destination = self.root / "source"
        dp.extract_source(self.root / "source.tar.gz", destination)
        (destination / "my-notes.md").write_text("keep", encoding="utf-8")
        result = dp.extract_source(self.root / "source.tar.gz", destination)
        self.assertEqual((destination / "my-notes.md").read_text(), "keep")
        self.assertEqual(result["state"], "verified-existing")
        self.assertEqual(result["bundle_sha256"], dp.sha256(self.root / "source.tar.gz"))

    def test_existing_source_must_match_bundle_and_remains_untouched_on_failure(self):
        archive_at(self.root / "source.tar.gz")
        destination = self.root / "source"
        dp.extract_source(self.root / "source.tar.gz", destination)
        changed = destination / "main.tex"
        changed.write_text("A different or edited theorem", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "differs from the current bundle"):
            dp.extract_source(self.root / "source.tar.gz", destination)
        self.assertEqual(changed.read_text(), "A different or edited theorem")
        self.assertFalse(list(self.root.glob(".extract-*")))

    def test_existing_source_rejects_missing_original_and_extra_tex(self):
        archive_at(self.root / "source.tar.gz")
        destination = self.root / "source"
        dp.extract_source(self.root / "source.tar.gz", destination)
        (destination / "other-version.tex").write_text("extra theorem", encoding="utf-8")
        with self.assertRaisesRegex(ValueError, "TeX absent"):
            dp.extract_source(self.root / "source.tar.gz", destination)
        (destination / "other-version.tex").unlink()
        (destination / "main.tex").unlink()
        with self.assertRaisesRegex(ValueError, "differs from the current bundle"):
            dp.extract_source(self.root / "source.tar.gz", destination)

    def test_existing_source_rejects_symlink_without_following_or_replacing_it(self):
        archive_at(self.root / "source.tar.gz")
        destination = self.root / "source"
        dp.extract_source(self.root / "source.tar.gz", destination)
        original = destination / "main.tex"
        contents = original.read_bytes()
        external = self.root / "external.tex"
        external.write_bytes(contents)
        original.unlink()
        original.symlink_to(external)
        with self.assertRaisesRegex(ValueError, "symlinks"):
            dp.extract_source(self.root / "source.tar.gz", destination)
        self.assertTrue(original.is_symlink())
        self.assertEqual(external.read_bytes(), contents)

    def test_changed_bundle_does_not_silently_reuse_previous_extraction(self):
        path = self.root / "source.tar.gz"
        archive_at(path, content=b"\\documentclass{article}\nVersion one")
        destination = self.root / "source"
        dp.extract_source(path, destination)
        archive_at(path, content=b"\\documentclass{article}\nVersion two")
        with self.assertRaisesRegex(ValueError, "differs from the current bundle"):
            dp.extract_source(path, destination)
        self.assertIn("Version one", (destination / "main.tex").read_text())

    def test_gzipped_single_tex_can_be_verified_again(self):
        import gzip
        path = self.root / "source.tar.gz"
        with gzip.open(path, "wb") as handle:
            handle.write(b"\\documentclass{article}\nSingle source")
        destination = self.root / "source"
        self.assertEqual(dp.extract_source(path, destination)["state"], "extracted")
        self.assertEqual(dp.extract_source(path, destination)["state"], "verified-existing")

    def test_invalid_source_keeps_no_partial_directory(self):
        archive_at(self.root / "source.tar.gz", "image.png", b"not TeX")
        with self.assertRaises(ValueError):
            dp.extract_source(self.root / "source.tar.gz", self.root / "source")
        self.assertFalse((self.root / "source").exists())
        self.assertFalse(list(self.root.glob(".extract-*")))

    def test_metadata_pins_version_and_decodes_title(self):
        client = Mock()
        client.text.return_value = '<meta name="citation_title" content="A &amp; B"><meta name="citation_author" content="Author">1405.4980v1 1405.4980v2'
        result = dp.fetch_metadata("1405.4980", client)
        self.assertEqual(result["resolved_id"], "1405.4980v2")
        self.assertEqual(result["title"], "A & B")
        self.assertEqual(dp.fetch_metadata("1405.4980v1", client)["resolved_id"], "1405.4980v1")

    def test_valid_cache_skips_network_preserves_readme(self):
        record = self.record()
        directory = dp.repo_path(self.root, record["path"])
        directory.mkdir(parents=True)
        (directory / "paper.pdf").write_bytes(PDF)
        archive_at(directory / "source.tar.gz")
        (directory / "README.md").write_text("human backlink", encoding="utf-8")
        client = Mock()
        result = dp.download_one(self.root, record, client)
        self.assertFalse(result["errors"])
        self.assertEqual(result["actions"], {"pdf":"cached", "source":"cached"})
        client.text.assert_not_called()
        client.download.assert_not_called()
        self.assertTrue((directory / "README.md").read_text().startswith("human backlink"))
        dp.update_card(self.root, record, {})
        self.assertEqual((directory / "README.md").read_text().count("[学习关联与返回路径](LINKS.md)"), 1)

    def test_source_failure_does_not_erase_pdf_success(self):
        record = self.record()
        client = Mock()
        def download(url, path, kind):
            if kind == "source":
                raise OSError("source unavailable")
            path.write_bytes(PDF)
        client.download.side_effect = download
        with patch.object(dp, "fetch_metadata", return_value={"title":record["title"], "resolved_id":"1405.4980v2"}):
            result = dp.download_one(self.root, record, client)
        self.assertEqual(result["actions"]["pdf"], "downloaded")
        self.assertIn("source", result["errors"])

    def test_metadata_identity_and_explicit_version_conflicts_preserve_everything(self):
        cases = [
            (self.record(), {"resolved_id": "2105.04026v1"}),
            (self.record(), {"resolved_id": "1405.4980"}),
            (self.record(), {"identifier": "2105.04026", "resolved_id": "1405.4980v1"}),
            ({**self.record(), "arxiv_id": "1405.4980v1"}, {"resolved_id": "1405.4980v2"}),
            (self.record(), {"identifier": "1405.4980v1", "resolved_id": "1405.4980v2"}),
        ]
        for record, metadata in cases:
            with self.subTest(metadata=metadata):
                directory = dp.repo_path(self.root, record["path"])
                directory.mkdir(parents=True, exist_ok=True)
                path = directory / "metadata.json"
                dp.write_json(path, metadata)
                (directory / "paper.pdf").write_bytes(PDF)
                before = path.read_bytes()
                client = Mock()
                result = dp.download_one(self.root, record, client)
                self.assertIn("metadata", result["errors"])
                client.text.assert_not_called()
                client.download.assert_not_called()
                self.assertEqual(path.read_bytes(), before)
                self.assertEqual((directory / "paper.pdf").read_bytes(), PDF)

    def test_partial_legacy_cache_cannot_be_relabelled_with_a_new_pin(self):
        record = self.record()
        directory = dp.repo_path(self.root, record["path"])
        directory.mkdir(parents=True)
        (directory / "paper.pdf").write_bytes(PDF)
        metadata = {"artifacts": {"pdf": {"sha256": dp.sha256(directory / "paper.pdf")}}}
        path = directory / "metadata.json"
        dp.write_json(path, metadata)
        before = path.read_bytes()
        client = Mock()
        result = dp.download_one(self.root, record, client)
        self.assertIn("legacy-unpinned", result["errors"]["metadata"])
        client.text.assert_not_called()
        client.download.assert_not_called()
        self.assertEqual(path.read_bytes(), before)
        self.assertEqual((directory / "paper.pdf").read_bytes(), PDF)
        self.assertFalse((directory / "source.tar.gz").exists())

    def test_fresh_clone_with_unpinned_expected_hashes_also_requires_version_review(self):
        record = self.record()
        path = dp.repo_path(self.root, record["path"]) / "metadata.json"
        dp.write_json(path, {"artifacts": {"pdf": {"sha256": "a" * 64}}})
        before = path.read_bytes()
        client = Mock()
        result = dp.download_one(self.root, record, client)
        self.assertIn("fresh clone", result["errors"]["metadata"])
        client.text.assert_not_called()
        client.download.assert_not_called()
        self.assertEqual(path.read_bytes(), before)

    def test_refresh_does_not_relabel_complete_legacy_cache(self):
        record = self.record()
        directory = dp.repo_path(self.root, record["path"])
        directory.mkdir(parents=True)
        (directory / "paper.pdf").write_bytes(PDF)
        archive_at(directory / "source.tar.gz")
        client = Mock()
        result = dp.download_one(self.root, record, client, refresh=True)
        self.assertIn("legacy-unpinned", result["errors"]["metadata"])
        client.text.assert_not_called()
        client.download.assert_not_called()
        self.assertFalse((directory / "metadata.json").exists())

    def test_pinned_empty_clone_downloads_exact_edition_without_metadata_refresh(self):
        record = self.record()
        directory = dp.repo_path(self.root, record["path"])
        dp.write_json(directory / "metadata.json", {"resolved_id": "1405.4980v1"})
        client = Mock()
        def download(url, path, kind):
            self.assertIn("1405.4980v1", url)
            if kind == "pdf":
                path.write_bytes(PDF)
            else:
                archive_at(path)
        client.download.side_effect = download
        result = dp.download_one(self.root, record, client)
        self.assertFalse(result["errors"])
        self.assertEqual(result["actions"], {"pdf": "downloaded", "source": "downloaded"})
        client.text.assert_not_called()
        metadata = json.loads((directory / "metadata.json").read_text())
        self.assertEqual(metadata["source_extraction"]["state"], "extracted")

    def test_redownload_must_match_recorded_hash_before_replacing_any_file(self):
        record = self.record()
        directory = dp.repo_path(self.root, record["path"])
        directory.mkdir(parents=True)
        original = directory / "paper.pdf"
        original.write_bytes(PDF)
        expected = dp.sha256(original)
        original.write_bytes(PDF.replace(b"minimal", b"local modified"))
        kept = original.read_bytes()
        metadata_path = directory / "metadata.json"
        dp.write_json(metadata_path, {"resolved_id": "1405.4980v1", "artifacts": {"pdf": {"sha256": expected}}})
        client = Mock()
        client.download.side_effect = lambda url, path, kind: path.write_bytes(PDF.replace(b"minimal", b"different remote"))
        result = dp.download_one(self.root, record, client, sources=False)
        self.assertIn("differ from the recorded SHA-256", result["errors"]["pdf"])
        self.assertEqual(original.read_bytes(), kept)
        metadata = json.loads(metadata_path.read_text())
        self.assertEqual(metadata["artifacts"]["pdf"]["sha256"], expected)
        self.assertFalse(list(directory.glob(".partial-check-*")))

    def test_pinned_empty_clone_keeps_expected_hash_when_remote_bytes_disagree(self):
        record = self.record()
        directory = dp.repo_path(self.root, record["path"])
        metadata_path = directory / "metadata.json"
        dp.write_json(metadata_path, {"resolved_id": "1405.4980v1", "artifacts": {"pdf": {"sha256": "0" * 64}}})
        client = Mock()
        client.download.side_effect = lambda url, path, kind: path.write_bytes(PDF)
        result = dp.download_one(self.root, record, client, sources=False)
        self.assertIn("differ from the recorded SHA-256", result["errors"]["pdf"])
        self.assertFalse((directory / "paper.pdf").exists())
        self.assertEqual(json.loads(metadata_path.read_text())["artifacts"]["pdf"]["sha256"], "0" * 64)

    def test_extraction_mismatch_reports_error_and_clears_stale_verification_record(self):
        record = self.record()
        directory = dp.repo_path(self.root, record["path"])
        directory.mkdir(parents=True)
        (directory / "paper.pdf").write_bytes(PDF)
        archive_at(directory / "source.tar.gz")
        dp.extract_source(directory / "source.tar.gz", directory / "source")
        (directory / "source/main.tex").write_text("Unrelated theorem", encoding="utf-8")
        dp.write_json(directory / "metadata.json", {"resolved_id": "1405.4980v1", "source_extraction": {"state": "verified-existing"}})
        result = dp.download_one(self.root, record, Mock())
        self.assertIn("differs from the current bundle", result["errors"]["extract"])
        metadata = json.loads((directory / "metadata.json").read_text())
        self.assertNotIn("source_extraction", metadata)
        self.assertEqual((directory / "source/main.tex").read_text(), "Unrelated theorem")

    def test_versioned_ids_cli_is_rejected_instead_of_silently_stripping_version(self):
        dp.write_json(self.root / "catalog/a.json", {"schema_version": 1, "papers": [self.record()]})
        output = io.StringIO()
        with patch("sys.stderr", output), self.assertRaises(SystemExit) as result:
            dp.main(["--root", str(self.root), "--ids", "1405.4980v1", "--dry-run"])
        self.assertEqual(result.exception.code, 2)
        self.assertIn("base arXiv IDs only", output.getvalue())
        self.assertFalse((self.root / ".download.lock").exists())

    def test_title_mismatch_prevents_download(self):
        client = Mock()
        with patch.object(dp, "fetch_metadata", return_value={"title":"An unrelated paper", "resolved_id":"1405.4980v2"}):
            result = dp.download_one(self.root, self.record(), client)
        self.assertIn("metadata", result["errors"])
        client.download.assert_not_called()

    def test_atomic_failed_download_preserves_old_file(self):
        path = self.root / "paper.pdf"
        path.write_bytes(PDF)
        client = dp.Client(retries=0, delay=0)
        with patch.object(client, "open", return_value=io.BytesIO(b"<html>broken</html>")):
            with self.assertRaises(ValueError):
                client.download("https://arxiv.org/pdf/1405.4980", path, "pdf")
        self.assertEqual(path.read_bytes(), PDF)
        self.assertFalse(list(self.root.glob(".partial-*")))

    def test_reindex_rejects_identity_conflict_before_rewriting_metadata(self):
        record=self.record()
        path=self.root/record["path"]/"metadata.json"
        dp.write_json(path,{"identifier":"2105.04026","resolved_id":"2105.04026v2",
                            "path":"proof_ref/another-paper","topic":"different"})
        before=path.read_bytes()
        with self.assertRaises(ValueError):
            dp.write_reports(self.root,[record])
        self.assertEqual(path.read_bytes(),before)
        self.assertFalse((self.root/"PAPERS.md").exists())

    def test_both_fence_styles_survive_export(self):
        source = self.root / "source.md"
        source.write_text("", encoding="utf-8")
        for fence in ("```", "~~~"):
            text = f"{fence}python\nx = [[0.7]]\n{fence}\n"
            self.assertEqual(convert_links(text, source, self.root, {source:self.root / "out.md"}, [source], "abc", set()), text)


if __name__ == "__main__":
    unittest.main()
