# DL 理论框架：覆盖了什么，怎样证明

[首页](../README.md) · [模板目录](../proofs/README.md) · [论文级审查](THEORY_REVIEW.md)

## 当前审计结论（2026-10-20）

2026-09-28 的 T32–T39 连通逼近、统计估计与经验优化；10-02 的 T40–T49 增加专项原型；10-20 新增 T50/T51 的证书量词和 Flow 轨迹桥，现在共 47 张卡。每条路线的使用边界保留在下表。

最新改进还包括 [经典与近期证明蒸馏](PROOF_DISTILLATION.md)、[AI 证明合同](AI_PROOF_CONTRACT.md)及逐 Claim 账本检查；[近期精读](RECENT_RESEARCH_2026_10.md) 明确区分局部核验通过与来源问题记录。

现在有一个 [从可执行算法到测试风险的完整例子](END_TO_END_LEARNING_PROOF.md)，关闭模型、数据、训练、风险与失败概率接口。对明确假设下的基础论证，框架和工作流程具备论文级理论审查所需的主要环节；单个研究项目仍须逐条实例化自己的定理。

## 1. 没有单一的 DL 理论认证模板

不同论文可能只贡献逼近下界、优化收敛、泛化界、机制解释或一个新的数学模型，并不要求每篇把所有方向都证明一遍。

共同要求是：主张和形式结论一致、假设适当且完整、核心推导正确、依赖引理可追溯，并解释贡献的范围与直觉。NeurIPS 2026 的理论审稿指导也明确强调这些方面，且纯理论贡献不必以实验作为必要条件。[官方审稿指导](https://neurips.cc/Conferences/2026/ReviewerGuidelines)

因此本库使用“研究问题 + 证明义务”的框架，而非把一组术语当作投稿认证。

## 2. 学习系统的共同对象

先固定数据生成分布 $\mathcal D$、样本 $S$、模型族 $\mathcal H$、损失、训练算法 $A$ 和输出 $\widehat h=A(S,U)$，其中 $U$ 是算法随机性。

接着选要证明哪一件事：

| 问题 | 典型量词/目标 | 主要模板 |
|---|---|---|
| 模型能否表示目标 | 对函数类逐个存在网络，误差与资源受限 | [T34](../proofs/deep-learning/T34-neural-approximation.md)、[T41](../proofs/deep-learning/T41-barron-random-feature-approximation.md)、[T20A](../proofs/lower-bounds-expressivity/T20A-constructive-simulation.md) |
| 算法能否训练到某种解 | 轨迹/随机输出的 stationarity、gap 或方向 | [T01](../proofs/optimization/T01-descent.md)、[T40](../proofs/optimization/T40-second-order-stationarity.md)、[T42](../proofs/deep-learning/T42-feature-drift-kernel-dynamics.md)、[T39](../proofs/optimization/T39-proximal-nonsmooth.md) |
| 有限样本能否泛化 | 固定类或数据依赖学习器的风险偏差 | [T04](../proofs/generalization/T04-stability.md)、[T05](../proofs/generalization/T05-pac-bayes-information.md)、[T33](../proofs/generalization/T33-uniform-convergence.md) |
| 为什么复杂模型仍可能泛化 | norm/margin、稳定性、信息或压缩控制 | [T35](../proofs/generalization/T35-margin-norm.md)、[T38](../proofs/generalization/T38-compression.md) |
| 表示是否对任务有用 | 预训练目标与 downstream risk 的连接 | [T37](../proofs/deep-learning/T37-contrastive-transfer.md)、[T19](../proofs/generation-transport/T19-transport-risk.md) |
| 最终任务风险怎样组合 | approximation + estimation + optimization；训练 loss 到评价 loss | [T32](../proofs/generalization/T32-excess-risk-decomposition.md)、[T49](../proofs/generalization/T49-surrogate-bayes-risk.md)、[完整例子](END_TO_END_LEARNING_PROOF.md) |
| 哪些能力不可能实现 | 覆盖全部允许算法/模型的下界 | [T12](../proofs/lower-bounds-expressivity/T12-information-lower-bounds.md)、[T20B](../proofs/lower-bounds-expressivity/T20B-expressivity-lower-bound.md)、[T44](../proofs/lower-bounds-expressivity/T44-message-passing-wl.md) |
| 系统附加保证是什么 | 对称变换、输入扰动、相邻数据、通信或干预各自有不同量词 | [T43](../proofs/deep-learning/T43-equivariance-symmetry.md)、[T45](../proofs/generalization/T45-certified-robustness.md)、[T46](../proofs/statistics/T46-gaussian-privacy-accounting.md)、[T47](../proofs/optimization/T47-local-training-client-drift.md)、[T48](../proofs/statistics/T48-causal-identification.md) |

以上维度参考 DL 数学领域的问题分类；具体路线与覆盖判断是本库的整理。[The Modern Mathematics of Deep Learning](https://arxiv.org/abs/2105.04026)

## 3. 当前覆盖矩阵

新卡的 `self-contained-core` 表示卡内给出了列明条件下的基础推导；它仍依赖注明的基本引理，不代表形式化证明器认证或整篇原论文都已重证。`bounded-scope` 则继续强调特定模型和来源范围。

| 模块 | 当前覆盖 | 使用边界 |
|---|---|---|
| 一阶/随机优化 | T01–T03、T15–T16、PL 扩展 | bias、state recursion 和 good event 必须实例化 |
| 二阶优化 | T40 | 精确负曲率 oracle 原型闭合；一阶扰动算法的逃逸概率/总成本另证 |
| 非光滑/复合目标 | T39 | smooth + convex-prox 部分；不包办任意非凸非光滑 ReLU 目标 |
| 学习误差闭环 | T32、完整随机特征例子、T49 | 小梯度需额外条件才等于小 gap；训练/评价 loss 需桥 |
| 经验过程/一致收敛 | T33、P09 | i.i.d. 固定类；数据依赖类、相关样本另证 |
| 网络逼近与表达 | T34、T41、T14、T20A/B | 一维与 variation/random-feature 原型；一般 Sobolev 最紧 rate 专修 |
| 现代泛化路线 | T04/T05/T35/T38/T50 | 观测证书对期望 gap 的高概率界，仍须保留左端量词 |
| 训练机制 | T09/T10/T36/T42 | 时变核恒等式闭合；谱下界、表示收益与长期极限仍需项目证明 |
| 对称架构与图表达力 | T43/T44 | 有限群、无位置 attention、标准 message passing；其他结构重定义接口 |
| 对抗鲁棒 | T45 | Lipschitz 与 Gaussian L2 平滑；实际证书须有效概率估计 |
| 差分隐私 | T46 | Gaussian/RDP/full-batch 原型；subsampled accountant 与 user-level 另证 |
| 分布式/联邦 | T47、T02/T03 | 完整确定性 drift 原型；抽样、异步、噪声、压缩需新的递推 |
| 因果识别 | T48/T11 | basic g-formula 与估计分开；一般图、序列、mediation 专修 |
| 表示/对比/迁移 | T37/T19 | 信息量、pairing 与任务标签必须有明确联系 |
| 生成与采样 | T13/T51、CFM 扩展 | SDE/ODE/CTMC 各有条件；Flow 误差 law、学习场正则性与 solver 误差分别检查 |
| 在线决策与可靠性 | T06–T08、T11、T17–T24 | 模型正确性、coverage、交换性、因果识别各自检查 |

## 4. 仍需按项目专修的方向

本轮给上次缺口建立了有完整推导的基础原型。尚未穷尽的是更强/更广的结果：一阶随机扰动的最紧鞍点复杂度、深度分离与 Sobolev 类的最优速率、隐藏层真正学习任务结构的有限样本理论、连续群/高阶 GNN、所有扰动范数的鲁棒认证、subsampled/user-level DP、全部联邦通信模型、一般因果图/动态干预，以及特定大模型的长时间训练和 scaling law。

这些是显式扩展边界。遇到相应研究任务，应沿原论文补专用条件与证明；不能因为目录里有“下界”“谱”“稳定性”就宣称已经覆盖。

## 5. 建议的循序渐进阅读

1. 先读 T32，知道最终希望控制什么。
2. 读 T33 与 T34，分清数据带来的误差与模型类的局限。
3. 回到 T01/T02/T09/T39，确认训练过程实际控制的是哪种量。
4. 用 T35/T36/T38 研究模型尺度、方向和编码。
5. 用 T37 检查预训练目标与下游任务之间是否有真正的桥。
6. 写论文前按 [论文级审查](THEORY_REVIEW.md) 关闭假设、依赖与范围缺口。
7. 通读 [完整学习证明](END_TO_END_LEARNING_PROOF.md)，练习三条引理的合法合成；再按具体项目挑 T40–T49。

## 6. 怎样判断一条证明是否已经完成

“有主题入口”“卡内基础命题已推导”“固定原文中的特定 claim 已核对”“新项目的全部证明义务已关闭”是四种不同进度。查 [核验状态](../证明模板核验状态.md) 与论文核验卡可以确定具体范围。

最后核对五件事：命题的所有对象都已定义；假设在陈述中可找到；引理依赖无循环；结论确实由同一度量/概率事件推出；资源和输出规则与算法一致。若其中某项未闭合，记录具体缺口后继续证明。
