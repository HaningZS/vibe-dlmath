---
id: T34
type: proof-template
refined: 2026-09-28
status: self-contained-core
---

# T34. Quantitative neural-network approximation

[主题目录](README.md) · [风险分解](../generalization/T32-excess-risk-decomposition.md)

## 复用契约

**输入对象**：目标函数类、定义域、误差范数、激活函数、深度/宽度/参数个数和参数精度。

**输出结论**：给定误差需要多大的网络，或固定网络预算能保证多小的误差。

必需假设：先限定函数光滑性/结构与范数，再给构造。只知道目标连续，通常只有定性的存在性，不足以声称某个 dimension-free rate。

**失败例子**：Universal approximation 允许网络规模随误差变化，不能据此说某个固定宽度、固定精度的已训练模型能准确拟合任意目标。

## 实例化时必须完成

- [ ] 写清对哪个函数类取 supremum，对哪个网络类取 infimum。
- [ ] 记录误差范数、输入维数、边界、depth/width/weights/precision。
- [ ] 给出构造或恰当的原文定理，再独立处理 learnability。
- [ ] 从函数逼近转成任务风险时，检查 loss 的连续性或校准关系。

## 1. 三个不同的问题

“存在某个网络”“规模足够小的网络存在”“某个训练算法能找到它”依次更强。定量逼近回答第二个，通常不回答第三个。

例如可研究

$$
E_M=\sup_{f\in\mathcal F}
\inf_{h\in\mathcal H_M}\|f-h\|_\infty.
$$

$M$ 可以是非零参数数，但若允许无限精度实数，参数数并不等于描述长度，参见 [T38](../generalization/T38-compression.md)。

## 2. 一维 ReLU 的可完整构造例子

在 $[0,1]$ 上取均匀网格 $x_k=k/m$。记相邻斜率

$$
s_k=\frac{f(x_{k+1})-f(x_k)}{1/m}.
$$

线性插值可写成

$$
h_m(x)=f(0)+s_0x+
\sum_{k=1}^{m-1}(s_k-s_{k-1})\operatorname{ReLU}(x-x_k).
$$

每越过一个节点，一个新 ReLU 改变斜率；把这些“折页”拼起来，就得到插值曲线。由于 $x\geq0$，$s_0x$ 也可写为 $s_0\operatorname{ReLU}(x)$，所以标准单隐藏层网络使用至多 $m$ 个隐藏单元即可实现这段构造。

这里先使用精确实数权重。有限精度实现还需加入参数量化和数值计算造成的误差。

## 3. Lipschitz 目标的误差

若 $f$ 是 $L$-Lipschitz，令 $x=(1-t)x_k+tx_{k+1}$、$h=1/m$，则

$$
\begin{aligned}
|f(x)-h_m(x)|
&\leq(1-t)|f(x)-f(x_k)|+
t|f(x)-f(x_{k+1})|\\
&\leq2Lt(1-t)h
\leq\frac{L}{2m}.
\end{aligned}
$$

因此此构造达到 $O(m^{-1})$ 的一维 sup-norm 误差。这里只分析一维，不暗中把 $m$ 当成高维问题的总网格点数。

## 4. 二阶光滑能改进什么

若 $f\in C^2$ 且 $|f''|\leq M_2$，线性插值余项给出

$$
|f(x)-h_m(x)|
\leq\frac{M_2}{2}|(x-x_k)(x-x_{k+1})|
\leq\frac{M_2}{8m^2}.
$$

逼近率改善来自目标光滑性，而不是只来自“使用了深度学习”。

## 5. 高维与深度收益需要重新核对

Sobolev、Barron、组合结构和低维流形等函数类有不同的复杂度。深层网络可以复用中间计算，但何时打破某个浅层构造的复杂度，要用具体定理证明。

阅读 depth separation 时，至少对齐两边的深度、宽度、参数大小、输入分布、误差范数和精度。不能只比较“层数多/少”。

## 6. 连接到学习保证

若损失对预测值是 $L_\ell$-Lipschitz，且统一逼近误差为 $\epsilon$，则对同一数据 law 有风险差至多 $L_\ell\epsilon$。平方损失还要控制输出/标签范围，不能把它当全局 Lipschitz。

随后仍要分析 [T33 统计误差](../generalization/T33-uniform-convergence.md) 和优化误差，才能回到 [T32](../generalization/T32-excess-risk-decomposition.md)。

来源：[Yarotsky 的定量 ReLU 逼近](https://arxiv.org/abs/1610.01145)、[DL 数学综述](https://arxiv.org/abs/2105.04026)。上面的插值例子在本卡完整推导，不代替这些论文的高维定理。

## 本地论文与前置工具

通用工具：P01, P02，见 [证明原语](../../通用证明原语.md)。

- [Error bounds for approximations with deep ReLU networks](../../proof_ref/dl-core-2026-09/error-bounds-for-approximations-with-deep-relu-networks-1610.01145/README.md)
- [The Modern Mathematics of Deep Learning](../../proof_ref/dl-core-2026-09/the-modern-mathematics-of-deep-learning-2105.04026/README.md)

## 专项证明接口（2026-10-02）

- [T41：用表示范数与 Hilbert-space 方差控制高维随机特征的逼近误差。](T41-barron-random-feature-approximation.md)
