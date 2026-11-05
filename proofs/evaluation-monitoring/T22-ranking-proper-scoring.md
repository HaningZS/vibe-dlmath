---
id: T22
type: proof-template
refined: 2026-09-28
status: "refined-algebra"
---

# T22. Metric algebra: AUROC vs Brier / proper scoring

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

分开证明 AUROC 排序不变性与 Brier proper-scoring 分解。

## 复用契约

**输入对象**：正负样本、score/概率、严格递增映射与总体条件概率。

**输出结论**：保序不变性和总体 Brier excess-risk 恒等式；不是经验模型已经校准的证书。

**必需假设**：

- AUROC 正负类都非空，ties 约定明确。
- 严格递增保序；非严格变换可能合并分数。
- Brier 输入在 [0,1]，总体 properness 与经验改善分开。

**失败例子**：常数变换把所有正负对变平局，可使 AUROC 从 1 降到 0.5。

## 实例化时必须完成

- [ ] 写 pairwise 定义。
- [ ] 另按 Y|X 展开平方风险。
- [ ] 指标、校准和显著性分别给证据。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [概率论主干：联合、条件、期望与协方差](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md) · [信息论基础：熵、交叉熵与 KL 散度](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E4%BF%A1%E6%81%AF%E8%AE%BA%E5%9F%BA%E7%A1%80%EF%BC%9A%E7%86%B5%E3%80%81%E4%BA%A4%E5%8F%89%E7%86%B5%E4%B8%8E%20KL%20%E6%95%A3%E5%BA%A6.md) · [置信区间、假设检验与多重比较](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E7%BD%AE%E4%BF%A1%E5%8C%BA%E9%97%B4%E3%80%81%E5%81%87%E8%AE%BE%E6%A3%80%E9%AA%8C%E4%B8%8E%E5%A4%9A%E9%87%8D%E6%AF%94%E8%BE%83.md)

## 适用场景

解释“ranking 变好”和“概率校准变好”不是一回事。适合 evaluation section、calibration section、reliability paper、monitoring paper。

## AUROC pairwise 形式

令 $P$ 是 positive 样本集合， $N$ 是 negative 样本集合，并要求 $|P|,|N|>0$：

$$
\mathrm{AUROC}(r,y)
=\frac{1}{|P||N|}
\sum_{i\in P}\sum_{j\in N}
\left[\mathbf{1}\lbrace r_i>r_j\rbrace+\frac12\mathbf{1}\lbrace r_i=r_j\rbrace\right].
$$

如果 `g` 严格单调递增，则 pairwise order 不变：

$$
\mathrm{AUROC}(g(r),y)=\mathrm{AUROC}(r,y).
$$

## Brier score

对二分类概率预测 $\widehat p_i\in[0,1]$，

$$
\mathrm{Brier}(\hat p,y)
=\frac{1}{n}\sum_i(\hat p_i-y_i)^2.
$$

Brier 对概率数值敏感，而不仅仅对排序敏感。

更重要的是它是 strictly proper scoring rule。若 $p(x)=\mathbb P(Y=1\mid X=x)$，则任意 $q\in[0,1]$ 满足

$$
\mathbb E[(q-Y)^2\mid X=x]
=(q-p(x))^2+p(x)(1-p(x)).
$$

因此条件期望 Brier risk 在 $q=p(x)$ 处唯一最小。这个结论说明诚实概率最优，但不意味着有限样本上的某个模型已经 calibrated。

总体上，若 $R_{\mathrm{Brier}}(q)=\mathbb E[(q(X)-Y)^2]$，则

$$
R_{\mathrm{Brier}}(q)-R_{\mathrm{Brier}}(p)
=\mathbb E[(q(X)-p(X))^2]\ge0,
$$

等号当且仅当 $q(X)=p(X)$ almost surely。

<a id="t22-brier-proper"></a>

^t22-brier-proper

## 逐步证明模板

```text
Step 1. 写 AUROC 的 pairwise definition。
Step 2. 对任意 positive-negative pair，证明严格单调变换保持 >, =, <。
Step 3. 因此每个 pair contribution 不变。
Step 4. 求和得到 AUROC 不变。
Step 5. 写 Brier 定义。
Step 6. 展开 conditional Brier risk，得到 proper-scoring decomposition。
Step 7. 给一个两点例子，说明严格单调变换可保持 AUROC 但改变 Brier。
Step 8. 将“应分开报告 ranking 与 probability quality”明确标为评估建议，而不是由代数自动推出的总体性能结论。
```

## 常见坑

- 非严格单调函数可能合并分数产生 ties，从而改变 AUROC tie contribution。
- empirical AUROC 在正类或负类为空时未定义。
- Brier 输入必须是 $[0,1]$ 中的概率；对任意 score 直接计算不具有 proper-scoring 含义。
- Brier 改善不代表 ranking 改善。
- AUROC 改善不代表概率 calibrated。

## 来源论文 / 参考

- An Introduction to ROC Analysis, Fawcett, 2006. https://www.sciencedirect.com/science/article/abs/pii/S016786550500303X
- A Simple Generalisation of the Area Under the ROC Curve for Multiple Class Classification Problems, Hand & Till, 2001. https://doi.org/10.1023/A:1010920819831
- Verification of Forecasts Expressed in Terms of Probability, Brier, 1950. https://journals.ametsoc.org/view/journals/mwre/78/1/1520-0493_1950_078_0001_vofeit_2_0_co_2.xml
- Strictly Proper Scoring Rules, Prediction, and Estimation, Gneiting & Raftery, 2007. https://doi.org/10.1198/016214506000001437

## 关联模板与本地证据

- [T17：将 calibration 连接到特定在线问题的成本分解。](T17-calibrated-predictions.md)
- [T24：记录方法超过多种 baseline 的经验数值关系。](T24-baseline-gap.md)

通用证明工具：P01；见 [证明原语](../../通用证明原语.md)。

## 专项证明接口（2026-10-02）

- [T49：由 binary log-loss excess 推到分类 excess，并保留模型与裁剪误差。](../generalization/T49-surrogate-bayes-risk.md)
