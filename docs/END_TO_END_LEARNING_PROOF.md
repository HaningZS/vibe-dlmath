# 一个闭合的学习证明：随机特征、训练与测试风险

[DL 框架](DL_THEORY_FRAMEWORK.md) · [证明审查](THEORY_REVIEW.md) · [T41 高维逼近](../proofs/deep-learning/T41-barron-random-feature-approximation.md) · [可运行代码](../examples/dl_specialization_checks.py)

这个例子从完整假设出发，证明有限宽、有限样本、有限训练步数下的总体风险界。它训练的是固定隐藏特征的输出层，模型可取两层网络；端到端训练隐藏层要另外分析。

## 1. 先固定能执行的算法与最终问题

数据 $(X_i,Y_i)$ 独立同分布，$|Y|\le Y_0$。损失为
$\ell(h,y)=\frac12(h-y)^2$，总体风险 $R(h)=\mathbb E\ell(h(X),Y)$，经验风险 $R_n(h)=n^{-1}\sum_i\ell(h(X_i),Y_i)$。

事先给定一个**可抽样、与训练集独立**的特征分布 $\pi$，特征 $|\psi_\theta(x)|\le1$。假设条件均值 $f_*(x)=\mathbb E[Y\mid X=x]$ 存在表示

$$
f_*(x)=\mathbb E_{\theta\sim\pi}[a(\theta)\psi_\theta(x)],\qquad |a(\theta)|\le V,
$$

其中 $V>0$ 是已给的预算；未知函数 $a$ 只用于证明比较解存在，算法不需要读取它。注意：任意 Barron variation 有限，未必能在这个**事先给定**的 $\pi$ 下用同一 $V$ 表示。这是明确的目标类假设。

算法独立抽取 $m$ 个特征，令 $\phi(x)=(\psi_{\theta_j}(x))_{j=1}^m$，训练 $h_w=w^\top\phi$，约束 $\|w\|_2\le W=V/\sqrt m$。从 $w_0=0$ 出发，做 $T$ 步 projected GD，$\eta=1/m$，输出 $\bar w=T^{-1}\sum_{t=1}^T w_t$。

假设通常的可测性与期望存在条件；这里的有限维参数球紧，损失连续、有界，uniform supremum 可用可数稠密参数集处理。

## 2. 主定理先写完整

令 $n,m,T\ge1$、$\delta_A,\delta_S\in(0,1)$。在特征抽样与训练样本的联合概率空间上，概率至少 $1-\delta_A-\delta_S$ 有

$$
\boxed{
R(h_{\bar w})-R^*
\le\frac{V^2}{2m\delta_A}
+\frac{4V(V+Y_0)}{\sqrt n}
+(V+Y_0)^2\sqrt{\frac{\log(2/\delta_S)}{2n}}
+\frac{V^2}{2T}.
}
$$

$R^*=\frac12\mathbb E\operatorname{Var}(Y\mid X)$ 是平方损失的 Bayes 风险。四项分别是特征逼近、复杂度统计误差、尾部统计误差和训练误差。

这是基础教学界：Markov 给出的 $1/\delta_A$ 较松，某些参数下风险界也会空泛；它的作用是完整展示合法接口，不宣称最优 rate。

## 3. 引理 A：Bayes 风险与逼近预算

条件展开平方可得

$$
R(h)-R^*=\tfrac12\|h-f_*\|_{L^2(P_X)}^2.
$$

因为 $\mathbb E[Y-f_*\mid X]=0$，展开中的交叉项为 0。

分析用的候选系数是 $w_j^A=a(\theta_j)/m$，范数不超过 $V/\sqrt m$，所以在允许球内。它是未知的比较解，训练并不使用它。

[T41](../proofs/deep-learning/T41-barron-random-feature-approximation.md) 的 Hilbert 方差计算应用于 $Z=a(\theta)\psi_\theta$，给出期望平方误差不超过 $V^2/m$。故概率至少 $1-\delta_A$，有

$$
\inf_{\|w\|\le W}R(h_w)-R^*\le\frac{V^2}{2m\delta_A}.
$$

## 4. 引理 B：训练集控制整个固定模型类

给定已抽取特征，$\|\phi(x)\|\le B=\sqrt m$，且 $|h_w(x)|\le WB=V$。因此损失在 $[0,M]$，$M=(V+Y_0)^2/2$；在预测区间 $[-V,V]$ 上对预测为 $C=V+Y_0$-Lipschitz。

线性预测类的 Rademacher complexity 满足

$$
\mathfrak R_n(\mathcal H)\le\frac{WB}{\sqrt n}=\frac V{\sqrt n}.
$$

减去损失的 $h$ 无关常数后，用 Lipschitz contraction 得到损失类复杂度不超过 $CV/\sqrt n$。为自包含地看清 contraction 的系数，可对一维符号逐步条件化：
$\frac12\sup_{u,v}[A_u+A_v+\psi(u)-\psi(v)]\le\frac12\sup_{u,v}[A_u+A_v+C|u-v|]$；交换 $u,v$ 使右边的绝对值可写成 $C(u-v)$，再逐坐标重复。这是 one-sided expected supremum 的系数 1 版本。

[T33](../proofs/generalization/T33-uniform-convergence.md) 的双侧界因此给出，条件概率至少 $1-\delta_S$，

$$
b_n:=\sup_{\|w\|\le W}|R(h_w)-R_n(h_w)|
\le\frac{2CV}{\sqrt n}+M\sqrt{\frac{\log(2/\delta_S)}{2n}}.
$$

它控制整个参数球，因此包括训练之后才选出的 $\bar w$。特征与训练集独立，使条件化后仍是 iid；若隐藏特征用本训练集学习，这个接口要重证。

## 5. 引理 C：确实控制经验优化 gap

固定特征后 $F(w)=R_n(h_w)$ 为凸函数，Hessian 为 $n^{-1}\sum_i\phi(X_i)\phi(X_i)^\top\preceq mI$。参数球紧，$F$ 连续，所以经验最优 $w^*$ 存在。

更新为 $w_{t+1}=\Pi_{\|w\|\le W}(w_t-\eta\nabla F(w_t))$。投影最优性给出

$$
\langle\nabla F(w_t),w_{t+1}-w^*\rangle
\le\frac{\|w_t-w^*\|^2-\|w_{t+1}-w^*\|^2-\|w_{t+1}-w_t\|^2}{2\eta}.
$$

再用 convexity 与 smoothness：
$F(w_{t+1})-F(w^*)\le\langle\nabla F(w_t),w_{t+1}-w^*\rangle+\frac m2\|w_{t+1}-w_t\|^2$。
$\eta=1/m$ 使移动平方项抵消。望远镜求和与 Jensen 得到

$$
F(\bar w)-F(w^*)\le\frac{\|w_0-w^*\|^2}{2\eta T}
\le\frac{mW^2}{2T}=\frac{V^2}{2T}.
$$

这里靠固定特征的凸性得到真正的 gap；只证明梯度小无法代替这一引理。

## 6. 合成主定理

对训练集事件中的任意输出，[T32](../proofs/generalization/T32-excess-risk-decomposition.md) 给出

$$
R(h_{\bar w})-R^*
\le[\inf_{\|w\|\le W}R(h_w)-R^*]+2b_n+[F(\bar w)-\inf F].
$$

代入 A、B、C 得到第 2 节的所有常数。A 的失败概率是 $\delta_A$；B 对每个已固定特征集的条件失败概率至多 $\delta_S$，tower property 给出无条件同一上界。union bound 因而为 $\delta_A+\delta_S$，不需要假设两个事件独立。

## 7. 检查哪些条件提供了结论

| 条件 | 在证明中的位置 | 改变后的义务 |
|---|---|---|
| 已知可抽样 $\pi$，目标有有界系数表示 | A 与可执行特征抽样 | 任意 variation 表示可能使用未知的目标依赖分布 |
| 特征与训练集独立 | B 的条件 iid | 学习隐藏层后需稳定性、sample split 或新复杂度界 |
| $|Y|$、$|\psi|$ 有界 | B 的 Lipschitz 与 loss range | 无界标签改用矩/尾条件，常数重推 |
| 参数球与 projected GD | C 的凸性、投影和输出 | Adam/全网络训练不能直接沿用 |
| 平均 $w_1,\ldots,w_T$ | C 的 Jensen | 最后迭代需另证对应结论 |
| 同一平方风险和输入 law | 三个引理接口 | 分类或分布转移分别用 T49/T19 的桥 |

计算上每步需 $n$ 个宽度 $m$ 的特征预测/梯度及一次球投影，特征本身的评估成本另计。比较 rate 时需同时报告宽度、样本、步数、精度与置信度。

若 $V,Y_0,\pi$ 与目标 law 固定，一个合法的联合增长安排是 $m(n)=T(n)=n$、$\delta_A(n)=\delta_S(n)=n^{-1/4}$（$n\ge2$）。逼近项为 $V^2/(2n^{3/4})$，训练项为 $V^2/(2n)$，统计项趋零，失败概率也趋零，因此得到总体 excess risk 依概率趋零。这里没有把期望界或依概率收敛升级为几乎处处收敛，也没有宣称此安排计算最优。

## 8. 怎样把它迁移到自己的论文

先保留第 2 节的目标量，再逐条替换 A/B/C。某个引理不适用，就把新的义务写在接口处；只有全部关闭后才更新主定理。

数学来源入口：[T41](../proofs/deep-learning/T41-barron-random-feature-approximation.md)、[T33](../proofs/generalization/T33-uniform-convergence.md)、[凸优化来源](../proof_ref/foundations-2026-09/convex-optimization-algorithms-and-complexity-1405.4980/README.md)。
可运行的小模型检查见 [代码](../examples/dl_specialization_checks.py)；代码检查有限实例的代数与行为，正文给出一般条件下的推导。
