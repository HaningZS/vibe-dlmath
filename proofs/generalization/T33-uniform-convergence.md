---
id: T33
type: proof-template
refined: 2026-09-28
status: self-contained-core
---

# T33. Uniform convergence, Rademacher complexity and covering

[主题目录](README.md) · [风险分解](T32-excess-risk-decomposition.md)

## 复用契约

**输入对象**： $S\sim\mathcal D^n$、预先固定的非空 loss class $\mathcal G\subseteq[0,1]^{\mathcal Z}$。假设涉及的 supremum 可测，例如使用可数或适当可分的类。

**输出结论**：同一事件上对整个类成立的 population–empirical deviation，允许训练后从该类选模型。

**失败例子**：在同一数据上训练特征提取器后，只把最后一层当成预先固定的类，会漏掉特征选择的数据依赖。

## 实例化时必须完成

- [ ] 规定类、损失范围、采样 law 与 supremum 的可测性。
- [ ] 统一 Rademacher 的 $1/n$、单侧/绝对值等约定。
- [ ] 证明 complexity 上界，而非只写“由 Rademacher 可得”。
- [ ] 调参、类选择、多个 margin 或 norm 半径需要统一事件/独立数据/复杂度预算。

## 1. 从固定候选到有限候选

对固定 $g$，Hoeffding 给出

$$
\Pr(|Pg-P_ng|>\epsilon)\leq2e^{-2n\epsilon^2}.
$$

若类有 $M$ 个函数，union bound 给出

$$
\sup_{g\in\mathcal G}|Pg-P_ng|
\leq \sqrt{\frac{\log(2M/\delta)}{2n}}
$$

以概率至少 $1-\delta$ 同时成立。候选多，会增加“偶然找到一个训练误差很低的函数”的机会。

## 2. 无限类用随机符号衡量可拟合噪声的能力

本卡固定单侧约定：

$$
\widehat{\mathfrak R}_S(\mathcal G)
=\mathbb E_\sigma\sup_{g\in\mathcal G}\frac1n\sum_i\sigma_i g(Z_i),
\qquad \mathfrak R_n=\mathbb E_S\widehat{\mathfrak R}_S.
$$

$\sigma_i$ 独立、均匀取 $\{-1,1\}$。这个定义不在 supremum 内加绝对值。

引入独立 ghost sample $S'$，由 Jensen 与成对样本交换对称性，

$$
\begin{aligned}
\mathbb E\sup_g(Pg-P_ng)
&\leq \mathbb E\sup_g(P_n'g-P_ng)\\
&=\mathbb E\sup_g\frac1n\sum_i\sigma_i(g(Z_i')-g(Z_i))\\
&\leq2\mathfrak R_n(\mathcal G).
\end{aligned}
$$

最后一步将两部分 supremum 分开，并利用随机符号对称性。

## 3. 从期望到高概率

改变一个样本， $\sup_g(Pg-P_ng)$ 至多改变 $1/n$。McDiarmid 因而给出

$$
\forall g\in\mathcal G:\quad
Pg\leq P_ng+2\mathfrak R_n(\mathcal G)
+\sqrt{\frac{\log(1/\delta)}{2n}}
$$

的概率至少为 $1-\delta$。

另一侧对 $-\mathcal G$ 处理；其函数取值范围长度仍为 1，且 Rademacher complexity 相同。分配 $\delta/2$ 后，

$$
\sup_g|Pg-P_ng|
\leq2\mathfrak R_n(\mathcal G)+
\sqrt{\frac{\log(2/\delta)}{2n}}.
$$

若想使用观测样本上的 $\widehat{\mathfrak R}_S$，还需控制它的波动。分别对单侧 deviation 和 $\mathfrak R_n-\widehat{\mathfrak R}_S$ 分配 $\delta/2$，可得常见的单侧经验版本：

$$
Pg\leq P_ng+2\widehat{\mathfrak R}_S+
3\sqrt{\frac{\log(2/\delta)}{2n}}\quad(\forall g).
$$

三项中的常数来自这两次浓缩；不能不加说明地与带绝对值的另一套定义混用。

## 4. 怎样真正计算复杂度

先控制预测函数类，再用 Lipschitz contraction 连接 loss class。标量 loss 应采用与本卡单侧定义匹配的版本，并按需要中心化；带绝对值版本可能多一个常数。

另一种路线是做 $\epsilon$-net。若使用总体一致的 sup-norm cover，且覆盖误差至多 $\epsilon$，则

$$
\sup_{g\in\mathcal G}|Pg-P_ng|
\leq\max_{g_j\in\mathcal N_\epsilon}|Pg_j-P_ng_j|+2\epsilon.
$$

有限 net 的部分再 union bound。仅在训练点上近似好的 empirical cover，不能未经处理就控制总体积分；通常应在 symmetrized process 中使用对应 covering/chaining 定理。

## 5. 与深度学习的关系和边界

参数数量可以给粗的 VC/pseudo-dimension 控制，但 norm、margin、谱结构或压缩有时更适合具体网络。全局 uniform bound 空泛时，应考虑局部 complexity、算法稳定性或其他有条件路线，而不是隐藏大常数。

非 i.i.d.、在线适应采样、用同一数据选择函数类都需要新工具。

前置：[经验过程与 contraction](<../../Math 基础/统计学习理论/算法稳定性、经验过程与 PAC-Bayes.md>)。后续：[T35 间隔](T35-margin-norm.md)、[T38 压缩](T38-compression.md)、[T32 总风险](T32-excess-risk-decomposition.md)。

综述：[The Modern Mathematics of Deep Learning](https://arxiv.org/abs/2105.04026)。本卡给出基础 bounded-loss 证明，不将其视为所有现代网络的紧泛化解释。

## 本地论文与前置工具

通用工具：P04, P09，见 [证明原语](../../通用证明原语.md)。

- [The Modern Mathematics of Deep Learning](../../proof_ref/dl-core-2026-09/the-modern-mathematics-of-deep-learning-2105.04026/README.md)
- [Spectrally-normalized margin bounds for neural networks](../../proof_ref/dl-core-2026-09/spectrally-normalized-margin-bounds-for-neural-networks-1706.08498/README.md)

## 专项证明接口（2026-10-02）

- [T41：用表示范数与 Hilbert-space 方差控制高维随机特征的逼近误差。](../deep-learning/T41-barron-random-feature-approximation.md)
- [T43：以群作用和层间恒等式证明等变性，并核对 attention 的位置与 mask。](../deep-learning/T43-equivariance-symmetry.md)
- [T44：通过 1-WL 归纳和具体图对证明消息传递 GNN 的表达力限制。](../lower-bounds-expressivity/T44-message-passing-wl.md)
- [T49：由 binary log-loss excess 推到分类 excess，并保留模型与裁剪误差。](T49-surrogate-bayes-risk.md)

## 经典与近期证明蒸馏

- [T50：用指数距离上包络把观测证书接到总体期望，保持量词与选择预算。](T50-data-dependent-certificate-envelope.md)
- [T51：在真实边缘分布下控制速度误差，用学习场 Lipschitz 与耦合推出 Wasserstein 界。](../generation-transport/T51-flow-trajectory-error.md)
- [经典编码界与数据依赖解码器](../../extensions/%E7%BB%8F%E5%85%B8%E7%BC%96%E7%A0%81%E7%95%8C%E4%B8%8E%E6%95%B0%E6%8D%AE%E4%BE%9D%E8%B5%96%E8%A7%A3%E7%A0%81%E5%99%A8.md)
