---
type: note
domain: math/linear-algebra
status: active
reviewed: 2026-09-01
---

# 像与核问答

[kernel and image](kernel%20and%20image.md)
[Q2: 矩阵变换中的image和kernel](QA%20about%20image%20and%20kernel.md#q2-%E7%9F%A9%E9%98%B5%E5%8F%98%E6%8D%A2%E4%B8%AD%E7%9A%84image%E5%92%8Ckernel)
## Q1: 基于直线理解image
***那关于image，就比如一个变换是 1，1， 它的像是否就是x+1的那条直线，这个直线的维度是1吗***

你的问题有两部分，我来帮你拆解一下：
### 1. "它的像是否就是 $y=x+1$ 的那条直线？"

**答案是：不是。**

这是一个非常常见的误解。关键原因在于：

- 一个矩阵（线性变换）的 Image **必须**是一个**子空间 (subspace)**。

- 一个子空间**必须**包含**原点**（零向量）。


你提到的 $y=x+1$ 这条直线，当 $x=0$ 时，$y=1$。它经过点 $(0, 1)$，但**不经过原点 $(0, 0)$**。

因此，$y=x+1$ 这条线**不能**是任何矩阵的 Image。

---

### 2. 那么 "1, 1" 的 Image 是什么？

你说的“一个变换是 1, 1”有点模糊，但我猜你可能指的是一个与向量 $\begin{bmatrix} 1 \\ 1 \end{bmatrix}$ 相关的变换。

让我们来看一个最可能的例子：

假设我们有一个 $2 \times 1$ 的矩阵 $A = \begin{bmatrix} 1 \\ 1 \end{bmatrix}$。

这个矩阵 $A$ 定义了一个从 $\mathbb{R}^1$（一条数轴）到 $\mathbb{R}^2$（一个平面）的变换 $T$。

$T(x) = A \cdot x = \begin{bmatrix} 1 \\ 1 \end{bmatrix} [x] = \begin{bmatrix} x \\ x \end{bmatrix}$

这个变换的意思是：

- 你输入 $x=1$，它输出 $\begin{bmatrix} 1 \\ 1 \end{bmatrix}$。

- 你输入 $x=2$，它输出 $\begin{bmatrix} 2 \\ 2 \end{bmatrix}$。

- 你输入 $x=0$，它输出 $\begin{bmatrix} 0 \\ 0 \end{bmatrix}$。

- ... ...


它的 **Image** 就是所有可能的输出 $\begin{bmatrix} x \\ x \end{bmatrix}$ 的集合。

这个集合在 $\mathbb{R}^2$ 平面上是什么样的？它就是** $y=x$ 这条直线**。

这条 $y=x$ 的直线：

1. 是一个子空间（是的）。

2. **它通过原点** $(0, 0)$（是的）。

3. 它就是这个变换 $T$ 的 Image。


---

### 3. "这个直线的维度是1吗？"

**是的，绝对是！**

- 这个 Image（即 $y=x$ 这条直线）是由一个向量 $\begin{bmatrix} 1 \\ 1 \end{bmatrix}$ **张成 (span)** 的。

- 换句话说，这条线上的每一个点都可以表示为 $c \cdot \begin{bmatrix} 1 \\ 1 \end{bmatrix}$（其中 $c$ 是一个标量）。

- 这个 Image 的**基 (basis)** 是 $\left\{ \begin{bmatrix} 1 \\ 1 \end{bmatrix} \right\}$。

- **维度 (Dimension)** 就是基向量的个数。


因为基里只有一个向量，所以**维度是 1**。

### 总结

- $y=x+1$ **不是** Image，因为它不经过原点。

- 与 $\begin{bmatrix} 1 \\ 1 \end{bmatrix}$ 相关的变换，其 Image 是 $y=x$ 这条直线。

- $y=x$ 这条直线（作为一个子空间）的**维度是 1**。

## Q2: 矩阵变换中的image和kernel
***再给我举个例子，因为你目前设定的x是一个标量，x是否也可以是一个多维度的向量***
是的，$x$ 当然可以是多维向量，这也是矩阵变换 $T(x)=Ax$ 的一般情形。

我们来看一个 **$x$ 是多维向量**的例子。

### 例子：从 3D 空间到 3D 空间的投影

假设我们有一个 $3 \times 3$ 的矩阵 $A$。这意味着它接受一个 3 维向量 $x$ 作为输入，并输出一个 3 维向量 $b$。

$A \cdot x = b$

$\begin{bmatrix} ? & ? & ? \\ ? & ? & ? \\ ? & ? & ? \end{bmatrix} \begin{bmatrix} x_1 \\ x_2 \\ x_3 \end{bmatrix} = \begin{bmatrix} b_1 \\ b_2 \\ b_3 \end{bmatrix}$

让我们定义一个具体的变换 $T$：**它将 3D 空间中的任何点“压扁”或“投影”到 $xy$ 平面上**。

一个在 3D 空间中的点 $x = \begin{bmatrix} x \\ y \\ z \end{bmatrix}$，经过这个变换后，它的 $z$ 坐标会变成 0。

$T\left(\begin{bmatrix} x \\ y \\ z \end{bmatrix}\right) = \begin{bmatrix} x \\ y \\ 0 \end{bmatrix}$

那么实现这个变换的矩阵 $A$ 是什么呢？

$A = \begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0 \end{bmatrix}$

（你可以验证一下：$\begin{bmatrix} 1 & 0 & 0 \\ 0 & 1 & 0 \\ 0 & 0 & 0 \end{bmatrix} \begin{bmatrix} x \\ y \\ z \end{bmatrix} = \begin{bmatrix} (1 \cdot x + 0 \cdot y + 0 \cdot z) \\ (0 \cdot x + 1 \cdot y + 0 \cdot z) \\ (0 \cdot x + 0 \cdot y + 0 \cdot z) \end{bmatrix} = \begin{bmatrix} x \\ y \\ 0 \end{bmatrix}$。 正确！）

现在，我们来分析这个矩阵 $A$ 的 **Image** 和 **Kernel**：

---

### 1. 🚀 Image (像)

Image 是**所有可能的输出**的集合。

- 直观理解：

    无论你输入 3D 空间中的哪个向量（比如 $\begin{bmatrix} 3 \\ 4 \\ 5 \end{bmatrix}$ 或 $\begin{bmatrix} -1 \\ 10 \\ 999 \end{bmatrix}$），这个变换 $A$ 都会把它“压扁”。

    - $A \cdot \begin{bmatrix} 3 \\ 4 \\ 5 \end{bmatrix} = \begin{bmatrix} 3 \\ 4 \\ 0 \end{bmatrix}$

    - $A \cdot \begin{bmatrix} -1 \\ 10 \\ 999 \end{bmatrix} = \begin{bmatrix} -1 \\ 10 \\ 0 \end{bmatrix}$

    - $A \cdot \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix} = \begin{bmatrix} 1 \\ 2 \\ 0 \end{bmatrix}$


    所有这些输出向量有什么共同点？它们的第三个分量（$z$ 坐标）永远是 0。

    所有 $z$ 坐标为 0 的向量 $\begin{bmatrix} x \\ y \\ 0 \end{bmatrix}$ 组成了什么？

    它们组成了 $\mathbb{R}^3$ 空间中的 $xy$ 平面。

- 数学定义：

    Image 是 $A$ 的列空间。$A$ 的列向量是 $\begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}$, $\begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}$ 和 $\begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}$。

    $\text{Im}(A) = \text{span}\left(\begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}, \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}\right) = \text{span}\left(\begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix}\right)$

    这就是 $xy$ 平面的数学定义。

- 维度：

    这个 Image ( $xy$ 平面) 是由两个线性无关的基向量 $\left\{ \begin{bmatrix} 1 \\ 0 \\ 0 \end{bmatrix}, \begin{bmatrix} 0 \\ 1 \\ 0 \end{bmatrix} \right\}$ 张成的。

    所以，$\dim(\text{Im}(A)) = 2$。


---

### 2. 🎯 Kernel (核)

Kernel 是所有被变换到**零向量** $\begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}$ 的**输入** $x$ 的集合。

- 直观理解：

    我们需要找到所有的 $\begin{bmatrix} x \\ y \\ z \end{bmatrix}$ 使得 $A \begin{bmatrix} x \\ y \\ z \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}$。

    我们知道 $A \begin{bmatrix} x \\ y \\ z \end{bmatrix} = \begin{bmatrix} x \\ y \\ 0 \end{bmatrix}$。

    所以我们要求解 $\begin{bmatrix} x \\ y \\ 0 \end{bmatrix} = \begin{bmatrix} 0 \\ 0 \\ 0 \end{bmatrix}$。

    这组方程的解是：

    - $x = 0$

    - $y = 0$

    - $0 = 0$ (这个方程对 $z$ 没有任何限制！)


    所以，只要 $x=0$ 且 $y=0$，$z$ 可以是任何数。

    这些向量长什么样？它们长这样：$\begin{bmatrix} 0 \\ 0 \\ z \end{bmatrix}$。

    （例如 $\begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}$, $\begin{bmatrix} 0 \\ 0 \\ 5 \end{bmatrix}$, $\begin{bmatrix} 0 \\ 0 \\ -10 \end{bmatrix}$ 等）

    所有这些“被压扁后会消失”的向量组成了什么？

    它们组成了 $z$ 轴。

- 数学定义：

    $\text{Ker}(A) = \left\{ \begin{bmatrix} 0 \\ 0 \\ z \end{bmatrix} \mid z \in \mathbb{R} \right\} = \text{span}\left(\begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix}\right)$

- 维度：

    这个 Kernel ($z$ 轴) 是由一个基向量 $\left\{ \begin{bmatrix} 0 \\ 0 \\ 1 \end{bmatrix} \right\}$ 张成的。

    所以，$\dim(\text{Ker}(A)) = 1$。


---

### 总结这个例子

- **输入空间**：$\mathbb{R}^3$（3维空间）， $n=3$。

- **Image (像)**： $xy$ 平面。 维度 (Rank) = 2。

- **Kernel (核)**： $z$ 轴。 维度 (Nullity) = 1。


验证秩-零度定理：

$\dim(\text{Im}(A)) + \dim(\text{Ker}(A)) = 2 + 1 = 3 = n$ (输入空间的维度)

完全正确！
