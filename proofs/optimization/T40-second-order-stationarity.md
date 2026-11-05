---
id: T40
type: proof-template
refined: 2026-10-02
status: self-contained-core
---

# T40. 二阶驻点、负曲率与鞍点逃逸

[主题目录](README.md) · [总框架](../../docs/DL_THEORY_FRAMEWORK.md) · [一阶下降 T01](T01-descent.md)

## 复用契约

**对象**：二次连续可微、下有界的 $f:\mathbb R^d\to\mathbb R$；梯度为 $L$-Lipschitz，Hessian 为 $\rho$-Lipschitz， $L,\rho>0$。范数均为 Euclidean/operator norm。

**结论**：在精确梯度和负曲率方向 oracle 下，有限次更新到达 $\Vert\nabla f\Vert\le\epsilon_g$、 $\lambda_{\min}(\nabla^2f)\ge-\epsilon_H$。这里计算的是更新次数；寻找特征向量的成本另外记账。

**失败例子**： $f(x)=x^3$ 在 0 处梯度、Hessian 都为 0，却不是局部极小。二阶必要条件仍不是一般全局最优证书；此例用于说明逻辑关系，不满足本卡全局下有界假设。

## 实例化时必须完成

- [ ] 证明梯度/Hessian 正则性在整个访问区域成立，并关闭不退出条件。
- [ ] 写出负曲率 oracle 的误差、成功概率和计算成本。
- [ ] 要推局部/全局极小，额外证明 landscape 条件。
- [ ] ReLU 原目标是否真有本卡所需 Hessian；平滑替代后的误差如何处理。

## 1. 直觉：山坡很平，仍可能横向下滑

梯度描述当前位置的坡度。鞍点附近坡度可能很小，但某个方向仍向下弯；Hessian 的负特征值就是这条方向。像站在马鞍中心：前后向上，左右向下。

两个阈值分别问“现在还陡不陡”和“有没有明显向下弯的方向”，不能只检测前者。

## 2. 二阶 Taylor 余项从哪里来

Hessian-Lipschitz 给出

$$
f(x+s)\le f(x)+\langle\nabla f(x),s\rangle
+\tfrac12s^\top\nabla^2f(x)s+\tfrac\rho6\Vert s\Vert^3.
$$

可沿线段积分两次：二阶余项为
$\int_0^1(1-t)s^\top[H(x+ts)-H(x)]s\thinspace dt$，其绝对值不超过
$\rho\Vert s\Vert^3\int_0^1t(1-t)dt=\rho\Vert s\Vert^3/6$。

## 3. 负曲率下降的完整一步

若单位向量 $v$ 满足 $v^\top H(x)v\le-\epsilon_H$，选 $s=\pm av$ 的符号使 $\langle\nabla f,s\rangle\le0$，并取 $a=2\epsilon_H/\rho$。于是

$$
f(x+s)-f(x)
\le-\tfrac12\epsilon_Ha^2+\tfrac\rho6a^3
=-\frac{2\epsilon_H^3}{3\rho^2}.
$$

符号选择很重要：即使梯度很小，沿错误方向走也可能先上升。

## 4. 与一阶下降组合成有限更新界

算法每次按以下顺序判断：

1. 若 $\Vert\nabla f(x)\Vert>\epsilon_g$，走 $s=-\nabla f(x)/L$；[T01](T01-descent.md) 给出下降至少 $\epsilon_g^2/(2L)$。
2. 否则查 Hessian；若存在上面的负曲率方向，做第 3 节更新。
3. 否则停止，输出满足两个阈值的点。

令 $\Delta=f(x_0)-\inf f$。两种更新次数分别满足

$$
N_g\le\frac{2L\Delta}{\epsilon_g^2},\qquad
N_H\le\frac{3\rho^2\Delta}{2\epsilon_H^3}.
$$

总更新不超过两个上界之和；每次判断和特征方向求解另有成本。常用 $\epsilon_H=\sqrt{\rho\epsilon_g}$ 时，负曲率更新预算为 $3\sqrt\rho\Delta/(2\epsilon_g^{3/2})$。

## 5. 怎样读“扰动 GD 可以逃逸鞍点”

[Jin 等人的原论文](https://arxiv.org/abs/1703.00887) 分析一阶方法如何借随机扰动和局部动力学找到逃逸方向。本卡的精确 Hessian-oracle 原型解释下降机制；该论文的一阶 oracle 总复杂度还需要局部耦合、逃逸概率、时间窗口和失败预算等证明。

严格鞍点性质、无坏局部极小、定量 basin 条件也各有作用。不能从“二阶驻点”直接跳到“深网络已达到全局最优”。

## 前置、关联与证据

- [Hessian 与自动微分](<../../Math 基础/微积分与分析/导数、梯度、Jacobian、Hessian 与自动微分.md>) · [二次型与谱](<../../Math 基础/线性代数/二次型、正定矩阵与谱.md>)。
- [T39 非光滑边界](T39-proximal-nonsmooth.md) · [T32 风险分解](../generalization/T32-excess-risk-decomposition.md)；二阶驻点如何控制优化 gap 仍需桥梁。
- [本地论文卡](../../proof_ref/dl-specializations-2026-10/how-to-escape-saddle-points-efficiently-1703.00887/README.md)。本卡完整证明的是列明 oracle 下的基础结论，未重证该论文全部主定理。
