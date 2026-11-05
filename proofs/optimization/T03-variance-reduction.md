---
id: T03
type: proof-template
refined: 2026-09-28
status: "refined"
---

# T03. Variance reduction estimator recursion

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

用同一随机样本的梯度差，把估计误差绑定到移动路径。

## 复用契约

**输入对象**：refresh 步、配对梯度差、batch size b、误差 e_t。

**输出结论**：refresh error 加 (L²/b) 累计移动平方的估计误差界；估计器一般不是逐步条件无偏。

**必需假设**：

- 抽当前 batch 前，x_t、x_{t-1}、v_{t-1} 已确定。
- 新 batch 对历史条件独立；同一 sample/common randomness 用于配对差。
- component mean-square smoothness；1/b 需要相应的 batch 抽样假设。

**失败例子**：相同 x 处用独立噪声作差，即使移动为零也仍有 2σ²/b 的方差。

## 实例化时必须完成

- [ ] 对差值减去条件均值。
- [ ] 保留 batch factor、refresh error 与 epoch 边界。
- [ ] 将误差递推与带误差的 descent 联立。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [测度、条件期望、滤过与适应过程](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%B5%8B%E5%BA%A6%E3%80%81%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E3%80%81%E6%BB%A4%E8%BF%87%E4%B8%8E%E9%80%82%E5%BA%94%E8%BF%87%E7%A8%8B.md) · [集中不等式、MGF、鞅与自归一化过程](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E9%9B%86%E4%B8%AD%E4%B8%8D%E7%AD%89%E5%BC%8F%E3%80%81MGF%E3%80%81%E9%9E%85%E4%B8%8E%E8%87%AA%E5%BD%92%E4%B8%80%E5%8C%96%E8%BF%87%E7%A8%8B.md) · [量词、归纳、不变量与望远镜求和](../../Math%20%E5%9F%BA%E7%A1%80/%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/%E9%87%8F%E8%AF%8D%E3%80%81%E5%BD%92%E7%BA%B3%E3%80%81%E4%B8%8D%E5%8F%98%E9%87%8F%E4%B8%8E%E6%9C%9B%E8%BF%9C%E9%95%9C%E6%B1%82%E5%92%8C.md)

## 适用场景

先在 finite-sum 或 stochastic component-gradient 模型中定义可验证对象。设 $f(x)=\mathbb E_i f_i(x)$；在非刷新步，取给定 $\mathcal F_{t-1}$ 后独立的新 mini-batch $B_t$（大小 $b$），并对 $x_t,x_{t-1}$ 使用**同一批 indices/common randomness**：

$$
v_t
=v_{t-1}
+\frac1b\sum_{i\in B_t}
\left(\nabla f_i(x_t)-\nabla f_i(x_{t-1})\right).
$$

## 核心 intuition

假设 component gradients 满足 mean-square smoothness

$$
\mathbb E_i\Vert\nabla f_i(x)-\nabla f_i(y)\Vert^2
\le L^2\Vert x-y\Vert^2.
$$

令 $e_t=v_t-\nabla f(x_t)$。把 mini-batch difference 减去其条件均值后，cross term 为零，因此

$$
\mathbb E[\Vert e_t\Vert^2\mid\mathcal F_{t-1}]
\le
\Vert e_{t-1}\Vert^2
+\frac{L^2}{b}\Vert x_t-x_{t-1}\Vert^2.
$$

在 epoch 起点 $q$ 刷新 $v_q$ 后递推，得到

$$
\mathbb E\Vert e_t\Vert^2
\le
\mathbb E\Vert e_q\Vert^2
+\frac{L^2}{b}\sum_{k=q+1}^t\mathbb E\Vert x_k-x_{k-1}\Vert^2.
$$

刷新误差 $\mathbb E\Vert e_q\Vert^2$ 由 full gradient 或大 batch 单独控制。注意 $\mathbb E[e_t\mid\mathcal F_{t-1}]=e_{t-1}$，所以 SARAH/SPIDER estimator 一般**不是每一步对真实梯度条件无偏**，不能直接套 T01 的 unbiased-SGD 结论。

<a id="t03-vr-recursion"></a>

^t03-vr-recursion

## 逐步证明模板

```text
Step 1. 定义 filtration、refresh step 与 non-refresh mini-batch。
Step 2. 保证 paired difference 使用同一 sample/common randomness，且 batch 对历史条件独立。
Step 3. 写 e_t，并减去 mini-batch difference 的条件均值。
Step 4. 用条件期望消掉 centered cross term，保留 batch variance 的 1/b 因子。
Step 5. 用 component mean-square smoothness 控制 gradient difference。
Step 6. 从 refresh point 递推并保留 refresh error。
Step 7. 把 estimator error 作为 bias/error term与 descent/Lyapunov 联立，而不是宣称逐步无偏。
Step 8. 选择 epoch length、refresh batch 与 inner batch，平衡 path error 和 oracle cost。
```

## 可复用 lemma 形状

```text
Lemma: Under fresh paired mini-batches and component mean-square smoothness,
E||v_t-grad f(x_t)||^2
<= refresh_error + (L^2/b) sum_{k=q+1}^t E||x_k-x_{k-1}||^2.
```

## 可以迁移的想法

把 `gradient oracle` 换成：

- LLM judge oracle；
- preference oracle；
- PDE/simulator evaluator；
- rollout return estimator；
- offline policy value estimator。

只有在能构造 paired/common-randomness difference，或给出合法 importance correction/coupling 时，才能尝试减少 oracle 调用。“相邻 policy/model 变化小”本身不保证 estimator recursion 成立。

## 常见坑

- 漏掉 $1/b$，或使用两批独立样本分别评价 $x_t,x_{t-1}$，会破坏期望中的方差消减形状。
- $L$-smooth 的 population objective 不自动推出 component mean-square smoothness。
- Rollout/preference/judge 分布随 policy 变化时，还要处理 change of measure；不能把同一 index 当作同一随机实验。

## 来源论文 / 参考

- SPIDER, NeurIPS 2018. https://proceedings.neurips.cc/paper/2018/hash/1543843a4723ed2ab08e18053ae6dc5b-Abstract.html
- SpiderBoost and Momentum, NeurIPS 2019. https://proceedings.neurips.cc/paper_files/paper/2019/hash/512c5cad6c37edb98ae91c8a76c3a291-Abstract.html
- Conditional Gradient Methods via Stochastic Path-Integrated Differential Estimator, ICML 2019. https://proceedings.mlr.press/v97/yurtsever19b.html

## 关联模板与本地证据

- [T01：把单步目标下降累积成平均梯度平方界。](T01-descent.md)
- [T02：给辅助状态误差记账，让联合势函数下降。](T02-lyapunov.md)

通用证明工具：P02、P04；见 [证明原语](../../通用证明原语.md)。

- [SPIDER: Near-Optimal Non-Convex Optimization via Stochastic Path-Integrated Differential Estimator](../../proof_ref/foundations-2026-09/spider-near-optimal-non-convex-optimization-via-stochastic-1807.01695/README.md) · [官方 arXiv](https://arxiv.org/abs/1807.01695)
- [A Stochastic Gradient Method with an Exponential Convergence Rate for Finite Training Sets](../../proof_ref/foundations-2026-09/a-stochastic-gradient-method-with-an-exponential-convergence-1202.6258/README.md) · [官方 arXiv](https://arxiv.org/abs/1202.6258)

## 专项证明接口（2026-10-02）

- [T47：分解 local training 的位置偏差并控制客户端分歧、通信与输出。](T47-local-training-client-drift.md)
