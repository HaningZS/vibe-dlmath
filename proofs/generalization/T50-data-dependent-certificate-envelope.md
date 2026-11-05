---
id: T50
type: proof-template
refined: 2026-10-20
status: self-contained-core
---

# T50. 从样本证书到总体期望：指数距离上包络

[主题目录](README.md) · [稳定性 T04](T04-stability.md) · [证明蒸馏](../../docs/PROOF_DISTILLATION.md)

## 复用契约

**对象**： $S=(Z_1,\ldots,Z_n)\sim\mathcal D^n$，样本独立；预先固定非负函数 $\epsilon(S)$、 $\beta>0$、 $\delta\in(0,1)$。 $d(S,S')$ 是替换了几个坐标的 Hamming 距离。

定义
$$B_\beta(S)=\sup_{S'}\epsilon(S')e^{-\beta d(S,S')}.$$
假设包络可测且有限。若不恒为零，它处处正； $\log B_\beta$ 有界，所用期望存在。

**输出**：以至少 $1-\delta$ 的概率抽到 $S_{obs}$ 时，
$$\mathbb E_S\epsilon(S)\le B_\beta(S_{obs})\exp\negthinspace\left(\beta\sqrt{\frac n2\log\frac1\delta}+\frac{n\beta^2}{8}\right).$$

**失败例子**：只看几个邻近数据集取最大值，通常是对 supremum 的下估计，不能代入右端作为认证上界。预先固定的 $\beta$ 看数据后自由优化，也会改变概率保证。

## 实例化时必须完成

- [ ] 证明所需总体量确实不超过 $\mathbb E\epsilon(S)$。
- [ ] 处理包络的可测、有限、零值，以及实际计算得到的是上界。
- [ ] 固定全部随机性：训练 seed、观测样本、独立验证集各自在哪里。
- [ ] 同时比较多个 $\beta$ 时分配失败概率，不把期望 gap 换成 realized gap。

## 1. 直觉：给局部证书套一个不会突变的外壳

同一算法换一个训练点，证书可能跳变。包络向附近乃至更远的数据集看去，按距离打折，取最大的潜在影响。这样观察到的小值不会仅仅来自刚好避开一个紧邻的坏数据集。

折扣越快（ $\beta$ 大），包络越贴近局部，但从观测值推总体期望时付出的浓缩代价越大。

## 2. 上包络为什么是 log-Lipschitz

取 $S'=S$ 可知 $B_\beta(S)\ge\epsilon(S)$。由三角不等式，对任何 $U$，
$$\epsilon(U)e^{-\beta d(S,U)}\le e^{\beta d(S,V)}\epsilon(U)e^{-\beta d(V,U)}.$$
取上确界并交换 $S,V$，得到
$$|\log B_\beta(S)-\log B_\beta(V)|\le\beta d(S,V).$$
若某处包络为零，所有被 supremum 覆盖的非负项都为零，所以它恒为零，结论直接成立。否则，Hamming 直径为 $n$，某处正且有限就给出全域正下界和有限上界，可以安全取对数。

## 3. 两个经典概率工具怎样拼起来

写 $g(S)=\log B_\beta(S)$。替换一个坐标改变 $g$ 至多 $\beta$，McDiarmid 下尾给出
$$\Pr\lbrace\mathbb Eg-g(S_{obs})>t\rbrace\le e^{-2t^2/(n\beta^2)}.$$
故概率至少 $1-\delta$ 时， $\mathbb Eg\le g(S_{obs})+\beta\sqrt{n\log(1/\delta)/2}$。

还不能直接把 $\mathbb E e^g$ 写成 $e^{\mathbb Eg}$。依次揭示独立坐标，构造 $g$ 的 Doob martingale；每个中心化增量的条件取值区间长度至多 $\beta$。Hoeffding 引理在指数参数 1 下给出每步因子 $e^{\beta^2/8}$，逐步条件化得到
$$\mathbb E e^{g-\mathbb Eg}\le e^{n\beta^2/8}.$$

于是，在同一个观测事件上，

$$\mathbb E\epsilon\le\mathbb E B_\beta
=e^{\mathbb Eg}\mathbb E e^{g-\mathbb Eg}
\le B_\beta(S_{obs})e^{\beta\sqrt{n\log(1/\delta)/2}+n\beta^2/8}.$$

这解释了两个常数各自来自哪一步，而不是只记住最后的指数。

## 4. 接回算法稳定性时，左端是什么

固定学习程序 $A$，损失可积。让 $S^{(i)}$ 替换第 $i$ 个样本为独立 $Z_i'$。交换 $Z_i,Z_i'$ 得到 [T04](T04-stability.md) 的恒等式

$$\mathbb E_S[R(A(S))-\widehat R_S(A(S))]
=\frac1n\sum_i\mathbb E_{S,Z_i'}[\ell(A(S),Z_i')-\ell(A(S^{(i)}),Z_i')].$$

若 $\epsilon(S)$ 是这些替换/测试点损失差绝对值的统一上界，则左端不超过 $\mathbb E\epsilon(S)$，可以使用第 3 节。

结论是：一个随机观测到的上界，以高概率控制一个固定的**期望泛化差**。它没有直接控制该次 $S_{obs}$ 的 realized gap。若算法 seed 先独立固定，结论相对于该 seed；要再对 seed 平均，必须把随机性放回相应定义与证明。

## 5. 参数选择与实际证书

预先取 $\beta=c/\sqrt n$ 可使指数因子不随 $n$ 增长，但还需证明包络本身下降，不能凭此宣称一致性。对预先固定的有限候选 $\beta_j$，可给各自 $\delta_j$ 且 $\sum_j\delta_j\le\delta$，联合事件上再选择最小上界。

若只有可认证的 $\widehat B(S_{obs})\ge B_\beta(S_{obs})$，代入仍合法； $\widehat B$ 自己不必 smooth。独立验证集能估计哪些 expectation、所需域何时固定，则按具体认证算法另证。

## 经典来源与近期证据

- [MGF 与集中不等式前置](<../../Math 基础/概率统计/集中不等式、MGF、鞅与自归一化过程.md>) · [T33](T33-uniform-convergence.md) · [T46](../statistics/T46-gaussian-privacy-accounting.md)。
- 核心工具是 bounded differences、Doob 条件化和 Hoeffding 引理；近期应用为 [Certification-Enhanced Generalization Bounds v1](https://arxiv.org/abs/2610.06238v1) 的 Proposition 2 / Theorem 1。
- [本地 PDF、源码与核验范围](../../proof_ref/proof-distillation-2026-10/certification-enhanced-generalization-bounds-2610.06238/核验笔记.md)。本卡闭合上面的基础包络和稳定性接口，不将全部 AGT 算法或实验一并标为已核验。
