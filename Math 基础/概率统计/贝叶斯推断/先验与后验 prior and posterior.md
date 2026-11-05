---
status: canonical
reviewed: 2026-08-24
---

# 先验、似然、证据与后验

> [!tip] 前置主干
> 先复习 [概率论主干：联合、条件、期望与协方差](../%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md#7-bayes%E5%85%A8%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%85%A8%E6%96%B9%E5%B7%AE)。
> MLE、MAP 与完整后验的区别见 [最大似然、MAP 与贝叶斯估计](../%E6%9C%80%E5%A4%A7%E4%BC%BC%E7%84%B6%E3%80%81MAP%20%E4%B8%8E%E8%B4%9D%E5%8F%B6%E6%96%AF%E4%BC%B0%E8%AE%A1.md)；后验难以解析计算时见 [蒙特卡洛、重要性采样与 MCMC](../%E8%92%99%E7%89%B9%E5%8D%A1%E6%B4%9B%E3%80%81%E9%87%8D%E8%A6%81%E6%80%A7%E9%87%87%E6%A0%B7%E4%B8%8E%20MCMC.md)。

贝叶斯推断把未知量视为随机变量，并用观测数据更新其概率分布。

## 参数形式

令 $\theta$ 是未知参数， $D$ 是观测数据：

$$
p(\theta\mid D)
=\frac{p(D\mid\theta)p(\theta)}{p(D)}.
$$

- **先验** $p(\theta)$：看数据前对 $\theta$ 的概率分布；
- **似然** $p(D\mid\theta)$：固定已观测的 $D$，把它视为 $\theta$ 的函数；它通常不是关于 $\theta$ 的归一化概率分布；
- **证据/边际似然**

  $$p(D)=\int p(D\mid\theta)p(\theta)\thinspace d\theta;$$

- **后验** $p(\theta\mid D)$：结合先验与数据后的参数分布。

因此常写

$$
p(\theta\mid D)\propto p(D\mid\theta)p(\theta),
$$

其中正比关系只允许忽略**与 $\theta$ 无关**的因子。

## 一个离散例子

设 $R$ 表示下雨， $C$ 表示看到乌云：

$$
P(R\mid C)=\frac{P(C\mid R)P(R)}{P(C)}.
$$

这里必须同时知道先验降雨率以及晴雨情况下出现乌云的概率。仅凭“乌云通常意味着下雨”不能任意把后验写成 80%。

## 后验预测

贝叶斯建模通常关心新观测 $x_*$：

$$
p(x_\ast\mid D)
=\int p(x_\ast\mid\theta)p(\theta\mid D)\thinspace d\theta.
$$

它对后验参数不确定性进行积分，和只使用一个点估计 $\hat\theta$ 的预测不同。

## 与最大似然、MAP 的区别

- 最大似然： $\hat\theta_{\mathrm{MLE}}=\arg\max_\theta p(D\mid\theta)$；
- 最大后验： $\hat\theta_{\mathrm{MAP}}=\arg\max_\theta p(D\mid\theta)p(\theta)$；
- 完整贝叶斯推断：保留整个 $p(\theta\mid D)$，而不只保留单个最优参数。

# 与 LLM 的关系：哪些是严格结论，哪些只是类比

## Next-token 分布不是自动意义下的贝叶斯后验

自回归 LLM 输出

$$
p_\phi(x_t\mid x_{< t}),
$$

这是给定上下文的**条件预测分布**。上下文确实改变预测，但普通 Transformer 前向传播并没有显式定义参数先验 $p(\phi)$、计算参数后验 $p(\phi\mid D)$，也没有执行贝叶斯定理。

因此可说“上下文条件化预测”，不应直接说“模型正在做贝叶斯后验更新”。若某个模型明确采用贝叶斯参数、隐变量或贝叶斯上下文学习分析，才可使用严格的 posterior 术语。

## 普通微调不是自动意义下的贝叶斯更新

预训练权重通常只是优化的初始化点，不是一个完整的参数概率分布。监督微调通过梯度优化得到另一组点估计，一般不能直接称为后验。

在明确指定先验、似然并做 MAP、Laplace approximation、变分推断或 MCMC 时，才有严格的贝叶斯解释。把预训练模型称为“prior”可以作为直觉类比，但必须标注其非严格性。

## RLHF 也不是证据更新

RLHF/PPO 通常根据奖励模型优化策略。奖励信号不是贝叶斯公式中的 evidence，优化后策略也不是自然得到的 posterior。某些 KL-regularized objectives 可以与概率推断建立数学联系，但需要具体目标函数与假设，不能据此把所有 RLHF 都称为贝叶斯更新。

## 记忆要点

1. 条件概率不等于贝叶斯参数后验。
2. “先验 × 似然”中，先验必须是分布，似然必须对应明确的数据生成模型。
3. 把预训练、上下文或奖励称作 prior/evidence 时，要区分严格模型与启发式类比。

## 来源

- [Variational Inference: A Review for Statisticians](https://arxiv.org/abs/1601.00670)
