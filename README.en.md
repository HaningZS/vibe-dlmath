<p align="center">
  <img src="assets/readme-hero.svg" alt="vibe-dlmath: intuition, explicit assumptions, reusable arguments, and evidence for deep learning theory" width="100%">
</p>

<p align="center">
  <strong>Make the intuition clear. Make the proof obligations explicit.</strong><br>
  Deep learning theory · Classical and recent proof methods · A constrained AI proof workflow
</p>

<p align="center">
  <a href="README.md">简体中文</a> · English<br>
  <a href="proofs/README.md">Proof library</a> ·
  <a href="docs/SKILL.md">Install the skill</a> ·
  <a href="docs/AI_PROOF_CONTRACT.md">AI proof contract</a> ·
  <a href="docs/PROOF_DISTILLATION.md">Proof distillation</a> ·
  <a href="docs/OPEN_SOURCE.md">Maintenance and releases</a>
</p>

---

**vibe-dlmath** is a library of mathematical prerequisites, reusable proof templates, and paper evidence for AI researchers. It also provides an installable agent skill for selecting, explaining, constructing, and reviewing proofs. The workflow connects intuition to explicit assumptions, justified steps, and clearly stated limits.

**8 topics · 47 template and tool cards · 56 prerequisite notes · 101 paper records.** The notes, catalog, and discovery tools work offline. Paper PDFs and TeX sources are optional downloads. The mathematical corpus is primarily in Chinese, with standard mathematical notation and Chinese/English search keywords; this README is an English entry point, not a claim that every linked document is translated.

## Motivation

**Understanding a paper's conclusion is not the same as being able to reuse its proof.** Changing the optimizer, sampling procedure, or error metric can invalidate an independence assumption, a smoothness condition, or the scope of a quantifier. We want to preserve not only what a paper proves, but why its key argument works and where it stops working.

AI makes derivations faster, but also makes fluent, unjustified proofs easier to produce. For example, a vanishing training gradient is an optimization statement; it does not by itself establish optimal test risk. Generalization and the approximation capacity of the function class still need arguments. A sequence of plausible formulas is not a closed logical chain.

This library connects learning with review: explain concepts through intuition and prerequisites, distill classical and recent arguments into templates with explicit conditions, then track each proof obligation against a derivation or a precisely located source. **Help researchers understand, adapt, and challenge an argument; require agents to expose its evidence, limits, and unresolved gaps.**

The goal is reusable, traceable, reviewable mathematical work—not one-click correct proofs. A template does not replace a theorem, and skill instructions are not formal verification. Important conclusions still need step-by-step review.

## Choose an entry point

| Your task | Start here |
|---|---|
| Rebuild mathematical foundations | [Learning roadmap](Math%20基础/AI%20Researcher%20数学学习路线.md) → [Proof prerequisites](Math%20基础/证明工具/AI%20理论证明前置学习路线.md) |
| Understand how a DL guarantee fits together | [Theory framework and coverage](docs/DL_THEORY_FRAMEWORK.md) → [An end-to-end learning proof](docs/END_TO_END_LEARNING_PROOF.md) |
| Find a reusable argument | [Proof library](proofs/README.md) → [Proof primitives](通用证明原语.md) → [Instantiation workflow](docs/PROOF_WORKFLOW.md) |
| Extract a method from a paper | [Proof distillation](docs/PROOF_DISTILLATION.md) → [October 2026 research review](docs/RECENT_RESEARCH_2026_10.md) → [Paper catalog](PAPERS.md) |
| Review an AI-generated proof | [AI proof contract](docs/AI_PROOF_CONTRACT.md) → [Claim ledger](templates/PROOF_LEDGER.json) → [Theory review](docs/THEORY_REVIEW.md) |
| Review release contents and later changes | [Initial release and release notes](CHANGELOG.md) |

## Start offline

First obtain the complete repository. If access is restricted, authenticate with a GitHub account that has permission to read it.

```bash
git clone https://github.com/HaningZS/vibe-dlmath.git
cd vibe-dlmath
python3 --version
```

Use **Python 3.11+** consistently. If your system `python3` is older, use an installed `python3.11` or newer interpreter for all commands. An optional isolated environment can be created with `python3 -m venv .venv` and activated with `source .venv/bin/activate`; no `pip install` is required.

Run the following commands from the repository root. No third-party Python packages are required.

```bash
python3 scripts/proof_templates.py search "Bayes risk"
python3 scripts/proof_templates.py show T32

# Optional: link the skill into your Codex skills directory.
python3 scripts/install_skill.py
```

Keep the repository at a stable location: the installer creates a symlink and refuses to replace unrelated existing content. See [skill setup](docs/SKILL.md) for custom paths and use with other tools that support `SKILL.md`.

An example request after installation:

```text
Use $vibe-dlmath to review this claim:
"The training gradient tends to zero, so test risk converges to Bayes risk."
Explain the intuition, then fix the objects, quantifiers, randomness,
and algorithm output. List every proof obligation and its evidence.
If the claim fails, give a counterexample and a valid conditional version.
```

To create an unfinished worksheet for your own problem:

```bash
python3 scripts/proof_templates.py scaffold T32 T33 \
  --problem "Connect empirical optimization error to population risk" \
  --out my-proof.md
```

The worksheet records obligations still to be resolved and refuses to overwrite an existing file. Search results are candidates; applicability depends on the actual mathematical objects and assumptions.

## Distill the proof, preserve its scope

The [distillation workflow](docs/PROOF_DISTILLATION.md) connects classical arguments to recent papers through five steps:

1. Fix the source version, theorem, assumptions, and proof location.
2. Identify the reusable mechanism, such as descent, coupling, a potential function, or a change of measure.
3. State what survives a change in model, optimizer, sampling, or error metric, and what needs a new proof.
4. Record each claim, its dependencies, its evidence, and its unresolved obligations.
5. Check quantifiers, probability, constants, resources, counterexamples, and the actual algorithm output.

Start with worked routes for [descent with bias and variance](extensions/经典下降证明的偏差与方差接口.md) or [coding bounds with data-dependent decoders](extensions/经典编码界与数据依赖解码器.md). Continue with [data-dependent certificates (T50)](proofs/generalization/T50-data-dependent-certificate-envelope.md) or [Flow Matching velocity-to-trajectory error (T51)](proofs/generation-transport/T51-flow-trajectory-error.md).

For a complete worked argument, see the [end-to-end learning proof](docs/END_TO_END_LEARNING_PROOF.md). Use the [theorem dossier](templates/THEOREM_DOSSIER.md) when developing a new result.

## Constraints for AI-assisted proofs

The [AI proof contract](docs/AI_PROOF_CONTRACT.md) requires explicit proof obligations and forbids silently adding assumptions, changing quantifiers, or inventing references. An experiment, numerical check, or search match cannot stand in for a mathematical derivation. When a step remains open, the output should identify the missing assumption, unproved lemma, counterexample, or conditional conclusion.

```bash
# Check a completed example ledger for structural consistency.
python3 scripts/audit_proof.py examples/biased_sgd_ledger.json

# The blank template intentionally reports unresolved fields.
python3 scripts/audit_proof.py templates/PROOF_LEDGER.json
```

The audit tool checks structure and internal consistency. **It does not establish mathematical correctness.** Each derivation and cited result still needs review; a passing script does not upgrade a paper's verification status.

## Theory map

| Topic | Typical arguments |
|---|---|
| [Optimization and stochastic estimation](proofs/optimization/README.md) | Descent, potentials, variance reduction, heavy tails, nonsmooth problems, second-order stationarity, client drift |
| [Generalization and information theory](proofs/generalization/README.md) | Excess risk, uniform convergence, stability, PAC-Bayes, margins, compression, robustness |
| [Neural networks and representations](proofs/deep-learning/README.md) | Approximation, NTK, feature dynamics, implicit bias, contrastive learning, equivariance |
| [Generation and transport](proofs/generation-transport/README.md) | Learning error, continuous processes, sampling discretization, distribution metrics |
| [Sequential decisions](proofs/sequential-decision/README.md) | Bandits, Bellman error, mirror descent, regret |
| [Statistics and coverage](proofs/statistics/README.md) | Doubly robust estimation, conformal prediction, privacy accounting, causal identification |
| [Lower bounds and expressivity](proofs/lower-bounds-expressivity/README.md) | Hard instances, constructive simulation, expressivity limits, GNNs and 1-WL |
| [Evaluation and monitoring](proofs/evaluation-monitoring/README.md) | Calibration, proper scoring, Bayesian filtering, adaptedness and stopping times |

The 47 cards comprise 43 proof templates, 2 problem-specific method cards, 1 empirical algebra tool, and 1 routing page. See the [coverage matrix](docs/DL_THEORY_FRAMEWORK.md) for the scope and remaining gaps, and [TOPICS](TOPICS.md) for reading order.

## Download papers when needed

```bash
# Preview records without network access or file changes.
python3 scripts/download_papers.py --dry-run

# Choose a topic or a specific arXiv record.
python3 scripts/download_papers.py --topic generative
python3 scripts/download_papers.py --ids 2105.04026

# Rebuild the local inventory offline.
python3 scripts/download_papers.py --reindex
```

Without filters, the downloader processes the entire catalog. Use `--no-sources` for PDFs only. It supports macOS/Linux and skips cached files that pass format and SHA-256 checks. See [download documentation](docs/DOWNLOADING.md) for details.

Git tracks notes, metadata, manifests, review cards, and scripts. PDFs, source archives, and extracted files are rebuildable local caches excluded from Git. Paper cards link to official online sources; local PDF/TeX links work after downloading. The catalog count is not a count of fully verified papers. The tracked [inventory](reports/inventory.json) is a snapshot from the machine that generated it, not evidence that a fresh clone contains the cache. Run `python3 scripts/check_library.py` for local availability, or use `--reindex` above to refresh your local report.

## Maintain and contribute

Canonical cards live in `proofs/`; the registry generates topic indexes and paper backlinks. `Math 基础/` contains prerequisites, `templates/` and `examples/` support proof work, and `skills/vibe-dlmath/` contains the agent instructions. Knowledge updates keep the relevant indexes, sources, and verification status current. The [release notes](CHANGELOG.md) describe additions, corrections, and limitations that affect users.

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_library.py
```

These checks cover tool behavior, links, and record consistency. Mathematical verification scope is documented separately in the [template status](证明模板核验状态.md) and [paper review index](proof_ref/核验导航.md). A CI configuration is provided as an [example](docs/check-workflow.example.yml); consult the actual repository configuration for whether it is enabled.

Read [CONTRIBUTING](CONTRIBUTING.md) for the maintenance workflow, and [PROVENANCE](docs/PROVENANCE.md) for content origins, verification scope, and access to optional external notes. The templates, prerequisites, source records, and tools needed for the core proof workflow are included in this library.

**License:** original code and documentation in this library are licensed under the [MIT License](LICENSE). Third-party papers, sources, and quoted material retain their own licenses; see [third-party notices](THIRD_PARTY_NOTICES.md). Maintainers should follow the [release checklist](docs/OPEN_SOURCE.md) before publishing a release.
