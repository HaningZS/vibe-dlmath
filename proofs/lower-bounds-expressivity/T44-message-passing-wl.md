---
id: T44
type: proof-template
refined: 2026-10-02
status: self-contained-core
---

# T44. 消息传递 GNN 与 1-WL 表达力上界

[主题目录](README.md) · [等变性 T43](../deep-learning/T43-equivariance-symmetry.md) · [表达力下界 T20B](T20B-expressivity-lower-bound.md)

## 复用契约

**对象**：有限无向图；节点初始特征；共享更新的消息传递网络
$h_v^{t+1}=U_t(h_v^t,\mathop{\mathrm{AGG}}\nolimits_t(\lbrace\negthinspace\lbrace h_u^t:u\in N(v)\rbrace\negthinspace\rbrace))$，aggregation 只依赖邻居多重集，readout 只依赖节点多重集。

**结论**：1-WL 在同样初始标签和深度下无法区分的图，该模型也无法区分。双重花括号表示 multiset：重复次数保留，顺序不保留。

**条件**：两张图共享参数；没有额外 ID、位置编码、边标签、全局 oracle 或高阶结构输入。加入这些输入后要重定义比较对象。

**失败例子**：节点级随机 ID 或结构位置编码可能破坏本卡的不可区分关系；不能把结论推广到所有叫“GNN”的模型。

## 实例化时必须完成

- [ ] 固定模型实际能观察的图特征和邻域接口。
- [ ] 归纳处理每层、skip、readout 和深度。
- [ ] 用一个具体图对展示区分失败，并检查任务标签是否不同。
- [ ] 声称达到 1-WL 能力时，另证聚合、更新和 readout 的 injectivity。

## 1. 直觉：每个节点只能听见邻居的摘要

把节点想成住在网络里的观察者。它知道自己的特征，并听邻居重复汇报；若两处每轮收到的摘要都相同，再复杂的共享神经网络也没有额外信息可用。

表达力瓶颈因此可能来自观察接口，而不是参数不足。

## 2. 1-WL 是怎样更新颜色的

初始颜色 $c_v^0$ 编码初始特征。第 $t+1$ 轮把
$(c_v^t,\lbrace\negthinspace\lbrace c_u^t:u\in N(v)\rbrace\negthinspace\rbrace)$ 用 injective 编码变成新颜色。
比较两张图时使用同一编码规则，检查各轮颜色多重集是否不同。

颜色是数学上无碰撞的记号，不是默认某个有限维神经网络已经学会的编码。

## 3. 上界的完整归纳

归纳断言：相同 WL 颜色的节点具有相同 $h_v^t$。

初始特征相同，断言在 $t=0$ 成立。若下一轮颜色相同，旧颜色和邻居旧颜色的多重集相同；依归纳假设，旧 embedding 和邻居 embedding 的多重集也相同。相同的 aggregation 与 $U_t$ 因而给出相同输出。

若两图颜色多重集相同，节点 embedding 多重集也相同；相同 readout 输出相同图表示。证明针对所有参数成立，因此属于 [T20B](T20B-expressivity-lower-bound.md) 的全模型量词。

## 4. 可手算的失败图对

取 6 节点环 $C_6$ 与两个互不连接的三角形 $C_3\sqcup C_3$；所有节点给相同初始特征。每个节点的度都为 2。

第一轮每个节点都看见两个相同颜色。以后仍如此，所以两图每轮都是 6 份同色节点，任意上述网络的 readout 相同。但一个图连通，另一个不连通。

对“是否连通”的任务，这一模型族在这个图对上有表达限制；训练更多轮不能补回没有观察到的信息。

## 5. 上界、可达性和泛化是三件事

injective sum aggregation、更新与 readout 在相应可数/有界条件下可达到 1-WL 区分能力；这些条件与具体构造应回到 [原论文](https://arxiv.org/abs/1810.00826)。上界归纳本身不证明任意网络已达到它，也不证明训练能找到权重。

更强表达力对目标任务是否有益还要统计学习分析。能够区分更多图，也可能增加模型复杂度；参见 [T33](../generalization/T33-uniform-convergence.md)。

## 前置、关联与证据

- [量词与归纳](<../../Math 基础/证明工具/量词、归纳、不变量与望远镜求和.md>) · [群与排列](<../../Math 基础/信号与几何/对称性、群表示与等变网络.md>)。
- [T43](../deep-learning/T43-equivariance-symmetry.md) · [T20B](T20B-expressivity-lower-bound.md) · [本地论文卡](../../proof_ref/dl-specializations-2026-10/how-powerful-are-graph-neural-networks-1810.00826/README.md)。
- [固定 v3 的 scoped 核验记录](../../proof_ref/dl-specializations-2026-10/how-powerful-are-graph-neural-networks-1810.00826/核验笔记.md)。
