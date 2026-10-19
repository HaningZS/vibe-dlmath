---
type: roadmap
domain: math
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# AI Researcher 高阶数学路线：LLM、CV 与生成模型

这条路线接在 [AI Researcher 数学学习路线](AI%20Researcher%20%E6%95%B0%E5%AD%A6%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md) 后面。它不是“数学越难越好”的课程表，而是专门补 LLM、CV 与现代生成模型论文里经常被默认掌握的桥梁。

先抓住总原则：

> 高阶数学的价值，不是让公式更华丽，而是把几个看似不同的模型放进同一个结构里，从而看清它们共享什么、差在哪里、结论需要哪些前提。

例如：

- CLIP 检索、attention 打分和度量学习都在问“两个表示怎样比较”；
- CNN、位置编码和 RoPE 都在处理“平移、频率或旋转下，信息怎样变化”；
- normalizing flow、diffusion 和 flow matching 都在研究“概率分布怎样沿变换或时间演化”；
- natural gradient、TRPO 和一部分二阶优化都在问“参数坐标变了以后，什么才算同样大小的一步”。

## 0. 进入高阶路线前的最低门槛

不要求先做完一本数学教材，但至少应能回答：

- 向量、矩阵、随机变量和函数的形状是什么，见 [向量空间、基、秩与 SVD](%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E5%90%91%E9%87%8F%E7%A9%BA%E9%97%B4%E3%80%81%E5%9F%BA%E3%80%81%E7%A7%A9%E4%B8%8E%20SVD.md)；
- 梯度、Jacobian 和 Hessian 分别近似什么，见 [导数、梯度、Jacobian、Hessian 与自动微分](%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E5%AF%BC%E6%95%B0%E3%80%81%E6%A2%AF%E5%BA%A6%E3%80%81Jacobian%E3%80%81Hessian%20%E4%B8%8E%E8%87%AA%E5%8A%A8%E5%BE%AE%E5%88%86.md)；
- 联合、条件、期望和 Bayes 在对谁求和或积分，见 [概率论主干：联合、条件、期望与协方差](%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md)；
- 局部线性化、梯度下降和数值误差各有什么边界，见 [梯度下降、学习率与收敛](%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E6%A2%AF%E5%BA%A6%E4%B8%8B%E9%99%8D%E3%80%81%E5%AD%A6%E4%B9%A0%E7%8E%87%E4%B8%8E%E6%94%B6%E6%95%9B.md)、[浮点数、数值稳定性与条件数](%E6%95%B0%E5%80%BC%E8%AE%A1%E7%AE%97/%E6%B5%AE%E7%82%B9%E6%95%B0%E3%80%81%E6%95%B0%E5%80%BC%E7%A8%B3%E5%AE%9A%E6%80%A7%E4%B8%8E%E6%9D%A1%E4%BB%B6%E6%95%B0.md)。

如果这些问题答不稳，先沿基础路线回退。高阶概念不会替你修复缺失的形状感和概率对象感。

## 1. 第一层：表示几何——模型眼里的“近”和“远”

### 1.1 范数、距离与相似度

先读 [范数、距离、相似度与度量学习](%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E8%8C%83%E6%95%B0%E3%80%81%E8%B7%9D%E7%A6%BB%E3%80%81%E7%9B%B8%E4%BC%BC%E5%BA%A6%E4%B8%8E%E5%BA%A6%E9%87%8F%E5%AD%A6%E4%B9%A0.md)。

它回答：

- 点积、余弦相似度和欧氏距离何时等价，何时完全不是一回事？
- embedding 归一化后，为什么最大余弦相似度等价于最小平方距离？
- Mahalanobis 距离为什么会按数据方差重新缩放方向？
- 对比学习中的 temperature 改变了几何，还是只改变了 logits 的尺度？

这层直接连接 [CLIP](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/CV%20%E5%9F%BA%E7%A1%80/%E8%A7%86%E8%A7%89%E8%AF%AD%E8%A8%80%E6%A8%A1%E5%9E%8B/CLIP.md)、[InfoNCE Loss](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0/InfoNCE%20Loss.md)、[NT-Xent Loss](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0/NT-Xent%20Loss.md)、[RAG embedding](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/LLM%20%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93/RAG/RAG%20embedding.md) 和 attention 打分。

### 1.2 高维几何与随机投影

再读 [高维几何、集中现象与随机投影](%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E9%AB%98%E7%BB%B4%E5%87%A0%E4%BD%95%E3%80%81%E9%9B%86%E4%B8%AD%E7%8E%B0%E8%B1%A1%E4%B8%8E%E9%9A%8F%E6%9C%BA%E6%8A%95%E5%BD%B1.md)。

高维空间不能只靠二维图想象：随机向量常近似正交，距离可能集中，样本协方差会在样本少、维度高时失真。它帮助理解：

- embedding 相似度为什么需要基线和归一化；
- 随机投影为什么可能在降维后近似保留距离；
- 谱离群值何时可能是信号，何时只是有限样本噪声；
- “维度高所以表达力强”为什么不是完整结论。

### 1.3 流形与切空间

[流形、切空间与 Riemannian 几何直觉](%E4%BF%A1%E5%8F%B7%E4%B8%8E%E5%87%A0%E4%BD%95/%E6%B5%81%E5%BD%A2%E3%80%81%E5%88%87%E7%A9%BA%E9%97%B4%E4%B8%8E%20Riemannian%20%E5%87%A0%E4%BD%95%E7%9B%B4%E8%A7%89.md) 把“局部像平面、整体可能弯曲”说清楚。它对球面归一化 embedding、旋转空间、姿态估计和 natural gradient 很有用。

这是 CV/3D/Embodied/信息几何方向的建议选修；纯 LLM 路线若暂时不研究球面优化、姿态或信息几何，可以先跳过，再在需要时回来。

注意：把数据称为“低维流形”通常是建模假设或经验直觉，不是对任意真实数据集已经证明的事实。

## 2. 第二层：矩阵微分——从论文公式走到可验证梯度

读 [矩阵微分、Trace Trick 与反向传播](%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E7%9F%A9%E9%98%B5%E5%BE%AE%E5%88%86%E3%80%81Trace%20Trick%20%E4%B8%8E%E5%8F%8D%E5%90%91%E4%BC%A0%E6%92%AD.md)。

基础自动微分笔记告诉你链式法则怎样沿计算图传播；矩阵微分进一步回答：

- 为什么 $x^\top Ax$ 的梯度与 $A+A^\top$ 有关？
- 为什么 `trace` 能把矩阵表达式改写成便于求导的标量？
- softmax、attention、归一化和最小二乘的梯度形状怎样检查？
- 为什么“分子布局”和“分母布局”会让不同资料中的 Jacobian 看起来互为转置？

目标不是背一张导数表，而是能做到：先写微分，再用 trace 重排，最后用有限差分或自动微分检查。

### 2.1 期望里面有采样时，梯度从哪里来

[期望的梯度：重参数化、Score Function 与直通估计](%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%9C%9F%E6%9C%9B%E7%9A%84%E6%A2%AF%E5%BA%A6%EF%BC%9A%E9%87%8D%E5%8F%82%E6%95%B0%E5%8C%96%E3%80%81Score%20Function%20%E4%B8%8E%E7%9B%B4%E9%80%9A%E4%BC%B0%E8%AE%A1.md) 处理普通链式法则不够用的情形：目标是 $\nabla_\theta\mathbb E_{X\sim p_\theta}[f(X)]$，但样本 $X$ 的分布本身依赖参数。

- pathwise / reparameterization：把随机性搬到与参数无关的基础噪声上，再沿可微路径反传；
- score-function / REINFORCE：用 $f(X)\nabla_\theta\log p_\theta(X)$ 构造在适当条件下无偏、但常高方差的估计；
- baseline / control variate：在不改变期望的前提下降低方差；
- straight-through：前向用离散值、反向借用另一个导数，一般有偏，属于工程估计器而非真实导数。

这条桥连接 VAE/ELBO、Gumbel–Softmax、policy gradient、Actor–Critic 与 RLHF。

## 3. 第三层：频率与对称性——CV 和位置机制的共同语言

### 3.1 复数、傅里叶、卷积

[复数、傅里叶变换、卷积与频域](%E4%BF%A1%E5%8F%B7%E4%B8%8E%E5%87%A0%E4%BD%95/%E5%A4%8D%E6%95%B0%E3%80%81%E5%82%85%E9%87%8C%E5%8F%B6%E5%8F%98%E6%8D%A2%E3%80%81%E5%8D%B7%E7%A7%AF%E4%B8%8E%E9%A2%91%E5%9F%9F.md) 从“用不同快慢的旋转指针拆信号”开始，连接：

- 卷积定理与 CNN；
- 低频/高频、模糊和边缘；
- 正弦位置编码与频率；
- RoPE 中二维旋转块为何能把相对位置信息带入点积。

傅里叶视角可以解释机制，但不能单独证明一个 Transformer 会怎样使用位置，也不能把所有神经网络都简化成线性频率滤波器。

### 3.2 群、表示与等变性

[对称性、群表示与等变网络](%E4%BF%A1%E5%8F%B7%E4%B8%8E%E5%87%A0%E4%BD%95/%E5%AF%B9%E7%A7%B0%E6%80%A7%E3%80%81%E7%BE%A4%E8%A1%A8%E7%A4%BA%E4%B8%8E%E7%AD%89%E5%8F%98%E7%BD%91%E7%BB%9C.md) 区分两个常被混用的词：

- **不变**：输入变了，输出保持不变；
- **等变**：输入按某种方式变，输出按可预测的对应方式变。

普通卷积天然对应平移等变；旋转、反射、置换和三维刚体运动需要明确所选群以及输入/输出怎样表示。它连接 CNN、Deep Sets、图网络、分子模型和视觉数据增强。

## 4. 第四层：概率密度怎样随变换移动

先读 [积分、变量替换与概率密度变换](%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E7%A7%AF%E5%88%86%E3%80%81%E5%8F%98%E9%87%8F%E6%9B%BF%E6%8D%A2%E4%B8%8E%E6%A6%82%E7%8E%87%E5%AF%86%E5%BA%A6%E5%8F%98%E6%8D%A2.md)。

如果把一块橡皮泥拉伸两倍，同样的概率质量会摊在更大体积上，所以密度必须下降。Jacobian determinant 正是在记录局部体积被放大或压缩多少。

这条线连接：

- 一维随机变量变换；
- 多维 change-of-variables；
- normalizing flows 与精确 likelihood；
- 连续时间下的瞬时变量替换公式。

必须分清：Jacobian 矩阵描述局部线性变换，determinant 描述有向体积缩放；非方阵、不可逆映射或多对一映射不能机械套普通可逆公式。

## 5. 第五层：连续时间动力学——diffusion 与 flow 的数学底座

读 [ODE、SDE 与连续时间生成模型](%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/ODE%E3%80%81SDE%20%E4%B8%8E%E8%BF%9E%E7%BB%AD%E6%97%B6%E9%97%B4%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B.md)，再回看 [扩散模型、Score Matching 与 Flow Matching](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B/%E6%89%A9%E6%95%A3%E6%A8%A1%E5%9E%8B%E3%80%81Score%20Matching%20%E4%B8%8E%20Flow%20Matching.md)。

- ODE：给定初值后，向量场决定一条确定轨迹；
- SDE：在漂移之外加入随机扩散，同一初值可产生不同轨迹；
- continuity equation / Fokker–Planck：不追踪单个样本，而追踪整个概率密度怎样流动；
- probability-flow ODE：在合适条件和理想 score 下，可以与某个 SDE 共享同一族边缘分布，但单条路径不相同。

Flow Matching 的“simulation-free training”通常是指训练时无需反复模拟待学习 ODE 才获得监督目标，不表示生成时完全不需要 ODE 求解，也不表示模型没有随机初始噪声。

## 6. 第六层：分布之间的几何

### 6.1 最优传输与 Wasserstein

[最优传输与 Wasserstein 距离](%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%9C%80%E4%BC%98%E4%BC%A0%E8%BE%93%E4%B8%8E%20Wasserstein%20%E8%B7%9D%E7%A6%BB.md) 把分布比较想成搬土：一个分布是一堆土，另一个分布是目标地形，代价取决于搬多少和搬多远。

它连接 WGAN、Sinkhorn、domain adaptation、matching 与某些 flow path。需要特别警惕：

- Wasserstein 距离与 KL 衡量的不是同一种差异；
- mini-batch OT 不是总体 OT 的无偏替代；
- WGAN critic 给的是 Kantorovich 对偶中的函数优化，不是普通二分类器；
- “OT 路径更直”依赖成本、耦合和具体构造，不是所有生成模型的免费保证。

### 6.2 Fisher 信息与自然梯度

[Fisher 信息、自然梯度与信息几何](%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/Fisher%20%E4%BF%A1%E6%81%AF%E3%80%81%E8%87%AA%E7%84%B6%E6%A2%AF%E5%BA%A6%E4%B8%8E%E4%BF%A1%E6%81%AF%E5%87%A0%E4%BD%95.md) 把参数空间中的步长改成“模型分布实际改变了多少”。

普通梯度依赖参数坐标的刻度；自然梯度使用 Fisher 信息作为局部度量。它连接 maximum likelihood、Cramér–Rao、natural policy gradient、TRPO、K-FAC 与分布空间的局部 KL 几何。

Fisher、Hessian、Gauss–Newton 和 empirical Fisher 彼此相关，但不能默认相等。

## 7. LLM 常见问题的数学回退表

| 研究问题 | 数学入口 |
|---|---|
| attention 为什么除以 $\sqrt d$，高维点积会怎样缩放 | [高维几何、集中现象与随机投影](%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E9%AB%98%E7%BB%B4%E5%87%A0%E4%BD%95%E3%80%81%E9%9B%86%E4%B8%AD%E7%8E%B0%E8%B1%A1%E4%B8%8E%E9%9A%8F%E6%9C%BA%E6%8A%95%E5%BD%B1.md) |
| cosine、dot product 与检索距离如何选择 | [范数、距离、相似度与度量学习](%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E8%8C%83%E6%95%B0%E3%80%81%E8%B7%9D%E7%A6%BB%E3%80%81%E7%9B%B8%E4%BC%BC%E5%BA%A6%E4%B8%8E%E5%BA%A6%E9%87%8F%E5%AD%A6%E4%B9%A0.md) |
| attention / norm / loss 的矩阵梯度怎样检查 | [矩阵微分、Trace Trick 与反向传播](%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E7%9F%A9%E9%98%B5%E5%BE%AE%E5%88%86%E3%80%81Trace%20Trick%20%E4%B8%8E%E5%8F%8D%E5%90%91%E4%BC%A0%E6%92%AD.md) |
| 正弦位置编码、RoPE 的旋转和频率直觉 | [复数、傅里叶变换、卷积与频域](%E4%BF%A1%E5%8F%B7%E4%B8%8E%E5%87%A0%E4%BD%95/%E5%A4%8D%E6%95%B0%E3%80%81%E5%82%85%E9%87%8C%E5%8F%B6%E5%8F%98%E6%8D%A2%E3%80%81%E5%8D%B7%E7%A7%AF%E4%B8%8E%E9%A2%91%E5%9F%9F.md) |
| 没有位置机制的 self-attention 为什么是置换等变 | [对称性、群表示与等变网络](%E4%BF%A1%E5%8F%B7%E4%B8%8E%E5%87%A0%E4%BD%95/%E5%AF%B9%E7%A7%B0%E6%80%A7%E3%80%81%E7%BE%A4%E8%A1%A8%E7%A4%BA%E4%B8%8E%E7%AD%89%E5%8F%98%E7%BD%91%E7%BB%9C.md) |
| TRPO、KL trust region、natural policy gradient | [Fisher 信息、自然梯度与信息几何](%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/Fisher%20%E4%BF%A1%E6%81%AF%E3%80%81%E8%87%AA%E7%84%B6%E6%A2%AF%E5%BA%A6%E4%B8%8E%E4%BF%A1%E6%81%AF%E5%87%A0%E4%BD%95.md) |
| VAE 重参数化、REINFORCE、Gumbel 或 straight-through | [期望的梯度：重参数化、Score Function 与直通估计](%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%9C%9F%E6%9C%9B%E7%9A%84%E6%A2%AF%E5%BA%A6%EF%BC%9A%E9%87%8D%E5%8F%82%E6%95%B0%E5%8C%96%E3%80%81Score%20Function%20%E4%B8%8E%E7%9B%B4%E9%80%9A%E4%BC%B0%E8%AE%A1.md) |
| embedding 是否真的位于某个语义流形 | [流形、切空间与 Riemannian 几何直觉](%E4%BF%A1%E5%8F%B7%E4%B8%8E%E5%87%A0%E4%BD%95/%E6%B5%81%E5%BD%A2%E3%80%81%E5%88%87%E7%A9%BA%E9%97%B4%E4%B8%8E%20Riemannian%20%E5%87%A0%E4%BD%95%E7%9B%B4%E8%A7%89.md) 中的假设边界 |

## 8. CV 与生成模型常见问题的数学回退表

| 研究问题 | 数学入口 |
|---|---|
| 卷积为什么对应频域相乘，模糊为何压低高频 | [复数、傅里叶变换、卷积与频域](%E4%BF%A1%E5%8F%B7%E4%B8%8E%E5%87%A0%E4%BD%95/%E5%A4%8D%E6%95%B0%E3%80%81%E5%82%85%E9%87%8C%E5%8F%B6%E5%8F%98%E6%8D%A2%E3%80%81%E5%8D%B7%E7%A7%AF%E4%B8%8E%E9%A2%91%E5%9F%9F.md) |
| 数据增强和等变架构有什么根本区别 | [对称性、群表示与等变网络](%E4%BF%A1%E5%8F%B7%E4%B8%8E%E5%87%A0%E4%BD%95/%E5%AF%B9%E7%A7%B0%E6%80%A7%E3%80%81%E7%BE%A4%E8%A1%A8%E7%A4%BA%E4%B8%8E%E7%AD%89%E5%8F%98%E7%BD%91%E7%BB%9C.md) |
| 旋转、姿态和单位球面 embedding 怎样优化 | [流形、切空间与 Riemannian 几何直觉](%E4%BF%A1%E5%8F%B7%E4%B8%8E%E5%87%A0%E4%BD%95/%E6%B5%81%E5%BD%A2%E3%80%81%E5%88%87%E7%A9%BA%E9%97%B4%E4%B8%8E%20Riemannian%20%E5%87%A0%E4%BD%95%E7%9B%B4%E8%A7%89.md) |
| normalizing flow 的 log-det 从哪里来 | [积分、变量替换与概率密度变换](%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E7%A7%AF%E5%88%86%E3%80%81%E5%8F%98%E9%87%8F%E6%9B%BF%E6%8D%A2%E4%B8%8E%E6%A6%82%E7%8E%87%E5%AF%86%E5%BA%A6%E5%8F%98%E6%8D%A2.md) |
| VAE 的 pathwise gradient 或离散潜变量怎样训练 | [期望的梯度：重参数化、Score Function 与直通估计](%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%9C%9F%E6%9C%9B%E7%9A%84%E6%A2%AF%E5%BA%A6%EF%BC%9A%E9%87%8D%E5%8F%82%E6%95%B0%E5%8C%96%E3%80%81Score%20Function%20%E4%B8%8E%E7%9B%B4%E9%80%9A%E4%BC%B0%E8%AE%A1.md) |
| diffusion 的 reverse SDE 和 probability-flow ODE 有何关系 | [ODE、SDE 与连续时间生成模型](%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/ODE%E3%80%81SDE%20%E4%B8%8E%E8%BF%9E%E7%BB%AD%E6%97%B6%E9%97%B4%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B.md) |
| WGAN 的 Wasserstein 与 KL/JS 有何差别 | [最优传输与 Wasserstein 距离](%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%9C%80%E4%BC%98%E4%BC%A0%E8%BE%93%E4%B8%8E%20Wasserstein%20%E8%B7%9D%E7%A6%BB.md) |
| 高维协方差谱、随机初始化为何需要谨慎解释 | [高维几何、集中现象与随机投影](%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E9%AB%98%E7%BB%B4%E5%87%A0%E4%BD%95%E3%80%81%E9%9B%86%E4%B8%AD%E7%8E%B0%E8%B1%A1%E4%B8%8E%E9%9A%8F%E6%9C%BA%E6%8A%95%E5%BD%B1.md) |

## 9. 建议的 11 周进阶节奏

| 周次 | 主题 | 最低成果 |
|---|---|---|
| 1 | 范数、相似度、度量学习 | 能解释归一化前后 dot/cosine/L2 的关系 |
| 2 | 矩阵微分与 trace trick | 手推二次型和线性层梯度，并做有限差分检查 |
| 3 | 高维几何与随机投影 | 模拟随机向量夹角和距离集中 |
| 4 | 复数、傅里叶与卷积 | 用 FFT 验证卷积定理并解释频谱 |
| 5 | 群、不变性与等变性 | 写出一个平移等变性的可执行检查 |
| 6 | 流形与切空间（方向选修） | 在球面上比较欧氏一步和切空间一步 |
| 7 | 变量替换与 normalizing flow | 手推一维密度变换和多维 log-det |
| 8 | 期望的梯度 | 比较 pathwise、REINFORCE 与 straight-through 的偏差—方差 |
| 9 | ODE、SDE 与连续时间生成 | 模拟 Euler 与 Euler–Maruyama，解释分布级差别 |
| 10 | 最优传输 | 在一维中用排序计算 Wasserstein 距离 |
| 11 | Fisher 与自然梯度 | 对 Bernoulli 模型比较普通梯度和自然梯度 |

## 10. 什么暂时不需要作为前置

这些方向有价值，但不应为了“显得高阶”强行前置：

- 完整测度论：做严格概率论或理论生成模型时再系统学；当前先把密度、积分和变量替换用准。
- 完整抽象代数：等变网络先掌握群作用和表示，不必先完成群论全部结构。
- 代数拓扑与微分拓扑：除非研究拓扑数据分析、几何深度学习或严格流形理论。
- 自由概率与完整随机矩阵理论：先掌握谱噪声、高维集中和有限样本边界。
- 泛函分析全套：只有研究算子、PDE、无限维优化或核方法理论时再深入。

## 11. 掌握标准

每个高阶概念至少通过四关：

1. **能画出对象**：知道研究的是点、向量、变换、分布还是路径。
2. **能说变换规律**：输入变了，长度、体积、概率或输出怎样变。
3. **能写最小例子**：用二维、有限群、一维分布或简单 ODE 验证。
4. **能说适用边界**：指出可逆性、光滑性、独立性、对称性或高维渐近条件。

## 12. 当目标从“读懂模型”变成“读懂证明”

本路线主要解释模型中的高阶数学对象；它不自动覆盖 PAC-Bayes、martingale concentration、Fano lower bound、matrix perturbation 或 PDE error proof。需要复现理论论文时，继续进入 [AI 理论证明前置学习路线](%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/AI%20%E7%90%86%E8%AE%BA%E8%AF%81%E6%98%8E%E5%89%8D%E7%BD%AE%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)，并使用 [数学前置与论文证明导航](../%E6%95%B0%E5%AD%A6%E5%89%8D%E7%BD%AE%E4%B8%8E%E8%AE%BA%E6%96%87%E8%AF%81%E6%98%8E%E5%AF%BC%E8%88%AA.md) 从数学笔记跳到 T/P/R 模板、核验卡和本地 PDF 页码。

从 [Math 基础目录](Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md) 进入各阶段；本轮新增内容与改动明细记录在 [2026-09-01 知识框架补全与前沿更新目录](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/2026-09-01%20%E7%9F%A5%E8%AF%86%E6%A1%86%E6%9E%B6%E8%A1%A5%E5%85%A8%E4%B8%8E%E5%89%8D%E6%B2%BF%E6%9B%B4%E6%96%B0%E7%9B%AE%E5%BD%95.md)。

## 来源入口

- Deisenroth, Faisal & Ong, [*Mathematics for Machine Learning*](https://mml-book.github.io/)
- Vershynin, [*High-Dimensional Probability*](https://www.math.uci.edu/~rvershyn/papers/HDP-book/HDP-book.html)
- Bronstein et al., [Geometric Deep Learning](https://arxiv.org/abs/2104.13478)
- Chen et al., [Neural Ordinary Differential Equations](https://arxiv.org/abs/1806.07366)
- Song et al., [Score-Based Generative Modeling through SDEs](https://arxiv.org/abs/2011.13456)
- Lipman et al., [Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747)
- Peyré & Cuturi, [*Computational Optimal Transport*](https://arxiv.org/abs/1803.00567)
- Amari, *Information Geometry and Its Applications*, Springer, 2016.
