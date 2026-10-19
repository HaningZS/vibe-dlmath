---
id: T45
type: proof-template
refined: 2026-10-02
status: self-contained-core
---

# T45. 间隔、Lipschitz 与随机平滑的鲁棒认证

[主题目录](README.md) · [Margin T35](T35-margin-norm.md) · [统计覆盖 T18](../statistics/T18-split-conformal.md)

## 复用契约

**对象**：固定分类器、指定输入范数。路线 A 控制 logits 的 Lipschitz 常数；路线 B 定义 Gaussian smoothing 后的分类器 $g(x)=\arg\max_c\Pr(f(x+Z)=c)$，$Z\sim N(0,\sigma^2I)$。

**结论**：针对指定点、指定模型和指定范数的认证半径。平滑证书针对 $g$；Monte Carlo 估计须提供真实类别概率的有效置信界。

**条件**：类别有限、预测事件可测；$\sigma>0$，公式使用 $p_A,p_B\in(0,1)$；概率下/上界同时成立。半径用 strict inequality，边界 tie 不自动认证；概率端点可另取极限。

**失败例子**：攻击器没找到对抗例只说明这次搜索失败；不能给出“所有半径内扰动”的量词。

## 实例化时必须完成

- [ ] 扰动范数、输入预处理、模型和输出规则完全一致。
- [ ] Lipschitz 常数覆盖整个候选球，或 Gaussian 概率界合法。
- [ ] 类别选择和认证采样的独立性/多重比较预算明确。
- [ ] 区分 clean accuracy、empirical attack accuracy 和 certified accuracy。

## 1. 直觉：离决策边界多远，最多能走多快

margin 是当前领先类别的优势；Lipschitz 常数是扰动能改变这种优势的最大速度。距离大、速度小，才保证有一段路走不到决策边界。

随机平滑走另一条路：先把分类器在邻域噪声下的投票变成新分类器，再控制移动邻域中心后，投票概率最多改变多少。

## 2. 确定性 logit 证书

设当前类别 $a$，$s_a(x)-s_b(x)\ge\gamma_b>0$。若 $s_c$ 在球内为 $L_c$-Lipschitz，则

$$
s_a(x+u)-s_b(x+u)\ge\gamma_b-(L_a+L_b)\|u\|.
$$

因此 $\|u\|<\min_{b\ne a}\gamma_b/(L_a+L_b)$ 保证类别不变；分母为 0 且 margin 正时该对无限制。统一 $L$ 给出 $\gamma/(2L)$。

深网络用各层 operator norm 乘积控制全局 Lipschitz 时，需把 residual、normalization、attention 和激活常数都算进去。宽松常数可能让证书接近 0。

## 3. Gaussian 平移的最坏事件

令 $P=N(x,\sigma^2I)$、$Q=N(x+u,\sigma^2I)$，$k=\|u\|_2/\sigma$。沿 $u$ 的标准化投影记为 $z$；$P$ 下 $z\sim N(0,1)$，$Q$ 下 $z\sim N(k,1)$，密度比 $dQ/dP=e^{kz-k^2/2}$ 单调增加。

固定 $P(A)=p$，最小 $Q(A)$ 的集合是左半空间 $H=\{z\le\Phi^{-1}(p)\}$。证明：令其边界密度比为 $c$，则
$\int(1_A-1_H)(dQ-c\,dP)\ge0$；在 $H$ 内两个因子均非正，在外均非负，且 $P(A)-P(H)=0$。所以 $Q(A)\ge Q(H)$。

右半空间同理最大化 $Q(A)$。扩大/缩小事件后也得到概率界版本：

$$
P(A)\ge p\Rightarrow Q(A)\ge\Phi(\Phi^{-1}(p)-k),
\quad P(B)\le q\Rightarrow Q(B)\le\Phi(\Phi^{-1}(q)+k).
$$

## 4. 多类别平滑半径

若 $p_A$ 是领先类别真实概率的下界，$p_B$ 是所有其他类别概率的共同上界，$p_A>p_B$，则

$$
R=\frac\sigma2\big[\Phi^{-1}(p_A)-\Phi^{-1}(p_B)\big]
$$

保证所有 $\|u\|_2<R$ 下仍预测 $A$。两边的 Gaussian 界保持严格领先即可。使用 $p_B=1-p_A$ 且 $p_A>1/2$ 得到简化的 $R=\sigma\Phi^{-1}(p_A)$。

## 5. 有限采样怎样保持认证含义

认证阶段抽取独立噪声，使用有效的 binomial 概率置信界。可先用独立 pilot 选择类别，再对这个固定类别构造下界；或对数据依赖选择使用同时置信界。多类别上界也要同时有效。

若事件的失败概率为 $\delta_{MC}$，上面的认证随该事件成立。对多个输入给联合结论时还要分配失败预算。这个概率来自噪声估计，并不是 [T18](../statistics/T18-split-conformal.md) 的交换性覆盖保证。

## 前置、关联与证据

- [Lipschitz](<../../Math 基础/微积分与分析/Lipschitz constant.md>) · [范数与距离](<../../Math 基础/线性代数/范数、距离、相似度与度量学习.md>) · [置信区间](<../../Math 基础/概率统计/置信区间、假设检验与多重比较.md>)。
- [T35](T35-margin-norm.md) · [T18](../statistics/T18-split-conformal.md) · [原论文](https://arxiv.org/abs/1902.02918) · [本地卡](../../proof_ref/dl-specializations-2026-10/certified-adversarial-robustness-via-randomized-smoothing-1902.02918/README.md)。
- [固定 v2 的 scoped 核验记录](../../proof_ref/dl-specializations-2026-10/certified-adversarial-robustness-via-randomized-smoothing-1902.02918/核验笔记.md)。
