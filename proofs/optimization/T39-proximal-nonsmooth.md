---
id: T39
type: proof-template
refined: 2026-09-28
status: self-contained-core
---

# T39. Proximal-gradient mapping and nonsmooth boundaries

[主题目录](README.md) · [普通下降](T01-descent.md)

## 复用契约

**输入对象**：复合目标 $F=f+g$，其中 $f$ 可非凸但为 $L$-smooth， $g$ proper、closed、convex 且可计算 proximal map； $F$ 有有限下界。

**输出结论**：proximal-gradient mapping 的下降与平均 stationarity 界，不把不可微 $F$ 的普通梯度当作目标量。

**失败例子**： $F(w)=(\mathop{\mathrm{ReLU}}(w)-1)^2$ 在 0 处左右导数分别为 0 与 -2，既不能直接套全局 smooth descent，也不能把任意 ReLU 网络目标视为本卡的 smooth-plus-convex 结构。

## 实例化时必须完成

- [ ] 证明真实目标确有所述分解，不能把“不可微”当作满足所有 proximal 条件。
- [ ] 写出 proximal 子问题与步长，区分精确和近似解。
- [ ] 使用 gradient mapping/合适 subdifferential stationarity。
- [ ] 对一般非凸非光滑 ReLU 目标，选择真正适用的分析，不自动从几乎处处可微推出下降。

## 1. 为什么需要换一个下降工具

L1 正则和凸约束可能没有普通梯度，却有可计算的 prox。它像一次带规则的纠偏：先按 smooth 部分走，再用一个局部二次子问题处理非光滑部分。

$$
x^+=\mathop{\mathrm{prox}}\nolimits_{\eta g}(x-\eta\nabla f(x))
=\arg\min_z\left\lbrace
g(z)+\frac1{2\eta}\Vert z-x+\eta\nabla f(x)\Vert^2
\right\rbrace.
$$

例如 $g$ 是凸集的 indicator 时，prox 就是 Euclidean projection； $g(x)=\lambda\Vert x\Vert_1$ 时，prox 是 soft thresholding。

## 2. 定义正确的 stationarity 量

$$
G_\eta(x)=\frac{x-x^+}{\eta}.
$$

若 $g=0$，它退化成 $\nabla f(x)$。一般情形中
$G_\eta(x)=0$ 等价于 $0\in\nabla f(x)+\partial g(x)$，这里 $\partial g$ 为凸次微分。

## 3. 从子问题最优性得到下降

记 $\Delta=x^+-x$。prox 的最优性条件给出

$$
-\nabla f(x)-\Delta/\eta\in\partial g(x^+).
$$

由 $g$ 凸，

$$
g(x)\geq g(x^+)+\langle\nabla f(x),\Delta\rangle+
\Vert\Delta\Vert^2/\eta.
$$

另由 $f$ 光滑，

$$
f(x^+)\leq f(x)+\langle\nabla f(x),\Delta\rangle+
\frac L2\Vert\Delta\Vert^2.
$$

相加、抵消内积后得到

$$
F(x^+)\leq F(x)-\left(\frac1\eta-\frac L2\right)\Vert\Delta\Vert^2.
$$

若 $0<\eta\leq1/L$，

$$
F(x^+)\leq F(x)-\frac\eta2\Vert G_\eta(x)\Vert^2.
$$

## 4. 累加后的保证

确定性精确 proximal-gradient 迭代因此满足

$$
\frac1T\sum_{t< T}\Vert G_\eta(x_t)\Vert^2
\leq\frac{2(F(x_0)-F_\inf)}{\eta T}.
$$

这个结果不要求整体 $F$ 凸，但只控制 stationarity。若要全局函数 gap、线性收敛或统计风险，仍须补凸性、PL 型条件或 [T32](../generalization/T32-excess-risk-decomposition.md) 的其他环节。

还可在 $x^+$ 构造一个真实复合次梯度

$$
v^+=\nabla f(x^+)-\nabla f(x)+G_\eta(x)
\in\nabla f(x^+)+\partial g(x^+),
$$

并界 $\Vert v^+\Vert\leq(1+L\eta)\Vert G_\eta(x)\Vert$。

## 5. 不能跳过的实现差异

近似 prox、随机梯度、非凸 penalty 或自适应 metric 都改变证明，需要保留子问题残差、估计误差或新的最优性条件。

“ReLU 几乎处处可微”本身不证明全局 Lipschitz gradient；跨 kink 的更新必须由适用的非光滑理论分析。本卡不覆盖任意非凸非光滑网络。

前置：[凸性](<../../Math 基础/微积分与分析/凸集、凸函数与优化直觉.md>)、[最优性与约束](<../../Math 基础/微积分与分析/拉格朗日乘子、对偶与约束优化.md>)。来源：[Convex Optimization: Algorithms and Complexity](https://arxiv.org/abs/1405.4980)；本卡给出上述复合结构的具体下降推导。

## 本地论文与前置工具

通用工具：P02, P06，见 [证明原语](../../通用证明原语.md)。

- [Convex Optimization: Algorithms and Complexity](../../proof_ref/foundations-2026-09/convex-optimization-algorithms-and-complexity-1405.4980/README.md)
- [The Modern Mathematics of Deep Learning](../../proof_ref/dl-core-2026-09/the-modern-mathematics-of-deep-learning-2105.04026/README.md)

## 专项证明接口（2026-10-02）

- [T40：用负曲率下降补一阶驻点，并显式区分 Hessian oracle 与一阶逃逸复杂度。](T40-second-order-stationarity.md)
