---
type: note
domain: math/information-geometry
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# Fisher 信息、自然梯度与信息几何

普通梯度在参数坐标里问：“参数改一点，目标变化多快？”自然梯度多问一步：“**模型所表示的概率分布究竟改变了多少？**”

类比地图：经纬度各移动 1 度不代表真实距离相同；在赤道和极地含义不同。模型参数也只是分布空间的坐标。Fisher 信息扮演局部度量尺，自然梯度用这把尺子校正方向。

这个视角连接统计估计、二阶优化、TRPO、K-FAC 和 RLHF，但工程算法通常只近似理想 Fisher 几何，不能把所有“带 KL”或“二阶预条件”的方法都叫自然梯度。

## 知识依赖与相关笔记

- 总入口：[Math 基础目录](../Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md)、[AI Researcher 数学学习路线](../AI%20Researcher%20%E6%95%B0%E5%AD%A6%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)、[AI Researcher 高阶数学路线：LLM、CV 与生成模型](../AI%20Researcher%20%E9%AB%98%E9%98%B6%E6%95%B0%E5%AD%A6%E8%B7%AF%E7%BA%BF%EF%BC%9ALLM%E3%80%81CV%20%E4%B8%8E%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B.md)。
- 梯度、Hessian：[导数、梯度、Jacobian、Hessian 与自动微分](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E5%AF%BC%E6%95%B0%E3%80%81%E6%A2%AF%E5%BA%A6%E3%80%81Jacobian%E3%80%81Hessian%20%E4%B8%8E%E8%87%AA%E5%8A%A8%E5%BE%AE%E5%88%86.md)。
- 二次型与正定矩阵：[二次型、正定矩阵与谱](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E4%BA%8C%E6%AC%A1%E5%9E%8B%E3%80%81%E6%AD%A3%E5%AE%9A%E7%9F%A9%E9%98%B5%E4%B8%8E%E8%B0%B1.md)。
- 概率、期望和似然：[概率论主干：联合、条件、期望与协方差](%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md)、[最大似然、MAP 与贝叶斯估计](%E6%9C%80%E5%A4%A7%E4%BC%BC%E7%84%B6%E3%80%81MAP%20%E4%B8%8E%E8%B4%9D%E5%8F%B6%E6%96%AF%E4%BC%B0%E8%AE%A1.md)。
- KL 散度：[信息论基础：熵、交叉熵与 KL 散度](%E4%BF%A1%E6%81%AF%E8%AE%BA%E5%9F%BA%E7%A1%80%EF%BC%9A%E7%86%B5%E3%80%81%E4%BA%A4%E5%8F%89%E7%86%B5%E4%B8%8E%20KL%20%E6%95%A3%E5%BA%A6.md)。
- 策略优化与 RLHF：[PPO math, origin and PPO-rlhf](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/LLM%20%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93/%E5%BE%AE%E8%B0%83%E4%B8%8E%E5%AF%B9%E9%BD%90/PPO%20math%2C%20origin%20and%20PPO-rlhf.md)、[DPO和PPO的区别](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/LLM%20%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93/%E5%BE%AE%E8%B0%83%E4%B8%8E%E5%AF%B9%E9%BD%90/DPO%E5%92%8CPPO%E7%9A%84%E5%8C%BA%E5%88%AB.md)、[BT model and RLHF math basic](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/LLM%20%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93/%E5%BE%AE%E8%B0%83%E4%B8%8E%E5%AF%B9%E9%BD%90/BT%20model%20and%20RLHF%20math%20basic.md)。
- diffusion 中另一种 score：[样本 score](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/ODE%E3%80%81SDE%20%E4%B8%8E%E8%BF%9E%E7%BB%AD%E6%97%B6%E9%97%B4%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B.md#7-score-based-diffusion%E5%AD%A6%E4%B9%A0%E5%AF%86%E5%BA%A6%E6%9C%9D%E5%93%AA%E9%87%8C%E4%B8%8A%E5%8D%87)。

## 1. 参数距离不等于分布距离

考虑同一个 Bernoulli 分布：

- 用成功率 $p\in(0,1)$ 参数化；
- 用 logit $\eta=\log\frac{p}{1-p}$ 参数化。

在 $p=0.5$ 附近改 $p$ 一点，与在 $p=0.999$ 附近改同样数值，对分布的可区分程度不同。换成 logit 后，参数增量的数值又完全不同。

因此欧氏长度 $\Vert d\theta\Vert_2$ 依赖坐标选择。信息几何希望定义由分布族本身诱导的局部长度，使一一光滑重参数化不改变理想的无穷小方向。

## 2. Score：对数概率对参数的敏感度

参数 score 定义为

$$
s_\theta(x)=\nabla_\theta\log p_\theta(x).
$$

它回答：观察到 $x$ 后，log likelihood 希望把参数往哪里推？

在支持集不随 $\theta$ 改变、可交换微分和积分等正则条件下：

$$
\mathbb E_{X\sim p_\theta}[s_\theta(X)]
=\int p_\theta(x)\nabla_\theta\log p_\theta(x)\thinspace dx
=\nabla_\theta\int p_\theta(x)\thinspace dx=0.
$$

如果支持集依赖参数或边界项不消失，这个等式可能失效； $\mathrm{Uniform}(0,\theta)$ 是经典反例之一。

### 2.1 不要混淆两种 score

- Fisher score： $\nabla_\theta\log p_\theta(x)$，对**参数**求导；
- diffusion score： $\nabla_x\log p_t(x)$，对**样本位置**求导。

名字相同是因为两者都是 log-density 的梯度，但变量和用途不同。

## 3. Fisher 信息矩阵

Fisher 信息定义为 score 的二阶矩：

$$
F(\theta)
=\mathbb E_{X\sim p_\theta}
\left[s_\theta(X)s_\theta(X)^\top\right].
$$

它是半正定矩阵，因为对任意向量 $v$：

$$
v^\top Fv
=\mathbb E[(v^\top s_\theta(X))^2]\ge0.
$$

只有在 regular、可辨识的参数化中，或去掉冗余方向后的商空间上， $F$ 正定时才严格给出 Riemannian metric。若 Fisher 奇异，它在原参数空间只是退化的半度量；后文会讨论 pseudoinverse 与 damping。

在更强的正则条件下还有 information equality：

$$
F(\theta)
=-\mathbb E_{p_\theta}
\left[\nabla_\theta^2\log p_\theta(X)\right].
$$

右侧是期望 log likelihood 的负曲率。等号不是任意 loss 下都成立，也不能直接把 Fisher、训练 loss Hessian 和 Gauss–Newton 矩阵混为一谈。

### 3.1 Bernoulli 例子

对 $X\sim\mathop{\mathrm{Bernoulli}}(p)$：

$$
\frac{\partial}{\partial p}\log p(X)
=\frac{X-p}{p(1-p)},
$$

因此

$$
F_p(p)=\frac1{p(1-p)}.
$$

在概率边界附近， $p$ 的微小绝对变化会让分布更容易区分，故 Fisher 变大。

改用 logit $\eta$ 后：

$$
F_\eta(\eta)=p(1-p).
$$

两个数看似相反，却通过坐标变换规则

$$
F_\eta
=\left(\frac{dp}{d\eta}\right)^2F_p
$$

表示同一局部几何。

## 4. KL 的二阶展开：Fisher 是局部度量

在正则、光滑条件下，对小增量 $d\theta$：

$$
D_{\mathrm{KL}}
\left(p_\theta\Vert p_{\theta+d\theta}\right)
=\frac12d\theta^\top F(\theta)d\theta
+o(\Vert d\theta\Vert^2).
$$

一阶项消失，因为 score 的期望为零；二阶项就是 Fisher。于是可定义无穷小长度

$$
ds^2=d\theta^\top F(\theta)d\theta.
$$

严格说 KL 本身不对称、不是距离；这里只是它在同一点附近的二阶项诱导出对称 Riemannian metric。大步更新时，局部二次近似可能很差。

## 5. Cramér–Rao：信息越多，估计可越精确

对满足正则条件的无偏估计量 $\hat\theta$，标量形式的 Cramér–Rao lower bound 为

$$
\mathop{\mathrm{Var}}(\hat\theta)
\ge\frac1{nF(\theta)}.
$$

矩阵形式用半正定序比较 covariance 与 $F^{-1}/n$。它表达单个样本 Fisher 信息可相加，更多数据能降低可达到的估计方差。

边界：有限样本有偏估计、不可辨识模型、奇异参数、支持集变化和 nuisance parameters 都需要更细版本。深度网络中的参数对称性常让 Fisher 奇异，不能机械用逆矩阵或把该下界解释成泛化保证。

## 6. 自然梯度：在固定分布变化预算下最陡

设要最小化目标 $L(\theta)$，普通梯度 $g=\nabla_\theta L$ 在欧氏球内选最陡方向。若改用局部 KL 预算：

$$
\min_{\delta}\quad g^\top\delta
\qquad
\text{s.t.}\quad
\frac12\delta^\top F\delta\le\varepsilon,
$$

Lagrange multiplier 推导给出方向

$$
\delta\propto-F^{-1}g.
$$

因此自然梯度为

$$
\widetilde\nabla_\theta L
=F(\theta)^{-1}\nabla_\theta L.
$$

它不是“总比 Adam 好的二阶优化器”，而是相对于 Fisher metric 的最陡方向。理想连续极限下，它对光滑一一重参数化具有不变性；有限步长、近似 Fisher、damping 和离散 optimizer 都会削弱这种性质。

### 6.1 Fisher 奇异怎么办

神经网络常有缩放、排列和冗余参数，使不同 $\theta$ 表示同一分布，Fisher 因而只有半正定。实践会使用：

- Moore–Penrose pseudoinverse；
- damping： $F+\lambda I$；
- trust-region 截断；
- block-diagonal、diagonal 或 Kronecker-factored 近似。

damping 改善数值稳定性，但也混入欧氏几何，因此不再是精确自然梯度。

## 7. True Fisher、empirical Fisher、Hessian 不一样

对条件模型 $p_\theta(y\mid x)$，给定某个输入分布，true Fisher 通常对模型自己的标签分布取期望：

$$
F_{\mathrm{true}}
=\mathbb E_x\mathbb E_{Y\sim p_\theta(\cdot\mid x)}
[g_Yg_Y^\top],
$$

其中 $g_Y=\nabla_\theta\log p_\theta(Y\mid x)$。

empirical Fisher 常用训练标签：

$$
F_{\mathrm{emp}}
=\frac1n\sum_i
g_{y_i}g_{y_i}^\top.
$$

它容易计算，但在模型错设、未拟合或有限样本时可与 true Fisher 差很多。NLL Hessian 还包含模型非线性产生的额外曲率项；generalized Gauss–Newton 在特定输出分布/loss 下与 Fisher 有联系，却也不是无条件相等。

K-FAC 进一步假设某些激活与反向梯度因子可分解，用 Kronecker 结构近似 Fisher blocks。它是有用的结构近似，不是精确矩阵恒等式。

## 8. TRPO：策略分布上的局部 trust region

策略 $\pi_\theta(a\mid s)$ 本身是条件分布，其 Fisher 由策略 score

$$
\nabla_\theta\log\pi_\theta(a\mid s)
$$

构造，并依赖如何对状态 $s$ 加权。

TRPO 的核心近似问题是最大化旧策略下的 surrogate improvement，同时约束新旧策略的平均 KL：

$$
\max_\theta L_{\theta_{\mathrm{old}}}(\theta)
\quad\text{s.t.}\quad
\mathbb E_{s\sim d_{\mathrm{old}}}
[D_{\mathrm{KL}}(\pi_{\mathrm{old}}\Vert\pi_\theta)]
\le\delta.
$$

在旧参数附近，把目标一阶展开、KL 二阶展开，就得到 Fisher-vector product 与自然梯度方向；conjugate gradient 无需显式存储巨大 Fisher。

严格边界：TRPO 理论中的性能界使用更强的最大状态 KL 等条件，而常用算法优化平均 KL、有限采样 surrogate，并用 line search 近似求解。函数逼近与估计误差下不能把每次更新都宣称为严格单调改进。

## 9. PPO 与 RLHF：相关，但不等于自然梯度

PPO 的 clipped surrogate 限制 probability ratio 偏离 1，希望产生 trust-region-like 行为，但它既不精确解 KL 约束，也不等于 $F^{-1}g$。clip 只能作用在采样动作及其 surrogate 上，实际 KL 仍应监控。详见 [PPO math, origin and PPO-rlhf](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/LLM%20%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93/%E5%BE%AE%E8%B0%83%E4%B8%8E%E5%AF%B9%E9%BD%90/PPO%20math%2C%20origin%20and%20PPO-rlhf.md)。

RLHF 中还常出现两种不同 KL：

- 对旧策略的 KL：控制一次 optimizer update 的 trust region；
- 对固定 reference/SFT policy 的 KL：作为任务目标中的长期行为正则。

二者参考分布和作用不同。即使实现都打印 `kl`，也不能混为一谈。DPO 则通过偏好目标与 reference policy 构造隐式正则关系，见 [DPO和PPO的区别](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/LLM%20%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93/%E5%BE%AE%E8%B0%83%E4%B8%8E%E5%AF%B9%E9%BD%90/DPO%E5%92%8CPPO%E7%9A%84%E5%8C%BA%E5%88%AB.md)。

## 10. 可运行示例：Bernoulli 的坐标不变直觉

我们拟合目标成功率 $q$，交叉熵梯度在 $p$ 与 logit $\eta$ 坐标中数值不同；自然梯度的小步更新映回分布后近似一致。

```python
import numpy as np

p = 0.25
q = 0.80
lr = 1e-3

def sigmoid(x):
    return 1.0 / (1.0 + np.exp(-x))

# L(p)=-q log p-(1-q)log(1-p)
grad_p = (p - q) / (p * (1.0 - p))
fisher_p = 1.0 / (p * (1.0 - p))
natural_grad_p = grad_p / fisher_p       # = p-q
p_new_from_p = p - lr * natural_grad_p

eta = np.log(p / (1.0 - p))
grad_eta = p - q
fisher_eta = p * (1.0 - p)
natural_grad_eta = grad_eta / fisher_eta
eta_new = eta - lr * natural_grad_eta
p_new_from_eta = sigmoid(eta_new)

print("natural step in p coordinates:", p_new_from_p)
print("natural step in eta, mapped to p:", p_new_from_eta)
assert abs(p_new_from_p - p_new_from_eta) < 1e-6

# 普通梯度依赖坐标，映回 p 后两步明显不同。
p_ordinary = p - lr * grad_p
p_from_eta_ordinary = sigmoid(eta - lr * grad_eta)
print("ordinary p-coordinate step:", p_ordinary)
print("ordinary eta-coordinate step mapped to p:", p_from_eta_ordinary)
assert abs(p_ordinary - p_from_eta_ordinary) > 1e-3

# KL 的局部二阶项约为 0.5 * F_p * dp^2。
dp = 1e-3
kl = p * np.log(p / (p + dp)) + (1.0 - p) * np.log(
    (1.0 - p) / (1.0 - p - dp)
)
quadratic = 0.5 * fisher_p * dp**2
print("exact local KL / Fisher quadratic:", kl, quadratic)
assert abs(kl - quadratic) / quadratic < 0.01
```

两种自然更新只有一阶一致，因为我们用了有限的离散步；步长变大后，坐标差异和局部 KL 近似误差都会增大。

## 11. 常见误区

1. **“Fisher 就是任意 loss 的 Hessian。”** 只有特定似然和正则条件下有相应期望等式。
2. **“empirical Fisher 是 true Fisher 的无偏通用替代。”** 标签来源和模型错设会让二者明显不同。
3. **“自然梯度完全不依赖参数化。”** 理想无穷小方向具有几何不变性；有限步与近似实现不完全具有。
4. **“Fisher 一定可逆。”** 冗余和不可辨识会使其奇异。
5. **“damping 只是无害数值技巧。”** 它改变方向，也引入欧氏度量成分。
6. **“PPO clipping 就是 TRPO 或自然梯度。”** PPO 是一阶 surrogate 启发式，不显式乘 $F^{-1}$。
7. **“RLHF 里的 reference KL 就是 old-policy trust region。”** 一个约束长期偏离参考模型，一个控制单次更新，角色不同。
8. **“diffusion score 就是 Fisher score。”** 求导变量分别是样本和参数。
9. **“Fisher 大表示模型一定更好。”** 它描述局部可区分性/估计信息，不是任务质量分数。

## 12. 自测

1. 推导在正则条件下 score 期望为何为零；支持集依赖参数时哪一步会坏？
2. Bernoulli 的 Fisher 在 $p$ 坐标和 logit 坐标为何数值相反，却表示同一几何？
3. 从局部 KL 约束推导自然梯度方向 $-F^{-1}g$。
4. true Fisher、empirical Fisher 与 NLL Hessian 分别对什么取期望或求导？
5. TRPO 的实际算法为什么不能无条件继承理论单调改进保证？
6. PPO clipping 与 reference-policy KL 分别限制什么？
7. 深度网络 Fisher 奇异时，pseudoinverse 与 damping 各有什么代价？

## 延伸阅读

- Amari, [Natural Gradient Works Efficiently in Learning](https://doi.org/10.1162/089976698300017746), *Neural Computation*, 1998.
- Amari & Nagaoka, *Methods of Information Geometry*, 2000.
- Kakade, [A Natural Policy Gradient](https://proceedings.neurips.cc/paper/2001/hash/4b86abe48d358ecf194c56c69108433e-Abstract.html), NeurIPS 2001.
- Schulman et al., [Trust Region Policy Optimization](https://proceedings.mlr.press/v37/schulman15.html), ICML 2015.
- Martens & Grosse, [Optimizing Neural Networks with Kronecker-factored Approximate Curvature](https://proceedings.mlr.press/v37/martens15.html), ICML 2015.
