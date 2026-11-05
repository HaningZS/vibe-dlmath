---
id: T09
type: proof-template
refined: 2026-09-28
status: "bounded-scope"
---

# T09. NTK / overparameterization induction

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

闭合初始谱、核稳定、下降与参数移动的联合归纳。

## 复用契约

**输入对象**：训练预测向量、Jacobian、Gram、参数化尺度与初始化邻域。

**输出结论**：特定 scaling 下的训练收敛；不是自动的 feature learning 或测试泛化。

**必需假设**：

- 初始最小特征值、邻域谱上界与稳定性可证。
- 离散非线性网络的 Taylor remainder 单独控制。
- 累计移动留在同一个邻域，宽度/步长条件可行。

**失败例子**：K_0 非退化，但大步长使参数离开稳定区，不能据此推出后续几何下降。

## 实例化时必须完成

- [ ] 写清 loss 的样本数缩放。
- [ ] 证明谱界与非线性余项共同导出收缩。
- [ ] 反向累计移动并闭合归纳。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [矩阵浓缩、谱扰动与子空间误差](../../Math%20%E5%9F%BA%E7%A1%80/%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E7%9F%A9%E9%98%B5%E6%B5%93%E7%BC%A9%E3%80%81%E8%B0%B1%E6%89%B0%E5%8A%A8%E4%B8%8E%E5%AD%90%E7%A9%BA%E9%97%B4%E8%AF%AF%E5%B7%AE.md) · [高维几何、集中现象与随机投影](../../Math%20%E5%9F%BA%E7%A1%80/%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E9%AB%98%E7%BB%B4%E5%87%A0%E4%BD%95%E3%80%81%E9%9B%86%E4%B8%AD%E7%8E%B0%E8%B1%A1%E4%B8%8E%E9%9A%8F%E6%9C%BA%E6%8A%95%E5%BD%B1.md) · [量词、归纳、不变量与望远镜求和](../../Math%20%E5%9F%BA%E7%A1%80/%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/%E9%87%8F%E8%AF%8D%E3%80%81%E5%BD%92%E7%BA%B3%E3%80%81%E4%B8%8D%E5%8F%98%E9%87%8F%E4%B8%8E%E6%9C%9B%E8%BF%9C%E9%95%9C%E6%B1%82%E5%92%8C.md)

## 适用场景

证明 overparameterized neural network 在训练中接近线性化模型、kernel 稳定、gradient descent 能达到 zero training loss 或 global minima。

## 核心 induction

```text
Initialization good
→ Gram matrix well-conditioned
→ weights stay close to initialization
→ NTK / Gram matrix stays stable
→ loss decreases geometrically
→ cumulative movement remains small
→ induction closes
```

## 典型公式

初始化 Gram matrix：

$$
\lambda_{\min}(K_0) \ge \lambda_0 > 0.
$$

kernel stability：

$$
\Vert K_t-K_0\Vert \le \lambda_0/2.
$$

linearized loss decrease：

$$
\Vert y-f_{\theta_{t+1}}(X)\Vert^2
\le
(1-c\eta\lambda_0)\Vert y-f_{\theta_t}(X)\Vert^2.
$$

movement bound：

$$
\Vert\theta_t-\theta_0\Vert \le R.
$$

## 逐步证明模板

### 离散非线性网络还欠一个余项

以平方损失 $\frac12\Vert f_\theta(X)-y\Vert^2$ 为例，记
$r_t=y-f_{\theta_t}(X)$、 $J_t=D_\theta f_{\theta_t}(X)$、 $K_t=J_tJ_t^\top$。
若损失含 $1/n$，应同时调整下面的 $K_t$ 或步长。

真实网络沿参数更新展开为

$$
r_{t+1}=(I-\eta K_t)r_t-\rho_t,
$$

其中 $\rho_t$ 是非线性 Taylor remainder。若在同一个归纳区域中
$\lambda_{\min}(K_t)\geq\lambda_0/2$、
$\lambda_{\max}(K_t)\leq\Lambda$、 $\eta\leq1/\Lambda$，且
$\Vert\rho_t\Vert\leq\eta\lambda_0\Vert r_t\Vert/4$，则

$$
\Vert r_{t+1}\Vert\leq(1-\eta\lambda_0/4)\Vert r_t\Vert.
$$

再从 $\Vert\theta_{t+1}-\theta_t\Vert\leq\eta\Vert J_t\Vert_{\mathrm{op}}\Vert r_t\Vert$ 累计移动。只有累计量确实不超过前面使用的邻域半径，联合归纳才闭合。初始化谱下界不能替代余项控制。

```text
Step 1. 用随机初始化 concentration 证明 Gram matrix 初始条件。
Step 2. 假设到 t 为止参数都在半径 R 的球内。
Step 3. 在这个球内证明激活模式/NTK/Gram matrix 变化很小。
Step 4. 用稳定 Gram matrix 证明预测误差几何下降。
Step 5. 用下降的误差反推每步 gradient 小，累计参数移动小。
Step 6. 证明累计移动 <= R，关闭 induction。
Step 7. 得到 convergence theorem。
```

## 常见坑

- NTK 主要解释 lazy training，不一定解释 feature learning。
- 宽度条件可能是很大的 polynomial，不一定实践紧。
- 若目标是解释 feature learning，需要额外分析表示和核的变化；lazy-regime 收敛本身不提供这个结论。

## 来源论文 / 参考

- Neural Tangent Kernel: Convergence and Generalization in Neural Networks, NeurIPS 2018. https://proceedings.neurips.cc/paper/8076-neural-tangen-kernel-convergence-and-generalization-in-neural-networks.pdf
- A Convergence Theory for Deep Learning via Over-Parameterization, ICML 2019. https://proceedings.mlr.press/v97/allen-zhu19a.html
- Gradient Descent Finds Global Minima of Deep Neural Networks, ICLR 2019. https://openreview.net/forum?id=S1eK3i09YQ

## 关联模板与本地证据

- [T02：给辅助状态误差记账，让联合势函数下降。](../optimization/T02-lyapunov.md)
- [T10：分开控制极限动力学优化误差与有限粒子近似误差。](T10-mean-field.md)
- [T14：通过逐层构造与稳定性说明受限网络能模拟哪个算法。](T14-algorithm-simulation.md)

通用证明工具：P02、P07、P08；见 [证明原语](../../通用证明原语.md)。

- [Neural Tangent Kernel: Convergence and Generalization in Neural Networks](../../proof_ref/foundations-2026-09/neural-tangent-kernel-convergence-and-generalization-in-neural-1806.07572/README.md) · [官方 arXiv](https://arxiv.org/abs/1806.07572)
- [Wide Neural Networks of Any Depth Evolve as Linear Models Under Gradient Descent](../../proof_ref/foundations-2026-09/wide-neural-networks-of-any-depth-evolve-as-1902.06720/README.md) · [官方 arXiv](https://arxiv.org/abs/1902.06720)
- [On Lazy Training in Differentiable Programming](../../proof_ref/foundations-2026-09/on-lazy-training-in-differentiable-programming-1812.07956/README.md) · [官方 arXiv](https://arxiv.org/abs/1812.07956)

## 专项证明接口（2026-10-02）

- [T42：精确跟踪时变核、参数移动与冻结核近似，不把核变化当下游收益。](T42-feature-drift-kernel-dynamics.md)
