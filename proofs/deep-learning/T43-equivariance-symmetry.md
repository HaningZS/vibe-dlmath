---
id: T43
type: proof-template
refined: 2026-10-20
status: self-contained-core
---

# T43. 群作用、等变架构与对称化

[主题目录](README.md) · [GNN 表达力 T44](../lower-bounds-expressivity/T44-message-passing-wl.md)

## 复用契约

**对象**：群 $G$、输入/输出上的线性表示 $\rho_{in},\rho_{out}$。等变指 $F(\rho_{in}(g)x)=\rho_{out}(g)F(x)$；输出表示恒为 identity 时是不变。

**结论**：线性层的 intertwining 条件、有限群对称化恒等式和有条件的风险改进。self-attention 的排列恒等式只对相应 mask/位置结构成立。

**必需假设**：组合中的每层与非线性均满足指定表示；风险比较要求数据与标签的群不变 law 和凸损失。

**失败例子**：把 6 与 9 的数字分类强制成所有旋转都不变，会把本应不同的标签混在一起。选错群会限制任务信息。

## 实例化时必须完成

- [ ] 写出输入、输出、隐藏特征各自怎样变换。
- [ ] 检查 bias、非线性、pooling、padding、stride 和 mask。
- [ ] 区分函数恒等式、风险比较与训练可达性。
- [ ] 扩展为紧群的归一化 Haar 概率积分时，给出可测性、可积性及采样/离散化误差；非紧群不能直接套有限平均。

## 1. 直觉：换坐标，答案应相应换坐标

图节点重新编号不该改变“这是不是同一张图”。关键点坐标却必须跟着图像旋转。所以分类常需要不变，定位常需要等变；二者由输出任务决定。

表示 $\rho(g)$ 是变换 $g$ 在向量坐标中的具体操作。例如排列矩阵重排行，二维旋转矩阵旋转坐标。

## 2. 线性层的完整条件

对 $F(x)=Wx+b$，比较两边得到

$$
W\rho_{in}(g)=\rho_{out}(g)W,\qquad
b=\rho_{out}(g)b\quad(\forall g).
$$

前者称 intertwining，意思是“先变换再过层”和“先过层再变换”一致。满足条件的层可组合，因为中间输出/输入使用同一种表示。

逐元素 ReLU 与排列矩阵可交换；它与一般旋转表示通常不交换。因此任意矩阵满足线性条件后再接 ReLU，并不自动保持旋转等变。

## 3. 有限群平均直接构造等变函数

对任意 $f$，定义

$$
F_G(x)=\frac1{|G|}\sum_{g\in G}\rho_{out}(g)^{-1}f(\rho_{in}(g)x).
$$

把输入换为 $\rho_{in}(h)x$，令 $k=gh$；因 $g=kh^{-1}$，有
$\rho_{out}(g)^{-1}=\rho_{out}(h)\rho_{out}(k)^{-1}$。于是
$F_G(\rho_{in}(h)x)=\rho_{out}(h)F_G(x)$。

计算成本是 $|G|$ 次调用；有限群的恒等式不等于任意连续群都能精确枚举。

紧群可使用归一化 Haar 概率测度，把有限求和改为积分；等变性证明仍需换元不变性和向量值积分存在。非紧群没有归一化的有限 Haar 概率测度，例如平移群 $\mathbb R$ 的 Haar 测度是 Lebesgue 测度的常数倍，总质量无限。给群元素任意选一个概率分布或截断窗口，通常不再保持所需的平移不变性，因此不能据此声称精确等变或直接套下一节的平均风险比较。

## 4. 对称化何时不会增加风险

标量不变任务令 $\rho_{out}=1$。若 $(\rho_{in}(g)X,Y)$ 与 $(X,Y)$ 同分布，且 $\ell(\cdot,y)$ 凸，Jensen 与分布不变性给出

$$
R(F_G)\le\frac1{|G|}\sum_g\mathbb E\ell(f(\rho_{in}(g)X),Y)=R(f).
$$

这证明风险比较；有限样本统计复杂度改善或训练算法找到 $F_G$ 仍要 [T33](../generalization/T33-uniform-convergence.md) 与优化证明。标签 law 不保留时，此结论没有依据。

## 5. 无位置 self-attention 的排列证明

令 $A(X)=\mathop{\mathrm{softmax}}\nolimits_{row}(QK^\top/\sqrt d)V$， $Q=XW_Q$ 等。排列矩阵 $P$ 作用后 $Q'=PQ$ 等，且

$$
\mathop{\mathrm{softmax}}\nolimits_{row}(PMP^\top)
=P\mathop{\mathrm{softmax}}\nolimits_{row}(M)P^\top,
\qquad A(PX)=PA(X).
$$

每行共享的 FFN、LayerNorm 和 residual 同样保持排列等变。加固定位置表 $E$ 时， $PX+E$ 通常不等于 $P(X+E)$。固定 mask $M$ 只保留满足 $PMP^\top=M$ 的排列；causal mask 不允许任意 token 重排。对称 readout 才把 token 级等变转成全局不变。

## 前置、关联与证据

- [群、表示与等变直觉](<../../Math 基础/信号与几何/对称性、群表示与等变网络.md>) · [T44](../lower-bounds-expressivity/T44-message-passing-wl.md) · [T14 算法模拟](T14-algorithm-simulation.md)。
- [原论文](https://arxiv.org/abs/1602.07576) · [本地论文卡](../../proof_ref/dl-specializations-2026-10/group-equivariant-convolutional-networks-1602.07576/README.md)。这里给出有限群和排列原型；具体连续群卷积按来源条件继续推导。
