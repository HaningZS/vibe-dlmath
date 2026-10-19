---
type: note
domain: math/probability/proof-tools
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# 集中不等式、MGF、鞅与自归一化过程

近期证明蒸馏：[T50 指数距离包络](../../proofs/generalization/T50-data-dependent-certificate-envelope.md)，展示 McDiarmid 下尾与 Hoeffding 指数矩如何共同控制总体期望。

证明进阶：[T46 隐私损失 MGF、条件组合与尾界](../../proofs/statistics/T46-gaussian-privacy-accounting.md) · [T45 认证概率估计](../../proofs/generalization/T45-certified-robustness.md)。

证明练习：[Ville 不等式与随时有效推断](../../extensions/Ville不等式与随时有效推断.md)，从条件 MGF 构造超鞅，再通过截断 stopping time 控制全部时刻。

先抓住一句话：

> 集中不等式是在回答：“一个带随机噪声的量，偏离它的正常水平很多，究竟有多不可能？”

大数定律告诉我们平均值最终会稳定，中心极限定理描述典型波动的渐近形状；理论论文里的高概率证明还经常需要更强的东西：在有限样本下，直接给出失败概率不超过 $\delta$ 的误差半径，而且要能处理在线选择、相关历史、随机停止和随数据变化的归一化矩阵。

可以把整条证明链想成给随机噪声做“安检”：

1. 先确认噪声在什么信息条件下均值为零；
2. 再确认尾部有多轻——有界、次高斯、次指数，还是只有有限矩；
3. 用 MGF 把“尾概率”改写成可优化的指数上界；
4. 若数据按时间到达，就把独立和升级成鞅；
5. 若不同方向的数据量不同，就用随机 Gram 矩阵自适应地归一化。

## 知识依赖与导航

- 总入口：[Math 基础目录](../Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md)；证明阅读顺序：[AI 理论证明前置学习路线](../%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/AI%20%E7%90%86%E8%AE%BA%E8%AF%81%E6%98%8E%E5%89%8D%E7%BD%AE%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)。
- 先修：[概率论主干：联合、条件、期望与协方差](%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md)、[moment(矩)](moment%28%E7%9F%A9%29.md)、[大数定律、中心极限定理与采样误差](%E5%A4%A7%E6%95%B0%E5%AE%9A%E5%BE%8B%E3%80%81%E4%B8%AD%E5%BF%83%E6%9E%81%E9%99%90%E5%AE%9A%E7%90%86%E4%B8%8E%E9%87%87%E6%A0%B7%E8%AF%AF%E5%B7%AE.md)。
- 在线信息语言：[测度、条件期望、滤过与适应过程](%E6%B5%8B%E5%BA%A6%E3%80%81%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E3%80%81%E6%BB%A4%E8%BF%87%E4%B8%8E%E9%80%82%E5%BA%94%E8%BF%87%E7%A8%8B.md)。
- 向量和矩阵版本：[矩阵浓缩、谱扰动与子空间误差](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E7%9F%A9%E9%98%B5%E6%B5%93%E7%BC%A9%E3%80%81%E8%B0%B1%E6%89%B0%E5%8A%A8%E4%B8%8E%E5%AD%90%E7%A9%BA%E9%97%B4%E8%AF%AF%E5%B7%AE.md)、[二次型、正定矩阵与谱](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E4%BA%8C%E6%AC%A1%E5%9E%8B%E3%80%81%E6%AD%A3%E5%AE%9A%E7%9F%A9%E9%98%B5%E4%B8%8E%E8%B0%B1.md)。
- Bandit/RL 应用：[MDP、Bellman 方程与时序差分学习](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0/%E5%9F%BA%E7%A1%80/MDP%E3%80%81Bellman%20%E6%96%B9%E7%A8%8B%E4%B8%8E%E6%97%B6%E5%BA%8F%E5%B7%AE%E5%88%86%E5%AD%A6%E4%B9%A0.md)。

### 对应证明模板

- 通用概率原语：[P04：MGF、martingale 与自归一化](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p04-mgf-concentrationmartingale-%E4%B8%8E%E8%87%AA%E5%BD%92%E4%B8%80%E5%8C%96)。
- 线性 bandit/RL：[T06：confidence ellipsoid 与 elliptical potential](../../proofs/sequential-decision/T06-linear-bandit.md)。
- 重尾与 clipping：[T16：重尾噪声的高概率证明](../../proofs/optimization/T16-heavy-tail-clipping.md)。
- 在线可测性：[T23：filtration 与 adaptedness](../../proofs/evaluation-monitoring/T23-prefix-safety.md)。
- 新式统一时间界：[R03：time-uniform self-normalized concentration](../../%E8%BF%91%E6%9C%9F%E9%A1%B6%E4%BC%9A%E7%90%86%E8%AE%BA%E6%A1%86%E6%9E%B6%EF%BC%882025-2026%EF%BC%89.md#r03-time-uniform-self-normalized-concentration)。

### 本地原文定位（页码已抽查；核验等级见导航）

- Clipping、重尾矩与 Bernstein 工具：[Clipping Improves Adam-Norm，PDF p14](../../proof_ref/core-theory-2026-09/clipping-improves-adam-norm-and-adagrad-norm-when-2406.04443/paper.pdf#page=14)。
- 线性 MDP 的 self-normalized concentration：[LSVI-UCB，PDF p27](../../proof_ref/core-theory-2026-09/provably-efficient-reinforcement-learning-with-linear-function-approximation-1907.05388/paper.pdf#page=27)。
- RLHF 中的 Freedman、martingale exponential inequality：[f-Divergence RLHF，PDF p28](../../proof_ref/core-theory-2026-09/f-divergence-regularized-rlhf-two-tales-of-sampling-2605.06977/paper.pdf#page=28)。
- Preference learning 的 elliptical-potential 工具：[Iterative Preference Learning，PDF p46](../../proof_ref/core-theory-2026-09/iterative-preference-learning-from-human-feedback-bridging-theory-2312.11456/paper.pdf#page=46)。

## 1. 从 Markov 不等式开始：只用平均值控制极端事件

设 $Y\ge 0$，对任意 $a>0$：

$$
\mathbb P(Y\ge a)\le \frac{\mathbb E[Y]}{a}.
$$

证明只有一行，但值得看懂：

$$
Y\ge a\,\mathbf 1\{Y\ge a\}.
$$

两边取期望后，右边就是 $a\mathbb P(Y\ge a)$。

直觉上，若一个非负量的平均值只有 2，它不可能以很大概率超过 100；否则平均值早就被抬高了。Markov 不等式非常通用，因为它只要求非负和期望存在；代价是通常比较松。

### 1.1 从 Markov 到矩方法

若想控制 $|X|$，可以把非负变量换成 $|X|^p$：

$$
\mathbb P(|X|\ge t)
=\mathbb P(|X|^p\ge t^p)
\le \frac{\mathbb E|X|^p}{t^p}.
$$

这给出多项式尾部 $t^{-p}$。当随机变量只有有限 $p$ 阶矩、MGF 不存在时，这条简单方法仍然合法；这正是重尾分析的最低保底工具。

## 2. Chernoff 技巧：把尾事件送进指数函数

指数函数单调递增。对任意 $\lambda>0$：

$$
\begin{aligned}
\mathbb P(X\ge t)
&=\mathbb P(e^{\lambda X}\ge e^{\lambda t})\\
&\le e^{-\lambda t}\,\mathbb E[e^{\lambda X}].
\end{aligned}
$$

这里使用的仍然只是 Markov 不等式，只不过对象换成了 $e^{\lambda X}$。定义矩母函数（moment generating function, MGF）

$$
M_X(\lambda)=\mathbb E[e^{\lambda X}],
$$

便得到 Chernoff 上界

$$
\mathbb P(X\ge t)
\le \inf_{\lambda>0}
\exp\bigl(-\lambda t+\log M_X(\lambda)\bigr).
$$

参数 $\lambda$ 像调节“放大极端值的倍率”：太小，区分不出普通值和极端值；太大，MGF 自己会爆长。对 $\lambda$ 优化，就是寻找最划算的放大倍率。

### 2.1 为什么独立性很有用

若 $X_1,\ldots,X_n$ 独立，则

$$
\mathbb E\exp\left(\lambda\sum_iX_i\right)
=\prod_i\mathbb E[e^{\lambda X_i}].
$$

取对数以后，乘法变加法：

$$
\log M_{\sum_iX_i}(\lambda)
=\sum_i\log M_{X_i}(\lambda).
$$

所以“许多随机量之和”的尾部问题，被拆成了每一项的 MGF 账本。鞅情形不再有无条件乘法分解，但可以逐步控制**条件 MGF**，第 6 节会看到它。

> [!warning] MGF 不是自动存在
> Cauchy、Pareto 等重尾分布可能有某些有限矩，却对所有 $\lambda>0$ 都满足 $\mathbb E e^{\lambda X}=\infty$。此时不能假装 Chernoff 仍然可用。

## 3. 三种常见尾部等级

### 3.1 次高斯：像高斯一样快速衰减

若中心化随机变量 $X$ 满足，对所有 $\lambda\in\mathbb R$，

$$
\log\mathbb E[e^{\lambda X}]
\le \frac{\sigma^2\lambda^2}{2},
$$

就称它是参数为 $\sigma$ 的次高斯变量。代入 Chernoff 上界：

$$
\mathbb P(X\ge t)
\le \inf_{\lambda>0}
\exp\left(-\lambda t+\frac{\sigma^2\lambda^2}{2}\right).
$$

右边关于 $\lambda$ 是一个二次函数，在 $\lambda=t/\sigma^2$ 处最小，因此

$$
\mathbb P(X\ge t)
\le \exp\left(-\frac{t^2}{2\sigma^2}\right).
$$

次高斯的重点不是“分布一定是 Gaussian”，而是尾部至少像 Gaussian 那样快。Gaussian 本身、中心化 Rademacher 变量和有界中心化变量都是典型例子。

参数 $\sigma^2$ 是 **variance proxy**，不必恰好等于 $\operatorname{Var}(X)$；它是一个足以控制整个 MGF 的尺度。

### 3.2 次指数：中等偏差像高斯，极端偏差像指数

一种常见参数化是：存在 $\nu,b>0$，使得

$$
\log\mathbb E[e^{\lambda X}]
\le \frac{\nu^2\lambda^2}{2},
\qquad |\lambda|<\frac1b.
$$

与次高斯的区别是：这个二次 MGF 控制只在原点附近成立。优化 $\lambda$ 时会撞上 $1/b$ 的边界，于是尾部出现两段：

$$
\mathbb P(|X|\ge t)
\lesssim
2\exp\left[-c\min\left(
\frac{t^2}{\nu^2},\frac{t}{b}
\right)\right].
$$

- 中等偏差时由 $t^2/\nu^2$ 控制，像 Gaussian；
- 很大偏差时由 $t/b$ 控制，只剩指数衰减。

Gaussian 变量的平方减去其期望，是常见的次指数变量。这也是样本方差和协方差分析经常从 sub-Gaussian 走到 sub-exponential 的原因。

### 3.3 重尾：不能再免费使用指数尾部

“重尾”没有唯一统一定义。在优化论文中，常见假设只是

$$
\mathbb E[|X|^p]\le C_p,
\qquad p\in(1,2]
$$

或有限方差，而不假设 MGF 存在。此时常用策略包括：

- clipping/truncation：先限制单步极端值，但要额外计算截断偏差；
- median-of-means：把样本分组求均值，再取中位数；
- Catoni 等鲁棒均值；
- 直接用高阶矩的 Markov 界。

Clipping 不是“把噪声变成无偏有界噪声”。若

$$
\widetilde X=\operatorname{clip}(X,\tau),
$$

通常

$$
\mathbb E[\widetilde X]\neq\mathbb E[X].
$$

高概率证明必须把误差拆为

$$
\widetilde X-\mathbb E[X]
=\underbrace{\widetilde X-\mathbb E[\widetilde X]}_{\text{有界随机波动}}
+\underbrace{\mathbb E[\widetilde X]-\mathbb E[X]}_{\text{clipping bias}}.
$$

这正是 [T16](../../proofs/optimization/T16-heavy-tail-clipping.md) 强调的误差账本。

## 4. Hoeffding：只知道范围，也能得到平方指数尾部

设独立随机变量 $X_i\in[a_i,b_i]$。Hoeffding 不等式给出

$$
\mathbb P\left(
\sum_{i=1}^n(X_i-\mathbb E X_i)\ge t
\right)
\le
\exp\left(
-\frac{2t^2}{\sum_i(b_i-a_i)^2}
\right).
$$

它的证明路线是：

1. Hoeffding lemma 用区间宽度控制每一项的中心化 MGF；
2. 独立性把总 MGF 拆成乘积；
3. Chernoff 对 $\lambda$ 优化。

若 $X_i\in[0,1]$ 且 $\bar X=n^{-1}\sum_iX_i$，则

$$
\mathbb P(|\bar X-\mathbb E\bar X|\ge \varepsilon)
\le 2e^{-2n\varepsilon^2}.
$$

反过来令右边等于 $\delta$，得到置信半径

$$
|\bar X-\mathbb E\bar X|
\le \sqrt{\frac{\log(2/\delta)}{2n}}
$$

以至少 $1-\delta$ 的概率成立。

Hoeffding 的优点是条件简单；缺点是只看最坏范围，不看真实方差。一个几乎总在 0 附近、偶尔到 1 的变量，与均匀铺满 $[0,1]$ 的变量会得到相同的范围型界。

## 5. Bernstein：把方差也记进账本

设独立、中心化的 $X_i$ 满足 $|X_i|\le b$，并令

$$
V=\sum_{i=1}^n\mathbb E[X_i^2].
$$

Bernstein 型结论的一种常见写法是：对 $x>0$，

$$
\sum_iX_i
\le
\sqrt{2Vx}+\frac{bx}{3}
$$

以至少 $1-e^{-x}$ 的概率成立。

把 $x$ 取成 $\log(1/\delta)$，就得到失败概率为 $\delta$ 的界。

这个式子里有两个尺度：

- $\sqrt{Vx}$：普通波动区域，方差主导；
- $bx$：极端区域，单步最大幅度主导。

因此 Bernstein 常比只用范围的 Hoeffding 更敏感。但“variance-aware”不等于可以把未知随机方差直接塞进公式；使用经验 Bernstein、predictable variance 或 plug-in variance 时，需要对应的独立定理。

## 6. 从独立和到鞅：允许下一步依赖过去

在线学习、RL 和自适应数据收集里，动作 $x_t$ 会根据过去选择，$X_t$ 通常不独立。正确替代品是 filtration 和 martingale difference。

设 $\mathcal F_t$ 表示看到时刻 $t$ 为止的全部信息。若

$$
X_t\in\mathcal F_t,
\qquad
\mathbb E[X_t\mid\mathcal F_{t-1}]=0,
$$

则 $(X_t)$ 是 martingale difference sequence（MDS），而

$$
M_t=\sum_{s=1}^tX_s
$$

是鞅。

人话解释：$X_t$ 可以受过去影响，但在已经知道过去的前提下，它仍然没有可预测的系统偏差。像“每一步都可能根据旧牌调整策略，但庄家下一张牌仍公平”。

### 6.1 Azuma–Hoeffding：鞅的范围型界

若 $|X_t|\le c_t$ 几乎处处成立，且 $c_t$ 为确定常数，则

$$
\mathbb P(M_T\ge u)
\le
\exp\left(
-\frac{u^2}{2\sum_{t=1}^Tc_t^2}
\right).
$$

它只看每一步最多跳多远，不看实际条件方差。因此当多数步非常安静时，Azuma 可能很保守。

### 6.2 Freedman：鞅的 Bernstein 版本

定义 predictable quadratic variation

$$
V_t=
\sum_{s=1}^t
\mathbb E[X_s^2\mid\mathcal F_{s-1}].
$$

它是在每一步发生前，根据已有信息能预测的累计方差。若 $X_t\le b$，Freedman 的一个最大型版本是

$$
\mathbb P\left(
\exists t\le T:
M_t\ge u\ \text{且}\ V_t\le v
\right)
\le
\exp\left(
-\frac{u^2}{2(v+bu/3)}
\right).
$$

它看起来像 Bernstein，只是普通方差换成了条件方差账本。

> [!warning] 不能随意把随机 $V_t$ 代入固定 $v$
> 上式同时控制“$M_t$ 很大且 $V_t\le v$”。若要得到直接依赖观察到的 $V_t$ 的边界，通常还要 peeling、stitching 或更专门的 empirical-Bernstein/confidence-sequence 结果。

## 7. 停时与 time-uniform：为什么“训练到看起来够好就停”会改变问题

固定时间结论

$$
\mathbb P(M_T\ge b_T)\le\delta
$$

并不自动推出在观察轨迹后选择的随机时间 $\tau$ 也满足同一个界。若我们每天看一次实验，第一次显著就停止，实际上进行了多次机会选择。

### 7.1 Stopping time

随机时间 $\tau$ 是 stopping time，意思是事件 $\{\tau\le t\}$ 只用 $\mathcal F_t$ 的信息就能判断。它允许“看到现在决定停”，不允许偷看未来。

Optional stopping theorem 也不是一句“鞅在任意停时的期望不变”。常见充分条件包括有界停时、有界增量配合可积控制、uniform integrability 等；条件不满足时，赌徒策略可以制造反例。

### 7.2 Ville 不等式：从非负超鞅得到统一时间保证

若 $(L_t)$ 是非负 supermartingale，且 $\mathbb E L_0\le1$，则

$$
\mathbb P\left(
\sup_{t\ge0}L_t\ge\frac1\delta
\right)
\le\delta.
$$

这条结果的力量在于“同时对所有时间成立”。把条件 MGF 组合成指数 supermartingale，再用 Ville，就能构造 confidence sequence：

$$
\mathbb P\bigl(
\forall t\ge1:\ \mu\in C_t
\bigr)\ge1-\delta.
$$

简单地对 $t=1,\ldots,T$ 做 union bound 往往多付一个 $\log T$；mixture、peeling 或 stitching 可以把代价降为更细的 $\log\log$ 型项。不同方法的条件和常数不同，不能只写“time-uniform concentration”而省略构造。

## 8. 自归一化：每个方向按自己积累的信息量计费

考虑在线线性模型

$$
y_t=x_t^\top\theta_\star+\eta_t.
$$

允许 $x_t$ 根据过去选择，即 $x_t$ 对 $\mathcal F_{t-1}$ 可测；假设噪声在条件于过去时是 $R$-sub-Gaussian：

$$
\mathbb E[e^{\lambda\eta_t}\mid\mathcal F_{t-1}]
\le e^{R^2\lambda^2/2}.
$$

定义

$$
S_t=\sum_{s=1}^tx_s\eta_s,
\qquad
V_t=\lambda_0 I+\sum_{s=1}^tx_sx_s^\top,
\qquad \lambda_0>0.
$$

普通欧氏范数 $\|S_t\|_2$ 会把所有方向一视同仁；但数据可能在某些方向采得很多、另一些方向几乎没采。自归一化范数

$$
\|S_t\|_{V_t^{-1}}
=\sqrt{S_t^\top V_t^{-1}S_t}
$$

会自动降低“已经收集很多数据的方向”的权重，提高信息稀少方向的相对重要性。

经典 self-normalized bound 的一种形式是：以至少 $1-\delta$ 的概率，对所有 $t$ 同时成立

$$
\|S_t\|_{V_t^{-1}}
\le
R\sqrt{
2\log\left(
\frac{\det(V_t)^{1/2}}
{\det(\lambda_0 I)^{1/2}\delta}
\right)
}.
$$

若 ridge least-squares 估计为

$$
\widehat\theta_t
=V_t^{-1}\sum_{s=1}^tx_sy_s,
$$

且 $\|\theta_\star\|_2\le S$，还会有 ridge bias：

$$
\|\widehat\theta_t-\theta_\star\|_{V_t}
\le
R\sqrt{
2\log\left(
\frac{\det(V_t)^{1/2}}
{\det(\lambda_0 I)^{1/2}\delta}
\right)
}
+\sqrt{\lambda_0}S.
$$

### 8.1 为什么出现 log-det

$V_t$ 描述数据在各方向积累的二次信息。若其特征值为 $\lambda_1(V_t),\ldots,\lambda_d(V_t)$，则

$$
\log\frac{\det(V_t)}{\det(V_0)}
=\sum_{i=1}^d
\log\frac{\lambda_i(V_t)}{\lambda_i(V_0)}.
$$

它像“置信椭球体积缩小了多少”的信息账单：只有真正被数据激活的方向会显著增加代价。粗糙地把它上界成 $d\log(1+T/\lambda_0)$ 会更容易读，但也可能丢掉有效维数结构。

## 9. Elliptical potential：同一个新方向不能无限次都算“很新”

由矩阵行列式引理：

$$
\det(V_t)
=\det(V_{t-1})
\left(1+\|x_t\|_{V_{t-1}^{-1}}^2\right).
$$

取对数并求和：

$$
\log\frac{\det(V_T)}{\det(V_0)}
=\sum_{t=1}^T
\log\left(1+\|x_t\|_{V_{t-1}^{-1}}^2\right).
$$

利用 $\min(1,u)\le2\log(1+u)$，得到 elliptical potential lemma：

$$
\sum_{t=1}^T
\min\left(1,\|x_t\|_{V_{t-1}^{-1}}^2\right)
\le
2\log\frac{\det(V_T)}{\det(V_0)}.
$$

直觉是：第一次探索一个新方向时，$V_{t-1}$ 在那里很小，所以不确定性大；反复访问后，那个方向的特征值上升，后续 bonus 自动缩小。线性 bandit 和 LSVI-UCB 就用它把逐轮置信宽度压成总体 regret。

注意区分两个工具：

- self-normalized concentration 控制随机噪声向量 $S_t$；
- elliptical potential 控制设计向量自身累计了多少“不确定方向”。

它们经常一起出现，但不是同一个 lemma。

## 10. NumPy 示例：自适应设计下的自归一化与 log-det 账本

下面让算法每一步选择当前信息最少的坐标方向。选择依赖过去的 $V_t$，但发生在新噪声之前，因此是 predictable 的。

~~~python
import numpy as np

rng = np.random.default_rng(23)
d, horizon = 6, 600
ridge = 1.0
delta = 0.01
noise_scale = 1.0  # 标准高斯是 1-sub-Gaussian

V = ridge * np.eye(d)
S = np.zeros(d)
elliptical_sum = 0.0

for _ in range(horizon):
    # 在看到本轮噪声前，根据过去选择信息最少的坐标方向。
    coordinate = int(np.argmin(np.diag(V)))
    x = np.eye(d)[coordinate]

    V_inv = np.linalg.inv(V)
    leverage = x @ V_inv @ x
    elliptical_sum += min(1.0, leverage)

    eta = rng.normal(scale=noise_scale)
    S += x * eta
    V += np.outer(x, x)

sign, logdet_V = np.linalg.slogdet(V)
_, logdet_V0 = np.linalg.slogdet(ridge * np.eye(d))
assert sign > 0

self_normalized = np.sqrt(S @ np.linalg.solve(V, S))
radius = noise_scale * np.sqrt(
    (logdet_V - logdet_V0) + 2.0 * np.log(1.0 / delta)
)
potential_bound = 2.0 * (logdet_V - logdet_V0)

print("self-normalized noise:", self_normalized)
print("confidence radius:", radius)
print("elliptical sum / bound:", elliptical_sum, potential_bound)

# 对这个固定随机种子，样本路径落在 99% 理论事件内。
assert self_normalized <= radius
# 这是逐路径的确定性 log-det 不等式，不依赖噪声分布。
assert elliptical_sum <= potential_bound + 1e-12
~~~

这个实验不是定理的证明。第一条断言仍有 $\delta$ 概率可能失败；第二条是对任意给定设计序列成立的确定性代数关系。两种断言的逻辑地位不要混在一起。

## 11. 阅读高概率证明时的检查顺序

1. **随机对象是谁？** 数据、噪声、动作、初始化还是算法内部采样？
2. **中心化相对于什么？** 是 $\mathbb E X_t=0$，还是更强的 $\mathbb E[X_t\mid\mathcal F_{t-1}]=0$？
3. **尾部条件是什么？** 有界、条件 sub-Gaussian、条件方差有界，还是只有有限 $p$ 阶矩？
4. **结论作用于什么范围？** 固定 $t$、所有 $t\le T$、所有方向，还是整个函数类？
5. **失败概率怎样分配？** 是否对时间、状态、动作、层数粗暴 union bound？
6. **归一化矩阵可逆吗？** 是否加入 ridge $\lambda_0 I$？
7. **设计是否 predictable？** $x_t$ 必须在看到当前噪声前确定。
8. **随机方差能否直接代入？** 还是需要 peeling/stitching/empirical-Bernstein？
9. **重尾处理是否记了 bias？** clipping 后不能继续假设原来的无偏性。
10. **最终 bound 的 metric 是什么？** 欧氏范数、$V_t$-norm、函数值还是 regret？

## 12. 常见误区

1. **“方差有限就能用 sub-Gaussian 界。”** 错。有限方差远弱于指数 MGF 控制。
2. **“独立是鞅不等式的必要条件。”** 不需要完全独立；关键是相对于过去的条件均值和条件尾部控制。
3. **“Azuma 一定比 Hoeffding 更强。”** Azuma 处理适应性，但只看步长范围时也可能更松。
4. **“Freedman 允许直接把观察到的随机方差塞进去。”** 需要查看所用版本是否支持随机边界、peeling 或 time-uniform 结论。
5. **“optional stopping 对任意停时都成立。”** 必须检查可积性、有界性或 uniform integrability 等条件。
6. **“confidence sequence 只是每个时刻置信区间的集合。”** 逐时 95% 区间不保证整个序列同时 95% 覆盖。
7. **“self-normalized 就是除以样本标准差。”** 这里常指用随机设计矩阵 $V_t$ 在各方向分别归一化。
8. **“log-det 只是证明里的难看常数。”** 它记录置信椭球在多少方向上真正收缩。
9. **“elliptical potential 本身就是概率定理。”** 给定向量序列后，它主要是确定性的矩阵代数结论。
10. **“clipping 只降低方差，没有代价。”** 它通常引入偏差，阈值决定 bias–fluctuation trade-off。

## 13. 自测

1. Markov 不等式为什么要求被控制的变量非负？如何用它控制 $|X|$？
2. 从 Chernoff 上界推导 sub-Gaussian 尾界时，最优 $\lambda$ 是多少？
3. 次高斯和次指数尾部在“大偏差区域”有什么不同？
4. 为什么 $\mathbb E[X_t]=0$ 不足以保证 $(X_t)$ 是 martingale difference？
5. Azuma 与 Freedman 分别忽略和利用了什么信息？
6. 为什么固定时间高概率界不能直接用于“看到显著就停止”？
7. 在线线性回归里，$x_t$ 可以依赖过去，却为什么不能依赖当前 $\eta_t$？
8. $\log\det(V_T/V_0)$ 在几何上和信息上分别表示什么？
9. self-normalized concentration 与 elliptical potential lemma 在 regret 证明中各控制哪一部分？
10. 对重尾梯度做 clipping 后，高概率误差应拆成哪两项？

## 权威来源

- Boucheron, Lugosi & Massart, *Concentration Inequalities*, Oxford University Press, 2013。
- Wainwright, *High-Dimensional Statistics*, Cambridge University Press, 2019，Chapters 2–3。
- Vershynin, [*High-Dimensional Probability*](https://www.math.uci.edu/~rvershyn/papers/HDP-book/HDP-book.html)，Chapters 2–5。
- de la Peña, Lai & Shao, *Self-Normalized Processes*, Springer, 2009。
- Abbasi-Yadkori, Pál & Szepesvári, [Improved Algorithms for Linear Stochastic Bandits](https://proceedings.neurips.cc/paper/2011/hash/e1d5be1c7f2f456670de3d53c7b54f4a-Abstract.html), NeurIPS 2011。
- Howard et al., [Time-uniform, nonparametric, nonasymptotic confidence sequences](https://projecteuclid.org/journals/annals-of-statistics/volume-49/issue-2/Time-uniform-nonparametric-nonasymptotic-confidence-sequences/10.1214/20-AOS1991.full), *Annals of Statistics*, 2021。
- Tropp, [Freedman's Inequality for Matrix Martingales](https://projecteuclid.org/journals/electronic-communications-in-probability/volume-16/issue-none/Freedmans-inequality-for-matrix-martingales/10.1214/ECP.v16-1624.full), 2011；矩阵版本见 [矩阵浓缩、谱扰动与子空间误差](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E7%9F%A9%E9%98%B5%E6%B5%93%E7%BC%A9%E3%80%81%E8%B0%B1%E6%89%B0%E5%8A%A8%E4%B8%8E%E5%AD%90%E7%A9%BA%E9%97%B4%E8%AF%AF%E5%B7%AE.md)。
