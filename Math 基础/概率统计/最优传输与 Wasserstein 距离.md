---
type: note
domain: math/optimal-transport
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# 最优传输与 Wasserstein 距离

近期证明蒸馏：[T51 同起点 coupling 到 Wasserstein 界](../../proofs/generation-transport/T51-flow-trajectory-error.md)，完整展示为什么一次合法耦合可以给分布距离上界。

把两个概率分布想成两堆等质量的沙土。KL 散度比较“同一位置上的密度比例”，而最优传输（optimal transport, OT）问：**把第一堆土搬成第二堆，最省的运输方案是什么？** Wasserstein 距离就是最小运输成本的一个家族。

这个类比很有力量，因为它把样本空间的几何距离纳入比较：把一张图片平移一个像素，和换成完全不同的图片，运输成本可以不同。但严格意义上的“土”“位置”和“距离”都必须由概率测度、coupling 与 ground metric 定义，不能只凭视觉直觉。

## 知识依赖与相关笔记

- 总入口：[Math 基础目录](../Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md)、[AI Researcher 数学学习路线](../AI%20Researcher%20%E6%95%B0%E5%AD%A6%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)、[AI Researcher 高阶数学路线：LLM、CV 与生成模型](../AI%20Researcher%20%E9%AB%98%E9%98%B6%E6%95%B0%E5%AD%A6%E8%B7%AF%E7%BA%BF%EF%BC%9ALLM%E3%80%81CV%20%E4%B8%8E%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B.md)。
- 概率分布与联合分布：[概率论主干：联合、条件、期望与协方差](%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md)。
- KL 与信息论：[信息论基础：熵、交叉熵与 KL 散度](%E4%BF%A1%E6%81%AF%E8%AE%BA%E5%9F%BA%E7%A1%80%EF%BC%9A%E7%86%B5%E3%80%81%E4%BA%A4%E5%8F%89%E7%86%B5%E4%B8%8E%20KL%20%E6%95%A3%E5%BA%A6.md)。
- 连续流与 continuity equation：[ODE、SDE 与连续时间生成模型](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/ODE%E3%80%81SDE%20%E4%B8%8E%E8%BF%9E%E7%BB%AD%E6%97%B6%E9%97%B4%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B.md)。
- Lipschitz critic：[Lipschitz constant](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/Lipschitz%20constant.md)。
- 生成模型：[扩散模型、Score Matching 与 Flow Matching](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B/%E6%89%A9%E6%95%A3%E6%A8%A1%E5%9E%8B%E3%80%81Score%20Matching%20%E4%B8%8E%20Flow%20Matching.md)、[Flow Matching](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B/Flow%20Matching.md)。
- 线性代数与高斯协方差：[二次型、正定矩阵与谱](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E4%BA%8C%E6%AC%A1%E5%9E%8B%E3%80%81%E6%AD%A3%E5%AE%9A%E7%9F%A9%E9%98%B5%E4%B8%8E%E8%B0%B1.md)。

## 1. Coupling：决定每一份质量从哪搬到哪

给定分布 $\mu$ 和 $\nu$，coupling $\gamma(x,y)$ 是一个联合分布，其两个边缘分别为 $\mu$、 $\nu$：

$$
\gamma\in\Pi(\mu,\nu).
$$

$\gamma(x,y)$ 表示从位置 $x$ 搬到位置 $y$ 的质量。边缘约束保证每个出发点的土都被搬走、每个目标点都得到规定质量。

离散情形中，若 $a_i,b_j$ 是两边质量，coupling 是非负矩阵 $\Gamma$：

$$
\sum_j\Gamma_{ij}=a_i,
\qquad
\sum_i\Gamma_{ij}=b_j.
$$

同一对边缘分布有许多 coupling。独立 coupling $\mu\otimes\nu$ 通常不是最省运输的；OT 要在所有合法 coupling 中优化。

## 2. Kantorovich 最优传输问题

给定从 $x$ 搬到 $y$ 的成本 $c(x,y)$：

$$
\operatorname{OT}_c(\mu,\nu)
=\inf_{\gamma\in\Pi(\mu,\nu)}
\int c(x,y)\,d\gamma(x,y).
$$

这是 Kantorovich 的“可以拆分质量”版本。更早的 Monge 问题寻找确定映射 $T$，使 $T_\#\mu=\nu$ 并最小化

$$
\int c(x,T(x))\,d\mu(x).
$$

Monge map 不一定存在：一个原子不能通过确定映射拆成两个目标原子；Kantorovich coupling 可以拆分，因此可行性和凸性更好。合适条件下最优 coupling 可能由一个 map 诱导，但不能默认如此。

## 3. $p$-Wasserstein 距离

在度量空间上取 ground distance $d(x,y)$。若 $\mu,\nu$ 都有有限 $p$ 阶矩， $p\ge1$，定义

$$
W_p(\mu,\nu)
=\left(
\inf_{\gamma\in\Pi(\mu,\nu)}
\mathbb E_{(X,Y)\sim\gamma}[d(X,Y)^p]
\right)^{1/p}.
$$

- $W_1$ 最小化平均搬运距离；
- $W_2^2$ 最小化平方欧氏运输能量；
- ground metric 决定“什么算近”。像素欧氏距离、特征空间距离和语义距离会产生完全不同的 Wasserstein 几何。

在这些条件下 $W_p$ 是概率测度空间上的真正距离：非负、对称、相同分布时为零，并满足三角不等式。KL 散度不满足后两项中的对称和三角不等式，因此不是度量。

## 4. 一维特例：按分位数对齐就是最优

一维实线上，凸成本 $|x-y|^p$ 下，最优方案按从小到大配对：

$$
W_p(\mu,\nu)^p
=\int_0^1
|F_\mu^{-1}(u)-F_\nu^{-1}(u)|^p\,du.
$$

直觉是不能“交叉运输”：若 $x_1<x_2$ 却把 $x_1$ 搬到更右的目标、 $x_2$ 搬到更左的目标，交换目的地通常不会增加凸距离成本。

这条公式让一维经验 Wasserstein 非常容易计算：等权、等样本数时，分别排序后逐项比较即可。高维没有这么简单的统一排序。

## 5. Kantorovich–Rubinstein 对偶与 WGAN

对合适的度量空间， $W_1$ 有对偶形式

$$
W_1(\mu,\nu)
=\sup_{\|f\|_{\mathrm{Lip}}\le1}
\left(
\mathbb E_{X\sim\mu}[f(X)]
-\mathbb E_{Y\sim\nu}[f(Y)]
\right).
$$

这把“优化 coupling”变成“寻找所有 1-Lipschitz 函数中最能区分两分布的 critic”。WGAN 用神经网络近似这个 critic，从而给 generator 提供梯度。

### 5.1 严格结论与工程实现之间的距离

只有对**所有** 1-Lipschitz 函数取到 supremum，目标才等于精确 $W_1$。有限 critic 网络、有限优化步、有限样本和近似 Lipschitz 约束下，训练目标只是对该对偶问题的近似。

- 原始 weight clipping 粗糙地限制参数，不等价于精确函数 Lipschitz 约束；
- WGAN-GP 在选定插值点附近惩罚梯度范数偏离 1，是实用正则，但也不严格强制全空间 1-Lipschitz；
- spectral normalization 给各层算子范数上界，也可能保守或受结构影响。

因此不要把日志里的 critic loss 直接报告成“真实 Wasserstein 距离”。

## 6. 为什么支持集不重叠时 Wasserstein 仍有信号

若两个连续分布支撑在不相交低维流形上，某些 KL/JS 目标可能无限、饱和或缺少有用梯度。Wasserstein 仍能根据两个支撑集在 ground metric 下相距多远给出有限变化。

但这不是说 Wasserstein 总比 KL 好：

- $W_p$ 强依赖坐标尺度和 ground metric；
- 高维经验 Wasserstein 的样本复杂度可能很差；
- KL 对密度比、最大似然和统计推断有直接意义；
- 不同距离控制不同的函数期望与收敛拓扑。

应根据任务需要什么性质选择 discrepancy，而不是排名“谁更高级”。

## 7. 动态 OT：把搬土变成连续流

对欧氏空间中的 $W_2$，Benamou–Brenier 公式在适当正则条件下给出

$$
W_2(\mu_0,\mu_1)^2
=\inf_{(\rho_t,v_t)}
\int_0^1\int
\|v_t(x)\|^2\rho_t(x)\,dx\,dt,
$$

约束为

$$
\partial_t\rho_t+\nabla\cdot(\rho_t v_t)=0,
\qquad \rho_0=\mu_0,\quad \rho_1=\mu_1.
$$

这把静态搬运计划改写成“用最小动能的速度场连续搬运概率云”。最优路径是 Wasserstein 空间中的 displacement geodesic。

它和 flow matching 都使用连续性方程，但**任意 flow matching 路径不等于动态 OT 最优路径**。要成为 $W_2$ geodesic，需要 coupling、速度和动能都满足对应最优性条件。OT coupling 常被用来降低条件 flow matching 的轨迹交叉或回归方差，这是设计选择，不是 flow matching 定义本身。

## 8. Entropic OT 与 Sinkhorn

离散 OT 是线性规划，高维大样本计算昂贵。加入熵正则：

$$
\min_{\gamma\in\Pi(\mu,\nu)}
\langle C,\gamma\rangle
+\varepsilon\operatorname{KL}(\gamma\|\mu\otimes\nu)
$$

可用 Sinkhorn 矩阵缩放高效求解，并得到更平滑的 coupling。

$\varepsilon$ 大时更平滑、更容易算，但偏离原始 OT 更远。正则化 OT cost 甚至可能在 $\mu=\nu$ 时不为零；Sinkhorn divergence 通过减去自成本进行 debias。小 $\varepsilon$ 又可能带来数值下溢，应使用 log-domain stabilization，连接 [浮点数、数值稳定性与条件数](../%E6%95%B0%E5%80%BC%E8%AE%A1%E7%AE%97/%E6%B5%AE%E7%82%B9%E6%95%B0%E3%80%81%E6%95%B0%E5%80%BC%E7%A8%B3%E5%AE%9A%E6%80%A7%E4%B8%8E%E6%9D%A1%E4%BB%B6%E6%95%B0.md)。

## 9. 生成模型评估：FID 与 Wasserstein 的关系

若把真实与生成的 feature 分别近似成高斯

$$
\mathcal N(m_r,C_r),\qquad \mathcal N(m_g,C_g),
$$

它们的平方 $W_2$ 为

$$
\|m_r-m_g\|_2^2
+\operatorname{Tr}\left(
C_r+C_g
-2(C_r^{1/2}C_gC_r^{1/2})^{1/2}
\right).
$$

FID 使用这类公式比较 Inception feature 的经验高斯近似。因此它不是原始图像分布之间的完整 Wasserstein 距离：它依赖 feature extractor、只保留前两阶矩、有限样本下有偏，也可能漏掉非高斯模式差异。

同理，sliced Wasserstein 通过许多一维投影降低计算成本，但只在投影充分、估计可靠时反映高维差异。

## 10. 可运行示例：一维排序得到最优 coupling

```python
import numpy as np

def empirical_wasserstein_1d(x, y, p=1):
    """等样本数、等权的一维经验 W_p。"""
    x = np.sort(np.asarray(x, dtype=float))
    y = np.sort(np.asarray(y, dtype=float))
    assert x.shape == y.shape
    return np.mean(np.abs(x - y) ** p) ** (1.0 / p)

x = np.array([0.0, 1.0, 2.0, 8.0])
y = np.array([1.0, 3.0, 4.0, 5.0])

w1 = empirical_wasserstein_1d(x, y, p=1)
w2 = empirical_wasserstein_1d(x, y, p=2)

# 一个故意交叉的合法配对；成本高于排序配对。
crossed_cost = np.mean(np.abs(np.sort(x) - np.sort(y)[::-1]))

print("W1:", w1)
print("W2:", w2)
print("crossed coupling mean cost:", crossed_cost)

assert np.isclose(w1, 2.0)
assert np.isclose(w2, np.sqrt(4.5))
assert crossed_cost > w1

# 整个经验分布平移 2：任意 p>=1 的 W_p 都恰为 2。
rng = np.random.default_rng(2)
samples = rng.normal(size=10_000)
shifted = samples + 2.0
assert np.isclose(empirical_wasserstein_1d(samples, shifted, 1), 2.0)
assert np.isclose(empirical_wasserstein_1d(samples, shifted, 2), 2.0)
```

## 11. 常见误区

1. **“coupling 就是把两边独立采样配对。”** 独立 coupling 只是众多方案之一，通常不是最优。
2. **“Wasserstein 只比较密度高度。”** 它还使用样本空间 ground metric。
3. **“任意 critic 差值就是 $W_1$。”** 只有对全部 1-Lipschitz 函数的最优值才是。
4. **“WGAN-GP 精确保证 1-Lipschitz。”** 它只在采样位置做软惩罚。
5. **“Wasserstein 在高维天然好估计。”** 经验 OT 可能遭遇维度灾难。
6. **“flow matching 轨迹就是 OT geodesic。”** 需要额外的最优 coupling 与动能条件。
7. **“FID 是真实数据分布之间的 Wasserstein 距离。”** 它是特定 feature 空间中的高斯近似量。
8. **“熵正则只加速、不改变答案。”** 它改变优化目标并引入可控偏差。
9. **“ $W_2^2$ 也是距离。”** $W_2$ 是距离；平方后一般不满足三角不等式。

## 12. 自测

1. coupling 的两个边缘约束分别保证什么？
2. Monge map 为什么可能不存在，而 Kantorovich coupling 仍存在？
3. 一维 $W_p$ 为什么可以通过分位数对齐计算？
4. WGAN critic 必须满足什么函数约束？有限神经网络训练为何只是近似？
5. 写出 Benamou–Brenier 的连续性方程约束，并解释动能项。
6. 为什么两个 support 不相交的分布仍可有有限 Wasserstein 距离？
7. FID 在什么意义下连接高斯 $W_2^2$，又遗漏了什么？

## 延伸阅读

- Villani, *Optimal Transport: Old and New*, Springer, 2009.
- Peyré & Cuturi, [Computational Optimal Transport](https://arxiv.org/abs/1803.00567), 2019.
- Benamou & Brenier, [A Computational Fluid Mechanics Solution to the Monge–Kantorovich Mass Transfer Problem](https://doi.org/10.1007/s002110050002), 2000.
- Arjovsky, Chintala & Bottou, [Wasserstein GAN](https://proceedings.mlr.press/v70/arjovsky17a.html), ICML 2017.
- Gulrajani et al., [Improved Training of Wasserstein GANs](https://proceedings.neurips.cc/paper/2017/hash/892c3b1c6dccd52936e27cbd0ff683d6-Abstract.html), NeurIPS 2017.
- Cuturi, [Sinkhorn Distances: Lightspeed Computation of Optimal Transport](https://proceedings.neurips.cc/paper/2013/hash/af21d0c97db2e27e13572cbf59eb343d-Abstract.html), NeurIPS 2013.
- Heusel et al., [GANs Trained by a Two Time-Scale Update Rule Converge to a Local Nash Equilibrium](https://proceedings.neurips.cc/paper/2017/hash/8a1d694707eb0fefe65871369074926d-Abstract.html), NeurIPS 2017（提出 FID）。
