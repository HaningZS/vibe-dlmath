# 近期证明进展：2026 年 9–10 月的三个精读案例

[首页](../README.md) · [证明蒸馏](PROOF_DISTILLATION.md) · [AI 证明合同](AI_PROOF_CONTRACT.md)

检索截至 2026-10-19，本地 PDF/TeX 交叉复核完成于 2026-10-20。本轮围绕可迁移证明选择三篇原文：两篇提取了完整基础引理，一篇保留为带来源问题的审核案例。选择依据是推导的复用价值和实际核验范围。

| 原文 | 时间与发表证据 | 实际吸收的内容 | 当前状态 |
|---|---|---|---|
| [Certification-Enhanced Generalization Bounds](https://arxiv.org/abs/2610.06238v1)，Elmecker-Plakolm / Wicker | 2026-10-05；作者声明 NeurIPS 2026 accepted，[官方目录](https://neurips.cc/Downloads/2026) 有题名；未进一步确认展示类别 | 指数距离包络 + bounded differences + MGF，接经典稳定性 | Proposition 2 / Theorem 1 的指定范围已核 |
| [Flow Matching under Noisy Latent Structure](https://arxiv.org/abs/2609.38918v1)，Hao / Ji | 2026-09-30；preprint | 同起点 coupling + 学习场 Lipschitz + Grönwall | Theorem 5.2 的连续流桥已核，完整统计率未逐式审计 |
| [Riemannian Diffusion under Nonnegative Ricci Curvature](https://arxiv.org/abs/2609.36568v1)，Liu / Huang | 2026-09-29；preprint | 路径 KL、Fisher 耗散、score 与 Brownian 成本分账的审核方式 | `source-issues-recorded`，不能标作全文证明已核验 |

## 1. 样本特定证书：新的外壳连接经典概率工具

一个数据集上的稳定性证书本身，不能直接推出总体泛化。新工作用按替换距离衰减的上包络，使其对数满足 bounded differences，再把观察到的证书接到一个总体期望量。

[T50](../proofs/generalization/T50-data-dependent-certificate-envelope.md) 完整重推这条基础链，并处理零包络、预先固定参数和多个参数的选择预算。关键量词是：高概率发生在观测到的右端证书，左端仍是训练集上的期望泛化差。

实际算法需要一个可靠的包络上界。有限次扰动试验只得到已观察样本的最大值，不能自动升级为 supremum 的上界。

[本地 PDF/TeX 核验记录](../proof_ref/proof-distillation-2026-10/certification-enhanced-generalization-bounds-2610.06238/核验笔记.md) 给出 v1、物理页码、TeX label/行号及重新计算的哈希。

## 2. Noisy latent Flow Matching：误差评估的分布不能换

这篇研究带固定正噪声的低维 latent 生成结构。它的采样桥在给定训练数据后，从同一初值耦合真实流和学习流；关键加减项让速度误差在真实边缘 law 下评估，同时使用学习场的空间 Lipschitz 常数。

[T51](../proofs/generation-transport/T51-flow-trajectory-error.md) 抽取并完整重推连续时间引理。随后接统计率，还需原文特定的生成器、受约束 ERM 和对时间/辅助噪声的精确积分；实际 SGD 的优化误差不能被省略。Euler 离散化需要额外的时间正则性。固定噪声是目标的一部分，不能据此声称恢复了无噪声流形。

[本地 PDF/TeX 核验记录](../proof_ref/proof-distillation-2026-10/flow-matching-under-noisy-latent-structure-beyond-exact-2609.38918/核验笔记.md) 定位了连续流、空间约束和独立的 Euler 条件。

## 3. 流形扩散：保留原式，并记录来源中的问题

该文主定理声明的离散误差同时包含
$hd\log(T/\delta)+h^2d^4T^2+Ch^3d^7T^3$。缩写成近线性维数需要限定其他量和足够小的目标误差；采样到 $p_\delta$ 与逼近原始 $p_0$ 是不同目标。

本地 PDF 与 TeX 的交叉检查确认三类展示不一致：Hessian 的上标重复缺失、附录步长括号与主定理不同、Pinsker 平方位置与随后声称的步长阶不一致。核验卡给出准确位置和可能的局部修复方向；本轮没有完成修复后的全证明链，也没有据此判定整篇主结论为假。

因此它进入 [T13](../proofs/generation-transport/T13-sampler-error.md) 的复杂度/来源审核案例。读者应学习如何把 score 估计、离散化、Brownian 模拟和目标平滑分开记账，同时保留未闭合义务。

[问题清单与本地证据](../proof_ref/proof-distillation-2026-10/sharp-convergence-and-sampling-trade-offs-for-riemannian-2609.36568/核验笔记.md)。

## 4. 后续更新如何保持可信

每篇新论文先进入 intake；下载只核对工件。选定核心 claim 后，从固定 PDF/source 提取精确陈述和依赖，再重推能迁移的基础步骤，记录作用域与反例。论文如有新版本，先比较已用定理和已记录疑点，不能只更换日期和下载链接。

经典推导、近期核验与实际 skill 回答分别留证；[行为评测](../evals/README.md) 检查 agent 是否遵守这些接口，而不把目录数量当作证明能力。
