from pathlib import Path
import sys
import unittest

ROOT=Path(__file__).resolve().parents[1]
sys.path.insert(0,str(ROOT/"examples"))
sys.path.insert(0,str(ROOT/"scripts"))
from recent_distillation_checks import run_checks
from proof_templates import load_registry, search


class RecentDistillationTests(unittest.TestCase):
    def test_finite_envelope_and_exact_flow_moments(self):
        result=run_checks()
        self.assertLessEqual(result["envelope"]["true_failure_probability"],.1)
        self.assertEqual(len(result["flows"]),12)
        self.assertGreater(result["nonunique_flow"]["selected_path_squared_error"],0)

    def test_new_proof_questions_route_to_the_distilled_cards(self):
        data=load_registry(ROOT)
        self.assertEqual(search(data,"证书 指数包络 期望泛化差")[0]["id"],"T50")
        self.assertEqual(search(data,"Flow Matching 速度误差 误差分布")[0]["id"],"T51")


if __name__ == "__main__":
    unittest.main()
