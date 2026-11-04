from collections import Counter
import json
from pathlib import Path
import re
import subprocess
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "scripts"))
from download_papers import load_catalog

SAMPLE = re.compile(r'proof_templates\.py search "([^"]+)" --limit (\d+)\n```\n\n```text\n(.*?)```', re.S)


class ReadmeFactsTests(unittest.TestCase):
    """Numbers and sample output quoted in the READMEs must match the library."""

    @classmethod
    def setUpClass(cls):
        registry = json.loads((ROOT / "proofs/registry.json").read_text(encoding="utf-8"))
        cls.topics = len(registry["topics"])
        cls.cards = len(registry["templates"])
        cls.kinds = Counter(row["kind"] for row in registry["templates"])
        cls.notes = len(list((ROOT / "Math 基础").rglob("*.md")))
        cls.papers = len(load_catalog(ROOT))
        cls.readmes = {name: (ROOT / name).read_text(encoding="utf-8") for name in ("README.md", "README.en.md")}

    def test_headline_counts_match_the_library(self):
        expected = {
            "README.md": f"{self.topics} 个主题 · {self.cards} 张模板与工具卡 · {self.notes} 篇数学前置 · {self.papers} 篇论文条目",
            "README.en.md": f"{self.topics} topics · {self.cards} template and tool cards · "
                            f"{self.notes} prerequisite notes · {self.papers} paper records",
        }
        for name, line in expected.items():
            with self.subTest(readme=name):
                self.assertIn(line, self.readmes[name])

    def test_card_breakdown_matches_registry_kinds(self):
        k = self.kinds
        # A new kind needs its own wording in both READMEs.
        self.assertEqual(set(k), {"proof-template", "method-card", "project-tool", "router"})
        expected = {
            "README.md": f"{self.cards} 张卡包括 {k['proof-template']} 个证明模板、{k['method-card']} 张问题特定方法卡、"
                         f"{k['project-tool']} 个经验代数工具和 {k['router']} 个路由页",
            "README.en.md": f"The {self.cards} cards comprise {k['proof-template']} proof templates, "
                            f"{k['method-card']} problem-specific method cards, {k['project-tool']} empirical algebra tool, "
                            f"and {k['router']} routing page",
        }
        for name, line in expected.items():
            with self.subTest(readme=name):
                self.assertIn(line, self.readmes[name])

    def test_sample_search_output_is_current(self):
        for name, text in self.readmes.items():
            with self.subTest(readme=name):
                samples = SAMPLE.findall(text)
                self.assertEqual(len(samples), 1)
                query, limit, shown = samples[0]
                result = subprocess.run(
                    [sys.executable, "-B", str(ROOT / "scripts/proof_templates.py"), "search", query, "--limit", limit],
                    cwd=ROOT, capture_output=True, text=True, check=True)
                self.assertEqual(result.stdout, shown)


if __name__ == "__main__":
    unittest.main()
