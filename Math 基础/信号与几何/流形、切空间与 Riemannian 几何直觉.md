---
type: note
domain: math/signal-geometry
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# 流形、切空间与 Riemannian 几何直觉

先抓住一个类比：

> 地球表面整体是弯的，但站在城市尺度上可以画一张近似平面的地图。流形就是“局部像普通欧氏空间、整体却可以弯曲或有特殊拓扑”的空间；切空间是某一点上所有合法瞬时方向组成的局部平面。

AI 中的向量通常放在 $\mathbb R^D$ 里计算，但它们未必能任意移动：单位归一化 embedding 被限制在球面上，三维旋转矩阵被限制在 $SO(3)$ 上，概率向量被限制在单纯形上。严格说，$p_i>0$ 的开放单纯形是光滑流形；包含 $p_i=0$ 的闭单纯形带有边界与角点。流形语言让“约束是什么、距离怎样量、梯度该往哪里走”变得明确。

## 知识依赖与相关笔记

- 路线入口：[AI Researcher 数学学习路线](../AI%20Researcher%20%E6%95%B0%E5%AD%A6%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)、[AI Researcher 高阶数学路线：LLM、CV 与生成模型](../AI%20Researcher%20%E9%AB%98%E9%98%B6%E6%95%B0%E5%AD%A6%E8%B7%AF%E7%BA%BF%EF%BC%9ALLM%E3%80%81CV%20%E4%B8%8E%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B.md)、[Math 基础目录](../Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md)。
- 线性代数先修：[向量空间](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E5%90%91%E9%87%8F%E7%A9%BA%E9%97%B4%E3%80%81%E5%9F%BA%E3%80%81%E7%A7%A9%E4%B8%8E%20SVD.md#1-%E5%90%91%E9%87%8F%E4%B8%8D%E5%8F%AA%E6%98%AF%E4%B8%80%E5%88%97%E6%95%B0%E5%AD%97)、[投影](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E6%8A%95%E5%BD%B1%E3%80%81%E6%9C%80%E5%B0%8F%E4%BA%8C%E4%B9%98%E4%B8%8E%E4%BC%AA%E9%80%86.md#1-%E6%8A%95%E5%BD%B1%E5%9C%A8%E5%85%81%E8%AE%B8%E7%9A%84%E6%96%B9%E5%90%91%E9%87%8C%E6%89%BE%E6%9C%80%E8%BF%91%E7%82%B9)、[Orthogonal Matrix](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/Orthogonal%20Matrix.md)。
- 微积分先修：[导数、梯度、Jacobian、Hessian 与自动微分](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E5%AF%BC%E6%95%B0%E3%80%81%E6%A2%AF%E5%BA%A6%E3%80%81Jacobian%E3%80%81Hessian%20%E4%B8%8E%E8%87%AA%E5%8A%A8%E5%BE%AE%E5%88%86.md)、[拉格朗日乘子、对偶与约束优化](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E6%8B%89%E6%A0%BC%E6%9C%97%E6%97%A5%E4%B9%98%E5%AD%90%E3%80%81%E5%AF%B9%E5%81%B6%E4%B8%8E%E7%BA%A6%E6%9D%9F%E4%BC%98%E5%8C%96.md)。
- 对称性连接：[对称性、群表示与等变网络](%E5%AF%B9%E7%A7%B0%E6%80%A7%E3%80%81%E7%BE%A4%E8%A1%A8%E7%A4%BA%E4%B8%8E%E7%AD%89%E5%8F%98%E7%BD%91%E7%BB%9C.md)。
- 表示学习连接：[RAG embedding](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/LLM%20%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93/RAG/RAG%20embedding.md)、[Embedding-向量运算-word2vec简介](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E8%A1%A8%E7%A4%BA%E5%AD%A6%E4%B9%A0/Embedding-%E5%90%91%E9%87%8F%E8%BF%90%E7%AE%97-word2vec%E7%AE%80%E4%BB%8B.md)、[InfoNCE Loss](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0/InfoNCE%20Loss.md)、[NT-Xent Loss](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0/NT-Xent%20Loss.md)、[所有的norm](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/LLM%20%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93/Transformer/%E6%B3%A8%E6%84%8F%E5%8A%9B%E4%B8%8E%E7%BB%84%E4%BB%B6/%E6%89%80%E6%9C%89%E7%9A%84norm.md)。

## 1. 为什么不直接把所有东西都当作普通向量

普通欧氏空间 $\mathbb R^D$ 允许沿任意方向走任意距离。但很多对象带有必须满足的约束：

- 单位向量：$\|x\|_2=1$；
- 概率向量：$p_i\ge0$ 且 $\sum_i p_i=1$；
- 三维旋转矩阵：$R^\top R=I$ 且 $\det R=1$；
- 正定协方差矩阵：$A=A^\top$ 且 $x^\top Ax>0$。

如果把它们当作无约束向量直接相加或做梯度更新，结果可能离开合法集合。例如两个旋转矩阵的逐元素平均通常不再是旋转矩阵。

流形方法不只是说“数据看起来弯”。它要求先明确合法空间，再在这个空间内部定义局部方向、距离和优化。

## 2. 流形：局部可用坐标描述的空间

粗略地说，一个 $d$ 维流形 $\mathcal M$ 满足：每个点附近都能与 $\mathbb R^d$ 中的一小块建立光滑的一一对应坐标，而且不同局部坐标之间能光滑转换。

### 2.1 内在维数与环境维数

单位圆

$$
S^1=\{(x,y)\in\mathbb R^2:x^2+y^2=1\}
$$

放在二维环境中，但沿圆只需一个角度 $\theta$ 就能描述局部位置，所以它的内在维数是 1，环境维数是 2。

单位球面

$$
S^{d-1}=\{x\in\mathbb R^d:\|x\|_2=1\}
$$

放在 $\mathbb R^d$ 中，却只有 $d-1$ 个自由度，因为一个范数约束拿走了一个自由度。

“内在维数更低”不表示一定存在一张无失真的全局平面坐标图。地球经纬度在极点有奇异，任何世界平面地图也会扭曲某些距离或面积；所以流形通常需要多张局部坐标图拼接。

### 2.2 AI 中的常见例子

| 空间 | 对象 | 典型用途 |
|---|---|---|
| 球面 $S^{d-1}$ | 单位范数向量 | cosine embedding、方向表示 |
| 开放/闭单纯形 | 正概率或允许零概率、且和为 1 的向量 | 类别概率、混合权重；闭单纯形有边界/角点 |
| $SO(3)$ | 三维旋转 | 相机、机器人、物体姿态 |
| $SE(3)$ | 三维旋转 + 平移 | 刚体位姿 |
| 正定矩阵流形 | 协方差、度量矩阵 | 统计、信号与几何学习 |
| 双曲空间 | 负曲率表示 | 某些层级或树状 embedding |

这些空间的几何不同，不能仅凭“都能存成数组”就默认欧氏直线和欧氏距离最合适。

## 3. 切空间：在一点附近，哪些方向是合法的

想象一只蚂蚁站在球面点 $x$。它的瞬时速度不能指向球面法线，否则下一瞬间就会钻离球面。所有合法速度组成点 $x$ 的切空间 $T_x\mathcal M$。

对单位球面，因为约束是

$$
c(x)=x^\top x-1=0,
$$

沿曲线 $x(t)$ 求导可得

$$
\frac{d}{dt}c(x(t))
=2x(t)^\top \dot x(t)=0.
$$

所以在点 $x$：

$$
T_xS^{d-1}
=\{v\in\mathbb R^d:x^\top v=0\}.
$$

也就是说，球面的切向量必须与半径正交。任意环境向量 $g$ 投影到切空间的方法是

$$
\operatorname{Proj}_x(g)
=g-(x^\top g)x
=(I-xx^\top)g.
$$

这和约束优化联系起来：拉格朗日乘子中的约束梯度给出法向方向；切空间则保留不在一阶上违反约束的方向。

## 4. Riemannian 度量：每一点上的尺子

只有流形还不够，我们还需要定义“两个切向量的夹角和长度”。Riemannian 度量为每个点 $x$ 的切空间指定一个随位置光滑变化的内积

$$
g_x(u,v).
$$

它决定：

- 曲线长度怎样计算；
- 两点间最短路径是什么；
- 梯度应如何定义；
- 曲率怎样度量。

球面可以直接继承环境欧氏内积：$g_x(u,v)=u^\top v$。但“尺子”只作用于切方向，路径必须留在球面上。

## 5. 测地线：空间内部真正的“直线”

欧氏空间中，两点最短路径是直线。流形中的对应物叫测地线（geodesic）：局部最直、通常也局部最短的合法路径。

单位球面上，两点的测地线沿大圆走，距离是夹角

$$
d_{S}(x,y)=\arccos(x^\top y),
\qquad \|x\|=\|y\|=1.
$$

而环境欧氏距离是弦长

$$
\|x-y\|_2
=\sqrt{2-2x^\top y}
=2\sin\frac{d_S(x,y)}2.
$$

它们随夹角单调变化，因此做最近邻排序时常给出相同结果；数值和全局几何解释却不相同。

### 5.1 指数映射、对数映射与 retraction

- 指数映射 $\operatorname{Exp}_x(v)$：从点 $x$ 沿切向量 $v$ 指定的测地线走单位时间；
- 对数映射 $\operatorname{Log}_x(y)$：反过来，把邻近点 $y$ 表示成 $x$ 处的切向量；
- retraction：用计算更便宜的一步近似指数映射，只要在小步长下方向正确。

球面上常见 retraction 是

$$
R_x(v)=\frac{x+v}{\|x+v\|_2}.
$$

它先在切平面走一步，再拉回球面。它不是精确大圆运动，但小步长下足以支撑许多优化算法。

## 6. Riemannian 梯度：先找下降方向，再限制为合法方向

在嵌入于欧氏空间、并采用环境欧氏内积诱导的 Riemannian metric 时，一种常见做法是：

1. 计算普通欧氏梯度 $\nabla f(x)$；
2. 把它正交投影到切空间，得到 Riemannian 梯度；若选择别的 metric，则需要按该 metric 重新定义梯度，不能直接使用普通欧氏投影；
3. 沿负切向梯度走一步；
4. 用指数映射或 retraction 回到流形。

对单位球面并采用继承度量：

$$
\operatorname{grad}f(x)
=(I-xx^\top)\nabla f(x).
$$

这与“普通梯度更新后再归一化”在很小步长下一阶接近，但二者的几何解释和大步长行为不应无条件混为一谈。

## 7. Embedding 归一化：把尺度自由度拿掉

对非零表示 $z$ 做

$$
y=\frac{z}{\|z\|_2}
$$

后，$y$ 落在单位球面 $S^{d-1}$ 上。此时

$$
y_1^\top y_2=\cos\theta,
$$

相似度只取决于方向，不再取决于原向量长度。检索和对比学习经常采用这种设计，因为向量范数可能混入置信度、频率或训练尺度等因素，而任务希望按方向比较。

### 7.1 归一化的 Jacobian 揭示了什么

归一化映射的 Jacobian 为

$$
\frac{\partial y}{\partial z}
=\frac1{\|z\|_2}(I-yy^\top).
$$

$I-yy^\top$ 正是到球面切空间的投影：反向传播会去掉纯径向分量。直觉上，若损失只看归一化后的方向，那么只把 $z$ 整体放大并不会改变输出；梯度自然不需要沿这个无效方向更新。

但前面的 $1/\|z\|$ 也说明：非常小的向量可能放大梯度与数值误差，实际实现通常会加入小的 `eps`。

### 7.2 不要把所有 norm 都说成“在球面上学习”

LayerNorm 会对每个样本/每个 token 的特征做中心化和缩放，之后通常还有可学习的逐维仿射参数 $\gamma,\beta$。因此其最终输出不必位于同一个固定单位球面。RMSNorm、BatchNorm 和显式 L2 embedding normalization 约束也不同。

流形视角可以帮助理解归一化消除了哪些自由度，但必须针对真实公式讨论，详见 [所有的norm](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/LLM%20%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93/Transformer/%E6%B3%A8%E6%84%8F%E5%8A%9B%E4%B8%8E%E7%BB%84%E4%BB%B6/%E6%89%80%E6%9C%89%E7%9A%84norm.md)。

## 8. LLM 与 CV 中的具体连接

### 8.1 对比学习、CLIP 与向量检索

很多对比学习目标把图像/文本表示 L2 归一化，再以 cosine similarity 和 temperature 构造 logits。几何上，模型在球面上安排方向：正样本靠近，负样本分开。

这并不意味着表示自动“均匀覆盖球面”，也不保证余弦距离适合所有下游语义。数据分布、负样本、温度和目标函数共同塑造几何；相关损失见 [InfoNCE Loss](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0/InfoNCE%20Loss.md) 与 [NT-Xent Loss](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%8D%9F%E5%A4%B1%E5%87%BD%E6%95%B0/NT-Xent%20Loss.md)。

### 8.2 LLM hidden states

Transformer hidden state 通常仍在环境欧氏空间中经过线性层、attention、残差和归一化。可以研究它们的角度、局部维数或子空间结构，但“语言一定落在某个光滑低维流形上”是待检验的建模假设，不是已证定理。

对 RAG，归一化 embedding 与 cosine/inner-product 索引必须采用一致约定；否则离线训练的相似度与线上检索评分可能不一致，见 [RAG embedding](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/LLM%20%E4%B8%8E%E6%99%BA%E8%83%BD%E4%BD%93/RAG/RAG%20embedding.md)。

### 8.3 三维视觉与机器人

相机或刚体姿态的旋转属于

$$
SO(3)=\{R\in\mathbb R^{3\times3}:R^\top R=I,\det R=1\}.
$$

它看起来有 9 个矩阵元素，实际只有 3 个自由度。直接回归 9 个互不约束的数不会自动得到合法旋转；常用方法包括规范化参数化、在李代数/切空间中更新，或把结果投影回 $SO(3)$。

欧拉角会有奇异性和周期边界，四元数有单位范数约束且 $q$ 与 $-q$ 表示同一旋转。没有一种表示在所有任务中都无代价，选择时应同时考虑连续性、损失、数值稳定性和部署接口。

### 8.4 数据增强轨道与商空间

对称群作用于样本 $x$ 后，所有 $\{g\cdot x:g\in G\}$ 构成它的轨道。若任务标签对这些变换不变，可以把整条轨道看成“同一个语义对象的不同外观”。

把每条轨道压成一个点会通向商空间的思想；构造不变表示就是尝试忽略轨道内部差异。但真实增强不一定是精确群作用，过度压缩也会丢掉方向、位置等有效信息，详见 [增强与对称性](%E5%AF%B9%E7%A7%B0%E6%80%A7%E3%80%81%E7%BE%A4%E8%A1%A8%E7%A4%BA%E4%B8%8E%E7%AD%89%E5%8F%98%E7%BD%91%E7%BB%9C.md#6-%E6%95%B0%E6%8D%AE%E5%A2%9E%E5%BC%BA%E4%B8%8E%E7%AD%89%E5%8F%98%E7%BB%93%E6%9E%84%E4%B8%A4%E7%A7%8D%E4%B8%8D%E5%90%8C%E7%9A%84%E5%BD%92%E7%BA%B3%E5%81%8F%E7%BD%AE)。

## 9. 曲率：不同空间中的“平行线行为”

曲率描述空间偏离平坦欧氏几何的方式。只保留最实用的直觉：

- 正曲率球面：测地线倾向重新靠近，可容纳的周长增长比欧氏空间慢；
- 零曲率欧氏空间：熟悉的平直几何；
- 负曲率双曲空间：可用空间随半径增长更快，适合表达某些指数分支的层级结构。

Poincaré embedding 用双曲空间表达层级关系，是“选择几何以匹配数据结构”的经典例子。但树状结构只是适用情形之一，训练稳定性、距离畸变和任务指标仍要实验评估；不能因为“数据有层级”就断言双曲表示必胜。

## 10. 可运行示例：在单位球面上做投影梯度下降

目标是让单位向量 $x$ 对齐单位目标 $t$，最小化 $f(x)=-t^\top x$。普通梯度是 $-t$；我们把它投影到球面切空间，再归一化回球面。

```python
import numpy as np

target = np.array([0.3, 0.4, 0.8660254])
target = target / np.linalg.norm(target)
x = np.array([1.0, 0.0, 0.0])

initial_similarity = x @ target
step_size = 0.2

for _ in range(30):
    euclidean_grad = -target
    tangent_grad = euclidean_grad - (x @ euclidean_grad) * x

    # 切向量必须与球面半径正交。
    assert abs(x @ tangent_grad) < 1e-12

    # retraction：切平面走一步，再拉回单位球面。
    x = x - step_size * tangent_grad
    x = x / np.linalg.norm(x)

final_similarity = x @ target
print("initial cosine:", initial_similarity)
print("final cosine:", final_similarity)
print("final norm:", np.linalg.norm(x))

assert np.allclose(np.linalg.norm(x), 1.0)
assert final_similarity > initial_similarity
assert final_similarity > 0.999
```

这个例子刻意很小：重点不是发明新优化器，而是观察“欧氏梯度 → 切空间投影 → retraction”三步分别承担什么责任。

## 常见误区

1. **“画在高维空间里的弯曲集合都是流形。”** 自交点、尖点或维数突变处可能不满足局部欧氏性质，需要逐点检查。
2. **“流形一定是低维的。”** 维数是相对概念；流形本身可以很高维，只是局部像某个 $\mathbb R^d$。
3. **“切空间就是流形本身。”** 切空间是某一点的线性近似；走得远后，平面近似会失真。
4. **“归一化 embedding 后，欧氏距离和球面距离完全相同。”** 它们是单调相关的弦长与弧长，但数值、插值路径和曲率解释不同。
5. **“LayerNorm 等于把所有 hidden state 投到单位球面。”** 它的统计维度、中心化、`eps` 和可学习仿射参数使这个说法不准确。
6. **“manifold hypothesis 是已经证明的普遍事实。”** 它是有用但需实证检查的建模假设；真实数据可能有噪声、分支、离散因素和多尺度结构。
7. **“Riemannian 方法一定优于欧氏方法。”** 只有当约束和几何确实匹配问题，且计算代价值得时，结构才可能带来收益。
8. **“两个合法旋转或单位向量直接平均后仍合法。”** 环境空间中的线性组合通常会离开流形，需要插值、投影或 retraction。

## 自测

1. 单位圆的内在维数和环境维数分别是多少？一个约束为什么会减少一个自由度？
2. 从 $x^\top x=1$ 推导球面切空间为何满足 $x^\top v=0$。
3. 测地线与环境空间直线有什么区别？球面两点的弦长和弧长何时接近？
4. 为什么归一化映射的 Jacobian 含有 $I-yy^\top$？它去掉了什么方向？
5. 为什么 $SO(3)$ 用 9 个数存储，却只有 3 个自由度？
6. 若任务要求预测物体朝向，为什么把整个旋转轨道压成同一个不变表示可能有害？

## 延伸阅读与权威来源

- Lee, *Introduction to Smooth Manifolds*, 2nd ed., Springer, 2013：流形、切空间与光滑映射的标准教材。
- Lee, *Riemannian Manifolds: An Introduction to Curvature*, Springer, 1997：Riemannian 度量、测地线与曲率。
- [Absil, Mahony & Sepulchre, Optimization Algorithms on Matrix Manifolds](https://press.princeton.edu/books/hardcover/9780691132983/optimization-algorithms-on-matrix-manifolds), Princeton University Press, 2008：流形优化、retraction 与矩阵流形。
- [Bronstein et al., Geometric Deep Learning](https://arxiv.org/abs/2104.13478)：几何、群、图与神经网络的统一视角。
- [Nickel & Kiela, Poincaré Embeddings for Learning Hierarchical Representations, NeurIPS 2017](https://proceedings.neurips.cc/paper/2017/hash/59dfa2df42d9e3d41f5b02bfc32229dd-Abstract.html)：双曲 embedding 的经典工作。
- [Wang & Isola, Understanding Contrastive Representation Learning through Alignment and Uniformity on the Hypersphere, ICML 2020](https://proceedings.mlr.press/v119/wang20k.html)：单位超球面上的对比表示分析。
