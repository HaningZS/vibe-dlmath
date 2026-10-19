---
id: T38
type: proof-template
refined: 2026-09-28
status: self-contained-core
---

# T38. Compression, description length and generalization

[主题目录](README.md) · [PAC-Bayes](T05-pac-bayes-information.md)

## 复用契约

**输入对象**：预先固定的 decoder、允许的二进制码集合、每个码的长度，以及码对应的模型。

**输出结论**：在同一高概率事件上，短描述模型的总体风险由经验风险与码长控制。

必需假设：i.i.d. 数据、bounded loss、有效的 Kraft/计数条件；decoder 与未计费的 side information 不能偷看当前训练样本。

**失败例子**：把所有训练标签写入一个数据依赖 decoder，再只用 1 bit 指向它，不能按“1 bit 模型”计算泛化复杂度。

## 实例化时必须完成

- [ ] 明确需编码哪些内容：架构、权重精度、量化器、种子、选择索引等。
- [ ] 检查 decoder 和 side information 是否独立于当前证明使用的数据。
- [ ] 对压缩前模型的结论，单独加入压缩导致的 loss/预测扰动。
- [ ] 不把 sample-compression theorem、参数个数和比特码长混为同一个结果。

## 1. 为什么“参数少”还不够

一个实数参数在理想无限精度下可以存无限信息。反过来，大网络也可能有短的近似描述。

因此描述长度问的是：给定共同约定的解码器，接收方还需要多少 bits 才能重建这个候选模型？

## 2. 用码长分配失败概率

设允许码集合 $\mathcal C$ 是可数的 prefix-free code，长度 $L(c)$ 满足

$$
\sum_{c\in\mathcal C}2^{-L(c)}\leq1.
$$

decoder $D$ 预先固定，模型为 $h_c=D(c)$。每个固定模型的 $[0,1]$ loss 满足单侧 Hoeffding。

给码 $c$ 分配 $\delta_c=\delta2^{-L(c)}$，则

$$
\Pr\!\left(R(h_c)>\widehat R_S(h_c)+
\sqrt{\frac{L(c)\log2+\log(1/\delta)}{2n}}\right)
\leq\delta_c.
$$

对所有码 union bound，总失败概率至多为 $\delta$。因此可以在看完数据后选择码，结论仍同时覆盖它，因为 decoder 与允许码的规则早已固定。

## 3. 零训练分类误差时的更快形式

对 0–1 loss，若固定候选的真实错误率为 $r$，它在 $n$ 个独立样本上全对的概率是 $(1-r)^n\leq e^{-nr}$。

再次按码长分配失败概率，得到：以至少 $1-\delta$ 的概率，同时对所有经验错误为零的 $h_c$，

$$
R(h_c)\leq
\frac{L(c)\log2+\log(1/\delta)}{n}.
$$

这是 bounded coding family 加零经验错误下的保证，不是任意 deep-net 训练到 interpolation 就自动有 $1/n$ 泛化率。

## 4. 怎样接回未压缩网络

若 $\widetilde h$ 是压缩模型，上述界控制的是 $R(\widetilde h)$。还需一个合法关系，例如

$$
R(h)\leq R(\widetilde h)+\epsilon_{\rm compress}.
$$

要得到它，可以使用统一输出扰动与 loss Lipschitz 性；分类任务也可通过 margin 分析保证小扰动不改变多数预测。只有训练点上的扰动小，不足以控制总体风险差。

## 5. 与 sample compression 和 PAC-Bayes 的关系

Sample compression 从训练集中保存少量样本，再用 reconstruction map 重建模型。这些样本本身依赖训练数据，不能直接当作这里预先固定 decoder 的免费 side information；相应 theorem 要处理样本选择、重建与 held-out 点的依赖。

对于这里的离散码，可定义先验 $P(c)=2^{-L(c)}/Z$，其中 $0<Z\leq1$。确定码的 Dirac 后验相对该离散先验有有限 KL，可与 [T05](T05-pac-bayes-information.md) 连接。若先验是连续权重分布，Dirac 后验的 KL 则通常无穷大。

## 自测与来源

LoRA rank 低是否等于描述长度短？还需记录矩阵尺寸、精度、基座是否为独立 side information、adapter 选择与编码方式。

来源：[Stronger generalization bounds via compression](https://arxiv.org/abs/1802.05296)。本卡的 prefix-code 证明是基础原型，原论文对深网络的可压缩性与扰动控制有额外结构。

## 本地论文与前置工具

通用工具：P03, P05，见 [证明原语](../../通用证明原语.md)。

- [Stronger generalization bounds for deep nets via a compression approach](../../proof_ref/dl-core-2026-09/stronger-generalization-bounds-for-deep-nets-via-a-1802.05296/README.md)

## 经典与近期证明蒸馏

- [经典编码界与数据依赖解码器](../../extensions/%E7%BB%8F%E5%85%B8%E7%BC%96%E7%A0%81%E7%95%8C%E4%B8%8E%E6%95%B0%E6%8D%AE%E4%BE%9D%E8%B5%96%E8%A7%A3%E7%A0%81%E5%99%A8.md)
