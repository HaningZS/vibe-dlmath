---
type: note
domain: math/calculus
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# 矩阵微分、Trace Trick 与反向传播

先抓住一句话：

> 矩阵求导最稳的方法不是背“分子布局还是分母布局”，而是先问最终输出是不是标量，再写它的一阶微小变化，把所有变化量整理到同一个位置，最后读出梯度。

在 LLM/CV 论文里，参数天然是矩阵或张量。直接逐元素求导虽然可行，却很快被下标淹没。微分与 trace trick 的作用，是把大量逐元素链式法则压缩成形状清楚的矩阵表达式。

## 知识依赖与相关笔记

- 总入口：[AI Researcher 数学学习路线](../AI%20Researcher%20%E6%95%B0%E5%AD%A6%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)、[AI Researcher 高阶数学路线：LLM、CV 与生成模型](../AI%20Researcher%20%E9%AB%98%E9%98%B6%E6%95%B0%E5%AD%A6%E8%B7%AF%E7%BA%BF%EF%BC%9ALLM%E3%80%81CV%20%E4%B8%8E%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B.md)、[Math 基础目录](../Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md)。
- 先修：[导数、梯度、Jacobian、Hessian 与自动微分](%E5%AF%BC%E6%95%B0%E3%80%81%E6%A2%AF%E5%BA%A6%E3%80%81Jacobian%E3%80%81Hessian%20%E4%B8%8E%E8%87%AA%E5%8A%A8%E5%BE%AE%E5%88%86.md)、[向量空间、基、秩与 SVD](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E5%90%91%E9%87%8F%E7%A9%BA%E9%97%B4%E3%80%81%E5%9F%BA%E3%80%81%E7%A7%A9%E4%B8%8E%20SVD.md)。
- 二次型与最小二乘：[二次型、正定矩阵与谱](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E4%BA%8C%E6%AC%A1%E5%9E%8B%E3%80%81%E6%AD%A3%E5%AE%9A%E7%9F%A9%E9%98%B5%E4%B8%8E%E8%B0%B1.md)、[投影、最小二乘与伪逆](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E6%8A%95%E5%BD%B1%E3%80%81%E6%9C%80%E5%B0%8F%E4%BA%8C%E4%B9%98%E4%B8%8E%E4%BC%AA%E9%80%86.md)。
- 代码表达：[Einsum](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0%E5%B7%A5%E7%A8%8B/PyTorch/Einsum.md)、[神经网络训练闭环：前向、反向与优化](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0%E5%B7%A5%E7%A8%8B/PyTorch/%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C%E8%AE%AD%E7%BB%83%E9%97%AD%E7%8E%AF%EF%BC%9A%E5%89%8D%E5%90%91%E3%80%81%E5%8F%8D%E5%90%91%E4%B8%8E%E4%BC%98%E5%8C%96.md)。
- 后续：[Fisher 信息、自然梯度与信息几何](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/Fisher%20%E4%BF%A1%E6%81%AF%E3%80%81%E8%87%AA%E7%84%B6%E6%A2%AF%E5%BA%A6%E4%B8%8E%E4%BF%A1%E6%81%AF%E5%87%A0%E4%BD%95.md)、[积分、变量替换与概率密度变换](%E7%A7%AF%E5%88%86%E3%80%81%E5%8F%98%E9%87%8F%E6%9B%BF%E6%8D%A2%E4%B8%8E%E6%A6%82%E7%8E%87%E5%AF%86%E5%BA%A6%E5%8F%98%E6%8D%A2.md)。

## 1. 先固定约定：标量对矩阵的梯度与原矩阵同形状

本篇采用深度学习中常见约定：若

$$
f:\mathbb R^{m\times n}\to\mathbb R,
$$

则梯度 $\nabla_X f$ 与 $X$ 同形状，并满足

$$
df=\langle\nabla_X f,dX\rangle_F
=\operatorname{tr}\big((\nabla_X f)^\top dX\big).
$$

这里 $dX$ 表示给 $X$ 一个任意的无穷小扰动，Frobenius 内积为

$$
\langle A,B\rangle_F=\operatorname{tr}(A^\top B)
=\sum_{ij}A_{ij}B_{ij}.
$$

因此求导的目标变成：把 $df$ 整理成

$$
df=\operatorname{tr}(G^\top dX),
$$

然后读出 $\nabla_X f=G$。

不同教材对向量到向量 Jacobian 可能采用互为转置的布局。不要争论哪个“唯一正确”，先检查线性近似与形状是否一致。

## 2. 为什么 trace 能帮忙

任何标量都等于自己的 trace。trace 还允许循环移动矩阵乘积：

$$
\operatorname{tr}(ABC)
=\operatorname{tr}(BCA)
=\operatorname{tr}(CAB).
$$

注意只能**循环移动**，不能随意交换次序。一般而言 $AB\ne BA$。

trace trick 的核心是把 $dX$ 转到表达式末尾，并把其余部分整理成某个矩阵的转置：

$$
\operatorname{tr}(A\,dX\,B)
=\operatorname{tr}(BA\,dX).
$$

一旦写成 $\operatorname{tr}(G^\top dX)$，梯度就是 $G$。

## 3. 最基础的例子：线性函数

令

$$
f(X)=\operatorname{tr}(A^\top X).
$$

微分为

$$
df=\operatorname{tr}(A^\top dX),
$$

所以

$$
\nabla_Xf=A.
$$

这和普通向量函数 $f(x)=a^\top x$ 的梯度是 $a$ 完全一致。

## 4. 二次型：为什么非对称矩阵会出现 $A+A^\top$

令

$$
f(x)=x^\top Ax.
$$

使用乘积法则：

$$
df=(dx)^\top Ax+x^\top A\,dx.
$$

第一项是标量，可以转置：

$$
(dx)^\top Ax=x^\top A^\top dx.
$$

于是

$$
df=x^\top(A^\top+A)dx
=\big((A+A^\top)x\big)^\top dx,
$$

所以

$$
\nabla_x f=(A+A^\top)x.
$$

若 $A$ 对称，才可简化为 $2Ax$。看到 $\nabla(x^\top Ax)=2Ax$ 时，必须检查对称性前提。

## 5. 最小二乘的矩阵梯度

令

$$
f(X)=\frac12\|AX-B\|_F^2.
$$

设残差 $R=AX-B$，则

$$
f=\frac12\operatorname{tr}(R^\top R).
$$

微分：

$$
df=\operatorname{tr}(R^\top dR)
=\operatorname{tr}(R^\top A\,dX)
=\operatorname{tr}\big((A^\top R)^\top dX\big).
$$

因此

$$
\nabla_X f=A^\top(AX-B).
$$

这就是线性层反向传播里不断出现的“上游误差乘输入或权重转置”的来源。

## 6. 链式法则不要求显式形成巨大 Jacobian

若 $Y=g(X)$、 $L=f(Y)$，完整 Jacobian 可能有四个甚至更多索引。实际自动微分通常计算：

- **JVP**： $J_g(X)v$，问输入沿 $v$ 变化时输出怎样变；
- **VJP**： $u^\top J_g(X)$，把上游梯度从输出拉回输入。

标量损失对海量参数的训练适合反向模式，因为最终只需 VJP，不需要存下完整 Jacobian。

所以“反向传播会构造每一层完整 Jacobian”通常是误解。框架为每个基本算子实现局部 backward，再把 VJP 沿图反向组合。

## 7. Softmax Jacobian：一个输出会影响所有类别

对

$$
p_i=\frac{e^{z_i}}{\sum_j e^{z_j}},
$$

有

$$
\frac{\partial p_i}{\partial z_j}
=p_i(\delta_{ij}-p_j).
$$

矩阵形式为

$$
J_{\text{softmax}}(z)
=\operatorname{diag}(p)-pp^\top.
$$

对角项为正，非对角项为负：提高一个 logit 不只提高自己的概率，还会通过归一化压低其他类别。

实践中 softmax 与 cross-entropy 常融合求导。对 one-hot 标签 $y$，单样本 logits 梯度简化为

$$
\nabla_z L=p-y.
$$

这个简洁结果来自 softmax Jacobian 与 NLL 链式法则的抵消，不表示 softmax 本身“没有 Jacobian”。

## 8. Attention 的形状检查比背公式更重要

单头 attention 写成

$$
S=\frac{QK^\top}{\sqrt d},
\qquad
P=\operatorname{softmax}_{\text{row}}(S),
\qquad
O=PV.
$$

若 $Q,K\in\mathbb R^{n\times d}$、 $V\in\mathbb R^{n\times d_v}$，则：

- $S,P\in\mathbb R^{n\times n}$；
- $O\in\mathbb R^{n\times d_v}$。

反向时， $O=PV$ 首先给出

$$
dO=dP\,V+P\,dV.
$$

因此上游梯度会同时流向注意力权重 $P$ 和 value $V$；再经过 row-wise softmax 与 $QK^\top$ 流回 $Q,K$。真实实现会批量化、分头并融合 kernel，但形状逻辑不变。

## 9. Log-determinant：变量替换和高斯似然中的高频导数

对可逆矩阵 $X$，在相应定义域内：

$$
d\log|\det X|
=\operatorname{tr}(X^{-1}dX),
$$

因此

$$
\nabla_X\log|\det X|=X^{-\top}.
$$

若 $X$ 是对称正定矩阵，可写成 $X^{-1}$。实现中不要为了得到这个结果就显式求逆；线性求解和 Cholesky 通常更稳定，见 [浮点数、数值稳定性与条件数](../%E6%95%B0%E5%80%BC%E8%AE%A1%E7%AE%97/%E6%B5%AE%E7%82%B9%E6%95%B0%E3%80%81%E6%95%B0%E5%80%BC%E7%A8%B3%E5%AE%9A%E6%80%A7%E4%B8%8E%E6%9D%A1%E4%BB%B6%E6%95%B0.md)。

这个公式会在 Gaussian log-likelihood、normalizing flow 和协方差优化中反复出现。

## 10. 广播与 reduction 是工程求导的隐藏部分

假设 $Y=X+b$，其中 $X$ 是 batch 矩阵， $b$ 沿 batch 维广播。前向看似只是加法，反向对 $b$ 的梯度却要沿所有被广播的维度求和。

同样，loss 使用 `sum` 还是 `mean` 会让梯度相差 batch size 等比例。数学推导与代码对不上时，优先检查：

- shape 与 transpose；
- broadcasting；
- sum/mean reduction；
- batch、token、head 维分别在哪里；
- 实现是否融合了 softmax、NLL 或 normalization。

## 11. 可运行示例：用方向导数检查矩阵梯度

```python
import numpy as np

rng = np.random.default_rng(0)
A = rng.normal(size=(5, 3))
X = rng.normal(size=(3, 2))
B = rng.normal(size=(5, 2))
direction = rng.normal(size=X.shape)

def loss(x):
    residual = A @ x - B
    return 0.5 * np.sum(residual**2)

analytic_gradient = A.T @ (A @ X - B)

# 任意方向 H 上，方向导数应等于 <grad, H>_F。
epsilon = 1e-6
finite_difference = (
    loss(X + epsilon * direction)
    - loss(X - epsilon * direction)
) / (2.0 * epsilon)
gradient_prediction = np.sum(analytic_gradient * direction)

print("finite difference:", finite_difference)
print("gradient inner product:", gradient_prediction)
assert np.allclose(finite_difference, gradient_prediction, rtol=1e-6, atol=1e-7)

# 检查 softmax Jacobian 的行和为 0：所有 logits 同加常数，概率不变。
z = np.array([0.2, -0.3, 1.1])
p = np.exp(z - z.max())
p /= p.sum()
softmax_jacobian = np.diag(p) - np.outer(p, p)
assert np.allclose(softmax_jacobian @ np.ones_like(z), 0.0)
```

方向导数检查一次覆盖整个梯度，比逐元素检查更便宜；若失败，再缩小到具体坐标排查。epsilon 太大有截断误差，太小会被浮点消减吞掉，因此应尝试多个数量级。

## 常见误区

1. **“矩阵导数公式在所有资料中形状都一样。”** Jacobian 布局约定可能不同，先检查微分关系和形状。
2. **“trace 里可以随意交换矩阵顺序。”** 只能循环移动，不能一般地交换。
3. **“ $x^\top Ax$ 的梯度永远是 $2Ax$。”** 只有对称 $A$ 才如此。
4. **“自动微分不用理解矩阵微分。”** autograd 会算，但研究者仍需检查目标、形状、reduction 和数值是否符合意图。
5. **“反向传播要存完整 Jacobian。”** 通常直接组合 VJP。
6. **“有限差分通过就证明所有点都正确。”** 它只检查当前输入与方向，还受 epsilon 和浮点误差影响。
7. **“写出 $X^{-1}$ 就应该在代码里求逆。”** 公式表达与数值实现要分开。

## 自测

1. 用微分推导 $f(W)=\tfrac12\|Wx-y\|_2^2$ 对 $W$ 的梯度。
2. 为什么 $\operatorname{tr}(ABC)=\operatorname{tr}(BCA)$，却不能说 $ABC=CBA$？
3. softmax Jacobian 乘全 1 向量为何得到 0？
4. batch mean 改成 batch sum，梯度尺度怎样变化？
5. attention 的 $QK^\top$ 对 $Q$ 和 $K$ 的梯度形状各是什么？

## 延伸阅读

- Petersen & Pedersen, [*The Matrix Cookbook*](https://www.math.uwaterloo.ca/~hwolkowi/matrixcookbook.pdf)。
- Magnus & Neudecker, *Matrix Differential Calculus with Applications in Statistics and Econometrics*, 3rd ed.。
- Baydin et al., [Automatic Differentiation in Machine Learning: a Survey](https://jmlr.org/papers/v18/17-468.html), JMLR 2018。
- Parr & Howard, [The Matrix Calculus You Need For Deep Learning](https://explained.ai/matrix-calculus/)。
- Vaswani et al., [Attention Is All You Need](https://arxiv.org/abs/1706.03762), 2017。
