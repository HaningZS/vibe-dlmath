---
id: T20B
type: proof-template
refined: 2026-09-28
status: bounded-scope
---

# T20B. Expressivity limitations and computational lower bounds

[主题目录](README.md) · [T20 路由](T20-expressivity-router.md) · [模板总目录](../README.md)

## 复用契约

**输入对象**：整个模型族 $\mathcal M_n$、资源/精度约束、输入类与任务 $f_n$。

**输出结论**：覆盖全部允许模型的能力限制。确定性最坏情形的一种量词是

$$
\forall M_n\in\mathcal M_n,\ \exists x\in\mathcal X_n:
\quad d(M_n(x),f_n(x))>\epsilon.
$$

平均情形、随机模型和近似错误概率要写各自的分布与量词，不能由此免费得到。

**失败例子**：一次训练失败没有覆盖其他参数或算法，因此不是模型类的能力下界。

## 实例化时必须完成

- [ ] 固定输入表示、预处理、模型资源和外部工具。
- [ ] 覆盖整个模型族，而非一个实例。
- [ ] 给出匹配资源模型的已知下界或自证结构限制。
- [ ] 若依赖未证明的复杂度类分离，标为条件定理。
- [ ] 架构对比使用一致的精度、顺序步数和输入访问范围。

## 归约方向

先证明 $\mathcal M_n\subseteq\mathcal C_n$，即每个允许模型都可被某受限计算类模拟；再证明目标不在 $\mathcal C_n$，从而不在 $\mathcal M_n$。

这是“模型 → 受限类”的方向。构造模型模拟一个算法是另一方向，不能用来推出模型无能。

## 可以完整证明的结构下界

考虑输入层每个节点只读一个 bit、每个 gate fan-in 至多为 $k\geq2$、单输出、深度 $L$ 的确定性无环电路。权重/门规则固定，不随当前输入变化。

归纳：深度 0 节点依赖至多一个 bit；深度 $\ell+1$ 的 gate 合并至多 $k$ 个上层节点，因此依赖至多 $k^{\ell+1}$ 个输入。

若 $n>k^L$，输出至少不读一个 bit。选两个只在该 bit 不同的输入，电路输出相同，parity 却相反。因此精确计算全部 $n$-bit parity 必须满足

$$
L\geq\lceil\log_k n\rceil.
$$

这不是 full-attention Transformer 的下界：一个 attention 节点可以读全部 token，预处理也可能混合多个输入，都会破坏本例的依赖数假设。

## 与信息下界的连接

[T12](T12-information-lower-bounds.md) 限制可得信息，本卡限制计算结构。二者可组合，但必须说明瓶颈，不把统计 sample lower bound 改称计算 lower bound。

相关：[T20A 构造上界](T20A-constructive-simulation.md) · [T14 算法模拟](../deep-learning/T14-algorithm-simulation.md) · [P10 归约工具](../../通用证明原语.md)。

## 专项证明接口（2026-10-02）

- [T44：通过 1-WL 归纳和具体图对证明消息传递 GNN 的表达力限制。](T44-message-passing-wl.md)
