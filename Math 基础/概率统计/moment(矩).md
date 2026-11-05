---
status: canonical
reviewed: 2026-08-24
---

# 概率分布的矩

矩用幂函数的期望概括分布的位置、尺度和形状。讨论“第几阶矩”时，必须说明是原点矩、中心矩还是标准化矩。

## 原点矩

若期望存在，随机变量 $X$ 的 $k$ 阶原点矩为

$$
\mu'_k=\mathbb E[X^k].
$$

离散情形：

$$
\mathbb E[X^k]=\sum_x x^k P(X=x).
$$

连续情形：

$$
\mathbb E[X^k]=\int x^kf(x)\thinspace dx.
$$

- 零阶矩通常为 1；
- 一阶原点矩是均值 $\mathbb E[X]$；
- 二阶原点矩是 $\mathbb E[X^2]$，它**不是方差**。

## 中心矩

令 $\mu=\mathbb E[X]$。 $k$ 阶中心矩为

$$
\mu_k=\mathbb E[(X-\mu)^k].
$$

- 一阶中心矩为 0；
- 二阶中心矩是方差： $\mu_2=\mathop{\mathrm{Var}}(X)$；
- 三、四阶中心矩分别参与偏度和峰度的定义。

原点二阶矩与方差的关系是

$$
\mathop{\mathrm{Var}}(X)=\mathbb E[X^2]-\mathbb E[X]^2.
$$

## 标准化矩

令标准差为 $\sigma>0$：

$$
\mathbb E\negthinspace\left[\left(\frac{X-\mu}{\sigma}\right)^k\right].
$$

- 三阶标准化矩是偏度；正值通常表示右尾更长，负值表示左尾更长。
- 四阶标准化矩常称峰度。不同资料可能报告峰度或超额峰度（减 3），必须说明约定。

峰度更可靠的直觉是“对尾部和极端值的敏感程度”，不宜只解释成峰顶有多尖。

## 物理类比的边界

概率矩与质量分布矩有直接形式类比，例如均值类似质心，方差类似关于质心的二阶质量矩。

但“矩”不是统一的标量乘法口诀：力矩在三维中是

$$
\boldsymbol\tau=\mathbf r\times\mathbf F,
$$

其大小才可写为 $rF\sin\theta$。物理力矩、转动惯量和概率矩有相关数学形式，但不应混成同一个定义。

## Adam 中的 moment estimates

Adam 对每个参数维护

$$
m_t=\beta_1m_{t-1}+(1-\beta_1)g_t,
$$

$$
v_t=\beta_2v_{t-1}+(1-\beta_2)g_t^2,
$$

其中平方是逐元素的。

- $m_t$ 是梯度一阶原点矩的指数移动估计；
- $v_t$ 是梯度二阶原点矩 $\mathbb E[g^2]$ 的指数移动估计；
- $v_t$ **不是梯度方差**，因为没有减去均值平方；
- $v_t$ 也不是 Hessian 或 Hessian 对角线的一般估计。

初始化为零会产生偏差，因此 Adam 使用

$$
\hat m_t=\frac{m_t}{1-\beta_1^t},
\qquad
\hat v_t=\frac{v_t}{1-\beta_2^t}.
$$

更新中的分母 $\sqrt{\hat v_t}+\epsilon$ 根据近期梯度平方尺度做坐标级归一化。若梯度“变化剧烈”且幅度很大， $v_t$ 仍会很大；不能把它简单解释为“稳定性”或“方差”。

## 来源

- [Adam: A Method for Stochastic Optimization](https://arxiv.org/abs/1412.6980)
- [NIST: Measures of Skewness and Kurtosis](https://www.itl.nist.gov/div898/handbook/eda/section3/eda35b.htm)
