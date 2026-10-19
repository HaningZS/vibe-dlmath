#!/usr/bin/env python3
"""Finite independent examples for the two classical distillations, not proofs."""
from __future__ import annotations

from itertools import product
import json
import math


def quadratic_noise_tree(steps=6):
    """Enumerate all branches of an actual two-dimensional stochastic update."""
    if not isinstance(steps, int) or not 1 <= steps <= 9:
        raise ValueError("Use 1 to 9 steps for this exponential-size illustration")
    curvature = (1.0, 3.0)
    smoothness, eta = 3.0, 0.2
    initial = (0.8, -0.5)
    noises = ((0.4, 0.0), (-0.2, 0.3), (-0.2, -0.3))
    variance = sum(sum(v*v for v in noise) for noise in noises) / len(noises)

    def objective(x):
        return 0.5 * sum(c*v*v for c, v in zip(curvature, x))

    states = [(1.0, initial)]
    gradient_sum = bias_sum = 0.0
    min_step_slack = math.inf
    for t in range(steps):
        next_states = []
        for probability, x in states:
            gradient = tuple(c*v for c, v in zip(curvature, x))
            bias = (0.15 + 0.04*x[0], -0.08 + 0.02*t)
            gradient_squared = sum(v*v for v in gradient)
            bias_squared = sum(v*v for v in bias)
            gradient_sum += probability * gradient_squared
            bias_sum += probability * bias_squared
            actual_next_value = 0.0
            for noise in noises:
                updated = tuple(x[j] - eta*(gradient[j]+bias[j]+noise[j]) for j in range(2))
                actual_next_value += objective(updated) / len(noises)
                next_states.append((probability / len(noises), updated))
            predicted_upper = (objective(x) - eta*gradient_squared/2
                               + eta*bias_squared/2 + smoothness*eta**2*variance/2)
            min_step_slack = min(min_step_slack, predicted_upper-actual_next_value)
        states = next_states
    average_gradient = gradient_sum / steps
    bound = (2*objective(initial)/(eta*steps) + bias_sum/steps
             + smoothness*eta*variance)
    return {
        "paths": len(states), "total_probability": sum(p for p, _ in states),
        "expected_average_gradient_squared": average_gradient, "theorem_upper_bound": bound,
        "minimum_conditional_step_slack": min_step_slack,
        "expected_terminal_objective": sum(p*objective(x) for p, x in states),
        "average_bias_squared": bias_sum/steps, "conditional_noise_variance": variance,
    }


def persistent_bias_counterexample(steps=8, bias=0.3):
    """Follow x <- x - (x+b) for f(x)=x²/2, starting at its minimizer."""
    if steps < 2:
        raise ValueError("At least two iterates are needed to expose the omitted bias")
    x, gradient_sum = 0.0, 0.0
    for _ in range(steps):
        gradient_sum += x*x
        x -= x+bias
    return {
        "last_position": x, "last_estimated_gradient": x+bias,
        "actual_average_gradient_squared": gradient_sum/steps,
        "correct_bias_budget": bias*bias,
        "incorrect_unbiased_bound": 0.0,
    }


def prefix_code_failure_probability(sample_size=12, delta=0.2):
    """Exactly sum multinomial sample probabilities for a fixed four-model code."""
    if not 1 <= sample_size <= 30 or not 0 < delta < 1:
        raise ValueError("Use sample size 1..30 and delta in (0,1)")
    atoms = tuple(product((0, 1), repeat=2))
    # X is a fair bit, Y is independently Bernoulli(1/4).
    masses = tuple(0.5*(0.25 if y else 0.75) for _, y in atoms)
    models = (lambda x: 0, lambda x: 1, lambda x: x, lambda x: 1-x)
    codes = ("0", "10", "110", "111")
    losses = tuple(tuple(float(model(x) != y) for x, y in atoms) for model in models)
    risks = tuple(sum(p*loss for p, loss in zip(masses, row)) for row in losses)
    penalties = tuple(math.sqrt((len(code)*math.log(2)+math.log(1/delta))/(2*sample_size))
                      for code in codes)
    failure_probability = total_probability = 0.0
    zero_error_failure_probability = 0.0
    for a in range(sample_size+1):
        for b in range(sample_size-a+1):
            for c in range(sample_size-a-b+1):
                counts = (a, b, c, sample_size-a-b-c)
                multiplicity = math.factorial(sample_size)
                for count in counts:
                    multiplicity //= math.factorial(count)
                probability = multiplicity * math.prod(p**count for p, count in zip(masses, counts))
                empirical = tuple(sum(count*loss for count, loss in zip(counts, row))/sample_size
                                  for row in losses)
                total_probability += probability
                if any(risk > empirical_risk+penalty+1e-14
                       for risk, empirical_risk, penalty in zip(risks, empirical, penalties)):
                    failure_probability += probability
                if any(empirical_risk == 0 and risk > (len(code)*math.log(2)+math.log(1/delta))/sample_size
                       for risk, empirical_risk, code in zip(risks, empirical, codes)):
                    zero_error_failure_probability += probability
    return {
        "sample_size": sample_size, "delta": delta,
        "kraft_sum": sum(2**(-len(code)) for code in codes),
        "total_sample_probability": total_probability,
        "simultaneous_failure_probability": failure_probability,
        "zero_training_error_failure_probability": zero_error_failure_probability,
    }


def data_dependent_decoder_counterexample(sample_size=64, delta=0.05):
    """Exhibit memorization and average over both labels at a fresh input.

    The continuous-input population risk follows from the text's measure argument;
    this finite calculation checks decoder behavior, not continuity by simulation.
    """
    if sample_size < 1 or not 0 < delta < 1:
        raise ValueError("Need a positive sample size and delta in (0,1)")
    training = tuple((i/(sample_size+1), i % 2) for i in range(1, sample_size+1))
    table = dict(training)

    def decode(code, x):
        if code != "0":
            raise ValueError("The decoder accepts only its one-bit code")
        return table.get(x, 0)

    empirical_error = sum(decode("0", x) != y for x, y in training)/sample_size
    fresh_input = 0.0  # In [0,1], outside this finite table; all such inputs predict 0.
    fresh_label_error = sum(decode("0", fresh_input) != y for y in (0, 1))/2
    return {
        "training_error": empirical_error,
        "error_averaged_over_fair_labels_at_a_fresh_input": fresh_label_error,
        "incorrect_one_bit_bound": math.sqrt((math.log(2)+math.log(1/delta))/(2*sample_size)),
        "incorrect_zero_training_error_bound": (math.log(2)+math.log(1/delta))/sample_size,
    }


def run_checks():
    tree = quadratic_noise_tree()
    assert abs(tree["total_probability"]-1) < 1e-12
    assert tree["minimum_conditional_step_slack"] >= -1e-12
    assert tree["expected_average_gradient_squared"] <= tree["theorem_upper_bound"]+1e-12
    bias = persistent_bias_counterexample()
    assert bias["actual_average_gradient_squared"] > bias["incorrect_unbiased_bound"]
    assert bias["actual_average_gradient_squared"] <= bias["correct_bias_budget"]+1e-12
    coding = prefix_code_failure_probability()
    assert abs(coding["total_sample_probability"]-1) < 1e-12
    assert coding["simultaneous_failure_probability"] <= coding["delta"]+1e-12
    assert coding["zero_training_error_failure_probability"] <= coding["delta"]+1e-12
    decoder = data_dependent_decoder_counterexample()
    assert decoder["training_error"] == 0
    assert decoder["incorrect_one_bit_bound"] < decoder["error_averaged_over_fair_labels_at_a_fresh_input"]
    return {"biased_quadratic_tree": tree, "persistent_bias": bias,
            "prefix_code": coding, "data_dependent_decoder": decoder}


if __name__ == "__main__":
    print(json.dumps(run_checks(), ensure_ascii=False, indent=2))
