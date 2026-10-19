import sys
from pathlib import Path
import tempfile
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"scripts"))
sys.path.insert(0,str(ROOT/"examples"))
import proof_templates as pt
from dl_core_checks import run_checks


class DLCoreTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.data = pt.load_registry(ROOT)

    def test_core_questions_route_to_relevant_cards(self):
        cases = {
            "逼近误差 估计误差 优化误差":"T32",
            "训练梯度趋零 万能逼近 测试风险 Bayes 风险":"T32",
            "一致收敛 Rademacher":"T33",
            "ReLU 逼近":"T34",
            "margin 谱范数":"T35",
            "隐式偏置 方向收敛":"T36",
            "InfoNCE 下游":"T37",
            "压缩 描述长度":"T38",
            "ReLU 非光滑 gradient mapping":"T39",
        }
        for query, expected in cases.items():
            with self.subTest(query=query):
                self.assertEqual(pt.search(self.data,query)[0]["id"],expected)

    def test_core_numerical_identities(self):
        results=run_checks()
        self.assertEqual(len(results),7)
        self.assertLessEqual(results["infonce"]["lower_bound"],results["infonce"]["mutual_information"])

    def test_worksheet_includes_assumption_and_resource_audit(self):
        with tempfile.TemporaryDirectory() as directory:
            path=Path(directory)/"dl-proof.md"
            pt.worksheet(ROOT,self.data,["T32","T33"],"证明训练结果的测试风险界",path)
            text=path.read_text()
            self.assertIn("未完成证明",text)
            self.assertIn("假设与引理账本",text)
            self.assertIn("范围与资源检查",text)
            self.assertIn("数据依赖",text)


if __name__ == "__main__":
    unittest.main()
