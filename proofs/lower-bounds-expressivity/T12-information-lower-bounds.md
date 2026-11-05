---
id: T12
type: proof-template
refined: 2026-09-28
status: "refined + claim-checked"
---

# T12. Fano / Le Cam / Assouad / interactive lower bound

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

由困难实例的不可区分性推出指定算法类的风险下界。

## 复用契约

**输入对象**：算法/oracle、hard instances、参数间距、transcript laws 与损失。

**输出结论**：指定信息接口下的 minimax 下界；不是单个算法失败的演示。

**必需假设**：

- 全部 hard instances 属于问题类。
- separation 到 loss 的转换明确。
- 交互式 KL 检查 action kernel、随机性与绝对连续性。

**失败例子**：违反噪声或有界性约束的 hard instance 不能约束原问题。

## 实例化时必须完成

- [ ] 先规定算法量词和 oracle。
- [ ] 计算信息预算。
- [ ] 把 testing error 转成有单位的风险并优化间距。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [统计距离、Le Cam、Fano、Assouad 与 Yao 下界](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E7%BB%9F%E8%AE%A1%E8%B7%9D%E7%A6%BB%E3%80%81Le%20Cam%E3%80%81Fano%E3%80%81Assouad%20%E4%B8%8E%20Yao%20%E4%B8%8B%E7%95%8C.md) · [测度、条件期望、滤过与适应过程](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%B5%8B%E5%BA%A6%E3%80%81%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E3%80%81%E6%BB%A4%E8%BF%87%E4%B8%8E%E9%80%82%E5%BA%94%E8%BF%87%E7%A8%8B.md)

## 适用场景

证明 minimax lower bound、regret lower bound、sample complexity lower bound、某个 trade-off 不可避免。

## 三个经典工具与 Yao 原理

### Le Cam

两点法：构造参数 $\theta_0,\theta_1$ 及对应观测分布 $P_0,P_1$。对等先验二元 0-1 测试，

$$
\inf_{\hat\theta}\sup_{\theta\in\lbrace0,1\rbrace}
\mathbb{P}_\theta(\hat\theta\ne\theta)
\ge
\frac{1}{2}(1-\mathrm{TV}(P_0,P_1)).
$$

若损失度量满足 $d(\theta_0,\theta_1)=\Delta$，由估计器诱导最近邻测试可得

$$
\inf_{\widehat\theta}\sup_{i\in\lbrace0,1\rbrace}
\mathbb E_i d(\widehat\theta,\theta_i)
\ge
\frac{\Delta}{4}\left(1-\mathop{\mathrm{TV}}(P_0,P_1)\right).
$$

因此从 testing error 转成 estimation risk 时不能漏掉参数间距 $\Delta$。

### Fano

多点 packing：令 $V$ 均匀分布在 $M$ 个假设上，且任意两参数的距离至少 $2s$。Fano 给出典型形式

$$
\inf_{\widehat V}\mathbb P(\widehat V\ne V)
\ge
1-\frac{I(V;X)+\log 2}{\log M},
$$

进而把右端乘以 $s$ 得到对应的期望 estimation-risk 下界。关键工作是构造 packing 并上界 $I(V;X)$，不是只写“应用 Fano”。

### Assouad

hypercube：构造 $\theta\in\lbrace-1,+1\rbrace^d$，把风险下界分解为逐坐标二元测试。需要明确 Hamming separation、相邻顶点诱导分布的 TV/KL，以及目标损失如何控制 Hamming error。

若 $\omega^{(j)}$ 表示翻转第 $j$ 位，并令

$$
\alpha_{\mathrm{TV}}
=\max_{\omega,j}\mathop{\mathrm{TV}}(P_\omega,P_{\omega^{(j)}}),
$$

则一个常用的 Assouad 形式是

$$
\inf_{\widehat\omega}\sup_{\omega\in\lbrace-1,+1\rbrace^d}
\mathbb E_\omega d_H(\widehat\omega,\omega)
\ge
\frac d2(1-\alpha_{\mathrm{TV}}).
$$

若原问题损失下界为 $c\thinspace d_H(\widehat\omega,\omega)$，再乘 $c$ 转回 minimax risk。

### Yao minimax principle

随机算法下界通常先选一个困难输入先验，再证明任意确定性算法的平均风险：

$$
\inf_{A\ \mathrm{randomized}}\sup_{x}\mathbb E L(A,x)
\ge
\sup_{\mu}\inf_{a\ \mathrm{deterministic}}\mathbb E_{x\sim\mu}L(a,x).
$$

使用时要写清随机性来自算法还是困难实例；有限问题中的等式版本依赖标准 minimax 条件。

## 逐步证明模板

```text
Step 1. 构造 hard instance family {P_theta}。
Step 2. 证明不同 theta 对应的 optimal answer / parameter / policy 距离足够大。
Step 3. 上界不同实例诱导数据分布之间的 KL / TV / mutual information。
Step 4. 应用 Fano / Le Cam / Assouad。
Step 5. 把 hypothesis testing error 转成 estimation error / regret / suboptimality。
Step 6. 选 instance separation epsilon，平衡 distinguishability 和 loss gap。
Step 7. 对 randomized adaptive algorithm，说明使用 Yao 还是直接在 transcript 分布上取算法随机性的期望。
```

## interactive setting 的升级

bandit/RL 中，算法会 adaptive 地选择 action，观测分布依赖历史。此时不能简单用 i.i.d. KL，需要写 interaction transcript：

$$
H_T=(a_1,o_1,\dots,a_T,o_T).
$$

设算法在两个环境中使用**同一个**可测 action kernel（其随机种子分布也相同），并假设所需绝对连续性。对 transcript 概率作链式分解时，action-kernel 的 KL 项抵消，于是

$$
\mathrm{KL}(P_\theta^{H_T}\Vert P_{\theta'}^{H_T})
=\sum_{t=1}^T
\mathbb{E}_{\theta}
\left[
\mathrm{KL}(P_\theta(o_t|H_{t-1},a_t)\Vert P_{\theta'}(o_t|H_{t-1},a_t))
\right].
$$

若 stopping time、batch feedback 或环境同时改变 action availability，必须重写 transcript 并重新检查哪些 kernel 真正抵消。

<a id="t12-interactive-kl"></a>

^t12-interactive-kl

## 常见坑

- lower bound 不是证明某个算法失败，而是证明所有算法信息不足。
- hard instances 要同时满足你的问题假设。
- interactive lower bound 要考虑 algorithm adaptivity、算法随机性、transcript measurability 与绝对连续性。
- Le Cam 的测试错误、Fano 的识别错误和最终风险有不同单位；必须通过 separation/reduction 显式转换。

## 来源论文 / 参考

- Assouad, Fano, and Le Cam with Interaction, NeurIPS 2024. https://proceedings.neurips.cc/paper_files/paper/2024/hash/8a23a95e26d016711c0d70f79ade3c95-Abstract-Conference.html
- 本地 PDF/TeX：[核验笔记](../../proof_ref/core-theory-2026-09/assouad-fano-and-le-cam-with-interaction-a-2410.05117/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md) · [PDF](../../proof_ref/core-theory-2026-09/assouad-fano-and-le-cam-with-interaction-a-2410.05117/paper.pdf#page=5)
- 近期 oracle divergence decomposition：[核验笔记](../../proof_ref/recent-accepted-2025-2026/new-lower-bounds-for-stochastic-non-convex-optimization-2502.14060/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md) · [PDF](../../proof_ref/recent-accepted-2025-2026/new-lower-bounds-for-stochastic-non-convex-optimization-2502.14060/paper.pdf#page=5)
- Assouad, Fano, and Le Cam, Bin Yu, 1997. https://www.stat.berkeley.edu/users/binyu/ps/LeCam.pdf
- Bandit Algorithms, Lattimore & Szepesvári. https://tor-lattimore.com/downloads/book/book.pdf

## 关联模板与本地证据

- [T06：用置信椭球、optimism 与 elliptical potential 控制 pseudo-regret。](../sequential-decision/T06-linear-bandit.md)

通用证明工具：P05、P10；见 [证明原语](../../通用证明原语.md)。

- [An Introductory Guide to Fano's Inequality with Applications in Statistical Estimation](../../proof_ref/foundations-2026-09/an-introductory-guide-to-fano-s-inequality-with-1901.00555/README.md) · [官方 arXiv](https://arxiv.org/abs/1901.00555)
- [Lower Bounds for Non-Convex Stochastic Optimization](../../proof_ref/foundations-2026-09/lower-bounds-for-non-convex-stochastic-optimization-1912.02365/README.md) · [官方 arXiv](https://arxiv.org/abs/1912.02365)
- [Assouad, Fano, and Le Cam with Interaction: A Unifying Lower Bound Framework and Characterization for Bandit Learnability](../../proof_ref/core-theory-2026-09/assouad-fano-and-le-cam-with-interaction-a-2410.05117/README.md) · [官方 arXiv](https://arxiv.org/abs/2410.05117)
