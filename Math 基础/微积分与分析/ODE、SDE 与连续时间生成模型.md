---
type: note
domain: math/dynamical-systems
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# ODE、SDE 与连续时间生成模型

把生成过程想成搬运一团“概率云”：

- ODE 给每个点一支确定的速度箭头，点沿流线移动；
- SDE 除了确定漂移，还不断加入随机抖动；
- 连续性方程或 Fokker–Planck 方程站在上帝视角，描述整团概率云怎样变化。

Neural ODE、continuous normalizing flow、flow matching 和 score-based diffusion 都在使用这套语言，但它们学习的对象、路径随机性和训练目标并不相同。

## 知识依赖与相关笔记

- 总入口：[Math 基础目录](../Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md)、[AI Researcher 数学学习路线](../AI%20Researcher%20%E6%95%B0%E5%AD%A6%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)、[AI Researcher 高阶数学路线：LLM、CV 与生成模型](../AI%20Researcher%20%E9%AB%98%E9%98%B6%E6%95%B0%E5%AD%A6%E8%B7%AF%E7%BA%BF%EF%BC%9ALLM%E3%80%81CV%20%E4%B8%8E%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B.md)。
- 导数、Jacobian 与 divergence：[导数、梯度、Jacobian、Hessian 与自动微分](%E5%AF%BC%E6%95%B0%E3%80%81%E6%A2%AF%E5%BA%A6%E3%80%81Jacobian%E3%80%81Hessian%20%E4%B8%8E%E8%87%AA%E5%8A%A8%E5%BE%AE%E5%88%86.md)。
- 积分和密度变换：[积分、变量替换与概率密度变换](%E7%A7%AF%E5%88%86%E3%80%81%E5%8F%98%E9%87%8F%E6%9B%BF%E6%8D%A2%E4%B8%8E%E6%A6%82%E7%8E%87%E5%AF%86%E5%BA%A6%E5%8F%98%E6%8D%A2.md)。
- 随机过程：[Markov 链、随机过程与状态空间模型](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/Markov%20%E9%93%BE%E3%80%81%E9%9A%8F%E6%9C%BA%E8%BF%87%E7%A8%8B%E4%B8%8E%E7%8A%B6%E6%80%81%E7%A9%BA%E9%97%B4%E6%A8%A1%E5%9E%8B.md)。
- 分布与 score：[概率论主干：联合、条件、期望与协方差](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md)、[信息论基础：熵、交叉熵与 KL 散度](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E4%BF%A1%E6%81%AF%E8%AE%BA%E5%9F%BA%E7%A1%80%EF%BC%9A%E7%86%B5%E3%80%81%E4%BA%A4%E5%8F%89%E7%86%B5%E4%B8%8E%20KL%20%E6%95%A3%E5%BA%A6.md)。
- 生成模型专题：[扩散模型、Score Matching 与 Flow Matching](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B/%E6%89%A9%E6%95%A3%E6%A8%A1%E5%9E%8B%E3%80%81Score%20Matching%20%E4%B8%8E%20Flow%20Matching.md)、[Flow Matching](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B/Flow%20Matching.md)。
- 数值误差：[浮点数、数值稳定性与条件数](../%E6%95%B0%E5%80%BC%E8%AE%A1%E7%AE%97/%E6%B5%AE%E7%82%B9%E6%95%B0%E3%80%81%E6%95%B0%E5%80%BC%E7%A8%B3%E5%AE%9A%E6%80%A7%E4%B8%8E%E6%9D%A1%E4%BB%B6%E6%95%B0.md)、[Lipschitz constant](Lipschitz%20constant.md)。

## 1. ODE：速度场决定确定性轨迹

常微分方程（ODE）写成

$$
\frac{dx_t}{dt}=v(x_t,t),\qquad x_0\sim p_0.
$$

$v(x,t)$ 是向量场：它告诉位于 $x$ 的粒子在时刻 $t$ 应往哪里走、多快走。给定同一个初值，若解唯一，轨迹没有额外随机性；随机性只来自初值 $x_0$。

积分形式是

$$
x_t=x_0+\int_0^t v(x_s,s)\,ds.
$$

这说明 ODE 不是“每步套公式”，而是沿时间累计速度。

### 1.1 解何时存在且唯一

一个常用局部结论是：若 $v(x,t)$ 对 $t$ 连续，并在 $x$ 上局部 Lipschitz，则每个初值附近存在唯一局部解。若再有合适的全局增长控制，才能排除有限时间爆炸并得到更长区间的解。

“神经网络是连续的”不自动保证所有理想性质；激活、参数大小、时间依赖与数值误差都会影响轨迹。Lipschitz 条件的直觉见 [Lipschitz constant](Lipschitz%20constant.md)。

## 2. 数值解：电脑看到的是离散步

最简单的 Euler 法：

$$
x_{k+1}=x_k+v(x_k,t_k)\Delta t.
$$

它把短时间内的弯曲轨迹近似成直线。步长越小通常越准，但计算次数增加；高阶 Runge–Kutta 会在一步中多次评估速度场来降低误差。

需要区分三类误差：

- 模型误差：学到的 $v_\theta$ 不是真实目标速度；
- 离散化误差：数值 solver 没精确积分 ODE；
- 浮点误差：有限精度计算造成误差。

stiff ODE 含有差异很大的时间尺度，显式 solver 可能被迫使用极小步长。生成模型采样的 NFE（function evaluations）与误差容忍度是实际成本的一部分，不能只比较理论连续方程。

## 3. SDE：漂移上叠加持续随机扰动

Itô 随机微分方程写作

$$
dX_t=f(X_t,t)\,dt+G(X_t,t)\,dW_t,
$$

其中 $f$ 是 drift，$G$ 是 diffusion coefficient，$W_t$ 是 Brownian motion。

全局 Lipschitz 与线性增长是保证强解存在唯一的一组常用充分条件；更弱条件也可能成立，但若系数不规则或增长过快，解可能不唯一或发生爆炸。SDE 的建模公式并不自动附送良定性。

不要把 $dW_t$ 当普通的 $dt$。在很小时间段 $\Delta t$ 上：

$$
\Delta W\sim\mathcal N(0,\Delta t),
$$

所以随机增量尺度是 $\sqrt{\Delta t}$，比确定 drift 的 $\Delta t$ 更大阶。Brownian 轨迹几乎处处不可导，SDE 需要 Itô 或 Stratonovich 等随机积分定义。

### 3.1 Euler–Maruyama

SDE 对应的基本离散化为

$$
X_{k+1}=X_k+f(X_k,t_k)\Delta t
+G(X_k,t_k)\sqrt{\Delta t}\,\varepsilon_k,
\qquad \varepsilon_k\sim\mathcal N(0,I).
$$

漏掉平方根是常见且致命的错误。SDE 数值方法还要区分 strong error（同一噪声路径上的轨迹误差）和 weak error（期望/分布误差）；生成采样常更关心后者，但并非总是如此。

## 4. 从粒子轨迹到整团密度

### 4.1 ODE 对应连续性方程

若粒子按 $v(x,t)$ 移动，其密度满足

$$
\frac{\partial p_t(x)}{\partial t}
=-\nabla\cdot\big(p_t(x)v(x,t)\big).
$$

右边是概率流的散度：一个区域流出多于流入，密度就下降。它表达概率质量守恒，没有凭空创造或删除质量。

### 4.2 SDE 对应 Fokker–Planck 方程

一般 Itô SDE 令 $a(x,t)=G(x,t)G(x,t)^\top$，则在足够正则条件下

$$
\frac{\partial p_t}{\partial t}
=-\sum_i\partial_i(f_i p_t)
+\frac12\sum_{i,j}\partial_i\partial_j(a_{ij}p_t).
$$

第一项搬运密度，第二项扩散、抹平密度。若 $G=g(t)I$，第二项简化为 $\tfrac12g(t)^2\Delta p_t$。

这两个 PDE 描述边缘密度，而 ODE/SDE 描述单条样本路径。不要把“路径相同”和“每个时刻边缘分布相同”混为一谈。

## 5. 连续性方程：速度场怎样搬运密度

沿 ODE 轨迹 $x_t$，instantaneous change-of-variables 给出

$$
\frac{d}{dt}\log p_t(x_t)
=-\nabla\cdot v(x_t,t)
=-\operatorname{Tr}\left(\frac{\partial v}{\partial x}\right).
$$

它是离散 flow 的 $-\log|\det J|$ 在无限小时间步下的版本。continuous normalizing flow 可以同时积分状态和 log-density，但高维 divergence 的精确 trace 很贵，实践中常用 Hutchinson trace estimator 等随机近似。

## 6. Flow matching：直接学习搬运速度

flow matching 通常先指定从简单分布 $p_0$ 到数据分布 $p_1$ 的概率路径 $p_t$，再训练速度场 $v_\theta(x,t)$ 使其满足该路径的连续性方程。

一种常见训练形式是采样端点/条件变量和时间，构造中间点 $X_t$ 及条件目标速度 $u_t$，最小化

$$
\mathbb E\left[\|v_\theta(X_t,t)-u_t\|^2\right].
$$

在平方损失、采样过程与可积性等条件下，人口最优解是条件期望

$$
v^*(x,t)=\mathbb E[u_t\mid X_t=x],
$$

它产生所需的边缘概率流。工程上我们只得到有限网络、有限数据和有限优化下的近似。

重要边界：选择线性插值路径不自动意味着得到了 Wasserstein 最优传输 geodesic。是否为 OT 路径取决于端点 coupling 和速度场结构，见 [动态 OT](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%9C%80%E4%BC%98%E4%BC%A0%E8%BE%93%E4%B8%8E%20Wasserstein%20%E8%B7%9D%E7%A6%BB.md#7-%E5%8A%A8%E6%80%81-ot%E6%8A%8A%E6%90%AC%E5%9C%9F%E5%8F%98%E6%88%90%E8%BF%9E%E7%BB%AD%E6%B5%81)。

## 7. Score-based diffusion：学习密度朝哪里上升

分布 $p_t$ 的 score 是

$$
s_t(x)=\nabla_x\log p_t(x).
$$

注意这是对**样本 $x$** 求导，与 [Fisher 信息中的参数 score](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/Fisher%20%E4%BF%A1%E6%81%AF%E3%80%81%E8%87%AA%E7%84%B6%E6%A2%AF%E5%BA%A6%E4%B8%8E%E4%BF%A1%E6%81%AF%E5%87%A0%E4%BD%95.md#2-score%E5%AF%B9%E6%95%B0%E6%A6%82%E7%8E%87%E5%AF%B9%E5%8F%82%E6%95%B0%E7%9A%84%E6%95%8F%E6%84%9F%E5%BA%A6) 不同。

考虑常见的各向同性前向 SDE：

$$
dX_t=f(X_t,t)\,dt+g(t)\,dW_t.
$$

在密度光滑、正值等正则条件下，其 reverse-time SDE 可写成

$$
dX_t=\left[f(X_t,t)-g(t)^2\nabla_x\log p_t(X_t)\right]dt
+g(t)\,d\bar W_t,
$$

其中时间从 $T$ 向 $0$ 运行，所以这里的 $dt$ 是反向时间增量。若改用递增的新时间 $s=T-t$，漂移符号必须相应变换；抄公式时必须先确认时间约定。

训练网络 $s_\theta(x,t)$ 近似未知 score 后，就能从简单噪声分布反向采样。

## 8. Probability flow ODE：相同边缘，不同路径

同一个前向 SDE 还对应 probability flow ODE：

$$
\frac{dX_t}{dt}
=f(X_t,t)-\frac12g(t)^2\nabla_x\log p_t(X_t).
$$

在正则条件下，它与前向 SDE 在每个时刻拥有相同边缘分布 $p_t$，但单条路径和联合路径分布不同：

- SDE 路径随机、粗糙；
- probability flow ODE 给定初值后确定、通常平滑；
- reverse SDE 的 score 系数是 $1$，probability flow ODE 是 $1/2$。

“边缘相同”不代表任意路径相关量、coupling 或离散 solver 结果都相同。实际神经 score 有误差，数值离散也会进一步拉开差异。

## 9. 可运行示例：Ornstein–Uhlenbeck SDE

考虑

$$
dX_t=-\frac\beta2X_t\,dt+\sqrt\beta\,dW_t,
\qquad X_0=x_0.
$$

解析边缘为

$$
\mathbb E[X_t]=x_0e^{-\beta t/2},
\qquad
\operatorname{Var}(X_t)=1-e^{-\beta t}.
$$

```python
import numpy as np

rng = np.random.default_rng(13)
n_paths = 100_000
n_steps = 250
T = 1.0
dt = T / n_steps
beta = 2.0
x0 = 3.0

# Euler-Maruyama：噪声项必须乘 sqrt(dt)。
x = np.full(n_paths, x0)
for _ in range(n_steps):
    x += -0.5 * beta * x * dt + np.sqrt(beta * dt) * rng.normal(size=n_paths)

true_mean = x0 * np.exp(-0.5 * beta * T)
true_var = 1.0 - np.exp(-beta * T)
print("SDE empirical mean/variance:", x.mean(), x.var())
print("SDE analytic mean/variance:", true_mean, true_var)

assert abs(x.mean() - true_mean) < 0.02
assert abs(x.var() - true_var) < 0.02

# 去掉噪声后是确定 ODE dx/dt=-beta*x/2。
x_ode = x0
for _ in range(n_steps):
    x_ode += -0.5 * beta * x_ode * dt

print("ODE Euler / analytic:", x_ode, true_mean)
assert abs(x_ode - true_mean) < 0.01
```

这里“去掉噪声的 drift-only ODE”只是用来隔离随机项的作用，**不是**该 SDE 的 probability flow ODE；后者还需要依赖 score 的修正。drift-only ODE 与 SDE 的均值在这个线性例子中一致，但 SDE 产生非零方差，“均值轨迹相同”显然不等于“分布相同”。

## 10. 常见误区

1. **“ODE 只是连续层数的 ResNet。”** 这是有用类比，但严格分析还涉及解的存在唯一性、solver 与伴随梯度误差。
2. **“$dW$ 和 $dt$ 同阶。”** Brownian 增量尺度是 $\sqrt{dt}$。
3. **“SDE 路径可以普通求导。”** Brownian 路径几乎处处不可导，需要随机微积分；Itô 与 Stratonovich 约定也不能不加 drift 修正地互换。
4. **“Fokker–Planck 描述一条样本轨迹。”** 它描述整个边缘密度。
5. **“reverse SDE 只把 drift 加负号。”** 还会出现依赖 score 的修正项，且时间约定决定符号。
6. **“probability flow ODE 与 SDE 是同一随机过程。”** 它们可共享边缘密度，但路径 law 不同。
7. **“flow matching 必然学到最优传输。”** 一般只保证目标概率路径的速度回归，OT 需额外 coupling/目标。
8. **“连续模型没有离散化误差。”** 电脑最终仍运行数值 solver。
9. **“扩散 score 与 Fisher score 相同。”** 一个对样本求导，一个对参数求导。

## 11. 自测

1. ODE 的局部 Lipschitz 条件为什么与轨迹唯一性有关？
2. Euler–Maruyama 的噪声项为什么是 $\sqrt{\Delta t}$？
3. 连续性方程与 Fokker–Planck 方程分别对应什么动力学？
4. 写出沿 CNF 轨迹的 log-density 变化率，并解释 divergence。
5. reverse-time SDE 和 probability flow ODE 中 score 系数为何分别为 1 和 $1/2$？
6. “相同边缘分布”为什么不意味着相同 sample path 或 coupling？
7. flow matching 的人口平方损失最优解为什么是条件期望？

## 延伸阅读

- Øksendal, *Stochastic Differential Equations: An Introduction with Applications*.
- Kloeden & Platen, *Numerical Solution of Stochastic Differential Equations*.
- Chen et al., [Neural Ordinary Differential Equations](https://arxiv.org/abs/1806.07366), NeurIPS 2018.
- Song et al., [Score-Based Generative Modeling through Stochastic Differential Equations](https://openreview.net/forum?id=PxTIG12RRHS), ICLR 2021.
- Lipman et al., [Flow Matching for Generative Modeling](https://openreview.net/forum?id=PqvMRDCJT9t), ICLR 2023.
