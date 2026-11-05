---
type: note
domain: math/information-theory
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# 信息论基础：熵、交叉熵与 KL 散度

证明进阶：[T49 从交叉熵 excess 到分类 excess](../../proofs/generalization/T49-surrogate-bayes-risk.md) · [T46 Gaussian Rényi 预算](../../proofs/statistics/T46-gaussian-privacy-accounting.md)。

应用证明：[T37 InfoNCE 的 KL 分解与下游边界](../../proofs/deep-learning/T37-contrastive-transfer.md)、[T38 编码长度与泛化](../../proofs/generalization/T38-compression.md)。

> [!tip] 统计连接
> 从“最大化似然”理解交叉熵训练，见 [最大似然、MAP 与贝叶斯估计](%E6%9C%80%E5%A4%A7%E4%BC%BC%E7%84%B6%E3%80%81MAP%20%E4%B8%8E%E8%B4%9D%E5%8F%B6%E6%96%AF%E4%BC%B0%E8%AE%A1.md)；期望难以精确计算时的近似见 [蒙特卡洛、重要性采样与 MCMC](%E8%92%99%E7%89%B9%E5%8D%A1%E6%B4%9B%E3%80%81%E9%87%8D%E8%A6%81%E6%80%A7%E9%87%87%E6%A0%B7%E4%B8%8E%20MCMC.md)。
> KL 的局部二阶几何见 [Fisher 信息、自然梯度与信息几何](Fisher%20%E4%BF%A1%E6%81%AF%E3%80%81%E8%87%AA%E7%84%B6%E6%A2%AF%E5%BA%A6%E4%B8%8E%E4%BF%A1%E6%81%AF%E5%87%A0%E4%BD%95.md)；与“搬运质量”的分布距离对照见 [最优传输与 Wasserstein 距离](%E6%9C%80%E4%BC%98%E4%BC%A0%E8%BE%93%E4%B8%8E%20Wasserstein%20%E8%B7%9D%E7%A6%BB.md)。

先把最容易混淆的三个量放进同一个故事：

- **熵**：真实数据本身平均有多难预测；
- **交叉熵**：如果真实数据来自 $p$，却用模型 $q$ 编码，平均要付出多少代价；
- **KL 散度**：用错模型 $q$ 相比知道真实分布 $p$ 多付出的代价。

## 知识依赖与相关笔记

- 概率、期望和条件分布：[概率论主干：联合、条件、期望与协方差](%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md)。
- 分类分布：[Categorical Distribution](Categorical%20Distribution.md#3-%E4%B8%8E-cross-entropy-%E4%BA%A4%E5%8F%89%E7%86%B5-%E7%9A%84%E8%81%94%E7%B3%BB)。
- 训练中的实现：[CrossEntropy](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0/CrossEntropy.md)、[NLL loss](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0/NLL%20loss.md)、[神经网络训练闭环：前向、反向与优化](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0%E5%B7%A5%E7%A8%8B/PyTorch/%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C%E8%AE%AD%E7%BB%83%E9%97%AD%E7%8E%AF%EF%BC%9A%E5%89%8D%E5%90%91%E3%80%81%E5%8F%8D%E5%90%91%E4%B8%8E%E4%BC%98%E5%8C%96.md)。
- 对比学习：[InfoNCE Loss](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0/InfoNCE%20Loss.md#infonce-%E7%9A%84%E6%95%B0%E5%AD%A6%E5%BD%A2%E5%BC%8F)、[NT-Xent Loss](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0/NT-Xent%20Loss.md)。
- 变分推断：[Bayesian ELBO](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E5%BB%BA%E6%A8%A1/%E5%8F%98%E5%88%86%E6%8E%A8%E6%96%AD/Bayesian%20ELBO.md#%E5%AE%9A%E4%B9%89)、[变分自编码器（VAE）intro](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E5%BB%BA%E6%A8%A1/VAE/%E5%8F%98%E5%88%86%E8%87%AA%E7%BC%96%E7%A0%81%E5%99%A8%EF%BC%88VAE%EF%BC%89intro.md#2-vae%E7%9A%84%E5%8E%9F%E7%90%86-principle)。
- 生成模型中的 diffusion、score 与概率流：[扩散模型、Score Matching 与 Flow Matching](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B/%E6%89%A9%E6%95%A3%E6%A8%A1%E5%9E%8B%E3%80%81Score%20Matching%20%E4%B8%8E%20Flow%20Matching.md)。
- 模型评估与校准：[从任务到可信结论：数据划分、泛化与评估](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%9C%BA%E5%99%A8%E5%AD%A6%E4%B9%A0%E5%9F%BA%E7%A1%80/%E4%BB%8E%E4%BB%BB%E5%8A%A1%E5%88%B0%E5%8F%AF%E4%BF%A1%E7%BB%93%E8%AE%BA%EF%BC%9A%E6%95%B0%E6%8D%AE%E5%88%92%E5%88%86%E3%80%81%E6%B3%9B%E5%8C%96%E4%B8%8E%E8%AF%84%E4%BC%B0.md)。

## 1. 自信息：越意外，信息越大

事件概率为 $p(x)$ 时，它的自信息定义为

$$
I(x)=-\log p(x).
$$

这个形式满足直觉：

- 必然事件 $p=1$ 的信息为 0；
- 越罕见的事件，出现时越“意外”，信息越大；
- 独立事件同时发生时，概率相乘而信息相加。

对数底决定单位：底为 2 时单位是 bit；自然对数时单位是 nat。机器学习损失通常使用自然对数。

## 2. 熵：预测真实分布所需的平均信息

离散随机变量 $X\sim p$ 的 Shannon 熵为

$$
H(p)=H(X)=-\sum_x p(x)\log p(x)
=\mathbb E_{X\sim p}[-\log p(X)].
$$

熵是**一个分布的平均不确定性**，不是单个样本的属性。

- 分布集中在一个结果上时，熵为 0；
- 在固定的有限类别数下，均匀分布熵最大；
- 类别数增大时，最大熵也会增大，因此不能脱离支持集直接比较。

## 3. 交叉熵：真实来自 p，却按 q 付费

若真实分布是 $p$，模型分布是 $q$，交叉熵为

$$
H(p,q)=-\sum_x p(x)\log q(x)
=\mathbb E_{X\sim p}[-\log q(X)].
$$

在 one-hot 分类标签下， $p$ 只在真实类别 $y$ 上为 1，所以

$$
H(p,q)=-\log q(y).
$$

这就是单样本负对数似然。实践中的 `CrossEntropyLoss` 通常直接接收 logits，并在内部稳定地组合 `log_softmax` 与 NLL；不要先手动 `softmax` 再取对数。

## 4. KL 散度：额外付出的编码代价

KL 散度定义为

$$
D_{\mathrm{KL}}(p\Vert q)
=\sum_x p(x)\log\frac{p(x)}{q(x)}.
$$

把式子展开：

$$
H(p,q)=H(p)+D_{\mathrm{KL}}(p\Vert q).
$$

训练时真实分布 $p$ 固定，因此最小化交叉熵等价于最小化前向 KL $D_{\mathrm{KL}}(p\Vert q)$。KL 满足非负性，并且当且仅当两个分布几乎处处相同时为 0。

但 KL **不是距离**：

- 通常 $D_{\mathrm{KL}}(p\Vert q)\ne D_{\mathrm{KL}}(q\Vert p)$；
- 不满足三角不等式；
- 若某处 $p(x)>0$ 而 $q(x)=0$，则 $D_{\mathrm{KL}}(p\Vert q)=\infty$。

方向很重要。前向 KL 对“漏掉真实分布有质量的区域”惩罚很重；反向 KL 的行为不同，常更偏向选择某个高密度模式，但“覆盖模式/寻找模式”只是直觉，具体结论依赖分布族和优化条件。

## 5. 最大似然为什么得到交叉熵

对独立样本 $x_1,\ldots,x_n\sim p_{\text{data}}$，模型为 $q_\theta$。最大化似然：

$$
\max_\theta\prod_{i=1}^n q_\theta(x_i)
$$

等价于最小化平均 NLL：

$$
\min_\theta-\frac{1}{n}\sum_{i=1}^n\log q_\theta(x_i).
$$

样本足够多时，这个经验平均估计 $H(p_{\text{data}},q_\theta)$。所以交叉熵并不是随意选择的分类公式，而是最大似然的直接结果。

对语言模型，序列概率按链式法则分解为 token 条件概率，因而总 NLL 是各 token NLL 之和，见 [NLL loss](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0/NLL%20loss.md#4-%E5%AE%8C%E6%95%B4%E7%9A%84-sft-loss)。

## 6. 条件熵与互信息

条件熵衡量知道 $Y$ 后 $X$ 还剩多少不确定性：

$$
H(X\mid Y)=\mathbb E_Y[H(X\mid Y=y)].
$$

互信息衡量知道一个变量后，另一个变量的不确定性平均减少多少：

$$
I(X;Y)=H(X)-H(X\mid Y)
=D_{\mathrm{KL}}(p(x,y)\Vert p(x)p(y)).
$$

因此 $I(X;Y)=0$ 当且仅当 $X,Y$ 独立。[InfoNCE](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0/InfoNCE%20Loss.md#infonce-%E5%90%8D%E5%AD%97%E7%9A%84%E7%94%B1%E6%9D%A5) 在特定采样假设下给互信息下界，但不能把任意对比损失都无条件称为“等价最大化互信息”。

## 7. KL 在变分推断中的两次出现

ELBO 有两种常用理解：

$$
\log p(x)=\mathop{\mathrm{ELBO}}(q)+D_{\mathrm{KL}}(q(z\mid x)\Vert p(z\mid x)),
$$

以及 VAE 常用形式

$$
\mathop{\mathrm{ELBO}}
=\mathbb E_{q(z\mid x)}[\log p(x\mid z)]
-D_{\mathrm{KL}}(q(z\mid x)\Vert p(z)).
$$

第一式说明 ELBO 是证据下界；第二式把目标拆成重构项与潜变量正则项。详见 [Bayesian ELBO](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E5%BB%BA%E6%A8%A1/%E5%8F%98%E5%88%86%E6%8E%A8%E6%96%AD/Bayesian%20ELBO.md#vae-%E5%B8%B8%E7%94%A8%E5%BD%A2%E5%BC%8F)。

## 8. 可运行示例：验证三者关系

```python
import numpy as np

p = np.array([0.7, 0.2, 0.1])       # 真实分布
q = np.array([0.6, 0.25, 0.15])     # 模型分布

entropy = -(p * np.log(p)).sum()
cross_entropy = -(p * np.log(q)).sum()
kl = (p * np.log(p / q)).sum()

print("H(p):", entropy)
print("H(p, q):", cross_entropy)
print("KL(p || q):", kl)
print("H(p) + KL:", entropy + kl)

assert kl >= -1e-12
assert np.allclose(cross_entropy, entropy + kl)
```

## 常见误区

1. **“熵越高，模型越差。”** 熵首先是数据分布的不确定性；模型质量要看它对真实数据的交叉熵、校准和任务指标。
2. **“交叉熵就是 KL。”** 两者相差 $H(p)$；优化时 $p$ 固定才有相同最优解。
3. **“KL 是对称距离。”** 方向不同会产生不同目标和行为。
4. **“把概率先 `softmax` 再喂给交叉熵更保险。”** 大多数框架的交叉熵接口要 logits；重复 softmax 会得到错误目标且数值更差。
5. **“连续分布的微分熵也总是非负。”** 微分熵可以为负，并且会随坐标尺度改变；KL 仍保持非负。
6. **“训练 NLL 下降就等于生成质量全面提升。”** NLL 是重要目标，但有限样本、分布偏移、解码策略和下游偏好都会造成差异。

## 来源

- Shannon, [A Mathematical Theory of Communication](https://people.math.harvard.edu/~ctm/home/text/others/shannon/entropy/entropy.pdf), 1948.
- Cover & Thomas, *Elements of Information Theory*, 2nd ed., Wiley, 2006.
- [PyTorch: `CrossEntropyLoss`](https://docs.pytorch.org/docs/stable/generated/torch.nn.CrossEntropyLoss.html)
- [PyTorch: `KLDivLoss`](https://docs.pytorch.org/docs/stable/generated/torch.nn.KLDivLoss.html)
- van den Oord et al., [Representation Learning with Contrastive Predictive Coding](https://arxiv.org/abs/1807.03748), 2018.
- Blei, Kucukelbir & McAuliffe, [Variational Inference: A Review for Statisticians](https://arxiv.org/abs/1601.00670), JASA 2017.
