---
id: T13
type: proof-template
refined: 2026-10-20
status: "refined + claim-checked"
---

# T13. Diffusion sampler error decomposition in one chosen metric

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

在同一度量中组合连续过程、学习与离散采样误差。

## 复用契约

**输入对象**：目标 law、ideal/learned process、离散算法、时间和最终 metric。

**输出结论**：选定过程/度量下的误差分解；训练 score loss 小本身不保证采样分布准。

**必需假设**：

- 度量与可转换条件明确。
- Girsanov 条件、diffusion coefficient 与初始化差不能省略。
- ODE、CTMC、consistency、FM 各用合法桥梁。

**失败例子**：未经矩或支持条件，TV 误差不能直接改成 Wasserstein 误差。

## 实例化时必须完成

- [ ] 定义各中间 law 和比较方向。
- [ ] 保留时间权重、采样 law 与初始误差。
- [ ] 只在同一 metric 合并。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [ODE、SDE 与连续时间生成模型](../../Math%20%E5%9F%BA%E7%A1%80/%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/ODE%E3%80%81SDE%20%E4%B8%8E%E8%BF%9E%E7%BB%AD%E6%97%B6%E9%97%B4%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B.md) · [Grönwall、Duhamel 与稳定性误差传播](../../Math%20%E5%9F%BA%E7%A1%80/%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/Gr%C3%B6nwall%E3%80%81Duhamel%20%E4%B8%8E%E7%A8%B3%E5%AE%9A%E6%80%A7%E8%AF%AF%E5%B7%AE%E4%BC%A0%E6%92%AD.md) · [统计距离、Le Cam、Fano、Assouad 与 Yao 下界](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E7%BB%9F%E8%AE%A1%E8%B7%9D%E7%A6%BB%E3%80%81Le%20Cam%E3%80%81Fano%E3%80%81Assouad%20%E4%B8%8E%20Yao%20%E4%B8%8B%E7%95%8C.md)

## 适用场景

连续 score-based diffusion 或离散 diffusion sampler 的收敛证明。SDE diffusion、probability-flow ODE、consistency model、flow matching 和离散 CTMC **不是同一个定理**；先选过程和最终误差度量，再选工具。

## 核心 decomposition

不定义 `GenError`，也不把 $L^2$ score error、path KL、TV 和 Wasserstein 直接相加。固定目标度量，例如 total variation：

$$
\operatorname{TV}(p_0,\widehat p_0^{\mathrm{disc}})
\le
\operatorname{TV}(p_0,p_0^{\mathrm{ideal}})
+\operatorname{TV}(p_0^{\mathrm{ideal}},\widehat p_0^{\mathrm{cont}})
+\operatorname{TV}(\widehat p_0^{\mathrm{cont}},\widehat p_0^{\mathrm{disc}}).
$$

三项分别对应 terminal/early-stopping mismatch、连续过程的 drift/score estimation error、以及 discretization error。所有项已经处于同一 metric。

若 learned 与 ideal reverse SDE 从**同一个初始 law** 出发、具有相同且在相关子空间上可逆/非退化的 diffusion coefficient，并满足绝对连续、可积性和 Novikov/Girsanov 条件，可先在 path space 上得到

$$
D_{\mathrm{KL}}(\mathbb P\,\|\,\widehat{\mathbb P})
=
\frac12\,
\mathbb E_{\mathbb P}\int_0^T
\|g_t^{-1}(b_t-\widehat b_t)(X_t)\|_2^2\,dt.
$$

若两条路径的初始 laws 分别为 $\nu$ 与 $\widehat\nu$，右侧还要加 $D_{\mathrm{KL}}(\nu\|\widehat\nu)$，不能省略 initialization mismatch。

再由 data processing 控制同一方向上的终点 marginal KL。记终点 laws 为 $\nu_T,\widehat\nu_T$，由 Pinsker：

$$
\operatorname{TV}(\nu_T,\widehat\nu_T)
\le
\sqrt{\tfrac12 D_{\mathrm{KL}}(\nu_T\|\widehat\nu_T)}
\le
\sqrt{\tfrac12 D_{\mathrm{KL}}(\mathbb P\|\widehat{\mathbb P})}.
$$

如果最终目标是 Wasserstein，可以用 coupling/stability 直接推导，也可以使用已核对假设、方向和常数的 transport-entropy 转换。不能把 Pinsker 得到的 TV 项无条件替换成 Wasserstein 项。

例如，在固定 ground metric 上，若参照分布 $Q$ 已被证明满足 $T_2(C)$，即对所需的 $P$ 有

$$
W_2^2(P,Q)\le 2C\,D_{\mathrm{KL}}(P\|Q),
$$

那么同一方向的有限 marginal KL 界 $D_{\mathrm{KL}}(P\|Q)\le\epsilon$ 就给出 $W_2(P,Q)\le\sqrt{2C\epsilon}$。这里 $T_2(C)$ 是额外需要核验的分布性质，不由“存在密度”或 score loss 小自动得到；还要检查所用空间、矩条件和常数依赖。

特别是，上面的 Girsanov 路线给出 ideal $P$ 相对 learned $Q$ 的 KL。要这样转换，必须掌握 learned $Q$ 的对应 $T_2$ 性质；只有 ideal $P$ 的性质时，通常需要反方向 $D_{\mathrm{KL}}(Q\|P)$，不能把 KL 的参数交换。这条接口只陈述有条件的转换，不声称任意目标或学习分布都满足 $T_2$。前置见 [Wasserstein 距离](<../../Math 基础/概率统计/最优传输与 Wasserstein 距离.md>)。

## 逐步证明模板

```text
Step 1. 固定 forward process、reverse process、初末时间和最终 metric。
Step 2. 定义 ideal reverse process 与 learned continuous reverse process，写清 drift 和 diffusion coefficient。
Step 3. 选择合法桥梁：Girsanov→path KL→marginal KL→Pinsker，coupling→Wasserstein，或核验过方向与假设的 KL→Wasserstein 转换。
Step 4. 将 score/drift estimation assumption 精确代入桥梁定理的积分权重。
Step 5. 单独比较 learned continuous process 与具体离散算法，给出步长、regularity 与累积误差。
Step 6. 单独控制 terminal Gaussian approximation、early stopping 或 initialization mismatch。
Step 7. 只在同一 metric 下用 triangle inequality 合并。
Step 8. 最后优化时间截断、步长和 score sample size；不要先把异质量纲项写成形式化加法。
```

## 常见数学工具

- SDE / ODE discretization。
- Girsanov theorem。
- Fokker-Planck equation。
- Markov chain coupling。
- Gronwall inequality。
- KL-to-TV conversion。
- Wasserstein stability。

## 离散 diffusion 变体

discrete diffusion 常把过程写成 CTMC。其 proof 通常使用 transition-kernel KL chain rule、Poisson/tau-leaping error 或 coupling，不能直接复制连续 SDE 的 Girsanov 公式：

$$
X_t \sim \text{continuous-time Markov chain}.
$$

证明重点变成：

```text
true reverse CTMC
vs learned reverse CTMC
vs discrete-time tau-leaping / approximate sampler
```

consistency model 又是独立的统计估计问题；先定义其 distribution discrepancy 和函数类，再讨论 estimation/approximation rate。

## 来源论文 / 参考

- Theory of Consistency Diffusion Models: Distribution Estimation Meets Fast Sampling, ICML 2024. https://proceedings.mlr.press/v235/dou24a.html
- Accelerating Convergence of Score-Based Diffusion Models, Provably, ICML 2024. https://proceedings.mlr.press/v235/li24ad.html
- O(d/T) Convergence Theory for Diffusion Probabilistic Models under Minimal Assumptions, ICLR 2025. https://openreview.net/forum?id=4EjdYiNRzE
- 本地核验：[O(d/T) 核验卡](../../proof_ref/core-theory-2026-09/o-d-t-convergence-theory-for-diffusion-probabilistic-2409.18959/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md) · [PDF](../../proof_ref/core-theory-2026-09/o-d-t-convergence-theory-for-diffusion-probabilistic-2409.18959/paper.pdf#page=4)
- Consistency model 本地核验：[reference](../../proof_ref/core-theory-2026-09/provable-statistical-rates-for-consistency-diffusion-models-2406.16213/README.md) · [PDF](../../proof_ref/core-theory-2026-09/provable-statistical-rates-for-consistency-diffusion-models-2406.16213/paper.pdf#page=5)
- Convergence of Score-Based Discrete Diffusion Models, ICLR 2025. https://openreview.net/forum?id=pq1WUegkza
- Flow PDE/Duhamel 核验：[核验笔记](../../proof_ref/recent-accepted-2025-2026/improving-flow-matching-by-aligning-flow-divergence-2602.00869/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md) · [PDF](../../proof_ref/recent-accepted-2025-2026/improving-flow-matching-by-aligning-flow-divergence-2602.00869/paper.pdf#page=5)

## 关联模板与本地证据

- [T10：分开控制极限动力学优化误差与有限粒子近似误差。](../deep-learning/T10-mean-field.md)
- [T19：先指定 joint/label 条件，再把 transport cost 连接到风险差。](T19-transport-risk.md)

通用证明工具：P05、P07；见 [证明原语](../../通用证明原语.md)。

- [Score-Based Generative Modeling through Stochastic Differential Equations](../../proof_ref/foundations-2026-09/score-based-generative-modeling-through-stochastic-differential-equations-2011.13456/README.md) · [官方 arXiv](https://arxiv.org/abs/2011.13456)
- [Sampling is as easy as learning the score: theory for diffusion models with minimal data assumptions](../../proof_ref/foundations-2026-09/sampling-is-as-easy-as-learning-the-score-2209.11215/README.md) · [官方 arXiv](https://arxiv.org/abs/2209.11215)
- [Flow Matching for Generative Modeling](../../proof_ref/foundations-2026-09/flow-matching-for-generative-modeling-2210.02747/README.md) · [官方 arXiv](https://arxiv.org/abs/2210.02747)
- [O(d/T) Convergence Theory for Diffusion Probabilistic Models under Minimal Assumptions](../../proof_ref/core-theory-2026-09/o-d-t-convergence-theory-for-diffusion-probabilistic-2409.18959/README.md) · [官方 arXiv](https://arxiv.org/abs/2409.18959)

## 经典与近期证明蒸馏

- [T51：在真实边缘分布下控制速度误差，用学习场 Lipschitz 与耦合推出 Wasserstein 界。](T51-flow-trajectory-error.md)
- [流形扩散来源问题审计：保留未闭合项](../../proof_ref/proof-distillation-2026-10/sharp-convergence-and-sampling-trade-offs-for-riemannian-2609.36568/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md)
