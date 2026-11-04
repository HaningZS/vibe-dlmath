---
id: T16
type: proof-template
refined: 2026-09-28
status: "refined + claim-checked"
---

# T16. Heavy-tailed noise + clipping high-probability proof

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

把裁剪梯度分成 centered martingale 与 clipping bias。

## 复用契约

**输入对象**：完整 g_t、裁剪定义、可预测阈值、p 阶矩与梯度界。

**输出结论**：bias–martingale 分解；期望下降公式不是已完成的高概率收敛定理。

**必需假设**：

- 条件零均值噪声和明确 p>1 矩界。
- 阈值不读当前梯度；gradient bound 或 full-gradient moment 有证明。
- 高概率下降中的可预测内积 martingale 需 increment/variation 界。

**失败例子**：噪声以 0.1 概率取 9、0.9 概率取 -1，均值为零；阈值 1 裁剪后的均值为 -0.8。

## 实例化时必须完成

- [ ] 裁剪可观测完整梯度后重新中心化。
- [ ] 分别界 bias、波动和二阶项。
- [ ] 在同一事件上闭合阈值/梯度条件。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [集中不等式、MGF、鞅与自归一化过程](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E9%9B%86%E4%B8%AD%E4%B8%8D%E7%AD%89%E5%BC%8F%E3%80%81MGF%E3%80%81%E9%9E%85%E4%B8%8E%E8%87%AA%E5%BD%92%E4%B8%80%E5%8C%96%E8%BF%87%E7%A8%8B.md) · [测度、条件期望、滤过与适应过程](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%B5%8B%E5%BA%A6%E3%80%81%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E3%80%81%E6%BB%A4%E8%BF%87%E4%B8%8E%E9%80%82%E5%BA%94%E8%BF%87%E7%A8%8B.md)

## 适用场景

LLM training、RLHF、人类反馈、LLM judge、simulator outlier、Adam/AdaGrad under noisy gradients。噪声不是 sub-Gaussian，只能假设有限 p-th moment。

## 核心 decomposition

令 $x_t$ 为 $\mathcal F_t$-可测，并写

$$
g_t=\nabla f(x_t)+\xi_t,
\qquad
\mathbb E[\xi_t\mid\mathcal F_t]=0,
\qquad
\mathbb E[\|\xi_t\|^p\mid\mathcal F_t]\le\sigma^p,
\quad p>1.
$$

阈值 $\tau_t$ 必须是可预测的（ $\mathcal F_t$-可测）。明确采用 radial clipping：

$$
\operatorname{clip}(v,\tau)=v\min\left\{1,\frac{\tau}{\|v\|}\right\},
\qquad
\widetilde g_t=\operatorname{clip}(g_t,\tau_t).
$$

约定 $\operatorname{clip}(0,\tau)=0$，并要求 $g_t,\widetilde g_t$ 为 $\mathcal F_{t+1}$-可测；这样下面的 $m_t$ 才是相对 $(\mathcal F_t)$ 的 martingale difference。

算法实际裁剪的是完整 stochastic gradient $g_t$，而不是不可观测噪声 $\xi_t$。适合 martingale 分析的精确分解是

$$
\widetilde g_t-\nabla f(x_t)
=
\underbrace{\widetilde g_t-\mathbb E[\widetilde g_t\mid\mathcal F_t]}_{m_t\text{: centered martingale difference}}
+
\underbrace{\mathbb E[\widetilde g_t\mid\mathcal F_t]-\nabla f(x_t)}_{b_t\text{: clipping bias}}.
$$

其中 $\|m_t\|\le2\tau_t$，可以结合条件方差使用 Freedman/Bernstein 型 martingale 界。偏差必须单独控制：若直接假设 $\mathbb E[\|g_t\|^p\mid\mathcal F_t]\le G_p^p$，则

$$
\|b_t\|
\le
\mathbb E[\|g_t\|\mathbf 1\{\|g_t\|>\tau_t\}\mid\mathcal F_t]
\le
\frac{G_p^p}{\tau_t^{p-1}}.
$$

若只有噪声矩界，则还需一个可预测的 gradient 上界 $\|\nabla f(x_t)\|\le G_t<\tau_t$；此时由 $\|g_t\|>\tau_t\Rightarrow\|\xi_t\|>\tau_t-G_t$ 可得相应的 $O(\sigma^p/(\tau_t-G_t)^{p-1})$ 偏差控制。没有 $G_t$ 或 localization argument 时，不能只用噪声尾界声称 clipping bias 已受控。

对 $L$-smooth $f$ 与更新 $x_{t+1}=x_t-\eta\widetilde g_t$，条件期望的一步界可写为

$$
\mathbb E[f(x_{t+1})\mid\mathcal F_t]
\le
f(x_t)-\eta\|\nabla f(x_t)\|^2
-\eta\langle\nabla f(x_t),b_t\rangle
+\frac{L\eta^2}{2}\mathbb E[\|\widetilde g_t\|^2\mid\mathcal F_t].
$$

再用 $\|\widetilde g_t\|\le\tau_t$ 与 Young 不等式，得到可接入 Lyapunov/telescoping 的版本

$$
\mathbb E[f(x_{t+1})\mid\mathcal F_t]
\le
f(x_t)-\frac\eta2\|\nabla f(x_t)\|^2
+\frac\eta2\|b_t\|^2
+\frac{L\eta^2\tau_t^2}{2}.
$$

<a id="t16-clipping-decomposition"></a>

^t16-clipping-decomposition

## 逐步证明模板

### 要对哪一个 martingale 应用概率界

在下降分析中，常见对象是标量
$Z_t=\langle\nabla f(x_t),m_t\rangle$，其中前一个因子对 $\mathcal F_t$ 可测。若已证明
$\|\nabla f(x_t)\|\leq G_t$，则

$$
\mathbb E[Z_t\mid\mathcal F_t]=0,\qquad
|Z_t|\leq2G_t\tau_t,
$$

并需计算或上界 $\sum_t\mathbb E[Z_t^2\mid\mathcal F_t]$。这才是接入标量 Freedman 的对象；直接控制向量范数时，应采用对应的向量/矩阵浓缩工具并报告维度依赖。

本卡前面的条件期望 descent 只是一条中间式。要声称高概率收敛，还须将未取期望的下降不等式、martingale 界、bias 界和安全区闭合放在同一事件中。

```text
Step 1. 定义 filtration、条件均值零噪声和条件 p 阶矩；写明 p 的范围。
Step 2. 定义 radial 或 coordinate-wise clipping，并令 threshold predictable。
Step 3. 把完整 clipped gradient 减去其条件期望，得到 centered martingale difference m_t。
Step 4. 用 Freedman/Bernstein 控制 m_t；不能对未中心化的 clipped noise 直接套 martingale bound。
Step 5. 用 full-gradient moment，或 gradient localization + noise moment，控制 bias b_t。
Step 6. 选择 tau_t 平衡 martingale fluctuation、bias 与 optimization descent。
Step 7. 把 m_t+b_t 塞进 descent / Lyapunov，并在同一 good event 上闭合 trajectory bound。
Step 8. 显式写出 delta、步数、维数/范数和初始 gap 的依赖。
```

## 关键不等式形状

条件矩界蕴含条件 tail probability：

$$
\mathbb{P}(\|\xi_t\|>\tau\mid\mathcal F_t)
\le
\frac{\sigma^p}{\tau^p}.
$$

以及（ $p>1$）

$$
\mathbb{E}[\|\xi_t\|\mathbf{1}\{\|\xi_t\|>\tau\}\mid\mathcal F_t]
\le
\frac{\sigma^p}{\tau^{p-1}}.
$$

这两个式子只控制噪声尾部；它们本身不等于完整 $g_t$ 的 clipping bias bound。

## 常见坑

- clipping 会引入 bias，不能只说方差变小。
- 必须区分 radial clipping 与 coordinate-wise clipping；对应范数、维数依赖和 bias 不同。
- naive clipping 在 composite/distributed setting 可能破坏 fixed point，需要 clip gradient difference 或特殊设计。
- high-probability bound 需要重新中心化并处理 confidence parameter；Markov tail bound 不能替代整段 martingale concentration。

## 来源论文 / 参考

- High-Probability Convergence for Composite and Distributed Stochastic Minimization and Variational Inequalities with Heavy-Tailed Noise, ICML 2024. https://proceedings.mlr.press/v235/gorbunov24a.html
- Clipping Improves Adam-Norm and AdaGrad-Norm when the Noise Is Heavy-Tailed, ICML 2025. https://proceedings.mlr.press/v267/chezhegov25a.html
- 本地 PDF/TeX：[核验笔记](../../proof_ref/core-theory-2026-09/clipping-improves-adam-norm-and-adagrad-norm-when-2406.04443/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md) · [PDF](../../proof_ref/core-theory-2026-09/clipping-improves-adam-norm-and-adagrad-norm-when-2406.04443/paper.pdf#page=5)
- `Convergence of Clipped-SGD for Convex (L0,L1)-Smooth Optimization with Heavy-Tailed Noise` 目前只作为待核对 intake 条目；在确认最终录用与 camera-ready 版本前不作为“已收录”证据。

## 关联模板与本地证据

- [T01：把单步目标下降累积成平均梯度平方界。](T01-descent.md)
- [T02：给辅助状态误差记账，让联合势函数下降。](T02-lyapunov.md)
- [T15：曲率随梯度变化时，先证明局部下降和轨迹闭合。](T15-generalized-smoothness.md)

通用证明工具：P03、P04、P07；见 [证明原语](../../通用证明原语.md)。

- [Clipping Improves Adam-Norm and AdaGrad-Norm when the Noise Is Heavy-Tailed](../../proof_ref/core-theory-2026-09/clipping-improves-adam-norm-and-adagrad-norm-when-2406.04443/README.md) · [官方 arXiv](https://arxiv.org/abs/2406.04443)

## 专项证明接口（2026-10-02）

- [T46：显式计算 Gaussian RDP、条件组合和 DP 转换，区分裁剪对象与采样。](../statistics/T46-gaussian-privacy-accounting.md)

## 经典与近期证明蒸馏

- [经典下降证明的偏差与方差接口](../../extensions/%E7%BB%8F%E5%85%B8%E4%B8%8B%E9%99%8D%E8%AF%81%E6%98%8E%E7%9A%84%E5%81%8F%E5%B7%AE%E4%B8%8E%E6%96%B9%E5%B7%AE%E6%8E%A5%E5%8F%A3.md)
