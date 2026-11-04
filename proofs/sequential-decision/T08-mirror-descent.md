---
id: T08
type: proof-template
refined: 2026-09-28
status: "refined + claim-checked"
---

# T08. Mirror descent / Bregman / KL geometry

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

用三点恒等式与 Bregman 几何分析在线/策略更新。

## 复用契约

**输入对象**：凸域、mirror map ψ、对偶范数、步长、comparator 与 state weighting。

**输出结论**：线性化损失的 Bregman 界；非凸网络或 on-policy 改善需要额外连接。

**必需假设**：

- ψ 相对指定范数 σ-strongly convex，argmin 存在且迭代合法。
- 变步长保留额外差分项。
- policy KL 的方向、共同支持与状态分布清楚；regret 需凸 loss/有效次梯度。

**失败例子**：把变化的 1/η_t 当常数提出 telescope 会漏掉 divergence 的差分项。

## 实例化时必须完成

- [ ] 从最优性条件推三点不等式。
- [ ] 使用正确 σ 与对偶范数。
- [ ] 区分分布更新、参数训练与 occupancy 变化。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [Bregman 散度、Mirror Descent 与在线学习](../../Math%20%E5%9F%BA%E7%A1%80/%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/Bregman%20%E6%95%A3%E5%BA%A6%E3%80%81Mirror%20Descent%20%E4%B8%8E%E5%9C%A8%E7%BA%BF%E5%AD%A6%E4%B9%A0.md) · [绝对连续/共同支撑](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%B5%8B%E5%BA%A6%E3%80%81%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E3%80%81%E6%BB%A4%E8%BF%87%E4%B8%8E%E9%80%82%E5%BA%94%E8%BF%87%E7%A8%8B.md#11-%E7%BB%9D%E5%AF%B9%E8%BF%9E%E7%BB%AD%E4%B8%8E-radonnikodym-derivative)

## 适用场景

online convex optimization、policy optimization、RLHF、DPO、preference learning、distributional update、recommendation policy update。

## 核心不等式

设 $\mathcal X$ 闭且凸、 $u\in\mathcal X$， $\psi$ 在其有效域相对内部可微并相对范数 $\|\cdot\|$ 为 $\sigma$-strongly convex；假设下面的 argmin 存在且迭代留在 Bregman 有效域。记 $D_\psi$ 为 Bregman divergence， $\|\cdot\|_\ast$ 为对偶范数。对常步长 $\eta>0$，Online Mirror Descent 更新：

$$
x_{t+1}
=
\arg\min_{x\in\mathcal{X}}
\left\{
\eta\langle g_t,x\rangle + D_\psi(x,x_t)
\right\}.
$$

由最优性条件、three-point identity 和 Young 不等式得到

$$
\langle g_t, x_t-u\rangle
\le
\frac{D_\psi(u,x_t)-D_\psi(u,x_{t+1})}{\eta}
+
\frac{\eta}{2\sigma}\|g_t\|_\ast^2.
$$

求和后 Bregman term 在**常步长**下 telescope：

$$
\sum_{t=1}^T \langle g_t,x_t-u\rangle
\le
\frac{D_\psi(u,x_1)}{\eta}
+
\frac{\eta}{2\sigma}\sum_{t=1}^T\|g_t\|_\ast^2.
$$

若 $\eta_t$ 随时间变化，则 $D_\psi(u,x_t)/\eta_t$ 会产生额外差分项；不能继续照抄上式。

<a id="t08-omd-bound"></a>

^t08-omd-bound

## KL policy update

在有限 action simplex 上，negative entropy 的 Bregman divergence 是 KL。对 policy，正则项通常还要在某个明确的 state distribution $d$ 下加权：

$$
D_\psi(\pi,\pi_t)
=
\mathbb E_{s\sim d}\!\left[\operatorname{KL}\bigl(\pi(\cdot\mid s)\|\pi_t(\cdot\mid s)\bigr)\right].
$$

若各状态上 reference policy 的支撑覆盖候选 policy，policy update 可写成

$$
\pi_{t+1}
=
\arg\max_\pi
\left[
\mathbb E_{s\sim d,a\sim\pi(\cdot\mid s)}\widehat r_t(s,a)
-
\frac{1}{\eta}\mathbb E_{s\sim d}\operatorname{KL}(\pi(\cdot\mid s)\|\pi_t(\cdot\mid s))
\right].
$$

这里 $d$ 是固定分布、当前 occupancy 还是新 policy 的 occupancy，会改变优化问题与证明。离散 action、逐状态可分且 $d$ 固定时才有熟悉的 exponentiated update。

## 逐步证明模板

```text
Step 1. 找到问题的自然几何：L2 / simplex / probability distribution / policy。
Step 2. 选择 mirror map psi。
Step 3. 把 update 写成 linearized loss + Bregman penalty。
Step 4. 用一阶最优性条件推出 three-point inequality。
Step 5. 对 t 求和，Bregman divergence telescope。
Step 6. 加入 stochastic estimation error / bonus / KL reference penalty。
Step 7. 整理 regret 或 policy improvement bound。
```

## 可迁移用法

- DPO/RLHF：在 reference policy、Bradley--Terry 偏好模型及指数倾斜最优策略等条件下，可把特定目标联系到 KL-regularized reward maximization。
- OPD：teacher-student distribution matching 可写成 KL geometry。
- 推荐闭环：用户 exposure policy update 可写成 mirror update。
- memory agent：Bayesian update 与 entropic mirror descent 只在匹配的 likelihood/loss 选择下等价，不能仅凭形式相似宣称。

## 常见坑

- KL 方向很重要：`KL(pi || ref)` 与 `KL(ref || pi)` 给出不同 geometry。
- 必须写明 mirror map 的 strong-convexity 常数和所用范数；否则二次项常数错误。
- policy KL 必须逐状态定义并说明 state weighting、共同支撑集和绝对连续性。
- 如果 action space 连续，KL update 的闭式形式可能不存在。
- DPO 的 loss 不等于任意 preference loss；其等价推导依赖 reference policy 与偏好模型。

## 来源论文 / 参考

- Online Learning and Online Convex Optimization, Shalev-Shwartz. https://www.cs.huji.ac.il/~shais/papers/OLsurvey.pdf
- Follow-the-Regularized-Leader and Mirror Descent, AISTATS 2011. https://proceedings.mlr.press/v15/mcmahan11b.html
- Direct Preference Optimization: Your Language Model is Secretly a Reward Model, NeurIPS 2023. https://openreview.net/forum?id=HPuSIXJaa9
- 本地 DPO PDF/TeX：[核验笔记](../../proof_ref/core-theory-2026-09/direct-preference-optimization-your-language-model-is-secretly-2305.18290/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md) · [PDF](../../proof_ref/core-theory-2026-09/direct-preference-optimization-your-language-model-is-secretly-2305.18290/paper.pdf#page=3)
- Iterative Preference Learning from Human Feedback: Bridging Theory and Practice for RLHF under KL-Constraint, ICML 2024. https://arxiv.org/abs/2312.11456
- Online Iterative Reinforcement Learning from Human Feedback, NeurIPS 2024. https://proceedings.neurips.cc/paper_files/paper/2024/file/94d13c2401fe119e57ba325b6fe526e0-Paper-Conference.pdf
- Logarithmic Regret for Online KL-Regularized Reinforcement Learning, ICML 2025. https://proceedings.mlr.press/v267/zhao25ac.html
- 近期 OMD 适用边界：[README](../../proof_ref/core-theory-2026-09/the-hidden-cost-of-approximation-in-online-mirror-2511.22283/README.md) · [PDF](../../proof_ref/core-theory-2026-09/the-hidden-cost-of-approximation-in-online-mirror-2511.22283/paper.pdf#page=4)

## 关联模板与本地证据

- [T05：分开使用 PAC-Bayes 高概率界和互信息期望界。](../generalization/T05-pac-bayes-information.md)
- [T07：在正确策略的 occupancy 下展开 Bellman 价值误差。](T07-bellman.md)

通用证明工具：P02、P06；见 [证明原语](../../通用证明原语.md)。

- [Convex Optimization: Algorithms and Complexity](../../proof_ref/foundations-2026-09/convex-optimization-algorithms-and-complexity-1405.4980/README.md) · [官方 arXiv](https://arxiv.org/abs/1405.4980)
- [Direct Preference Optimization: Your Language Model is Secretly a Reward Model](../../proof_ref/core-theory-2026-09/direct-preference-optimization-your-language-model-is-secretly-2305.18290/README.md) · [官方 arXiv](https://arxiv.org/abs/2305.18290)
- [Iterative Preference Learning from Human Feedback: Bridging Theory and Practice for RLHF under KL-Constraint](../../proof_ref/core-theory-2026-09/iterative-preference-learning-from-human-feedback-bridging-theory-2312.11456/README.md) · [官方 arXiv](https://arxiv.org/abs/2312.11456)
