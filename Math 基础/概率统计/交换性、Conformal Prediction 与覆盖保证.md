---
type: note
domain: math/statistics-conformal-prediction
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# 交换性、Conformal Prediction 与覆盖保证

假设你训练了一个回归模型，它预测明天温度是 $25^\circ$C。真正困难的问题不是再给一个小数位，而是：**怎样给出一个预测区间，并保证新观测以至少 90% 的概率落进去？**

Conformal prediction 的妙处在于：它不要求残差是高斯，也不要求基础模型正确。它主要依赖一个很朴素的对称性：如果校准样本与新样本可以交换位置，而算法无法辨认谁是“最后来的那一个”，那么新样本的异常程度在所有异常分数中的排名也是对称的。

可以把它想成把 $n$ 个校准学生和一个新学生的试卷混在一起、遮住名字后按“离谱程度”排序。新学生没有理由系统性地排在某个特殊名次。Conformal 的有限样本保证，本质上就是这条 rank symmetry。

## 知识依赖与证明导航

- 数学入口：[Math 基础目录](../Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md)、[AI 理论证明前置学习路线](../%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/AI%20%E7%90%86%E8%AE%BA%E8%AF%81%E6%98%8E%E5%89%8D%E7%BD%AE%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)。
- 概率基础：[概率论主干：联合、条件、期望与协方差](%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md)、[置信区间、假设检验与多重比较](%E7%BD%AE%E4%BF%A1%E5%8C%BA%E9%97%B4%E3%80%81%E5%81%87%E8%AE%BE%E6%A3%80%E9%AA%8C%E4%B8%8E%E5%A4%9A%E9%87%8D%E6%AF%94%E8%BE%83.md)。
- 证明语言：[量词、归纳、不变量与望远镜求和](../%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/%E9%87%8F%E8%AF%8D%E3%80%81%E5%BD%92%E7%BA%B3%E3%80%81%E4%B8%8D%E5%8F%98%E9%87%8F%E4%B8%8E%E6%9C%9B%E8%BF%9C%E9%95%9C%E6%B1%82%E5%92%8C.md)、[测度、条件期望、滤过与适应过程](%E6%B5%8B%E5%BA%A6%E3%80%81%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E3%80%81%E6%BB%A4%E8%BF%87%E4%B8%8E%E9%80%82%E5%BA%94%E8%BF%87%E7%A8%8B.md)。
- 泛化邻居：[算法稳定性、经验过程与 PAC-Bayes](../%E7%BB%9F%E8%AE%A1%E5%AD%A6%E4%B9%A0%E7%90%86%E8%AE%BA/%E7%AE%97%E6%B3%95%E7%A8%B3%E5%AE%9A%E6%80%A7%E3%80%81%E7%BB%8F%E9%AA%8C%E8%BF%87%E7%A8%8B%E4%B8%8E%20PAC-Bayes.md)。
- 核心模板：[T18：Split conformal marginal coverage](../../proofs/statistics/T18-split-conformal.md)。
- 定理规格：[P01：先分清 marginal 与 conditional](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p01-%E5%AE%9A%E7%90%86%E8%A7%84%E6%A0%BC%E5%85%88%E5%86%99%E9%87%8F%E8%AF%8D%E5%AF%B9%E8%B1%A1%E4%B8%8E%E5%A4%B1%E8%B4%A5%E6%96%B9%E5%BC%8F)。
- 邻近但不同的方法卡：[R04：without-replacement concentration](../../%E8%BF%91%E6%9C%9F%E9%A1%B6%E4%BC%9A%E7%90%86%E8%AE%BA%E6%A1%86%E6%9E%B6%EF%BC%882025-2026%EF%BC%89.md#r04-sampling-without-replacement%E4%BA%A4%E6%8D%A2%E6%95%8F%E6%84%9F%E5%BA%A6--efronstein--local-complexity)；它也利用置换结构，但不能代替 conformal 的 rank proof。
- 已核验原文：[Distribution-Free Predictive Inference 核验卡](../../proof_ref/core-theory-2026-09/distribution-free-predictive-inference-for-regression-1604.04173/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md)、[PDF p.7：full conformal theorem](../../proof_ref/core-theory-2026-09/distribution-free-predictive-inference-for-regression-1604.04173/paper.pdf#page=7)、[PDF p.10：split conformal theorem](../../proof_ref/core-theory-2026-09/distribution-free-predictive-inference-for-regression-1604.04173/paper.pdf#page=10)、[PDF p.42：rank-symmetry proofs](../../proof_ref/core-theory-2026-09/distribution-free-predictive-inference-for-regression-1604.04173/paper.pdf#page=42)。

## 1. Exchangeability：顺序不携带信息

随机变量 $Z_1,\ldots,Z_m$ 是 exchangeable（可交换）的，如果对任意排列 $\pi$，都有

$$
(Z_1,\ldots,Z_m)
\overset{d}{=}
(Z_{\pi(1)},\ldots,Z_{\pi(m)}).
$$

意思是：把编号重新洗牌，联合分布不变。编号只是标签，不代表时间、难度或不同来源。

### 1.1 IID 一定 exchangeable，但反过来不一定

- IID 样本当然可交换；
- 从有限总体中无放回抽取后再随机打乱，样本相关但仍可交换；
- de Finetti theorem 在无限序列等条件下把 exchangeability 联系到“给定潜变量后 IID”，但有限样本不能随便把它简化成 IID。

Conformal 的基础秩证明需要校准与测试 **scores** exchangeable，不一定需要完整的参数分布模型。普通 split 方法用独立训练得到的同一固定 score 逐点处理可交换的 calibration/test pairs，从而保留这种对称性；raw points 可交换本身还不够。

### 1.2 哪些数据通常不可交换

- 按时间采集、存在趋势的时间序列；
- 用户行为改变了后续推荐数据的在线系统；
- 训练医院与部署医院分布不同；
- 根据 calibration inputs 或 labels 非对称地选择模型或 score，破坏分数的交换性；
- 一个患者贡献许多记录，却把每条记录当独立样本。

“数据看起来差不多”不是 exchangeability 的证明。必须说明数据生成、抽样和算法使用数据的方式为何具有置换对称性。

## 2. Rank symmetry：为什么名次近似均匀

设 $S_1,\ldots,S_n,S_{n+1}$ 是 exchangeable nonconformity scores；分数越大表示越“不像训练分布中的正常样本”。若几乎必然没有 ties，则测试分数 $S_{n+1}$ 在 $n+1$ 个分数中的 rank 均匀分布于

$$
\{1,2,\ldots,n+1\}.
$$

因此对整数 $k$：

$$
\mathbb P\bigl(\operatorname{rank}(S_{n+1})\le k\bigr)
=\frac{k}{n+1}.
$$

这不是中心极限定理，也不是大样本近似；在 exchangeability 成立时，它是有限样本的组合对称性。

有 ties 时，rank 不再严格均匀。使用“ $\le$ 阈值”的常见构造仍给保守的至少覆盖；若需要精确等式，必须显式随机化 tie-breaking，不能假装 ties 不存在。

## 3. Nonconformity score：把“离谱”变成数字

回归中最简单的 score 是绝对残差：

$$
S(x,y)=|y-\hat\mu(x)|.
$$

给定阈值 $q$，预测集合为

$$
C(x)=\{y:S(x,y)\le q\}
=[\hat\mu(x)-q,\hat\mu(x)+q].
$$

还可以使用归一化残差、分类中的 $1-\hat p_y(x)$、APS/RAPS score 等。Conformal 校准的是所选 score 的 rank；它不会自动证明这个 score 高效、区间短或适合业务损失。

一个好的 score 往往让难样本得到更宽集合、容易样本得到更窄集合，但**coverage guarantee 与 efficiency 是两个问题**。

## 4. Full conformal：把候选标签也放进对称游戏

full conformal 对每个候选标签 $y$：

1. 把候选点 $(x_{n+1},y)$ 加入原数据；
2. 用对 $n+1$ 个点置换对称的程序拟合并计算所有 scores；
3. 比较候选点 score 与其余 scores，得到 conformal p-value；
4. 保留没有被判得过于异常的 $y$。

一种常见 p-value 形式是

$$
p_y
=\frac{1}{n+1}
\sum_{i=1}^{n+1}
\mathbf{1}\{S_i^{(y)}\ge S_{n+1}^{(y)}\}.
$$

然后令

$$
C(x_{n+1})=\{y:p_y>\alpha\}.
$$

full conformal 充分利用数据且对称性直观，但候选 $y$ 很多时可能需要反复拟合，计算昂贵。不同文献对严格/非严格不等号和随机 ties 有不同约定；证明与实现必须保持同一 convention。

## 5. Split conformal：一次训练，一次校准

split conformal 把数据分为互不重叠的两部分：

- training set：拟合模型并确定 score function；
- calibration set：只计算分数和阈值。

设 calibration scores 为

$$
s_i=S(x_i,y_i),\qquad i=1,\ldots,n,
$$

排序为 $s_{(1)}\le\cdots\le s_{(n)}$。对目标 miscoverage $\alpha$，取

$$
k=\left\lceil(n+1)(1-\alpha)\right\rceil,
$$

并定义

$$
q=
\begin{cases}
s_{(k)},&k\le n,\\
+\infty,&k=n+1.
\end{cases}
$$

最后输出

$$
C(x)=\{y:S(x,y)\le q\}.
$$

给定 proper-training data 与独立拟合随机性后，若模型与 score 只由这些信息确定，不使用任何 calibration pair，且 $n$ 个 calibration points 与新点在该条件下 exchangeable，便有

$$
\mathbb P\bigl(Y_{n+1}\in C(X_{n+1})\bigr)
\ge1-\alpha.
$$

只避开 calibration labels 仍不够：一个 score 可以记住 calibration inputs，对它们全部输出 0、对新输入输出 1，导致覆盖失败。[T18 的完整反例](../../proofs/statistics/T18-split-conformal.md#calibration-input-leakage) 展示了这个区别。

### 5.1 为什么分位数里是 $n+1$

测试 score 也是 rank 游戏中的一员，所以总共有 $n+1$ 个位置。若无 ties 且 $k\le n$，覆盖率实际为

$$
\frac{k}{n+1}
\in
\left[1-\alpha,
1-\alpha+\frac{1}{n+1}\right).
$$

若错误地直接取 calibration scores 的普通经验 $(1-\alpha)$ 分位数，可能少算测试点对应的有限样本修正，从而欠覆盖。

### 5.2 $k=n+1$ 不是程序崩了

当 calibration set 很小或要求覆盖极高时， $k$ 可能等于 $n+1$。此时没有第 $n+1$ 个 calibration order statistic；安全 convention 是 $q=+\infty$，返回整个标签空间。它很宽，但诚实地表达了“这么少的数据不足以给出有限阈值同时保证所需覆盖”。

## 6. 有限样本 marginal coverage 到底保证什么

上面的概率同时对 calibration sample 和新样本取：

$$
\mathbb P_{\text{calibration},(X_{new},Y_{new})}
\{Y_{new}\in C(X_{new})\}\ge1-\alpha.
$$

它叫 marginal coverage。它不等于：

$$
\mathbb P\{Y_{new}\in C(X_{new})\mid X_{new}=x\}
\ge1-\alpha
\quad\text{对每个 }x.
$$

举例：总体 90% 是容易样本、10% 是困难样本。一个方法可能在容易样本上覆盖 100%，在困难样本上覆盖 0%，总体仍有 90% marginal coverage。保证没有错，但它没有回答子群公平性或每个输入附近的可靠性。

还要区分：

- **unconditional/marginal over calibration**：标准有限样本结论；
- **conditional on the realized calibration set**：覆盖率本身通常是随机的，不自动恰好等于 $1-\alpha$；
- **conditional on $X=x$**：一般更强，在完全 distribution-free 且集合非平凡时通常不可能普遍保证。

## 7. Conditional coverage：为什么不能免费得到

对任意连续分布、有限样本且没有结构假设时，要求每个 $x$ 都有精确 conditional coverage，通常会迫使预测集合变得几乎处处非常宽，甚至没有实用价值。

想做更局部的保证，需要额外结构或改变目标，例如：

- 预先定义的 groups / Mondrian conformal；
- 局部平滑、密度或回归一致性假设下的渐近 conditional coverage；
- 只要求对概率质量足够大的子集近似成立；
- subgroup coverage、multivalid coverage 等不同规格。

关键不是在摘要中把 “marginal” 换成 “conditional”，而是明确新增了什么假设、保证对哪些集合成立、是否有限样本、区间代价多大。

## 8. Coverage 不等于 risk control

普通 conformal 控制的是 miss indicator：

$$
\ell(C(X),Y)=\mathbf{1}\{Y\notin C(X)\}.
$$

而实际任务可能关心：

- set size 或区间长度；
- false positive 数量；
- segmentation 中未覆盖像素比例；
- $\text{top-}k$ 候选集合的成本；
- 选择性预测中的错误率。

Risk-controlling prediction sets 会先定义损失、嵌套集合族和风险上置信界，再校准集合大小。它与 conformal rank 思想相关，但**不能由普通 coverage theorem 自动推出**。

因此看到“distribution-free risk control”时至少检查：loss 是否有界、候选集合是否嵌套、是期望风险还是高概率风险、是否在同一数据上选择超参数、使用了哪个 concentration theorem。

## 9. Distribution shift：交换性坏了怎么办

标准 split conformal 默认 calibration 与 test 来自同一可交换机制。部署时常见三种变化：

1. **Covariate shift**： $P_X$ 变了，但 $P_{Y\mid X}$ 不变；在 density ratio 可得且满足条件时，可用 weighted conformal。
2. **Label/concept shift**： $P_{Y\mid X}$ 也变了；只给 calibration scores 加权通常不够。
3. **Online/adaptive shift**：数据分布随时间或模型行动改变；需要 online conformal、martingale 或专门的 adaptive guarantee。

估计权重会引入额外误差；“double robust”也只在特定 nuisance assumptions 和相应 theorem 下成立，常常是渐近结论。不能把 vanilla split conformal 的 exact finite-sample guarantee 原样搬过去。

## 10. 可运行 NumPy 示例：看见 $n+1$ 修正

下面固定一个预测器 $\hat\mu(x)$，让 calibration 与 test residual IID 连续。真实模型形式并不重要；我们直接模拟 absolute residual score。

当 $n=20$、目标覆盖为 90% 时：

$$
k=\lceil21\times0.9\rceil=19.
$$

正确阈值是第 19 个 order statistic；若错误采用 $k=\lceil n(1-\alpha)\rceil$ 这一 order-statistic convention，就会取第 18 个，理论覆盖仅约 $18/21\approx85.7\%$。NumPy/R 的默认 quantile 还可能插值，不能笼统称为同一种“普通 quantile”。

```python
import numpy as np

rng = np.random.default_rng(23)
n_trials = 50_000
n_cal = 20
alpha = 0.10

# score = |Y - mu_hat(X)|；固定预测器可视为已在独立 training set 上训练好。
cal_scores = np.abs(rng.normal(size=(n_trials, n_cal)))
test_scores = np.abs(rng.normal(size=n_trials))

k = int(np.ceil((n_cal + 1) * (1.0 - alpha)))
assert k == 19

# np.partition 的索引从 0 开始，所以第 k 个 order statistic 用 k-1。
q_correct = np.partition(cal_scores, k - 1, axis=1)[:, k - 1]
coverage_correct = np.mean(test_scores <= q_correct)

# 常见错误：忘记测试点也占一个 rank，使用 ceil(n * (1-alpha))。
k_naive = int(np.ceil(n_cal * (1.0 - alpha)))
q_naive = np.partition(cal_scores, k_naive - 1, axis=1)[:, k_naive - 1]
coverage_naive = np.mean(test_scores <= q_naive)

print("correct k / empirical coverage:", k, coverage_correct)
print("naive k / empirical coverage:", k_naive, coverage_naive)
print("rank-theory targets:", k / (n_cal + 1), k_naive / (n_cal + 1))

assert coverage_correct >= 0.895  # Monte Carlo 允许少量波动。
assert coverage_naive < 0.88
```

代码验证的是 rank 机制，不是正态性特例：把连续 residual 换成其他 IID 连续分布，理论 rank 结论不变。

## 11. 在项目中正确实现 split conformal

```text
Step 1. 在看任何 calibration pair 之前，用 proper-training data 固定模型、score 与随机性。
Step 2. 只用 proper-training set 拟合模型；若方法要使用 calibration covariates，必须另证它对 calibration/test covariates 置换等变，或引用允许该用法的扩展 theorem。
Step 3. 在 calibration set 上计算 nonconformity scores。
Step 4. 用 k=ceil((n+1)(1-alpha)) 和明确的 +infinity/tie convention。
Step 5. 对新 x 返回 {y: S(x,y) <= q}。
Step 6. 用独立 audit data 检查总体与关键 subgroup 的经验覆盖和 set size。
Step 7. 若数据有时间、群组或 shift 结构，停止套 vanilla theorem，改用对应扩展。
```

经验 audit 不能替代 theorem，但能发现实现错误、数据泄漏和关键子群欠覆盖。应同时报告 coverage 与集合宽度；只报告 coverage，返回整个标签空间也能“完美得分”。

## 12. 常见误区

1. **“Conformal 证明模型是对的。”** 它校准 prediction set 的覆盖，不证明 $\hat\mu$ 或概率模型正确。
2. **“90% marginal coverage 表示每类样本都覆盖 90%。”** 子群和逐点 conditional coverage 可能差很多。
3. **“用 NumPy 的 0.9 quantile 就行。”** 必须核对 $(n+1)$ 有限样本修正、插值方式、索引和 ties。
4. **“Calibration set 可以反复调 score，只要最后再算一次 quantile。”** 根据同一批 calibration inputs 或 labels 选模型都可能破坏最简单的 rank argument；需要相应变体的额外证明。
5. **“区间越宽，uncertainty estimation 越准确。”** 整个实数轴覆盖率 100%，却没有信息；coverage 与 efficiency 要一起评估。
6. **“IID 是唯一能做 conformal 的条件。”** exchangeability 更一般；但相关、时序或 adaptive 数据也不会自动 exchangeable。
7. **“加 importance weights 就解决所有 distribution shift。”** weighted conformal 依赖具体 shift assumption 和权重条件，不能修复任意 concept drift。
8. **“Coverage theorem 就是 risk-control theorem。”** 两者损失、量词与校准步骤不同。

## 13. 自测

1. 用自己的话区分 IID 与 exchangeability，并举一个“exchangeable 但不独立”的例子。
2. 为什么测试点在分位数修正中贡献了那个额外的 $+1$？
3. 当 $k=n+1$ 时，为什么 $q=+\infty$ 是诚实而不是 bug？
4. 写出 marginal coverage 与以 $X=x$ 为条件的 coverage 的概率公式，并解释量词差异。
5. 为什么用 calibration labels 选择 score 后再校准可能失效？
6. 一个方法在 90% 样本上覆盖 100%、另 10% 上覆盖 0%，它满足 90% marginal coverage 吗？这说明了什么？
7. Covariate shift 与 concept shift 对 conformal 的影响为什么不同？

## 权威来源与延伸阅读

- Lei, G'Sell, Rinaldo, Tibshirani & Wasserman, [Distribution-Free Predictive Inference for Regression](https://doi.org/10.1080/01621459.2017.1307116), *JASA*, 2018；本地核验：[PDF p.10](../../proof_ref/core-theory-2026-09/distribution-free-predictive-inference-for-regression-1604.04173/paper.pdf#page=10)。
- Vovk, Gammerman & Shafer, *Algorithmic Learning in a Random World*, Springer, 2005。
- Angelopoulos & Bates, [Conformal Prediction: A Gentle Introduction](https://arxiv.org/abs/2107.07511), 2021/2023。
- Barber, Candès, Ramdas & Tibshirani, [The Limits of Distribution-Free Conditional Predictive Inference](https://doi.org/10.1093/imaiai/iaaa017), *Information and Inference*, 2021。
- Tibshirani, Barber, Candès & Ramdas, [Conformal Prediction Under Covariate Shift](https://proceedings.neurips.cc/paper/2019/hash/8fb21ee7a2207526da55a679f0332de2-Abstract.html), NeurIPS 2019。
- Bates, Angelopoulos, Lei, Malik & Jordan, [Distribution-Free, Risk-Controlling Prediction Sets](https://arxiv.org/abs/2101.02703), 2021。
