# 证明怎样蒸馏：留下可迁移的步骤和必须重证的接口

[首页](../README.md) · [AI 证明合同](AI_PROOF_CONTRACT.md) · [近期精读](RECENT_RESEARCH_2026_10.md)

蒸馏的单位是一个可以重新实例化的论证。先问它解决什么缺口，再写输入/输出、关键变换、每一步条件，以及迁移后哪些部分仍需证明。

## 一张蒸馏卡应该保留什么

1. **源命题**：固定版本、位置、全部关键假设和目标量。
2. **核心动作**：例如换一个 ghost sample、构造指数包络、耦合同起点轨迹或按码长分配失败预算。
3. **基础推导**：在简化而明确的设定下完整重推，解释每个中间量的作用。
4. **接口**：误差在哪个分布下、输出是哪个迭代、oracle 如何获得、概率事件怎样传递。
5. **一个反例**：只破坏一个关键条件，说明为什么不能迁移。
6. **新增义务**：论文更强的 rate、架构或算法结论还需要什么 lemma。

新旧方法的比较要对齐数据、loss、算法、资源、随机性、度量与参数范围。版本很新或来自知名会议，不免除逐条核验。

## 本轮的四条实际路线

| 经典动作 | 本轮蒸馏 | 可复用输出 | 需要保留的接口 |
|---|---|---|---|
| smoothness + 条件期望 + telescope | [有偏 SGD](../extensions/经典下降证明的偏差与方差接口.md) | 平均/随机输出的期望 stationarity | 条件偏差、中心化噪声、可测性和步长 |
| Hoeffding + Kraft + union bound | [编码界](../extensions/经典编码界与数据依赖解码器.md) | 数据选择模型的同时风险界 | decoder 与候选族必须事先固定 |
| ghost sample + bounded differences + MGF | [T50 证书指数包络](../proofs/generalization/T50-data-dependent-certificate-envelope.md) | 从观测证书控制总体期望 | 外层观测概率不改变左端的期望量词 |
| coupling + Young + Grönwall | [T51 Flow 轨迹误差](../proofs/generation-transport/T51-flow-trajectory-error.md) | 速度 L2 误差到 Wasserstein | 误差评估 law、学习场 Lipschitz、起点与数值解算 |

前三篇近期原文的精读记录与未闭合处见 [2026-10 精读](RECENT_RESEARCH_2026_10.md)。流形扩散作为复杂度与来源审计案例使用，原文疑点保留在核验卡中。

## 如何让 AI 真正完成证明

先让 agent 写原命题与核心路线，再展开关键步骤；遇到缺口，明确是要补 lemma、增条件、弱化结论还是给反例。只有修正后的命题也能闭合时，才声明对应结果。

[有偏 SGD 账本](../examples/biased_sgd_ledger.json) 是填写完成的正例；[完整学习证明](END_TO_END_LEARNING_PROOF.md) 展示更长的模型—训练—泛化组合。两者说明严格约束也要支持合法证明的完成。

新增内容进入 canonical 模板或扩展，更新 registry 和反链；来源核验卡记录具体范围；根目录另建当次更新目录。不要将同一推导复制到 skill、README 和多份索引里。
