import json
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
import proof_templates as pt
from check_library import anchors
from download_papers import base_id, load_catalog
from install_skill import install


class TemplateTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pt.load_registry(ROOT)

    def test_legacy_ids_and_children_remain_addressable(self):
        ids = {row["id"] for row in self.data["templates"]}
        self.assertTrue(({f"T{i:02d}" for i in range(1,26)} | {"T20A","T20B"}) <= ids)
        self.assertTrue({f"T{i}" for i in range(32,40)} <= ids)
        self.assertFalse(ids & {f"T{i}" for i in range(26,32)})

    def test_old_anchors_and_blocks_remain_valid(self):
        actual = anchors(ROOT / "证明模板库（待核查）.md")
        for row in self.data["templates"]:
            if row.get("legacy_anchor"):
                self.assertIn(row["legacy_anchor"], actual)
            for block in row.get("legacy_blocks", []):
                self.assertIn(block, actual)
                self.assertIn(block, anchors(ROOT / row["path"]))

    def test_contracts_and_obligations_can_be_loaded(self):
        for row in self.data["templates"]:
            text = (ROOT / row["path"]).read_text(encoding="utf-8")
            self.assertTrue(pt.section(text, "复用契约"))
            self.assertIn("- [ ]", pt.section(text, "实例化时必须完成"))

    def test_sources_and_related_routes_resolve(self):
        papers = {base_id(row["arxiv_id"]) for row in load_catalog(ROOT)}
        for row in self.data["templates"]:
            self.assertTrue({base_id(item) for item in row["sources"]} <= papers)
            for related in row["related"]:
                self.assertTrue((ROOT / pt.get_template(self.data, related)["path"]).is_file())

    def test_exact_id_takes_precedence(self):
        self.assertEqual(pt.search(self.data, "t20b 能力限制")[0]["id"], "T20B")

    def test_chinese_and_english_queries(self):
        self.assertEqual(pt.search(self.data, "重尾裁剪")[0]["id"], "T16")
        self.assertEqual(pt.search(self.data, "mean-field")[0]["id"], "T10")
        self.assertIn("T05", {row["id"] for row in pt.search(self.data, "PAC-Bayes 高概率泛化")})

    def test_unknown_query_does_not_invent_a_match(self):
        self.assertEqual(pt.search(self.data, "unrelated-navigation-widget"), [])
        self.assertEqual(pt.search(self.data, ""), [])

    def test_quantifier_query_finds_expected_vs_high_probability_card(self):
        self.assertEqual(pt.search(self.data, "期望界 高概率")[0]["id"], "T05")
        self.assertEqual(pt.search(self.data, "互信息 期望 高概率")[0]["id"], "T05")

    def test_non_theorem_types_survive_retrieval(self):
        self.assertEqual(pt.search(self.data, "T24")[0]["kind"], "project-tool")
        self.assertEqual(pt.search(self.data, "T25")[0]["kind"], "method-card")
        self.assertEqual(pt.search(self.data, "T17")[0]["kind"], "method-card")
        self.assertEqual(pt.search(self.data, "T20")[0]["kind"], "router")

    def test_unknown_id_fails(self):
        with self.assertRaises(ValueError):
            pt.get_template(self.data, "T99")

    def test_scaffold_is_explicit_draft_and_preserves_existing_file(self):
        with tempfile.TemporaryDirectory() as directory:
            output = Path(directory) / "proof.md"
            pt.worksheet(ROOT, self.data, ["T02", "T16"], "分析裁剪与动量", output)
            text = output.read_text()
            self.assertIn("未完成证明", text)
            self.assertIn("失败例子", text)
            self.assertIn("T02", text)
            self.assertIn("T16", text)
            with self.assertRaises(FileExistsError):
                pt.worksheet(ROOT, self.data, ["T01"], "overwrite", output)
            self.assertEqual(text, output.read_text())

    def test_router_and_duplicate_scaffolds_are_rejected(self):
        with tempfile.TemporaryDirectory() as directory:
            for ids in (["T20"], ["T01","T01"]):
                with self.assertRaises(ValueError):
                    pt.worksheet(ROOT, self.data, ids, "question", Path(directory)/"out.md")
            self.assertFalse((Path(directory)/"out.md").exists())

    def test_registry_rejects_escape(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "proofs").mkdir()
            data = json.loads(json.dumps(self.data))
            data["templates"][0]["path"] = "../outside.md"
            (root / "proofs/registry.json").write_text(json.dumps(data))
            with self.assertRaises(ValueError):
                pt.load_registry(root)

    def test_install_is_idempotent_and_does_not_overwrite(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            source = root / "source"
            source.mkdir()
            (source / "SKILL.md").write_text("skill")
            target = root / "skills/vibe-dlmath"
            self.assertEqual(install(source, target), "linked")
            self.assertEqual(install(source, target), "already-linked")
            other = root / "other"
            other.mkdir()
            (other / "SKILL.md").write_text("different")
            with self.assertRaises(FileExistsError):
                install(other, target)
            self.assertEqual(target.resolve(), source.resolve())

    def test_unsafe_topic_cannot_escape_index_directory(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            (root / "proofs").mkdir()
            data = json.loads(json.dumps(self.data))
            data["topics"]["../outside"] = "invalid"
            (root / "proofs/registry.json").write_text(json.dumps(data))
            with self.assertRaisesRegex(ValueError, "Topic names"):
                pt.load_registry(root)

    def test_skill_helper_finds_repository_from_another_directory(self):
        helper = ROOT / "skills/vibe-dlmath/scripts/templates.py"
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(helper), "search", "T18", "--json"],
                cwd=directory, capture_output=True, text=True, check=True,
            )
            self.assertEqual(json.loads(result.stdout)[0]["id"], "T18")

    def test_skill_explicit_invalid_root_fails_without_fallback(self):
        helper = ROOT / "skills/vibe-dlmath/scripts/templates.py"
        with tempfile.TemporaryDirectory() as directory:
            result = subprocess.run(
                [sys.executable, str(helper), "--repo", directory, "list"],
                capture_output=True, text=True,
            )
            self.assertNotEqual(result.returncode, 0)
            self.assertIn("Cannot find", result.stderr)

    def test_forwarded_sgd_search_finds_a_usable_card(self):
        helper = ROOT / "skills/vibe-dlmath/scripts/templates.py"
        result = subprocess.run(
            [sys.executable, str(helper), "search", "SGD 无偏 梯度范数", "--json"],
            capture_output=True, text=True, check=True,
        )
        candidate = json.loads(result.stdout)[0]
        self.assertEqual(candidate["id"], "T01")
        self.assertEqual(candidate["kind"], "proof-template")
        self.assertIn("复用契约", (ROOT / candidate["path"]).read_text())


if __name__ == "__main__":
    unittest.main()
