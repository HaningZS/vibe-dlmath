# 从数学前置走到 AI 论文证明

[返回首页](README.md) · [论文总目录](PAPERS.md) · [补充证明专题](extensions/README.md)

按具体证明任务检索：[独立模板目录](proofs/README.md) · [组合工作流](docs/PROOF_WORKFLOW.md) · [Skill](docs/SKILL.md)。

## DL 核心主线

先读 [T32 风险分解](proofs/generalization/T32-excess-risk-decomposition.md)，再分别补 [T33 统计估计](proofs/generalization/T33-uniform-convergence.md)、[T34 函数逼近](proofs/deep-learning/T34-neural-approximation.md) 和优化路线。随后用 [T35 间隔](proofs/generalization/T35-margin-norm.md)、[T36 隐式偏置](proofs/deep-learning/T36-implicit-bias.md)、[T37 对比/下游](proofs/deep-learning/T37-contrastive-transfer.md)、[T38 压缩](proofs/generalization/T38-compression.md) 分析模型选择与表示。

非光滑目标先检查 [T39](proofs/optimization/T39-proximal-nonsmooth.md) 是否适用。完整覆盖范围和仍需专修的方向见 [DL 框架](docs/DL_THEORY_FRAMEWORK.md)。

然后通读 [从随机特征到测试风险的闭合证明](docs/END_TO_END_LEARNING_PROOF.md)。它把可抽样特征 law、未知比较解、数据独立性、projected GD gap 和失败概率放在同一个定理里。

## 专项理论分支

| 研究问题 | 循序渐进的入口 |
|---|---|
| 小梯度附近是不是鞍点 | Hessian/谱前置 → [T40 负曲率与二阶驻点](proofs/optimization/T40-second-order-stationarity.md) |
| 高维函数为什么仍能被有限宽网络近似 | Monte Carlo/内积 → [T41 表示范数](proofs/deep-learning/T41-barron-random-feature-approximation.md) → 完整学习例子 |
| 隐藏特征到底改变了什么 | Jacobian/ODE → [T42 时变核](proofs/deep-learning/T42-feature-drift-kernel-dynamics.md) → T09/T10 的专用条件 |
| 架构对称性与图能力 | 群/归纳 → [T43 等变](proofs/deep-learning/T43-equivariance-symmetry.md) → [T44 1-WL 限制](proofs/lower-bounds-expressivity/T44-message-passing-wl.md) |
| 小扰动内如何保证类别不变 | Lipschitz/概率尾界 → [T45 鲁棒认证](proofs/generalization/T45-certified-robustness.md) |
| 加噪声怎样给隐私保证 | Gaussian/MGF → [T46 RDP](proofs/statistics/T46-gaussian-privacy-accounting.md) → 再读 DP-SGD accountant |
| 少通信为什么改变训练轨迹 | 一步下降/势函数 → [T47 drift](proofs/optimization/T47-local-training-client-drift.md) → Local SGD/SCAFFOLD |
| 预测能否回答干预问题 | 条件期望 → [T48 因果识别](proofs/statistics/T48-causal-identification.md) → T11 估计 |
| 交叉熵下降怎样控制分类错误 | KL/风险分解 → [T49 surrogate 桥](proofs/generalization/T49-surrogate-bayes-risk.md) |

先学习共同工具，再按研究问题选分支。每条分支先用讲义或可计算模型建立直觉，再读技术性结果。

## 共同前置

1. [数学学习路线](<Math 基础/AI Researcher 数学学习路线.md>)：向量、梯度、概率、优化与统计。
2. [量词、归纳与望远镜求和](<Math 基础/证明工具/量词、归纳、不变量与望远镜求和.md>)：把“算法表现好”改写成精确命题。
3. [测度、条件期望与滤过](<Math 基础/概率统计/测度、条件期望、滤过与适应过程.md>)：说清每一步已经知道什么。
4. [集中不等式与鞅](<Math 基础/概率统计/集中不等式、MGF、鞅与自归一化过程.md>)：把随机误差接到高概率结论。
5. [通用证明原语](通用证明原语.md)：定位一步不等式、好事件、信息预算与误差递推。

模板、前置和旧论文 PDF 的对应关系见 [数学前置与论文证明导航](数学前置与论文证明导航.md)。

## 优化与随机梯度

阅读：Bubeck 凸优化 → Bottou–Curtis–Nocedal 大规模优化 → PL 条件 → SAG/SPIDER。

从 smoothness 写出一步下降，识别 bias/variance/状态误差，再选 telescoping 或 Lyapunov。对应 T01–T03、T08、T15–T16。

练习：[PL 条件与 SGD 噪声地板](extensions/PL条件与SGD噪声地板.md)。能手推有限 $T$ 的几何级数，解释常数学习率为何留下噪声残差。

论文入口：[optimization](PAPERS.md#optimization)。原有广义光滑与重尾优化从 [原库核验导航](proof_ref/核验导航.md) 阅读。

## 高维概率与持续有效推断

阅读：Vershynin 非渐近随机矩阵 → Tropp 矩阵浓缩 → Howard 等人的 time-uniform Chernoff / confidence sequences。

矩阵分支控制所有方向的最坏误差；时间分支控制任意时刻的越界。维度和时间是两个不同的“同时”。

练习：[协方差误差](extensions/矩阵Bernstein与协方差误差.md)、[Ville 不等式](extensions/Ville不等式与随时有效推断.md)。对应 T06、T09、T18、T23。

论文入口：[concentration](PAPERS.md#concentration)。

## 泛化、PAC-Bayes 与插值

阅读：Alquier PAC-Bayes 教程 → Xu–Raginsky 信息论泛化 → 随机标签实验 → double descent → ridgeless least squares。

分清 posterior/先验与高概率量词、MI 期望界、稳定性中的相邻数据集，以及风险曲线中的插值阈值。这些结果的对象与假设不同。

前置：[算法稳定性、经验过程与 PAC-Bayes](<Math 基础/统计学习理论/算法稳定性、经验过程与 PAC-Bayes.md>)。对应 T04–T05、T09。

论文入口：[generalization](PAPERS.md#generalization)。最低掌握标准：明确训练集、测试样本、学习算法随机性和保证对谁成立。

## 宽网络、隐式偏置与特征学习

阅读：NTK → 宽网络线性化 → Lazy Training → mean-field → separable-data implicit bias。

先看参数化与 scaling，再看极限。NTK 常跟踪初始化附近的核；mean-field 跟踪粒子经验分布；implicit bias 则问优化路径偏向哪种解。

前置：[矩阵谱](<Math 基础/线性代数/二次型、正定矩阵与谱.md>)、[Grönwall 与误差传播](<Math 基础/微积分与分析/Grönwall、Duhamel 与稳定性误差传播.md>)。对应 T09–T10。

论文入口：[neural-dynamics](PAPERS.md#neural-dynamics)。检查宽度、学习率、时间范围、初始条件与特征是否真的变化。

## Transformer 与上下文学习

阅读：线性模型中的 learning algorithm → in-context gradient descent → implicit Bayesian inference，再回到原库的新近 ICL 动力学论文。

把三个问题分开写：存在某组权重能否实现算法；训练能否找到它；实际模型在做什么。构造性证明通常只回答第一个。

前置：[矩阵微分](<Math 基础/微积分与分析/矩阵微分、Trace Trick 与反向传播.md>)、[贝叶斯估计](<Math 基础/概率统计/最大似然、MAP 与贝叶斯估计.md>)。对应 T14、T20–T21。

论文入口：[transformer-icl](PAPERS.md#transformer-icl)。

## Bandit 与强化学习

阅读：bandit regret 综述 → self-normalized 在线最小二乘 → 原库 linear-MDP → offline pessimism → TRPO。

先分清 regret、value suboptimality、sample complexity，再区分 online 数据与 offline 日志。在线探索常使用 optimism；离线覆盖不足则需要处理未见过的动作。

前置：[Markov/状态空间](<Math 基础/概率统计/Markov 链、随机过程与状态空间模型.md>)、[Bregman 与 Mirror Descent](<Math 基础/微积分与分析/Bregman 散度、Mirror Descent 与在线学习.md>)。对应 T06–T08、T12。

论文入口：[rl-bandits](PAPERS.md#rl-bandits)。同作者论文的 arXiv 长版与会议题目可能不同，引用时核对具体版本。

## 偏好学习与后训练

原库已有 DPO、KL 约束下的 iterative preference learning 与 f-divergence RLHF。按 KL 几何 → 奖励/策略变量替换 → 数据分布与覆盖的顺序读，明确何时是目标等价、何时只是有限样本训练近似。

前置：[Bregman 与 Mirror Descent](<Math 基础/微积分与分析/Bregman 散度、Mirror Descent 与在线学习.md>)、[KL 散度](<Math 基础/概率统计/信息论基础：熵、交叉熵与 KL 散度.md>)。对应 T07–T08。论文入口：[post-training](PAPERS.md#post-training)。

## 统计可靠性、DR 与 conformal

阅读：Gentle Introduction to Conformal → Conformal Risk Control；另一分支读 Double/Debiased ML → sequential doubly robust evaluation。

conformal 依赖交换性与名次结构；DR/orthogonal 方法用残差校正减弱 nuisance estimation error。两者的适用条件应分别写清。

前置：[覆盖保证](<Math 基础/概率统计/交换性、Conformal Prediction 与覆盖保证.md>)、[重要性采样](<Math 基础/概率统计/蒙特卡洛、重要性采样与 MCMC.md>)。对应 T11、T18。

论文入口：[statistics](PAPERS.md#statistics)。检查 coverage 是 marginal 还是 conditional、risk 是期望还是高概率、propensity 是否有共同支持。

## 信息下界

阅读：Fano 教程 → 随机非凸优化 lower bounds，再回到原库 interactive lower-bound 卡。

先规定算法能问什么 oracle，再构造彼此难区分的世界。若算法类别或信息接口改变，原下界不一定适用。

前置：[Le Cam、Fano、Assouad 与 Yao](<Math 基础/概率统计/统计距离、Le Cam、Fano、Assouad 与 Yao 下界.md>)。对应 T12、T20。

论文入口：[lower-bounds](PAPERS.md#lower-bounds)。

## 最优传输、扩散与 Flow Matching

阅读：Computational OT → Sinkhorn；连续生成分支读 Score SDE → sampling theory → FM → Rectified Flow → Consistency Models。

先认清 coupling、path、velocity、density 和 metric，再区分训练误差、过程近似与 solver 误差。不同距离的上界不能不加条件地相加。

前置：[最优传输](<Math 基础/概率统计/最优传输与 Wasserstein 距离.md>)、[ODE/SDE](<Math 基础/微积分与分析/ODE、SDE 与连续时间生成模型.md>)。对应 T13、T19。

练习：[CFM 的条件期望证明](extensions/条件期望怎样连接CFM与FM.md)。论文入口：[transport](PAPERS.md#transport)、[generative](PAPERS.md#generative)。

## 表示学习理论

阅读：Arora 等人的 latent-class contrastive theory → 球面 alignment/uniformity，再回到原库自然图像与预训练归纳偏置论文。

前置：[信息论](<Math 基础/概率统计/信息论基础：熵、交叉熵与 KL 散度.md>)、[表示几何](<Math 基础/线性代数/范数、距离、相似度与度量学习.md>)。

论文入口：[representation](PAPERS.md#representation)。检查 positive/negative 的生成方式、false negatives、下游标签假设，以及 population 与 finite-batch 的差异。

## 日常更新方式

本轮的经典—近期连接见 [证明蒸馏](docs/PROOF_DISTILLATION.md)：[有偏下降](extensions/经典下降证明的偏差与方差接口.md)、[编码界与 decoder](extensions/经典编码界与数据依赖解码器.md)、[T50 证书包络](proofs/generalization/T50-data-dependent-certificate-envelope.md)、[T51 Flow 轨迹桥](proofs/generation-transport/T51-flow-trajectory-error.md)。原文核验与待修问题见 [近期精读](docs/RECENT_RESEARCH_2026_10.md)，AI 输出按 [证明合同](docs/AI_PROOF_CONTRACT.md) 留下逐 Claim 状态。

发现缺口 → 搜索已有模板与前置 → 在 catalog 加入官方论文 → 下载并保留版本 → 写核验卡 → 把关键 lemma 接回专题 → 根目录新增详细更新目录。

学完一篇的最低成果是：能说明它新增了哪个连接、全部关键假设、一个失败例子，以及原文中具体的证明位置。
