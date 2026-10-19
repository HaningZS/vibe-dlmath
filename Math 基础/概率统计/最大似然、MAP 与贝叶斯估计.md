---
type: note
domain: math/statistics
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# 最大似然、MAP 与贝叶斯估计

同一份数据可以支持三种不同回答：

- **MLE**：哪个参数最能解释已经看到的数据？
- **MAP**：结合事前经验后，哪个参数值最可信？
- **完整贝叶斯推断**：看完数据后，各种参数值分别还有多可信，以及这种不确定性如何传到预测？

类比侦探破案：似然是“如果嫌疑人是他，这些证据出现得有多合理”；先验是“看证据前，各种可能性多可信”；后验是两者合并后的判断。MLE 只找最能解释证据的人，MAP 找后验最高点，而完整贝叶斯推断保留整份嫌疑概率清单。

## 知识依赖与相关笔记

- 总入口：[Math 基础目录](../Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md)；针对 AI research 的学习顺序：[AI Researcher 数学学习路线](../AI%20Researcher%20%E6%95%B0%E5%AD%A6%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)。
- 条件概率与 Bayes 公式：[Bayes 公式](%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md#7-bayes%E5%85%A8%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%85%A8%E6%96%B9%E5%B7%AE)。
- 分布与似然：[常见概率分布与指数族](%E5%B8%B8%E8%A7%81%E6%A6%82%E7%8E%87%E5%88%86%E5%B8%83%E4%B8%8E%E6%8C%87%E6%95%B0%E6%97%8F.md)。
- 先验、后验和共轭：[先验与后验 prior and posterior](%E8%B4%9D%E5%8F%B6%E6%96%AF%E6%8E%A8%E6%96%AD/%E5%85%88%E9%AA%8C%E4%B8%8E%E5%90%8E%E9%AA%8C%20prior%20and%20posterior.md)、[Beta 分布](%E8%B4%9D%E5%8F%B6%E6%96%AF%E6%8E%A8%E6%96%AD/Beta%20%E5%88%86%E5%B8%83.md)、[共轭先验](%E8%B4%9D%E5%8F%B6%E6%96%AF%E6%8E%A8%E6%96%AD/%E5%85%B1%E8%BD%AD%E5%85%88%E9%AA%8C.md)。
- 负对数似然与 KL：[最大似然与交叉熵](%E4%BF%A1%E6%81%AF%E8%AE%BA%E5%9F%BA%E7%A1%80%EF%BC%9A%E7%86%B5%E3%80%81%E4%BA%A4%E5%8F%89%E7%86%B5%E4%B8%8E%20KL%20%E6%95%A3%E5%BA%A6.md#5-%E6%9C%80%E5%A4%A7%E4%BC%BC%E7%84%B6%E4%B8%BA%E4%BB%80%E4%B9%88%E5%BE%97%E5%88%B0%E4%BA%A4%E5%8F%89%E7%86%B5)。
- 近似推断：[Bayesian ELBO](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E5%BB%BA%E6%A8%A1/%E5%8F%98%E5%88%86%E6%8E%A8%E6%96%AD/Bayesian%20ELBO.md)、[蒙特卡洛、重要性采样与 MCMC](%E8%92%99%E7%89%B9%E5%8D%A1%E6%B4%9B%E3%80%81%E9%87%8D%E8%A6%81%E6%80%A7%E9%87%87%E6%A0%B7%E4%B8%8E%20MCMC.md)。
- 优化视角：[凸集、凸函数与优化直觉](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E5%87%B8%E9%9B%86%E3%80%81%E5%87%B8%E5%87%BD%E6%95%B0%E4%B8%8E%E4%BC%98%E5%8C%96%E7%9B%B4%E8%A7%89.md)、[梯度下降、学习率与收敛](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E6%A2%AF%E5%BA%A6%E4%B8%8B%E9%99%8D%E3%80%81%E5%AD%A6%E4%B9%A0%E7%8E%87%E4%B8%8E%E6%94%B6%E6%95%9B.md)。

## 1. 先分清概率和似然

模型 $p(x\mid\theta)$ 同时可以从两个方向阅读：

- 固定参数 $\theta$，把 $x$ 当变量：它是数据的概率分布；
- 固定已经观察到的数据 $x$，把 $\theta$ 当变量：它是似然函数 $L(\theta;x)$。

似然通常**不是参数上的概率分布**，不必对 $\theta$ 积分为 1。它只比较不同参数对同一批数据的相对解释力。

例如连续模型里，$p(x\mid\theta)$ 是密度，不是“参数为 $\theta$ 的概率”。把 $P(\theta\mid x)$ 与 $p(x\mid\theta)$ 对调，是最常见的 Bayes 错误。

## 2. 最大似然估计（MLE）

给定独立样本 $D=\{x_i\}_{i=1}^n$：

$$
\hat\theta_{\mathrm{MLE}}
=\arg\max_\theta p(D\mid\theta)
=\arg\max_\theta\prod_{i=1}^n p(x_i\mid\theta).
$$

乘很多小概率数容易下溢，也不方便求导，所以通常最大化对数似然：

$$
\ell(\theta)=\sum_{i=1}^n\log p(x_i\mid\theta).
$$

最大化 $\ell$ 等价于最小化负对数似然（NLL）。机器学习中很多“损失函数”就是 NLL。

### 2.1 Bernoulli 的 MLE

若 $x_i\in\{0,1\}$ 且 $x_i\sim\operatorname{Bernoulli}(p)$，记成功次数 $s=\sum_i x_i$：

$$
\ell(p)=s\log p+(n-s)\log(1-p).
$$

当 $0<s<n$ 时，最优解在区间内部，令导数为零可得

$$
\hat p_{\mathrm{MLE}}=\frac{s}{n}.
$$

结论很直观：未知成功率由样本成功比例估计。若 $s=0$ 或 $s=n$，内部没有导数为零的最优点，最大值分别落在边界 $p=0$ 或 $p=1$；公式 $s/n$ 仍给出边界解。只观察一次且成功时 MLE 就会给 $p=1$，这也暴露了小样本点估计的过度自信。

### 2.2 高斯回归为什么得到 MSE

若在给定输入 $x_i$ 后，各样本误差条件独立同分布，且

$$
y_i=f_\theta(x_i)+\varepsilon_i,
\qquad \varepsilon_i\overset{\mathrm{iid}}{\sim}\mathcal N(0,\sigma^2),
$$

并假定 $\sigma^2$ 固定、不随输入或参数改变，则最小化 NLL 等价于

$$
\min_\theta\sum_i\big(y_i-f_\theta(x_i)\big)^2.
$$

因此 MSE 不只是“方便求导”，它明确假设条件噪声以预测值为中心、近似高斯、条件独立且同方差。若是已知异方差 $\sigma_i^2$，对应的是按 $1/\sigma_i^2$ 加权的平方误差；若方差本身也要学习，完整 Gaussian NLL 还包含 $\log\sigma_i^2$，只最小化普通 MSE 就不再等价。

## 3. MAP：在似然上加入事前约束

Bayes 公式写成参数形式：

$$
p(\theta\mid D)
=\frac{p(D\mid\theta)p(\theta)}{p(D)}.
$$

最大后验估计为

$$
\hat\theta_{\mathrm{MAP}}
=\arg\max_\theta p(\theta\mid D)
=\arg\max_\theta
\left[\log p(D\mid\theta)+\log p(\theta)\right],
$$

因为证据 $p(D)$ 不依赖 $\theta$。MAP 等于“数据拟合项 + 先验偏好”的折中。

### 3.1 正则化就是某种先验吗？

在特定概率模型和参数化下：

- 零均值各向同性高斯先验 $p(\theta)\propto\exp(-\lambda\|\theta\|_2^2)$ 对应 L2 正则；
- 独立 Laplace 先验 $p(\theta)\propto\exp(-\lambda\|\theta\|_1)$ 对应 L1 正则。

但不要反过度：一个工程正则项未必代表我们真的相信该先验；MAP 也会依赖参数化，同一个模型换坐标后，密度最高点未必对应同一实体。

### 3.2 Beta–Bernoulli 的 MAP

令先验 $p\sim\operatorname{Beta}(\alpha,\beta)$，观测 $s$ 次成功、$f=n-s$ 次失败，则

$$
p\mid D\sim\operatorname{Beta}(\alpha+s,\beta+f).
$$

当 $\alpha+s>1,\beta+f>1$ 时，后验众数（MAP）为

$$
\hat p_{\mathrm{MAP}}
=\frac{\alpha+s-1}{\alpha+\beta+n-2}.
$$

先验像两边各放入一些“虚拟计数”，避免小样本结论跑到极端边界。不同公式中的 $-1$ 来自“众数”，不能把它与后验均值混淆。

## 4. 完整贝叶斯推断：保留整条后验分布

MLE 与 MAP 都把不确定性压成一个点。贝叶斯推断则保留

$$
p(\theta\mid D).
$$

对新观测 $x_*$，后验预测分布是

$$
p(x_*\mid D)
=\int p(x_*\mid\theta)p(\theta\mid D)\,d\theta.
$$

直觉上，它让每个可能参数都投票，权重就是后验概率，而不是只让最高点独断。

Beta–Bernoulli 下，下一次成功的后验预测概率恰好是后验均值：

$$
P(X_*=1\mid D)=\frac{\alpha+s}{\alpha+\beta+n}.
$$

完整贝叶斯的优势是能传播参数不确定性；代价是积分常常不可解，需要 Laplace 近似、变分推断、MCMC 等方法。

## 5. 三种方法放在一起

| 方法 | 输出 | 是否用先验 | 是否保留参数不确定性 | 常见优势 | 常见风险 |
|---|---|---:|---:|---|---|
| MLE | 一个点 | 否 | 否 | 简洁、数据多时常有效 | 小样本过拟合、边界解 |
| MAP | 一个点 | 是 | 否 | 便于加入约束、常等价正则化 | 对先验和参数化敏感 |
| 完整 Bayes | 一个分布 | 是 | 是 | 可给后验预测与不确定性 | 计算难、先验检查重要 |

数据足够多且模型可辨识、正则条件成立时，先验影响通常减弱，三者的中心可能靠近。但深度网络存在多组等价参数、非凸几何和分布外输入，不能机械套用“大数据后都一样”。

## 6. AI researcher 为什么需要这条主线

1. **损失设计**：Cross-Entropy 是 Categorical NLL，MSE 常是 Gaussian NLL。
2. **正则化解释**：weight decay 可在特定条件下看作高斯先验的 MAP，但 [AdamW](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E4%BC%98%E5%8C%96%E6%96%B9%E6%B3%95/AdamW%20and%20Adam%20and%20Momentum.md) 中的解耦 weight decay 与朴素 L2 梯度并非总等价。
3. **不确定性**：模型集成、Laplace 近似、Bayesian neural network 都试图恢复点估计丢掉的信息。
4. **生成模型**：VAE 的 [ELBO](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E5%BB%BA%E6%A8%A1/%E5%8F%98%E5%88%86%E6%8E%A8%E6%96%AD/Bayesian%20ELBO.md) 是不可解证据的变分下界。
5. **模型选择**：单看最大训练似然会奖励复杂模型；预测验证、边际似然或信息准则试图处理复杂度。

## 7. 可运行示例：少量硬币数据下三种回答

```python
import numpy as np

# 观察 8 次，其中 6 次成功；先验 Beta(2, 2) 温和偏向中间。
s, n = 6, 8
alpha, beta = 2.0, 2.0

mle = s / n
post_alpha = alpha + s
post_beta = beta + (n - s)
map_est = (post_alpha - 1.0) / (post_alpha + post_beta - 2.0)
posterior_mean = post_alpha / (post_alpha + post_beta)
posterior_sd = np.sqrt(
    post_alpha * post_beta
    / ((post_alpha + post_beta) ** 2 * (post_alpha + post_beta + 1.0))
)

print("MLE:", mle)
print("MAP:", map_est)
print("posterior mean / predictive P(success):", posterior_mean)
print("posterior standard deviation:", posterior_sd)

assert np.isclose(mle, 0.75)
assert 0.5 < map_est < mle
assert 0.5 < posterior_mean < mle
assert posterior_sd > 0
```

这里 MAP 和后验均值都被先验从 0.75 拉回一些，但两者不是同一个量。随着 $n$ 增大而样本比例保持不变，先验的相对影响会下降。

## 8. 常见误区

1. **“似然就是 $P(\theta\mid D)$。”** 似然是 $p(D\mid\theta)$ 作为参数函数；后验还要乘先验并归一化。
2. **“MLE 给出参数真的概率。”** MLE 只给点估计，没有直接给参数概率。
3. **“MAP 就是完整贝叶斯。”** MAP 只保留后验最高点，丢掉宽度、多峰和偏斜。
4. **“后验均值等于 MAP。”** 对称单峰分布可能接近，但一般不相同。
5. **“先验是主观拍脑袋。”** 先验可以来自物理边界、历史数据或层级结构，但必须做敏感性分析。
6. **“MLE 在任何参数化下都不变，MAP 也一样。”** MLE 对一一参数重参数化通常保持对应关系；密度众数 MAP 一般不具有这种不变性。
7. **“训练 NLL 最低的模型一定泛化最好。”** 有限样本、模型错设和过拟合都会打破这种推断。

## 9. 自测

1. 为什么似然函数不需要对参数积分为 1？
2. 从高斯噪声模型推导 MSE 时，哪些假设被悄悄带入？
3. Beta–Bernoulli 下，MAP 为什么通常不同于后验均值？为什么“下一次成功”的后验预测概率恰好等于后验均值，但完整预测不确定性仍不能由一个点估计替代？
4. 高斯先验如何对应 L2 正则？这个对应关系有哪些边界？
5. 哪种情形下你必须保留完整后验，而一个点估计明显不够？

## 延伸阅读

- Murphy, *Probabilistic Machine Learning: An Introduction*, Chapters 4–5.
- Bishop, *Pattern Recognition and Machine Learning*, Chapters 1–3.
- Gelman et al., *Bayesian Data Analysis*, 3rd ed., Chapters 1–3.
- Blei, Kucukelbir & McAuliffe, [Variational Inference: A Review for Statisticians](https://arxiv.org/abs/1601.00670).
- Stanford CS229, [Generative Learning Algorithms](https://cs229.stanford.edu/notes2022fall/cs229-notes2.pdf).
