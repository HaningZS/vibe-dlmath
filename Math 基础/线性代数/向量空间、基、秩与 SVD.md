---
type: note
domain: math/linear-algebra
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# 向量空间、基、秩与 SVD

这篇笔记补齐线性代数的主干。先抓住一句话：

> 向量是可以被组合的对象；基是一套不重复的“坐标尺”；矩阵描述线性变换；秩表示变换真正保留了多少个独立方向；SVD 则把任意矩阵拆成“旋转—缩放—再旋转”。

## 知识依赖与相关笔记

- 读完本篇后再看：[像与核](kernel%20and%20image.md#1--image-%E5%83%8F)、[可逆矩阵](%E9%80%86%E7%9F%A9%E9%98%B5.md#%E5%AE%9A%E4%B9%89)、[特征值与特征向量](eigenvalue%20and%20eigenvector.md#-%E6%A0%B8%E5%BF%83%E5%AE%9A%E4%B9%89)、[正交矩阵](Orthogonal%20Matrix.md#%E5%AE%9A%E4%B9%89)。
- SVD 的应用见：[SVD、低秩与伪逆](%E6%AD%A3%E4%BA%A4%E7%9F%A9%E9%98%B5%E7%9A%84%E5%BA%94%E7%94%A8%E4%BB%A5%E5%8F%8A%E5%93%88%E8%BE%BE%E7%8E%9B%E7%9F%A9%E9%98%B5.md#svd)。
- 从“投影到子空间”走到可计算解，见 [投影、最小二乘与伪逆](%E6%8A%95%E5%BD%B1%E3%80%81%E6%9C%80%E5%B0%8F%E4%BA%8C%E4%B9%98%E4%B8%8E%E4%BC%AA%E9%80%86.md)；从方向缩放走到曲率，见 [二次型、正定矩阵与谱](%E4%BA%8C%E6%AC%A1%E5%9E%8B%E3%80%81%E6%AD%A3%E5%AE%9A%E7%9F%A9%E9%98%B5%E4%B8%8E%E8%B0%B1.md)。
- 数据中的内积和协方差见：[协方差矩阵](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md#6-%E6%96%B9%E5%B7%AE%E5%8D%8F%E6%96%B9%E5%B7%AE%E4%B8%8E%E7%9B%B8%E5%85%B3%E7%B3%BB%E6%95%B0)、[Gram 矩阵](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%A8%A1%E5%9E%8B%E5%8E%8B%E7%BC%A9/%E5%8D%8F%E6%96%B9%E5%B7%AE%E4%B8%8E%E7%89%B9%E5%BE%81%E5%85%B1%E5%90%8C%E5%BC%BA%E5%BA%A6-SparseGPT%E7%9A%84%E5%90%AF%E5%8F%91.md#gram-%E7%9F%A9%E9%98%B5)。
- 张量计算见：[矩阵乘法与 einsum](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0%E5%B7%A5%E7%A8%8B/PyTorch/Einsum.md#1-%E7%9F%A9%E9%98%B5%E4%B9%98%E6%B3%95-matrix-multiplication)。
- 梯度和神经网络中的线性层见：[导数、梯度、Jacobian、Hessian 与自动微分](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E5%AF%BC%E6%95%B0%E3%80%81%E6%A2%AF%E5%BA%A6%E3%80%81Jacobian%E3%80%81Hessian%20%E4%B8%8E%E8%87%AA%E5%8A%A8%E5%BE%AE%E5%88%86.md)、[神经网络训练闭环：前向、反向与优化](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0%E5%B7%A5%E7%A8%8B/PyTorch/%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C%E8%AE%AD%E7%BB%83%E9%97%AD%E7%8E%AF%EF%BC%9A%E5%89%8D%E5%90%91%E3%80%81%E5%8F%8D%E5%90%91%E4%B8%8E%E4%BC%98%E5%8C%96.md)。
- 理论可逆与实际可靠之间的差别见 [浮点数、数值稳定性与条件数](../%E6%95%B0%E5%80%BC%E8%AE%A1%E7%AE%97/%E6%B5%AE%E7%82%B9%E6%95%B0%E3%80%81%E6%95%B0%E5%80%BC%E7%A8%B3%E5%AE%9A%E6%80%A7%E4%B8%8E%E6%9D%A1%E4%BB%B6%E6%95%B0.md)。

## 1. 向量不只是“一列数字”

向量可以表示位置、速度、模型参数或一条样本的特征。真正重要的是：向量可以相加，也可以乘标量，而且结果仍在同一个集合中。

给定向量 $v_1,\ldots,v_k$，形如

$$
c_1v_1+\cdots+c_kv_k
$$

的表达式叫作**线性组合**。所有线性组合构成的集合叫作它们的**张成空间**：

$$
\operatorname{span}(v_1,\ldots,v_k).
$$

例如，平面中的两个不共线向量能张成整个平面；两个共线向量仍只能张成一条直线。

### 子空间的最低检查

一个集合要成为向量子空间，至少必须：

1. 包含零向量；
2. 对向量加法封闭；
3. 对标量乘法封闭。

所以不经过原点的直线一般不是线性子空间。这也是 [为什么 $y=x+1$ 不能成为线性变换的像](QA%20about%20image%20and%20kernel.md#q1-%E5%9F%BA%E4%BA%8E%E7%9B%B4%E7%BA%BF%E7%90%86%E8%A7%A3image) 的根本原因。

## 2. 线性无关、基与维数

若

$$
c_1v_1+\cdots+c_kv_k=0
$$

只有零解 $c_1=\cdots=c_k=0$，则这些向量**线性无关**。直觉上，没有哪个向量能由其他向量拼出来，因此没有重复方向。

一组向量若既线性无关，又能张成整个空间，就是这个空间的一组**基**。基的作用像坐标尺：选定基后，每个向量都有唯一坐标。

- 同一个空间可以有很多组基；
- 任何一组基所含向量数相同，这个数就是空间的**维数**；
- 换基改变坐标表示，不改变向量本身。

标准基只是最熟悉的一组基，不是唯一正确的基。PCA、傅里叶变换和 Hadamard 变换都可以理解成选择更有用的坐标系。

## 3. 矩阵是线性变换的坐标表示

设 $A\in\mathbb R^{m\times n}$。它把输入 $x\in\mathbb R^n$ 映射为输出 $Ax\in\mathbb R^m$：

$$
T(x)=Ax.
$$

如果把 $A$ 的列写成 $a_1,\ldots,a_n$，则

$$
Ax=x_1a_1+\cdots+x_na_n.
$$

因此，$A$ 的所有可能输出就是它的列向量张成的空间，即 [列空间或像](kernel%20and%20image.md#1--image-%E5%83%8F)。

与之对应，[核或零空间](kernel%20and%20image.md#2--kernel-%E6%A0%B8) 是所有满足 $Ax=0$ 的输入。核中的方向经过变换后完全消失。

## 4. 秩：真正保留下来的独立方向数

矩阵的秩是列空间的维数，也等于行空间的维数：

$$
\operatorname{rank}(A)=\dim\operatorname{Im}(A).
$$

秩不是“非零元素的数量”，而是独立信息方向的数量。秩—零度定理给出：

$$
\operatorname{rank}(A)+\dim\ker(A)=n,
$$

其中 $n$ 是输入空间维数。它说明输入方向只有两种去向：要么被保留到像空间中，要么落入核中而丢失。

对 $n\times n$ 方阵，下列说法等价：

- 满秩，即 $\operatorname{rank}(A)=n$；
- $\ker(A)=\{0\}$；
- $Ax=b$ 对每个 $b$ 都有唯一解；
- $A$ 可逆。

详见 [可逆性的等价条件](%E9%80%86%E7%9F%A9%E9%98%B5.md#%E5%AE%9A%E4%B9%89)。

## 5. 内积、范数、正交与投影

欧氏内积为

$$
\langle x,y\rangle=x^\top y,
$$

它同时编码长度和夹角：

$$
\|x\|_2=\sqrt{x^\top x},\qquad
\cos\theta=\frac{x^\top y}{\|x\|_2\|y\|_2}.
$$

若 $x^\top y=0$，两向量正交。若一组基向量彼此正交且长度为 1，就是**标准正交基**。在这种基下，坐标可以直接用内积读出，数值计算也通常更稳定。

把 $x$ 投影到非零向量 $u$ 所在直线：

$$
\operatorname{proj}_u(x)=
\frac{u^\top x}{u^\top u}u.
$$

最小二乘本质上是在把目标 $b$ 投影到 $A$ 的列空间，见 [逆矩阵](%E9%80%86%E7%9F%A9%E9%98%B5.md#%E6%9C%80%E5%B0%8F%E4%BA%8C%E4%B9%98)。

## 6. 特征分解和 SVD 不要混为一谈

特征分解研究方阵中保持方向不变的向量：

$$
Av=\lambda v.
$$

但不是每个实方阵都能在实数域中用一组特征向量对角化。SVD 更普适：任意 $A\in\mathbb R^{m\times n}$ 都可写成

$$
A=U\Sigma V^\top.
$$

可以依次理解为：

1. $V^\top$ 把输入旋转或反射到一组正交方向；
2. $\Sigma$ 沿这些方向按奇异值 $\sigma_i\ge 0$ 缩放；
3. $U$ 再把结果旋转或反射到输出空间。

非零奇异值个数等于矩阵的秩。保留最大的前 $k$ 个奇异值，在谱范数和 Frobenius 范数意义下得到最佳的秩-$k$ 近似：

$$
A_k=U_k\Sigma_kV_k^\top.
$$

这连接了降维、压缩、去噪、伪逆和最小二乘。

## 7. 数值计算：数学可逆不等于计算可靠

条件数

$$
\kappa_2(A)=\frac{\sigma_{\max}}{\sigma_{\min}}
$$

衡量输入或舍入误差被放大的程度。$\kappa$ 很大时，矩阵即使理论上可逆，数值解也可能非常敏感。

工程上应优先：

- 解 $Ax=b$：使用 `solve`，不要先算 `inv(A) @ b`；
- 最小二乘：使用 `lstsq`、QR 或 SVD；
- 判断数值秩：必须说明容差，不能把“奇异值恰好等于 0”当作浮点判断标准。

## 8. 可运行示例：秩、SVD 与最小二乘

```python
import numpy as np

A = np.array([
    [1.0, 1.0],
    [2.0, 2.0],
    [0.0, 1.0],
])
b = np.array([1.0, 2.1, 0.9])

rank = np.linalg.matrix_rank(A)
U, singular_values, Vt = np.linalg.svd(A, full_matrices=False)
reconstructed = (U * singular_values) @ Vt
x, *_ = np.linalg.lstsq(A, b, rcond=None)

print("rank:", rank)
print("singular values:", singular_values)
print("SVD reconstructs A:", np.allclose(A, reconstructed))
print("least-squares x:", x)
print("residual norm:", np.linalg.norm(A @ x - b))

assert rank == 2
assert np.allclose(A, reconstructed)
```

## 常见误区

1. **“维数就是向量里数字的个数。”** 那只是环境空间的坐标数；子空间维数由其基向量数决定。
2. **“生成集合中的向量越多，空间维数越高。”** 重复或线性相关向量不会增加维数。
3. **“行变换后得到的列可以直接当原矩阵列空间的基。”** 行变换一般会改变列空间；应在行最简形中找主元位置，再取原矩阵对应列。
4. **“特征分解和 SVD 是同一种分解。”** 它们相关但条件、向量和用途不同；SVD 适用于任意矩阵。
5. **“可逆就应该显式求逆。”** 理论表达和数值实现要分开；求解线性系统通常更稳定。

## 来源

- [MIT OpenCourseWare: Linear Algebra 18.06](https://ocw.mit.edu/courses/18-06-linear-algebra-spring-2010/)
- [NumPy: Linear algebra routines](https://numpy.org/doc/stable/reference/routines.linalg.html)
- [NumPy: `numpy.linalg.svd`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.svd.html)
- [NumPy: `numpy.linalg.lstsq`](https://numpy.org/doc/stable/reference/generated/numpy.linalg.lstsq.html)
- Trefethen & Bau, *Numerical Linear Algebra*, SIAM, 1997.
