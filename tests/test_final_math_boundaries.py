"""Finite exact counterexamples for dependence assumptions, not universal proofs."""
from fractions import Fraction
from itertools import product
import unittest


class FinalMathBoundaryTests(unittest.TestCase):
    def test_reward_selected_policy_bias_survives_true_nuisances(self):
        # Every action has true value 1/2; each (A,Y) has probability 1/4.
        # Choosing a policy from this very Y defeats the usual DR conditioning.
        scores = []
        for action, reward in product((0, 1), repeat=2):
            chosen = action if reward else 1 - action
            score = Fraction(1, 2) + 2 * (chosen == action) * (
                reward - Fraction(1, 2)
            )
            scores.append(score)
        self.assertEqual(sum(scores) / 4, 1)
        self.assertEqual(sum(scores) / 4 - Fraction(1, 2), Fraction(1, 2))
        # Both nuisance errors are zero, so the invalidly applied product is zero.
        self.assertEqual((Fraction(1, 2) - Fraction(1, 2)) ** 2, 0)

    def test_fixed_policy_dr_expectation_restores_true_value(self):
        # Enumerate each possible fixed policy separately, rather than averaging
        # an adaptively selected policy as though it had been fixed.
        for chosen in (0, 1):
            scores = [
                Fraction(1, 2) + 2 * (chosen == action)
                * (reward - Fraction(1, 2))
                for action, reward in product((0, 1), repeat=2)
            ]
            self.assertEqual(sum(scores) / 4, Fraction(1, 2))

    def test_calibration_input_memorizer_breaks_coverage_without_labels(self):
        # Finite analogue of T18's continuous counterexample: three IID inputs
        # from four atoms, n=2 and alpha=1/3, hence corrected order k=2.
        # All labels are zero. Calibration scores are always zero; a test point
        # is covered only if its input is already in the calibration set.
        outcomes = list(product(range(4), repeat=3))
        covered = sum(test in (x1, x2) for x1, x2, test in outcomes)
        self.assertEqual(Fraction(covered, len(outcomes)), Fraction(7, 16))
        self.assertLess(Fraction(covered, len(outcomes)), Fraction(2, 3))

    def test_fixed_score_preserves_conformal_rank_guarantee(self):
        # On the same exhaustive IID law, fixed s(x,y)=x yields the valid
        # k=2 threshold max(x1,x2); ties are handled by <=.
        outcomes = list(product(range(4), repeat=3))
        covered = sum(test <= max(x1, x2) for x1, x2, test in outcomes)
        self.assertGreaterEqual(Fraction(covered, len(outcomes)), Fraction(2, 3))

    def test_mixing_model_means_does_not_preserve_zero_subgaussian_noise(self):
        # ell(w,z)=w: each fixed model has no sampling noise, yet mixing models
        # produces variance 1/4. Centering by L_D(w) makes G identically zero.
        losses_by_model = {0: (Fraction(0), Fraction(0)),
                           1: (Fraction(1), Fraction(1))}
        centered_gaps = []
        mixed_losses = []
        for losses in losses_by_model.values():
            model_mean = sum(losses) / len(losses)
            self.assertEqual(sum((value - model_mean) ** 2 for value in losses), 0)
            centered_gaps.extend(model_mean - value for value in losses)
            mixed_losses.extend(losses)
        overall_mean = sum(mixed_losses) / len(mixed_losses)
        overall_variance = sum((value - overall_mean) ** 2 for value in mixed_losses) / len(mixed_losses)
        self.assertEqual(overall_variance, Fraction(1, 4))
        self.assertTrue(all(value == 0 for value in centered_gaps))


if __name__ == "__main__":
    unittest.main()
