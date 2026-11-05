---
id: T11
type: proof-template
refined: 2026-09-28
status: "refined-contextual"
---

# T11. Doubly robust / orthogonal decomposition

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

用残差校正把 nuisance 的一阶误差变成乘积余项。

## 复用契约

**输入对象**：真实/估计 propensity、目标 π、outcome m 与对应 held-out fold。

**输出结论**：contextual score 的精确 product-bias identity；CLT/root-n/高概率需要额外速率和矩条件。

**必需假设**：

- 真实 e 和估计 e_hat 在目标支持上为正；权重/可积性受控。
- 目标 policy π 预先固定，或与 nuisance 一起仅由独立 fit 数据选定。
- 单个 held-out score 只条件于它对应的独立 policy/nuisance fit。
- 因果解释另需识别假设；序列 RL 另写 horizon recursion。

**失败例子**：真实 e>0 不保证估计 e_hat>0；分母为零时估计器没有定义。

## 实例化时必须完成

- [ ] 写目标与 joint law 后算条件期望。
- [ ] 逐 fold 管理依赖，不把交叉拟合 score 全部当条件独立。
- [ ] clipping weights 的新增 bias 单列。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [条件期望的投影直觉](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%B5%8B%E5%BA%A6%E3%80%81%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E3%80%81%E6%BB%A4%E8%BF%87%E4%B8%8E%E9%80%82%E5%BA%94%E8%BF%87%E7%A8%8B.md#7-%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E4%B8%8D%E6%98%AF%E6%8A%8A%E6%9D%A1%E4%BB%B6%E4%BB%A3%E8%BF%9B%E5%8E%BB) · [算法稳定性、经验过程与 PAC-Bayes](../../Math%20%E5%9F%BA%E7%A1%80/%E7%BB%9F%E8%AE%A1%E5%AD%A6%E4%B9%A0%E7%90%86%E8%AE%BA/%E7%AE%97%E6%B3%95%E7%A8%B3%E5%AE%9A%E6%80%A7%E3%80%81%E7%BB%8F%E9%AA%8C%E8%BF%87%E7%A8%8B%E4%B8%8E%20PAC-Bayes.md)

## 适用场景

off-policy evaluation、contextual bandit、causal inference、logged data、agent evaluation、recommendation evaluation。

## Contextual-bandit estimator

设 logged data $Z_i=(X_i,A_i,Y_i)$ 独立同分布，behavior propensity 为 $e(a\mid x)$，目标 policy 可随机选择动作，记为 $\pi(a\mid x)$；令 $m(x,a)=\mathbb E[Y\mid X=x,A=a]$。要求 target support 上 positivity： $e(a\mid x)>0$。目标 $V(\pi)=\mathbb E_X\sum_a\pi(a\mid X)m(X,a)$。

本节先考虑预先固定的 $\pi$，或只使用独立 fit 数据训练出的 $\pi$。用独立训练样本或 cross-fitting 得到 nuisance estimates $\widehat m,\widehat e$；**policy 与 nuisance 都必须和用于评估它们的 held-out observation 分离**。允许 policy 对动作随机化，不等于允许它读取该条评估数据的 reward 后再选动作。

对 stochastic target policy，DR estimator 是

$$
\widehat V_{DR}
=\frac{1}{n}\sum_{i=1}^n
\left[
\sum_a\pi(a\mid X_i)\widehat m(X_i,a)
+\frac{\pi(A_i\mid X_i)}{\widehat e(A_i\mid X_i)}
\bigl(Y_i-\widehat m(X_i,A_i)\bigr)
\right].
$$

确定性 target policy 是 $\pi(a\mid x)=\mathbf1\lbrace a=\pi(x)\rbrace$ 的特例；不能把随机 policy 直接写成单个 $\widehat m(x,\pi(x))$。

## 核心性质

对某个 held-out observation，令 $\mathcal F_{fit}$ 包含**用于它的独立训练数据与拟合随机性**，使 $\pi,\widehat m,\widehat e$ 都由它确定；held-out observation 独立于 $\mathcal F_{fit}$。条件于 $\mathcal F_{fit}$，并要求目标支持上 $\widehat e(a\mid x)>0$，可得单个 score 的精确 bias identity：

$$
\mathbb E[\widehat\phi_{DR}\mid\mathcal F_{fit}]-V(\pi)
=\mathbb E_X\sum_a\pi(a\mid X)
\bigl(\widehat m(X,a)-m(X,a)\bigr)
\left(1-\frac{e(a\mid X)}{\widehat e(a\mid X)}\right).
$$

右侧 $\mathbb E_X$ 对新 $X$ 积分，拟合对象在该条件下视为固定。因此，在 positivity/可积性条件下，若 $\widehat m=m$ 或 $\widehat e=e$，bias 为零；两者都近似时，剩余项是两个 nuisance errors 的乘积。有限样本 high-probability/渐近正态结论还需权重有界、函数范数、cross-fitting 与经验过程/矩条件。

若第 $k$ 个 fold 评估的是独立训练出的 $\pi_k$，按 fold 组合后的对应目标是 $\sum_k(n_k/n)V(\pi_k)$。这些 policies 可能不同；这不是自动针对最后用全部数据训练的单个 $\pi_{final}$ 的价值保证。

<a id="t11-contextual-dr"></a>

^t11-contextual-dr

## 逐步证明模板

```text
Step 1. 写 joint data law、behavior e、target pi、outcome model m、positivity 与精确目标 V(pi)。
Step 2. 用 sample splitting/cross-fitting 训练 m_hat、e_hat；若 pi 也学习，同样排除对应 held-out 数据，并标明每个 fold 的依赖关系。
Step 3. 写 stochastic-policy plug-in 与 importance-weighted residual。
Step 4. 条件在独立的 policy/nuisance fit 信息上计算 expectation，推出上面的 product-bias identity。
Step 5. 用 overlap 把 1/e_hat 控制住，并选择明确的 L2/Linfty norm 上界 product term。
Step 6. 对 centered influence-function term 使用 i.i.d. concentration/CLT；adaptive log data 则改用 martingale 工具。
Step 7. 合并 nuisance remainder 与 empirical noise。
Step 8. Sequential RL 另写 horizon-wise DR recursion；不要把本节 bandit score 直接复制过去。
```

## 正交性表达

不同 folds 的 nuisance fits 共享部分训练数据，因此不能在条件于全部 fits 后，把全部 cross-fitted scores 当成相互独立样本。有限样本界可按 fold 分析再组合；渐近正态通常另需 nuisance 一致性、方差控制，以及合适范数下乘积误差为 $o_p(n^{-1/2})$ 等条件。

若把目标解释为 causal treatment effect，还须额外给出识别条件，例如 consistency 与 unconfoundedness；DR 代数不能证明不存在未观测混杂。

在满足正交 score、cross-fitting 与相应范数条件时，常写成：

$$
\widehat\psi - \psi
=\mathrm{empirical\ noise}
+O(\Vert\hat m-m\Vert\cdot\Vert\hat e-e\Vert)
+\mathrm{higher\ order}.
$$

这就是 nuisance error 的一阶抵消。

## 反例：正确 nuisance 也不能补救偷看评估 reward 的 policy

取单个评估样本， $X$ 为常数， $A,Y$ 是相互独立的公平 Bernoulli。两个动作的真实均值都是 $m(a)=1/2$，behavior 为 $e(a)=1/2$；直接使用真值 $\widehat m=m,\widehat e=e$。

现在观察该条评估数据后选 policy： $Y=1$ 时选刚看到的动作 $A$， $Y=0$ 时选另一个动作 $1-A$。不论选哪个动作，在独立新样本上的真实价值均为 $V(\pi)=1/2$，但

$$
\widehat\phi_{DR}
=\frac12+2\mathbf1\lbrace\pi=A\rbrace(Y-\tfrac12)
=\frac12+Y,
\qquad \mathbb E\widehat\phi_{DR}=1.
$$

若忽略 policy 的数据依赖，乘积余项因两 nuisance 正确而为零，却会错误地预测无偏。失效的是条件期望步骤：选择 $\pi$ 的信息已经包含评估 reward，条件化后不能继续沿用原来的 $m,e$。四种 $(A,Y)$ 的精确枚举见 [边界测试](../../tests/test_final_math_boundaries.py)。

## 常见坑

- importance weight 可能爆炸，需要 clipping 或 overlap assumption。
- sequential RL 的 DR 比 contextual bandit 更复杂，因为有 horizon-wise recursion。
- logged policy propensity 如果未知，要估计；估计错误会影响 guarantee。
- 同一数据同时 fit nuisance 与评估时，有限样本“无偏”通常不成立；要用 sample splitting/cross-fitting 或专门 empirical-process 论证。
- Clipping importance weights 会引入新的 bias，double robustness 不会自动消除它。

## 来源论文 / 参考

- Doubly Robust Policy Evaluation and Learning, ICML 2011. https://icml.cc/2011/papers/554_icmlpaper.pdf
- Doubly Robust Off-policy Value Evaluation for Reinforcement Learning, ICML 2016. https://proceedings.mlr.press/v48/jiang16.html
- More Robust Doubly Robust Off-policy Evaluation, ICML 2018. https://research.google/pubs/more-robust-doubly-robust-off-policy-evaluation/

## 关联模板与本地证据

- [T07：在正确策略的 occupancy 下展开 Bellman 价值误差。](../sequential-decision/T07-bellman.md)
- [T18：用交换性和名次对称性证明边际覆盖。](T18-split-conformal.md)

通用证明工具：P01、P04、P09；见 [证明原语](../../通用证明原语.md)。

- [Doubly Robust Off-policy Value Evaluation for Reinforcement Learning](../../proof_ref/foundations-2026-09/doubly-robust-off-policy-value-evaluation-for-reinforcement-1511.03722/README.md) · [官方 arXiv](https://arxiv.org/abs/1511.03722)
- [Double/Debiased Machine Learning for Treatment and Structural Parameters](../../proof_ref/foundations-2026-09/double-debiased-machine-learning-for-treatment-and-structural-1608.00060/README.md) · [官方 arXiv](https://arxiv.org/abs/1608.00060)

## 专项证明接口（2026-10-02）

- [T48：先用识别假设连接干预与观察 law，再分析 DR 或深度表示的估计误差。](T48-causal-identification.md)
