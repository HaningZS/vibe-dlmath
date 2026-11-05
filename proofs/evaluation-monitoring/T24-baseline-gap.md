---
id: T24
type: project-tool
refined: 2026-09-28
status: "project-tool"
---

# T24. Project-specific empirical max-baseline algebra (not a significance proof)

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

记录方法超过多种 baseline 的经验数值关系。

## 复用契约

**输入对象**：同一评估样本、同向指标、非空 baseline 集与方法分数。

**输出结论**：经验代数恒等式，不是显著性、机制或信息非冗余证明。

**必需假设**：

- 指标数据与方向统一。
- higher-is-better 用 max，loss 用 min 并反向差值。
- 总体声明另做配对不确定性与选择效应分析。

**失败例子**：正 gap 仅 0.001 而抽样波动更大时，正号不能支持显著性。

## 实例化时必须完成

- [ ] 规定指标方向与 baseline 集。
- [ ] 应用 a-max(b,c)=min(a-b,a-c)。
- [ ] 总体结论另做检验/区间。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [量词、归纳、不变量与望远镜求和](../../Math%20%E5%9F%BA%E7%A1%80/%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/%E9%87%8F%E8%AF%8D%E3%80%81%E5%BD%92%E7%BA%B3%E3%80%81%E4%B8%8D%E5%8F%98%E9%87%8F%E4%B8%8E%E6%9C%9B%E8%BF%9C%E9%95%9C%E6%B1%82%E5%92%8C.md) · [多重比较](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E7%BD%AE%E4%BF%A1%E5%8C%BA%E9%97%B4%E3%80%81%E5%81%87%E8%AE%BE%E6%A3%80%E9%AA%8C%E4%B8%8E%E5%A4%9A%E9%87%8D%E6%AF%94%E8%BE%83.md#5-%E5%A4%9A%E9%87%8D%E6%AF%94%E8%BE%83%E7%9C%8B%E5%BE%97%E8%B6%8A%E5%A4%9A%E8%B6%8A%E5%AE%B9%E6%98%93%E5%81%B6%E7%84%B6%E6%98%BE%E8%91%97)；本模板不构成显著性证明。

## 适用场景

你有一个 proposed method 和一个 audit baseline，想**描述同一评估样本上的数值差值**。这只是 evaluation bookkeeping，不证明总体显著性、机制正确性或信息源非冗余。

```text
方法是否超过普通 baseline？
方法是否超过一个 flexible same-information classifier？
```

## 核心定义

令标准 baseline 集合 $\mathcal B^{std}$ **有限且非空**：

$$
\mathcal{B}^{std}.
$$

audit baseline：

$$
b^{audit}.
$$

以下先限定 $M$ 是同一数据、同一方向、higher-is-better 的经验指标。标准 gap：

$$
\Delta^{std}_m
=M_m-
\max_{b\in\mathcal{B}^{std}}M_b.
$$

audit gap：

$$
\Delta^{audit}_m
=M_m-
\max_{b\in\mathcal{B}^{std}\cup\lbrace b^{audit}\rbrace}M_b.
$$

若定义 direct audit gap：

$$
\Delta^{direct}_m=M_m-M_{b^{audit}},
$$

则

$$
\Delta^{audit}_m
=\min\lbrace\Delta^{std}_m,\Delta^{direct}_m\rbrace.
$$

对 lower-is-better 的 loss，应改用 $\min$ baseline 和反向差值，例如

$$
\Gamma_m^{std}
=\min_{b\in\mathcal B^{std}}L_b-L_m,
\qquad
\Gamma_m^{direct}=L_{b^{audit}}-L_m,
\qquad
\Gamma_m^{audit}
=\min_{b\in\mathcal B^{std}\cup\lbrace b^{audit}\rbrace}L_b-L_m
=\min\lbrace\Gamma_m^{std},\Gamma_m^{direct}\rbrace.
$$

## 逐步证明模板

```text
Step 1. 写 audit maximum = max(standard maximum, audit baseline metric)。
Step 2. 写 method metric minus audit maximum。
Step 3. 使用恒等式 a - max(b,c) = min(a-b,a-c)。
Step 4. 得到 audit gap = min(standard gap, direct audit gap)。
Step 5. 在 higher-is-better 约定下推出 audit gap > 0 iff two empirical gaps 都 > 0。
Step 6. 只解释为“在这份数据和这个指标上数值同时更高”。
Step 7. 若要总体结论，另外给 paired bootstrap、permutation test、confidence interval 或跨 seed/dataset hierarchical analysis，并处理多 baseline selection。
```

## 可迁移用法

- PFC / same-prefix classifier audit。
- strong learned baseline audit。
- oracle-free vs oracle baseline 分层。
- ablation 中记录某一信息源对应的 empirical gap；是否非冗余需要额外识别假设和控制实验。

## 常见坑

- audit gap 不为正不代表方法没用，只代表它没有超过这个 audit baseline。
- audit baseline 的信息集必须与方法公平，否则解释不成立。
- 如果 audit baseline 用了 test label tuning，就不能作为 fair audit。
- 对多个 baseline 取 max 会产生 selection effect；不能把正 gap 当作未校正的显著性结论。
- 模型容量、优化预算和调参差异也可能造成 gap，不能仅凭 gap 推断“新信息源有效”。

## 来源论文 / 参考

这个恒等式是项目自定义代数，不由下面的论文证明。相关文献只定义/解释评价指标：

- ROC/AUROC evaluation: Fawcett, 2006. https://www.sciencedirect.com/science/article/abs/pii/S016786550500303X
- Proper scoring / probabilistic forecast evaluation: Gneiting & Raftery, 2007. https://doi.org/10.1198/016214506000001437
- Calibration and evaluation of neural probabilities: Guo et al., 2017. https://proceedings.mlr.press/v70/guo17a.html

## 关联模板与本地证据

- [T22：分开证明 AUROC 排序不变性与 Brier proper-scoring 分解。](T22-ranking-proper-scoring.md)
- [T23：从信息依赖图证明适应性和停止时间性质。](T23-prefix-safety.md)

通用证明工具：P01；见 [证明原语](../../通用证明原语.md)。
