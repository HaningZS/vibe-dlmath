---
id: T47
type: proof-template
refined: 2026-10-02
status: self-contained-core
---

# T47. 本地训练、客户端漂移与通信预算

[主题目录](README.md) · [Lyapunov T02](T02-lyapunov.md) · [估计递推 T03](T03-variance-reduction.md)

## 复用契约

**对象**：固定非负权重 $p_i$、 $\sum_i p_i=1$，目标 $F=\sum_i p_if_i$。所有客户端参与，同一步长，精确本地梯度；每至多 $\tau$ 步同步到加权平均。

**条件**： $f_i$ 均 $L$-smooth， $F$ 下有界； $0<\eta\le1/L$。若使用下面的粗漂移界，还要求实际局部路径上 $\Vert\nabla f_i\Vert\le G$。

**结论**：virtual averaged iterate 的平均梯度平方界与通信误差项。随机梯度、客户端抽样、压缩或异步不是本卡基本定理的一部分。

**失败例子**：本地更新多步后平均模型，一般不等于在全局目标上走同样多步梯度下降。不同本地步数/学习率甚至可能改变有效目标权重。

## 实例化时必须完成

- [ ] 目标权重与实际采样、聚合、样本量权重一致。
- [ ] 写出 drift 递推、初值和同步后是否归零。
- [ ] 区分 virtual iterate、实际通信点、last iterate 和输出规则。
- [ ] 每轮本地梯度次数、通信轮数及额外取输出的通信都登记。

## 1. 直觉：先各自走，再集合，会走偏

所有客户端从同一点出发时，梯度的加权平均就是全局梯度。但各自走了几步，测量梯度的位置就不同了。这个“站错位置造成的误差”是 drift；它与随机采样噪声是不同来源。

## 2. 不隐藏 drift 的精确更新

定义 $\bar x_k=\sum_i p_ix_{i,k}$、 $D_k=\sum_i p_i\Vert x_{i,k}-\bar x_k\Vert^2$。两次同步之间

$$
\bar x_{k+1}=\bar x_k-\eta(\nabla F(\bar x_k)+e_k),
\quad e_k=\sum_i p_i[\nabla f_i(x_{i,k})-\nabla f_i(\bar x_k)].
$$

Jensen 与 smoothness 给出 $\Vert e_k\Vert^2\le L^2D_k$。同步把所有 $x_i$ 设为平均，不改变 $\bar x$，并让下一轮初始 $D$ 为 0。

## 3. 带确定性偏差的一步下降

令 $g=\nabla F(\bar x_k)$。利用
$-\langle g,g+e\rangle=-\Vert g\Vert^2/2-\Vert g+e\Vert^2/2+\Vert e\Vert^2/2$，smoothness 得到

$$
F(\bar x_{k+1})\le F(\bar x_k)
-\tfrac\eta2\Vert g\Vert^2+\tfrac\eta2\Vert e_k\Vert^2
\le F(\bar x_k)-\tfrac\eta2\Vert g\Vert^2+\tfrac{\eta L^2}2D_k.
$$

因 $\eta\le1/L$，省略的 $\Vert g+e\Vert^2$ 系数非正。望远镜相加得到

$$
\frac1K\sum_{k< K}\Vert\nabla F(\bar x_k)\Vert^2
\le\frac{2(F(\bar x_0)-\inf F)}{\eta K}
+\frac{L^2}{K}\sum_{k< K}D_k.
$$

这已经明确了下一条需要证明的 lemma：控制客户端分歧，而不是把 $e_k$ 当成无偏噪声。

## 4. 一个粗但完整的漂移闭合

一轮开始时共同位置为 $x^{round}$。若本地路径梯度至多 $G$，轮内第 $j$ 步有
$\Vert x_{i,j}-x^{round}\Vert\le\eta Gj$，平均同样成立。于是
$D_j\le4\eta^2G^2j^2\le4\eta^2G^2\tau^2$。

代回得到

$$
\frac1K\sum_{k< K}\Vert\nabla F(\bar x_k)\Vert^2
\le\frac{2\Delta_F}{\eta K}+4L^2\eta^2G^2\tau^2.
$$

这个基础界显示减少通信可能增加 drift 项；它不是最优 local-SGD rate。全局梯度有界是附加假设，不能在任意二次目标的全部空间直接宣称成立。

## 5. 输出与实际算法怎样对齐

平均梯度界可以给随机选择的 virtual $\bar x_k$ 的期望保证。如果实际只输出最后一个通信点，仍须另证对应结论。

要实现随机 virtual 输出，可预先独立选择一个 $k$，保存该时刻各客户端模型并额外通信一次取平均；需要计入这一通信。不能让理论输出一个服务器从未收到的参数。

随机梯度会加入条件方差项，client sampling 需要权重校正，SCAFFOLD/control variate 则改变 drift 递推；参见 [T02](T02-lyapunov.md)、[T03](T03-variance-reduction.md)。

## 前置、关联与证据

- [梯度下降](<../../Math 基础/微积分与分析/梯度下降、学习率与收敛.md>) · [条件期望](<../../Math 基础/概率统计/测度、条件期望、滤过与适应过程.md>)。
- [Local SGD 原论文](https://arxiv.org/abs/1805.09767) · [本地卡](../../proof_ref/dl-specializations-2026-10/local-sgd-converges-fast-and-communicates-little-1805.09767/README.md)。
- [SCAFFOLD 原论文](https://arxiv.org/abs/1910.06378) · [本地卡](../../proof_ref/dl-specializations-2026-10/scaffold-stochastic-controlled-averaging-for-federated-learning-1910.06378/README.md)。本卡原型与两篇来源的完整算法/rate 分开核验。

## 专项证明接口（2026-10-02）

- [T01：把单步目标下降累积成平均梯度平方界。](T01-descent.md)

## 经典与近期证明蒸馏

- [经典下降证明的偏差与方差接口](../../extensions/%E7%BB%8F%E5%85%B8%E4%B8%8B%E9%99%8D%E8%AF%81%E6%98%8E%E7%9A%84%E5%81%8F%E5%B7%AE%E4%B8%8E%E6%96%B9%E5%B7%AE%E6%8E%A5%E5%8F%A3.md)
