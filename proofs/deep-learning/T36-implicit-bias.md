---
id: T36
type: proof-template
refined: 2026-10-20
status: bounded-scope
---

# T36. Implicit bias and directional convergence

[主题目录](README.md) · [优化模板](../optimization/T01-descent.md)

## 复用契约

**输入对象**：参数化、固定数据、loss、优化器、初始化、步长与要观察的极限对象。

**输出结论**：算法在许多低损失解中偏向何种方向或结构。参数、函数、方向、margin 和风险是不同对象。

本卡的主要实例限定为有限可分数据上的无正则、齐次线性 logistic regression 与 full-batch GD。

**失败例子**：loss 趋近零，但权重范数趋于无穷；因此不能写“参数收敛到一个有限全局最优点”。

## 实例化时必须完成

- [ ] 固定参数化与优化几何；Adam、GD、因子化参数不能互换结论。
- [ ] 说明收敛的是 loss、方向、预测函数还是参数。
- [ ] 检查可分性、loss tail、学习率和初始点条件。
- [ ] 若要从隐式偏置推出测试风险改善，额外连接统计理论。

## 1. 优化目标没有写出的偏好

多个模型都能拟合训练集，优化器却不一定等概率选择它们。更新规则、参数化和初始化共同决定路径，这种路径偏好称为 implicit bias。

它不是额外加到 objective 上的显式正则，也不自动意味着对新数据有益。

## 2. 一维例子：为什么权重会继续长大

只有一个有效样本 $yx=1$ 时，logistic loss 为

$$
\ell(w)=\log(1+e^{-w}),\qquad
w_{t+1}=w_t+\frac{\eta}{1+e^{w_t}}.
$$

只要 $\eta>0$，迭代严格增加。假设它被某个 $M$ 上界，则每步增量至少为 $\eta/(1+e^M)>0$，与有界性矛盾。因此 $w_t\to+\infty$，而 loss 趋于 0。

这里优化 infimum 为 0，却没有有限 minimizer。分类早已正确后，logistic objective 仍推动 margin 增大。

## 3. 多维线性 logistic 的方向结论

令 $X=[x_1,\ldots,x_n]\in\mathbb R^{d\times n}$， $n\geq1$，标签 $y_i\in\lbrace-1,1\rbrace$，数据严格线性可分。使用

$$
F(w)=\sum_i\log(1+\exp(-y_iw^\top x_i)).
$$

单样本 logistic loss 对 margin 的梯度 Lipschitz 常数为 $\beta=1/4$，因此 $F$ 的 smoothness 至多 $\beta\Vert X\Vert_{\mathrm{op}}^2$。

Soudry 等论文的相应结论适用于固定正步长

$$
0<\eta<\frac{2}{\beta\Vert X\Vert_{\mathrm{op}}^2},
$$

任意有限初始化，以及论文的 loss tail 条件（logistic 满足）。有

$$
w_t=\widehat w\log t+\rho_t,\qquad
\Vert\rho_t\Vert=O(\log\log t),
$$

其中

$$
\widehat w=\arg\min_w\Vert w\Vert^2
\quad\text{s.t.}\quad y_iw^\top x_i\geq1\ \forall i.
$$

所以归一化方向趋向 $\widehat w/\Vert\widehat w\Vert$。若用平均 loss，步长的样本数因子须相应调整。

上述渐近式是引用的专门定理，不是仅由“小梯度”推得；论文完整证明处理 support vectors 与残差。退化数据可出现 log-log 残差，不应把“几乎所有数据 residual 有界”升级成对全部数据有界。

## 4. 证明骨架与直觉

1. 可分性与合适步长使经验 loss 下降到 infimum，margin 逐渐增大。
2. logistic 梯度在大正 margin 下近似指数衰减。
3. 较小 margin 的样本衰减更慢，长期主导方向。
4. 将这种主导关系接到 hard-margin 问题的最优性条件。
5. 真正困难的是证明渐近展开与残差控制，而非猜出 max-margin 方向。

固定特征的结论不能自动推广到同时学习表示的深网络；更换优化器或参数化也会改变几何。

## 5. 原文定位与关联

2026-10-20 已交叉核对固定版本 `arxiv:1710.10345v7` 的本地 PDF、TeX 与 metadata 哈希：PDF 物理第 3 页的 Lemma 1、第 4 页的 Theorem 3，及 [源码](../../proof_ref/foundations-2026-09/the-implicit-bias-of-gradient-descent-on-separable-1710.10345/source/JMLR_paper_24.2.2018.tex) 的 `thm: main theorem`。求和 loss、步长条件、初始化范围与残差结论一致；详细定位和复用边界见 [限定范围核验笔记](../../proof_ref/foundations-2026-09/the-implicit-bias-of-gradient-descent-on-separable-1710.10345/核验笔记.md)。

这不表示已逐式复核整个附录。方向极限可以再连接 [T35 margin](../generalization/T35-margin-norm.md)，但统计假设与有限时间 rate 仍需满足。

来源：[The Implicit Bias of Gradient Descent on Separable Data v7](https://arxiv.org/abs/1710.10345v7)。

## 本地论文与前置工具

通用工具：P01, P02，见 [证明原语](../../通用证明原语.md)。

- [The Implicit Bias of Gradient Descent on Separable Data](../../proof_ref/foundations-2026-09/the-implicit-bias-of-gradient-descent-on-separable-1710.10345/README.md)
- [The Modern Mathematics of Deep Learning](../../proof_ref/dl-core-2026-09/the-modern-mathematics-of-deep-learning-2105.04026/README.md)

## 专项证明接口（2026-10-02）

- [T42：精确跟踪时变核、参数移动与冻结核近似，不把核变化当下游收益。](T42-feature-drift-kernel-dynamics.md)
