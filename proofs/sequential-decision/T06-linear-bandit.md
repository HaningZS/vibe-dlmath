---
id: T06
type: proof-template
refined: 2026-09-28
status: "refined + claim-checked"
---

# T06. Optimism + self-normalized concentration + elliptical potential

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

用置信椭球、optimism 与 elliptical potential 控制 pseudo-regret。

## 复用契约

**输入对象**：可预测 x_t、线性参数、噪声、ridge V_t 和 UCB action。

**输出结论**：good event 上的 mean-reward pseudo-regret；realized regret 还需噪声项。

**必需假设**：

- 线性 realizability、范数界与条件 sub-Gaussian 噪声。
- λ>0，feature 在当前反馈前可测。
- 截断的椭圆势和未截断 uncertainty 求和之间需合法连接。

**失败例子**：先观察本轮噪声再选择 feature，置信椭球的 predictable 条件失效。

## 实例化时必须完成

- [ ] 保留 ridge bias 与 log-det radius。
- [ ] 在统一事件上证明 optimism。
- [ ] 用归一化条件或明确截断机制完成 regret 求和。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [集中不等式、MGF、鞅与自归一化过程](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E9%9B%86%E4%B8%AD%E4%B8%8D%E7%AD%89%E5%BC%8F%E3%80%81MGF%E3%80%81%E9%9E%85%E4%B8%8E%E8%87%AA%E5%BD%92%E4%B8%80%E5%8C%96%E8%BF%87%E7%A8%8B.md) · [矩阵浓缩、谱扰动与子空间误差](../../Math%20%E5%9F%BA%E7%A1%80/%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E7%9F%A9%E9%98%B5%E6%B5%93%E7%BC%A9%E3%80%81%E8%B0%B1%E6%89%B0%E5%8A%A8%E4%B8%8E%E5%AD%90%E7%A9%BA%E9%97%B4%E8%AF%AF%E5%B7%AE.md) · [测度、条件期望、滤过与适应过程](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%B5%8B%E5%BA%A6%E3%80%81%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E3%80%81%E6%BB%A4%E8%BF%87%E4%B8%8E%E9%80%82%E5%BA%94%E8%BF%87%E7%A8%8B.md)

## 适用场景

linear bandit、contextual bandit、linear reward model、linear preference model、linear RL 的基础模板。

## 核心结构

令 $x_t$ 在选择 action 时为 $\mathcal F_{t-1}$-可测，并假设

$$
y_t=\langle x_t,\theta_\star\rangle+\varepsilon_t,
\qquad
\mathbb E[e^{u\varepsilon_t}\mid\mathcal F_{t-1}]\le e^{u^2R^2/2},
\qquad
\Vert\theta_\star\Vert_2\le S,
\quad
\Vert x_t\Vert_2\le L_x.
$$

设计矩阵：

$$
V_t = \lambda I + \sum_{\tau< t} x_\tau x_\tau^\top.
$$

least-squares estimator：

$$
\hat\theta_t = V_t^{-1}\sum_{\tau< t}x_\tau y_\tau.
$$

self-normalized concentration 给出一个常用的 simultaneous confidence radius：以至少 $1-\delta$ 的概率，对所有 $t$，

$$
\Vert\hat\theta_t-\theta_\star\Vert_{V_t}
\le
\beta_t(\delta)
:=
R\sqrt{2\log\frac{\det(V_t)^{1/2}}{\det(\lambda I)^{1/2}\delta}}
+\sqrt\lambda S.
$$

optimistic action：

$$
a_t
=\arg\max_a
\max_{\theta:\Vert\theta-\hat\theta_t\Vert_{V_t}\le\beta_t}
\langle x(a),\theta\rangle.
$$

在这个 good event 上，若线性模型 realizable 且 $a_t$ 最大化 UCB，mean-reward pseudo-regret 满足

$$
\langle x(a_t^\star)-x_t,\theta_\star\rangle
\le
2\beta_t\Vert x_t\Vert_{V_t^{-1}}.
$$

这不是含 observation noise 的 realized regret 恒等式。Elliptical potential 的精确常用形式是

$$
\sum_{t=1}^T \min\lbrace1,\Vert x_t\Vert_{V_t^{-1}}^2\rbrace
\le
2\log\frac{\det(V_{T+1})}{\det(V_1)}
\le
2d\log\left(1+\frac{TL_x^2}{\lambda d}\right).
$$

<a id="t06-linear-bandit-confidence"></a>

^t06-linear-bandit-confidence

## 逐步证明模板

### 从截断的椭圆势到未截断的 regret

必须补上 $\lambda>0$。若进一步选 $\lambda\geq L_x^2$，则
$\Vert x_t\Vert_{V_t^{-1}}\leq1$，此时 $\min\lbrace1,\Vert x_t\Vert_{V_t^{-1}}^2\rbrace$ 才能直接去掉。由 Cauchy–Schwarz 和 $\beta_t$ 单调性，

$$
\mathop{\mathrm{PseudoRegret}}(T)
\leq
2\beta_{T+1}
\sqrt{2Td\log\negthinspace\left(1+\frac{TL_x^2}{\lambda d}\right)}.
$$

若不采用这一归一化，必须另外处理大 uncertainty 的步，或使用带额外系数的未截断求和界；不能只从截断势函数公式跳到上述 rate。

```text
Step 1. 写出线性模型假设 y_t = <x_t, theta*> + noise_t。
Step 2. 构造 V_t 和 theta_hat_t。
Step 3. 用 self-normalized martingale inequality 得到 good event。
Step 4. 在 good event 上证明 true theta 在 confidence set 内。
Step 5. 用 optimism 证明 chosen action 的 optimistic value >= optimal action true value。
Step 6. 把 regret 上界为 uncertainty radius。
Step 7. 用 elliptical potential lemma 求和。
Step 8. 得到 regret bound。
```

## 可迁移用法

- preference learning：`x(a,b)` 是两个 response 的特征差。
- recommendation：`x(user,item)` 是上下文特征。
- LLM agent exploration：每个 tool/action 有 feature embedding。
- online clustering bandit：在 cluster 正确后，对每个 cluster 套这个模板。

## 常见坑

- noise 需要 martingale/sub-Gaussian 或可替代 heavy-tail 处理。
- feature 必须是 action 选择前可见，不能用 post-action 信息。
- 如果模型 misspecified，要加 misspecification bias。
- Pairwise Bradley--Terry/logistic preference 不是高斯线性 bandit；需要 GLM confidence set 或局部 curvature，不能只把 feature 换成 response difference。
- Embedding 相似度不自动给 linear realizability；需要单独的 approximation-error 假设。

## 来源论文 / 参考

- Improved Algorithms for Linear Stochastic Bandits, NeurIPS 2011. https://papers.nips.cc/paper/4417-improved-algorithms-for-linear-stochastic-bandits
- Bandit Algorithms, Lattimore & Szepesvári, Cambridge University Press. https://tor-lattimore.com/downloads/book/book.pdf
- Time-uniform 向量浓缩：[核验笔记](../../proof_ref/recent-accepted-2025-2026/time-uniform-self-normalized-concentration-for-vector-valued-2310.09100/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md) · [PDF](../../proof_ref/recent-accepted-2025-2026/time-uniform-self-normalized-concentration-for-vector-valued-2310.09100/paper.pdf#page=7)
- Average-reward linear MDP 特化：[核验笔记](../../proof_ref/recent-accepted-2025-2026/reinforcement-learning-for-infinite-horizon-average-reward-linear-2405.15050/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md) · [PDF](../../proof_ref/recent-accepted-2025-2026/reinforcement-learning-for-infinite-horizon-average-reward-linear-2405.15050/paper.pdf#page=5)

## 关联模板与本地证据

- [T07：在正确策略的 occupancy 下展开 Bellman 价值误差。](T07-bellman.md)
- [T08：用三点恒等式与 Bregman 几何分析在线/策略更新。](T08-mirror-descent.md)
- [T12：由困难实例的不可区分性推出指定算法类的风险下界。](../lower-bounds-expressivity/T12-information-lower-bounds.md)

通用证明工具：P03、P04、P08；见 [证明原语](../../通用证明原语.md)。

- [Online Least Squares Estimation with Self-Normalized Processes: An Application to Bandit Problems](../../proof_ref/foundations-2026-09/online-least-squares-estimation-with-self-normalized-processes-1102.2670/README.md) · [官方 arXiv](https://arxiv.org/abs/1102.2670)
- [Regret Analysis of Stochastic and Nonstochastic Multi-armed Bandit Problems](../../proof_ref/foundations-2026-09/regret-analysis-of-stochastic-and-nonstochastic-multi-armed-1204.5721/README.md) · [官方 arXiv](https://arxiv.org/abs/1204.5721)
- [Time-Uniform Self-Normalized Concentration for Vector-Valued Processes](../../proof_ref/recent-accepted-2025-2026/time-uniform-self-normalized-concentration-for-vector-valued-2310.09100/README.md) · [官方 arXiv](https://arxiv.org/abs/2310.09100)
