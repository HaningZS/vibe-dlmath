---
type: note
domain: math/analysis-dynamical-systems
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# Grönwall、Duhamel 与稳定性误差传播

近期证明蒸馏：[T51 Flow Matching 的速度—轨迹—分布误差](../../proofs/generation-transport/T51-flow-trajectory-error.md)，重点是加减哪个中间场、误差在哪个 law 下，以及学习场正则性。

证明进阶：[T42 时变核与冻结核之间的 Duhamel 误差](../../proofs/deep-learning/T42-feature-drift-kernel-dynamics.md)。

很多理论证明最终都在回答同一个问题：**一个很小的局部误差，经过很多步或很长时间后，会变成多大的全局误差？**

可以把误差想成银行账户：

- 系统本身的动力学决定旧误差会“生利息”还是“被打折”；
- 每一步的近似、噪声和模型偏差会继续往账户里存入新误差；
- Grönwall 不等式负责算最坏情况下的复利总额；
- Duhamel 公式进一步告诉我们：**每个时刻注入的误差，后来分别经过了怎样的传播。**

这套语言连接优化器稳定性、ODE/SDE 数值误差、Neural ODE、flow matching、diffusion，以及受迫输运 PDE。

## 知识依赖与证明导航

- 数学入口：[Math 基础目录](../Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md)、[AI 理论证明前置学习路线](../%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/AI%20%E7%90%86%E8%AE%BA%E8%AF%81%E6%98%8E%E5%89%8D%E7%BD%AE%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)。
- 建议先读：[Lipschitz constant](Lipschitz%20constant.md)、[一阶泰勒展开](%E4%B8%80%E9%98%B6%E6%B3%B0%E5%8B%92%E5%B1%95%E5%BC%80.md)、[ODE、SDE 与连续时间生成模型](ODE%E3%80%81SDE%20%E4%B8%8E%E8%BF%9E%E7%BB%AD%E6%97%B6%E9%97%B4%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B.md)。
- 离散势函数：[梯度下降、学习率与收敛](%E6%A2%AF%E5%BA%A6%E4%B8%8B%E9%99%8D%E3%80%81%E5%AD%A6%E4%B9%A0%E7%8E%87%E4%B8%8E%E6%94%B6%E6%95%9B.md)、[量词、归纳、不变量与望远镜求和](../%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/%E9%87%8F%E8%AF%8D%E3%80%81%E5%BD%92%E7%BA%B3%E3%80%81%E4%B8%8D%E5%8F%98%E9%87%8F%E4%B8%8E%E6%9C%9B%E8%BF%9C%E9%95%9C%E6%B1%82%E5%92%8C.md)。
- 证明原语：[P07：收缩、Grönwall 与稳定性](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p07-contractiongr%C3%B6nwall-%E4%B8%8E%E7%A8%B3%E5%AE%9A%E6%80%A7%E9%80%92%E6%8E%A8)。
- 相关模板：[T10：mean-field / propagation of chaos](../../proofs/deep-learning/T10-mean-field.md)、[T13：生成采样误差分解](../../proofs/generation-transport/T13-sampler-error.md)。
- 近期方法卡：[R10：Flow error PDE](../../%E8%BF%91%E6%9C%9F%E9%A1%B6%E4%BC%9A%E7%90%86%E8%AE%BA%E6%A1%86%E6%9E%B6%EF%BC%882025-2026%EF%BC%89.md#r10-flow-error-pde--duhamel--tv-bound--trainable-surrogate)。
- 原文入口：[Flow divergence PDF p.4：受迫 PDE 与 Duhamel](../../proof_ref/recent-accepted-2025-2026/improving-flow-matching-by-aligning-flow-divergence-2602.00869/paper.pdf#page=4)、[Flow divergence PDF p.14：完整推导](../../proof_ref/recent-accepted-2025-2026/improving-flow-matching-by-aligning-flow-divergence-2602.00869/paper.pdf#page=14)。

## 1. 为什么“局部误差求和”通常不够

假设第 $k$ 步新产生误差 $b_k$。直接写

$$
e_n\le e_0+\sum_{k=0}^{n-1}b_k
$$

隐含了一个很强的假设：旧误差进入后，系统既不放大它，也不缩小它。

真实递推更常见的是

$$
e_{k+1}\le a_k e_k+b_k.
$$

- $a_k<1$：系统会遗忘旧误差；
- $a_k=1$：误差近似直接累加；
- $a_k>1$：早期误差会被反复放大。

所以不能只问“每一步错多少”，还要问“这一步错误之后要乘多少次传播因子”。这就是稳定性分析的核心。

## 2. Contraction：每走一步，距离都打折

设 $(X,d)$ 是完备度量空间。映射 $F:X\to X$ 若满足

$$
d(F(x),F(y))\le q\,d(x,y),\qquad 0\le q<1,
$$

就叫 contraction（压缩映射）。它像一台每次都把两点距离压成原来 $q$ 倍的机器。

Banach fixed-point theorem 告诉我们：

1. $F$ 有唯一不动点 $x^*$，即 $F(x^*)=x^*$；
2. 迭代 $x_{k+1}=F(x_k)$ 从任意初值收敛到 $x^*$；
3. 误差按几何速度缩小：

$$
d(x_k,x^*)\le q^k d(x_0,x^*).
$$

### 2.1 为什么必须是 $q<1$

Lipschitz 常数有限只说明映射不会无限敏感；只有 $q<1$ 才说明每步都严格压缩。 $q=1$ 的恒等映射有无数不动点， $q>1$ 更可能放大差异。

### 2.2 带扰动的 contraction

以下进入 Banach/赋范向量空间，并令度量由范数诱导，才能写 $F(x_k)+r_k$。在一般 metric space 中，应改写为

$$
d(x_{k+1},F(x_k))\le r_k
$$

再用三角不等式递推。

现实算法常是

$$
x_{k+1}=F(x_k)+r_k,
$$

而理想轨迹为 $y_{k+1}=F(y_k)$。令 $e_k=d(x_k,y_k)$，则

$$
e_{k+1}\le q e_k+\|r_k\|.
$$

展开后得到

$$
e_n\le q^n e_0+\sum_{j=0}^{n-1}q^{n-1-j}\|r_j\|.
$$

早期扰动会多乘几次 $q$，因此被遗忘；最近的扰动还没来得及衰减。若每步 $\|r_j\|\le r$，长期误差不超过约 $r/(1-q)$，而不是随步数无限线性增长。

## 3. 离散 Grönwall：把递推完整展开

对一般非负递推

$$
e_{k+1}\le (1+a_k)e_k+b_k,
\qquad a_k,b_k\ge0,
$$

逐步代入可得

$$
e_n
\le
e_0\prod_{i=0}^{n-1}(1+a_i)
+\sum_{j=0}^{n-1}
b_j\prod_{i=j+1}^{n-1}(1+a_i).
$$

这比“套一个指数”更有信息：它保留了每个 $b_j$ 的注入时间和传播长度。

利用 $1+x\le e^x$，可进一步得到较易读但可能较松的形式：

$$
e_n
\le
\exp\!\left(\sum_{i=0}^{n-1}a_i\right)
\left(e_0+\sum_{j=0}^{n-1}b_j\right).
$$

### 3.1 从离散算法到连续时间尺度

若一步长度为 $h$，递推为

$$
e_{k+1}\le (1+hL)e_k+h\delta_k,
$$

且 $t_n=nh$，那么

$$
(1+hL)^n\le e^{Lnh}=e^{Lt_n}.
$$

这解释了连续 Grönwall 中 $e^{Lt}$ 的来源：它就是许多个微小放大因子的复利极限。

### 3.2 有收缩性时不要丢掉负号

如果真正得到

$$
e_{k+1}\le (1-h\mu)e_k+h\delta,
\qquad 0<h\mu<1,
$$

则

$$
e_k\le (1-h\mu)^k e_0
+\frac{\delta}{\mu}\bigl(1-(1-h\mu)^k\bigr).
$$

长期误差趋近 $\delta/\mu$。若粗暴地把 $-\mu$ 改成 $+\mu$ 再套 Grönwall，会得到指数增长的无用上界。证明时应尽量保留单调性、strong convexity 或 dissipativity 提供的收缩结构。

## 4. 连续 Grönwall：连续时间的误差复利

设非负函数 $u(t)$ 满足

$$
u(t)\le A+\int_0^t a(s)u(s)\,ds,
\qquad a(s)\ge0.
$$

则

$$
u(t)\le A\exp\!\left(\int_0^t a(s)\,ds\right).
$$

若还有持续外力 $b(t)$：

$$
u(t)\le A+\int_0^t a(s)u(s)\,ds+\int_0^t b(s)\,ds,
$$

更精细的形式是

$$
u(t)
\le
A e^{\int_0^t a(r)\,dr}
+\int_0^t
b(s)e^{\int_s^t a(r)\,dr}\,ds.
$$

直觉上，时刻 $s$ 注入的误差 $b(s)\,ds$ 只在剩余区间 $[s,t]$ 内生“利息”。

### 4.1 一个最常用的推导

若两条 ODE 轨迹满足

$$
\dot x=f(x,t),\qquad
\dot y=g(y,t),
$$

并且 $f$ 对状态是 $L$-Lipschitz，那么形式上

$$
\frac{d}{dt}\|x-y\|
\le
L\|x-y\|+\|f(y,t)-g(y,t)\|.
$$

于是

$$
\|x_t-y_t\|
\le
e^{Lt}\|x_0-y_0\|
+\int_0^t e^{L(t-s)}
\|f(y_s,s)-g(y_s,s)\|\,ds.
$$

两类误差被清楚分开了：初值差异，以及动力学本身的差异。

## 5. Duhamel / variation of constants：每一份外力怎样传播

考虑线性受迫系统

$$
\dot x(t)=Ax(t)+r(t),\qquad x(0)=x_0.
$$

齐次系统 $\dot x=Ax$ 的传播算子是 $e^{At}$。Duhamel 公式为

$$
x(t)
=e^{At}x_0
+\int_0^t e^{A(t-s)}r(s)\,ds.
$$

可以把 $r(s)\,ds$ 想成时刻 $s$ 敲响的一记小钟声； $e^{A(t-s)}$ 描述这记声音传播到时刻 $t$ 后还剩多少、转到了哪些方向。

- 第一项是没有外力时的自由演化；
- 第二项是过去所有 forcing 的响应叠加；
- 若 $\|e^{At}\|\le Me^{\omega t}$，马上得到稳定性上界。

Grönwall 通常只给“总量最多多大”；Duhamel 还保留了误差来源、注入时间与传播算子，因此更适合做精细误差分解。

### 5.1 非线性系统怎么用

非线性差值常可写成

$$
\dot e(t)=A(t)e(t)+r(t),
$$

其中 $A(t)$ 来自 Jacobian 的积分平均，例如

$$
f(x)-f(y)
=\left[\int_0^1
J_f\bigl(y+\tau(x-y)\bigr)\,d\tau\right](x-y).
$$

随后使用 time-ordered fundamental matrix，或只对范数应用 Grönwall。前者更精细，后者更简单。

## 6. Characteristics：沿着流线读受迫输运 PDE

ODE 描述单个粒子，连续性方程描述整团密度。考虑保守形式的受迫输运 PDE：

$$
\partial_t\varepsilon_t(x)
+\nabla\cdot\bigl(\varepsilon_t(x)v_t(x)\bigr)
=L_t(x).
$$

展开散度：

$$
\partial_t\varepsilon
+v\cdot\nabla\varepsilon
+(\nabla\cdot v)\varepsilon
=L.
$$

令 characteristic flow 满足

$$
\frac{d}{dt}\phi_t(x)=v_t(\phi_t(x)),
\qquad \phi_0(x)=x.
$$

沿着这条流线，PDE 变成一个 ODE。若 $J_t(x)=\det D\phi_t(x)$，则

$$
\frac{d}{dt}
\left[\varepsilon_t(\phi_t(x))J_t(x)\right]
=L_t(\phi_t(x))J_t(x).
$$

积分得到 PDE 版 Duhamel：

$$
\varepsilon_t(\phi_t(x))J_t(x)
=\varepsilon_0(x)
+\int_0^t L_s(\phi_s(x))J_s(x)\,ds.
$$

这里 Jacobian determinant 负责记录流把体积压缩或膨胀了多少。再对空间积分并做变量替换，就能把 forcing 的 $L^1$ 大小转成 density error 或 TV distance 的上界。

这正是 [R10](../../%E8%BF%91%E6%9C%9F%E9%A1%B6%E4%BC%9A%E7%90%86%E8%AE%BA%E6%A1%86%E6%9E%B6%EF%BC%882025-2026%EF%BC%89.md#r10-flow-error-pde--duhamel--tv-bound--trainable-surrogate) 的关键链条：

```text
两条 continuity equations 相减
→ 得到受迫输运 PDE
→ 沿 characteristics 写 Duhamel
→ 换元控制 L1 / TV
→ 再把不可训练的 marginal residual 换成可训练 surrogate
```

注意：这一步需要密度、向量场、flow 和 Jacobian 的正则性。不能看到 continuity equation 就默认所有换元和微分都合法。

## 7. 它怎样出现在 AI 理论里

### 7.1 数值 ODE：local truncation error 到 global error

数值方法每步有局部截断误差 $\tau_k$：

$$
e_{k+1}\le (1+hL)e_k+h\tau_k.
$$

离散 Grönwall 将局部一致性升级成有限时间全局误差。稳定性差时，即使每步很准，误差也可能被动力学放大。

### 7.2 优化器与算法稳定性

在只相差一个样本的两个数据集上运行同一优化器，令参数差为 $\Delta_t$。常见递推是

$$
\mathbb E\|\Delta_{t+1}\|
\le
(1+\eta_t L_t)\mathbb E\|\Delta_t\|
+\eta_t\,\text{single-sample perturbation}.
$$

离散 Grönwall 把单样本影响传播到最终参数或 loss。这只是骨架；最终是 parameter stability、loss stability，还是 expectation/high-probability guarantee，必须单独说明。

### 7.3 Mean-field 与 propagation of chaos

比较有限粒子系统和极限分布时，coupling 后常得到

$$
e(t)\le e(0)+L\int_0^t e(s)\,ds+\text{finite-particle fluctuation}.
$$

Grönwall 给有限时间误差。但 $e^{LT}$ 可能使长时间结论很弱；若系统有 dissipativity、凸性或 contractivity，应使用更强结构。

### 7.4 SDE：共同噪声 coupling 与 Itô 修正

只有在 additive/common noise 下，或耦合后两条路径上的 diffusion matrix 逐时完全相同（例如同一个 state-independent $\Sigma_t$），同步使用同一 Brownian path 才会让噪声项抵消。若只是使用同一个状态依赖函数 $\sigma(\cdot)$，但 $X_t\ne Y_t$，差分仍含 $(\sigma(X_t)-\sigma(Y_t))\,dW_t$；这时对 $\|X_t-Y_t\|^2$ 使用 Itô formula 会出现 quadratic-variation 项，随后往往还需要 martingale/BDG 不等式。

因此本笔记只给稳定性入口，**没有完整覆盖随机积分理论**。Girsanov 更是“改变路径测度”的工具，不是 Grönwall 的别名；可先看 [Score-model PDF p.91–93：Girsanov 与路径 KL](../../proof_ref/recent-accepted-2025-2026/approximation-and-generalization-abilities-of-score-based-neural-2505.10880/paper.pdf#page=91)，再系统学习 Itô calculus、Novikov 条件和 Radon–Nikodym derivative。

## 8. 可运行 NumPy 示例：离散 Duhamel 与误差包络

考虑二维稳定线性系统的误差递推：

$$
e_{k+1}=\Phi e_k+h r_k,
\qquad \Phi=I+hA.
$$

下面同时验证：

1. 递推解等于离散 Duhamel 卷积；
2. contraction bound 确实包住真实误差；
3. 越早注入的扰动会多乘几次传播矩阵。

```python
import numpy as np

dt = 0.02
n_steps = 200
A = np.diag([-1.0, -3.0])
Phi = np.eye(2) + dt * A
rho = np.linalg.norm(Phi, ord=2)
assert rho < 1.0  # 这个离散步长下，传播矩阵是 contraction。

t = np.arange(n_steps) * dt
forcing = np.column_stack([
    0.08 * np.ones(n_steps),
    0.05 * np.sin(2.0 * t),
])

e0 = np.array([0.5, -0.25])
errors = np.empty((n_steps + 1, 2))
errors[0] = e0

# 直接递推。
for k in range(n_steps):
    errors[k + 1] = Phi @ errors[k] + dt * forcing[k]

# 离散 Duhamel：初值的自由传播 + 每次 forcing 的传播。
duhamel = np.empty_like(errors)
duhamel[0] = e0
for n in range(1, n_steps + 1):
    value = np.linalg.matrix_power(Phi, n) @ e0
    for j in range(n):
        value += (
            np.linalg.matrix_power(Phi, n - 1 - j)
            @ (dt * forcing[j])
        )
    duhamel[n] = value

assert np.allclose(errors, duhamel, atol=1e-12)

# 范数包络：||e_{k+1}|| <= rho ||e_k|| + dt ||r_k||。
bound = np.empty(n_steps + 1)
bound[0] = np.linalg.norm(e0)
for k in range(n_steps):
    bound[k + 1] = rho * bound[k] + dt * np.linalg.norm(forcing[k])

actual = np.linalg.norm(errors, axis=1)
assert np.all(actual <= bound + 1e-12)

print("spectral contraction factor:", rho)
print("final error norm:", actual[-1])
print("final guaranteed bound:", bound[-1])
```

这个 bound 不一定紧，因为 $\|a+b\|\le\|a\|+\|b\|$ 丢掉了方向抵消；但它明确、可靠，并保留了收缩因子。

## 9. 读证明时的检查清单

- [ ] 被控制的误差 $e_t$ 是参数距离、函数值、 $L^1$、TV、Wasserstein，还是别的 metric？
- [ ] 递推是路径上成立、取期望后成立，还是只在 good event 上成立？
- [ ] 放大系数是否真是非负的？有没有可保留的收缩负号？
- [ ] 时间变化的 $L_t$ 是否被错误替换成一个极其松的全局最大值？
- [ ] forcing 的单位是否与误差一致？
- [ ] 连续 Duhamel 所需的 flow/Jacobian/换元正则性是否写明？
- [ ] SDE 中是否遗漏 quadratic variation 或 martingale 项？
- [ ] 结论只对固定有限时间成立，还是能 uniform-in-time？指数因子是否让长时间结论失效？

## 10. 常见误区

1. **“Grönwall 就是把所有东西乘 $e^{LT}$。”** 指数形式只是方便上界；有 contraction、time-varying coefficient 或 semigroup 信息时应保留更精细结构。
2. **“每步误差 $O(h^2)$，做 $1/h$ 步后必然是 $O(h)$。”** 还需要稳定性；传播因子可能放大误差。
3. **“Duhamel 只适用于 PDE。”** 它首先是线性受迫演化的 variation-of-constants 公式，ODE、PDE 和 semigroup 都使用同一思想。
4. **“Lipschitz 自动意味着 contraction。”** 只有常数严格小于 $1$ 的离散映射才是 contraction；连续动力学还常看 one-sided Lipschitz/dissipativity。
5. **“同步 coupling 后 SDE 和 ODE 一样。”** 只有某些噪声项相同才会抵消；一般还要 Itô、quadratic variation 和 martingale 控制。
6. **“TV bound 小就说明每条生成轨迹接近。”** TV 控制分布，不自动控制指定 coupling 下的逐路径距离。

## 11. 自测

1. 为什么 $e_{k+1}\le(1+hL)e_k+h\delta_k$ 不能只把 $\delta_k$ 求和？
2. 推导 $e_{k+1}\le q e_k+r$ 的闭式上界，并解释长期误差为什么是 $r/(1-q)$。
3. Duhamel 公式中的 $e^{A(t-s)}$ 为什么依赖 $t-s$ 而不是 $t$？
4. 在什么情况下保留 $-\mu e_t$ 会比套普通 Grönwall 强很多？
5. 连续性方程沿 characteristics 后为什么会出现 Jacobian determinant？
6. SDE 稳定性证明中，什么时候共同 Brownian noise 会抵消，什么时候不会？

## 权威来源与延伸阅读

- Banach fixed-point theorem 与 Grönwall：Gerald Teschl, *Ordinary Differential Equations and Dynamical Systems*, AMS, 2012。
- 变参数法与数值稳定性：Hairer, Nørsett & Wanner, *Solving Ordinary Differential Equations I*, 2nd ed., Springer, 1993。
- Characteristics 与输运 PDE：Lawrence C. Evans, *Partial Differential Equations*, 2nd ed., AMS, 2010。
- Flow-matching 证明实例：[Improving Flow Matching by Aligning Flow Divergence, p.4](../../proof_ref/recent-accepted-2025-2026/improving-flow-matching-by-aligning-flow-divergence-2602.00869/paper.pdf#page=4)。
- SDE 入门：Bernt Øksendal, *Stochastic Differential Equations*, 6th ed., Springer, 2003。
