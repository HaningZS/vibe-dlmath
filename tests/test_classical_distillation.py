import json
from pathlib import Path
import sys
import unittest

ROOT = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(ROOT / "examples"))
sys.path.insert(0, str(ROOT / "scripts"))
from audit_proof import audit
from classical_distillation_checks import (data_dependent_decoder_counterexample,
    persistent_bias_counterexample, prefix_code_failure_probability, quadratic_noise_tree)


class ClassicalDistillationTests(unittest.TestCase):
    def test_actual_noise_tree_satisfies_conditional_and_summed_bounds(self):
        result = quadratic_noise_tree()
        self.assertEqual(result["paths"], 729)
        self.assertAlmostEqual(result["total_probability"], 1)
        self.assertAlmostEqual(result["conditional_noise_variance"], 0.14)
        self.assertGreaterEqual(result["minimum_conditional_step_slack"], -1e-12)
        self.assertLessEqual(result["expected_average_gradient_squared"], result["theorem_upper_bound"]+1e-12)

    def test_omitting_persistent_bias_predicts_a_false_zero_bound(self):
        result = persistent_bias_counterexample(steps=8, bias=0.3)
        self.assertAlmostEqual(result["last_position"], -0.3)
        self.assertAlmostEqual(result["last_estimated_gradient"], 0)
        self.assertAlmostEqual(result["actual_average_gradient_squared"], 7*0.09/8)
        self.assertGreater(result["actual_average_gradient_squared"], result["incorrect_unbiased_bound"])
        self.assertLessEqual(result["actual_average_gradient_squared"], result["correct_bias_budget"])

    def test_exact_sample_enumeration_respects_both_simultaneous_code_bounds(self):
        result = prefix_code_failure_probability()
        self.assertAlmostEqual(result["kraft_sum"], 1)
        self.assertAlmostEqual(result["total_sample_probability"], 1)
        self.assertGreater(result["simultaneous_failure_probability"], 0)
        self.assertLessEqual(result["simultaneous_failure_probability"], result["delta"])
        self.assertLessEqual(result["zero_training_error_failure_probability"], result["delta"])

    def test_free_data_dependent_decoder_violates_the_claimed_one_bit_bound(self):
        result = data_dependent_decoder_counterexample()
        self.assertEqual(result["training_error"], 0)
        self.assertEqual(result["error_averaged_over_fair_labels_at_a_fresh_input"], 0.5)
        self.assertLess(result["incorrect_one_bit_bound"], 0.17)
        self.assertLess(result["incorrect_zero_training_error_bound"], 0.058)

    def test_complete_biased_sgd_example_is_accepted_under_its_given_assumptions(self):
        data = json.loads((ROOT / "examples/biased_sgd_ledger.json").read_text(encoding="utf-8"))
        result = audit(data, ROOT)
        self.assertTrue(result["ledger_consistent"], result["errors"])
        self.assertTrue(result["target_closed_under_given_assumptions"])
        self.assertEqual(result["mathematical_validity"], "not_checked")


if __name__ == "__main__":
    unittest.main()
