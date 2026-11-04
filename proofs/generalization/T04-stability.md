---
id: T04
type: proof-template
refined: 2026-09-28
status: "bounded-scope"
---

# T04. Algorithmic stability / leave-one-out generalization

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

耦合相邻训练集的算法轨迹，控制期望泛化差。

## 复用契约

**输入对象**：i.i.d. S、独立替换集 S^(i)、共享种子 U、总体与经验风险。

**输出结论**：本卡控制 |E[generalization gap]|，不是 E|gap| 或统一高概率界。

**必需假设**：

- 区分 replace-one/remove-one、uniform/on-average 的版本。
- 样本与算法随机性的联合分布明确。
- 参数差转 loss 差需要 Lipschitz 或对应稳定性条件。

**失败例子**：一次训练里参数变化小，不足以证明所有相邻数据集都稳定。

## 实例化时必须完成

- [ ] 先写目标量及全部期望。
- [ ] 分别分析替换每个 i 的耦合轨迹，再平均。
- [ ] 非 i.i.d. 或高概率版本另外证明。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [算法稳定性、经验过程与 PAC-Bayes](../../Math%20%E5%9F%BA%E7%A1%80/%E7%BB%9F%E8%AE%A1%E5%AD%A6%E4%B9%A0%E7%90%86%E8%AE%BA/%E7%AE%97%E6%B3%95%E7%A8%B3%E5%AE%9A%E6%80%A7%E3%80%81%E7%BB%8F%E9%AA%8C%E8%BF%87%E7%A8%8B%E4%B8%8E%20PAC-Bayes.md) · [Grönwall、Duhamel 与稳定性误差传播](../../Math%20%E5%9F%BA%E7%A1%80/%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/Gr%C3%B6nwall%E3%80%81Duhamel%20%E4%B8%8E%E7%A8%B3%E5%AE%9A%E6%80%A7%E8%AF%AF%E5%B7%AE%E4%BC%A0%E6%92%AD.md)

## 适用场景

当你想证明“一个训练算法为什么泛化”，而不是证明 hypothesis class 的 uniform convergence。特别适合 SGD、early stopping、regularized training、algorithm-dependent generalization。

## 核心思路

构造两个训练集：

$$
S=(z_1,\dots,z_i,\dots,z_n),
\quad
S'=(z_1,\dots,z_i',\dots,z_n),
$$

二者只差一个样本。用相同随机种子运行算法，比较轨迹：

$$
\Delta_t = \|w_t(S)-w_t(S')\|.
$$

如果算法对单个样本不敏感，则 `Delta_t` 小，从而 generalization gap 小。

## 逐步证明模板

```text
Step 1. 定义 S 和 S'，只替换一个样本。
Step 2. 用同一随机种子 coupling 两次训练。
Step 3. 写出两条轨迹的更新差。
Step 4. 分情况：本步采到相同样本 / 采到被替换样本。
Step 5. 用 Lipschitz / smoothness 控制距离增长。
Step 6. 得到 Delta_t 的递推式。
Step 7. 解递推式，得到 E Delta_T。
Step 8. 用 loss Lipschitz 把参数距离转成 loss difference。
Step 9. 对被替换样本位置取平均，得到 generalization bound。
```

## 常见 theorem 形状

$$
\left|\mathbb E_{S,U}\!\left[
R(A(S,U))-\widehat R_S(A(S,U))
\right]\right|
\leq
\frac{L_\ell}{n}\sum_{i=1}^n
\mathbb E_{S,Z_i',U}\|A(S,U)-A(S^{(i)},U)\|.
$$

这里 $S^{(i)}$ 用独立的 $Z_i'\sim\mathcal D$ 替换第 $i$ 个训练样本， $U$ 是独立于样本的算法随机性，两次训练使用同一个 $U$。 $R$ 与 $\widehat R_S$ 分别为总体和经验风险，并假设相关期望存在。

证明的关键是用独立替换把测试风险写成相邻训练集的损失期望，再用 loss 的 $L_\ell$-Lipschitz 性。左边是 **期望 gap 的绝对值**，不是绝对 gap 的期望；这两者也都不自动等于 high-probability generalization。

## 何时比 PAC-Bayes 更合适

- 你想强调训练动态本身。
- 你的算法有 early stopping / stochasticity / local update。
- 你不想构造 posterior/prior。

## 常见坑

- RL/agent 数据不是 i.i.d.，直接 leave-one-out 不成立，需要 trajectory-level coupling。
- 如果训练很久，稳定性 bound 可能变松。
- 非凸情况下要明确 smoothness / Lipschitz 条件，否则递推可能无法闭合。

## 来源论文 / 参考

- Train faster, generalize better: Stability of stochastic gradient descent, ICML 2016. https://proceedings.mlr.press/v48/hardt16.html
- Stability and Generalization of Learning Algorithms that Converge to Global Optima, ICML 2018. https://proceedings.mlr.press/v80/charles18a.html

## 关联模板与本地证据

- [T05：分开使用 PAC-Bayes 高概率界和互信息期望界。](T05-pac-bayes-information.md)
- [T01：把单步目标下降累积成平均梯度平方界。](../optimization/T01-descent.md)

通用证明工具：P01、P07、P09；见 [证明原语](../../通用证明原语.md)。

- [Train faster, generalize better: Stability of stochastic gradient descent](../../proof_ref/core-theory-2026-09/train-faster-generalize-better-stability-of-stochastic-gradient-1509.01240/README.md) · [官方 arXiv](https://arxiv.org/abs/1509.01240)

## 经典与近期证明蒸馏

- [T50：用指数距离上包络把观测证书接到总体期望，保持量词与选择预算。](T50-data-dependent-certificate-envelope.md)
