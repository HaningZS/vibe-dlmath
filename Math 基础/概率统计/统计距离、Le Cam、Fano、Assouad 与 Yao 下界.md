---
type: note
domain: math/probability-and-lower-bounds
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# 统计距离、Le Cam、Fano、Assouad 与 Yao 下界

很多论文的上界在回答：“这个算法最多需要多少样本、查询或迭代？”

下界反过来问：

> 即使把算法设计得再聪明，只给这些观测，它最多能分辨出多少关于真实世界的信息？

最有用的直觉不是“造一个让某个算法失败的反例”，而是一次**蒙眼辨味实验**：先准备几个答案相差很大的世界，再让它们产生非常相似的数据。如果观察者连自己身处哪个世界都难以判断，就不可能在每个世界都给出准确估计。

整条证明链通常是：

```text
构造困难实例
→ 证明正确答案彼此相隔很远
→ 证明观测分布彼此很近
→ 把估计问题归约成统计检验
→ 用 Le Cam / Fano / Assouad 控制检验错误
→ 把检验错误乘回原问题的损失尺度
```

## 知识依赖、模板与论文入口

- 学习路线：[AI 理论证明前置学习路线](../%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/AI%20%E7%90%86%E8%AE%BA%E8%AF%81%E6%98%8E%E5%89%8D%E7%BD%AE%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)；总入口：[Math 基础目录](../Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md)。
- 概率对象与条件分布：[概率论主干：联合、条件、期望与协方差](%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md)。
- 可测性、条件期望与 filtration：[测度、条件期望、滤过与适应过程](%E6%B5%8B%E5%BA%A6%E3%80%81%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E3%80%81%E6%BB%A4%E8%BF%87%E4%B8%8E%E9%80%82%E5%BA%94%E8%BF%87%E7%A8%8B.md)。
- KL、熵与互信息：[信息论基础：熵、交叉熵与 KL 散度](%E4%BF%A1%E6%81%AF%E8%AE%BA%E5%9F%BA%E7%A1%80%EF%BC%9A%E7%86%B5%E3%80%81%E4%BA%A4%E5%8F%89%E7%86%B5%E4%B8%8E%20KL%20%E6%95%A3%E5%BA%A6.md)。
- 几何型分布距离：[最优传输与 Wasserstein 距离](%E6%9C%80%E4%BC%98%E4%BC%A0%E8%BE%93%E4%B8%8E%20Wasserstein%20%E8%B7%9D%E7%A6%BB.md)。
- 通用原语：[P05：耦合与换测度](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p05-couplingchange-of-measure-%E4%B8%8E%E4%BF%A1%E6%81%AF%E9%A2%84%E7%AE%97)、[P10：检验归约与下界](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p10-reductiontesting-lower-bound-%E4%B8%8E-yao-principle)。
- 主模板：[T12：经典与交互式下界](../../proofs/lower-bounds-expressivity/T12-information-lower-bounds.md)。
- 近期框架：[R02：随机非凸优化 oracle 下界](../../%E8%BF%91%E6%9C%9F%E9%A1%B6%E4%BC%9A%E7%90%86%E8%AE%BA%E6%A1%86%E6%9E%B6%EF%BC%882025-2026%EF%BC%89.md#r02-oracle-lower-bound%E5%9B%B0%E9%9A%BE%E6%97%8F--%E8%AF%86%E5%88%AB--divergence-decomposition)。
- 核验卡与原文入口：[Interactive lower bound 核验卡](../../proof_ref/core-theory-2026-09/assouad-fano-and-le-cam-with-interaction-a-2410.05117/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md) · [Interactive Fano，PDF p.9](../../proof_ref/core-theory-2026-09/assouad-fano-and-le-cam-with-interaction-a-2410.05117/paper.pdf#page=9)；[Oracle lower bound 核验卡](../../proof_ref/recent-accepted-2025-2026/new-lower-bounds-for-stochastic-non-convex-optimization-2502.14060/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md) · [Divergence decomposition 下界，PDF p.7](../../proof_ref/recent-accepted-2025-2026/new-lower-bounds-for-stochastic-non-convex-optimization-2502.14060/paper.pdf#page=7)。

> [!important] 这篇笔记的边界
> 下面给的是证明工具和常见常数形式，不是一个能脱离假设直接套用的“万能下界”。每次都要重新检查损失的尺度、分布方向、绝对连续性、算法随机性与交互 transcript。

## 1. 统计距离究竟在量什么

两个参数很远，不代表数据容易区分；两个参数很近，也不代表观测分布一定接近。下界同时需要两把尺子：

1. **任务尺子**：参数、最优解或最优策略之间差多少，例如 $d(\theta_0,\theta_1)$；
2. **信息尺子**：这些参数诱导的数据分布 $P_0,P_1$ 有多容易被区分。

可以把它想成两种茶的配方和入口味道：配方差异是任务尺子，蒙眼后能否尝出来是信息尺子。下界要故意找到“配方差很多、入口味道却很像”的组合。

不同统计距离回答的问题不同：

| 工具 | 人话 | 常见证明角色 |
|---|---|---|
| Total variation（TV） | 最能区分两分布的事件，概率能差多少 | 直接连接最优二元检验错误 |
| KL divergence | 用 $Q$ 的编码/似然解释 $P$，平均多付多少 | 可沿样本和交互历史做 chain rule |
| Hellinger distance | 比较平方根密度，方向对称且数值稳定 | 产品分布、渐近统计与距离互换 |
| $f$-divergence | 用一个凸函数统一许多密度比差异 | data processing 与统一分析 |
| Wasserstein | 把质量从一处分布搬到另一处分布要多远 | 参数空间有几何、生成模型与稳定性 |

“距离更高级”不是选择标准。真正的问题是：**哪一种量既能从模型中算出来，又能接到目标 theorem 上？**

## 2. Coupling 与 total variation：把两个世界放在同一张桌上

### 2.1 Coupling 不是“默认独立采样”

给定边缘分布 $P,Q$，coupling 是任意联合分布 $\gamma$，使

$$
X\sim P,\qquad Y\sim Q.
$$

独立采样 $P\otimes Q$ 只是其中一种 coupling。证明中常主动设计 coupling，让 $X,Y$ 尽量相同，再用

$$
\mathbb P_\gamma(X\neq Y)
$$

控制两个随机过程或算法输出的差别。算法稳定性、Markov 链 mixing 和随机过程比较都在使用这类思想。

### 2.2 TV 是最坏事件的概率差

定义

$$
\operatorname{TV}(P,Q)
=\sup_A |P(A)-Q(A)|.
$$

若二者相对于共同测度有密度 $p,q$，则

$$
\operatorname{TV}(P,Q)
=\frac12\int |p-q|.
$$

TV 的范围是 $[0,1]$。 $0$ 表示同分布， $1$ 表示存在一个事件能把它们完全分开。

在常见的离散空间或标准 Borel 空间中，一个核心 coupling 表示是

$$
\operatorname{TV}(P,Q)
=\inf_{\gamma\in\Pi(P,Q)}\mathbb P_\gamma(X\neq Y).
$$

因此，TV 也可以理解为：**即使采用最聪明的配对，两份样本仍不得不不同的最小概率。** 达到等号的配对叫 maximal coupling；任意随手构造的 coupling 只会给上界。

### 2.3 TV 与二元检验错误精确相连

假设世界 $0$ 和世界 $1$ 的先验各为 $1/2$，观测分别服从 $P_0,P_1$。最优检验的平均错误率为

$$
\inf_\phi \frac12P_0(\phi=1)+\frac12P_1(\phi=0)
=\frac12\bigl(1-\operatorname{TV}(P_0,P_1)\bigr).
$$

这是 Le Cam 两点法的发动机：只要 TV 小，任何检验都不得不经常认错世界。

## 3. KL、Hellinger 与 $f$-divergence

### 3.1 KL 有方向

若 $P\ll Q$，即 $Q$ 认为不可能的事件在 $P$ 下也不发生，则

$$
D_{\mathrm{KL}}(P\|Q)
=\int \log\frac{dP}{dQ}\,dP.
$$

在离散情形中：

$$
D_{\mathrm{KL}}(P\|Q)
=\sum_x p(x)\log\frac{p(x)}{q(x)}.
$$

一般有

$$
D_{\mathrm{KL}}(P\|Q)\neq D_{\mathrm{KL}}(Q\|P).
$$

而且一个方向有限，反方向可能是 $+\infty$。证明中写“两个分布的 KL 很小”是不完整的；必须写清方向，以及期望究竟在哪个分布下取。

### 3.2 Hellinger 先对密度开平方

本文采用约定

$$
H^2(P,Q)
=\frac12\int(\sqrt p-\sqrt q)^2
=1-\int\sqrt{pq}.
$$

$H$ 对称，范围也在 $[0,1]$。平方根会削弱极小密度比的爆炸，因此 Hellinger 在渐近统计和产品分布中常比 KL 温和。

在上述约定下有常用比较：

$$
H^2(P,Q)
\le \operatorname{TV}(P,Q)
\le \sqrt2,H(P,Q).
$$

常数会随作者对 $H$ 是否带 $1/2$ 的定义变化；引用前先看定义。

### 3.3 $f$-divergence 是一个统一外壳

令 $f:(0,\infty)\to\mathbb R$ 为凸函数，且 $f(1)=0$。在 $P\ll Q$ 时定义

$$
D_f(P\|Q)
=\int f\!\left(\frac{dP}{dQ}\right)dQ.
$$

- $f(t)=t\log t$ 给 KL；
- $f(t)=\tfrac12|t-1|$ 给 TV；
- $f(t)=\tfrac12(\sqrt t-1)^2$ 给本文约定的 $H^2$。

统一写法很方便，但不能因此把这些量当成可互换的同一个距离。不同 $f$ 对尾部、支撑错位和小密度区域的敏感度不同。

## 4. Data processing 与 Pinsker：观测加工不会凭空制造信息

### 4.1 Data processing inequality

若 $T$ 是一个可测映射，或更一般地是同一个 Markov kernel，把原始观测加工成摘要，则

$$
D_f(T_\#P\|T_\#Q)
\le D_f(P\|Q).
$$

人话是：把完整照片压成一个标签，不会让两个世界更容易区分。对 KL、TV、Hellinger 等 $f$-divergence 都成立。

这条不等式在归约中有两种常见用途：

1. 参数 $\theta$ 产生数据，数据再经过算法输出估计；算法输出不能比完整数据包含更多区分信息；
2. 复杂 transcript 最后只映射成一个决策，先上界 transcript divergence，再控制决策错误。

### 4.2 Pinsker 只给一个方向

Pinsker 不等式给出

$$
\operatorname{TV}(P,Q)
\le \sqrt{\frac12D_{\mathrm{KL}}(P\|Q)}.
$$

因此，小 KL 推出小 TV，再推出二元检验困难。

反过来一般不成立：很小的 TV 仍可能伴随很大的甚至无穷的 KL，因为 KL 对极小的 $q(x)$ 极敏感。若论文需要“TV 小推出 KL 小”，必须增加密度比有界、共同支撑等条件。

## 5. KL chain rule：信息怎样沿样本或时间累积

对序列 $Z_{1:T}$，若所需条件分布和绝对连续性成立，则

$$
D_{\mathrm{KL}}(P_{Z_{1:T}}\|Q_{Z_{1:T}})
=\sum_{t=1}^T
\mathbb E_{P}
\left[
D_{\mathrm{KL}}
\bigl(P(Z_t\mid Z_{<t})\|Q(Z_t\mid Z_{<t})\bigr)
\right].
$$

注意三个容易漏掉的细节：

1. 右边的外层期望在 $P$ 下；
2. 每一步比较的是**给定同一段历史值**后的条件分布；
3. 方向从头到尾都是 $P\|Q$，不能在某一步偷换。

IID 情形只是特例：若 $Z_t$ 独立同分布，则

$$
D_{\mathrm{KL}}(P^{\otimes T}\|Q^{\otimes T})
=T D_{\mathrm{KL}}(P\|Q).
$$

这解释了为什么样本数越多，两个很相近的单样本分布最终也可能被区分。

## 6. 交互 transcript：自适应查询为什么不能按 IID 写

bandit、RL、主动学习和 oracle optimization 中，算法会根据过去观测选择下一次动作。完整 transcript 应写成

$$
H_T=(A_1,O_1,\ldots,A_T,O_T).
$$

若两个环境中使用**同一个算法 kernel**，即给定相同历史时动作分布相同，则 action 部分的 KL 抵消：

$$
D_{\mathrm{KL}}(P_\theta^{H_T}\|P_{\theta'}^{H_T})
=\sum_{t=1}^T
\mathbb E_\theta
\left[
D_{\mathrm{KL}}
\bigl(
P_\theta(O_t\mid H_{t-1},A_t)
\|P_{\theta'}(O_t\mid H_{t-1},A_t)
\bigr)
\right].
$$

“抵消”不表示动作没有作用。算法选择哪些动作，会改变右边访问哪些信息区域，因此仍会改变总 KL。

以下情况不能机械照抄：

- 两个环境中的可用动作集合不同；
- 算法在两个世界使用了不同规则或不同随机种子分布；
- 在数据依赖 stopping time 停止；
- batch feedback、延迟反馈或部分可观测状态没有被完整写进 transcript；
- 某一步条件分布不满足绝对连续性。

此时先重写 joint law，再决定 chain rule 中哪些 kernel 真能抵消。

## 7. Testing reduction：把“估不准”变成“认不出世界”

设两个参数的任务距离为

$$
d(\theta_0,\theta_1)=\Delta.
$$

若估计器 $\widehat\theta$ 在两个世界都离真值小于 $\Delta/2$，就可以把它映射为“离哪个参数更近”的检验。因此，检验经常犯错意味着估计器至少在某些时候误差不小。

这是一个归约，而不是等号。需要逐项检查：

1. 参数集合确实满足原问题所有假设；
2. 两个答案在目标损失下有 separation；
3. 从估计器到检验的映射可测；
4. 检验错误能推出多大的原任务损失。

遗漏第 4 步，就会得到没有单位的“下界”。

## 8. Le Cam 两点法：先学会最小的困难族

对等先验二元检验，结合上一节可得到一种常见形式：

$$
\inf_{\widehat\theta}
\sup_{i\in\{0,1\}}
\mathbb E_i d(\widehat\theta,\theta_i)
\ge
\frac{\Delta}{4}
\left(1-\operatorname{TV}(P_0,P_1)\right).
$$

再用 Pinsker：

$$
\text{risk}
\ge
\frac{\Delta}{4}
\left(1-\sqrt{\frac12D_{\mathrm{KL}}(P_0\|P_1)}\right).
$$

使用套路：

1. 选 $\theta_0,\theta_1$，让答案间距 $\Delta$ 大；
2. 算出或上界数据 KL/TV；
3. 调一个扰动尺度 $\varepsilon$，平衡“答案够远”和“数据够像”。

Le Cam 很适合先证明 $n^{-1/2}$ 量级、局部不可辨识性或最简单的 oracle 下界，但只有两个世界，无法捕捉高维中“需要同时辨认许多方向”的困难。

## 9. Fano：在许多候选世界中找出一个

令隐藏索引 $V$ 在 $M\ge2$ 个假设上均匀分布，观测为 $X$。Fano 不等式的一种常见形式是

$$
\inf_{\widehat V}
\mathbb P(\widehat V\neq V)
\ge
1-\frac{I(V;X)+\log 2}{\log M}.
$$

三项各有直觉：

- $\log M$：要完整指出世界编号所需的信息量；
- $I(V;X)$：数据实际泄露了多少关于编号的信息；
- 若泄露远小于所需信息，识别错误必然很高。

应用到估计时，先构造一个 $2s$-packing：任意两个参数距离至少 $2s$。若估计误差小于 $s$，最近邻解码就能认出 $V$。于是典型风险下界是

$$
s\left[1-\frac{I(V;X)+\log2}{\log M}\right]_+,
$$

其中 $[a]_+=\max(a,0)$。不截断的原式即使右侧为负仍形式上成立，但只有括号为正时才给出非平凡风险下界。

真正困难的通常不是写 Fano 公式，而是：

1. 在参数空间中构造足够大的 packing；
2. 上界 $I(V;X)$。常见办法是选参考分布 $Q$，用

$$
I(V;X)
\le \frac1M\sum_{v=1}^M D_{\mathrm{KL}}(P_v\|Q).
$$

参考分布不一定属于困难族，但方向与绝对连续性仍要合法。

## 10. Assouad：把高维困难拆成许多二元困难

Assouad 构造超立方索引

$$
\omega\in\{-1,+1\}^d.
$$

每个坐标代表一个局部二选一。若 $\omega^{(j)}$ 表示翻转第 $j$ 位，则重点比较相邻顶点 $P_\omega$ 与 $P_{\omega^{(j)}}$。

一种常见形式是：若

$$
\alpha_{\mathrm{TV}}
=\max_{\omega,j}
\operatorname{TV}(P_\omega,P_{\omega^{(j)}}),
$$

则

$$
\inf_{\widehat\omega}
\sup_\omega
\mathbb E_\omega d_H(\widehat\omega,\omega)
\ge
\frac d2(1-\alpha_{\mathrm{TV}}).
$$

如果原任务损失满足

$$
L(\widehat\theta,\theta_\omega)
\ge c\,d_H(\widehat\omega,\omega),
$$

再把 Hamming 下界乘以 $c$。因此 Assouad 特别适合坐标可分、非参数估计、图像/函数局部块和高维稀疏构造。

不要只证明相邻分布很近；还必须证明每个错位坐标在原任务中至少付出多少损失。

## 11. Yao minimax：怎样给随机算法做下界

随机算法看起来像比确定性算法更难统一分析。Yao 的想法是反过来：

> 不逐个追踪算法的随机种子，而是先给输入选一个困难分布，再证明任何确定性算法在这个分布上的平均表现都不好。

有限问题中的典型不等式为

$$
\inf_{A\ \mathrm{randomized}}
\sup_x\mathbb E L(A,x)
\ge
\sup_\mu
\inf_{a\ \mathrm{deterministic}}
\mathbb E_{x\sim\mu}L(a,x).
$$

右边先由证明者选困难输入分布 $\mu$，再允许确定性算法选最佳响应。只要连这个最佳响应都损失很大，任何随机算法的 worst-case 风险也不会更小。

边界：

- 先写清算法随机性和实例随机性分别在哪里；
- 无穷空间里宣称 minimax 等号需要紧性、凸性、可测选择等额外条件；
- Yao 不是“随机算法等于确定性算法”，而是一种交换量词后得到的下界方法。

## 12. 一张选择表

| 困难结构 | 优先尝试 | 原因 |
|---|---|---|
| 两个局部世界 | Le Cam | 构造最简单，TV 与二元检验直接相连 |
| 很大的有限 packing | Fano | 用信息预算对抗 $\log M$ 个候选 |
| 许多近似独立的坐标位 | Assouad | 把总风险拆成逐坐标二元检验 |
| 随机/自适应算法 | Yao 或 transcript KL | 分离算法随机性，正确累计交互信息 |
| 连续时间路径 | Girsanov 后接 KL/TV | 先把 drift 差转成 path-space KL；需另查随机微积分条件 |

## 13. 可运行 NumPy 实验：TV、最优检验与 Pinsker

下面构造两个世界：每次观测是 Bernoulli，世界 $0$ 的正例率为 $0.45$，世界 $1$ 为 $0.55$。我们枚举长度为 $n$ 的所有二进制序列，精确计算产品分布的 TV、KL 和 Bayes 最优错误率。

```python
import numpy as np

rng = np.random.default_rng(12)
p0, p1 = 0.45, 0.55
n = 8

# 枚举所有 2^n 个序列；k 是每个序列中 1 的个数。
states = np.arange(2**n, dtype=np.uint32)
bits = ((states[:, None] >> np.arange(n)) & 1).astype(np.int8)
k = bits.sum(axis=1)

prob0 = p0**k * (1.0 - p0)**(n - k)
prob1 = p1**k * (1.0 - p1)**(n - k)

assert np.isclose(prob0.sum(), 1.0)
assert np.isclose(prob1.sum(), 1.0)

tv = 0.5 * np.abs(prob0 - prob1).sum()
kl_01 = np.sum(prob0 * np.log(prob0 / prob1))
bayes_error = 0.5 * np.minimum(prob0, prob1).sum()

# 只保留 parity 是一次数据处理；区分能力不能增加。
parity = k % 2
coarse0 = np.array([prob0[parity == j].sum() for j in (0, 1)])
coarse1 = np.array([prob1[parity == j].sum() for j in (0, 1)])
tv_after_parity = 0.5 * np.abs(coarse0 - coarse1).sum()

print(f"TV(P0^n, P1^n)        = {tv:.6f}")
print(f"KL(P0^n || P1^n)      = {kl_01:.6f}")
print(f"Bayes error            = {bayes_error:.6f}")
print(f"TV after parity summary = {tv_after_parity:.6f}")

assert np.isclose(bayes_error, 0.5 * (1.0 - tv))
assert tv <= np.sqrt(0.5 * kl_01) + 1e-12  # Pinsker
assert tv_after_parity <= tv + 1e-12       # data processing

# Monte Carlo 检查：采用似然比较的最优检验。
m = 200_000
world = rng.integers(0, 2, size=m)
success_prob = np.where(world == 0, p0, p1)
samples = rng.random((m, n)) < success_prob[:, None]
k_sample = samples.sum(axis=1)

log_lr = (
    k_sample * np.log(p1 / p0)
    + (n - k_sample) * np.log((1.0 - p1) / (1.0 - p0))
)
prediction = (log_lr > 0.0).astype(int)
empirical_error = np.mean(prediction != world)

print(f"simulated optimal error = {empirical_error:.6f}")
assert abs(empirical_error - bayes_error) < 0.005
```

这段代码验证的是有限例子，不是 Le Cam 定理的证明。它帮助建立三条直觉：

1. 最优二元检验错误确实等于 $(1-\mathrm{TV})/2$；
2. Pinsker 把易累积的 KL 接到直接控制检验的 TV；
3. 把完整序列压成 parity 后，区分能力只会下降。

## 14. 常见误区

1. **“下界就是找一个算法失败的例子。”** Minimax 下界要覆盖所有合法算法。
2. **“参数很接近，所以数据分布也很接近。”** 必须从观测模型计算 divergence。
3. **“KL 是距离。”** KL 不对称，也不满足三角不等式。
4. **“KL 很小和 TV 很小完全等价。”** Pinsker 只有 KL 小推出 TV 小；反向需要额外条件。
5. **“Coupling 就是独立配对。”** 证明通常需要主动设计相关 coupling。
6. **“Fano 写完公式就结束了。”** packing、信息预算和风险 separation 才是主体。
7. **“Assouad 只要构造超立方。”** 还要把 Hamming 错误转换成原损失。
8. **“交互数据也有 $T\,\mathrm{KL}$。”** 动作依赖历史时必须写 transcript chain rule。
9. **“算法 kernel 总会抵消。”** 只有两个环境中条件动作规则相同且 transcript 定义完整时才抵消。
10. **“Yao 证明了随机算法没有用。”** 它只是把 randomized worst-case 下界转成 deterministic average-case 下界。
11. **“互换 KL 方向不影响数量级。”** 支撑不同时，一个方向可能直接变成无穷。
12. **“把 TV、KL、Hellinger、Wasserstein 相加就是总误差。”** 先把各项转换到同一 metric，并核对方向与常数。

## 15. 自测

1. 为什么下界同时需要“答案分得开”和“观测分不开”？
2. 写出 TV 的事件定义、密度定义和 maximal-coupling 定义。
3. 等先验二元检验的最优错误率怎样由 TV 表示？
4. 为什么 Pinsker 不能倒过来无条件使用？
5. KL chain rule 的外层期望在哪个分布下？
6. 在 bandit 中 action kernel 抵消后，动作为什么仍会影响总 KL？
7. Le Cam、Fano、Assouad 分别适合怎样的困难族？
8. Fano 中 $\log M$ 和 $I(V;X)$ 各表示什么？
9. Assouad 的 Hamming 下界怎样转换成原问题风险？
10. Yao 不等式中两种随机性分别是什么？

## 权威来源

- Tsybakov, *Introduction to Nonparametric Estimation*, Springer, 2009：Chapter 2 的 minimax lower-bound 工具。
- Yu, [Assouad, Fano, and Le Cam](https://www.stat.berkeley.edu/~binyu/ps/LeCam.pdf), 1997。
- Cover & Thomas, *Elements of Information Theory*, 2nd ed., Wiley, 2006：KL、data processing、mutual information 与 Fano。
- Csiszár, “Information-type measures of difference of probability distributions and indirect observations,” *Studia Scientiarum Mathematicarum Hungarica*, 1967： $f$-divergence。
- Lattimore & Szepesvári, [*Bandit Algorithms*](https://tor-lattimore.com/downloads/book/book.pdf), Cambridge University Press, 2020：change of measure 与交互下界。
- Duchi, *Lecture Notes on Statistics and Information Theory*, 2023：统计距离、检验与 minimax lower bounds。
- [Interactive lower-bound 核验卡](../../proof_ref/core-theory-2026-09/assouad-fano-and-le-cam-with-interaction-a-2410.05117/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md)。
- [随机非凸优化下界核验卡](../../proof_ref/recent-accepted-2025-2026/new-lower-bounds-for-stochastic-non-convex-optimization-2502.14060/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md)。
