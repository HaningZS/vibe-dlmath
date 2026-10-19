---
type: note
domain: math/optimization
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# Bregman 散度、Mirror Descent 与在线学习

先抓住一句话：

> 普通梯度下降默认参数空间是一张铺着方格纸的平面；Mirror Descent 先选择一面适合可行域的“弯镜子”，在镜像坐标里走梯度步，再映回原空间。

概率单纯形、PSD 矩阵、稀疏向量和不同坐标尺度有不同几何。欧氏平方距离不是唯一合理的“走一步有多远”。Bregman divergence 用一个凸势函数定义局部几何，Mirror Descent 则把这个几何放进优化与在线 regret 证明。

## 知识依赖与导航

- 路线：[AI 理论证明前置学习路线](../%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/AI%20%E7%90%86%E8%AE%BA%E8%AF%81%E6%98%8E%E5%89%8D%E7%BD%AE%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)、[Math 基础目录](../Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md)。
- 凸优化：[凸集、凸函数与优化直觉](%E5%87%B8%E9%9B%86%E3%80%81%E5%87%B8%E5%87%BD%E6%95%B0%E4%B8%8E%E4%BC%98%E5%8C%96%E7%9B%B4%E8%A7%89.md)、[拉格朗日乘子、对偶与约束优化](%E6%8B%89%E6%A0%BC%E6%9C%97%E6%97%A5%E4%B9%98%E5%AD%90%E3%80%81%E5%AF%B9%E5%81%B6%E4%B8%8E%E7%BA%A6%E6%9D%9F%E4%BC%98%E5%8C%96.md)。
- 对偶范数与表示几何：[范数、距离、相似度与度量学习](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E8%8C%83%E6%95%B0%E3%80%81%E8%B7%9D%E7%A6%BB%E3%80%81%E7%9B%B8%E4%BC%BC%E5%BA%A6%E4%B8%8E%E5%BA%A6%E9%87%8F%E5%AD%A6%E4%B9%A0.md)。
- KL：[信息论基础：熵、交叉熵与 KL 散度](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E4%BF%A1%E6%81%AF%E8%AE%BA%E5%9F%BA%E7%A1%80%EF%BC%9A%E7%86%B5%E3%80%81%E4%BA%A4%E5%8F%89%E7%86%B5%E4%B8%8E%20KL%20%E6%95%A3%E5%BA%A6.md)。
- 模板：[T08](../../proofs/sequential-decision/T08-mirror-descent.md)、[P06](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p06-convex%E6%80%A7bregman-%E5%87%A0%E4%BD%95%E4%B8%8E%E5%AF%B9%E5%81%B6)、[R01](../../%E8%BF%91%E6%9C%9F%E9%A1%B6%E4%BC%9A%E7%90%86%E8%AE%BA%E6%A1%86%E6%9E%B6%EF%BC%882025-2026%EF%BC%89.md#r01-%E7%BB%93%E6%9E%84%E6%80%A7%E8%B4%A8--%E5%8F%98%E5%BA%A6%E9%87%8F%E5%8A%BF%E5%87%BD%E6%95%B0--%E7%AE%97%E6%B3%95%E7%89%B9%E5%8C%96)。
- PDF 映射：[数学前置与论文证明导航](../../%E6%95%B0%E5%AD%A6%E5%89%8D%E7%BD%AE%E4%B8%8E%E8%AE%BA%E6%96%87%E8%AF%81%E6%98%8E%E5%AF%BC%E8%88%AA.md#c-bregman%E5%9C%A8%E7%BA%BF%E4%BC%98%E5%8C%96%E4%B8%8E-kl-%E5%87%A0%E4%BD%95)。

## 1. 为什么欧氏梯度不是唯一几何

普通一步

$$
x_{t+1}=x_t-\eta g_t
$$

等价于解局部问题

$$
x_{t+1}
=\arg\min_x
\left\{
\eta\langle g_t,x\rangle
+\frac12\|x-x_t\|_2^2
\right\}.
$$

第一项希望沿梯度下降，第二项阻止一步走太远。这里“太远”使用欧氏平方距离。

如果 $x$ 是概率向量，直接欧氏一步可能产生负数，还要投影回单纯形；若某坐标接近 0，欧氏距离也未必反映概率比的变化。Mirror Descent 的想法是替换第二项的几何。

## 2. Convex conjugate 与 Fenchel–Young

对凸函数 $\psi$，凸共轭定义为

$$
\psi^*(y)
=\sup_x\{\langle y,x\rangle-\psi(x)\}.
$$

它把 primal 变量 $x$ 转到 dual 变量 $y$。由定义立即得到 Fenchel–Young：

$$
\langle x,y\rangle
\le\psi(x)+\psi^*(y).
$$

当 $y\in\partial\psi(x)$ 时取等号。Young 不等式和很多“拆交叉项”技巧都可以看成这条不等式的具体选择。

若 $\psi$ 满足适当的 Legendre-type 条件，并限制在梯度映射的像内，梯度映射

$$
y=\nabla\psi(x)
$$

把 primal 点送到 mirror/dual 坐标，逆映射可写为 $x=\nabla\psi^*(y)$。仅有“可微且严格凸”一般不足以保证它在整个空间上是全局双射。

## 3. Bregman divergence：切平面与函数之间的缺口

对可微凸函数 $\psi$：

$$
D_\psi(x,y)
=\psi(x)-\psi(y)-\langle\nabla\psi(y),x-y\rangle.
$$

凸函数图像在切平面上方，所以 $D_\psi(x,y)\ge0$。

直觉：从 $y$ 的一阶局部模型预测 $\psi(x)$，实际值多出来多少。

一般而言：

- $D_\psi(x,y)\ne D_\psi(y,x)$；
- 不满足三角不等式；
- 所以叫 divergence，不是 metric。

若 $\psi$ 关于范数 $\|\cdot\|$ 为 $\sigma$-strongly convex：

$$
D_\psi(x,y)
\ge\frac\sigma2\|x-y\|^2.
$$

这条下界让 Bregman potential 能控制真实参数距离。

## 4. 两个核心例子

### 4.1 欧氏势函数

$$
\psi(x)=\frac12\|x\|_2^2
$$

给出

$$
D_\psi(x,y)=\frac12\|x-y\|_2^2.
$$

因此普通 projected gradient descent 是 Mirror Descent 的欧氏特例。

### 4.2 单纯形上的负熵

在开放概率单纯形 $x_i>0,\sum_i x_i=1$ 上取

$$
\psi(x)=\sum_i x_i\log x_i.
$$

则

$$
D_\psi(x,y)
=\sum_i x_i\log\frac{x_i}{y_i}
=D_{\mathrm{KL}}(x\|y).
$$

方向、定义域和共同支撑不能省略。若 $x_i>0$ 而 $y_i=0$，KL 为无穷；这不是数值小问题，而是几何边界。

## 5. 三点恒等式

展开定义可得

$$
\langle\nabla\psi(x)-\nabla\psi(y),z-x\rangle
=D_\psi(z,y)-D_\psi(z,x)-D_\psi(x,y).
$$

它是 Mirror Descent 证明中的“望远镜接口”：右边包含前后两时刻相对比较点 $z$ 的 potential 差。

参数顺序决定符号。不能只记“三个 Bregman 会抵消”，应每次从定义检查 orientation。

## 6. Mirror Descent 更新

给定凸可行域 $\mathcal X$，一步 Mirror Descent：

$$
x_{t+1}
=\arg\min_{x\in\mathcal X}
\left\{
\eta_t\langle g_t,x\rangle
+D_\psi(x,x_t)
\right\}.
$$

它把线性化损失和“不要离 $x_t$ 太远”放在一起，只是距离换成 Bregman divergence。

无约束内部解的一阶条件给

$$
\nabla\psi(x_{t+1})
=\nabla\psi(x_t)-\eta_t g_t.
$$

这说明算法真正在 dual/mirror 坐标里做加法步，再通过 $\nabla\psi^*$ 回到 primal 空间。

## 7. 一步 regret 不等式

最优性条件与三点恒等式可推出，对任意比较点 $u\in\mathcal X$：

$$
\eta_t\langle g_t,x_{t+1}-u\rangle
\le
D_\psi(u,x_t)-D_\psi(u,x_{t+1})
-D_\psi(x_{t+1},x_t).
$$

若要控制 $\langle g_t,x_t-u\rangle$，再拆成

$$
\langle g_t,x_t-u\rangle
=\langle g_t,x_t-x_{t+1}\rangle
+\langle g_t,x_{t+1}-u\rangle.
$$

用对偶范数 Hölder：

$$
\langle g_t,x_t-x_{t+1}\rangle
\le\|g_t\|_*\|x_t-x_{t+1}\|,
$$

再由 Young 和 strong convexity 吸收到 $D_\psi(x_{t+1},x_t)$，得到典型界：

$$
\eta_t\langle g_t,x_t-u\rangle
\le
D_\psi(u,x_t)-D_\psi(u,x_{t+1})
+\frac{\eta_t^2}{2\sigma}\|g_t\|_*^2.
$$

固定步长求和时 Bregman 项 telescope；这就是 regret proof 的核心骨架。

### 7.1 从一步不等式到 static regret

在线学习在每轮 $t$ 先选择 $x_t\in\mathcal X$，再观察凸损失 $\ell_t$ 并支付 $\ell_t(x_t)$。相对固定比较点 $u$ 的 static regret 为

$$
\operatorname{Reg}_T(u)
=\sum_{t=1}^T\big(\ell_t(x_t)-\ell_t(u)\big).
$$

由凸性，取 $g_t\in\partial\ell_t(x_t)$：

$$
\ell_t(x_t)-\ell_t(u)
\le\langle g_t,x_t-u\rangle.
$$

若步长固定为 $\eta$，把上一节的一步界求和，并假设 $\psi$ 关于所选范数为 $\sigma$-strongly convex，可得

$$
\operatorname{Reg}_T(u)
\le
\frac{D_\psi(u,x_1)}{\eta}
+\frac{\eta}{2\sigma}\sum_{t=1}^T\|g_t\|_*^2.
$$

若 $D_\psi(u,x_1)\le D^2$ 且 $\|g_t\|_*\le G$，选择 $\eta$ 为 $1/\sqrt T$ 量级即可得到 $O(\sqrt T)$ static regret。这个结论依赖 convex loss、固定 comparator、Bregman 直径与 dual-gradient bound；不能直接搬到任意非凸训练 loss。

## 8. Negative entropy 导出 multiplicative weights

在单纯形上使用负熵，mirror 坐标为

$$
(\nabla\psi(x))_i=1+\log x_i.
$$

dual 步给

$$
\log x_{t+1,i}
=\log x_{t,i}-\eta g_{t,i}+\text{normalizer},
$$

所以

$$
x_{t+1,i}
\propto x_{t,i}e^{-\eta g_{t,i}}.
$$

这是 exponentiated gradient / multiplicative weights。它自动保持非负和归一化，比“欧氏一步再裁负数”更符合概率几何。

## 9. FTRL、prox 与 Mirror Descent 的关系

Follow-the-Regularized-Leader（FTRL）常写成

$$
x_{t+1}
=\arg\min_{x\in\mathcal X}
\left\{
\sum_{s=1}^t\langle g_s,x\rangle
+\frac1\eta\psi(x)
\right\}.
$$

Mirror Descent 使用局部 Bregman proximal step，FTRL 使用累计线性损失加 regularizer。在线性损失、特定 regularizer 和更新约定下二者可以等价或紧密对应，但变步长、约束、复合损失和近似解会改变关系。

不要把“都出现 KL/entropy”当成算法完全相同的证明。

## 10. KL policy update 与 RLHF

策略优化常用

$$
\pi_{t+1}
=\arg\max_\pi
\left\{
\langle r_t,\pi\rangle
-\frac1\eta D_{\mathrm{KL}}(\pi\|\pi_t)
\right\}.
$$

这在有限动作单纯形上给指数加权更新。但 RLHF 中还可能使用相对固定 reference policy 的 KL，它属于目标正则，不一定等于相邻迭代之间的 trust region。

[Fisher 信息、自然梯度与信息几何](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/Fisher%20%E4%BF%A1%E6%81%AF%E3%80%81%E8%87%AA%E7%84%B6%E6%A2%AF%E5%BA%A6%E4%B8%8E%E4%BF%A1%E6%81%AF%E5%87%A0%E4%BD%95.md) 的局部 KL 二次几何与这里的全局 Bregman/KL proximal geometry 相关，但不是同一个更新公式。

## 11. 变步长与近似更新

若 $\eta_t$ 变化，直接求和可能出现

$$
\frac{D_\psi(u,x_t)}{\eta_t}
-\frac{D_\psi(u,x_{t+1})}{\eta_t},
$$

与下一时刻 $1/\eta_{t+1}$ 不匹配，从而产生额外 correction。

若 proximal subproblem 只近似求解，还要把 optimality residual 加入 regret recursion。近似误差是否可求和、是否依赖 barrier 边界，决定最终 rate；这正是 [variable-metric](../../%E8%BF%91%E6%9C%9F%E9%A1%B6%E4%BC%9A%E7%90%86%E8%AE%BA%E6%A1%86%E6%9E%B6%EF%BC%882025-2026%EF%BC%89.md#r01-%E7%BB%93%E6%9E%84%E6%80%A7%E8%B4%A8--%E5%8F%98%E5%BA%A6%E9%87%8F%E5%8A%BF%E5%87%BD%E6%95%B0--%E7%AE%97%E6%B3%95%E7%89%B9%E5%8C%96) 与 Hidden Cost of OMD 类论文关注的问题。

## 12. 可运行示例：欧氏投影与 entropy mirror step

```python
import numpy as np

p = np.array([0.70, 0.20, 0.10])
loss = np.array([1.0, 0.0, 0.5])
eta = 0.8

# Negative-entropy mirror descent / multiplicative weights。
weights = p * np.exp(-eta * loss)
p_mirror = weights / weights.sum()

# 一个朴素欧氏步随后投影到 simplex；这里实现标准排序投影。
def project_simplex(v):
    u = np.sort(v)[::-1]
    cssv = np.cumsum(u)
    rho = np.nonzero(u * np.arange(1, len(v) + 1) > (cssv - 1.0))[0][-1]
    theta = (cssv[rho] - 1.0) / (rho + 1.0)
    return np.maximum(v - theta, 0.0)

p_euclidean = project_simplex(p - eta * loss)

print("start:", p)
print("entropy mirror:", p_mirror)
print("euclidean projection:", p_euclidean)

assert np.all(p_mirror > 0.0)
assert np.allclose(p_mirror.sum(), 1.0)
assert np.all(p_euclidean >= 0.0)
assert np.allclose(p_euclidean.sum(), 1.0)
assert not np.allclose(p_mirror, p_euclidean)
```

两种方法都合法，但选择了不同几何；“哪种更好”取决于可行域、梯度范数和任务，而不是 Mirror Descent 永远优于欧氏方法。

## 常见误区

1. **“Bregman divergence 是距离。”** 它通常不对称且不满足三角不等式。
2. **“负熵 Bregman 总等于有限 KL。”** 需要正确方向、正坐标和共同支撑。
3. **“Mirror Descent 就是自然梯度。”** 一个用全局 Bregman proximal step，一个使用局部 Fisher metric。
4. **“FTRL 与 OMD 永远相同。”** 等价需要具体损失、regularizer、步长和约束条件。
5. **“三点恒等式参数可以随便换。”** orientation 变化会改变符号。
6. **“变步长仍会自动望远镜。”** $1/\eta_t$ 的变化产生额外项。
7. **“近似解 proximal subproblem 不影响理论。”** optimality residual 会进入 regret。

## 自测

1. 从凸性解释 $D_\psi(x,y)\ge0$。
2. 推导欧氏势函数对应平方距离。
3. 推导负熵在单纯形上对应哪个方向的 KL。
4. 用三点恒等式推出一步 Mirror Descent inequality。
5. primal norm 与 dual norm 为什么必须一起出现？
6. RLHF 的 reference KL 与 online trust-region KL 有什么区别？

## PDF 入口

- DPO 的 KL-regularized policy optimum 推导：[PDF：DPO appendix derivation, p.15](../../proof_ref/core-theory-2026-09/direct-preference-optimization-your-language-model-is-secretly-2305.18290/paper.pdf#page=15)；问题设置可先看 p.3。
- 近似 OMD 的额外代价：[PDF：OMD/barrier preliminaries, p.4](../../proof_ref/core-theory-2026-09/the-hidden-cost-of-approximation-in-online-mirror-2511.22283/paper.pdf#page=4)。
- 变度量 adaptive optimization：[PDF：Structured preconditioners, p.5](../../proof_ref/recent-accepted-2025-2026/structured-preconditioners-in-adaptive-optimization-a-unified-analysis-2503.10537/paper.pdf#page=5)。
- 返回映射：[数学前置与论文证明导航](../../%E6%95%B0%E5%AD%A6%E5%89%8D%E7%BD%AE%E4%B8%8E%E8%AE%BA%E6%96%87%E8%AF%81%E6%98%8E%E5%AF%BC%E8%88%AA.md#c-bregman%E5%9C%A8%E7%BA%BF%E4%BC%98%E5%8C%96%E4%B8%8E-kl-%E5%87%A0%E4%BD%95)。

## 延伸阅读

- Bubeck, [*Convex Optimization: Algorithms and Complexity*](https://arxiv.org/abs/1405.4980)。
- Beck & Teboulle, *Mirror Descent and Nonlinear Projected Subgradient Methods*, 2003。
- Shalev-Shwartz, *Online Learning and Online Convex Optimization*, 2012。
- Orabona, [*A Modern Introduction to Online Learning*](https://arxiv.org/abs/1912.13213)。
