---
type: note
domain: math/statistical-learning-theory
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# 算法稳定性、经验过程与 PAC-Bayes

进一步实例化：[T32 风险分解](../../proofs/generalization/T32-excess-risk-decomposition.md)、[T33 一致收敛](../../proofs/generalization/T33-uniform-convergence.md)、[T35 间隔与范数](../../proofs/generalization/T35-margin-norm.md)、[T38 压缩](../../proofs/generalization/T38-compression.md)。

训练误差低，只说明模型会回答已经看过的考题；泛化关心的是：**换一批来自同一数据分布的新题，它还能答得好吗？**

统计学习理论有三种很常见、但经常被混成一团的解释路线：

1. **算法稳定性**：训练集只换一个样本，训练算法的输出会不会大变？
2. **经验过程 / 一致收敛**：一个函数类里，有没有模型只是因为候选太多而碰巧在训练集表现好？
3. **PAC-Bayes**：训练后的随机预测器相对训练前的先验移动了多远，这种数据依赖需要支付多少 KL 复杂度？

它们像三种体检：稳定性检查“训练过程是否敏感”，经验过程检查“候选空间是否太大”，PAC-Bayes 检查“数据把模型从先验推走了多远”。任何一种都不是大模型泛化的完整解释。

## 知识依赖、模板与论文入口

- 学习路线：[AI 理论证明前置学习路线](../%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/AI%20%E7%90%86%E8%AE%BA%E8%AF%81%E6%98%8E%E5%89%8D%E7%BD%AE%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)；总入口：[Math 基础目录](../Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md)。
- 样本均值与总体期望：[大数定律、中心极限定理与采样误差](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E5%A4%A7%E6%95%B0%E5%AE%9A%E5%BE%8B%E3%80%81%E4%B8%AD%E5%BF%83%E6%9E%81%E9%99%90%E5%AE%9A%E7%90%86%E4%B8%8E%E9%87%87%E6%A0%B7%E8%AF%AF%E5%B7%AE.md)。
- 条件期望、独立性与可测性：[测度、条件期望、滤过与适应过程](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%B5%8B%E5%BA%A6%E3%80%81%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E3%80%81%E6%BB%A4%E8%BF%87%E4%B8%8E%E9%80%82%E5%BA%94%E8%BF%87%E7%A8%8B.md)。
- KL 与互信息：[信息论基础：熵、交叉熵与 KL 散度](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E4%BF%A1%E6%81%AF%E8%AE%BA%E5%9F%BA%E7%A1%80%EF%BC%9A%E7%86%B5%E3%80%81%E4%BA%A4%E5%8F%89%E7%86%B5%E4%B8%8E%20KL%20%E6%95%A3%E5%BA%A6.md)。
- 统计检验与多重比较：[置信区间、假设检验与多重比较](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E7%BD%AE%E4%BF%A1%E5%8C%BA%E9%97%B4%E3%80%81%E5%81%87%E8%AE%BE%E6%A3%80%E9%AA%8C%E4%B8%8E%E5%A4%9A%E9%87%8D%E6%AF%94%E8%BE%83.md)。
- 下界与统计距离：[统计距离、Le Cam、Fano、Assouad 与 Yao 下界](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E7%BB%9F%E8%AE%A1%E8%B7%9D%E7%A6%BB%E3%80%81Le%20Cam%E3%80%81Fano%E3%80%81Assouad%20%E4%B8%8E%20Yao%20%E4%B8%8B%E7%95%8C.md)。
- 通用原语：[P05：换测度](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p05-couplingchange-of-measure-%E4%B8%8E%E4%BF%A1%E6%81%AF%E9%A2%84%E7%AE%97)、[P07：稳定性递推](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p07-contractiongr%C3%B6nwall-%E4%B8%8E%E7%A8%B3%E5%AE%9A%E6%80%A7%E9%80%92%E6%8E%A8)、[P09：经验过程](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p09-empirical-processsymmetrizationcovering-%E4%B8%8E-local-complexity)。
- 主模板：[T04：算法稳定性](../../proofs/generalization/T04-stability.md)、[T05：PAC-Bayes 与信息论泛化](../../proofs/generalization/T05-pac-bayes-information.md)。
- 近期框架：[R04：无放回采样与局部复杂度](../../%E8%BF%91%E6%9C%9F%E9%A1%B6%E4%BC%9A%E7%90%86%E8%AE%BA%E6%A1%86%E6%9E%B6%EF%BC%882025-2026%EF%BC%89.md#r04-sampling-without-replacement%E4%BA%A4%E6%8D%A2%E6%95%8F%E6%84%9F%E5%BA%A6--efronstein--local-complexity)、[R06：压缩与 PAC-Bayes](../../%E8%BF%91%E6%9C%9F%E9%A1%B6%E4%BC%9A%E7%90%86%E8%AE%BA%E6%A1%86%E6%9E%B6%EF%BC%882025-2026%EF%BC%89.md#r06-sample-compression--pac-bayes)、[R07：泛化界是否可估计](../../%E8%BF%91%E6%9C%9F%E9%A1%B6%E4%BC%9A%E7%90%86%E8%AE%BA%E6%A1%86%E6%9E%B6%EF%BC%882025-2026%EF%BC%89.md#r07-%E5%85%88%E5%88%A4%E6%96%AD%E7%95%8C%E6%98%AF%E5%90%A6%E5%8F%AF%E4%BC%B0%E8%AE%A1)。
- 本地论文：[SGD stability 定义与期望泛化，PDF p.4](../../proof_ref/core-theory-2026-09/train-faster-generalize-better-stability-of-stochastic-gradient-1509.01240/paper.pdf#page=4)、[稳定性递推，PDF p.5](../../proof_ref/core-theory-2026-09/train-faster-generalize-better-stability-of-stochastic-gradient-1509.01240/paper.pdf#page=5)；[PAC-Bayes + compression，PDF p.5](../../proof_ref/recent-accepted-2025-2026/generalization-bounds-via-meta-learned-model-representations-pac-2410.13577/paper.pdf#page=5)；[Transductive local complexity，PDF p.5](../../proof_ref/recent-accepted-2025-2026/improved-generalization-bounds-for-transductive-learning-by-transductive-2309.16858/paper.pdf#page=5)；[泛化界可估计性，PDF p.7](../../proof_ref/core-theory-2026-09/which-algorithms-have-tight-generalization-bounds-2410.01969/paper.pdf#page=7)。

> [!important] 三条路线不能拼成一句万能话
> 稳定性、uniform convergence 和 PAC-Bayes 控制的随机性、量词与对象不同。若一个证明先用期望稳定性，最后却写成对所有模型的高概率界，或把 Gibbs predictor 的界直接送给单个确定性网络，中间一定还缺 theorem。

## 1. Generalization gap：先把“训练好”和“未来好”分开

令数据

$$
S=(Z_1,\ldots,Z_n)\sim\mathcal D^n,
$$

损失为 $\ell(h,z)$。对固定模型 $h$，定义总体风险和经验风险：

$$
L_{\mathcal D}(h)
=\mathbb E_{Z\sim\mathcal D}\ell(h,Z),
\qquad
\widehat L_S(h)
=\frac1n\sum_{i=1}^n\ell(h,Z_i).
$$

generalization gap 是

$$
\mathop{\mathrm{gen}}(h,S)
=L_{\mathcal D}(h)-\widehat L_S(h).
$$

若 $h$ 在看数据前已经固定，普通浓缩通常足够。困难在于训练输出

$$
W=A(S)
$$

依赖同一批数据：算法会主动挑选训练误差小的模型，所以不能把 $W$ 当成与 $S$ 独立的固定对象。

读 theorem 前先辨认四组量词：

| 问题 | 可能的答案 |
|---|---|
| 对谁成立？ | 固定 $h$、训练算法输出 $A(S)$、还是所有 $h\in\mathcal H$ |
| 随机性来自哪里？ | 样本、算法内部随机性、posterior 抽样 |
| 结论形态？ | 期望、概率至少 $1-\delta$、几乎处处 |
| 比较什么？ | 单个 loss、Gibbs risk、整个函数类的 supremum |

这四组量词一变，所需证明工具也会变。

## 2. 算法稳定性：换一道训练题，模型会不会变脸

### 2.1 Replace-one coupling

构造两个只差第 $i$ 个样本的数据集：

$$
S=(Z_1,\ldots,Z_i,\ldots,Z_n),
\qquad
S^{(i)}=(Z_1,\ldots,Z_i',\ldots,Z_n).
$$

若算法有随机 mini-batch 顺序、dropout 或初始化，常让两次运行使用同一随机种子。这是 coupling：尽量只让“被替换样本”成为差异来源。

如果两条训练轨迹为 $w_t,w_t'$，研究

$$
\Delta_t=\Vert w_t-w_t'\Vert.
$$

典型递推是

$$
\Delta_{t+1}
\le a_t\Delta_t+b_t\mathbf1\lbrace\text{本步碰到被替换样本}\rbrace.
$$

$a_t$ 描述更新会放大还是收缩已有差异， $b_t$ 描述真正遇到不同样本时注入多少新差异。最后用 loss 的 Lipschitz 性把参数距离转成预测损失差。

### 2.2 Stability 有多种，不要只写一个词

一种常见的 randomized uniform stability 定义是：若 $S,S'$ 只差一个样本，则

$$
\sup_z
\left|
\mathbb E_U\ell(A(S;U),z)
-\mathbb E_U\ell(A(S';U),z)
\right|
\le\beta,
$$

其中 $U$ 是算法内部随机性。也有更强的 pathwise 版本，要求对每个固定 $U$ 都成立。

常见变体包括：

- **uniform stability**：对所有相邻数据集和测试点取 supremum，最强也常最松；
- **on-average stability**：只在随机替换位置和样本上取平均；
- **hypothesis/parameter stability**：先控制模型或参数距离，再借 loss 正则性转成 loss stability；
- **leave-one-out / delete-one stability**：删除一个样本，而不是替换；常数和耦合会不同；
- **high-probability stability**：控制随机 stability 本身的尾部，不等于“期望稳定性后面加一个 $\delta$”。

在上述 uniform-loss-stability 定义及 IID 等标准条件下，有经典结论

$$
\left|
\mathbb E_{S,U}
\left[L_{\mathcal D}(A(S;U))-\widehat L_S(A(S;U))\right]
\right|
\le\beta.
$$

它是**期望泛化界**。要得到高概率界，需要损失有界等额外条件与专门稳定性浓缩结果。

### 2.3 为什么早停可能改善稳定性

若每一步都可能放大 $\Delta_t$，训练越久，单个样本的影响可能积累越多。早停因此既是优化选择，也可能是稳定性正则。

但“训练越短一定泛化越好”也不成立：过早停止会增加 optimization bias；非凸、非光滑或自适应训练的递推可能根本不收缩。稳定性 theorem 只在其更新和损失假设下成立。

## 3. 经验过程：为什么候选越多，越容易碰巧赢

对函数类 $\mathcal F$，一致收敛关心

$$
\sup_{f\in\mathcal F}
\left|
Pf-P_nf
\right|,
$$

其中

$$
Pf=\mathbb E f(Z),
\qquad
P_nf=\frac1n\sum_{i=1}^n f(Z_i).
$$

这里的 supremum 很关键：我们不是事先固定一个模型，而是允许训练过程在看过数据后从整个类里挑一个。候选越丰富，就越可能有人靠偶然噪声拿到很低的经验风险。

经验过程把这件事拆成一条标准流水线：

```text
总体减经验
→ ghost sample
→ Rademacher 随机符号
→ contraction / covering
→ global 或 local complexity
→ 高概率界或 fixed point
```

## 4. Ghost sample 与 symmetrization

引入独立同分布的 ghost sample

$$
S'=(Z_1',\ldots,Z_n').
$$

因为 $Pf=\mathbb E_{S'}P_n'f$，有

$$
\mathbb E_S\sup_{f\in\mathcal F}(Pf-P_nf)
\le
\mathbb E_{S,S'}
\sup_{f\in\mathcal F}(P_n'f-P_nf).
$$

右侧仍有两份样本。引入独立 Rademacher signs

$$
\sigma_i\in\lbrace-1,+1\rbrace,
\qquad \mathbb P(\sigma_i=1)=\frac12,
$$

利用 $(Z_i,Z_i')$ 的交换对称性，得到典型 symmetrization 界

$$
\mathbb E
\sup_{f\in\mathcal F}|Pf-P_nf|
\le
2\thinspace\mathbb E_S\widehat{\mathfrak R}^{\pm}_S(\mathcal F),
$$

这里为直接控制双侧偏差，定义对称经验 Rademacher complexity

$$
\widehat{\mathfrak R}^{\pm}_S(\mathcal F)
=\mathbb E_\sigma
\left[
\sup_{f\in\mathcal F}
\left|\frac1n\sum_{i=1}^n\sigma_i f(Z_i)\right|
\right].
$$

若采用不带绝对值的单侧定义，则先控制 $\sup_f(Pf-P_nf)$，另一侧对 $-\mathcal F$ 处理；两种记法的常数不能不加说明地混用。

直觉是：如果函数类连完全随机的正负号都能拟合得很好，它也更容易利用训练样本中的偶然波动。

## 5. Rademacher complexity 与 contraction

### 5.1 它测的是数据上的有效自由度

参数很多不自动等于 Rademacher complexity 大；关键是函数类在当前样本上能产生多少不同变化。例如线性类

$$
\mathcal F
=\lbrace x\mapsto\langle w,x\rangle:\Vert w\Vert_2\le B\rbrace,
\qquad \Vert x_i\Vert_2\le R,
$$

满足典型量级

$$
\widehat{\mathfrak R}^{\pm}_S(\mathcal F)
\lesssim \frac{BR}{\sqrt n}.
$$

这里真正起作用的是范数控制，而不只是维度或参数个数。

### 5.2 Contraction lemma：经过 Lipschitz loss 后复杂度怎样变

若标量函数 $\phi$ 是 $L$-Lipschitz，且采用满足相应中心化条件的 contraction 版本，则

$$
\widehat{\mathfrak R}^{\pm}_S(\phi\circ\mathcal F)
\lesssim
L\widehat{\mathfrak R}^{\pm}_S(\mathcal F).
$$

这条桥把“预测函数有多复杂”转成“loss 函数有多复杂”。对本文带绝对值的对称定义，安全版本允许一个 universal factor，常见写法是 $2L$；一因子版本需要单侧 convention、函数类对称/含零或相应中心化条件。使用时必须锁定所引用 theorem 的定义与常数。

## 6. Covering number 与 $\varepsilon$-net：用有限代表覆盖无限类

在度量 $d$ 下， $\varepsilon$-cover 是有限集合

$$
\lbrace f_1,\ldots,f_M\rbrace
$$

使每个 $f\in\mathcal F$ 都距某个代表不超过 $\varepsilon$。最小所需数量记为

$$
N(\varepsilon,\mathcal F,d).
$$

直觉像给一片连续地形铺网格：网格越细，需要的点越多。证明常分两步：

1. 对有限 net 中每个代表使用 concentration，再 union bound；
2. 用 $\varepsilon$ 控制任意函数与其代表之间的近似误差。

因此复杂度通常以

$$
\log N(\varepsilon,\mathcal F,d)
$$

出现。只用一个固定 $\varepsilon$ 可能粗糙；chaining/Dudley entropy integral 会同时使用多层网格，从粗到细逐层逼近。

边界：covering metric 必须与最终经验过程匹配。参数空间中很近，不保证函数输出在样本上也近；神经网络参数有重参数化对称性时尤其如此。

## 7. Uniform convergence 与 local complexity

### 7.1 Global uniform convergence

若以至少 $1-\delta$ 的概率

$$
\sup_{f\in\mathcal F}|Pf-P_nf|
\le \epsilon_n,
$$

则经验风险最小化器 $\widehat f$ 与类中最优 $f^\star$ 通常满足

$$
P\widehat f-Pf^\star
\le 2\epsilon_n
$$

（忽略优化误差）。两个 $\epsilon_n$ 分别用于把 $P\widehat f$ 拉到经验风险、再把经验最优和 $f^\star$ 接回总体风险。

但 global bound 要控制整个函数类，包括训练根本不会访问的糟糕区域，因此可能非常松。

### 7.2 Local Rademacher complexity

local complexity 只看一个与低风险、低方差或小 excess risk 相关的局部集合，例如

$$
\mathcal F(r)
=\lbrace f\in\mathcal F: P(f-f^\star)^2\le r\rbrace.
$$

若局部半径越小，复杂度也随之下降，就可以寻找 fixed point

$$
r_\star\approx \psi(r_\star),
$$

并获得快于粗糙 $1/\sqrt n$ 的 rate。常见证明还需要 Bernstein/margin/noise 条件、peeling 和 sub-root 性质。

“local”不是把 global 公式里的 $\mathcal F$ 随手换成一个小集合；必须证明学习器确实落在该集合，并处理这个集合本身的数据依赖。

## 8. PAC-Bayes：用 KL 支付数据依赖

### 8.1 Prior 与 posterior 在这里是什么意思

设 $P$ 是训练前固定、独立于当前训练样本的 hypothesis distribution， $Q=Q(S)$ 是看过数据后选择的 distribution。PAC-Bayes 中的 “posterior” 不一定是由真实 Bayesian likelihood 得到的后验；它可以是为证书设计的任意 $Q$。

对 Gibbs predictor 定义

$$
\widehat L_S(Q)
=\mathbb E_{h\sim Q}\widehat L_S(h),
\qquad
L_{\mathcal D}(Q)
=\mathbb E_{h\sim Q}L_{\mathcal D}(h).
$$

### 8.2 Donsker–Varadhan change of measure

若 $Q\ll P$，则对合适的 $f$：

$$
\mathbb E_Q[f]
\le
D_{\mathrm{KL}}(Q\Vert P)
+\log\mathbb E_P[e^f].
$$

直觉是：在 prior $P$ 下罕见、但在 posterior $Q$ 下常见的模型，需要支付 KL 价格。这条不等式把“对固定 $h$ 的指数矩界”搬到“数据依赖的整个 $Q$”。

若把 $f$ 换成 $\lambda f$，整理后会出现

$$
\frac{D_{\mathrm{KL}}(Q\Vert P)}{\lambda}
$$

与 log-MGF 项的权衡；温度 $\lambda$ 不是装饰常数。

### 8.3 一个常用 PAC-Bayes-kl 形式

若损失在 $[0,1]$、 $S\sim\mathcal D^n$、 $n\ge2$，且 prior $P$ 与 $S$ 独立，则以至少 $1-\delta$ 的概率，同时对所有 $Q\ll P$：

$$
\mathop{\mathrm{kl}}
\left(
\widehat L_S(Q)\thinspace\middle\Vert\thinspace L_{\mathcal D}(Q)
\right)
\le
\frac{
D_{\mathrm{KL}}(Q\Vert P)
+\log(2\sqrt n/\delta)
}{n}.
$$

左边是 Bernoulli KL，不是模型分布之间的 KL。Pinsker 可给更易读但更松的推论：

$$
L_{\mathcal D}(Q)
\le
\widehat L_S(Q)
+\sqrt{
\frac{D_{\mathrm{KL}}(Q\Vert P)+\log(2\sqrt n/\delta)}{2n}
}.
$$

不同 PAC-Bayes theorem 的常数、温度、loss transform 和允许的数据依赖 prior 不同；论文中必须锁定具体版本。

### 8.4 确定性网络不是自动的 Gibbs predictor

若 $P$ 是连续分布，而 $Q=\delta_w$ 是单点确定性网络，则常有

$$
D_{\mathrm{KL}}(\delta_w\Vert P)=+\infty.
$$

常见处理包括给权重加随机扰动、使用离散/压缩编码、证明从随机 predictor 到单模型的反随机化，或采用专门 deterministic PAC-Bayes 结果。不能把 Gibbs risk 的公式直接把 $Q$ 删掉。

## 9. Sampling without replacement：IID symmetrization 为什么会断

在 transductive learning 中，常先固定一个有限总体，再无放回地切成 train/test。此时样本之间有负相关，普通 IID ghost sample 并不存在。

正确证明可能使用：

- train/test exchange identity；
- permutation symmetry；
- without-replacement concentration；
- exponential Efron–Stein；
- transductive Rademacher complexity；
- peeling 与 local fixed point。

这就是 [R04](../../%E8%BF%91%E6%9C%9F%E9%A1%B6%E4%BC%9A%E7%90%86%E8%AE%BA%E6%A1%86%E6%9E%B6%EF%BC%882025-2026%EF%BC%89.md#r04-sampling-without-replacement%E4%BA%A4%E6%8D%A2%E6%95%8F%E6%84%9F%E5%BA%A6--efronstein--local-complexity) 的结构。会议版与 arXiv 长版可能有不同定理编号，而且部分结果要求 train/test size 明显不平衡；不能把 IID symmetrization 的每一步原样复制。

## 10. 三条路线怎样选择

| 路线 | 主要控制对象 | 优点 | 常见瓶颈 |
|---|---|---|---|
| Stability | 特定算法对单样本扰动的敏感度 | 能反映学习率、步数、早停和训练动态 | 长时间、非凸或不光滑训练的递推可能爆炸 |
| Empirical process | 整个函数类的经验—总体偏差 | 算法无关，可给 uniform guarantee | 为覆盖全类而非常保守；网络范数界易巨大 |
| PAC-Bayes | posterior $Q$ 相对 prior $P$ 的 KL | 允许数据依赖 $Q$，可利用压缩/随机化结构 | 好 prior 难构造；KL 和常数可能让界 vacuous |

也可以组合，但每条桥都要证明。例如 sample compression 可以帮助构造 PAC-Bayes prior/posterior；localized class 可以改善经验过程界；稳定性可以帮助判断某类泛化界是否可估计。不能只把三个复杂度项相加。

## 11. 为什么经典界对大模型经常很松

对 LLM/CV 大模型，理论界出现 `>1` 并不罕见，尤其当 loss 已在 $[0,1]$ 时，这叫 **vacuous bound**。常见原因包括：

1. **全局控制过强**：uniform convergence 要照顾所有参数，而训练只访问很窄的轨迹；
2. **层间范数连乘**：spectral/product norm bound 随深度迅速膨胀；
3. **posterior KL 巨大**：数十亿维权重相对简单 prior 的移动代价很高；
4. **稳定性累积**：训练步数巨大，逐步敏感度相加后很松；
5. **有界损失假设不自然**：语言模型的 NLL 可无界，截断又会改变目标；
6. **数据不是理想 IID**：去重、课程排序、网页相关性、持续预训练和人类反馈会引入依赖；
7. **分布发生漂移**：同分布泛化界不控制部署分布变化；
8. **先验偷看数据**：为得到好数值而用训练数据调 prior，却仍套 data-independent-prior theorem；
9. **优化与选择未计入**：反复试超参数、checkpoint 和 benchmark 会产生额外选择偏差。

界很松不等于工具毫无价值。它仍可：

- 揭露 theorem 真正需要的假设；
- 比较两个算法的相对敏感度；
- 指导寻找压缩、局部化、低秩或数据依赖结构；
- 说明某种“解释大模型泛化”的论证还缺哪座桥。

但不能把“提供了一个解释视角”写成“已完整解释规模化神经网络为何泛化”。

## 12. 可运行 NumPy 实验：候选越多，训练集越容易出现幸运赢家

我们生成完全随机的二分类标签，并准备越来越多的随机线性分类器。因为标签与输入独立，每个固定分类器的真实风险都是 $0.5$；但从很多候选里选择训练误差最低者，会出现越来越漂亮的训练分数。

```python
import numpy as np

rng = np.random.default_rng(7)
n_train, n_test, d = 400, 20_000, 20
max_models = 4096
model_counts = [1, 8, 64, 512, 4096]
delta = 0.05

x_train = rng.normal(size=(n_train, d))
y_train = rng.integers(0, 2, size=n_train)

# 模型在看标签前生成，因此每个固定模型的真实错误率都是 1/2。
weights = rng.normal(size=(max_models, d))
train_prediction = (weights @ x_train.T > 0.0)
train_error = np.mean(train_prediction != y_train[None, :], axis=1)

x_test = rng.normal(size=(n_test, d))
y_test = rng.integers(0, 2, size=n_test)

rows = []
for m in model_counts:
    chosen = np.argmin(train_error[:m])
    selected_train = train_error[chosen]
    selected_test = np.mean((x_test @ weights[chosen] > 0.0) != y_test)

    # 对 M 个预先固定、[0,1] loss 的 Hoeffding + union-bound 半径。
    radius = np.sqrt(np.log(2.0 * m / delta) / (2.0 * n_train))
    uniform_gap = np.max(np.abs(train_error[:m] - 0.5))
    rows.append((m, selected_train, selected_test, uniform_gap, radius))

print("M    chosen_train  chosen_test  max_uniform_gap  union_radius")
for row in rows:
    print(f"{row[0]:4d} {row[1]:13.4f} {row[2]:12.4f} "
          f"{row[3]:16.4f} {row[4]:13.4f}")

chosen_train_curve = np.array([row[1] for row in rows])
chosen_test_curve = np.array([row[2] for row in rows])

# 候选集合嵌套，最小训练误差只能下降或不变。
assert np.all(np.diff(chosen_train_curve) <= 1e-12)
assert chosen_train_curve[-1] < chosen_train_curve[0]

# 新测试集揭示：幸运赢家的真实表现仍接近随机猜测。
assert np.all(np.abs(chosen_test_curve - 0.5) < 0.02)

# 这个固定随机种子下，所有经验风险都落在有限类 union bound 内。
for _, _, _, uniform_gap, radius in rows:
    assert uniform_gap <= radius
```

这段实验展示 selection effect，不证明 Rademacher 或 PAC-Bayes theorem：

- $M$ 增大时，最佳训练误差会下降；
- 被选中的模型在独立测试集仍接近 $0.5$；
- finite-class uniform bound 中出现 $\sqrt{\log M/n}$，正是在支付“从多少候选里挑赢家”的成本。

神经网络函数类不是一个简单有限集合；Rademacher、covering、compression 与 PAC-Bayes 是把这条直觉推广到结构化或无限类的不同办法。

## 13. 常见误区

1. **“训练误差是总体风险的无偏估计，所以训练后的模型也没问题。”** 对固定模型可以；训练输出依赖同一数据。
2. **“Stability 只有一种定义。”** replace/delete、uniform/on-average、parameter/loss、期望/高概率都不同。
3. **“参数距离小就一定 loss 差小。”** 还需要 loss 对参数或预测的 Lipschitz/平滑条件。
4. **“期望稳定性界后加 $\delta$ 就是高概率界。”** 需要额外 theorem。
5. **“Rademacher complexity 就是参数数量。”** 它还依赖函数值、范数约束和样本。
6. **“Symmetrization 对任何相关数据都成立。”** 标准版本依赖 IID/交换结构；无放回采样要重证。
7. **“Cover 参数空间就等于 cover 函数空间。”** 重参数化和非线性会破坏这种直觉。
8. **“Local complexity 只是把全类换成训练附近。”** 必须证明局部集合、fixed point 和进入该集合的事件。
9. **“PAC-Bayes posterior 必须是真 Bayesian posterior。”** 它是任意允许的数据依赖分布 $Q$。
10. **“Prior 可以先看训练集再说它是 prior。”** 标准 theorem 不允许；数据依赖 prior 需要专门版本并支付复杂度。
11. **“Gibbs predictor 的界自动属于权重均值网络。”** 预测非线性时二者不是同一对象。
12. **“界 vacuous，所以证明完全无意义。”** 数值证书与结构诊断是两种价值，但不能混写。
13. **“同分布泛化好就说明部署安全。”** distribution shift、选择偏差和反馈闭环是另外的问题。

## 14. 自测

1. 为什么固定 $h$ 的 concentration 不能直接应用于 $h=A(S)$？
2. Replace-one coupling 中为什么通常让两次训练共享算法随机性？
3. Uniform stability 与 on-average stability 的量词差在哪里？
4. 期望 stability-to-generalization 结论为什么不是高概率结论？
5. Ghost sample 在 symmetrization 中做了什么？
6. Rademacher signs 为什么能测出函数类拟合噪声的能力？
7. Contraction lemma 需要检查哪些 Lipschitz 与中心化条件？
8. Covering number 中 metric 选错会造成什么问题？
9. Global 与 local complexity 的控制区域有何区别？
10. Donsker–Varadhan 不等式中的 KL 在支付什么？
11. 为什么连续 prior 配单点 posterior 常导致 KL 无穷？
12. 无放回 train/test 划分为什么不能直接使用 IID ghost sample？
13. 大模型泛化界很松，可能是哪些项造成的？

## 权威来源

- Bousquet & Elisseeff, [Stability and Generalization](https://jmlr.org/papers/v2/bousquet02a.html), JMLR 2002。
- Hardt, Recht & Singer, [Train faster, generalize better: Stability of stochastic gradient descent](https://proceedings.mlr.press/v48/hardt16.html), ICML 2016。
- Mohri, Rostamizadeh & Talwalkar, *Foundations of Machine Learning*, 2nd ed., MIT Press, 2018：Rademacher complexity 与 uniform convergence。
- Shalev-Shwartz & Ben-David, *Understanding Machine Learning: From Theory to Algorithms*, Cambridge University Press, 2014。
- Bartlett & Mendelson, “Rademacher and Gaussian Complexities: Risk Bounds and Structural Results,” JMLR 2002。
- Bartlett, Bousquet & Mendelson, “Local Rademacher Complexities,” *Annals of Statistics*, 2005。
- van der Vaart & Wellner, *Weak Convergence and Empirical Processes*, Springer, 1996：covering、entropy 与经验过程的严格版本。
- McAllester, “A PAC-Bayesian Tutorial with A Dropout Bound,” 2013；Seeger, “PAC-Bayesian Generalisation Error Bounds for Gaussian Process Classification,” JMLR 2002。
- Catoni, *PAC-Bayesian Supervised Classification*, IMS, 2007。
- [PAC-Bayes + compression 核验卡](../../proof_ref/recent-accepted-2025-2026/generalization-bounds-via-meta-learned-model-representations-pac-2410.13577/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md)。
- [泛化界可估计性核验卡](../../proof_ref/core-theory-2026-09/which-algorithms-have-tight-generalization-bounds-2410.01969/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md)。
