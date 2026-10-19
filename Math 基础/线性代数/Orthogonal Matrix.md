---
status: canonical
reviewed: 2026-08-24
---

[正交矩阵的应用以及哈达玛矩阵](%E6%AD%A3%E4%BA%A4%E7%9F%A9%E9%98%B5%E7%9A%84%E5%BA%94%E7%94%A8%E4%BB%A5%E5%8F%8A%E5%93%88%E8%BE%BE%E7%8E%9B%E7%9F%A9%E9%98%B5.md)
[eigenvalue and eigenvector](eigenvalue%20and%20eigenvector.md)

# 正交矩阵

> [!tip] 放回主干
> 基、正交投影和 SVD 的整体关系见 [向量空间、基、秩与 SVD](%E5%90%91%E9%87%8F%E7%A9%BA%E9%97%B4%E3%80%81%E5%9F%BA%E3%80%81%E7%A7%A9%E4%B8%8E%20SVD.md#5-%E5%86%85%E7%A7%AF%E8%8C%83%E6%95%B0%E6%AD%A3%E4%BA%A4%E4%B8%8E%E6%8A%95%E5%BD%B1)。
> 投影矩阵、正规方程和伪逆的完整推导见 [投影、最小二乘与伪逆](%E6%8A%95%E5%BD%B1%E3%80%81%E6%9C%80%E5%B0%8F%E4%BA%8C%E4%B9%98%E4%B8%8E%E4%BC%AA%E9%80%86.md)。
> Fourier 换基与旋转表示见 [复数、傅里叶变换、卷积与频域](../%E4%BF%A1%E5%8F%B7%E4%B8%8E%E5%87%A0%E4%BD%95/%E5%A4%8D%E6%95%B0%E3%80%81%E5%82%85%E9%87%8C%E5%8F%B6%E5%8F%98%E6%8D%A2%E3%80%81%E5%8D%B7%E7%A7%AF%E4%B8%8E%E9%A2%91%E5%9F%9F.md)；高维随机旋转见 [高维几何、集中现象与随机投影](%E9%AB%98%E7%BB%B4%E5%87%A0%E4%BD%95%E3%80%81%E9%9B%86%E4%B8%AD%E7%8E%B0%E8%B1%A1%E4%B8%8E%E9%9A%8F%E6%9C%BA%E6%8A%95%E5%BD%B1.md)。

## 定义

实方阵 $Q\in\mathbb R^{n\times n}$ 若满足

$$
Q^\top Q=QQ^\top=I,
$$

则称为正交矩阵。等价地，

$$
Q^{-1}=Q^\top.
$$

它的列向量构成 $\mathbb R^n$ 的一组标准正交基；行向量也一样。

## 保持的量

对任意 $u,v\in\mathbb R^n$：

$$
\langle Qu,Qv\rangle=u^\top Q^\top Qv=\langle u,v\rangle.
$$

因此正交变换保持：

- 欧氏范数：$\|Qu\|_2=\|u\|_2$；
- 两点距离；
- 向量夹角；
- 体积的绝对值。

它是固定原点的欧氏等距线性变换。

## 行列式与几何

由 $Q^\top Q=I$ 可得

$$
\det(Q)^2=1,
$$

所以 $\det(Q)=\pm1$。

- $\det(Q)=1$：保持定向，属于特殊正交群 $SO(n)$；二维、三维中典型例子是旋转。
- $\det(Q)=-1$：反转定向；可以是反射，也可以是旋转与反射的复合，不能一概称为“纯反射”。

二维旋转矩阵为

$$
Q(\theta)=
\begin{bmatrix}
\cos\theta&-\sin\theta\\
\sin\theta&\cos\theta
\end{bmatrix}.
$$

## 奇异值、条件数与数值稳定性

正交矩阵的所有奇异值均为 1，因此在 2-范数下

$$
\|Q\|_2=1,
\qquad
\kappa_2(Q)=1.
$$

这解释了为什么正交变换不会放大相对误差或改变向量能量。

## 矩形情形的术语

矩形矩阵不能满足普通方阵意义下的“双边正交”。常见说法是：

- $U^\top U=I$：列标准正交（semi-orthogonal）；
- $UU^\top=I$：行标准正交。

PCA 降维矩阵和 reduced SVD 中的矩阵往往属于这种矩形情形。不要把它们无条件称为方阵正交矩阵。

## 复数情形

在复数空间中，对应概念是酉矩阵：

$$
U^*U=I,
$$

其中 $U^*$ 是共轭转置。

## 来源

- [MIT OpenCourseWare: Orthogonal Matrices and Gram-Schmidt](https://ocw.mit.edu/courses/18-06sc-linear-algebra-fall-2011/pages/least-squares-determinants-and-eigenvalues/orthogonal-matrices-and-gram-schmidt/)
