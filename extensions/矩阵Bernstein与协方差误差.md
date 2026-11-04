# 矩阵 Bernstein 与协方差误差

[返回专题目录](README.md) · [原证明模板](../proofs/README.md)

前置：[正定与谱](<../Math 基础/线性代数/二次型、正定矩阵与谱.md>)、[矩阵浓缩与谱扰动](<../Math 基础/线性代数/矩阵浓缩、谱扰动与子空间误差.md>)。

## 1. 一张矩阵的误差，为什么不能只逐元素看

假设模型用样本协方差 $\widehat\Sigma$ 来做 whitening 或判断一个子空间。每个元素都只错一点，某个方向上的误差仍可能累积。

operator norm 回答的是：在所有单位方向中，最坏的放大误差有多大？

对对称矩阵 $E$，

$$
\|E\|_{\mathrm{op}}=\sup_{\|u\|=1}|u^\top E u|.
$$

矩阵 Bernstein 控制随机矩阵和的这个最坏方向偏差。

## 2. 标准结论的合同

设 $X_1,\ldots,X_n$ 是独立、零均值、 $d\times d$ 自伴矩阵，且几乎处处

$$
\|X_i\|_{\mathrm{op}}\leq R.
$$

定义方差代理

$$
v=\left\|\sum_i\mathbb E[X_i^2]\right\|_{\mathrm{op}}.
$$

一个常用双侧版本为

$$
\Pr\!\left(\left\|\sum_iX_i\right\|_{\mathrm{op}}\geq t\right)
\leq2d\exp\!\left(-\frac{t^2}{2(v+Rt/3)}\right).
$$

不要把 $X_i^2$ 理解成逐元素平方；这里是矩阵乘法。也不要把仅有有限二阶矩写成“满足有界矩阵 Bernstein”。

它背后的矩阵 Laplace-transform 证明需要处理矩阵不交换性，不能把标量证明中的指数任意拆开。本篇使用这一标准结论，重点展示怎样把真实问题变成它的输入。

## 3. 两个尺度的直觉

当 $t$ 相对 $v/R$ 较小时，分母主要由 $v$ 决定，尾界近似 Gaussian：

$$
\exp(-t^2/(2v)).
$$

当 $t$ 很大时， $Rt$ 主导，呈近似 exponential 尾。

所以最终误差常有两项： $\sqrt{v\log(d/\delta)}$ 与 $R\log(d/\delta)$。前者是方差累积，后者是单个样本可能造成的最大冲击。

## 4. 把样本协方差写成随机矩阵和

设 $x_i$ 独立同分布、 $\mathbb E x_i=0$、 $\|x_i\|_2\leq K$，并定义

$$
\Sigma=\mathbb E[x_ix_i^\top],\qquad
\widehat\Sigma=\frac1n\sum_ix_ix_i^\top.
$$

令

$$
X_i=x_ix_i^\top-\Sigma.
$$

则 $\mathbb E X_i=0$，且

$$
n(\widehat\Sigma-\Sigma)=\sum_iX_i.
$$

接下来只需逐项核对独立性、 $R$ 与 $v$。

## 5. 控制单次冲击与方差

因为 $0\preceq x_ix_i^\top\preceq K^2I$ 且 $0\preceq\Sigma\preceq K^2I$，

$$
-K^2I\preceq X_i\preceq K^2I,\qquad R=K^2.
$$

再令 $A=x_ix_i^\top$。由于 $A^2=\|x_i\|^2A\preceq K^2A$，

$$
\mathbb E X_i^2
=\mathbb E A^2-\Sigma^2
\preceq\mathbb E A^2
\preceq K^2\Sigma.
$$

因此 $v\leq nK^2\|\Sigma\|_{\mathrm{op}}$。

注意：矩阵有序关系允许这里的上界； $\mathbb E A^2-\Sigma^2$ 不是把所有交叉项都随意丢掉，而是利用 $\mathbb E A=\Sigma$ 展开得到。

## 6. 最终误差界

取 $\ell=\log(2d/\delta)$。由 Bernstein 的反解，一个便利但稍松的高概率界是

$$
\|\widehat\Sigma-\Sigma\|_{\mathrm{op}}
\leq
\sqrt{\frac{2K^2\|\Sigma\|_{\mathrm{op}}\ell}{n}}
+\frac{2K^2\ell}{3n}.
$$

第一项按 $n^{-1/2}$ 衰减，第二项按 $n^{-1}$ 衰减。它们使你能够检查某个 eigengap 是否足以支撑下游子空间估计。

再接 Weyl 或 Davis–Kahan 时，要另外满足各自的对称性与 gap 条件。协方差估计准确并不自动意味着很小的特征值可以稳定求逆。

## 7. 哪些数据不能直接用这段证明

- Gaussian 向量没有有限的 almost-sure $K$，需要 sub-Gaussian covariance concentration 或 truncation 分析。
- 视频连续帧常相关，需要依赖过程的工具，不能视为独立样本。
- 如果均值未知并用样本均值中心化，要额外控制均值误差。
- 学出的 feature encoder 若使用了同一批数据，独立性/条件化方式也要重新检查。

自测： $v$ 是逐元素方差之和吗？不是，它是矩阵二阶矩和的 operator norm，控制最坏方向的随机波动。

## 论文

- Tropp：[User-Friendly Tail Bounds](https://arxiv.org/abs/1004.4389)；
- Tropp：[An Introduction to Matrix Concentration Inequalities](https://arxiv.org/abs/1501.01571)；
- Vershynin：[Non-asymptotic Analysis of Random Matrices](https://arxiv.org/abs/1011.3027)。

本地阅读卡见 [concentration 论文目录](../PAPERS.md#concentration)。
