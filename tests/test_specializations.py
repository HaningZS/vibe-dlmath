import json
import math
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"examples"))
sys.path.insert(0,str(ROOT/"scripts"))
from dl_specialization_checks import bernoulli_kl, projected_square_train, run_checks
from proof_templates import load_registry, search
from download_papers import update_card


class SpecializationTests(unittest.TestCase):
    def test_research_questions_have_specific_routes(self):
        data = load_registry(ROOT)
        queries = {
            "二阶驻点 负曲率":"T40",
            "Barron 高维逼近 随机特征":"T41",
            "核漂移 特征学习":"T42",
            "群作用 排列等变 mask":"T43",
            "GNN 1-WL 消息传递":"T44",
            "鲁棒认证 随机平滑":"T45",
            "RDP DP-SGD 隐私预算":"T46",
            "FedAvg 客户端漂移 通信":"T47",
            "因果识别 潜在结果":"T48",
            "交叉熵 分类风险 替代损失":"T49",
        }
        for query,expected in queries.items():
            with self.subTest(query=query):
                self.assertEqual(search(data,query)[0]["id"],expected)

    def test_small_models_check_the_boundaries(self):
        result = run_checks()
        self.assertEqual(len(result),11)
        self.assertAlmostEqual(result["privacy"]["integrated_rdp"],result["privacy"]["formula_rdp"],places=9)
        self.assertTrue(result["attention_equivariance"]["fixed_positions_break_it"])
        self.assertNotEqual(result["causal_nonidentification"]["first_ate"],result["causal_nonidentification"]["second_ate"])

    def test_training_input_contract_and_surrogate_endpoints(self):
        for args in (([[2.]], [1.], 1., 4), ([[1.]], [1.], 0., 4), ([[1.]], [1.], 1., 0)):
            with self.assertRaises(ValueError):
                projected_square_train(*args)
        self.assertAlmostEqual(bernoulli_kl(0,.5),math.log(2))
        self.assertAlmostEqual(bernoulli_kl(1,.5),math.log(2))

    def test_installed_style_helper_retrieves_new_card_outside_repo(self):
        result = subprocess.run([sys.executable,"-B",str(ROOT/"skills/vibe-dlmath/scripts/templates.py"),
                                 "search","GNN 1-WL 消息传递","--json"],
                                cwd=tempfile.gettempdir(),capture_output=True,text=True,check=True)
        self.assertEqual(json.loads(result.stdout)[0]["id"],"T44")

    def test_generated_paper_card_retains_scoped_review_evidence(self):
        with tempfile.TemporaryDirectory() as directory:
            root = Path(directory)
            paper = root/"proof_ref/paper"
            paper.mkdir(parents=True)
            (paper/"核验笔记.md").write_text("Only one claim checked",encoding="utf-8")
            record = {"path":"proof_ref/paper","arxiv_id":"1702.07476","title":"Example",
                      "topic":"privacy","review_status":"core-claim-checked"}
            update_card(root,record,{})
            self.assertIn("core-claim-checked",(paper/"README.md").read_text())
            self.assertIn("核验笔记.md",(paper/"LINKS.md").read_text())
            original = "Human-owned scope description\n"
            (paper/"README.md").write_text(original,encoding="utf-8")
            update_card(root,record,{})
            self.assertTrue((paper/"README.md").read_text().startswith(original))


if __name__ == "__main__":
    unittest.main()
