---
id: T41
type: proof-template
refined: 2026-10-02
status: self-contained-core
---

# T41. Barron 型表示、随机特征与高维逼近

[主题目录](README.md) · [定量逼近 T34](T34-neural-approximation.md) · [学习闭环例子](../../docs/END_TO_END_LEARNING_PROOF.md)

## 复用契约

**对象**：固定输入 law $P_X$；可测特征 $\psi_\theta$ 和有限 signed measure $\nu$，满足
$f_*(x)=\int\psi_\theta(x)d\nu(\theta)$。令 $V=|\nu|(\Theta)>0$，要求 $\|\psi_\theta\|_{L^2(P_X)}\le1$，随机特征为可积的 Hilbert-valued 对象。

**结论**：存在宽度 $m$ 的有限特征和，平方 $L^2$ 逼近误差不超过 $V^2/m$；随机抽取时期望同样受控。本卡使用表示的 variation norm，不宣称它与所有文献的 Fourier/Barron 范数定义完全相同。

**失败例子**： $V=V(d)$ 可随输入维度快速增加；式子没有显式 $d$ 不表示所有高维函数都容易学习。

## 实例化时必须完成

- [ ] 给出真实表示与特征归一化，或证明目标属于对应函数空间。
- [ ] 对齐 $L^2(P_X)$、uniform、Sobolev 等误差范数。
- [ ] 若随机特征随后用训练数据选择，重新处理数据依赖。
- [ ] 参数精度、特征计算成本、训练和统计误差分别记账。

## 1. 直觉：积分是一袋无限多的小积木

积分表示把函数写成很多简单特征的加权平均。宽度 $m$ 的网络只拿 $m$ 块积木。若这袋积木的总重量有限，抽样平均的误差就像 Monte Carlo，一般按 $1/\sqrt m$ 衰减。

与规则网格逐维切分不同，这个界由“目标需要多重的一袋积木”控制。难度被放进表示范数和特征族，不能省略。

## 2. 把 signed measure 改写为随机变量

写 $d\nu=s(\theta)d|\nu|$，实数情形 $s\in\{-1,1\}$ 在非零部分成立。令 $\theta\sim|\nu|/V$，则

$$
Z(x)=V s(\theta)\psi_\theta(x),\qquad \mathbb EZ=f_*.
$$

独立抽取 $Z_1,\ldots,Z_m$，构造 $f_m=m^{-1}\sum_jZ_j$。它是一个固定有限宽特征模型；若 $\psi$ 是归一化 ReLU，它就是两层 ReLU 表示。

## 3. 完整的 Hilbert-space 方差计算

独立性和中心化消掉交叉项：

$$
\mathbb E\|f_m-f_*\|_{L^2}^2
=\frac1m\mathbb E\|Z-f_*\|_{L^2}^2
=\frac{\mathbb E\|Z\|_{L^2}^2-\|f_*\|_{L^2}^2}{m}
\le\frac{V^2}{m}.
$$

所以至少存在一次抽样实现该误差界。随机特征若要带置信度，最基础的 Markov 界为

$$
\Pr\!\left(\|f_m-f_*\|_{L^2}^2>\frac{V^2}{m\delta_A}\right)\le\delta_A.
$$

这是较弱但自包含的 $1/\delta_A$ 界；更强尾界需要额外条件与工具，不能把期望结果直接写成 $\log(1/\delta_A)$。

## 4. ReLU 特征怎样归一化

若 $\|x\|_2\le R$，约束 $R\|w\|_2+|b|\le1$，则
$\psi_{w,b}(x)=\operatorname{ReLU}(w^\top x+b)\in[0,1]$。
利用 ReLU 正齐次性可以把特征的尺度移到外层系数，但迁移后的总 variation $V$ 必须保留。

这里解决的是给定表示的逼近。Sobolev 类到该表示范数的嵌入、最紧深度分离或 arbitrary feature learning 都另有证明。

## 5. 逼近怎样接到训练与泛化

若特征进一步满足 $|\psi_\theta(x)|\le1$，抽样构造系数为 $V s_j/m$，故其 $\ell_2$ 范数为 $V/\sqrt m$。固定随机特征后，可以在这只系数球里训练。

[完整例子](../../docs/END_TO_END_LEARNING_PROOF.md) 用这一预算同时控制模型误差、Rademacher 复杂度和 projected GD gap，最终给出同一风险量的有限样本结论。

本卡 $|\nu|/V$ 抽样 law 可能依赖未知目标，故存在性构造不自动给出可执行学习算法。完整例子另设可抽样、事先固定的 $\pi$，假设 $f_*=\mathbb E_\pi[a(\theta)\psi_\theta]$ 且 $|a|\le V$；同一方差计算适用，算法可从已知 $\pi$ 抽特征，而无需知道比较系数 $a$。

## 前置、关联与证据

- [Monte Carlo](<../../Math 基础/概率统计/蒙特卡洛、重要性采样与 MCMC.md>) · [向量空间与内积](<../../Math 基础/线性代数/向量空间、基、秩与 SVD.md>)。
- [T34](T34-neural-approximation.md) · [T33 一致收敛](../generalization/T33-uniform-convergence.md) · [T32 风险分解](../generalization/T32-excess-risk-decomposition.md)。
- [原论文](https://arxiv.org/abs/1906.08039) · [本地论文卡](../../proof_ref/dl-specializations-2026-10/the-barron-space-and-the-flow-induced-function-1906.08039/README.md)。具体 Barron 空间定义与 direct/inverse 定理按原文条件使用。
