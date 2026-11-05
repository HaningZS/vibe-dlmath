---
id: T18
type: proof-template
refined: 2026-09-28
status: "refined + claim-checked"
---

# T18. Split conformal marginal coverage; risk control is a separate extension

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

用交换性和名次对称性证明边际覆盖。

## 复用契约

**输入对象**：固定 score、训练/calibration/test 角色、α 与分位数。

**输出结论**：对 calibration/test 联合随机性的 marginal coverage；不保证条件覆盖、集合小或任意停止规则有效。

**必需假设**：

- 条件于独立训练数据与拟合随机性，calibration 与 test scores exchangeable。
- 普通 split-conformal 的 score 不使用 calibration inputs 或 labels 训练/挑选；其他数据用法须另证上述交换性。
- k=ceil((n+1)(1-α))，处理 k=n+1 与 ties。

**失败例子**：同一校准集上挑最优 score 再定阈值，不能照抄固定 score 的秩证明。

## 实例化时必须完成

- [ ] 注明数据角色与模型选择时序。
- [ ] 推 n+1 个分数的秩对称性。
- [ ] risk control 和 adaptive data 另找扩展。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [交换性、Conformal Prediction 与覆盖保证](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E4%BA%A4%E6%8D%A2%E6%80%A7%E3%80%81Conformal%20Prediction%20%E4%B8%8E%E8%A6%86%E7%9B%96%E4%BF%9D%E8%AF%81.md) · [测度、条件期望、滤过与适应过程](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%B5%8B%E5%BA%A6%E3%80%81%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E3%80%81%E6%BB%A4%E8%BF%87%E4%B8%8E%E9%80%82%E5%BA%94%E8%BF%87%E7%A8%8B.md)

## 适用场景

需要 exchangeability 下的 finite-sample **marginal coverage** prediction set。Selective risk control、online conformal、weighted/DR conformal 都需要额外定理，不能由普通 coverage 自动推出。

## 核心 conformal 模板

取 $n\ge1$、 $\alpha\in(0,1)$。先用独立的 proper-training data 训练模型/score，并固定其拟合随机性；不使用任何 calibration pair。给 $n$ 个 calibration nonconformity scores：

$$
s_i = S(x_i,y_i).
$$

排序 $s_{(1)}\le\cdots\le s_{(n)}$，取

$$
k=\left\lceil(n+1)(1-\alpha)\right\rceil,
\qquad
q=\begin{cases}
s_{(k)}, & k\le n,\\
+\infty, & k=n+1.
\end{cases}
$$

prediction set：

$$
C(x)=\lbrace y:S(x,y)\le q\rbrace.
$$

假设条件于 proper-training data 与拟合随机性后， $n+1$ 个 calibration/test **scores** exchangeable。常规 split 构造中，训练得到的同一固定 score 逐点作用于条件可交换的 calibration/test pairs，就满足这个条件。于是

$$
\mathbb{P}(Y_{new}\in C(X_{new}))\ge 1-\alpha.
$$

这是对新样本和 calibration sample 联合随机性的**边际**保证，不是对每个 $X=x$ 的 conditional coverage。无 ties 时 rank uniform；有 ties 时上式仍给保守 coverage，若要精确随机化 coverage 需显式 tie-breaking/randomization。

## 逐步证明模板

```text
Step 1. 明确训练集、calibration set 与 test point 的角色；普通 split score/model 只用独立训练数据，不读取 calibration inputs 或 labels 来训练/挑选。
Step 2. 定义 nonconformity score S(x,y)，并写明“大分数更不 conforming”。
Step 3. 条件于训练信息证明 n+1 个 scores exchangeable，再得到 test score 的 rank 对称性；raw points 可交换本身还不够。
Step 4. 使用 k=ceil((n+1)(1-alpha))，处理 k=n+1 和 ties。
Step 5. 得到 marginal coverage；如果 score 连续，可给常见的上界 1-alpha+1/(n+1)。
Step 6. 若目标是 conditional coverage、adaptive/online data 或 group coverage，停止并换用相应扩展定理。
Step 7. 若目标是 selective/risk control，另定义 bounded loss、nested set family 与 risk upper confidence bound；不要把它写成普通 conformal 的 Step 6。
```

<a id="calibration-input-leakage"></a>

## 反例：没有看 labels，也可能破坏交换性

令 $X\sim\mathop{\mathrm{Unif}}[0,1]$、 $Y\equiv0$，所有 calibration/test pairs 独立同分布。读取 calibration inputs 后、完全不读取 labels，定义

$$
s(x,y)=\mathbf1\lbrace x\notin\lbrace X_1,\ldots,X_n\rbrace\rbrace.
$$

取 $n=9,\alpha=0.1$，则 $k=9$，所有 calibration scores 都为 0，所以 $q=0$。独立 test input 撞上这有限个校准输入的概率为 0，因此 test score 几乎必然为 1，覆盖率为 0。

这里 raw pairs 仍然 IID，失效的是 **scores** 的交换性：score 记住了哪些输入属于 calibration。故“没看 calibration labels”不是足够条件。采用对称的 transductive 构造、允许 calibration covariates 的扩展定理等方案时，须证明相应的 score 交换性或新的覆盖结论；普通 split 公式本身没有提供这种许可。

## DR + conformal 变体

在 censoring / logged data / covariate shift 场景中，conformal calibration 可能需要 weighting 或 imputation。所谓 DR conformal 的 double robustness 是特定 nuisance/weighting 条件下的结论，常为渐近性质；它不自动保留 vanilla split conformal 的 exact distribution-free guarantee。

```text
model-based imputation
+
weighted conformal correction
+
double robustness condition
```

## 常见坑

- exchangeability 是关键；online/adaptive data 需要特别处理。
- conformal 保证 coverage，不保证 set 小。
- marginal coverage 不等于 conditional coverage。
- 如果只报告 calibration-chosen threshold，不要宣称 distribution-free risk control。
- 不要把 calibration inputs 或 labels 同时用于选择 score/model 和计算 quantile，除非使用的变体定理明确允许；只看 inputs 也可能破坏 score 交换性。

## 来源论文 / 参考

- Doubly Robust Conformalized Survival Analysis with Right-Censored Data, ICML 2025. https://openreview.net/forum?id=2PWn1LtCwP
- Conformalized Survival Analysis for General Right-Censored Data, ICLR 2025. https://openreview.net/forum?id=JQtuCumAFD
- Conformal Prediction literature: Vovk et al.; Angelopoulos & Bates tutorials can be added depending on venue style.
- 基础核验：[Distribution-Free Predictive Inference](../../proof_ref/core-theory-2026-09/distribution-free-predictive-inference-for-regression-1604.04173/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md) · [PDF](../../proof_ref/core-theory-2026-09/distribution-free-predictive-inference-for-regression-1604.04173/paper.pdf#page=5)

## 关联模板与本地证据

- [T11：用残差校正把 nuisance 的一阶误差变成乘积余项。](T11-doubly-robust.md)
- [T23：从信息依赖图证明适应性和停止时间性质。](../evaluation-monitoring/T23-prefix-safety.md)

通用证明工具：P01、P03；见 [证明原语](../../通用证明原语.md)。

- [A Gentle Introduction to Conformal Prediction and Distribution-Free Uncertainty Quantification](../../proof_ref/foundations-2026-09/a-gentle-introduction-to-conformal-prediction-and-distribution-2107.07511/README.md) · [官方 arXiv](https://arxiv.org/abs/2107.07511)
- [Conformal Risk Control](../../proof_ref/foundations-2026-09/conformal-risk-control-2208.02814/README.md) · [官方 arXiv](https://arxiv.org/abs/2208.02814)
- [Distribution-Free Predictive Inference For Regression](../../proof_ref/core-theory-2026-09/distribution-free-predictive-inference-for-regression-1604.04173/README.md) · [官方 arXiv](https://arxiv.org/abs/1604.04173)

## 专项证明接口（2026-10-02）

- [T45：从 Lipschitz margin 或 Gaussian 平移事件推导指定范数的认证半径。](../generalization/T45-certified-robustness.md)
