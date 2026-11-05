---
id: T49
type: proof-template
refined: 2026-10-02
status: self-contained-core
---

# T49. 交叉熵怎样接到分类错误：surrogate 与 Bayes 风险

[主题目录](README.md) · [风险分解 T32](T32-excess-risk-decomposition.md) · [Proper scoring T22](../evaluation-monitoring/T22-ranking-proper-scoring.md)

## 复用契约

**对象**：binary label $Y\in\lbrace0,1\rbrace$， $\eta(x)=P(Y=1\mid X=x)$，预测概率 $p(x)\in(0,1)$； $h_p(x)=1\lbrace p(x)\ge1/2\rbrace$。自然对数交叉熵风险有限。

**结论**：log-loss excess 等于条件 Bernoulli KL 的期望，且 $R_{01}(h_p)-R_{01}^\ast\le\sqrt{2(R_{log}(p)-R_{log}^\ast)}$。

**条件**：同一个数据 law 与同一个标签任务；reference 是 unrestricted Bayes risk，不是仅在当前模型类内最优的风险。

**失败例子**：模型族里最好的交叉熵仍可能有很大的逼近误差。把 empirical log loss 降到该族最小，不能直接推得接近 Bayes 分类器。

## 实例化时必须完成

- [ ] 固定 natural log/base、标签域、阈值和 tie 约定。
- [ ] 统计/优化保证控制的是 population excess，还是仅训练 loss。
- [ ] bounded-loss 泛化定理若需要 clipping，把 clipping approximation bias 保留。
- [ ] 多类别、序列生成、结构损失或下游任务另证对应 calibration function。

## 1. 直觉：训练用柔软刻度，评价用对错开关

分类错误只看跨没跨过 $1/2$；交叉熵还处罚错误的置信度。训练时它更容易优化，但要说明这个柔软刻度变好，为什么能带来“对错开关”变好。

下面的桥是 quantitative 的：不只说 loss 合理，还给出两个 excess risk 之间的明确关系。

## 2. 条件交叉熵的最优值

固定 $x$，记 $\eta=\eta(x)$。条件 log risk 为
$-\eta\log p-(1-\eta)\log(1-p)$，最优值为 Bernoulli entropy $H(\eta)$。其差正好是

$$
\eta\log\frac\eta p+(1-\eta)\log\frac{1-\eta}{1-p}
=\mathop{\mathrm{KL}}(\mathop{\mathrm{Ber}}(\eta)\Vert\mathop{\mathrm{Ber}}(p)).
$$

积分得到 $R_{log}(p)-R_{log}^*=\mathbb E\mathop{\mathrm{KL}}(\mathop{\mathrm{Ber}}(\eta)\Vert\mathop{\mathrm{Ber}}(p))$。
在 $\eta=0,1$ 处用 $0\log0=0$ 与极限；Bayes reference 可作为 inf，不要求 finite logits 恰好实现边界概率。

## 3. 条件分类 excess 的精确形式

Bayes 决策是 $h_\ast=1\lbrace\eta\ge1/2\rbrace$；不同决策的额外错误率为
$|2\eta-1|1\lbrace h_p\ne h_\ast\rbrace$。
若决策不同， $p$ 与 $\eta$ 位于阈值两侧，所以 $|\eta-1/2|\le|p-\eta|$，从而

$$
R_{01}(h_p)-R_{01}^*\le2\mathbb E|p-\eta|.
$$

## 4. Bernoulli KL 下界与完整桥梁

固定 $p$，把 KL 当作 $q\in(0,1)$ 的函数。它在 $q=p$ 处值与一阶导均为 0，二阶导为
$1/q+1/(1-q)=1/[q(1-q)]\ge4$。Taylor 积分给出
$\mathop{\mathrm{KL}}(\mathop{\mathrm{Ber}}(q)\Vert\mathop{\mathrm{Ber}}(p))\ge2(q-p)^2$；端点取极限。

于是 Cauchy–Schwarz 给出

$$
R_{01}(h_p)-R_{01}^\ast
\le2\sqrt{\mathbb E(p-\eta)^2}
\le\sqrt{2(R_{log}(p)-R_{log}^\ast)}.
$$

这个 Bernoulli 证明不需要把一般 Pinsker 不等式留成黑盒。

## 5. 与 T32 合成真正的学习结论

若 [T32](T32-excess-risk-decomposition.md) 已得到总体 log-loss excess $\le a+2b+c$，其中 $a$ 是相对 Bayes 的模型误差、 $b$ 是统一偏差、 $c$ 是经验优化 gap，则同一事件上分类 excess $\le\sqrt{2(a+2b+c)}$。

若使用 $p\in[\kappa,1-\kappa]$、 $0<\kappa<1/2$ 使 log loss 有界，令 $\eta_\kappa$ 为裁剪后的 Bayes 概率。裁剪导致的 log excess 至多 $-\log(1-\kappa)$：对 $\eta<\kappa$，条件 KL 关于 $\eta$ 凸，区间最大值在 0 或 $\kappa$，分别为 $-\log(1-\kappa)$ 与 0；另一端同理。该项必须计入 $a$。

语言模型 token cross-entropy 的改善不自动给任务成功率、推理能力或用户偏好保证；目标 law 和 loss 改变后，仍需自己的桥。

## 前置、关联与证据

- [交叉熵与 KL](<../../Math 基础/概率统计/信息论基础：熵、交叉熵与 KL 散度.md>) · [T32](T32-excess-risk-decomposition.md) · [T33](T33-uniform-convergence.md) · [T22](../evaluation-monitoring/T22-ranking-proper-scoring.md)。
- [Bartlett–Jordan–McAuliffe：Convexity, Classification, and Risk Bounds](https://www.stat.berkeley.edu/~jordan/638.pdf)：一般 surrogate calibration 的原始框架。本卡自包含 binary log-loss 原型。
- [DL 数学综述本地卡](../../proof_ref/dl-core-2026-09/the-modern-mathematics-of-deep-learning-2105.04026/README.md)。
