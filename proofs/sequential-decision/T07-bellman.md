---
id: T07
type: proof-template
refined: 2026-10-20
status: "refined + claim-checked"
---

# T07. Bellman telescoping: online optimism and offline pessimism

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

在正确策略的 occupancy 下展开 Bellman 价值误差。

## 复用契约

**输入对象**：有限时域 MDP、真实转移、策略、初始分布、fitted value 和 residual。

**输出结论**：精确 residual 恒等式；统计假设补齐后才有 regret/suboptimality。

**必需假设**：

- terminal value、reward 与 Bellman operator 定义完整。
- 每个期望注明真实 occupancy。
- confidence/realizability/coverage 与规划误差另行控制。

**失败例子**：数据分布上残差为零，目标策略却访问未覆盖区域，价值误差仍可能很大。

## 实例化时必须完成

- [ ] 逐层加减并检查边界项。
- [ ] 拆开估计误差和规划误差。
- [ ] 分布切换显式支付 coverage 代价。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> 仓库内学习路线：[条件概率与期望](<../../Math 基础/概率统计/概率论主干：联合、条件、期望与协方差.md>) → [Markov 链与受控转移](<../../Math 基础/概率统计/Markov 链、随机过程与状态空间模型.md>) → [条件期望的 tower property](<../../Math 基础/概率统计/测度、条件期望、滤过与适应过程.md>) → 本页的 MDP 定义与 Bellman 推导。统计误差另读 [浓缩工具](<../../Math 基础/概率统计/集中不等式、MGF、鞅与自归一化过程.md>)。

## 适用场景

有限时域 episodic MDP 中的 regret、policy suboptimality 与 fitted value error。用于 linear MDP 或 offline RL 前，必须另外写明 realizability、coverage、noise model 和 good event。

## 从 Markov 链到 Bellman：最短前置推导

先看有限状态、有限动作、长度为 $H$ 的情形。第 $h$ 步在状态 $s$ 按 Markov 策略 $\pi_h(a\mid s)$ 选择动作，再按真实转移 $P_h(s'\mid s,a)$ 进入下一状态；期望即时奖励为 $r_h(s,a)$。假设奖励有界，下面的有限和与期望都存在。固定初始状态 $s_1$ 后，这些规则唯一确定整条轨迹的分布，$d_h^\pi(s,a)=\Pr_\pi(s_h=s,a_h=a\mid s_1)$ 就是第 $h$ 步“走到哪里、采取什么动作”的概率。

价值 $V_h^\pi(s)$ 是从状态 $s$ 开始、继续按 $\pi$ 行动的预期剩余总奖励；$Q_h^\pi(s,a)$ 则先固定这一步的动作 $a$，以后再跟随 $\pi$。终点没有剩余奖励，所以 $V_{H+1}^\pi=0$。将第一步奖励从有限总和中取出，再用条件期望，得到

$$
Q_h^\pi(s,a)=r_h(s,a)+\sum_{s'}P_h(s'\mid s,a)V_{h+1}^\pi(s'),
\qquad
V_h^\pi(s)=\sum_a\pi_h(a\mid s)Q_h^\pi(s,a).
$$

这就是 Bellman 递推：今天的价值等于今天所得，加上明天价值的平均。$A_h^\pi(s,a)=Q_h^\pi(s,a)-V_h^\pi(s)$ 表示强制选动作 $a$ 比照常按 $\pi$ 选动作好多少。先理解这个含义，再区分真实 $V^\pi,Q^\pi$ 与算法估计的 $\widehat V,\widehat Q$。

对一般可测空间，把上面的求和改成转移核积分，并另行确认条件分布、可测性和可积性。以下等式使用固定 Markov 策略；若策略依赖额外历史，应扩充状态或改用历史条件化的价值函数。

可选补充：[旧笔记库中的 MDP 与时序差分学习](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E5%BC%BA%E5%8C%96%E5%AD%A6%E4%B9%A0/%E5%9F%BA%E7%A1%80/MDP%E3%80%81Bellman%20%E6%96%B9%E7%A8%8B%E4%B8%8E%E6%97%B6%E5%BA%8F%E5%B7%AE%E5%88%86%E5%AD%A6%E4%B9%A0.md) 可能需要访问权限；上面的仓库内路线与本页推导不依赖该链接。

## 核心思想

先固定对象。把 $r_h(s,a)$ 定义为给定 $(s,a)$ 的条件期望 reward。对任意策略 $\pi$ 和任意函数列 $\widehat V_1,\dots,\widehat V_{H+1}$（$\widehat V_{H+1}=0$），定义沿 $\pi$ 的 Bellman residual

$$
\delta_h^{\pi}(s,a)
=
\widehat V_h(s)-r_h(s,a)
-\mathbb E_{s'\sim P_h(\cdot\mid s,a)}[\widehat V_{h+1}(s')].
$$

则由逐层加减并望远镜求和，得到精确恒等式

$$
\begin{aligned}
\sum_{h=1}^H\mathbb E_\pi\delta_h^\pi(s_h,a_h)
&=\sum_{h=1}^H\left(\mathbb E_\pi\widehat V_h(s_h)
-\mathbb E_\pi r_h(s_h,a_h)-\mathbb E_\pi\widehat V_{h+1}(s_{h+1})\right)\\
&=\widehat V_1(s_1)-\mathbb E_\pi\sum_{h=1}^H r_h(s_h,a_h).
\end{aligned}
$$

第一步使用真实转移下的 tower property；第二步相邻价值项抵消，并使用 $\widehat V_{H+1}=0$。因此

$$
\widehat V_1(s_1)-V_1^{\pi}(s_1)
=
\sum_{h=1}^H
\mathbb E_{(s_h,a_h)\sim d_h^{\pi}}
[\delta_h^{\pi}(s_h,a_h)].
$$

这里 $d_h^{\pi}$ 是**该策略在真实 MDP 中**第 $h$ 步的 occupancy。不能省略 residual 的定义，也不能把 $d_h^{\pi}$ 换成另一个策略的 occupancy。

另一条独立工具是 performance-difference lemma：

$$
V_1^{\pi'}(s_1)-V_1^{\pi}(s_1)
=
\sum_{h=1}^H
\mathbb E_{(s_h,a_h)\sim d_h^{\pi'}}[A_h^{\pi}(s_h,a_h)].
$$

若初始状态随机，则等式两侧都再对同一个初始分布取期望。它使用**真实 advantage** $A_h^{\pi}=Q_h^{\pi}-V_h^{\pi}$，不是任意 fitted-Q residual。

## 逐步证明模板：online optimism

```text
Step 1. 明确 MDP、horizon、策略、估计量、occupancy 与 filtration。
Step 2. 构造 Q_hat_h = empirical Bellman backup + bonus，并定义 V_hat_h。
Step 3. 在统一 good event 上用 backward induction 证明 V_hat_h >= V_h*。
Step 4. 对算法实际执行的 pi_k 使用上面的 Bellman telescoping 恒等式。
Step 5. 将 residual 拆成 bonus、估计误差与 martingale difference。
Step 6. 用 concentration 控制 martingale，用 visitation / elliptical potential 控制 bonus sum。
Step 7. 对 episode 求和，并计入 good event 失败概率。
```

## 逐步证明模板：offline pessimism

```text
Step 1. 明确数据分布 mu、comparator pi^dagger 与 coverage/concentrability 条件。
Step 2. 构造带 penalty 的 pessimistic value，并说明截断和函数类。
Step 3. 在 good event 上证明对目标策略类的 pointwise 或 occupancy-weighted lower bound。
Step 4. 令 pi_hat 最大化 pessimistic value。
Step 5. 插入 comparator 的 pessimistic value，分成 planning error 与 estimation error。
Step 6. 在 d_h^{pi^dagger} 下用 coverage / covariance norm 控制 residual。
Step 7. 得到 data-dependent suboptimality bound；不能把训练分布下误差直接当作 comparator occupancy 下误差。
```

## 可迁移用法

- RLHF：只有给出 preference-to-reward 模型（例如 Bradley–Terry）及 Markov/state 假设后，才能把 preference 数据接到 RL decomposition；KL 几何另见 T08。
- agent evaluation：offline trajectory 数据不足时，用 pessimism 避免 OOD action exploitation。
- simulation-based optimization：未覆盖状态区域用 penalty。

## 常见坑

- offline RL 常用 pessimism 抑制 OOD value error，但“offline 绝不能 optimism”不是定理；结论取决于算法与可覆盖区域。
- coverage assumption 是 offline RL 的命门，要清楚写出。
- Bellman residual 的 expectation 是在哪个 occupancy 下取的，必须明确。
- $\widehat V\ge V^\star$ 或 $\widehat V\le V^\pi$ 都需要明确 good event、Bellman operator、截断及 backward induction，不能当作定义。

## 来源论文 / 参考

- Minimax Regret Bounds for Reinforcement Learning / UCBVI, ICML 2017. https://proceedings.mlr.press/v70/azar17a.html
- Provably Efficient Reinforcement Learning with Linear Function Approximation / LSVI-UCB, COLT 2020. https://proceedings.mlr.press/v125/jin20a.html
- 本地核验：[LSVI-UCB 核验卡](../../proof_ref/core-theory-2026-09/provably-efficient-reinforcement-learning-with-linear-function-approximation-1907.05388/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md) · [PDF](../../proof_ref/core-theory-2026-09/provably-efficient-reinforcement-learning-with-linear-function-approximation-1907.05388/paper.pdf#page=5)
- Is Pessimism Provably Efficient for Offline RL?, ICML 2021. https://proceedings.mlr.press/v139/jin21e.html
- A Unified Principle of Pessimism for Offline Reinforcement Learning, NeurIPS 2024. https://proceedings.neurips.cc/paper_files/paper/2024/hash/119b45b5c2020d6bc9bca1e42826a2b3-Abstract-Conference.html
- Bellman-consistent Pessimism for Offline Reinforcement Learning, NeurIPS 2021. https://openreview.net/forum?id=e8WWUBeafM

## 关联模板与本地证据

- [T06：用置信椭球、optimism 与 elliptical potential 控制 pseudo-regret。](T06-linear-bandit.md)
- [T08：用三点恒等式与 Bregman 几何分析在线/策略更新。](T08-mirror-descent.md)
- [T11：用残差校正把 nuisance 的一阶误差变成乘积余项。](../statistics/T11-doubly-robust.md)

通用证明工具：P02、P03、P04；见 [证明原语](../../通用证明原语.md)。

- [Provably Efficient Reinforcement Learning with Linear Function Approximation](../../proof_ref/core-theory-2026-09/provably-efficient-reinforcement-learning-with-linear-function-approximation-1907.05388/README.md) · [官方 arXiv](https://arxiv.org/abs/1907.05388)
- [Is Pessimism Provably Efficient for Offline RL?](../../proof_ref/foundations-2026-09/is-pessimism-provably-efficient-for-offline-rl-2012.15085/README.md) · [官方 arXiv](https://arxiv.org/abs/2012.15085)
- [Trust Region Policy Optimization](../../proof_ref/foundations-2026-09/trust-region-policy-optimization-1502.05477/README.md) · [官方 arXiv](https://arxiv.org/abs/1502.05477)
