---
id: T21
type: proof-template
refined: 2026-09-28
status: "refined-algebra"
---

# T21. Bayesian filtering / log-odds evidence accumulation

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

结合预测先验与当前 likelihood，区分静态和动态状态证据累积。

## 复用契约

**输入对象**：转移矩阵、emission、初始 law、观测历史与归一化常数。

**输出结论**：给定模型的过滤恒等式；现实校准和识别性另证。

**必需假设**：

- Markov/条件独立等模型假设明确。
- normalizer 非零；log-odds 涉及概率严格为正。
- 直接向初始 odds 累加只在静态状态等相应条件下成立。

**失败例子**：两行转移都为 (1/2,1/2) 时预测会忘掉上一后验，不能不断向初始 odds 加旧证据。

## 实例化时必须完成

- [ ] 先预测，再乘 likelihood 并归一化。
- [ ] 区分 filtering 与 smoothing。
- [ ] 分开代数正确和模型正确。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [测度、条件期望、滤过与适应过程](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%B5%8B%E5%BA%A6%E3%80%81%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E3%80%81%E6%BB%A4%E8%BF%87%E4%B8%8E%E9%80%82%E5%BA%94%E8%BF%87%E7%A8%8B.md) · [Markov 链、随机过程与状态空间模型](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/Markov%20%E9%93%BE%E3%80%81%E9%9A%8F%E6%9C%BA%E8%BF%87%E7%A8%8B%E4%B8%8E%E7%8A%B6%E6%80%81%E7%A9%BA%E9%97%B4%E6%A8%A1%E5%9E%8B.md)

## 适用场景

HMM、online monitoring、state tracking、belief update、prefix-safe reliability estimation、sequential evidence accumulation。

## 核心公式

令

$$
A_{s's}=\mathbb P(S_t=s\mid S_{t-1}=s'),
\qquad
\ell_s(o)=p(o\mid S_t=s).
$$

预测：

$$
\mu_t(s)=\sum_{s'}A_{s's}\pi_{t-1}(s').
$$

观测更新：

$$
u_t(s)=\ell_s(o_t)\mu_t(s),
\quad
\pi_t(s)=\frac{u_t(s)}{\sum_{s^\star}u_t(s^\star)}.
$$

若二状态的 predictive probabilities 与 likelihoods 都为正，则 log-odds：

$$
\log\frac{\pi_t(\mathrm{ON})}{\pi_t(\mathrm{OFF})}
=
\log\frac{\mu_t(\mathrm{ON})}{\mu_t(\mathrm{OFF})}
+
\log\frac{\ell_{\mathrm{ON}}(o_t)}{\ell_{\mathrm{OFF}}(o_t)}.
$$

若 latent state 是静态的（等价于 identity transition），且给定这个静态 state 后 $o_1,\ldots,o_t$ 条件独立，则

$$
\operatorname{logit}(p_t)
=
\operatorname{logit}(p_0)
+
\sum_{k=1}^t
\log\frac{\ell_{\mathrm{ON}}(o_k)}{\ell_{\mathrm{OFF}}(o_k)}.
$$

其中 $p_t=\pi_t(\mathrm{ON})$；emission density 应相对于同一个 dominating measure 定义。

一般 HMM 的 transition prediction $\pi_{t-1}\mapsto\mu_t$ 会非线性地改变 odds；此时只能逐步使用“predictive log-odds + 当前 likelihood ratio”，不能把所有 likelihood ratios 直接加到初始 odds。

<a id="t21-filtering-odds"></a>

^t21-filtering-odds

## 逐步证明模板

```text
Step 1. 写 predictive belief mu_t。
Step 2. 写 unnormalized posterior u_t = likelihood * predictive belief。
Step 3. 写 normalized posterior pi_t。
Step 4. 取两个 state 的 posterior ratio，normalizer cancel。
Step 5. 把 ratio 分解为 predictive odds 和 likelihood ratio。
Step 6. 取 log，得到 additive evidence。
Step 7. 如果 transition 是 identity，递推展开成 evidence sum。
```

## 可迁移用法

- 解释一个在线 tracker 如何整合 prefix evidence。
- 把 observation family 的差异解释为 log-likelihood ratio evidence 的差异。
- 区分 filtering 与 smoothing：filtering 只用 `o_{1:t}`，smoothing 用 `o_{1:T}`。

## 常见坑

- HMM latent state 不一定等于真实 process state；它可以只是 monitoring state。
- filtering 的 posterior calibration 依赖 model correctness，不要过度宣称。
- smoothing/Viterbi full path 不是 online prefix-safe score。
- log-odds 形式要求相关概率严格为正；零 likelihood 需在扩展实数或直接概率域中处理。

## 来源论文 / 参考

- A Tutorial on Hidden Markov Models and Selected Applications in Speech Recognition, Rabiner, 1989. https://www.cs.ubc.ca/~murphyk/Bayes/rabiner.pdf
- Bayesian Filtering and Smoothing, Särkkä, 2013. https://users.aalto.fi/~ssarkka/pub/cup_book_online_20131111.pdf

## 关联模板与本地证据

- [T23：从信息依赖图证明适应性和停止时间性质。](T23-prefix-safety.md)
- [T22：分开证明 AUROC 排序不变性与 Brier proper-scoring 分解。](T22-ranking-proper-scoring.md)

通用证明工具：P01、P02；见 [证明原语](../../通用证明原语.md)。
