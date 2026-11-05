# PL 条件与 SGD 的噪声地板

[返回专题目录](README.md) · [原证明模板](../proofs/README.md)

前置：[梯度下降](<../Math 基础/微积分与分析/梯度下降、学习率与收敛.md>)、[凸性](<../Math 基础/微积分与分析/凸集、凸函数与优化直觉.md>)、[条件期望](<../Math 基础/概率统计/测度、条件期望、滤过与适应过程.md>)。

## 1. 梯度小，到底代表什么

想象你在山坡上走向低处。脚下很平可能意味着接近谷底，也可能是一个高处的平台。因此“梯度很小”和“目标值接近最优”通常是两个结论。

Polyak–Łojasiewicz（PL）条件直接排除了“离最优还很远但已经很平”：

$$
\frac12\Vert\nabla f(x)\Vert^2\geq \mu(f(x)-f^\star),\qquad \mu>0.
$$

左边是当前能感受到的坡度，右边是离最低目标值的差距。它规定：如果差距大，坡度就不能太小。

这是关于整个适用区域的假设。不能从一条训练曲线下降很快就反过来宣布神经网络满足全局 PL。

## 2. PL 与强凸的关系

对可微的强凸函数，强凸下界可写为

$$
f(y)\geq f(x)+\langle\nabla f(x),y-x\rangle
+\frac\mu2\Vert y-x\Vert^2.
$$

右边关于 $y$ 的最小值在 $y=x-\nabla f(x)/\mu$，从而

$$
f^\star\geq f(x)-\frac{\Vert\nabla f(x)\Vert^2}{2\mu}.
$$

这就是 PL。但反方向不成立： $f(x_1,x_2)=x_1^2$ 满足 PL，却沿 $x_2$ 方向完全平坦，所以不是强凸，也没有唯一最优参数。

这个例子说明 PL 主要控制**函数值差距**，并不自动保证参数收敛到某一个指定点。

## 3. 把一步下降接到 PL

设 $f$ 是 $L$-smooth， $f^\star$ 有限，并在迭代经过的区域满足 PL。梯度下降为

$$
x_{t+1}=x_t-\eta\nabla f(x_t),\qquad 0<\eta\leq 1/L.
$$

由 smoothness，

$$
f(x_{t+1})
\leq f(x_t)-\eta\Vert\nabla f(x_t)\Vert^2
+\frac{L\eta^2}{2}\Vert\nabla f(x_t)\Vert^2
\leq f(x_t)-\frac\eta2\Vert\nabla f(x_t)\Vert^2.
$$

记 $\Delta_t=f(x_t)-f^\star$，代入 PL 得

$$
\Delta_{t+1}\leq(1-\eta\mu)\Delta_t.
$$

于是 $\Delta_t\leq(1-\eta\mu)^t\Delta_0$。这就是线性收敛，也叫几何收敛：每步缩掉相同比例，而非每步减少相同数值。

若 PL 只在局部区域成立，还必须证明迭代留在该区域。它不能被当作免费的全局假设。

## 4. SGD 多出了哪笔账

令 $\mathcal F_t$ 表示采样当前梯度前的全部信息， $x_t$ 对它可测。假设

$$
\mathbb E[g_t\mid\mathcal F_t]=\nabla f(x_t),\qquad
\mathbb E[\Vert g_t-\nabla f(x_t)\Vert^2\mid\mathcal F_t]\leq\sigma^2.
$$

用同样的 smoothness 展开，再取条件期望：

$$
\mathbb E[f(x_{t+1})\mid\mathcal F_t]
\leq f(x_t)-\eta\Vert\nabla f(x_t)\Vert^2
+\frac{L\eta^2}{2}\mathbb E[\Vert g_t\Vert^2\mid\mathcal F_t].
$$

无偏性使交叉项为零，因此

$$
\mathbb E[\Vert g_t\Vert^2\mid\mathcal F_t]\leq
\Vert\nabla f(x_t)\Vert^2+\sigma^2.
$$

在相同步长条件下得到

$$
\mathbb E[\Delta_{t+1}\mid\mathcal F_t]
\leq(1-\eta\mu)\Delta_t+\frac{L\eta^2\sigma^2}{2}.
$$

每步都缩小旧误差，但同时又注入新噪声。像一边抽水、一边有小水管进水，恒定学习率最终只能控制到一个平衡水位。

## 5. 完整展开递推

设 $q=1-\eta\mu\in[0,1)$、 $b=L\eta^2\sigma^2/2$。全期望与几何级数给出

$$
\mathbb E\Delta_T
\leq q^T\Delta_0+b\sum_{k=0}^{T-1}q^k
=q^T\Delta_0+\frac{L\eta\sigma^2}{2\mu}(1-q^T).
$$

因此极限上界是 $L\eta\sigma^2/(2\mu)$。减小学习率会降低这个残差，但也让 $q$ 更接近 1、早期下降变慢。

这不是说误差必然等于这个值，而是此组假设与推导给出的上界。

## 6. 数值检查

~~~python
import math

L, mu, eta, variance = 4.0, 1.0, 0.1, 0.2
q, b = 1 - eta * mu, L * eta**2 * variance / 2
delta0, bound = 3.0, 3.0
for t in range(1, 51):
    bound = q * bound + b
    closed = q**t * delta0 + b * (1 - q**t) / (1 - q)
    assert math.isclose(bound, closed, rel_tol=1e-12)
print("50 步后的递推上界:", round(bound, 6))
print("噪声地板上界:", round(b / (1 - q), 6))
~~~

这个例子只检查递推公式，不验证任何实际数据满足无偏、有界条件方差或 PL。

## 7. 常见误用与自测

- 梯度估计有 bias 时，原来的交叉项不会消失，需要另记一笔误差。
- Heavy-tailed 梯度若连二阶矩都不存在， $\sigma^2$ 假设失效，不能照搬。
- 加权/小批量采样的无偏性必须相对于实际目标成立。
- 期望界不自动给出对全部时刻同时成立的高概率界。

自测：为什么常数步长的无偏 SGD 也未必收敛到零误差？答案是每步二阶噪声项都被重新注入；无偏只消除一阶交叉项。

## 论文

Karimi、Nutini、Schmidt：[Linear Convergence … Under the PL Condition](https://arxiv.org/abs/1608.04636)。本文给出 smooth GD/SGD 的教学推导，原论文还有 proximal 等扩展。

本地阅读卡从 [optimization 论文目录](../PAPERS.md#optimization) 进入。
