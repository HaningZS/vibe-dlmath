---
status: canonical
reviewed: 2026-08-24
---

# Beta 分布

> [!tip] 前置主干
> 条件分布、期望、Bayes 和总体/样本的区别见 [概率论主干：联合、条件、期望与协方差](../%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md)。
> Beta 在常见分布谱系中的位置见 [常见概率分布与指数族](../%E5%B8%B8%E8%A7%81%E6%A6%82%E7%8E%87%E5%88%86%E5%B8%83%E4%B8%8E%E6%8C%87%E6%95%B0%E6%97%8F.md)；点估计视角见 [最大似然、MAP 与贝叶斯估计](../%E6%9C%80%E5%A4%A7%E4%BC%BC%E7%84%B6%E3%80%81MAP%20%E4%B8%8E%E8%B4%9D%E5%8F%B6%E6%96%AF%E4%BC%B0%E8%AE%A1.md)。

Beta 分布是一族定义在单位区间上的连续概率分布，常用于表示未知概率或比例的不确定性。

## 定义

若 $X\sim\mathop{\mathrm{Beta}}(\alpha,\beta)$，其中 $\alpha>0,\beta>0$，则在 $0<x<1$ 上

$$
f(x;\alpha,\beta)
=\frac{x^{\alpha-1}(1-x)^{\beta-1}}{B(\alpha,\beta)},
$$

其中

$$
B(\alpha,\beta)
=\int_0^1 t^{\alpha-1}(1-t)^{\beta-1}\thinspace dt.
$$

端点处的密度值取决于参数并可能发散；分布本身仍可定义在闭区间 $[0,1]$ 上。

## 常用统计量

均值：

$$
\mathbb E[X]=\frac{\alpha}{\alpha+\beta}.
$$

方差：

$$
\mathop{\mathrm{Var}}(X)
=\frac{\alpha\beta}
{(\alpha+\beta)^2(\alpha+\beta+1)}.
$$

当 $\alpha>1,\beta>1$ 时，众数为

$$
\mathop{\mathrm{mode}}(X)
=\frac{\alpha-1}{\alpha+\beta-2}.
$$

均值和众数一般不同，不能用均值代替“峰值位置”。

偏度为

$$
\gamma_1=
\frac{2(\beta-\alpha)\sqrt{\alpha+\beta+1}}
{(\alpha+\beta+2)\sqrt{\alpha\beta}}.
$$

因此：

- $\alpha>\beta$：质量更靠近 1，左尾更长，称为左偏/负偏；
- $\alpha<\beta$：质量更靠近 0，右尾更长，称为右偏/正偏。

## 形状直觉

- $\alpha=\beta=1$：均匀分布；
- $\alpha>1,\beta>1$：内部单峰；
- $\alpha<1,\beta<1$：U 形，密度在两端较高；
- $\alpha=1,\beta>1$：递减；
- $\alpha>1,\beta=1$：递增。

固定均值比例并同时增大 $\alpha+\beta$，方差会减小，分布更集中。

## Beta–Bernoulli / Beta–Binomial 共轭

设未知成功概率为 $p$：

$$
p\sim\mathop{\mathrm{Beta}}(\alpha,\beta).
$$

观察到 $s$ 次成功、 $f$ 次失败后，后验为

$$
p\mid D\sim\mathop{\mathrm{Beta}}(\alpha+s,\beta+f).
$$

在这种更新规则中， $\alpha$ 和 $\beta$ 常被口语化为“伪计数”。更精确地说，若以均匀先验 $\mathop{\mathrm{Beta}}(1,1)$ 为基准，先验相对增加的成功/失败计数是 $\alpha-1$ 和 $\beta-1$。不同参数化或基准先验下，不应机械地把 $\alpha,\beta$ 当作真实观测次数。

## “无信息先验”需要说明选择

$\mathop{\mathrm{Beta}}(1,1)$ 是对 $p$ 均匀的先验，但“均匀”依赖参数化，不等于唯一、公认的无信息先验。Bernoulli 参数常见的 Jeffreys 先验是 $\mathop{\mathrm{Beta}}(1/2,1/2)$。使用哪一种应根据建模目标说明。

## 使用边界

Beta 分布适合建模连续的 $0$ 到 $1$ 变量，但不是所有比例数据的自动首选：

- 数据若包含大量精确的 0 或 1，可考虑 zero/one-inflated 模型；
- 计数数据若保留了成功数和试验数，Binomial/Beta-Binomial 往往比直接对比例做 Beta 回归更合适；
- 项目管理中的 PERT 常使用经过缩放和重新参数化的 Beta/PERT 分布，不是原始标准 Beta 的直接应用。

## 来源

- [NIST/SEMATECH e-Handbook: Beta Distribution](https://itl.nist.gov/div898/handbook/eda/section3/eda366h.htm)
