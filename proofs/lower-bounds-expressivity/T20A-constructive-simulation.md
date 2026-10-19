---
id: T20A
type: proof-template
refined: 2026-09-28
status: bounded-scope
---

# T20A. Constructive simulation upper bounds

[主题目录](README.md) · [T20 路由](T20-expressivity-router.md) · [模板总目录](../README.md)

## 复用契约

**输入对象**：目标算法/函数族 $A_n$、输入域 $\mathcal X_n$、模型族 $\mathcal M_n$、状态编码与资源预算。

**输出结论**：在规定资源内，存在模型近似或精确实现目标。

典型量词是

$$
\forall n,\ \exists M_n\in\mathcal M_n,\ \forall x\in\mathcal X_n:
\quad d(M_n(x),A_n(x))\leq\varepsilon_n.
$$

先选 $M_n$ 再对所有输入成立，不能为每个输入定制写有答案的参数。若要求 uniform construction，还要给出从 $n$ 生成模型描述的有效过程及成本。

**失败例子**：只证明一组显式权重实现 GD，却声称随机初始化训练一定学到 GD。

## 实例化时必须完成

- [ ] 定义状态到 token/隐藏向量的编码、允许算术与精度。
- [ ] 为 primitive 给出真实参数与输入输出。
- [ ] 合计 depth、width、context、precision、循环和外部调用预算。
- [ ] 近似构造须保证中间状态留在单步近似的有效域。
- [ ] construction、optimization/learnability 与实证分开。

## 核心推导

设算法更新为 $z_{\ell+1}=A(z_\ell)$，模型更新为
$\widehat z_{\ell+1}=F_\ell(\widehat z_\ell)$。在所有实际中间状态所在的域上，假设

$$
\|F_\ell(z)-A(z)\|\leq\epsilon_\ell,\qquad
\|A(z)-A(z')\|\leq L_\ell\|z-z'\|.
$$

则 $e_{\ell+1}\leq L_\ell e_\ell+\epsilon_\ell$，进而

$$
e_L\leq
\left(\prod_{\ell=0}^{L-1}L_\ell\right)e_0+
\sum_{j=0}^{L-1}\epsilon_j
\prod_{\ell=j+1}^{L-1}L_\ell.
$$

空乘积为 1。再用 output decoder/task-loss 的稳定性将 $e_L$ 转成任务误差；目标算法本身的有限步误差另计。

## 精确的教学例子

在允许二输入 XOR gate 的 Boolean circuit 中，递归将 $n$ 个输入分成两半，各算 parity，再 XOR。单个 bit 的 parity 是自身，而两组 parity 的 XOR 等于合并组的 parity，因而归纳得到正确性。

构造使用 $n-1$ 个 XOR gates，深度可为 $\lceil\log_2 n\rceil$。迁移到 Transformer 时，仍须实现合法 XOR primitive、编码与精度；电路构造不自动等于网络实现。

## 引用与复用

复用论文 primitive 时记录版本、lemma、精度和输入范围；自行构造时完整证明。数值测试不能替代对全部输入的证明。

相关：[T14 算法模拟](../deep-learning/T14-algorithm-simulation.md) · [T20B 能力下界](T20B-expressivity-lower-bound.md) · [Grönwall 与误差传播](<../../Math 基础/微积分与分析/Grönwall、Duhamel 与稳定性误差传播.md>)。
