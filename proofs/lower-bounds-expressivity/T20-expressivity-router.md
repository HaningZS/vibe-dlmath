---
id: T20
type: router
refined: 2026-09-28
status: split-router
---

# T20. Formal language / circuit complexity for reasoning models

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

## 复用契约

表达能力上界和下界的量词、归约方向不同，分别进入：

- [T20A：构造性模拟](T20A-constructive-simulation.md)：给出一个合法模型，证明它能完成任务。
- [T20B：表达限制](T20B-expressivity-lower-bound.md)：覆盖全部允许模型，证明任务不能在所给资源下完成。

共同需要写清：输入长度、架构族、depth、width、precision、context、循环步数、外部工具、uniform/nonuniform，以及权重能依赖什么。本页仅路由，不提供统一表达能力定理。

## 实例化时必须完成

- [ ] 选择存在性构造还是全称能力限制。
- [ ] 明确所有资源如何随输入长度变化。
- [ ] 区分可表达、可训练与实际训练后行为。

**失败例子**：一个失败模型不能证明整个模型类失败；一个成功构造也不能证明训练算法会找到它。

## 与其他模板的连接

- [T14：算法模拟与误差传播](../deep-learning/T14-algorithm-simulation.md)：逐层数值实现。
- [T12：信息论下界](T12-information-lower-bounds.md)：信息/oracle 限制。
- [P01/P10：定理规格与归约](../../通用证明原语.md)。

来源论文须与具体计算模型逐项对齐。旧版对 CoT、looped Transformer、masked diffusion 的列举用于选题，不能充当统一能力定理。
