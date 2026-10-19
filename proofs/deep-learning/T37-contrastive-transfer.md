---
id: T37
type: proof-template
refined: 2026-09-28
status: self-contained-core
---

# T37. Contrastive objectives and downstream transfer

[主题目录](README.md) · [风险分解](../generalization/T32-excess-risk-decomposition.md)

## 复用契约

**输入对象**：positive joint law、negative sampling、critic/encoder、损失与下游任务。

**输出结论**：在规定采样机制下的 InfoNCE 信息关系，或另有任务假设支持的 downstream guarantee。二者不是同一句话。

必需假设：下文使用一个 positive 与 $K-1$ 个独立 marginal negatives；相关 density/可积性允许 KL 分解。下游风险还需要标签与表示的联系。

**失败例子**：两个视图只共享高熵背景 ID，而任务标签与背景独立；表示保留背景可让配对容易，却完全不帮助预测标签。

## 实例化时必须完成

- [ ] 写出完整 joint law，注明 $K$ 包含正样本。
- [ ] 检查 negatives 是否真从 marginal 独立采样；hard mining/时间相关负例需重推。
- [ ] 明确 loss 只控制配对、信息还是任务风险。
- [ ] 下游 class、表示选择的数据依赖、样本划分和 approximation 分别处理。

## 1. 先把对比学习变成一道分类题

随机选 $I\sim\mathrm{Unif}\{1,\ldots,K\}$。取 $X\sim P_X$，令
$Y_I\sim P_{Y|X}$，其余 $Y_j$ 独立来自 $P_Y$。

任务是看到 $(X,Y_1,\ldots,Y_K)$ 后猜哪个位置是 positive。softmax critic 定义

$$
q_\theta(i\mid x,y_{1:K})
=\frac{\exp s_\theta(x,y_i)}
{\sum_j\exp s_\theta(x,y_j)},
\qquad
L_{\rm NCE}=\mathbb E[-\log q_\theta(I\mid X,Y_{1:K})].
$$

零知识均匀猜测的 loss 是 $\log K$，因此 $\log K-L_{\rm NCE}$ 描述相对随机猜测的信息收益。

此处 critic 参数 $\theta$ 固定，或条件于独立训练数据后再对新的评估样本取期望。不能让参数偷看当前 positive 索引，再把训练批次上的经验 loss 当作这个总体条件交叉熵。

## 2. 一条完整的 KL 证明

令 $P$ 为上述 joint law，$Q$ 为 $I$ 均匀、$X$ 独立、所有 $Y_j$ 都来自 marginal 的参考 law。
若互信息有限且所需绝对连续性成立，

$$
D_{\rm KL}(P\|Q)=I(X;Y).
$$

对索引 $I$ 与其余变量作 KL 分解：

$$
I(X;Y)
=I_P(I;X,Y_{1:K})
+D_{\rm KL}\!\left(P_{X,Y_{1:K}}\middle\|P_XP_Y^{\otimes K}\right).
$$

丢掉非负的第二项，再用 cross-entropy 不小于真实条件熵：

$$
I(X;Y)\geq\log K-H(I\mid X,Y_{1:K})
\geq\log K-L_{\rm NCE}.
$$

这是总体分布的关系，不是有限 minibatch 实现已经估准 MI 的保证。下界最多为 $\log K$，也可能为负而无信息。

更精确地令 $V=(X,Y_{1:K})$，可把差值写为两个非负项：

$$
I(X;Y)-(\log K-L_{\rm NCE})
=D_{\rm KL}(P_V\|P_XP_Y^{\otimes K})
+\mathbb E_{P_V}D_{\rm KL}(P_{I|V}\|q_\theta(\cdot|V)).
$$

因此，即使 critic 达到 Bayes 分类器，有限 $K$ 的下界仍可能不等于原始互信息；不能称它为自动无偏的 MI 估计。

## 3. 为什么这还不是下游保证

设 $S$ 是背景 ID，$Y$ 是独立公平标签。两个视图共享 $S$，但任务相关部分被增强删除。编码器只输出 $S$ 时，配对可利用大量共享信息，然而

$$
I(\mathrm{representation};Y)=0.
$$

任何只读该表示的分类器仍只能在期望上达到随机猜测水平。这说明“视图之间的信息”必须和任务需要的信息建立联系。

## 4. 怎样补上 transfer 的桥

可复用的路线包括：明确 latent-class/augmentation 假设；证明表示保留任务充分信息；或直接上界下游预测类的 approximation error。随后再处理有限下游样本的 estimation 和 optimization。

冻结的独立预训练 encoder 可使下游类较容易固定；若 encoder 用同一批标签或测试信息选过，不能只对最后一层套 [T33](../generalization/T33-uniform-convergence.md)。

训练 loss 小、防 collapse、线性可分、跨域泛化是不同结论。EMA 或 stop-gradient 也不是脱离架构的普适防坍塌定理。

## 5. 来源与范围

- [Contrastive Predictive Coding](https://arxiv.org/abs/1807.03748)：InfoNCE 的经典来源。
- [Contrastive representation 的理论分析](https://arxiv.org/abs/1902.09229)：在额外 latent-class 假设下连接下游任务。
- [Alignment 与 uniformity](https://arxiv.org/abs/2005.10242)：球面表示的另一种分析视角。

本卡对上面的采样 law 给出自包含证明；不把这些不同论文的假设合成一条万能 transfer 定理。

## 本地论文与前置工具

通用工具：P01, P05，见 [证明原语](../../通用证明原语.md)。

- [Representation Learning with Contrastive Predictive Coding](../../proof_ref/dl-core-2026-09/representation-learning-with-contrastive-predictive-coding-1807.03748/README.md)
- [A Theoretical Analysis of Contrastive Unsupervised Representation Learning](../../proof_ref/foundations-2026-09/a-theoretical-analysis-of-contrastive-unsupervised-representation-learning-1902.09229/README.md)
- [Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere](../../proof_ref/foundations-2026-09/understanding-contrastive-representation-learning-through-alignment-and-uniformi-2005.10242/README.md)
