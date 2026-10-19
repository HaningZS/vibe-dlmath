---
id: T46
type: proof-template
refined: 2026-10-02
status: self-contained-core
---

# T46. Gaussian 机制、Rényi 散度与隐私组合

[主题目录](README.md) · [裁剪 T16](../optimization/T16-heavy-tail-clipping.md)

## 复用契约

**对象**：相邻数据集关系、机制 $M$ 和完整发布 transcript；Gaussian query $M(D)=q(D)+N(0,\sigma^2I)$，$q$ 的 $L^2$ sensitivity 为 $\Delta$。

**结论**：阶数 $\alpha>1$ 的 RDP 预算 $\rho_\alpha=\alpha\Delta^2/(2\sigma^2)$，统一条件预算的自适应组合，以及 $(\epsilon,\delta)$ 转换。这里不使用 subsampling amplification。

**条件**：query sensitivity 对每对相邻数据集成立；组合中每一步在同一已发布历史下满足条件预算；随机噪声与发布规则符合机制。

**失败例子**：给总梯度随便加噪声，但没有 sensitivity 界，无法得到上述预算。优化中的 gradient clipping 与 per-example DP clipping 也不是同一个对象。

## 实例化时必须完成

- [ ] 明确 replace-one/add-remove、样本级/用户级邻接与 normalization。
- [ ] 明确完整发布物，不能遗漏中间指标或数据依赖选择。
- [ ] 固定 clipping、Gaussian scale、每步预算和总步数。
- [ ] 若是 minibatch DP-SGD，用对应采样机制的 accountant 单独处理放大效应。

## 1. 直觉：一个人的替换，能把输出分布推多远

隐私限制的是两份只差一个人的数据，在算法输出分布上有多难区分。裁剪限制可移动的距离；噪声使这个移动难以辨认。多次发布则不断增加区分信息，需要累计预算。

这里的 $\epsilon$ 是分布可区分性参数，不是预测误差；隐私保证本身也不给优化或准确率。

## 2. Gaussian 散度的直接计算

定义 $D_\alpha(P\|Q)=(\alpha-1)^{-1}\log\mathbb E_P e^{(\alpha-1)L}$，其中 $L=\log(dP/dQ)$。
取 $P=N(\mu,\sigma^2I)$、$Q=N(\mu',\sigma^2I)$，$d=\mu-\mu'$，在 $P$ 下写 $Z=\mu+\sigma\xi$。有

$$
L(Z)=\frac{\|d\|^2}{2\sigma^2}+\frac{d^\top\xi}{\sigma},\qquad\xi\sim N(0,I).
$$

Gaussian MGF 得到
$\log\mathbb E_Pe^{(\alpha-1)L}=\alpha(\alpha-1)\|d\|^2/(2\sigma^2)$，故
$D_\alpha(P\|Q)=\alpha\|d\|^2/(2\sigma^2)$。交换两个均值后同一界仍成立。

## 3. 为什么自适应步骤仍能组合

完整历史的 log density ratio 可拆成每步条件 ratio 的和 $L_{1:T}=\sum_t L_t$。若对任意共同历史 $h$，

$$
\mathbb E_{P(\cdot|h)}e^{(\alpha-1)L_t}\le e^{(\alpha-1)\rho_t},
$$

则对最后一步条件化，再逐层积分，得到
$\mathbb E_Pe^{(\alpha-1)L_{1:T}}\le e^{(\alpha-1)\sum_t\rho_t}$。输出依赖之前发布物不破坏这条递推；只在平均历史上成立的预算则不够。

## 4. 转为普通 DP 的完整尾界

对总预算 $\rho$，取
$\epsilon=\rho+\log(1/\delta)/(\alpha-1)$。Markov 给出 $P(L>\epsilon)\le\delta$。任意输出事件 $E$ 因而满足

$$
P(E)\le e^\epsilon Q(E)+P(L>\epsilon)\le e^\epsilon Q(E)+\delta.
$$

对所有有向相邻对使用同一散度界，即得到 $(\epsilon,\delta)$-DP。可比较多个合法阶数的解析预算取最小值；数据驱动调参若另外发布则仍需记账。

## 5. full-batch clipping 的具体原型

初始化与原始数据独立。固定样本数 $n$，replace-one 邻接，每个样本梯度先裁到范数 $C$：
$q(D)=n^{-1}\sum_i\operatorname{clip}_C(g_i)$。在同一已发布参数历史下，只替换一个项，故 $\Delta\le2C/n$。

每步向平均梯度加标准差 $\sigma=zC/n$ 的噪声，则 $\rho_t=2\alpha/z^2$；$T$ 步预算为 $2T\alpha/z^2$。参数更新只使用这些带噪查询和与数据独立的随机性；最后参数是 noisy transcript 的后处理，不增加预算。若有另一个读取原始梯度的内部状态，也需重新证明它在相同发布历史下的条件 sensitivity。

这是 full-batch、固定大小、replace-one 的原型。add-remove、user-level、多步抽样和 Poisson minibatch 的常数/放大公式都要重新核对。把“抽了小 batch”直接乘一个采样率不构成证明。

## 前置、关联与证据

- [Gaussian 与指数族](<../../Math 基础/概率统计/常见概率分布与指数族.md>) · [MGF 与条件化](<../../Math 基础/概率统计/集中不等式、MGF、鞅与自归一化过程.md>)。
- [T16](../optimization/T16-heavy-tail-clipping.md) · [T05 信息泛化](../generalization/T05-pac-bayes-information.md)：Rényi 散度、KL 与泛化的量词分别检查。
- [RDP 原论文](https://arxiv.org/abs/1702.07476) · [本地卡](../../proof_ref/dl-specializations-2026-10/renyi-differential-privacy-1702.07476/README.md)。
- [DP-SGD 原论文](https://arxiv.org/abs/1607.00133) · [本地卡](../../proof_ref/dl-specializations-2026-10/deep-learning-with-differential-privacy-1607.00133/README.md)。本卡不重证其 subsampled accountant。
- [固定 RDP v3 的 scoped 核验记录](../../proof_ref/dl-specializations-2026-10/renyi-differential-privacy-1702.07476/核验笔记.md)，包含噪声标准差/方差的文字笔误辨析。

## 经典与近期证明蒸馏

- [T50：用指数距离上包络把观测证书接到总体期望，保持量词与选择预算。](../generalization/T50-data-dependent-certificate-envelope.md)
