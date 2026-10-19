# 可复用证明模板目录

[首页](../README.md) · [如何组合证明](../docs/PROOF_WORKFLOW.md) · [Skill 使用](../docs/SKILL.md)

按目标进入主题，再读单张卡的复用契约。当前 47 张卡；T01–T25 与 T20A/T20B 保留，T32 起按 DL 核心与专项理论增量扩展。T26–T31 仍是旧 intake 占位。

[DL 理论框架与覆盖边界](../docs/DL_THEORY_FRAMEWORK.md) · [论文级证明审查](../docs/THEORY_REVIEW.md)

类型决定能怎样使用：证明模板须重新实例化；方法卡只覆盖特定问题；经验代数工具不提供显著性或机制保证。

## 优化与随机估计

| 编号 | 适用目标 | 类型 |
|---|---|---|
| [T01](optimization/T01-descent.md) | 把单步目标下降累积成平均梯度平方界。 | 证明模板 |
| [T02](optimization/T02-lyapunov.md) | 给辅助状态误差记账，让联合势函数下降。 | 证明模板 |
| [T03](optimization/T03-variance-reduction.md) | 用同一随机样本的梯度差，把估计误差绑定到移动路径。 | 证明模板 |
| [T15](optimization/T15-generalized-smoothness.md) | 曲率随梯度变化时，先证明局部下降和轨迹闭合。 | 证明模板 |
| [T16](optimization/T16-heavy-tail-clipping.md) | 把裁剪梯度分成 centered martingale 与 clipping bias。 | 证明模板 |
| [T39](optimization/T39-proximal-nonsmooth.md) | 识别 smooth-plus-convex 结构，用 gradient mapping 处理复合目标。 | 证明模板 |
| [T40](optimization/T40-second-order-stationarity.md) | 用负曲率下降补一阶驻点，并显式区分 Hessian oracle 与一阶逃逸复杂度。 | 证明模板 |
| [T47](optimization/T47-local-training-client-drift.md) | 分解 local training 的位置偏差并控制客户端分歧、通信与输出。 | 证明模板 |

## 泛化与信息论

| 编号 | 适用目标 | 类型 |
|---|---|---|
| [T04](generalization/T04-stability.md) | 耦合相邻训练集的算法轨迹，控制期望泛化差。 | 证明模板 |
| [T05](generalization/T05-pac-bayes-information.md) | 分开使用 PAC-Bayes 高概率界和互信息期望界。 | 证明模板 |
| [T32](generalization/T32-excess-risk-decomposition.md) | 把总体 excess risk 拆成逼近、统计估计与经验优化误差。 | 证明模板 |
| [T33](generalization/T33-uniform-convergence.md) | 从固定函数类、ghost sample 和随机符号推出统一泛化界。 | 证明模板 |
| [T35](generalization/T35-margin-norm.md) | 用 normalized margin 与函数复杂度连接经验分类和总体风险。 | 证明模板 |
| [T38](generalization/T38-compression.md) | 用真实编码长度与统一事件控制压缩模型的泛化。 | 证明模板 |
| [T45](generalization/T45-certified-robustness.md) | 从 Lipschitz margin 或 Gaussian 平移事件推导指定范数的认证半径。 | 证明模板 |
| [T49](generalization/T49-surrogate-bayes-risk.md) | 由 binary log-loss excess 推到分类 excess，并保留模型与裁剪误差。 | 证明模板 |
| [T50](generalization/T50-data-dependent-certificate-envelope.md) | 用指数距离上包络把观测证书接到总体期望，保持量词与选择预算。 | 证明模板 |

## 在线决策与策略几何

| 编号 | 适用目标 | 类型 |
|---|---|---|
| [T06](sequential-decision/T06-linear-bandit.md) | 用置信椭球、optimism 与 elliptical potential 控制 pseudo-regret。 | 证明模板 |
| [T07](sequential-decision/T07-bellman.md) | 在正确策略的 occupancy 下展开 Bellman 价值误差。 | 证明模板 |
| [T08](sequential-decision/T08-mirror-descent.md) | 用三点恒等式与 Bregman 几何分析在线/策略更新。 | 证明模板 |

## 统计估计与覆盖

| 编号 | 适用目标 | 类型 |
|---|---|---|
| [T11](statistics/T11-doubly-robust.md) | 用残差校正把 nuisance 的一阶误差变成乘积余项。 | 证明模板 |
| [T18](statistics/T18-split-conformal.md) | 用交换性和名次对称性证明边际覆盖。 | 证明模板 |
| [T46](statistics/T46-gaussian-privacy-accounting.md) | 显式计算 Gaussian RDP、条件组合和 DP 转换，区分裁剪对象与采样。 | 证明模板 |
| [T48](statistics/T48-causal-identification.md) | 先用识别假设连接干预与观察 law，再分析 DR 或深度表示的估计误差。 | 证明模板 |

## 神经网络、表示与训练机制

| 编号 | 适用目标 | 类型 |
|---|---|---|
| [T09](deep-learning/T09-ntk.md) | 闭合初始谱、核稳定、下降与参数移动的联合归纳。 | 证明模板 |
| [T10](deep-learning/T10-mean-field.md) | 分开控制极限动力学优化误差与有限粒子近似误差。 | 证明模板 |
| [T14](deep-learning/T14-algorithm-simulation.md) | 通过逐层构造与稳定性说明受限网络能模拟哪个算法。 | 证明模板 |
| [T34](deep-learning/T34-neural-approximation.md) | 把网络存在性变成指定函数类、误差范数与资源的定量逼近。 | 证明模板 |
| [T36](deep-learning/T36-implicit-bias.md) | 区分 loss、参数与方向收敛，核对优化器的隐式偏置。 | 证明模板 |
| [T37](deep-learning/T37-contrastive-transfer.md) | 先证明对比目标的采样/信息关系，再单独连接下游任务风险。 | 证明模板 |
| [T41](deep-learning/T41-barron-random-feature-approximation.md) | 用表示范数与 Hilbert-space 方差控制高维随机特征的逼近误差。 | 证明模板 |
| [T42](deep-learning/T42-feature-drift-kernel-dynamics.md) | 精确跟踪时变核、参数移动与冻结核近似，不把核变化当下游收益。 | 证明模板 |
| [T43](deep-learning/T43-equivariance-symmetry.md) | 以群作用和层间恒等式证明等变性，并核对 attention 的位置与 mask。 | 证明模板 |

## 生成模型与分布输运

| 编号 | 适用目标 | 类型 |
|---|---|---|
| [T13](generation-transport/T13-sampler-error.md) | 在同一度量中组合连续过程、学习与离散采样误差。 | 证明模板 |
| [T19](generation-transport/T19-transport-risk.md) | 先指定 joint/label 条件，再把 transport cost 连接到风险差。 | 证明模板 |
| [T25](generation-transport/T25-feature-localization-card.md) | 复现单篇 feature-localization 论文的模型与假设。 | 问题特定方法卡 |
| [T51](generation-transport/T51-flow-trajectory-error.md) | 在真实边缘分布下控制速度误差，用学习场 Lipschitz 与耦合推出 Wasserstein 界。 | 证明模板 |

## 信息下界与表达能力

| 编号 | 适用目标 | 类型 |
|---|---|---|
| [T12](lower-bounds-expressivity/T12-information-lower-bounds.md) | 由困难实例的不可区分性推出指定算法类的风险下界。 | 证明模板 |
| [T20](lower-bounds-expressivity/T20-expressivity-router.md) | 将构造性上界与能力下界路由到两个独立模板。 | 路由页 |
| [T20A](lower-bounds-expressivity/T20A-constructive-simulation.md) | 显式构造满足资源约束的模型，并证明逐步模拟和组合误差。 | 证明模板 |
| [T20B](lower-bounds-expressivity/T20B-expressivity-lower-bound.md) | 覆盖全部允许模型，用资源限制或归约证明能力下界。 | 证明模板 |
| [T44](lower-bounds-expressivity/T44-message-passing-wl.md) | 通过 1-WL 归纳和具体图对证明消息传递 GNN 的表达力限制。 | 证明模板 |

## 评价、校准与在线监测

| 编号 | 适用目标 | 类型 |
|---|---|---|
| [T17](evaluation-monitoring/T17-calibrated-predictions.md) | 将 calibration 连接到特定在线问题的成本分解。 | 问题特定方法卡 |
| [T21](evaluation-monitoring/T21-bayesian-filtering.md) | 结合预测先验与当前 likelihood，区分静态和动态状态证据累积。 | 证明模板 |
| [T22](evaluation-monitoring/T22-ranking-proper-scoring.md) | 分开证明 AUROC 排序不变性与 Brier proper-scoring 分解。 | 证明模板 |
| [T23](evaluation-monitoring/T23-prefix-safety.md) | 从信息依赖图证明适应性和停止时间性质。 | 证明模板 |
| [T24](evaluation-monitoring/T24-baseline-gap.md) | 记录方法超过多种 baseline 的经验数值关系。 | 经验代数工具 |
