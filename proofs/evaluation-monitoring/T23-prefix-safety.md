---
id: T23
type: proof-template
refined: 2026-09-28
status: "refined-lemma"
---

# T23. Prefix-safety / adaptedness / filtration measurability

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

从信息依赖图证明适应性和停止时间性质。

## 复用契约

**输入对象**：预先资源、算法随机性、交互历史、filtration、状态更新与停止规则。

**输出结论**：可测性/停止时间结论；不自动给出随时有效的统计错误率。

**必需假设**：

- 所有处理节点只读当时允许的信息，预处理/调参不含测试未来。
- 独立预采样 random tape 可放入 F0；未来环境观测/标签不能偷放。
- 浓缩定理的 martingale 条件须对选定 filtration 重新检查。

**失败例子**：用全 test trajectory 选阈值，即使 score 只读 prefix，阈值也已泄漏未来。

## 实例化时必须完成

- [ ] 列信息出现时间与处理节点。
- [ ] 归纳状态和 score 可测性。
- [ ] 证明 {τ≤t}∈F_t 后，再单独做统计错误控制。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [filtration/adapted/predictable](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%B5%8B%E5%BA%A6%E3%80%81%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E3%80%81%E6%BB%A4%E8%BF%87%E4%B8%8E%E9%80%82%E5%BA%94%E8%BF%87%E7%A8%8B.md#9-filtration%E4%BF%A1%E6%81%AF%E9%9A%8F%E6%97%B6%E9%97%B4%E5%A2%9E%E9%95%BF) · [量词、归纳、不变量与望远镜求和](../../Math%20%E5%9F%BA%E7%A1%80/%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/%E9%87%8F%E8%AF%8D%E3%80%81%E5%BD%92%E7%BA%B3%E3%80%81%E4%B8%8D%E5%8F%98%E9%87%8F%E4%B8%8E%E6%9C%9B%E8%BF%9C%E9%95%9C%E6%B1%82%E5%92%8C.md)

## 适用场景

online evaluation、LLM prefix monitoring、streaming classifier、early stopping、agent intervention。你需要证明某个 score 在时间 `t` 没有使用未来信息。

## 核心定义

令 $\Theta_{\mathrm{pre}}$ 包含测试开始前已经固定的参数、calibrator 和特征变换；令 $U_{0:t}$ 表示截至 $t$ 已揭示的算法随机性，并令 $H_t$ 包含截至 $t$ 的 observations、actions 与 tool outputs。定义

$$
\mathcal F_t=\sigma(\Theta_{\mathrm{pre}},U_{0:t},H_t),
\qquad
\mathcal F_{t-1}\subseteq\mathcal F_t.
$$

prefix-safe 要求 $\widehat s_t$ 只由测试前固定资源和当前 prefix 通过可测映射生成，即

$$
\hat s_t \text{ is } \mathcal{F}_t\text{-measurable}.
$$

若在线状态满足

$$
h_0=\phi_0(\Theta_{\mathrm{pre}},U_0),
\qquad
h_t=\phi_t(h_{t-1},H_t,U_t),
\qquad
\widehat s_t=\psi_t(h_t,H_t),
$$

且 $\phi_t,\psi_t$ 均在测试前固定并可测，则可用归纳证明 $h_t,\widehat s_t$ 为 $\mathcal F_t$-可测。

若 action 在看到本轮 observation 前选择，时序还应写成 $A_t$ 对 $\mathcal F_{t-1}\vee\sigma(U_t)$ 可测，随后把 $O_t$ 和本轮 score 加入 $\mathcal F_t$。

对固定或 $\mathcal F_0$-可测阈值 $c$，

$$
\tau=\inf\{t\ge0:\widehat s_t\ge c\},
\qquad
\{\tau\le t\}=\bigcup_{k=0}^t\{\widehat s_k\ge c\}\in\mathcal F_t,
$$

所以 $\tau$ 是 stopping time。任意依赖完整轨迹后处理的“最佳停止点”不满足这个论证。

<a id="t23-adaptedness"></a>

^t23-adaptedness

## 逐步证明模板

```text
Step 1. 列举 Theta_pre、初始状态、算法随机性、actions、observations 与 tool outputs。
Step 2. 定义完整 filtration F_t，并验证 filtration 单调性。
Step 3. base case：h_0 / score_0 只依赖 F_0 中的变量。
Step 4. induction：假设 h_{t-1} 是 F_{t-1}-measurable，因此也是 F_t-measurable。
Step 5. 当前 update 是 pre-fixed measurable map，且只读 F_t 中的当前 prefix，所以 h_t 和 score_t 是 F_t-measurable。
Step 6. 审计特征计算链；若任一步读 future-token hidden state、完整 trajectory 或 test-set 调参结果，证明失败。
Step 7. 若定义 early-stopping time tau，再证明 {tau <= t} in F_t；adapted score 本身还不足以推出任意停止规则都是 stopping time。
Step 8. 说明 smoothing / full-trace decoder 依赖 future observations，因此不是 F_t-measurable。
```

## 可迁移用法

- 证明 early stopping 阈值没有偷看 final answer。
- 证明 hidden-state feature 只用 prefix hidden states。
- 区分 online filtering 与 offline smoothing。

## 常见坑

- calibration map 可以用 calibration labels，但必须 test 前固定。
- 如果 feature extraction 使用 future token hidden states，就不是 prefix-safe。
- 如果 threshold 根据 test performance 调整，也不是 prefix-safe。
- 可以预先采样独立于数据/环境创新的整个算法 random tape，并把它放入 $\mathcal F_0$；也可以逐步揭示随机性。两种约定都可用，但后续 martingale 条件必须对所选 filtration 重新验证。不可将未知的未来环境观测或标签伪装成算法随机性。
- 对交互式 agent，只记录 observations 而遗漏 actions/tool outputs，通常不是完整 filtration。
- “测试前固定”不自动排除泄漏：还要确认 $\Theta_{\mathrm{pre}}$ 的预处理、缓存和调参没有读到当前测试 trajectory 的未来 observations/labels。

## 来源论文 / 参考

- Bayesian Filtering and Smoothing, Särkkä, 2013. https://users.aalto.fi/~ssarkka/pub/cup_book_online_20131111.pdf
- HMM filtering/smoothing distinction: Rabiner tutorial. https://www.cs.ubc.ca/~murphyk/Bayes/rabiner.pdf
- Online learning notation and adaptedness appear broadly in online learning / stochastic process analyses; see Shalev-Shwartz survey. https://www.cs.huji.ac.il/~shais/papers/OLsurvey.pdf

## 关联模板与本地证据

- [T21：结合预测先验与当前 likelihood，区分静态和动态状态证据累积。](T21-bayesian-filtering.md)
- [T18：用交换性和名次对称性证明边际覆盖。](../statistics/T18-split-conformal.md)
- [T16：把裁剪梯度分成 centered martingale 与 clipping bias。](../optimization/T16-heavy-tail-clipping.md)

通用证明工具：P01、P02、P04；见 [证明原语](../../通用证明原语.md)。

- [Time-uniform Chernoff bounds via nonnegative supermartingales](../../proof_ref/foundations-2026-09/time-uniform-chernoff-bounds-via-nonnegative-supermartingales-1808.03204/README.md) · [官方 arXiv](https://arxiv.org/abs/1808.03204)
- [Time-uniform, nonparametric, nonasymptotic confidence sequences](../../proof_ref/foundations-2026-09/time-uniform-nonparametric-nonasymptotic-confidence-sequences-1810.08240/README.md) · [官方 arXiv](https://arxiv.org/abs/1810.08240)
