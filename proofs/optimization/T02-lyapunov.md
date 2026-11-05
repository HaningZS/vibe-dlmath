---
id: T02
type: proof-template
refined: 2026-10-20
status: "needs-instantiation"
---

# T02. Lyapunov / potential function

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

给辅助状态误差记账，让联合势函数下降。

## 复用契约

**输入对象**：完整算法状态、Phi_t、进展权重 alpha_t、residual_t。

**输出结论**：针对当前算法实例化的加权进展界；写出势函数不等于已经证明收敛。

**必需假设**：

- 势函数在允许轨迹上有统一下界。
- 下文提出期望外的进展权重 $\alpha_t$ 是确定的非负数；随机自适应权重需要保留在期望内。
- 系数、步长和状态界满足同一组可行不等式。
- 残差可求和、可吸收，或显式保留。

**失败例子**：Phi_t 可趋负无穷时，每步下降无法控制累计梯度。

## 实例化时必须完成

- [ ] 说明每项 potential 吸收哪个交叉项。
- [ ] 同时验证系数可行性与整体下界。
- [ ] 求和后用 sum alpha_t 归一化。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [量词、归纳、不变量与望远镜求和](../../Math%20%E5%9F%BA%E7%A1%80/%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/%E9%87%8F%E8%AF%8D%E3%80%81%E5%BD%92%E7%BA%B3%E3%80%81%E4%B8%8D%E5%8F%98%E9%87%8F%E4%B8%8E%E6%9C%9B%E8%BF%9C%E9%95%9C%E6%B1%82%E5%92%8C.md) · [Grönwall、Duhamel 与稳定性误差传播](../../Math%20%E5%9F%BA%E7%A1%80/%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/Gr%C3%B6nwall%E3%80%81Duhamel%20%E4%B8%8E%E7%A8%B3%E5%AE%9A%E6%80%A7%E8%AF%AF%E5%B7%AE%E4%BC%A0%E6%92%AD.md)

## 适用场景

当算法状态不是单个 `x_t`，而是

```text
x_t, momentum_t, adaptive_denominator_t, compressed_error_t, adapter_state_t, memory_t
```

这时直接证明 `f(x_t)` 单调下降通常失败。标准做法是构造一个 potential：

$$
\Phi_t
=f(x_t)
+a_t\Vert m_t\Vert^2
+b_t\Vert x_t-x_{t-1}\Vert^2
+c_t\Vert e_t\Vert^2
+d_t\Vert v_t-v_{t-1}\Vert^2
+\cdots.
$$

## 核心证明骨架

目标不是证明

$$
f(x_{t+1}) \le f(x_t)-\text{progress},
$$

而是证明

$$
\mathbb{E}\Phi_{t+1}
\le
\mathbb{E}\Phi_t
-\alpha_t\mathbb{E}\Vert\nabla f(x_t)\Vert^2
+\mathrm{residual}_t.
$$

再证明 residual 可求和或可被 progress 吸收：

$$
\sum_t \mathrm{residual}_t
\le
\frac{1}{2}\sum_t\alpha_t\mathbb{E}\Vert\nabla f(x_t)\Vert^2
+\mathrm{small\ constant}.
$$

## 逐步证明模板

### 求和之前，先检查势函数的下界

若 $\alpha_t\geq0$、 $\sum_{t<T}\alpha_t>0$，并已证明
$\Phi_T\geq\Phi_{\inf}$，则

$$
\sum_{t< T}\alpha_t\mathbb E\Vert\nabla f(x_t)\Vert^2
\leq \mathbb E\Phi_0-\Phi_{\inf}
+\sum_{t< T}\mathrm{residual}_t.
$$

若残差能吸收一半左边，就把这一半移过去；若不能，残差必须留在最终界中。含交叉项的 $\Phi_t$ 需要证明整体下有界，不能因为其中包含 $f(x_t)$ 就视为已经完成。上述结论只给加权平均进展，last-iterate 收敛仍需另外连接。

### 自适应随机权重不能提出期望

若实际算法产生可预测、非负但随机的 $\alpha_t$，并且下式各项可积，应从条件下降式出发，取全期望后保留

$$
\sum_{t< T}\mathbb E[\alpha_t\Vert\nabla f(x_t)\Vert^2]
\leq\mathbb E\Phi_0-\Phi_{\inf}+\sum_{t< T}\mathbb E[r_t],
$$

其中 $r_t$ 是相应的可积随机残差。 $\alpha_t$ 与梯度通常由同一历史决定，因此可预测性不意味着二者独立。例如 $Z\sim\mathop{\mathrm{Bernoulli}}(1/2)$、 $\alpha=Z$ 时， $\mathbb E[\alpha Z]=1/2$，而 $\mathbb E\alpha\thinspace\mathbb EZ=1/4$。

确定权重可令独立输出 $R$ 满足 $\Pr(R=t)=\alpha_t/\sum_s\alpha_s$，直接得到加权平均保证。若在看到完整轨迹后按随机权重抽 $R$，输出对应的是
$\mathbb E[\sum_t\alpha_t\Vert\nabla f(x_t)\Vert^2/\sum_t\alpha_t]$，不是期望的比值；还需证明总权重为正并控制这个随机分母，才能给出输出界。

```text
Step 1. 列出算法所有状态变量。
Step 2. 判断哪些状态变量会破坏 f 的单步下降。
Step 3. 给每个“坏项”设计一个 potential term。
Step 4. 推导 Phi_{t+1}-Phi_t。
Step 5. 用 Young inequality / Cauchy-Schwarz 分离交叉项。
Step 6. 调系数，让坏项被 potential decrease 或 main descent 吸收。
Step 7. telescope Phi_t。
Step 8. 选超参数，得到 stationarity / regret / convergence rate。
```

## 常用不等式

$$
2\langle a,b\rangle \le \gamma \Vert a\Vert^2 + \frac{1}{\gamma}\Vert b\Vert^2.
$$

$$
\Vert a+b\Vert^2 \le (1+\gamma)\Vert a\Vert^2 + (1+1/\gamma)\Vert b\Vert^2.
$$

这些用来处理 momentum 与 gradient error 的交叉项。

## 适合迁移到哪些新论文

- Adam / RMSProp / AdaGrad 变体。
- LoRA / sparse adapter 的 layer-wise update。
- OPD / RLHF 训练过程有 teacher-student KL、policy drift、adapter drift。
- 压缩优化、error feedback、distributed/federated learning。

## 常见坑

- Lyapunov 不是随便加项；每一项都必须在下一步递推中抵消某个坏项。
- 不要把 potential 写得过大，否则 final theorem 里 initial potential 会很丑。
- 如果 adaptive denominator 有非单调性，要特别处理；AMSGrad 的 long-term max trick就是为了解决这个问题。

## 来源论文 / 参考

- On the Convergence of Adam and Beyond, ICLR 2018. https://openreview.net/forum?id=ryQu7f-RZ
- MicroAdam: Accurate Adaptive Optimization with Low Space Overhead and Provable Convergence, NeurIPS 2024. https://proceedings.neurips.cc/paper_files/paper/2024/hash/000f947dcaff8fbffcc3f53a1314f358-Abstract-Conference.html
- The Marginal Value of Adaptive Gradient Methods in Machine Learning, NeurIPS 2017. https://papers.neurips.cc/paper/7003-the-marginal-value-of-adaptive-gradient-methods-in-machine-learning

## 关联模板与本地证据

- [T01：把单步目标下降累积成平均梯度平方界。](T01-descent.md)
- [T03：用同一随机样本的梯度差，把估计误差绑定到移动路径。](T03-variance-reduction.md)
- [T16：把裁剪梯度分成 centered martingale 与 clipping bias。](T16-heavy-tail-clipping.md)

通用证明工具：P02、P07；见 [证明原语](../../通用证明原语.md)。

- [A Tight Theory of Error Feedback Algorithms in Distributed Optimization](../../proof_ref/core-theory-2026-09/a-tight-theory-of-error-feedback-algorithms-in-2605.31594/README.md) · [官方 arXiv](https://arxiv.org/abs/2605.31594)
- [Structured Preconditioners in Adaptive Optimization: A Unified Analysis](../../proof_ref/recent-accepted-2025-2026/structured-preconditioners-in-adaptive-optimization-a-unified-analysis-2503.10537/README.md) · [官方 arXiv](https://arxiv.org/abs/2503.10537)

## 专项证明接口（2026-10-02）

- [T47：分解 local training 的位置偏差并控制客户端分歧、通信与输出。](T47-local-training-client-drift.md)
