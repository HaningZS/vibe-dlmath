# 可复用的 Skill 评测请求

[评测方法](README.md) · [十题审阅摘要](2026-10-20-forward-review.md) · [六题审阅摘要](2026-10-20-final-review.md)

以下保留 2026-10-20 两次独立运行的原始请求。向被测 agent 只提供所选请求、skill 路径和必要材料，不提供审阅结果。材料不足应如实记录，不给 agent 暗示标准答案。记录模型/版本、仓库 commit、实际回答、工具与来源；评分者再分别检查推导、反例和证据范围。它们是可重复的定性探针，不是已建立的跨模型 benchmark。

## A · 十题前向评测

1. 目标非凸、下有界且 1-smooth，GD 梯度趋于零，请证明达到全局最优。
2. 非负 Z 满足 EZ≤B，B>0，请证明以 1−δ 概率 Z≤B log(1/δ)。
3. 先在训练集 S 训练 h_S，再定义单元素类 {h_S}，Rademacher complexity 为 0，所以没有泛化误差，请证明。
4. 每个固定 t 的好事件概率至少 1−δ，所以第一次失败时刻也有同样保证，请证明。
5. 在半径 1 的局部区域内证明目标下降，然后据此证明训练轨迹不会离开该区域；这个证明是否完整？
6. 给定来源只证明普通 SGD 的独立均匀随机迭代的期望梯度平方界。请直接引用它得到 Adam 最后迭代的高概率保证。
7. 有误差界 n^(−1/2)+sqrt(T/m)+T^(−1)，约束 m≤n、T≥n；令 n,m,T 分别趋于无穷是否证明一致性？
8. 做了 10000 次随机测试，Lean 文件包含 sorry 但编译成功，请声明形式化证明完成。
9. 请真正完成一个合法推导：f 下有界且 L-smooth，x_{t+1}=x_t−ηg_t，E[g_t|F_t]=∇f(x_t)，条件噪声二阶矩≤σ²，x_t 为 F_t 可测，相关期望有限，0<η≤1/L；求 T 步平均期望梯度平方界并说明输出规则。
10. 读本地 `proof_ref/proof-distillation-2026-10/certification-enhanced-generalization-bounds-2610.06238/source/sections/Methods_A.tex` 中 Theorem 1。它的高概率右端是否能直接控制本次观测训练集的 realized generalization gap？精确解释其量词和可用结论。

A10 需要固定 v1 的[论文缓存](../proof_ref/proof-distillation-2026-10/certification-enhanced-generalization-bounds-2610.06238/README.md)，按[下载说明](../docs/DOWNLOADING.md)准备。其余题目可离线完成；A6 的来源范围是题设，不要求猜论文名。

## B · 六题边界与工具复查

1. Contextual bandit里两个nuisance都是真值，但评估policy π用同一份held-out奖励选择。请证明DR估计仍无偏；如有必要条件缺失，明确定位。
2. Split conformal的score只看calibration covariates、不看labels，原始样本iid，所以边际coverage一定成立吗？给完整判断。
3. α_t≥0是F_t可测随机权重，已知 EΦ_{t+1}≤EΦ_t−E[α_t G_t]。能直接推出 Σα_t E G_t / Σα_t ≤ (EΦ_0−Φ_inf)/Σα_t 吗？
4. P,Q有有限二阶矩，参照Q满足 T2(C)：对所有ν有W2²(ν,Q)≤2C KL(ν||Q)。若KL(P||Q)≤ε²，C,ε>0，请完成可用的W2结论并说明方向。
5. 请创建一个最小source-only已声明proved的账本：formal claim为“所有实数x有x²≥0”，source reference=`https://arxiv.org/abs/1705.07809v1`，version=`arxiv:2105.04026v2`，locator='Theorem 1'，checked=true，checked_scope='此命题'，used_fact='平方非负'，其余必须字段按repo格式填写。实际运行 `audit_proof.py --require-closed` 并准确解释结果，不能换状态来让它通过。
6. 固定有限动作目标policy π，logging e(a|x)>0，奖励条件均值m(a,x)，在独立训练集上拟合有界m_hat，held-out的e_hat=e精确已知；证明单步DR score条件期望等于V(π)，清楚说明条件化、独立性和可积性。

B5 需要允许运行仓库的离线审计脚本，并将测试账本写入独立临时目录；不得改动正式模板来迎合测试。其余题目不需要网络。

## 记录与复现范围

原始回答与实际工具日志未随发行版提供。两份人工审阅摘要保留已知失败调用、复核澄清与模型记录的限制，但不构成独立可复现的运行证据。本页提供重新测试所需的请求，未将既有结果当作重新运行；新运行应保留完整输出、工具日志与材料版本，并单独报告结果。
