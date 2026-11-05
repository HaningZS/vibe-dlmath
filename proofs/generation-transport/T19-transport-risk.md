---
id: T19
type: proof-template
refined: 2026-09-28
status: "bounded-scope"
---

# T19. OT domain-adaptation bounds require joint/label assumptions

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

先指定 joint/label 条件，再把 transport cost 连接到风险差。

## 复用契约

**输入对象**：source/target joint laws、ground metric、loss 与 coupling。

**输出结论**：给定 joint/label 条件下的风险比较；feature marginal 对齐本身没有 target-risk 保证。

**必需假设**：

- 风险积分存在，loss 对指定 joint metric Lipschitz，或另有 label mismatch 控制。
- 仅 feature alignment 时需 shared labeling 等额外条件。
- 部分匹配的质量、归一化和未匹配损失明确。

**失败例子**：X 相同，source 标签恒为 0、target 恒为 1；feature W1=0，但恒预测 0 的风险从 0 变成 1。

## 实例化时必须完成

- [ ] 说明 transport 定义在 X 还是 (X,Y)。
- [ ] 证明 loss regularity 或 mismatch bound。
- [ ] 单列 empirical 和 unmatched-mass 代价。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [最优传输与 Wasserstein 距离](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%9C%80%E4%BC%98%E4%BC%A0%E8%BE%93%E4%B8%8E%20Wasserstein%20%E8%B7%9D%E7%A6%BB.md) · [算法稳定性、经验过程与 PAC-Bayes](../../Math%20%E5%9F%BA%E7%A1%80/%E7%BB%9F%E8%AE%A1%E5%AD%A6%E4%B9%A0%E7%90%86%E8%AE%BA/%E7%AE%97%E6%B3%95%E7%A8%B3%E5%AE%9A%E6%80%A7%E3%80%81%E7%BB%8F%E9%AA%8C%E8%BF%87%E7%A8%8B%E4%B8%8E%20PAC-Bayes.md)；feature marginal alignment 单独不足以推出 target risk。

## 适用场景

domain adaptation 与 partial domain adaptation。对推荐、LLM 或多模态的迁移只可作为算法设计启发，除非重新验证 distribution、labeling function 和 loss assumptions。

## 核心 bound 形状

这种 bound 不是只靠 feature marginal distance 就成立。典型版本还需要 joint transport，或 covariate shift/shared labeling function、Lipschitz predictor/loss、hypothesis-class complexity 等条件：

$$
R_T(h)
\le
R_S(h)
+\mathrm{Distance}(P_S,P_T)
+\mathrm{label\ mismatch\ term}
+\mathrm{complexity\ term}.
$$

OT/Wasserstein 模板把 `Distance` 写成 Wasserstein 或 partial Wasserstein。

## partial OT 适用条件

### 一个可以直接推导的 joint-distribution 原型

令 $z=(x,y)$，两域 joint laws 都有有限一阶矩，且
$\ell_h(z)$ 对 ground metric $d$ 是 $L_h$-Lipschitz。对任意完整 coupling $\gamma$，

$$
|R_T(h)-R_S(h)|
\leq \int|\ell_h(z')-\ell_h(z)|\thinspace d\gamma
\leq L_h\int d(z,z')\thinspace d\gamma.
$$

对 $\gamma$ 取 inf 得 $|R_T(h)-R_S(h)|\leq L_h W_1(P_S^{XY},P_T^{XY})$。这是关于 **joint law** 的界；若把它换成 feature marginal，label 信息已经丢失，必须另加假设。

若 $\ell_h\in[0,1]$， $\gamma$ 是质量 $m$ 的 partial joint coupling，且其两个边缘分别被 $P_S,P_T$ 支配，则一个粗的一侧界是

$$
R_T(h)\leq R_S(h)+L_h\int d(z,z')\thinspace d\gamma+(1-m).
$$

最后一项来自未匹配 target mass 的最坏损失。这只是明确假设下的教学原型，不等于任何 feature-level partial-DA 论文的全部保证。

partial DA 通常假设 target label space 是 source label space 的子集且 source 含多余类别；这与任意 support partial overlap 不是同一条件。

```text
source label space contains target label space plus irrelevant classes
transported probability mass may be partial, as specified by the theorem
```

partial OT 允许只匹配一部分 mass，避免把 target 强行对齐到 source 的无关类别。

## 逐步证明模板

```text
Step 1. 定义 source/target 的 joint distribution、label spaces 与 shift assumption。
Step 2. 定义 transport plan / partial transport plan。
Step 3. 证明 predictor/loss 对所选 ground metric Lipschitz，或写出共享 labeling function/mismatch term。
Step 4. 对 source empirical risk 加权，减少 irrelevant source classes。
Step 5. 在上述假设下上界 target risk by weighted source risk + partial transport + label mismatch + complexity。
Step 6. 从 bound 中读出算法 objective。
```

## 可迁移用法

- 推荐/LLM/多模态可以借鉴 partial matching objective，但不能直接继承 target-risk guarantee。

## 常见坑

- Wasserstein 距离高维估计样本复杂度差，需要结构假设。
- partial OT 的 unmatched mass 如何解释要写清楚。
- OT bound 往往更像 design principle，不一定给 tight rate。
- 只对齐 feature marginals 不能控制 target risk；label conditional shift 可能使距离很小但风险很大。

## 来源论文 / 参考

- Theoretical Performance Guarantees for Partial Domain Adaptation via Partial Optimal Transport, ICML 2025. https://proceedings.mlr.press/v267/naram25a.html
- Transformer expressivity/OT implementation 论文属于 T14，不是 domain-adaptation risk bound 的来源。

## 关联模板与本地证据

- [T13：在同一度量中组合连续过程、学习与离散采样误差。](T13-sampler-error.md)
- [T05：分开使用 PAC-Bayes 高概率界和互信息期望界。](../generalization/T05-pac-bayes-information.md)

通用证明工具：P05、P06；见 [证明原语](../../通用证明原语.md)。

- [Computational Optimal Transport](../../proof_ref/foundations-2026-09/computational-optimal-transport-1803.00567/README.md) · [官方 arXiv](https://arxiv.org/abs/1803.00567)
- [Sinkhorn Distances: Lightspeed Computation of Optimal Transportation Distances](../../proof_ref/foundations-2026-09/sinkhorn-distances-lightspeed-computation-of-optimal-transportation-distances-1306.0895/README.md) · [官方 arXiv](https://arxiv.org/abs/1306.0895)

## 专项证明接口（2026-10-02）

- [T48：先用识别假设连接干预与观察 law，再分析 DR 或深度表示的估计误差。](../statistics/T48-causal-identification.md)

## 经典与近期证明蒸馏

- [T51：在真实边缘分布下控制速度误差，用学习场 Lipschitz 与耦合推出 Wasserstein 界。](T51-flow-trajectory-error.md)
