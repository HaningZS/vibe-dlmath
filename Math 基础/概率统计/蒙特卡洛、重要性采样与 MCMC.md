---
type: note
domain: math/probability-computation
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# 蒙特卡洛、重要性采样与 MCMC

证明进阶：[T41 用 Hilbert-space 方差证明随机特征逼近](../../proofs/deep-learning/T41-barron-random-feature-approximation.md) · [从抽样到学习风险的完整例子](../../docs/END_TO_END_LEARNING_PROOF.md)。

很多概率计算最终都长成一个难积分：

$$
I=\mathbb E_{X\sim p}[f(X)]=\int f(x)p(x)\thinspace dx.
$$

蒙特卡洛（Monte Carlo, MC）的核心想法非常朴素：**不会精确算整锅汤的平均味道，就按正确方式舀很多勺，再取平均。** 重要性采样改进舀汤位置，把样本集中到真正影响答案的区域；MCMC 则在无法独立舀样时，让一条满足特定规则的随机轨迹逐渐代表目标分布。

## 知识依赖与相关笔记

- 总入口：[Math 基础目录](../Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md)；针对 AI research 的学习顺序：[AI Researcher 数学学习路线](../AI%20Researcher%20%E6%95%B0%E5%AD%A6%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)。
- 先读：[概率论主干：联合、条件、期望与协方差](%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md) 与 [大数定律、中心极限定理与采样误差](%E5%A4%A7%E6%95%B0%E5%AE%9A%E5%BE%8B%E3%80%81%E4%B8%AD%E5%BF%83%E6%9E%81%E9%99%90%E5%AE%9A%E7%90%86%E4%B8%8E%E9%87%87%E6%A0%B7%E8%AF%AF%E5%B7%AE.md)。
- **MCMC 前置**：[Markov 链与平稳分布](Markov%20%E9%93%BE%E3%80%81%E9%9A%8F%E6%9C%BA%E8%BF%87%E7%A8%8B%E4%B8%8E%E7%8A%B6%E6%80%81%E7%A9%BA%E9%97%B4%E6%A8%A1%E5%9E%8B.md#2-markov-%E9%93%BE%E4%B8%8B%E4%B8%80%E6%AD%A5%E5%8F%AA%E7%9C%8B%E5%BD%93%E5%89%8D%E7%8A%B6%E6%80%81)。
- 后验积分与点估计：[最大似然、MAP 与贝叶斯估计](%E6%9C%80%E5%A4%A7%E4%BC%BC%E7%84%B6%E3%80%81MAP%20%E4%B8%8E%E8%B4%9D%E5%8F%B6%E6%96%AF%E4%BC%B0%E8%AE%A1.md)。
- 近似后验的另一条路线：[Bayesian ELBO](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E5%BB%BA%E6%A8%A1/%E5%8F%98%E5%88%86%E6%8E%A8%E6%96%AD/Bayesian%20ELBO.md)。
- 高维表示学习中的分布：[扩散模型、Score Matching 与 Flow Matching](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B/%E6%89%A9%E6%95%A3%E6%A8%A1%E5%9E%8B%E3%80%81Score%20Matching%20%E4%B8%8E%20Flow%20Matching.md)。
- 稳定计算权重：[浮点数、数值稳定性与条件数](../%E6%95%B0%E5%80%BC%E8%AE%A1%E7%AE%97/%E6%B5%AE%E7%82%B9%E6%95%B0%E3%80%81%E6%95%B0%E5%80%BC%E7%A8%B3%E5%AE%9A%E6%80%A7%E4%B8%8E%E6%9D%A1%E4%BB%B6%E6%95%B0.md)。

## 1. 普通蒙特卡洛：用样本均值代替积分

若能独立采样 $X_i\sim p$，则

$$
\hat I_N=\frac1N\sum_{i=1}^N f(X_i).
$$

在期望存在等条件下，大数定律使 $\hat I_N\to I$；若方差有限，中心极限定理给出近似标准误

$$
\mathop{\mathrm{SE}}(\hat I_N)
\approx\sqrt{\frac{\mathop{\mathrm{Var}}\nolimits_p[f(X)]}{N}}.
$$

### 1.1 为什么它强大

确定性网格积分会随维度指数爆炸，而在独立同分布、方差有限等条件下，MC 的典型标准误仍按 $N^{-1/2}$ 缩小，速率指数本身不直接依赖维度。因此它是贝叶斯推断、强化学习回报估计、渲染和生成模型中的基础工具。

但“速率不显含维度”不等于维度免费： $\mathop{\mathrm{Var}}[f(X)]$ 这个常数可能随维度急剧增大，单个样本的生成与评估成本也会变高，IS/MCMC 的 proposal 还可能在高维中迅速失配。因此高维问题仍可能需要指数级计算，只是困难藏在方差常数、采样器和每步成本里，而不是写在 $N^{-1/2}$ 的指数上。

### 1.2 为什么它也可能很浪费

若 $f(x)$ 只有在 $p$ 下极罕见的区域才非零，绝大多数样本贡献都是 0。估计罕见失效概率时，普通 MC 可能抽百万次也看不到一次失效。

方差降低技术包括 control variates、antithetic sampling、stratified sampling 和 quasi-Monte Carlo。它们不改变目标，只尽量让每个样本携带更多信息。

## 2. 重要性采样：去答案最重要的地方多采一些

选择较容易采样的提议分布 $q$，并要求凡是 $f(x)p(x)\ne0$ 的地方都有 $q(x)>0$。则

$$
I=\int f(x)\frac{p(x)}{q(x)}q(x)\thinspace dx
=\mathbb E_{X\sim q}[f(X)w(X)],
$$

其中重要性权重

$$
w(x)=\frac{p(x)}{q(x)}.
$$

估计量是

$$
\hat I_{\mathrm{IS}}
=\frac1N\sum_{i=1}^N f(X_i)w(X_i),
\qquad X_i\sim q.
$$

类比调查稀有人群：可以故意多访问目标人群，但汇总时必须按“被抽中概率”重新加权，否则样本构成不再代表总体。

### 2.1 自归一化重要性采样

若只知道未归一化目标 $\tilde p(x)=Zp(x)$，可使用

$$
\hat I_{\mathrm{SNIS}}
=\sum_i\bar w_i f(X_i),\qquad
\bar w_i=\frac{\tilde p(X_i)/q(X_i)}{\sum_j\tilde p(X_j)/q(X_j)}.
$$

它在有限样本下一般有偏，但在适当条件下一致。实际实现应在 log 空间计算并用 log-sum-exp 归一化，避免权重上溢或下溢。

### 2.2 提议分布的支持集和尾部是硬边界

如果目标有质量的区域里 $q(x)=0$，权重无法补救，估计会永久漏掉该区域。即使支持集覆盖， $q$ 的尾部太轻也可能产生少数巨大权重，导致方差极大甚至无穷。

常用权重有效样本量诊断为

$$
\mathop{\mathrm{ESS}}\nolimits_w
=\frac{(\sum_i w_i)^2}{\sum_i w_i^2}
=\frac1{\sum_i\bar w_i^2}.
$$

它是权重退化的启发式摘要，不是所有估计量的精确独立样本数。若 100,000 个样本的 ESS 只有 12，说明几乎全部答案由少数点决定。

## 3. MCMC：让相关轨迹代表目标分布

贝叶斯后验通常只知道未归一化形式

$$
p(\theta\mid D)\propto p(D\mid\theta)p(\theta),
$$

归一化常数难算，直接独立采样也困难。MCMC 构造一条 Markov 链

$$
X_0\to X_1\to X_2\to\cdots
$$

使目标分布 $\pi$ 成为其平稳分布；链充分混合后，沿轨迹的平均值可估计 $\mathbb E_\pi[f(X)]$。

这一段依赖 [平稳分布](Markov%20%E9%93%BE%E3%80%81%E9%9A%8F%E6%9C%BA%E8%BF%87%E7%A8%8B%E4%B8%8E%E7%8A%B6%E6%80%81%E7%A9%BA%E9%97%B4%E6%A8%A1%E5%9E%8B.md#3-%E5%B9%B3%E7%A8%B3%E5%88%86%E5%B8%83%E8%B5%B0%E5%BE%88%E4%B9%85%E5%90%8E%E7%9A%84%E9%95%BF%E6%9C%9F%E6%AF%94%E4%BE%8B)。MCMC 样本通常**不是独立的**，所以普通 $N^{-1/2}$ 标准误要用自相关修正。

## 4. Metropolis–Hastings：提出一步，再决定是否接受

当前位置为 $x$：

1. 从提议核 $q(x'\mid x)$ 提议候选 $x'$；
2. 以概率

$$
a(x,x')=
\min\left(1,
\frac{\pi(x')q(x\mid x')}{\pi(x)q(x'\mid x)}
\right)
$$

接受，否则留在 $x$。

若随机游走提议对称，即 $q(x'\mid x)=q(x\mid x')$，比值中提议项抵消。归一化常数也会在 $\pi(x')/\pi(x)$ 中抵消，这正是方法实用的关键。

要让长期样本代表完整目标，提议机制还必须让链能够到达目标支持集的所有相关区域，并满足相应的不可约、非周期与返归条件。若 proposal 永远无法跨过某个断开的区域，接受率公式本身也救不了漏掉的模式。

直觉上，链总愿意去高密度区域，也偶尔接受低密度方向，避免只做局部爬山。它不是优化算法：目标不是找到最高点，而是按正确比例访问所有区域。

## 5. 混合、相关性与有效样本量

链的“混合”描述它在目标分布不同区域之间移动得多快。随机游走步长太小，接受率高但挪得慢；步长太大，候选常被拒绝，也挪得慢。单看接受率无法证明采样正确。

对平稳 MCMC 序列，先选定关心的 estimand $\mathbb E_\pi[f(X)]$，再考察标量序列 $Y_t=f(X_t)$ 的自相关 $\rho_k^{(f)}$。对应有效样本量常近似为

$$
N_{\mathrm{eff}}^{(f)}
\approx\frac{N}{1+2\sum_{k\ge1}\rho_k^{(f)}}.
$$

同一条链对参数均值、尾部概率和非线性函数会有不同 ESS，不存在一个脱离 $f$ 的万能“链 ESS”。只有在链遍历目标、相关序列满足相应中心极限定理且自相关求和估计合理时，这个数才有意义。

### 5.1 Burn-in 不是万能橡皮擦

丢弃初始样本能减轻起点影响，但不能修复：

- 链被困在一个模式；
- 提议无法到达部分支持集；
- 后验几何病态；
- 代码或 log density 写错。

实践中应使用多条过度分散起点的链，检查 trace plot、分链与合并方差（如 $\hat R$）、bulk/tail ESS，并做模拟校准或已知分布单元测试。没有任何单个诊断能证明收敛。

### 5.2 高维方法

随机游走 MH 在高维中常很慢。Hamiltonian Monte Carlo（HMC）利用 log density 梯度沿高概率几何移动，NUTS 自动调节轨迹长度。变分推断则把采样问题变成优化问题，通常更快但会引入近似偏差，见 [Bayesian ELBO](https://github.com/HaningZS/HaningZS_Notes/blob/8ced9038b7611bcb8c2b2774fb870149df8ef780/ML%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E5%BB%BA%E6%A8%A1/%E5%8F%98%E5%88%86%E6%8E%A8%E6%96%AD/Bayesian%20ELBO.md)。

## 6. 普通 MC、IS 与 MCMC 怎么选

| 情形 | 方法起点 | 主要代价 | 首要诊断 |
|---|---|---|---|
| 能直接从目标独立采样 | 普通 MC | $f(X)$ 方差 | 重复估计、MC 标准误 |
| 稀有事件或已有良好提议分布 | IS | 权重退化 | 最大权重、权重 ESS |
| 只知未归一化目标且难直接采样 | MCMC | 自相关、混合慢 | 多链、 $\hat R$、ESS、trace |
| 高维可微后验 | HMC/NUTS | 梯度与几何计算 | divergence、ESS、能量诊断 |
| 大数据、需快速近似 | 变分推断 | 近似族偏差 | 后验预测、与 MCMC 小规模对照 |

## 7. 可运行示例一：用 IS 估计高斯罕见尾部

目标是 $P(Z>5)$，其中 $Z\sim\mathcal N(0,1)$。普通 MC 几乎全是 0；IS 改从 $q=\mathcal N(5,1)$ 采样，再用 $p/q$ 校正。

```python
import numpy as np

rng = np.random.default_rng(3)
n = 200_000
threshold = 5.0

# 普通 MC：期望命中数只有约 0.057，通常得到 0。
z_plain = rng.normal(size=n)
plain = np.mean(z_plain > threshold)

# Importance sampling: q=N(mu, 1), log(p/q)=-mu*x+mu^2/2。
mu = 5.0
z_is = rng.normal(loc=mu, scale=1.0, size=n)
log_w = -mu * z_is + 0.5 * mu**2
is_terms = (z_is > threshold) * np.exp(log_w)
estimate = is_terms.mean()
se = is_terms.std(ddof=1) / np.sqrt(n)

print("plain MC:", plain)
print("importance sampling:", estimate, "+/-", 1.96 * se)
print("reference is about 2.87e-7")

assert 2.5e-7 < estimate < 3.2e-7
assert se < 0.1 * estimate
```

这里 $q$ 仍覆盖整个实数轴，而且把大量样本放到阈值附近。若把 $q$ 截断到错误支持集，或均值移得过远导致权重极端，结果仍会不稳。

## 8. 可运行示例二：随机游走 Metropolis 的相关样本

```python
import numpy as np

rng = np.random.default_rng(8)
n = 60_000
x = np.empty(n)
x[0] = 8.0                     # 故意从目标 N(0,1) 的尾部开始
accepted = 0

def log_target(value):
    return -0.5 * value**2     # 省略会抵消的归一化常数

for i in range(1, n):
    proposal = x[i - 1] + rng.normal(scale=1.5)
    log_ratio = log_target(proposal) - log_target(x[i - 1])
    if np.log(rng.random()) < min(0.0, log_ratio):
        x[i] = proposal
        accepted += 1
    else:
        x[i] = x[i - 1]

samples = x[10_000:]           # 教学示例中的初始丢弃，不是收敛证明
lag1 = np.corrcoef(samples[:-1], samples[1:])[0, 1]

print("acceptance rate:", accepted / (n - 1))
print("mean / variance:", samples.mean(), samples.var())
print("lag-1 autocorrelation:", lag1)

assert abs(samples.mean()) < 0.08
assert abs(samples.var() - 1.0) < 0.10
assert lag1 > 0.0              # MCMC 样本不是独立样本
```

这个一维例子容易混合，不能代表复杂多峰后验。真实研究应使用成熟库及多链诊断，不要把教学实现直接用于论文结论。

## 9. 常见误区

1. **“MC 样本多就一定准。”** 方差可能极大；相关样本和错误目标也不会靠数量自动修复。
2. **“重要性权重能修复任何提议分布。”** $q$ 必须覆盖目标相关支持集，且尾部不能太轻。
3. **“ESS=500 就严格等价于 500 个独立样本。”** 权重 ESS 只是权重集中度诊断；MCMC ESS 还依赖具体 estimand $f(X)$。二者都不是适用于所有问题的精确兑换率。
4. **“接受率越高越好。”** 提议太小可让接受率接近 1，却移动极慢。
5. **“burn-in 后就是独立后验样本。”** 链仍相关，也可能尚未跨越模式。
6. **“trace 看起来像毛毛虫就证明收敛。”** 图形有帮助但不充分，需要多项诊断和模型检查。
7. **“MCMC 是寻找 MAP 的随机优化。”** MCMC 要按分布比例访问状态，不是只找最高点。
8. **“把链 thinning 后就产生更多信息。”** 丢样通常不会增加总 ESS；除非存储或下游计算受限，否则应保留并正确估计自相关。

## 10. 自测

1. 为什么普通 MC 的误差通常按 $1/\sqrt N$ 而不是 $1/N$ 缩小？
2. 重要性采样中， $q(x)=0$ 而 $f(x)p(x)\ne0$ 会发生什么？
3. 自归一化 IS 为什么不需要目标分布归一化常数？
4. Metropolis–Hastings 为什么能省掉目标的归一化常数？
5. 两条链分别困在两个模式、各自 trace 很稳定时，为什么仍未收敛？
6. MCMC 中的 ESS 与重要性权重 ESS 各自衡量什么？

## 延伸阅读

- Robert & Casella, *Monte Carlo Statistical Methods*, 2nd ed.
- Owen, [Monte Carlo Theory, Methods and Examples](https://artowen.su.domains/mc/).
- Neal, [MCMC Using Hamiltonian Dynamics](https://arxiv.org/abs/1206.1901).
- Vehtari et al., [Rank-Normalization, Folding, and Localization: An Improved R̂](https://projecteuclid.org/journals/bayesian-analysis/volume-16/issue-2/Rank-Normalization-Folding-and-Localization--An-Improved-R%CB%86-for/10.1214/20-BA1221.full), 2021.
- Stan, [MCMC Sampling](https://mc-stan.org/docs/reference-manual/mcmc.html).
