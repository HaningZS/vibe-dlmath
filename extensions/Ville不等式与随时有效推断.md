# Ville 不等式与随时有效推断

[返回专题目录](README.md) · [原证明模板](../proofs/README.md)

前置：[滤过与适应过程](<../Math 基础/概率统计/测度、条件期望、滤过与适应过程.md>)、[MGF 与鞅](<../Math 基础/概率统计/集中不等式、MGF、鞅与自归一化过程.md>)。

## 1. 一直看结果，为什么会改变问题

固定第 100 次实验才检验，与每来一个样本就检验、显著就停止，是不同的随机程序。后者会挑中偶然波动最有利的时刻。

直觉上，固定时刻的 5% 错误概率是一次查看的预算；不能把相同预算无偿用在无限次查看上。

随时有效推断希望直接保证

$$
\Pr(\text{任何时刻错误越界})\leq\delta.
$$

## 2. 把证据看作一个公平或吃亏的赌局

设 $M_t\geq0$ 适应滤过 $\mathcal F_t$，且

$$
\mathbb E[M_{t+1}\mid\mathcal F_t]\leq M_t,\qquad M_0=1.
$$

它是非负超鞅。你可以根据已观察信息调整下注，但在原假设下，条件期望财富不会凭空增长。

Ville 不等式说

$$
\Pr\left(\sup_{t\geq0}M_t\geq1/\delta\right)\leq\delta.
$$

这是一条同时控制所有时刻的最大值不等式。

## 3. 为什么成立：先证明有限时刻，再取极限

固定整数 $N$，令 $\tau$ 为首次达到 $1/\delta$ 的时刻，考虑 $\tau\wedge N$。它是有界 stopping time，因此

$$
\mathbb E[M_{\tau\wedge N}]\leq1.
$$

在事件 $\{\tau\leq N\}$ 上，$M_{\tau\wedge N}\geq1/\delta$；其余事件上财富非负。于是

$$
1\geq\mathbb E[M_{\tau\wedge N}]
\geq\frac1\delta\Pr(\tau\leq N).
$$

得到 $\Pr(\tau\leq N)\leq\delta$。最后对递增事件取 $N\to\infty$：

$$
\Pr(\tau<\infty)\leq\delta.
$$

这里没有直接对无界 stopping time 使用 optional stopping；先截断是关键。

## 4. 从条件 MGF 构造证据过程

设 $X_t$ 为 martingale difference，满足

$$
\mathbb E[e^{\lambda X_t}\mid\mathcal F_{t-1}]
\leq e^{\lambda^2\sigma_t^2/2}
$$

其中 $\sigma_t^2$ 是 predictable 方差代理。定义

$$
S_t=\sum_{i=1}^tX_i,\qquad
V_t=\sum_{i=1}^t\sigma_i^2,\qquad
M_t(\lambda)=e^{\lambda S_t-\lambda^2V_t/2}.
$$

把下一步的指数拆出并取条件期望，就能验证 $M_t(\lambda)$ 是非负超鞅。

因此对固定 $\lambda>0$，概率至少 $1-\delta$ 时，对全部 $t$ 同时有

$$
S_t<\frac{\log(1/\delta)}{\lambda}+\frac{\lambda V_t}{2}.
$$

## 5. 为什么不能每一步事后选最好的 λ

上面保证的是**预先固定**的 $\lambda$。观察完 $S_t,V_t$ 后任意选择 $\lambda_t$，不能直接沿用原来的 Ville 结论。

常见正确做法是预先选一个关于 $\lambda$ 的概率分布 $\pi$，做 mixture：

$$
\widetilde M_t=\int M_t(\lambda)\,\pi(d\lambda).
$$

非负性允许用 Tonelli 交换积分与条件期望，$\widetilde M_t$ 仍是超鞅。另一条路线是对分段时刻/参数分配失败概率，称为 stitching。

两者都会为“看了许多种尺度”付出相应代价。

## 6. 数值例子：边界不是一条任意画出的曲线

~~~python
import math
import random

rng = random.Random(7)
delta, lam = 0.05, 0.2
s = 0.0
max_wealth = 1.0
for t in range(1, 101):
    s += rng.gauss(0.0, 1.0)
    wealth = math.exp(lam * s - lam**2 * t / 2)
    boundary = math.log(1 / delta) / lam + lam * t / 2
    assert (wealth >= 1 / delta) == (s >= boundary)
    max_wealth = max(max_wealth, wealth)
print("这一次路径的最大财富:", round(max_wealth, 4))
~~~

代码验证指数越界与线性边界越界等价；单次模拟不会证明 $\delta$ 的概率控制。

## 7. 怎样连到 AI 实验

在线监控、持续评估、adaptive sampling 都可能需要同时控制多个时刻。但模型输出如果改变了数据生成机制，必须重新检查 conditional MGF、filtration 与 predictable 条件。

置信序列可以通过对每个候选参数构造检验并反演得到。多个任务或指标同时检测还要考虑多重比较；“time-uniform”并不自动包办所有比较维度。

自测：为什么非负性不能随意删去？因为有限截断证明用它保证未越界事件的财富不会抵消越界事件的正贡献。

## 论文

- Howard et al.：[Time-uniform Chernoff bounds](https://arxiv.org/abs/1808.03204)；
- Howard et al.：[Confidence sequences](https://arxiv.org/abs/1810.08240)。

本地阅读卡见 [concentration 论文目录](../PAPERS.md#concentration)。
