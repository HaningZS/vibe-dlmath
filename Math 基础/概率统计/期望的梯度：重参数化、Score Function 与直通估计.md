---
type: note
domain: math/gradient-estimation
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# 期望的梯度：重参数化、Score Function 与直通估计

许多 AI 目标都长成

$$
J(\theta)=\mathbb E_{X\sim p_\theta}[f_\theta(X)].
$$

困难在于：参数 $\theta$ 不只出现在 $f_\theta$ 里，还改变了“会采到什么样的 $X$”。VAE 要从 posterior 采 latent，policy gradient 要从策略采动作，RLHF 要从语言模型采 token，离散 latent 还要面对不可导的类别选择。

本篇的主线是：**先看梯度到底通过哪条路径影响期望，再选择无偏但可能高方差的估计，或低方差但带松弛偏差的估计。**

## 知识依赖与相关笔记

- 总入口：[Math 基础目录](../Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md)、[AI Researcher 数学学习路线](../AI%20Researcher%20%E6%95%B0%E5%AD%A6%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)、[AI Researcher 高阶数学路线：LLM、CV 与生成模型](../AI%20Researcher%20%E9%AB%98%E9%98%B6%E6%95%B0%E5%AD%A6%E8%B7%AF%E7%BA%BF%EF%BC%9ALLM%E3%80%81CV%20%E4%B8%8E%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B.md)。
- 期望、条件概率：[概率论主干：联合、条件、期望与协方差](%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md)。
- Monte Carlo：[蒙特卡洛、重要性采样与 MCMC](%E8%92%99%E7%89%B9%E5%8D%A1%E6%B4%9B%E3%80%81%E9%87%8D%E8%A6%81%E6%80%A7%E9%87%87%E6%A0%B7%E4%B8%8E%20MCMC.md)。
- 导数与自动微分：[导数、梯度、Jacobian、Hessian 与自动微分](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E5%AF%BC%E6%95%B0%E3%80%81%E6%A2%AF%E5%BA%A6%E3%80%81Jacobian%E3%80%81Hessian%20%E4%B8%8E%E8%87%AA%E5%8A%A8%E5%BE%AE%E5%88%86.md)。
- 变量替换与重参数化：[变量替换与重参数化](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E7%A7%AF%E5%88%86%E3%80%81%E5%8F%98%E9%87%8F%E6%9B%BF%E6%8D%A2%E4%B8%8E%E6%A6%82%E7%8E%87%E5%AF%86%E5%BA%A6%E5%8F%98%E6%8D%A2.md#7-%E5%8F%98%E9%87%8F%E6%9B%BF%E6%8D%A2%E4%B8%8E%E9%87%8D%E5%8F%82%E6%95%B0%E5%8C%96%E6%A2%AF%E5%BA%A6%E4%B8%8D%E6%98%AF%E4%B8%80%E5%9B%9E%E4%BA%8B)。
- VAE 与 ELBO：[Bayesian ELBO](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E5%BB%BA%E6%A8%A1/%E5%8F%98%E5%88%86%E6%8E%A8%E6%96%AD/Bayesian%20ELBO.md)、[变分自编码器（VAE）intro](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E5%BB%BA%E6%A8%A1/VAE/%E5%8F%98%E5%88%86%E8%87%AA%E7%BC%96%E7%A0%81%E5%99%A8%EF%BC%88VAE%EF%BC%89intro.md)。
- 离散松弛：[Gumbel-Softmax](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E5%BB%BA%E6%A8%A1/%E7%A6%BB%E6%95%A3%E5%8F%98%E9%87%8F/Gumbel-Softmax.md)。
- Policy gradient 与 RLHF：[MDP、Bellman 方程与时序差分学习](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0/%E5%9F%BA%E7%A1%80/MDP%E3%80%81Bellman%20%E6%96%B9%E7%A8%8B%E4%B8%8E%E6%97%B6%E5%BA%8F%E5%B7%AE%E5%88%86%E5%AD%A6%E4%B9%A0.md)、[PPO math, origin and PPO-rlhf](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/LLM%20%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93/%E5%BE%AE%E8%B0%83%E4%B8%8E%E5%AF%B9%E9%BD%90/PPO%20math%2C%20origin%20and%20PPO-rlhf.md)、[BT model and RLHF math basic](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/LLM%20%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93/%E5%BE%AE%E8%B0%83%E4%B8%8E%E5%AF%B9%E9%BD%90/BT%20model%20and%20RLHF%20math%20basic.md)。
- 参数 score 的几何：[Fisher score](Fisher%20%E4%BF%A1%E6%81%AF%E3%80%81%E8%87%AA%E7%84%B6%E6%A2%AF%E5%BA%A6%E4%B8%8E%E4%BF%A1%E6%81%AF%E5%87%A0%E4%BD%95.md#2-score%E5%AF%B9%E6%95%B0%E6%A6%82%E7%8E%87%E5%AF%B9%E5%8F%82%E6%95%B0%E7%9A%84%E6%95%8F%E6%84%9F%E5%BA%A6)。

## 1. 为什么梯度不能直接“穿过采样”

假设 $X\sim\mathcal N(\mu,1)$，目标是

$$
J(\mu)=\mathbb E[X^2].
$$

若程序只执行：

1. 调用随机数生成器得到一个浮点数 `x`；
2. 计算 `x ** 2`；
3. 把 `x` 当常数反向传播；

那么图里没有从 $\mu$ 到 `x` 的可导路径，自动微分会给 0 或停止梯度。但真实答案是

$$
J(\mu)=\mu^2+1,
\qquad J'(\mu)=2\mu.
$$

问题不是“随机数天生不可导”，而是**采样分布对参数的依赖没有被写成可微计算路径或 likelihood-ratio 恒等式**。

离散采样更明显：`argmax` 或 Categorical sample 在参数稍微变化时，输出类别大多完全不变，跨越边界时又突然跳变；普通逐样本导数几乎处处为 0，不能代表期望怎样变化。

## 2. 什么时候可以交换梯度与期望

从积分写起：

$$
J(\theta)=\int f_\theta(x)p_\theta(x)\thinspace dx.
$$

我们想写

$$
\nabla_\theta J(\theta)
=\int\nabla_\theta\left[f_\theta(x)p_\theta(x)\right]dx.
$$

这一步需要条件，而不是符号游戏。常用的一组充分直觉是：

- $f_\theta(x)p_\theta(x)$ 对参数几乎处处可微；
- 导数在参数邻域内被某个可积函数支配，或满足相应 Leibniz/dominated-convergence 条件；
- 积分域/支持集不随参数改变，或者边界变化产生的额外项被正确处理；
- 期望和所需方差有限。

若 $X\sim U(0,\theta)$，支持集端点随 $\theta$ 移动。只在固定内部对密度求导会漏掉边界项，机械使用“score 期望为零”会出错。此时 $X=\theta U, U\sim U(0,1)$ 的 pathwise 表示反而自然。

在支持集固定且可交换微分/积分时，乘积法则给出统一分解：

$$
\nabla_\theta J
=\mathbb E_{p_\theta}[\nabla_\theta f_\theta(X)]
+\mathbb E_{p_\theta}
\left[f_\theta(X)\nabla_\theta\log p_\theta(X)\right].
$$

第一项是 $f$ 对参数的显式依赖；第二项是分布移动带来的贡献。pathwise estimator 会用另一种坐标表达这整件事，而不是简单“删掉第二项”。

## 3. Pathwise / reparameterization gradient

如果能把样本写成

$$
\varepsilon\sim q(\varepsilon),
\qquad X=T_\theta(\varepsilon),
$$

其中基础噪声分布 $q$ 不依赖 $\theta$，则

$$
J(\theta)
=\mathbb E_{\varepsilon\sim q}
[f_\theta(T_\theta(\varepsilon))].
$$

在可交换梯度与期望、 $T_\theta$ 和 $f$ 可微等条件下：

$$
\nabla_\theta J
=\mathbb E_\varepsilon
\left[
\nabla_\theta f_\theta(T_\theta(\varepsilon))
+\nabla_x f_\theta(T_\theta(\varepsilon))
\frac{\partial T_\theta(\varepsilon)}{\partial\theta}
\right].
$$

直觉是“固定同一粒噪声，轻轻改变参数，看样本和 loss 怎样平滑移动”。这利用了 $f$ 的局部导数，通常比只看最终 reward 的 score-function estimator 方差低。

### 3.1 Gaussian 重参数化与 VAE

若

$$
Z\sim\mathcal N(\mu_\phi(x),\mathop{\mathrm{diag}}(\sigma_\phi(x)^2)),
$$

可以写成

$$
\varepsilon\sim\mathcal N(0,I),
\qquad
Z=\mu_\phi(x)+\sigma_\phi(x)\odot\varepsilon.
$$

VAE 的 encoder 参数 $\phi$ 因而能通过 sampled $Z$ 接收 reconstruction term 的梯度，见 [Bayesian ELBO](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E5%BB%BA%E6%A8%A1/%E5%8F%98%E5%88%86%E6%8E%A8%E6%96%AD/Bayesian%20ELBO.md)。实践常输出 `log_var` 或 `log_std` 再指数化，以保证尺度为正并改善数值行为。

### 3.2 Pathwise 的边界

- 需要可微的采样变换，或更高级的 implicit reparameterization；
- $f$ 若包含真正不可导的 simulator/离散决策，链式导数可能不可用；
- 分布能采样不代表容易构造低方差可微 $T_\theta$；
- pathwise 通常低方差，但不是无条件优于其他估计器；高维、长时间动力学和尖锐 loss 仍可能梯度爆炸。

## 4. Score-function / likelihood-ratio estimator

若 $f$ 暂不显式依赖 $\theta$，利用

$$
\nabla_\theta p_\theta(x)
=p_\theta(x)\nabla_\theta\log p_\theta(x),
$$

得到

$$
\nabla_\theta\mathbb E_{p_\theta}[f(X)]
=\mathbb E_{p_\theta}
\left[f(X)\nabla_\theta\log p_\theta(X)\right].
$$

Monte Carlo 样本 $X_i\sim p_\theta$ 给出

$$
\widehat g_{\mathrm{SF}}
=\frac1N\sum_i
f(X_i)\nabla_\theta\log p_\theta(X_i).
$$

这就是 score-function、likelihood-ratio 或 REINFORCE estimator。它不需要对 $f(X)$ 关于 $X$ 求导，所以能处理离散动作和黑盒 reward；代价通常是高方差。

若 $f_\theta$ 还显式依赖参数，别忘了再加 $\mathbb E[\nabla_\theta f_\theta(X)]$。

### 4.1 为什么它适合离散策略

对 Categorical 动作 $A\sim\pi_\theta(\cdot\mid s)$：

$$
\nabla_\theta\mathbb E[R(A)]
=\mathbb E
[R(A)\nabla_\theta\log\pi_\theta(A\mid s)].
$$

动作本身无需可导。采到好动作，就提高其 log-probability；采到坏动作，就降低它。完整 policy-gradient theorem 还处理状态分布对策略的依赖，不能仅由这一行独立动作公式代替。

## 5. Baseline 与 control variate：减方差而不改期望

在正则条件下

$$
\mathbb E_{p_\theta}
[\nabla_\theta\log p_\theta(X)]=0.
$$

因此对不依赖当前 sampled $X$ 的 baseline $b$：

$$
\mathbb E
[(f(X)-b)\nabla_\theta\log p_\theta(X)]
=\nabla_\theta J.
$$

baseline 改变方差，不改变期望。直觉是从每个 reward 中减去“本来就预期会得到的水平”，只学习超出预期的部分。

### 5.1 Baseline 可以依赖什么

在 policy gradient 中， $b$ 可以依赖 state/context，因为在给定 state 后它不随当前 sampled action 改变：

$$
\mathbb E_{A\sim\pi(\cdot\mid s)}
[b(s)\nabla\log\pi(A\mid s)]=0.
$$

若 baseline 偷看 sampled action，通常会引入偏差，除非另加解析校正项。value function $V(s)$ 形成 advantage $A(s,a)=Q(s,a)-V(s)$，是 RL 中最重要的 learned baseline。

actor–critic 实现中，critic baseline 可以有自己的参数，但在构造 actor 的 score-function 项时通常要对 baseline `stop-gradient`；critic 再用单独的回归目标训练。否则会把“训练 baseline 的梯度”和“策略目标的梯度”意外混在一起。

### 5.2 最优 baseline 不总是简单均值

对标量参数和常数 baseline，使 score estimator 方差最小的

$$
b^*
=\frac{\mathbb E[f(X)s_\theta(X)^2]}
{\mathbb E[s_\theta(X)^2]},
$$

不一定等于 $\mathbb E[f]$。向量参数时还取决于怎样度量总方差。实际 baseline 自己也由有限数据学习，会有估计误差和优化权衡。

control variate 是更一般的思想：找一个期望已知、与目标高度相关的随机量，并加上零均值修正。REBAR、RELAX 等方法把连续松弛用作离散 score estimator 的 control variate，目标是保留无偏性同时降方差。

## 6. Policy gradient 与 RLHF

对轨迹 $\tau$，REINFORCE 的骨架为

$$
\nabla_\theta J
=\mathbb E_\tau
\left[
\sum_t G_t\nabla_\theta\log\pi_\theta(a_t\mid s_t)
\right],
$$

其中 $G_t$ 是 reward-to-go 或相应 advantage 估计。因果结构允许早先动作只乘其后受影响的回报，从而减少无关噪声；actor–critic、GAE 进一步改善 bias–variance trade-off。

在 RLHF 中，token 是离散动作，最终 reward model 分数可能在序列末端才出现。PPO 使用旧策略采样得到的 token、importance ratio 和 advantage 更新新策略，并常加入 reference-policy KL。这里仍然是 score-function/policy-gradient 家族，不是把梯度直接穿过 sampled token 或 reward-model 输入文本，见 [PPO math, origin and PPO-rlhf](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/LLM%20%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93/%E5%BE%AE%E8%B0%83%E4%B8%8E%E5%AF%B9%E9%BD%90/PPO%20math%2C%20origin%20and%20PPO-rlhf.md)。

reward model 可微不代表能对离散 token 选择做普通 pathwise 反传；除非显式引入连续松弛或其他梯度估计器，而那会改变训练目标或引入偏差。

## 7. 离散变量与 Gumbel–Softmax

### 7.1 Gumbel–Max：精确采 Categorical

给定类别概率 $\pi_1,\ldots,\pi_K$，采

$$
G_k=-\log(-\log U_k),
\qquad U_k\sim U(0,1),
$$

则

$$
A=\arg\max_k(\log\pi_k+G_k)
$$

精确服从 $\mathrm{Categorical}(\pi)$。但 `argmax` 仍不可导。

### 7.2 Concrete / Gumbel–Softmax 松弛

用 temperature $\tau>0$ 的 softmax 替换 argmax：

$$
Y_k
=\frac{\exp((\log\pi_k+G_k)/\tau)}
{\sum_j\exp((\log\pi_j+G_j)/\tau)}.
$$

$Y$ 是 simplex 内的连续向量，可以 pathwise 反传：

- $\tau$ 大：分布软、梯度平滑，但离 one-hot 目标远；
- $\tau$ 小：样本接近 one-hot，但梯度含 $1/\tau$、易尖锐或数值不稳；
- $\tau\to0$ 时前向样本趋近 Categorical one-hot，不代表有限温度下的 relaxed gradient 就是原离散目标的无偏梯度。

训练时 anneal temperature 是工程策略，不是“最终必然恢复正确离散梯度”的定理。

## 8. Straight-through estimator：前向硬，反向假装软

straight-through（ST）常写成概念形式：

$$
Y_{\mathrm{ST}}
=\mathop{\mathrm{stopgrad}}(Y_{\mathrm{hard}}-Y_{\mathrm{soft}})
+Y_{\mathrm{soft}}.
$$

前向数值等于 one-hot $Y_{\mathrm{hard}}$，反向 Jacobian 却来自 $Y_{\mathrm{soft}}$。这让下游看到真正离散输入，同时保留一条 surrogate gradient。

关键边界：

- ST 一般是**有偏** estimator；
- backward 使用的不是 forward 离散运算的真实导数；
- 它甚至不一定对应某个全局标量目标的精确梯度场；
- 温度、soft surrogate 与下游非线性共同决定偏差；
- 训练有效是经验事实，不等于统计无偏。

binary quantization 中把 `sign` 的导数假装成 1，或 Gumbel-ST 中前向 argmax、反向 softmax，都是同一类思想。

## 9. 如何选择估计器

| 情形 | 常见选择 | 主要优点 | 主要风险 |
|---|---|---|---|
| 连续、可重参数化 | pathwise | 通常低方差、用局部导数 | 需可微变换和下游 |
| 离散/黑盒 reward | score function | 在条件满足时无偏、通用 | 方差高 |
| 离散但可接受 relaxed objective | Gumbel–Softmax | 可普通反传 | temperature bias |
| 前向必须硬离散 | straight-through | 简单、工程可用 | 一般有偏、目标不一致 |
| 离散且既要无偏又想降方差 | REBAR/RELAX 等 | control variate 可降方差 | 实现和调参复杂 |

“无偏”也不自动等于训练最好：一个无偏但巨大方差的估计器，有限 batch 下可能几乎不可用；有偏但稳定的 estimator 有时优化更好。正确做法是明确目标、偏差、方差和计算成本，而不是只看一个标签。

## 10. 可运行示例一：pathwise 与 score-function 方差

令 $X\sim\mathcal N(\mu,\sigma^2)$， $J(\mu)=\mathbb E[X^2]$，真梯度是 $2\mu$。

```python
import numpy as np

rng = np.random.default_rng(17)
n = 1_000_000
mu, sigma = 1.0, 1.0

eps = rng.normal(size=n)
x = mu + sigma * eps
true_grad = 2.0 * mu

# Pathwise: d(x^2)/dmu = 2x，因为 x=mu+sigma*eps。
g_pathwise = 2.0 * x

# Score function: f(x) * d log N(x;mu,sigma^2)/dmu。
score = (x - mu) / sigma**2
g_score = x**2 * score

# 此标量问题的最优常数 baseline：E[f score^2]/E[score^2]。
b_opt = mu**2 + 3.0 * sigma**2
g_score_baseline = (x**2 - b_opt) * score

for name, estimate in [
    ("pathwise", g_pathwise),
    ("score", g_score),
    ("score + optimal constant baseline", g_score_baseline),
]:
    print(
        f"{name:36s} mean={estimate.mean():.4f} "
        f"per-sample variance={estimate.var():.2f}"
    )
    assert abs(estimate.mean() - true_grad) < 0.02

assert g_pathwise.var() < g_score_baseline.var() < g_score.var()
```

三者在 Monte Carlo 误差内都无偏；baseline 明显降低 score estimator 方差，但这个光滑 Gaussian 目标下 pathwise 仍更低。方差排序不是所有问题的普遍定理。

## 11. 可运行示例二：Gumbel 松弛的 bias–variance

对三类别 reward，离散目标梯度可解析计算。下面比较无偏 REINFORCE 与有限温度 relaxed/ST backward 所使用的梯度。

```python
import numpy as np

rng = np.random.default_rng(23)
logits = np.array([0.2, -0.4, 0.7])
rewards = np.array([0.0, 1.0, 3.0])
n = 500_000

def softmax(x, axis=-1):
    shifted = x - np.max(x, axis=axis, keepdims=True)
    exp_x = np.exp(shifted)
    return exp_x / exp_x.sum(axis=axis, keepdims=True)

probs = softmax(logits)
true_grad = probs * (rewards - probs @ rewards)

u = rng.uniform(np.finfo(float).eps, 1.0, size=(n, len(logits)))
gumbel = -np.log(-np.log(u))
actions = np.argmax(logits + gumbel, axis=1)
one_hot = np.eye(len(logits))[actions]

# REINFORCE: reward(a) * grad_logits log pi(a) = reward(a)*(one_hot-pi)。
reinforce = rewards[actions, None] * (one_hot - probs)

print("true discrete gradient:", true_grad)
print("REINFORCE mean:", reinforce.mean(axis=0))
print("REINFORCE total variance:", reinforce.var(axis=0).sum())
assert np.allclose(reinforce.mean(axis=0), true_grad, atol=0.006)

for tau in (1.0, 0.3):
    relaxed = softmax((logits + gumbel) / tau, axis=1)
    relaxed_reward = relaxed @ rewards
    # d(rewards @ softmax)/dlogits
    relaxed_grad = relaxed * (rewards - relaxed_reward[:, None]) / tau
    mean_grad = relaxed_grad.mean(axis=0)
    bias = np.linalg.norm(mean_grad - true_grad)
    variance = relaxed_grad.var(axis=0).sum()
    print(f"tau={tau}: mean={mean_grad}, bias_norm={bias:.4f}, variance={variance:.4f}")

    # 有限温度估计的是 relaxed objective；ST backward 也会使用这类梯度。
    assert bias > 1e-3
```

temperature 变小时，bias 往往下降但梯度方差/尖锐程度会上升；具体单调性依赖目标与参数，不能把这一次模拟当作普遍曲线。

## 12. 常见误区

1. **“Monte Carlo 平均可导，所以 sampler 自动可导。”** 还需要显式 pathwise 图或 score identity。
2. **“把采样结果 detach 后反传就是无偏。”** 若参数只通过分布影响样本，这会漏掉全部分布梯度。
3. **“REINFORCE 必须 reward 可导。”** 它只需要能评价 reward 和计算 log-probability 梯度。
4. **“baseline 随便依赖 action 也不影响期望。”** action-dependent baseline 通常需要额外校正。
5. **“减去平均 reward 永远是最优 baseline。”** 最优值还受 score 大小和条件结构影响。
6. **“pathwise 永远低方差。”** 这是常见经验，不是无条件定理。
7. **“Gumbel–Max 本身可导。”** 精确采样仍含 argmax；可导的是 soft relaxation。
8. **“ $\tau\to0$ 就同时得到零偏差、零方差。”** 低温会让梯度尖锐，有限样本和数值问题更严重。
9. **“straight-through 是真实链式法则。”** 它故意用 surrogate derivative，通常有偏。
10. **“reward model 可微，就能从 reward 直接反传到 sampled token。”** 离散 token 选择仍阻断普通 pathwise 梯度。
11. **“Fisher score 与 diffusion score 是同一个导数。”** 前者对参数求导，后者对样本位置求导。

## 13. 自测

1. 为什么把 $X\sim p_\theta$ 的一次样本当常数，会漏掉分布移动的梯度？
2. 从积分推导 score-function identity，并列出支持集相关的条件。
3. 对 $X=\mu+\sigma\varepsilon$，写出关于 $\mu$、 $\sigma$ 的 pathwise gradient。
4. baseline 为什么能减方差却不改期望？它允许依赖 state、为什么通常不能依赖 sampled action？
5. 完整 policy gradient 相比单步 Categorical REINFORCE 还要处理什么？
6. Gumbel–Max 与 Gumbel–Softmax 分别是精确采样还是连续松弛？
7. straight-through 的 forward 和 backward 分别用了什么？偏差来自哪里？
8. 在 VAE、RLHF 和离散 latent 三种情形中，你会先选择哪类 estimator，为什么？

## 延伸阅读

- Williams, [Simple Statistical Gradient-Following Algorithms for Connectionist Reinforcement Learning](https://doi.org/10.1007/BF00992696), 1992.
- Kingma & Welling, [Auto-Encoding Variational Bayes](https://arxiv.org/abs/1312.6114), ICLR 2014.
- Rezende, Mohamed & Wierstra, [Stochastic Backpropagation and Approximate Inference in Deep Generative Models](https://proceedings.mlr.press/v32/rezende14.html), ICML 2014.
- Schulman et al., [Gradient Estimation Using Stochastic Computation Graphs](https://arxiv.org/abs/1506.05254), 2015.
- Jang, Gu & Poole, [Categorical Reparameterization with Gumbel-Softmax](https://openreview.net/forum?id=rkE3y85ee), ICLR 2017.
- Maddison, Mnih & Teh, [The Concrete Distribution](https://openreview.net/forum?id=S1jE5L5gl), ICLR 2017.
- Bengio, Léonard & Courville, [Estimating or Propagating Gradients Through Stochastic Neurons for Conditional Computation](https://arxiv.org/abs/1308.3432), 2013.
- Tucker et al., [REBAR: Low-variance, Unbiased Gradient Estimates for Discrete Latent Variable Models](https://proceedings.neurips.cc/paper/2017/hash/ebd6d2f5d60ff9afaeda1a81fc53e2d0-Abstract.html), NeurIPS 2017.
