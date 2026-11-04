---
id: T48
type: proof-template
refined: 2026-10-02
status: self-contained-core
---

# T48. 因果识别先于估计：从干预到 g-formula

[主题目录](README.md) · [DR 估计 T11](T11-doubly-robust.md) · [风险迁移 T19](../generation-transport/T19-transport-risk.md)

## 复用契约

**对象**：二元处理 $A$、处理前协变量 $X$、潜在结果 $Y(0),Y(1)$，目标 $\tau=\mathbb E[Y(1)-Y(0)]$；期望有限。

**条件**：consistency $Y=Y(A)$；条件可交换性 $(Y(0),Y(1))\perp A\mid X$；positivity $0<P(A=1\mid X)<1$ 几乎处处。处理定义、无干扰等设定须使潜在结果有明确含义。

**结论**： $\tau$ 可表示为观察分布的函数，即 g-formula。统计误差、模型拟合和因果假设的可信性是后续问题。

**失败例子**：两个世界可以生成同样的观察数据，却有不同干预效果；低预测误差和 DR 校正不能排除这一点。

## 实例化时必须完成

- [ ] 先写干预/潜在结果目标，并明确处理时间与处理前协变量。
- [ ] 给出识别假设及其领域依据，检查 collider/post-treatment 变量。
- [ ] 写出观察 law 到目标的等式，再套用估计方法。
- [ ] 学习表示 $Z=\phi(X)$ 后，重新检查是否保留识别所需信息。

## 1. 直觉：看到别人用了药，不等于替他换药

预测问“用了药的人结果如何”；因果问“同一个人换一种药会怎样”。使用者可能本来病情更重，观察差异会混进选择差异。

可交换性要求：给定处理前 $X$ 后，处理组和对照组在潜在结果上可比较。positivity 要求每类需要比较的人确实有两种处理机会。

## 2. g-formula 的完整推导

对 $a\in\{0,1\}$，逐步写

$$
\mathbb E[Y(a)]
=\mathbb E_X\mathbb E[Y(a)\mid X]
=\mathbb E_X\mathbb E[Y(a)\mid A=a,X]
=\mathbb E_X\mathbb E[Y\mid A=a,X].
$$

第一步是 tower property；第二步用条件可交换性，并用 positivity 使条件处理组有定义；第三步用 consistency。
令 $m_a(x)=\mathbb E[Y\mid A=a,X=x]$，则
$\tau=\mathbb E[m_1(X)-m_0(X)]$。

每一步的假设都承担具体作用，神经网络的逼近能力不会代替它们。

## 3. 不能识别的两个具体世界

令 $U\sim\operatorname{Bernoulli}(1/2)$、 $A=U$，不观测 $U$。

- 世界 1： $Y=A$。干预把 $A$ 设为 $a$ 时 $Y(a)=a$，所以 ATE 为 1。
- 世界 2： $Y=U$。干预不会改变 $U$，所以 $Y(a)=U$，ATE 为 0。

观察时两者都是 $P(A=Y=0)=P(A=Y=1)=1/2$。任何只依赖这份观察 law 的算法都无法分清它们。世界 2 不满足无协变量下的可交换性，因此识别推导在第二步断开。

## 4. 接到 DR 与深度表示

[T11](T11-doubly-robust.md) 的 nuisance 校正是在目标已识别后降低估计偏差。只有识别 law 固定，才能讨论 outcome model/propensity model 哪个正确，以及 cross-fitting 和乘积误差。

即使 $(Y(0),Y(1))\perp A\mid X$，一般也不推出给定压缩表示 $\phi(X)$ 的相同独立性。表示可能丢掉混杂变量；学习出“看起来平衡”的 embedding 不足以证明保留识别。

positivity 几乎处处足以写识别等式；稳定的有限样本估计常还需 $e(X)\in[\kappa,1-\kappa]$、矩界等更强条件。这两层条件应分开记。

## 前置、关联与证据

- [条件概率与期望](<../../Math 基础/概率统计/概率论主干：联合、条件、期望与协方差.md>) · [T11](T11-doubly-robust.md) · [T19](../generation-transport/T19-transport-risk.md)。
- [Pearl：Causal inference in statistics: An overview](https://ftp.cs.ucla.edu/pub/stat_ser/r350.pdf)：因果对象与识别框架的原始综述。
- [Double/debiased ML 本地卡](../../proof_ref/foundations-2026-09/double-debiased-machine-learning-for-treatment-and-structural-1608.00060/README.md)。这里完整推导 basic g-formula，不包办时间序列干预、mediation 或所有图识别规则。
