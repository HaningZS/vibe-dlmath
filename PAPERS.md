# 论文总目录

此表由 `scripts/download_papers.py --reindex` 生成。

PDF/source 为本表生成时的缓存快照；新 clone 需运行下载命令并 reindex。核验等级不会因下载自动提升。

[返回首页](README.md) · [主题阅读顺序](TOPICS.md) · [下载说明](docs/DOWNLOADING.md)

## approximation

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [Error bounds for approximations with deep ReLU networks](proof_ref/dl-core-2026-09/error-bounds-for-approximations-with-deep-relu-networks-1610.01145/README.md) · [arXiv](https://arxiv.org/abs/1610.01145v3) | [T34](proofs/deep-learning/T34-neural-approximation.md) | ✓/✓ | intake |
| [The Barron Space and the Flow-induced Function Spaces for Neural Network Models](proof_ref/dl-specializations-2026-10/the-barron-space-and-the-flow-induced-function-1906.08039/README.md) · [arXiv](https://arxiv.org/abs/1906.08039v2) | [T41](proofs/deep-learning/T41-barron-random-feature-approximation.md), [T34](proofs/deep-learning/T34-neural-approximation.md) | ✓/✓ | intake |

## architecture

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [Group Equivariant Convolutional Networks](proof_ref/dl-specializations-2026-10/group-equivariant-convolutional-networks-1602.07576/README.md) · [arXiv](https://arxiv.org/abs/1602.07576v3) | [T43](proofs/deep-learning/T43-equivariance-symmetry.md) | ✓/✓ | intake |
| [How Powerful are Graph Neural Networks?](proof_ref/dl-specializations-2026-10/how-powerful-are-graph-neural-networks-1810.00826/README.md) · [arXiv](https://arxiv.org/abs/1810.00826v3) | [T44](proofs/lower-bounds-expressivity/T44-message-passing-wl.md), [T20B](proofs/lower-bounds-expressivity/T20B-expressivity-lower-bound.md) | ✓/✓ | core-claim-checked |

## concentration

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [Introduction to the non-asymptotic analysis of random matrices](proof_ref/foundations-2026-09/introduction-to-the-non-asymptotic-analysis-of-random-1011.3027/README.md) · [arXiv](https://arxiv.org/abs/1011.3027v7) | [T06](proofs/sequential-decision/T06-linear-bandit.md), [T16](proofs/optimization/T16-heavy-tail-clipping.md) | ✓/✓ | intake |
| [User-friendly tail bounds for sums of random matrices](proof_ref/foundations-2026-09/user-friendly-tail-bounds-for-sums-of-random-1004.4389/README.md) · [arXiv](https://arxiv.org/abs/1004.4389v7) | [T09](proofs/deep-learning/T09-ntk.md) | ✓/✓ | intake |
| [An Introduction to Matrix Concentration Inequalities](proof_ref/foundations-2026-09/an-introduction-to-matrix-concentration-inequalities-1501.01571/README.md) · [arXiv](https://arxiv.org/abs/1501.01571v1) | [T09](proofs/deep-learning/T09-ntk.md) | ✓/✓ | intake |
| [Time-uniform Chernoff bounds via nonnegative supermartingales](proof_ref/foundations-2026-09/time-uniform-chernoff-bounds-via-nonnegative-supermartingales-1808.03204/README.md) · [arXiv](https://arxiv.org/abs/1808.03204v8) | [T06](proofs/sequential-decision/T06-linear-bandit.md), [T23](proofs/evaluation-monitoring/T23-prefix-safety.md) | ✓/✓ | intake |
| [Time-uniform, nonparametric, nonasymptotic confidence sequences](proof_ref/foundations-2026-09/time-uniform-nonparametric-nonasymptotic-confidence-sequences-1810.08240/README.md) · [arXiv](https://arxiv.org/abs/1810.08240v9) | [T18](proofs/statistics/T18-split-conformal.md), [T23](proofs/evaluation-monitoring/T23-prefix-safety.md) | ✓/✓ | intake |
| [Time-Uniform Self-Normalized Concentration for Vector-Valued Processes](proof_ref/recent-accepted-2025-2026/time-uniform-self-normalized-concentration-for-vector-valued-2310.09100/README.md) · [arXiv](https://arxiv.org/abs/2310.09100v2) | [T06](proofs/sequential-decision/T06-linear-bandit.md) | ✓/✓ | imported-claim-checked-long-version |

## distributed-optimization

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [Local SGD Converges Fast and Communicates Little](proof_ref/dl-specializations-2026-10/local-sgd-converges-fast-and-communicates-little-1805.09767/README.md) · [arXiv](https://arxiv.org/abs/1805.09767v3) | [T47](proofs/optimization/T47-local-training-client-drift.md), [T02](proofs/optimization/T02-lyapunov.md) | ✓/✓ | intake |
| [SCAFFOLD: Stochastic Controlled Averaging for Federated Learning](proof_ref/dl-specializations-2026-10/scaffold-stochastic-controlled-averaging-for-federated-learning-1910.06378/README.md) · [arXiv](https://arxiv.org/abs/1910.06378v4) | [T47](proofs/optimization/T47-local-training-client-drift.md), [T03](proofs/optimization/T03-variance-reduction.md) | ✓/✓ | intake |

## dl-foundations

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [The Modern Mathematics of Deep Learning](proof_ref/dl-core-2026-09/the-modern-mathematics-of-deep-learning-2105.04026/README.md) · [arXiv](https://arxiv.org/abs/2105.04026v2) | [T32](proofs/generalization/T32-excess-risk-decomposition.md), [T33](proofs/generalization/T33-uniform-convergence.md), [T34](proofs/deep-learning/T34-neural-approximation.md), [T35](proofs/generalization/T35-margin-norm.md), [T36](proofs/deep-learning/T36-implicit-bias.md), [T39](proofs/optimization/T39-proximal-nonsmooth.md) | ✓/✓ | intake |

## generalization

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [Spectrally-normalized margin bounds for neural networks](proof_ref/dl-core-2026-09/spectrally-normalized-margin-bounds-for-neural-networks-1706.08498/README.md) · [arXiv](https://arxiv.org/abs/1706.08498v2) | [T33](proofs/generalization/T33-uniform-convergence.md), [T35](proofs/generalization/T35-margin-norm.md) | ✓/✓ | intake |
| [Stronger generalization bounds for deep nets via a compression approach](proof_ref/dl-core-2026-09/stronger-generalization-bounds-for-deep-nets-via-a-1802.05296/README.md) · [arXiv](https://arxiv.org/abs/1802.05296v4) | [T38](proofs/generalization/T38-compression.md) | ✓/✓ | intake |
| [User-friendly introduction to PAC-Bayes bounds](proof_ref/foundations-2026-09/user-friendly-introduction-to-pac-bayes-bounds-2110.11216/README.md) · [arXiv](https://arxiv.org/abs/2110.11216v6) | [T05](proofs/generalization/T05-pac-bayes-information.md) | ✓/✓ | scoped-source-checked |
| [Information-theoretic analysis of generalization capability of learning algorithms](proof_ref/foundations-2026-09/information-theoretic-analysis-of-generalization-capability-of-learning-1705.07809/README.md) · [arXiv](https://arxiv.org/abs/1705.07809v2) | [T05](proofs/generalization/T05-pac-bayes-information.md) | ✓/✓ | scoped-source-checked |
| [Understanding deep learning requires rethinking generalization](proof_ref/foundations-2026-09/understanding-deep-learning-requires-rethinking-generalization-1611.03530/README.md) · [arXiv](https://arxiv.org/abs/1611.03530v2) | [T04](proofs/generalization/T04-stability.md), [T05](proofs/generalization/T05-pac-bayes-information.md) | ✓/✓ | intake |
| [Reconciling modern machine learning practice and the bias-variance trade-off](proof_ref/foundations-2026-09/reconciling-modern-machine-learning-practice-and-the-classical-1812.11118/README.md) · [arXiv](https://arxiv.org/abs/1812.11118v2) | [T04](proofs/generalization/T04-stability.md), [T09](proofs/deep-learning/T09-ntk.md) | ✓/✓ | intake |
| [Surprises in High-Dimensional Ridgeless Least Squares Interpolation](proof_ref/foundations-2026-09/surprises-in-high-dimensional-ridgeless-least-squares-interpolation-1903.08560/README.md) · [arXiv](https://arxiv.org/abs/1903.08560v5) | [T09](proofs/deep-learning/T09-ntk.md) | ✓/✓ | intake |
| [Train faster, generalize better: Stability of stochastic gradient descent](proof_ref/core-theory-2026-09/train-faster-generalize-better-stability-of-stochastic-gradient-1509.01240/README.md) · [arXiv](https://arxiv.org/abs/1509.01240v2) |  | ✓/✓ | imported-binary-validated |
| [Which Algorithms Have Tight Generalization Bounds?](proof_ref/core-theory-2026-09/which-algorithms-have-tight-generalization-bounds-2410.01969/README.md) · [arXiv](https://arxiv.org/abs/2410.01969v1) | [T05](proofs/generalization/T05-pac-bayes-information.md) | ✓/✓ | imported-claim-checked-arxiv |
| [Generalization Bounds via Meta-Learned Model Representations: PAC-Bayes and Sample Compression Hypernetworks](proof_ref/recent-accepted-2025-2026/generalization-bounds-via-meta-learned-model-representations-pac-2410.13577/README.md) · [arXiv](https://arxiv.org/abs/2410.13577v3) | [T05](proofs/generalization/T05-pac-bayes-information.md) | ✓/✓ | imported-claim-checked-arxiv |
| [Improved Generalization Bounds for Transductive Learning by Transductive Local Complexity and Its Applications](proof_ref/recent-accepted-2025-2026/improved-generalization-bounds-for-transductive-learning-by-transductive-2309.16858/README.md) · [arXiv](https://arxiv.org/abs/2309.16858v5) |  | ✓/✓ | imported-binary-validated |
| [Optimal Rates for Generalization of Gradient Descent for Deep ReLU Classification](proof_ref/recent-accepted-2025-2026/optimal-rates-for-generalization-of-gradient-descent-for-2510.02779/README.md) · [arXiv](https://arxiv.org/abs/2510.02779v4) |  | ✓/✓ | imported-binary-validated |
| [Certification-Enhanced Generalization Bounds](proof_ref/proof-distillation-2026-10/certification-enhanced-generalization-bounds-2610.06238/README.md) · [arXiv](https://arxiv.org/abs/2610.06238v1) | [T04](proofs/generalization/T04-stability.md), [T50](proofs/generalization/T50-data-dependent-certificate-envelope.md) | ✓/✓ | scoped-claim-checked |

## generative

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [Score-Based Generative Modeling through Stochastic Differential Equations](proof_ref/foundations-2026-09/score-based-generative-modeling-through-stochastic-differential-equations-2011.13456/README.md) · [arXiv](https://arxiv.org/abs/2011.13456v2) | [T13](proofs/generation-transport/T13-sampler-error.md) | ✓/✓ | intake |
| [Sampling is as easy as learning the score: theory for diffusion models with minimal data assumptions](proof_ref/foundations-2026-09/sampling-is-as-easy-as-learning-the-score-2209.11215/README.md) · [arXiv](https://arxiv.org/abs/2209.11215v3) | [T13](proofs/generation-transport/T13-sampler-error.md) | ✓/✓ | intake |
| [Flow Matching for Generative Modeling](proof_ref/foundations-2026-09/flow-matching-for-generative-modeling-2210.02747/README.md) · [arXiv](https://arxiv.org/abs/2210.02747v2) | [T13](proofs/generation-transport/T13-sampler-error.md), [T19](proofs/generation-transport/T19-transport-risk.md) | ✓/✓ | intake |
| [Flow Straight and Fast: Learning to Generate and Transfer Data with Rectified Flow](proof_ref/foundations-2026-09/flow-straight-and-fast-learning-to-generate-and-2209.03003/README.md) · [arXiv](https://arxiv.org/abs/2209.03003v1) | [T13](proofs/generation-transport/T13-sampler-error.md), [T19](proofs/generation-transport/T19-transport-risk.md) | ✓/✓ | intake |
| [Consistency Models](proof_ref/foundations-2026-09/consistency-models-2303.01469/README.md) · [arXiv](https://arxiv.org/abs/2303.01469v2) | [T13](proofs/generation-transport/T13-sampler-error.md) | ✓/✓ | intake |
| [Blink of an eye: a simple theory for feature localization in generative models](proof_ref/core-theory-2026-09/blink-of-an-eye-a-simple-theory-for-2502.00921/README.md) · [arXiv](https://arxiv.org/abs/2502.00921v2) | [T25](proofs/generation-transport/T25-feature-localization-card.md) | ✓/✓ | imported-method-card-only |
| [$f$-Trajectory Balance: A Loss Family for Tuning GFlowNets, Generative Models, and LLMs with Off- and On-Policy Data](proof_ref/core-theory-2026-09/f-trajectory-balance-a-loss-family-for-tuning-2605.15417/README.md) · [arXiv](https://arxiv.org/abs/2605.15417v1) |  | ✓/✓ | imported-binary-validated |
| [O(d/T) Convergence Theory for Diffusion Probabilistic Models under Minimal Assumptions](proof_ref/core-theory-2026-09/o-d-t-convergence-theory-for-diffusion-probabilistic-2409.18959/README.md) · [arXiv](https://arxiv.org/abs/2409.18959v2) | [T13](proofs/generation-transport/T13-sampler-error.md) | ✓/✓ | imported-claim-checked-arxiv |
| [Provable Statistical Rates for Consistency Diffusion Models](proof_ref/core-theory-2026-09/provable-statistical-rates-for-consistency-diffusion-models-2406.16213/README.md) · [arXiv](https://arxiv.org/abs/2406.16213v1) | [T13](proofs/generation-transport/T13-sampler-error.md) | ✓/✓ | imported-binary-validated |
| [Train for the Worst, Plan for the Best: Understanding Token Ordering in Masked Diffusions](proof_ref/core-theory-2026-09/train-for-the-worst-plan-for-the-best-2502.06768/README.md) · [arXiv](https://arxiv.org/abs/2502.06768v3) | [T20](proofs/lower-bounds-expressivity/T20-expressivity-router.md) | ✓/✓ | imported-binary-validated |
| [A Random Matrix Theory Perspective on the Consistency of Diffusion Models](proof_ref/recent-accepted-2025-2026/a-random-matrix-theory-perspective-on-the-consistency-2602.02908/README.md) · [arXiv](https://arxiv.org/abs/2602.02908v2) |  | ✓/✓ | imported-binary-validated |
| [Approximation and Generalization Abilities of Score-based Neural Network Generative Models for Sub-Gaussian Distributions](proof_ref/recent-accepted-2025-2026/approximation-and-generalization-abilities-of-score-based-neural-2505.10880/README.md) · [arXiv](https://arxiv.org/abs/2505.10880v2) |  | ✓/✓ | imported-binary-validated |
| [High-accuracy sampling for diffusion models and log-concave distributions](proof_ref/recent-accepted-2025-2026/high-accuracy-sampling-for-diffusion-models-and-log-2602.01338/README.md) · [arXiv](https://arxiv.org/abs/2602.01338v2) |  | ✓/✓ | imported-binary-validated |
| [Improving Flow Matching by Aligning Flow Divergence](proof_ref/recent-accepted-2025-2026/improving-flow-matching-by-aligning-flow-divergence-2602.00869/README.md) · [arXiv](https://arxiv.org/abs/2602.00869v1) | [T13](proofs/generation-transport/T13-sampler-error.md) | ✓/✓ | imported-claim-checked-arxiv |
| [Flow Matching under Noisy Latent Structure: Beyond Exact Low-Dimensional Support](proof_ref/proof-distillation-2026-10/flow-matching-under-noisy-latent-structure-beyond-exact-2609.38918/README.md) · [arXiv](https://arxiv.org/abs/2609.38918v1) | [T13](proofs/generation-transport/T13-sampler-error.md), [T51](proofs/generation-transport/T51-flow-trajectory-error.md) | ✓/✓ | scoped-claim-checked |
| [Sharp Convergence and Sampling Trade-offs for Riemannian Diffusion under Nonnegative Ricci Curvature](proof_ref/proof-distillation-2026-10/sharp-convergence-and-sampling-trade-offs-for-riemannian-2609.36568/README.md) · [arXiv](https://arxiv.org/abs/2609.36568v1) | [T13](proofs/generation-transport/T13-sampler-error.md) | ✓/✓ | source-issues-recorded |

## lower-bounds

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [An Introductory Guide to Fano's Inequality with Applications in Statistical Estimation](proof_ref/foundations-2026-09/an-introductory-guide-to-fano-s-inequality-with-1901.00555/README.md) · [arXiv](https://arxiv.org/abs/1901.00555v3) | [T12](proofs/lower-bounds-expressivity/T12-information-lower-bounds.md) | ✓/✓ | intake |
| [Lower Bounds for Non-Convex Stochastic Optimization](proof_ref/foundations-2026-09/lower-bounds-for-non-convex-stochastic-optimization-1912.02365/README.md) · [arXiv](https://arxiv.org/abs/1912.02365v2) | [T12](proofs/lower-bounds-expressivity/T12-information-lower-bounds.md) | ✓/✓ | intake |
| [Assouad, Fano, and Le Cam with Interaction: A Unifying Lower Bound Framework and Characterization for Bandit Learnability](proof_ref/core-theory-2026-09/assouad-fano-and-le-cam-with-interaction-a-2410.05117/README.md) · [arXiv](https://arxiv.org/abs/2410.05117v2) | [T12](proofs/lower-bounds-expressivity/T12-information-lower-bounds.md) | ✓/✓ | imported-claim-checked-arxiv |
| [New Lower Bounds for Stochastic Non-Convex Optimization through Divergence Decomposition](proof_ref/recent-accepted-2025-2026/new-lower-bounds-for-stochastic-non-convex-optimization-2502.14060/README.md) · [arXiv](https://arxiv.org/abs/2502.14060v2) | [T12](proofs/lower-bounds-expressivity/T12-information-lower-bounds.md) | ✓/✓ | imported-claim-checked-arxiv |

## neural-dynamics

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [Neural Tangent Kernel: Convergence and Generalization in Neural Networks](proof_ref/foundations-2026-09/neural-tangent-kernel-convergence-and-generalization-in-neural-1806.07572/README.md) · [arXiv](https://arxiv.org/abs/1806.07572v4) | [T09](proofs/deep-learning/T09-ntk.md) | ✓/✓ | intake |
| [Wide Neural Networks of Any Depth Evolve as Linear Models Under Gradient Descent](proof_ref/foundations-2026-09/wide-neural-networks-of-any-depth-evolve-as-1902.06720/README.md) · [arXiv](https://arxiv.org/abs/1902.06720v4) | [T09](proofs/deep-learning/T09-ntk.md) | ✓/✓ | intake |
| [On Lazy Training in Differentiable Programming](proof_ref/foundations-2026-09/on-lazy-training-in-differentiable-programming-1812.07956/README.md) · [arXiv](https://arxiv.org/abs/1812.07956v5) | [T09](proofs/deep-learning/T09-ntk.md), [T10](proofs/deep-learning/T10-mean-field.md) | ✓/✓ | intake |
| [A Mean Field View of the Landscape of Two-Layers Neural Networks](proof_ref/foundations-2026-09/a-mean-field-view-of-the-landscape-of-1804.06561/README.md) · [arXiv](https://arxiv.org/abs/1804.06561v2) | [T10](proofs/deep-learning/T10-mean-field.md) | ✓/✓ | intake |
| [The Implicit Bias of Gradient Descent on Separable Data](proof_ref/foundations-2026-09/the-implicit-bias-of-gradient-descent-on-separable-1710.10345/README.md) · [arXiv](https://arxiv.org/abs/1710.10345v7) | [T01](proofs/optimization/T01-descent.md), [T09](proofs/deep-learning/T09-ntk.md), [T36](proofs/deep-learning/T36-implicit-bias.md) | ✓/✓ | statement-and-interface-checked |
| [The Stability of Singular Distribution: A Spectral Perspective on the Two-Phase Dynamics of Language Model Pre-training](proof_ref/core-theory-2026-09/the-stability-of-singular-distribution-a-spectral-perspective-2605.26489/README.md) · [arXiv](https://arxiv.org/abs/2605.26489v1) |  | ✓/✓ | imported-binary-validated |
| [Sequences of Logits Reveal the Low Rank Structure of Language Models](proof_ref/recent-accepted-2025-2026/sequences-of-logits-reveal-the-low-rank-structure-2510.24966/README.md) · [arXiv](https://arxiv.org/abs/2510.24966v1) | [T14](proofs/deep-learning/T14-algorithm-simulation.md) | ✓/✓ | imported-claim-checked-arxiv |
| [To Grok Grokking: Provable Grokking in Ridge Regression](proof_ref/recent-accepted-2025-2026/to-grok-grokking-provable-grokking-in-ridge-regression-2601.19791/README.md) · [arXiv](https://arxiv.org/abs/2601.19791v4) |  | ✓/✓ | imported-binary-validated |

## optimization

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [How to Escape Saddle Points Efficiently](proof_ref/dl-specializations-2026-10/how-to-escape-saddle-points-efficiently-1703.00887/README.md) · [arXiv](https://arxiv.org/abs/1703.00887v1) | [T40](proofs/optimization/T40-second-order-stationarity.md) | ✓/✓ | intake |
| [Convex Optimization: Algorithms and Complexity](proof_ref/foundations-2026-09/convex-optimization-algorithms-and-complexity-1405.4980/README.md) · [arXiv](https://arxiv.org/abs/1405.4980v2) | [T01](proofs/optimization/T01-descent.md), [T02](proofs/optimization/T02-lyapunov.md), [T08](proofs/sequential-decision/T08-mirror-descent.md) | ✓/✓ | intake |
| [Optimization Methods for Large-Scale Machine Learning](proof_ref/foundations-2026-09/optimization-methods-for-large-scale-machine-learning-1606.04838/README.md) · [arXiv](https://arxiv.org/abs/1606.04838v3) | [T01](proofs/optimization/T01-descent.md), [T02](proofs/optimization/T02-lyapunov.md), [T03](proofs/optimization/T03-variance-reduction.md) | ✓/✓ | intake |
| [Linear Convergence of Gradient and Proximal-Gradient Methods Under the Polyak-\L{}ojasiewicz Condition](proof_ref/foundations-2026-09/linear-convergence-of-gradient-and-proximal-gradient-methods-1608.04636/README.md) · [arXiv](https://arxiv.org/abs/1608.04636v4) | [T01](proofs/optimization/T01-descent.md) | ✓/✓ | intake |
| [SPIDER: Near-Optimal Non-Convex Optimization via Stochastic Path Integrated Differential Estimator](proof_ref/foundations-2026-09/spider-near-optimal-non-convex-optimization-via-stochastic-1807.01695/README.md) · [arXiv](https://arxiv.org/abs/1807.01695v2) | [T03](proofs/optimization/T03-variance-reduction.md) | ✓/✓ | intake |
| [A Stochastic Gradient Method with an Exponential Convergence Rate for Finite Training Sets](proof_ref/foundations-2026-09/a-stochastic-gradient-method-with-an-exponential-convergence-1202.6258/README.md) · [arXiv](https://arxiv.org/abs/1202.6258v4) | [T02](proofs/optimization/T02-lyapunov.md), [T03](proofs/optimization/T03-variance-reduction.md) | ✓/✓ | intake |
| [A Tight Theory of Error Feedback Algorithms in Distributed Optimization](proof_ref/core-theory-2026-09/a-tight-theory-of-error-feedback-algorithms-in-2605.31594/README.md) · [arXiv](https://arxiv.org/abs/2605.31594v1) |  | ✓/✓ | imported-binary-validated |
| [Clipping Improves Adam-Norm and AdaGrad-Norm when the Noise Is Heavy-Tailed](proof_ref/core-theory-2026-09/clipping-improves-adam-norm-and-adagrad-norm-when-2406.04443/README.md) · [arXiv](https://arxiv.org/abs/2406.04443v3) | [T16](proofs/optimization/T16-heavy-tail-clipping.md) | ✓/✓ | imported-claim-checked-arxiv |
| [Generalized-Smooth Nonconvex Optimization is As Efficient As Smooth Nonconvex Optimization](proof_ref/core-theory-2026-09/generalized-smooth-nonconvex-optimization-is-as-efficient-as-2303.02854/README.md) · [arXiv](https://arxiv.org/abs/2303.02854v2) | [T15](proofs/optimization/T15-generalized-smoothness.md) | ✓/✓ | imported-claim-checked-arxiv |
| [The Hidden Cost of Approximation in Online Mirror Descent](proof_ref/core-theory-2026-09/the-hidden-cost-of-approximation-in-online-mirror-2511.22283/README.md) · [arXiv](https://arxiv.org/abs/2511.22283v2) | [T08](proofs/sequential-decision/T08-mirror-descent.md) | ✓/✓ | imported-binary-validated |
| [Structured Preconditioners in Adaptive Optimization: A Unified Analysis](proof_ref/recent-accepted-2025-2026/structured-preconditioners-in-adaptive-optimization-a-unified-analysis-2503.10537/README.md) · [arXiv](https://arxiv.org/abs/2503.10537v2) |  | ✓/✓ | imported-claim-checked-arxiv |

## post-training

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](proof_ref/core-theory-2026-09/direct-preference-optimization-your-language-model-is-secretly-2305.18290/README.md) · [arXiv](https://arxiv.org/abs/2305.18290v3) | [T08](proofs/sequential-decision/T08-mirror-descent.md) | ✓/✓ | imported-claim-checked-arxiv |
| [$f$-Divergence Regularized RLHF: Two Tales of Sampling and Unified Analyses](proof_ref/core-theory-2026-09/f-divergence-regularized-rlhf-two-tales-of-sampling-2605.06977/README.md) · [arXiv](https://arxiv.org/abs/2605.06977v1) |  | ✓/✓ | imported-binary-validated |
| [Iterative Preference Learning from Human Feedback: Bridging Theory and Practice for RLHF under KL-Constraint](proof_ref/core-theory-2026-09/iterative-preference-learning-from-human-feedback-bridging-theory-2312.11456/README.md) · [arXiv](https://arxiv.org/abs/2312.11456v4) | [T08](proofs/sequential-decision/T08-mirror-descent.md) | ✓/✓ | imported-binary-validated |

## privacy

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [Renyi Differential Privacy](proof_ref/dl-specializations-2026-10/renyi-differential-privacy-1702.07476/README.md) · [arXiv](https://arxiv.org/abs/1702.07476v3) | [T46](proofs/statistics/T46-gaussian-privacy-accounting.md) | ✓/✓ | core-claim-checked |
| [Deep Learning with Differential Privacy](proof_ref/dl-specializations-2026-10/deep-learning-with-differential-privacy-1607.00133/README.md) · [arXiv](https://arxiv.org/abs/1607.00133v2) | [T46](proofs/statistics/T46-gaussian-privacy-accounting.md), [T16](proofs/optimization/T16-heavy-tail-clipping.md) | ✓/✓ | intake |

## representation

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [Representation Learning with Contrastive Predictive Coding](proof_ref/dl-core-2026-09/representation-learning-with-contrastive-predictive-coding-1807.03748/README.md) · [arXiv](https://arxiv.org/abs/1807.03748v2) | [T37](proofs/deep-learning/T37-contrastive-transfer.md) | ✓/✓ | intake |
| [A Theoretical Analysis of Contrastive Unsupervised Representation Learning](proof_ref/foundations-2026-09/a-theoretical-analysis-of-contrastive-unsupervised-representation-learning-1902.09229/README.md) · [arXiv](https://arxiv.org/abs/1902.09229v1) | [T05](proofs/generalization/T05-pac-bayes-information.md) | ✓/✓ | intake |
| [Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere](proof_ref/foundations-2026-09/understanding-contrastive-representation-learning-through-alignment-and-uniformi-2005.10242/README.md) · [arXiv](https://arxiv.org/abs/2005.10242v10) | [T05](proofs/generalization/T05-pac-bayes-information.md), [T19](proofs/generation-transport/T19-transport-risk.md) | ✓/✓ | intake |
| [A Theory of Contrastive Learning with Natural Images](proof_ref/core-theory-2026-09/a-theory-of-contrastive-learning-with-natural-images-2607.07470/README.md) · [arXiv](https://arxiv.org/abs/2607.07470v1) |  | ✓/✓ | imported-binary-validated |
| [A Theory of How Pretraining Shapes Inductive Bias in Fine-Tuning](proof_ref/core-theory-2026-09/a-theory-of-how-pretraining-shapes-inductive-bias-2602.20062/README.md) · [arXiv](https://arxiv.org/abs/2602.20062v2) |  | ✓/✓ | imported-binary-validated |
| [Graph Representational Learning: When Does More Expressivity Hurt Generalization?](proof_ref/recent-accepted-2025-2026/graph-representational-learning-when-does-more-expressivity-hurt-2505.11298/README.md) · [arXiv](https://arxiv.org/abs/2505.11298v1) |  | ✓/✓ | imported-binary-validated |

## rl-bandits

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [Online Least Squares Estimation with Self-Normalized Processes: An Application to Bandit Problems](proof_ref/foundations-2026-09/online-least-squares-estimation-with-self-normalized-processes-1102.2670/README.md) · [arXiv](https://arxiv.org/abs/1102.2670v1) | [T06](proofs/sequential-decision/T06-linear-bandit.md) | ✓/✓ | intake |
| [Regret Analysis of Stochastic and Nonstochastic Multi-armed Bandit Problems](proof_ref/foundations-2026-09/regret-analysis-of-stochastic-and-nonstochastic-multi-armed-1204.5721/README.md) · [arXiv](https://arxiv.org/abs/1204.5721v2) | [T06](proofs/sequential-decision/T06-linear-bandit.md), [T08](proofs/sequential-decision/T08-mirror-descent.md), [T12](proofs/lower-bounds-expressivity/T12-information-lower-bounds.md) | ✓/✓ | intake |
| [Is Pessimism Provably Efficient for Offline RL?](proof_ref/foundations-2026-09/is-pessimism-provably-efficient-for-offline-rl-2012.15085/README.md) · [arXiv](https://arxiv.org/abs/2012.15085v3) | [T07](proofs/sequential-decision/T07-bellman.md) | ✓/✓ | intake |
| [Trust Region Policy Optimization](proof_ref/foundations-2026-09/trust-region-policy-optimization-1502.05477/README.md) · [arXiv](https://arxiv.org/abs/1502.05477v5) | [T07](proofs/sequential-decision/T07-bellman.md), [T08](proofs/sequential-decision/T08-mirror-descent.md) | ✓/✓ | intake |
| [Provably Efficient Reinforcement Learning with Linear Function Approximation](proof_ref/core-theory-2026-09/provably-efficient-reinforcement-learning-with-linear-function-approximation-1907.05388/README.md) · [arXiv](https://arxiv.org/abs/1907.05388v2) | [T07](proofs/sequential-decision/T07-bellman.md) | ✓/✓ | imported-claim-checked-arxiv |
| [The Surprising Difficulty of Search in Model-Based Reinforcement Learning](proof_ref/core-theory-2026-09/the-surprising-difficulty-of-search-in-model-based-2601.21306/README.md) · [arXiv](https://arxiv.org/abs/2601.21306v2) |  | ✓/✓ | imported-binary-validated |
| [Capacity-Constrained Online Learning with Delays: Scheduling Frameworks and Regret Trade-offs](proof_ref/recent-accepted-2025-2026/capacity-constrained-online-learning-with-delays-scheduling-frameworks-2503.19856/README.md) · [arXiv](https://arxiv.org/abs/2503.19856v2) |  | ✓/✓ | imported-binary-validated |
| [Reinforcement Learning for Infinite-Horizon Average-Reward Linear MDPs via Approximation by Discounted-Reward MDPs](proof_ref/recent-accepted-2025-2026/reinforcement-learning-for-infinite-horizon-average-reward-linear-2405.15050/README.md) · [arXiv](https://arxiv.org/abs/2405.15050v3) | [T06](proofs/sequential-decision/T06-linear-bandit.md) | ✓/✓ | imported-claim-checked-arxiv |

## robustness

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [Certified Adversarial Robustness via Randomized Smoothing](proof_ref/dl-specializations-2026-10/certified-adversarial-robustness-via-randomized-smoothing-1902.02918/README.md) · [arXiv](https://arxiv.org/abs/1902.02918v2) | [T45](proofs/generalization/T45-certified-robustness.md) | ✓/✓ | core-claim-checked |

## statistics

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [Doubly Robust Off-policy Value Evaluation for Reinforcement Learning](proof_ref/foundations-2026-09/doubly-robust-off-policy-value-evaluation-for-reinforcement-1511.03722/README.md) · [arXiv](https://arxiv.org/abs/1511.03722v3) | [T11](proofs/statistics/T11-doubly-robust.md) | ✓/✓ | intake |
| [Double/Debiased Machine Learning for Treatment and Causal Parameters](proof_ref/foundations-2026-09/double-debiased-machine-learning-for-treatment-and-structural-1608.00060/README.md) · [arXiv](https://arxiv.org/abs/1608.00060v7) | [T11](proofs/statistics/T11-doubly-robust.md) | ✓/✓ | intake |
| [A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification](proof_ref/foundations-2026-09/a-gentle-introduction-to-conformal-prediction-and-distribution-2107.07511/README.md) · [arXiv](https://arxiv.org/abs/2107.07511v6) | [T18](proofs/statistics/T18-split-conformal.md) | ✓/✓ | intake |
| [Conformal Risk Control](proof_ref/foundations-2026-09/conformal-risk-control-2208.02814/README.md) · [arXiv](https://arxiv.org/abs/2208.02814v4) | [T18](proofs/statistics/T18-split-conformal.md) | ✓/✓ | intake |
| [A Theoretical Framework for Statistical Evaluability of Generative Models](proof_ref/core-theory-2026-09/a-theoretical-framework-for-statistical-evaluability-of-generative-2604.05324/README.md) · [arXiv](https://arxiv.org/abs/2604.05324v3) |  | ✓/✓ | imported-binary-validated |
| [Algorithms with Calibrated Machine Learning Predictions](proof_ref/core-theory-2026-09/algorithms-with-calibrated-machine-learning-predictions-2502.02861/README.md) · [arXiv](https://arxiv.org/abs/2502.02861v4) | [T17](proofs/evaluation-monitoring/T17-calibrated-predictions.md) | ✓/✓ | imported-method-card-only |
| [Distribution-Free Predictive Inference For Regression](proof_ref/core-theory-2026-09/distribution-free-predictive-inference-for-regression-1604.04173/README.md) · [arXiv](https://arxiv.org/abs/1604.04173v2) | [T18](proofs/statistics/T18-split-conformal.md) | ✓/✓ | imported-claim-checked-arxiv |

## transformer-icl

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [Transformers learn in-context by gradient descent](proof_ref/foundations-2026-09/transformers-learn-in-context-by-gradient-descent-2212.07677/README.md) · [arXiv](https://arxiv.org/abs/2212.07677v2) | [T14](proofs/deep-learning/T14-algorithm-simulation.md) | ✓/✓ | intake |
| [What learning algorithm is in-context learning? Investigations with linear models](proof_ref/foundations-2026-09/what-learning-algorithm-is-in-context-learning-investigations-2211.15661/README.md) · [arXiv](https://arxiv.org/abs/2211.15661v3) | [T14](proofs/deep-learning/T14-algorithm-simulation.md) | ✓/✓ | intake |
| [An Explanation of In-context Learning as Implicit Bayesian Inference](proof_ref/foundations-2026-09/an-explanation-of-in-context-learning-as-implicit-2111.02080/README.md) · [arXiv](https://arxiv.org/abs/2111.02080v6) | [T14](proofs/deep-learning/T14-algorithm-simulation.md), [T21](proofs/evaluation-monitoring/T21-bayesian-filtering.md) | ✓/✓ | intake |
| [In-Context Deep Learning via Transformer Models](proof_ref/core-theory-2026-09/in-context-deep-learning-via-transformer-models-2411.16549/README.md) · [arXiv](https://arxiv.org/abs/2411.16549v2) | [T14](proofs/deep-learning/T14-algorithm-simulation.md) | ✓/✓ | imported-binary-validated |
| [Strategy Coopetition Explains the Emergence and Transience of In-Context Learning](proof_ref/core-theory-2026-09/strategy-coopetition-explains-the-emergence-and-transience-of-2503.05631/README.md) · [arXiv](https://arxiv.org/abs/2503.05631v2) |  | ✓/✓ | imported-binary-validated |
| [Training Dynamics of In-Context Learning in Linear Attention](proof_ref/core-theory-2026-09/training-dynamics-of-in-context-learning-in-linear-2501.16265/README.md) · [arXiv](https://arxiv.org/abs/2501.16265v2) | [T14](proofs/deep-learning/T14-algorithm-simulation.md) | ✓/✓ | imported-binary-validated |
| [In-Context Learning of Linear Dynamical Systems with Transformers: Approximation Bounds and Depth-Separation](proof_ref/recent-accepted-2025-2026/in-context-learning-of-linear-dynamical-systems-with-2502.08136/README.md) · [arXiv](https://arxiv.org/abs/2502.08136v3) | [T14](proofs/deep-learning/T14-algorithm-simulation.md) | ✓/✓ | imported-claim-checked-arxiv |

## transport

| 论文 | 模板 | PDF/source | 核验状态 |
|---|---|---|---|
| [Computational Optimal Transport](proof_ref/foundations-2026-09/computational-optimal-transport-1803.00567/README.md) · [arXiv](https://arxiv.org/abs/1803.00567v4) | [T08](proofs/sequential-decision/T08-mirror-descent.md), [T19](proofs/generation-transport/T19-transport-risk.md) | ✓/✓ | intake |
| [Sinkhorn Distances: Lightspeed Computation of Optimal Transportation Distances](proof_ref/foundations-2026-09/sinkhorn-distances-lightspeed-computation-of-optimal-transportation-distances-1306.0895/README.md) · [arXiv](https://arxiv.org/abs/1306.0895v1) | [T19](proofs/generation-transport/T19-transport-risk.md) | ✓/✓ | intake |
