---
type: note
domain: math/stochastic-processes
status: active
created: 2026-09-01
reviewed: 2026-10-20
---

# Markov 链、随机过程与状态空间模型

静态概率分布描述“一张照片里的不确定性”，随机过程描述“一段电影里的不确定性”。天气、机器人位置、用户状态、扩散采样轨迹都会随时间变化；关键不只是每一帧可能是什么，还包括**状态怎样从上一刻演化到下一刻**。

Markov 链用“当前状态浓缩了预测未来所需的信息”简化这段电影。状态空间模型再加入一个现实问题：真正状态常看不见，只能通过带噪观测推断。

## 知识依赖与相关笔记

- 总入口：[Math 基础目录](../Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md)；针对 AI research 的学习顺序：[AI Researcher 数学学习路线](../AI%20Researcher%20%E6%95%B0%E5%AD%A6%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)。
- 条件概率、联合分布：[概率论主干：联合、条件、期望与协方差](%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md)。
- 随机估计与相关样本：[大数定律、中心极限定理与采样误差](%E5%A4%A7%E6%95%B0%E5%AE%9A%E5%BE%8B%E3%80%81%E4%B8%AD%E5%BF%83%E6%9E%81%E9%99%90%E5%AE%9A%E7%90%86%E4%B8%8E%E9%87%87%E6%A0%B7%E8%AF%AF%E5%B7%AE.md)。
- 以 Markov 链构造采样器：[蒙特卡洛、重要性采样与 MCMC](%E8%92%99%E7%89%B9%E5%8D%A1%E6%B4%9B%E3%80%81%E9%87%8D%E8%A6%81%E6%80%A7%E9%87%87%E6%A0%B7%E4%B8%8E%20MCMC.md)。
- 仓库内决策版本：[T07 的 MDP、价值函数与 Bellman 推导](../../proofs/sequential-decision/T07-bellman.md)。
- 线性高斯模型依赖：[向量空间、基、秩与 SVD](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E5%90%91%E9%87%8F%E7%A9%BA%E9%97%B4%E3%80%81%E5%9F%BA%E3%80%81%E7%A7%A9%E4%B8%8E%20SVD.md)、[常见概率分布与指数族](%E5%B8%B8%E8%A7%81%E6%A6%82%E7%8E%87%E5%88%86%E5%B8%83%E4%B8%8E%E6%8C%87%E6%95%B0%E6%97%8F.md)。
- 生成过程：[扩散模型、Score Matching 与 Flow Matching](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B/%E6%89%A9%E6%95%A3%E6%A8%A1%E5%9E%8B%E3%80%81Score%20Matching%20%E4%B8%8E%20Flow%20Matching.md)。
- 从离散时间链走向连续轨迹与扩散：[ODE、SDE 与连续时间生成模型](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/ODE%E3%80%81SDE%20%E4%B8%8E%E8%BF%9E%E7%BB%AD%E6%97%B6%E9%97%B4%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B.md)。

## 1. 随机过程：一整族带索引的随机变量

随机过程是随机变量的集合

$$
\lbrace X_t:t\in\mathcal T\rbrace.
$$

$t$ 常表示时间，也可以是空间位置或其他索引。

- 时间离散、状态离散：网页之间的用户跳转；
- 时间离散、状态连续：每帧中的机器人位置；
- 时间连续、状态离散：服务器故障/恢复；
- 时间连续、状态连续：Brownian motion 或随机微分方程。

对单个 $t$ 的边缘分布 $p(X_t)$ 还不够。两个过程可以每一时刻都服从同样的分布，却有完全不同的时间相关性：一个每帧独立抽样，另一个缓慢漂移。

## 2. Markov 链：下一步只看当前状态

一阶 Markov 性写成

$$
P(X_{t+1}=x_{t+1}\mid X_t=x_t,\ldots,X_0=x_0)
=P(X_{t+1}=x_{t+1}\mid X_t=x_t).
$$

这不是说“过去没有影响”，而是说过去对未来的影响已经被当前状态压缩了。类比下棋：如果“当前状态”包含完整棋盘和轮到谁走，就不必知道棋子移动历史来决定大多数合法下一步；若状态只记录棋子总数，就丢失了必要信息，Markov 假设便不成立。

因此 Markov 性取决于**怎样定义状态**。把最近 $k$ 步拼成扩展状态，可以把 $k$ 阶依赖改写成一阶 Markov 过程，但状态空间会变大。

### 2.1 转移矩阵

有限状态、时间齐次 Markov 链由转移矩阵 $P$ 描述：

$$
P_{ij}=P(X_{t+1}=j\mid X_t=i),
\qquad P_{ij}\ge0,\quad \sum_jP_{ij}=1.
$$

本文用**行向量**表示状态分布。若当前分布为 $\mu_t$，则

$$
\mu_{t+1}=\mu_tP,\qquad
\mu_{t+k}=\mu_tP^k.
$$

不要混用行、列向量约定；不同教材会写成 $P\mu_t$。

## 3. 平稳分布：走很久后的长期比例

若分布 $\pi$ 满足

$$
\pi=\pi P,
$$

则称为平稳分布。若链从 $X_0\sim\pi$ 开始，之后每一时刻的边缘分布都仍是 $\pi$。

平稳不等于样本不动：链可以持续跳转，只是总体比例不变，像一座人口稳定的城市，居民每天仍在不同区域流动。

### 3.1 有平稳分布不等于一定收敛到它

对有限状态链，常见的充分条件是：

- **不可约**：任意状态最终都能到达任意其他状态；
- **非周期**：不会被迫只在固定节拍返回；
- 有限不可约链是正常返（positive recurrent）的，并有唯一平稳分布。

在这些条件下， $\mu_0P^t$ 会收敛到唯一 $\pi$。若链分成互不连通的类，长期结果会依赖起点；若严格在两个状态间来回跳，虽有平稳分布，边缘分布也可能振荡而不收敛。

### 3.2 Detailed balance 是方便的充分条件，不是定义

若

$$
\pi_iP_{ij}=\pi_jP_{ji}
$$

对所有 $i,j$ 成立，则链满足 detailed balance，因而 $\pi$ 平稳。它表达平衡时任意两状态间的概率流量相互抵消。

但平稳链不一定可逆，也不一定满足 detailed balance。MCMC 常用它来方便地构造目标平稳分布，不能把它当作所有 Markov 链的必要条件。

## 4. Mixing：忘掉起点需要多久

Mixing time 衡量从最坏起点出发，分布接近平稳分布需要多少步。对有限、不可约、非周期且可逆的链，转移算子在 $L^2(\pi)$ 中有良好的正交谱分解；此时第二大特征值模越接近 1，谱隙越小，某些偏离平稳的方向衰减越慢。

这连接到 [eigenvalue and eigenvector](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/eigenvalue%20and%20eigenvector.md)：平稳分布对应特征值 1 的左特征向量。在上述可逆/正规条件下，其他特征模式可清楚描述暂态衰减；对非可逆、非正规链，仅看特征值可能不够，还要结合奇异值、conductance、coupling 或其他 mixing 界。

高自环概率、狭窄瓶颈和相隔很远的模式都会导致慢混合。MCMC 中“链跑了十万步”没有脱离 mixing 的绝对意义。

## 5. 隐状态：我们看到的常常只是带噪信号

状态空间模型通常写成

$$
z_t\sim p(z_t\mid z_{t-1}),\qquad
y_t\sim p(y_t\mid z_t),
$$

其中：

- $z_t$ 是不可直接观察的状态；
- $y_t$ 是传感器、token、图像或行为观测；
- 转移模型说明世界怎样演化；
- 观测模型说明状态怎样产生数据。

类比在雾中跟踪汽车：汽车真实位置是 $z_t$，雷达读数是 $y_t$。你既不能完全相信雷达，也不能只靠上一刻速度外推；合理估计必须融合动力学预测和新观测证据。

### 5.1 Hidden Markov Model（HMM）

HMM 是离散隐状态的状态空间模型，通常假设：

$$
p(z_{1:T},y_{1:T})
=p(z_1)\prod_{t=2}^T p(z_t\mid z_{t-1})
\prod_{t=1}^T p(y_t\mid z_t).
$$

关键条件独立是假设给定 $z_t$ 后， $y_t$ 不再依赖其他状态和观测。这个假设便于计算，但是否合理取决于状态是否包含足够信息。

## 6. 预测、滤波和平滑不要混为一谈

在时刻 $t$：

- **预测**： $p(z_t\mid y_{1:t-1})$，看当前观测前预测状态；
- **滤波**： $p(z_t\mid y_{1:t})$，融合截至当前的所有观测；
- **平滑**： $p(z_t\mid y_{1:T})$，用未来观测回头改善过去状态；
- **一步预测观测**： $p(y_{t+1}\mid y_{1:t})$。

滤波的递推只有两步：

1. 通过转移模型预测：

$$
p(z_t\mid y_{1:t-1})
=\sum_{z_{t-1}}p(z_t\mid z_{t-1})p(z_{t-1}\mid y_{1:t-1});
$$

2. 用当前观测做 Bayes 更新：

$$
p(z_t\mid y_{1:t})
\propto p(y_t\mid z_t)p(z_t\mid y_{1:t-1}).
$$

这就是“先按动力学搬运信念，再用证据重新加权”。HMM 的 forward algorithm、Kalman filter 和粒子滤波都在实现这条思想，只是分布表示不同。

## 7. 线性高斯状态空间模型与 Kalman filter

若初始状态是高斯，状态和观测是连续向量，且

$$
z_t=Az_{t-1}+\varepsilon_t,
\quad \varepsilon_t\sim\mathcal N(0,Q),
$$

$$
y_t=Cz_t+\eta_t,
\quad \eta_t\sim\mathcal N(0,R),
$$

并且 $\lbrace\varepsilon_t\rbrace$、 $\lbrace\eta_t\rbrace$ 分别是时间上独立的高斯白噪声，二者相互独立且与初始状态独立，则所有滤波分布都保持高斯，均值和协方差可用 Kalman filter 精确递推。若噪声跨时间相关或状态噪声与观测噪声相关，需要扩展状态或使用相应的广义递推，不能直接套最基本公式。

Kalman gain 决定“信模型预测还是信传感器”：观测噪声 $R$ 大时更信预测，预测不确定性大时更信观测。非线性或非高斯模型可能使用 extended/unscented Kalman filter、粒子滤波或神经状态空间模型。

## 8. 与 MDP、序列模型和生成模型的关系

### 8.1 MDP：转移还受动作控制

Markov decision process 加入动作和奖励：

$$
p(s_{t+1},r_t\mid s_t,a_t).
$$

Markov 链描述“系统自己怎样走”，MDP 描述“智能体的动作怎样影响系统并获得回报”。仓库内的 [T07](../../proofs/sequential-decision/T07-bellman.md) 从有限时域价值函数开始，推导 Bellman 递推与误差望远镜恒等式；所需概率前置也在本仓库中。可选的 [旧笔记扩展阅读](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0/%E5%9F%BA%E7%A1%80/MDP%E3%80%81Bellman%20%E6%96%B9%E7%A8%8B%E4%B8%8E%E6%97%B6%E5%BA%8F%E5%B7%AE%E5%88%86%E5%AD%A6%E4%B9%A0.md) 可能需要额外访问权限。

### 8.2 序列神经网络

RNN 的隐藏状态试图压缩历史；如果它真是预测未来的充分摘要，就体现了类似 Markov state 的思想。Transformer 直接访问上下文，不等于数据本身没有 Markov 结构，也不保证 attention 表示因果机制。

### 8.3 Diffusion

经典离散时间 diffusion 的前向加噪过程通常构造成 Markov 链；反向生成需要学习条件转移。连续时间表述则连接随机微分方程。见 [扩散模型、Score Matching 与 Flow Matching](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B/%E6%89%A9%E6%95%A3%E6%A8%A1%E5%9E%8B%E3%80%81Score%20Matching%20%E4%B8%8E%20Flow%20Matching.md)。

## 9. 可运行示例：状态比例与 HMM 滤波

```python
import numpy as np

rng = np.random.default_rng(21)

# 两状态链：0=稳定，1=告警。本文采用行随机矩阵。
P = np.array([[0.95, 0.05],
              [0.20, 0.80]])

# 平稳分布满足 pi = pi @ P；这里解析结果是 [0.8, 0.2]。
pi = np.array([0.8, 0.2])
assert np.allclose(pi @ P, pi)

states = np.empty(200_000, dtype=int)
states[0] = 0
for t in range(1, len(states)):
    states[t] = rng.choice(2, p=P[states[t - 1]])

empirical = np.bincount(states[1_000:], minlength=2) / (len(states) - 1_000)
print("stationary:", pi)
print("long-run empirical proportions:", empirical)
assert np.allclose(empirical, pi, atol=0.015)

# HMM: 观测 y=1 在稳定态概率 0.1，在告警态概率 0.8。
prob_y1 = np.array([0.1, 0.8])
observations = [0, 0, 1, 1, 1]
belief = np.array([1.0, 0.0])  # p(z_0)：从确定的稳定态开始，而非平稳初值

for t, y in enumerate(observations, start=1):
    predicted = belief @ P     # p(z_t | y_1, ..., y_{t-1})
    likelihood = prob_y1 if y == 1 else (1.0 - prob_y1)
    belief = predicted * likelihood  # 未归一化 p(z_t, y_t | 过去)
    belief /= belief.sum()       # Bayes 归一化
    print(f"t={t}, after y_t={y}: P(z_t=stable/alarm | y_1:t)={belief}")

assert belief[1] > 0.85
```

连续出现三个告警信号后，滤波器显著提高对告警状态的信念；转移矩阵仍会防止单个噪声观测让信念瞬间变成 0 或 1。

## 10. 常见误区

1. **“Markov 假设说过去不影响未来。”** 它说给定当前状态后，过去不再提供额外预测信息；状态定义决定假设是否合理。
2. **“有平稳分布就一定从任何起点收敛。”** 可约性和周期性都可能阻止收敛。
3. **“平稳就意味着独立同分布。”** 平稳过程仍可有强时间相关性。
4. **“detailed balance 是平稳的必要条件。”** 它是方便的充分条件；非可逆链也能平稳。
5. **“观测就是状态。”** 状态空间模型特意区分潜在状态与带噪观测。
6. **“滤波和平滑相同。”** 平滑使用未来数据，在线系统通常只能滤波。
7. **“转移矩阵乘法方向随便。”** 行/列约定混用会产生错误结果。
8. **“神经网络能拟合序列，所以不需要检查状态假设。”** 表达能力不能自动解决不可辨识、分布漂移或错误观测模型。

## 11. 自测

1. 为什么“当前温度”可能不足以构成天气预测的 Markov 状态？还应加入什么？
2. 写出行向量约定下的两步状态分布更新。
3. 一个链有平稳分布但严格在两个状态间交替，它为何不从单点起始分布收敛？
4. 预测、滤波和平滑分别允许使用哪些观测？
5. Kalman filter 为什么能只维护均值和协方差？
6. HMM 与 MDP 的核心区别是什么？

## 延伸阅读

- Norris, *Markov Chains*, Cambridge University Press, 1997.
- Murphy, *Probabilistic Machine Learning: Advanced Topics*, chapters on state-space models and sequential Monte Carlo.
- Rabiner, [A Tutorial on Hidden Markov Models](https://www.cs.ubc.ca/~murphyk/Bayes/rabiner.pdf), 1989.
- Särkkä, [Bayesian Filtering and Smoothing](https://users.aalto.fi/~ssarkka/pub/cup_book_online_20131111.pdf), Cambridge University Press, 2013.
- Sutton & Barto, [Reinforcement Learning: An Introduction](http://incompleteideas.net/book/the-book-2nd.html), 2nd ed.
