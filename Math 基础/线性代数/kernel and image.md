---
type: note
domain: math/linear-algebra
status: active
reviewed: 2026-09-01
---

# 像与核（Image and Kernel）

[QA about image and kernel](QA%20about%20image%20and%20kernel.md)
[QA about image and kernel](QA%20about%20image%20and%20kernel.md#q2-%E7%9F%A9%E9%98%B5%E5%8F%98%E6%8D%A2%E4%B8%AD%E7%9A%84image%E5%92%8Ckernel)

这是一个线性代数中的核心概念。简而言之：

- **Image (像)**：矩阵“能去哪里”。

- **Kernel (核)**：矩阵“能把什么变成零”。


下面是更详细的解释：

一个 $m \times n$ 的矩阵 $A$ 可以看作一个从 $n$ 维空间 $\mathbb{R}^n$ (输入) 到 $m$ 维空间 $\mathbb{R}^m$ (输出) 的**线性变换**（函数）。

$T(x) = Ax$

其中 $x$ 是 $\mathbb{R}^n$ 中的一个 $n$ 维向量， $Ax$ 是 $\mathbb{R}^m$ 中的一个 $m$ 维向量。

---

### 1. 🚀 Image (像)

Image（也称为 **Column Space / 列空间** 或 **Range / 值域**）是所有可能的**输出**向量的集合。

换句话说，它是由 $A$ 的所有列向量“张成”（span）的空间。

- 直观理解：

    如果你把 $\mathbb{R}^n$ 中所有可能的向量 $x$ 都代入 $Ax$ 中，你得到的所有结果 $b$ 组成的集合，就是 $A$ 的 Image。

- 数学定义：

    $\text{Im}(A) = \lbrace b \in \mathbb{R}^m \mid b = Ax \text{ 对于某个 } x \in \mathbb{R}^n \rbrace$

- 如何找到：

    Image 就是 $A$ 的列空间。可以对 $A$ 做行消元来寻找**主元列的位置**，再从原矩阵 $A$ 中取出这些位置对应的列作为列空间的一组基。行变换一般会改变列空间，不能直接把行最简矩阵的非零列当作原列空间的基。

- 维度：

    Image 的维度被称为矩阵的秩 (Rank)。


---

### 2. 🎯 Kernel (核)

Kernel（也称为 **Null Space / 零空间**）是所有被矩阵 $A$ 映射到**零向量**的**输入**向量的集合。

- 直观理解：

    Kernel 回答了这个问题：“哪些输入向量 $x$ 经过 $Ax$ 变换后会‘消失’（变成零向量）？”

- 数学定义：

    $\text{Ker}(A) = \lbrace x \in \mathbb{R}^n \mid Ax = 0 \rbrace$

- 如何找到：

    Kernel 就是齐次线性方程组 $Ax = 0$ 的所有解。你通过高斯消元法解这个方程组得到的解空间，就是 Kernel。

- 维度：

    Kernel 的维度被称为零度 (Nullity)。


---

### 💡 总结与关联

这两个概念是相关的，它们的关系由**秩-零度定理 (Rank-Nullity Theorem)** 描述：

$$\dim(\text{Im}(A)) + \dim(\text{Ker}(A)) = n$$

$$(\text{秩}) + (\text{零度}) = (\text{输入空间的维度，即矩阵的列数})$$

这个定理告诉我们，输入空间（ $n$ 维）被分成了两部分：

1. 一部分（Kernel）在变换中“塌缩”成了零。

2. 选择任意一个与 Kernel 直和组成输入空间的补空间后，变换在该补空间上与 Image 一一对应。补空间通常不唯一；给定内积时常选正交补 $\ker(A)^\perp$。


投影、最小二乘和伪逆怎样利用像空间与核空间，见 [投影、最小二乘与伪逆](%E6%8A%95%E5%BD%B1%E3%80%81%E6%9C%80%E5%B0%8F%E4%BA%8C%E4%B9%98%E4%B8%8E%E4%BC%AA%E9%80%86.md)。
