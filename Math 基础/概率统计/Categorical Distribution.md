---
type: note
domain: math/probability
status: active
reviewed: 2026-09-01
---

# Categorical 分布

> [!tip] 学习位置
> 完整分布地图见 [常见概率分布与指数族](%E5%B8%B8%E8%A7%81%E6%A6%82%E7%8E%87%E5%88%86%E5%B8%83%E4%B8%8E%E6%8C%87%E6%95%B0%E6%97%8F.md)；概率与条件化基础见 [概率论主干：联合、条件、期望与协方差](%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md)。

[Definition](Categorical%20Distribution.md#definition)
[Example 与NLL, Cross Entropy](Categorical%20Distribution.md#example-%E4%B8%8Enll-cross-entropy)
[3. 与 Cross-Entropy (交叉熵) 的联系](Categorical%20Distribution.md#3-%E4%B8%8E-cross-entropy-%E4%BA%A4%E5%8F%89%E7%86%B5-%E7%9A%84%E8%81%94%E7%B3%BB)
## Definition
**Categorical 分布**（Categorical Distribution），又称**类别分布**或**多点分布**，是概率论中的一种离散概率分布。

简单来说，它描述了一个随机变量在 $k$ 个**互斥且有限**的类别中取值的概率。它是**伯努利分布（Bernoulli Distribution）**在多分类情况下的推广。

---

### 1. 核心定义

假设一个实验有 $k$ 种可能的结果（类别），每种结果出现的概率为 $p_1, p_2, \dots, p_k$。

- **参数约束**：

    - $p_i \in [0, 1]$

    - $\sum_{i=1}^{k} p_i = 1$


如果你掷一枚不均匀的骰子，六个面出现的概率各不相同，那么描述这枚骰子点数的分布就是一个 $k=6$ 的 Categorical 分布。

### 2. 数学表示

通常使用 **One-hot 向量** 来表示观测值 $x$。如果观测到了第 $i$ 类，则 $x$ 是一个第 $i$ 位为 1、其余位为 0 的向量： $x = (0, \dots, 1, \dots, 0)$。

其概率质量函数（PMF）可以写为：

$$f(x \mid \boldsymbol{p}) = \prod_{i=1}^{k} p_i^{x_i}$$

### 3. 与其他分布的关系

Categorical 分布是许多常用分布的“基石”：

|**关联分布**|**关系描述**|
|---|---|
|**Bernoulli 分布**|当 $k=2$ 时，Categorical 分布等同于伯努利分布（硬币正反面）。|
|**Multinomial 分布**|Categorical 是多项分布（Multinomial）在试验次数 $n=1$ 时的特例。就像伯努利分布之于二项分布。|
|**Softmax 函数**|在深度学习（如你的 LLM 领域）中，分类层输出的 Logits 经过 Softmax 后，得到的向量本质上就是 Categorical 分布的参数 $\boldsymbol{p}$。|

---

### 4. 在深度学习与 LLM 中的应用

在 **LLM 下一个词预测（Next Token Prediction）** 中：

1. 模型输出词表大小（Vocabulary Size）个 Logits。

2. 通过 `Softmax` 转化为概率分布。

3. 这个分布就是一个 **Categorical 分布**，其中 $k = \text{Vocab Size}$。

4. **采样（Sampling）**：当你使用 `top-p` 或 `temperature` 进行推理采样时，本质上是在根据这个 Categorical 分布抽取样本。


---

### 总结
Categorical 分布就是**“多选一”**的概率模型。


## Example 与NLL, Cross Entropy

我们可以用一个最直观的例子：**掷一枚不均匀（作弊）的四面体骰子**。

假设这枚骰子有四个面（ $k=4$），每个面出现的概率分布如下：

- $p_1 = 0.1$ （点数 1）

- $p_2 = 0.2$ （点数 2）

- $p_3 = 0.4$ （点数 3）

- $p_4 = 0.3$ （点数 4）


注意： $\sum p_i = 0.1 + 0.2 + 0.4 + 0.3 = 1.0$，符合概率约束。

---

### 1. 使用 One-hot 编码表示观测值

在 Categorical 分布中，我们通常不直接用标量 $x=3$，而是用 **One-hot 向量** $\boldsymbol{x}$。

如果这次实验的结果是 **3**，那么：

$$\boldsymbol{x} = [0, 0, 1, 0]$$

即 $x_1=0, x_2=0, x_3=1, x_4=0$。

### 2. 计算概率质量函数 (PMF)

Categorical 分布的 PMF 公式为：

$$f(\boldsymbol{x} \mid \boldsymbol{p}) = \prod_{i=1}^{k} p_i^{x_i}$$

我们将观测值 $\boldsymbol{x} = [0, 0, 1, 0]$ 代入公式：

$$P(\boldsymbol{x}=[0, 0, 1, 0]) = p_1^{0} \cdot p_2^{0} \cdot p_3^{1} \cdot p_4^{0}$$

根据指数幂运算规则（任何非零数的 0 次幂等于 1）：

$$P(\boldsymbol{x}=[0, 0, 1, 0]) = 1 \cdot 1 \cdot 0.4 \cdot 1 = 0.4$$

**结论**：观测到“点数 3”的概率就是 $p_3$。这个数学公式看起来繁琐，但在处理机器学习中的**损失函数**时非常有用。

---

### 3. 与 Cross-Entropy (交叉熵) 的联系

在你平时训练模型时，这个 PMF 就是计算 **NLL Loss (负对数似然)** 的基础。

如果我们对 PMF 取负对数：

$$-\log P(\boldsymbol{x}) = -\sum_{i=1}^{k} x_i \log p_i$$

因为 $x_i$ 只有在真实标签（Ground Truth）那一位是 1，其余都是 0，所以：

$$\text{Loss} = -\log p_{\text{target}}$$

这就是为什么你在做分类任务时，Loss 只取决于模型对“正确类别”预测出的那个概率值。

从 logits 到稳定的交叉熵实现，见 [CrossEntropy](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0/CrossEntropy.md)；从观测类别推断参数，见 [最大似然、MAP 与贝叶斯估计](%E6%9C%80%E5%A4%A7%E4%BC%BC%E7%84%B6%E3%80%81MAP%20%E4%B8%8E%E8%B4%9D%E5%8F%B6%E6%96%AF%E4%BC%B0%E8%AE%A1.md)。
