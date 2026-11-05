---
status: canonical
reviewed: 2026-08-24
---

# Lipschitz 连续性与 Lipschitz 常数

Lipschitz 条件给函数的变化速度一个**全局线性上界**。

> [!tip] 优化连接
> 为什么梯度的 Lipschitz 常数会限制安全学习率，见 [梯度下降、学习率与收敛](%E6%A2%AF%E5%BA%A6%E4%B8%8B%E9%99%8D%E3%80%81%E5%AD%A6%E4%B9%A0%E7%8E%87%E4%B8%8E%E6%94%B6%E6%95%9B.md)；凸性前提见 [凸集、凸函数与优化直觉](%E5%87%B8%E9%9B%86%E3%80%81%E5%87%B8%E5%87%BD%E6%95%B0%E4%B8%8E%E4%BC%98%E5%8C%96%E7%9B%B4%E8%A7%89.md)。

## 定义

给定带范数的空间，若存在有限常数 $L\ge0$，使定义域内任意 $x,y$ 都满足

$$
\Vert f(x)-f(y)\Vert\le L\Vert x-y\Vert,
$$

则称 $f$ 是 $L$-Lipschitz 的。所有可行 $L$ 的下确界称为最优 Lipschitz 常数：

$$
\mathop{\mathrm{Lip}}(f)
=\sup_{x\ne y}\frac{\Vert f(x)-f(y)\Vert}{\Vert x-y\Vert}.
$$

“ $f$ 是 1-Lipschitz”通常表示可取 $L=1$，即 $\mathop{\mathrm{Lip}}(f)\le1$，并不要求最优常数恰好等于 1。

Lipschitz 连续蕴含一致连续，但反过来不总成立。

## 与导数的关系

在实数区间上，若 $f$ 可微且 $|f'(x)|\le L$，由中值定理可知 $f$ 是 $L$-Lipschitz 的。

在凸域 $D\subset\mathbb R^n$ 上，若 $f$ 可微且

$$
\sup_{x\in D}\Vert J_f(x)\Vert_{\mathrm{op}}\le L,
$$

则 $f$ 在该域上是 $L$-Lipschitz 的。这里必须说明输入、输出所用的范数，因为算子范数随范数选择而变。

例子：

- $f(x)=3x+5$ 在 $\mathbb R$ 上的最优常数是 3；
- $f(x)=\sin x$ 的最优常数是 1；
- $f(x)=x^2$ 在整个 $\mathbb R$ 上不是 Lipschitz，但在 $[0,3]$ 上可取 $L=6$。

## 复合与神经网络

若 $f$ 是 $L_f$-Lipschitz， $g$ 是 $L_g$-Lipschitz，则

$$
\mathop{\mathrm{Lip}}(f\circ g)\le L_fL_g.
$$

线性映射 $x\mapsto Wx$ 在欧氏范数下的 Lipschitz 常数是谱范数 $\Vert W\Vert_2$。因此，对

$$
F(x)=\sigma(Wx+b),
$$

有

$$
\mathop{\mathrm{Lip}}(F)\le \mathop{\mathrm{Lip}}(\sigma)\Vert W\Vert_2.
$$

这只是上界；上界大于 1 不代表真实常数一定大于 1。

## 压缩映射与不动点

Banach 不动点定理要求：

1. $F$ 把一个完备度量空间映射回自身；
2. 存在统一常数 $0\le q<1$，使 $d(F(x),F(y))\le qd(x,y)$。

在这些条件下，迭代 $x_{k+1}=F(x_k)$ 收敛到唯一不动点。仅让某个激活函数的斜率小于 1 不够；必须控制**整个迭代映射**。

例如 $F(x)=0.5\thinspace\mathrm{ReLU}(3x)$ 在正半轴等于 $1.5x$，从正初值出发会发散。

## ODE 中的作用

从存在唯一性走到 Euler solver、SDE、diffusion 与 flow matching，见 [ODE、SDE 与连续时间生成模型](ODE%E3%80%81SDE%20%E4%B8%8E%E8%BF%9E%E7%BB%AD%E6%97%B6%E9%97%B4%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B.md)。

Picard–Lindelöf 定理的一种常见表述是：对初值问题

$$
y'(t)=f(t,y),\qquad y(t_0)=y_0,
$$

若 $f$ 在局部对 $t$ 连续，并对状态变量 $y$ 局部 Lipschitz，则可得到局部解的存在与唯一性。不能只写成“函数满足 Lipschitz 就保证所有 ODE 有唯一全局解”。

## WGAN 中的作用

Kantorovich–Rubinstein 对偶要求 critic 位于 1-Lipschitz 函数类中。常见实现只是近似施加该约束：

- 原始 WGAN 使用权重裁剪；
- WGAN-GP 在真假样本插值点上惩罚 critic 对输入的梯度范数偏离 1。

WGAN-GP 不等于限制每个权重矩阵的范数，也不能据此声称网络在整个输入空间上被严格证明为 1-Lipschitz。

## 来源

- [Wasserstein GAN](https://arxiv.org/abs/1701.07875)
- [Improved Training of Wasserstein GANs](https://arxiv.org/abs/1704.00028)
