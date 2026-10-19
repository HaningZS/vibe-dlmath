---
id: T17
type: method-card
refined: 2026-09-28
status: "method-card-only"
---

# T17. Calibrated predictions in algorithms-with-predictions: problem-specific design pattern

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

将 calibration 连接到特定在线问题的成本分解。

## 复用契约

**输入对象**：在线问题、baseline、概率预测、校准定义、决策与成本。

**输出结论**：问题特定的方法卡；不直接提供任意 agent/LLM 的 regret 定理。

**必需假设**：

- 校准定义与分组方式明确。
- 校准误差到成本的连接针对具体问题证明。
- consistency 与 robustness 分开证明。

**失败例子**：恒预测总体正例比例可以 marginally calibrated，却没有区分单个样本的能力。

## 实例化时必须完成

- [ ] 锁定来源的正式问题。
- [ ] 新任务重新分解成本。
- [ ] 尚未证明的迁移标为研究假设。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [概率论主干：联合、条件、期望与协方差](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md) · [置信区间、假设检验与多重比较](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E7%BD%AE%E4%BF%A1%E5%8C%BA%E9%97%B4%E3%80%81%E5%81%87%E8%AE%BE%E6%A3%80%E9%AA%8C%E4%B8%8E%E5%A4%9A%E9%87%8D%E6%AF%94%E8%BE%83.md)；calibration 不推出单样本正确。

## 适用场景

论文已证明的核心案例是 ski rental 与 online job scheduling。迁移到 LLM agent、推荐或 tool-use 只能标为 `design analogy`，需要为新问题重新证明 competitive/regret guarantee。

## 核心思想

先选择 calibration 定义：population calibration、bin calibration、multicalibration 或 online calibration error。连续概率下不能用“所有预测恰好等于 p 的样本”作为未经定义的条件事件。

```text
预测值 + calibrated confidence
```

## 证明目标

通常要同时证明：

```text
consistency: predictor 准确时接近该问题定义的 prediction-optimal 保证；
robustness: predictor 错时不比 worst-case baseline 差太多。
```

## 逐步证明模板

```text
Step 1. 定义在线问题、worst-case baseline、prediction 与 calibration notion。
Step 2. 证明 predictor 的 calibration error 如何进入该问题的 cost/regret decomposition。
Step 3. 设计 decision rule；不要把 calibrated probability 当作 per-instance correctness guarantee。
Step 4. 在论文使用的 partition/bin 或 population 条件下汇总 performance。
Step 5. 分别证明 consistency 与 robustness；二者形式由具体问题决定，不由 calibration 自动推出。
Step 6. 对新领域重新证明以上步骤，而不是引用 ski-rental theorem 直接迁移。
```

## 可迁移用法

- LLM agent 的 action confidence。
- 推荐系统的用户偏好置信度。
- early stopping：只有 calibrated probability 超过阈值才停止。
- tool-use：confidence 低时请求更多信息。

## 常见坑

- calibration 不等于 accuracy；高校准模型也可能很不 sharp。
- 要明确 calibration 是 marginal、group-wise、online 还是 distribution-free。
- 如果分布漂移，offline calibration 可能失效。
- calibrated probability（条件频率保证）、confidence interval、conformal coverage 和 sharpness 是不同对象。

## 来源论文 / 参考

- Algorithms with Calibrated Machine Learning Predictions, ICML 2025. https://openreview.net/forum?id=Obet2x6GNl
- 本地核验：[核验笔记](../../proof_ref/core-theory-2026-09/algorithms-with-calibrated-machine-learning-predictions-2502.02861/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md) · [PDF](../../proof_ref/core-theory-2026-09/algorithms-with-calibrated-machine-learning-predictions-2502.02861/paper.pdf#page=5)
- Calibration of Modern Neural Networks, ICML 2017. https://proceedings.mlr.press/v70/guo17a.html

## 关联模板与本地证据

- [T22：分开证明 AUROC 排序不变性与 Brier proper-scoring 分解。](T22-ranking-proper-scoring.md)
- [T23：从信息依赖图证明适应性和停止时间性质。](T23-prefix-safety.md)
- [T18：用交换性和名次对称性证明边际覆盖。](../statistics/T18-split-conformal.md)

通用证明工具：P01、P03；见 [证明原语](../../通用证明原语.md)。

- [Algorithms with Calibrated Machine Learning Predictions](../../proof_ref/core-theory-2026-09/algorithms-with-calibrated-machine-learning-predictions-2502.02861/README.md) · [官方 arXiv](https://arxiv.org/abs/2502.02861)
