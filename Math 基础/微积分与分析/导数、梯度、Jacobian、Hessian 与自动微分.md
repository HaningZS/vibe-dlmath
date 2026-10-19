---
type: note
domain: math/calculus
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# 导数、梯度、Jacobian、Hessian 与自动微分

证明进阶：[T40 负曲率与二阶驻点](../../proofs/optimization/T40-second-order-stationarity.md) · [T42 Jacobian 与时变训练核](../../proofs/deep-learning/T42-feature-drift-kernel-dynamics.md)。

先用一句人话串起来：

> 导数描述“一点点输入变化会带来多少输出变化”；梯度把标量输出对多个输入的敏感度排成向量；Jacobian 处理向量到向量；Hessian 描述梯度怎样变化；自动微分则把链式法则沿计算图系统地执行。

## 知识依赖与相关笔记

- 向量、矩阵和内积：[向量空间、基、秩与 SVD](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E5%90%91%E9%87%8F%E7%A9%BA%E9%97%B4%E3%80%81%E5%9F%BA%E3%80%81%E7%A7%A9%E4%B8%8E%20SVD.md)。
- 局部近似：[一阶泰勒展开](%E4%B8%80%E9%98%B6%E6%B3%B0%E5%8B%92%E5%B1%95%E5%BC%80.md)、[二阶 Taylor 与 Hessian](%E4%BA%8C%E9%98%B6%E6%B3%B0%E5%8B%92%E5%B1%95%E5%BC%80.md#%E5%A4%9A%E7%BB%B4%E5%BD%A2%E5%BC%8F)。
- 平滑性：[Lipschitz constant](Lipschitz%20constant.md#%E4%B8%8E%E5%AF%BC%E6%95%B0%E7%9A%84%E5%85%B3%E7%B3%BB)。
- 从局部导数走到优化保证：[凸集、凸函数与优化直觉](%E5%87%B8%E9%9B%86%E3%80%81%E5%87%B8%E5%87%BD%E6%95%B0%E4%B8%8E%E4%BC%98%E5%8C%96%E7%9B%B4%E8%A7%89.md)、[梯度下降、学习率与收敛](%E6%A2%AF%E5%BA%A6%E4%B8%8B%E9%99%8D%E3%80%81%E5%AD%A6%E4%B9%A0%E7%8E%87%E4%B8%8E%E6%94%B6%E6%95%9B.md)。
- 有等式或不等式约束时：[拉格朗日乘子、对偶与约束优化](%E6%8B%89%E6%A0%BC%E6%9C%97%E6%97%A5%E4%B9%98%E5%AD%90%E3%80%81%E5%AF%B9%E5%81%B6%E4%B8%8E%E7%BA%A6%E6%9D%9F%E4%BC%98%E5%8C%96.md)。
- 梯度如何用于学习：[SGD](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E4%BC%98%E5%8C%96%E6%96%B9%E6%B3%95/SGD.md#%E6%A2%AF%E5%BA%A6%E4%B8%8B%E9%99%8D%E7%9A%84%E4%B8%89%E7%A7%8D%E4%B8%BB%E8%A6%81%E5%BD%A2%E5%BC%8F)、[AdamW and Adam and Momentum](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E4%BC%98%E5%8C%96%E6%96%B9%E6%B3%95/AdamW%20and%20Adam%20and%20Momentum.md#1-adam-%E4%BC%98%E5%8C%96%E5%99%A8)。
- 完整训练过程：[神经网络训练闭环：前向、反向与优化](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%B7%B1%E5%BA%A6%E5%AD%A6%E4%B9%A0%E5%B7%A5%E7%A8%8B/PyTorch/%E7%A5%9E%E7%BB%8F%E7%BD%91%E7%BB%9C%E8%AE%AD%E7%BB%83%E9%97%AD%E7%8E%AF%EF%BC%9A%E5%89%8D%E5%90%91%E3%80%81%E5%8F%8D%E5%90%91%E4%B8%8E%E4%BC%98%E5%8C%96.md)。
- 策略梯度实例：[Actor 的梯度](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0/%E5%9F%BA%E7%A1%80/Actor-Critic%20Math.md#2--actor-%E7%9A%84%E6%95%B0%E5%AD%A6%E6%9B%B4%E6%96%B0-%E5%AD%A6%E4%B9%A0%E7%AD%96%E7%95%A5)。

## 1. 一维导数：局部变化率

函数 $f:\mathbb R\to\mathbb R$ 在 $x$ 处的导数定义为

$$
f'(x)=\lim_{h\to0}\frac{f(x+h)-f(x)}{h}.
$$

它是局部斜率，不是“函数整体上涨了多少”。当 $h$ 足够小时：

$$
f(x+h)\approx f(x)+f'(x)h.
$$

这正是 [一阶 Taylor 近似](%E4%B8%80%E9%98%B6%E6%B3%B0%E5%8B%92%E5%B1%95%E5%BC%80.md#2-%E7%9B%B4%E8%A7%82%E7%90%86%E8%A7%A3%E5%88%87%E7%BA%BF%E8%BF%91%E4%BC%BC)。

## 2. 偏导数和梯度：多个输入，一个输出

对标量函数 $f:\mathbb R^n\to\mathbb R$，偏导数

$$
\frac{\partial f}{\partial x_i}
$$

表示只改变第 $i$ 个坐标、暂时固定其他坐标时的变化率。把全部偏导排成列向量：

$$
\nabla f(x)=
\begin{bmatrix}
\partial f/\partial x_1\\
\vdots\\
\partial f/\partial x_n
\end{bmatrix}.
$$

梯度有两个重要含义：

- $\nabla f(x)$ 指向局部增长最快的方向；
- $-\nabla f(x)$ 是欧氏几何下的最速下降方向。

沿单位方向 $u$ 的方向导数是

$$
D_uf(x)=\nabla f(x)^\top u.
$$

所以梯度不是神秘的“优化信号”，而是把任意方向的局部变化压缩进一个向量。

## 3. Jacobian：多个输入，多个输出

设 $f:\mathbb R^n\to\mathbb R^m$。输出有 $m$ 个分量，每个分量都有一个梯度。常见的“输出行、输入列”约定下：

$$
J_f(x)_{ij}=\frac{\partial f_i}{\partial x_j},
\qquad
J_f(x)\in\mathbb R^{m\times n}.
$$

小扰动 $\Delta x$ 经过函数后近似变为

$$
f(x+\Delta x)-f(x)\approx J_f(x)\Delta x.
$$

Jacobian 就是非线性函数在一点附近对应的线性变换。不同教材可能使用转置约定，阅读公式时先检查形状，不要只背排列方向。

## 4. Hessian：梯度的 Jacobian

对 $f:\mathbb R^n\to\mathbb R$，Hessian 是二阶偏导矩阵：

$$
H_f(x)=\nabla^2 f(x),
\qquad
(H_f)_{ij}=\frac{\partial^2 f}{\partial x_i\partial x_j}.
$$

它进入二阶局部模型：

$$
f(x+\Delta x)\approx
f(x)+\nabla f(x)^\top\Delta x
+\frac12\Delta x^\top H_f(x)\Delta x.
$$

- Hessian 正定：附近像向上的碗；
- Hessian 不定：存在上升和下降方向，常见于鞍点；
- Hessian 奇异：有局部平坦或冗余方向。

深度学习中通常不会显式构造完整 Hessian，因为参数数目为 $n$ 时需要 $O(n^2)$ 存储。更常见的是 Hessian-vector product、近似曲率或纯一阶方法。

## 5. 链式法则：反向传播的数学核心

若 $x\mapsto y=f(x)\mapsto z=g(y)$，则

$$
J_{g\circ f}(x)=J_g(f(x))J_f(x).
$$

神经网络是很多层函数的复合。反向传播并不是另一种求导规则，而是**复用中间结果、高效执行链式法则**。

当最终损失 $L$ 是标量时，反向模式自动微分从

$$
\frac{\partial L}{\partial L}=1
$$

出发，逆着计算图传播 vector-Jacobian product（VJP）。对“参数很多、输出是一个损失”的训练任务，反向模式通常比逐个输入做前向求导高效得多。

## 6. 自动微分不是数值差分，也不是符号求导

三者要分清：

- **有限差分**：用 $[f(x+h)-f(x)]/h$ 近似，有截断误差和舍入误差；
- **符号求导**：操作代数表达式，可能产生庞大的表达式；
- **自动微分**：把程序拆成基本运算，并对每个运算应用精确的局部导数和链式法则，最终只受浮点计算误差影响。

PyTorch 的动态图会在前向计算时记录求导所需的操作；调用 `backward()` 后，叶子张量的 `.grad` 会**累加**梯度。因此每次优化步骤通常要先 `optimizer.zero_grad()`。

`model.eval()` 只切换 Dropout、BatchNorm 等模块的行为，并不会关闭梯度记录；验证时常同时使用 `model.eval()` 和 `torch.no_grad()` 或 `torch.inference_mode()`。

## 7. 可运行示例：让 PyTorch 求梯度和 Hessian

```python
import torch

x = torch.tensor([1.0, 2.0], requires_grad=True)

# f(x0, x1) = x0^2 + 3*x0*x1 + sin(x1)
f = x[0] ** 2 + 3 * x[0] * x[1] + torch.sin(x[1])

# create_graph=True 保留“梯度本身如何计算”的图，才能继续求二阶导。
(gradient,) = torch.autograd.grad(f, x, create_graph=True)
hessian = torch.stack([
    torch.autograd.grad(gradient[i], x, retain_graph=True)[0]
    for i in range(x.numel())
])

print("f:", f.item())
print("gradient:", gradient.detach())
print("Hessian:\n", hessian.detach())

expected_hessian = torch.tensor([
    [2.0, 3.0],
    [3.0, -0.9092974],  # -sin(2)
])
assert torch.allclose(hessian.detach(), expected_hessian)
```

## 常见误区

1. **“偏导都存在，所以函数一定可微。”** 多元函数只具有各方向偏导并不足以保证可微，还需要更强的局部一致性条件。
2. **“梯度永远是最速下降方向。”** 这依赖所选内积或度量；自然梯度会使用不同几何。
3. **“梯度为零就是最小值。”** 也可能是最大值、鞍点或平坦点。
4. **“Adam 的二阶矩就是 Hessian。”** [Adam 的梯度平方移动平均](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/moment%28%E7%9F%A9%29.md#adam-%E4%B8%AD%E7%9A%84-moment-estimates)不是曲率矩阵。
5. **“`eval()` 会关闭求导。”** 模块模式与 autograd 模式是两套独立机制。
6. **“反向传播必须把完整 Jacobian 存下来。”** 实现通常直接计算 VJP，不显式形成巨大 Jacobian。

## 来源

- [MIT OpenCourseWare: Multivariable Calculus 18.02SC](https://ocw.mit.edu/courses/18-02sc-multivariable-calculus-fall-2010/)
- [PyTorch: Autograd mechanics](https://docs.pytorch.org/docs/stable/notes/autograd.html)
- [PyTorch: Automatic differentiation package](https://docs.pytorch.org/docs/stable/autograd.html)
- Baydin et al., [Automatic Differentiation in Machine Learning: a Survey](https://jmlr.org/papers/v18/17-468.html), JMLR 2018.
