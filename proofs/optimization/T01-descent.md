---
id: T01
type: proof-template
refined: 2026-09-28
status: "refined"
---

# T01. Descent lemma + telescoping

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

把单步目标下降累积成平均梯度平方界。

## 复用契约

**输入对象**：目标 f、迭代 x_t、随机梯度 g_t、历史 F_t、步长与输出规则。

**输出结论**：平均或独立均匀随机迭代的期望 stationarity 界；最后迭代、函数值和高概率保证需额外条件。

**必需假设**：

- 目标下有界，更新线段上 L-smooth。
- g_t 给定历史后无偏且条件方差有界；x_t 对历史可测。
- 步长范围和随机迭代/平均/最后迭代的输出约定明确。

**失败例子**：f(x)=-x² 下梯度下降可能发散；缺少目标下界时 telescope 不产生有限初始 gap。

## 实例化时必须完成

- [ ] 代入真实更新，保留 bias/projection/proximal 项。
- [ ] 先取条件期望再求和。
- [ ] 约束步长并完整报告 T 和常数依赖。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [量词、归纳、不变量与望远镜求和](../../Math%20%E5%9F%BA%E7%A1%80/%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/%E9%87%8F%E8%AF%8D%E3%80%81%E5%BD%92%E7%BA%B3%E3%80%81%E4%B8%8D%E5%8F%98%E9%87%8F%E4%B8%8E%E6%9C%9B%E8%BF%9C%E9%95%9C%E6%B1%82%E5%92%8C.md) · [Lipschitz constant](../../Math%20%E5%9F%BA%E7%A1%80/%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/Lipschitz%20constant.md) · [梯度下降、学习率与收敛](../../Math%20%E5%9F%BA%E7%A1%80/%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E6%A2%AF%E5%BA%A6%E4%B8%8B%E9%99%8D%E3%80%81%E5%AD%A6%E4%B9%A0%E7%8E%87%E4%B8%8E%E6%94%B6%E6%95%9B.md)

## 适用场景

适用于大多数一阶优化算法：GD、SGD、normalized GD、简单 adaptive method、nonconvex optimization、RLHF optimizer 的基础收敛分析。只要你的算法可以写成

```text
x_{t+1} = x_t - eta_t * estimator_t
```

就可以先尝试这个模板。

## 核心证明骨架

令 $(\mathcal F_t)_ {t\ge0}$ 是算法历史， $x_t$ 为 $\mathcal F_t$-可测。假设 $f:\mathbb R^d\to\mathbb R$ 可微、 $L$-smooth 且下有界于 $f_\star$：

$$
f(y) \le f(x) + \langle \nabla f(x), y-x \rangle + \frac{L}{2}\Vert y-x\Vert^2.
$$

令

$$
x_{t+1}=x_t-\eta g_t.
$$

代入得到

$$
f(x_{t+1})
\le
f(x_t)
-\eta \langle \nabla f(x_t), g_t\rangle
+\frac{L\eta^2}{2}\Vert g_t\Vert^2.
$$

若 $g_t$ 在给定完整历史后条件无偏且方差有界：

$$
\mathbb E[g_t\mid\mathcal F_t]=\nabla f(x_t),
\qquad
\mathbb E[\Vert g_t-\nabla f(x_t)\Vert^2\mid\mathcal F_t]\le\sigma^2,
$$

则 $\mathbb E[\Vert g_t\Vert^2\mid\mathcal F_t]\le\Vert\nabla f(x_t)\Vert^2+\sigma^2$。对常步长 $0<\eta\le1/L$，有精确的一步界

$$
\mathbb E[f(x_{t+1})\mid\mathcal F_t]
\le
f(x_t)
-\eta\left(1-\frac{L\eta}{2}\right)\Vert\nabla f(x_t)\Vert^2
+\frac{L\eta^2}{2}\sigma^2
\le
f(x_t)-\frac{\eta}{2}\Vert\nabla f(x_t)\Vert^2
+\frac{L\eta^2}{2}\sigma^2.
$$

对 $t=0,\ldots,T-1$ 取全期望并求和，利用 $f(x_T)\ge f_\star$：

$$
\frac1T\sum_{t=0}^{T-1}\mathbb E\Vert\nabla f(x_t)\Vert^2
\le
\frac{2(f(x_0)-f_\star)}{\eta T}+L\eta\sigma^2.
$$

若 $R\sim\mathop{\mathrm{Unif}}\lbrace0,\ldots,T-1\rbrace$ 且独立于算法随机性，则平均项**等于** $\mathbb E\Vert\nabla f(x_R)\Vert^2$。还要区分下面三个量：

$$
\mathbb E\min_t\Vert\nabla f(x_t)\Vert^2
\leq \min_t\mathbb E\Vert\nabla f(x_t)\Vert^2
\leq \frac1T\sum_t\mathbb E\Vert\nabla f(x_t)\Vert^2.
$$

因此同一上界也控制前两项，但三者一般不相等；沿完整随机轨迹事后挑最小值，不等于预先独立抽取一个输出迭代。

上式默认 $x_0$ 确定；若 $x_0$ 随机，首项改为 $2(\mathbb E f(x_0)-f_\star)/(\eta T)$。步长仍需满足 $\eta\le1/L$；典型选择给出 $O(T^{-1/2})$ 噪声主导率。

<a id="t01-sgd-bound"></a>

^t01-sgd-bound

## 逐步证明模板

```text
Step 1. 写出 smoothness descent inequality。
Step 2. 把 y 换成算法更新 x_{t+1}。
Step 3. 把 estimator 拆成 true gradient + noise。
Step 4. 用 unbiasedness 消掉一阶噪声。
Step 5. 用 variance bound 控制二阶项。
Step 6. 得到 one-step expected descent。
Step 7. 对 t 求和，objective 项 telescope。
Step 8. 选 eta，整理 rate。
```

## 可复用 lemma 形状

```text
Lemma: Under lower boundedness, L-smoothness, conditional unbiasedness,
conditional variance at most sigma^2, and eta <= 1/L, SGD satisfies
(1/T) sum_t E||grad f(x_t)||^2
<= 2(f(x_0)-f_*)/(eta T) + L eta sigma^2.
```

## 常见坑

- `L-smooth` 对大模型训练经常太强；可以换成 T15 的 generalized smoothness。
- 如果算法有 momentum/EMA/error feedback，单看 `f(x_t)` 往往不下降；换 T02 的 Lyapunov。
- 如果 estimator 有 bias，要把 bias 项单独保留，不能直接用 unbiasedness 消掉。
- projected/proximal 更新不能直接把结论写成 $\Vert\nabla f\Vert$；应改用 gradient mapping 或 composite stationarity measure。
- SARAH/SPIDER 型 estimator 往往不逐步条件无偏；需要先用 T03 的 estimator-error 递推，再与 descent inequality 联立。

## 来源论文 / 参考

- SPIDER: Near-Optimal Non-Convex Optimization via Stochastic Path-Integrated Differential Estimator, NeurIPS 2018. https://proceedings.neurips.cc/paper/2018/hash/1543843a4723ed2ab08e18053ae6dc5b-Abstract.html
- SpiderBoost and Momentum: Faster Variance Reduction Algorithms, NeurIPS 2019. https://proceedings.neurips.cc/paper_files/paper/2019/hash/512c5cad6c37edb98ae91c8a76c3a291-Abstract.html
- Generalized-Smooth Nonconvex Optimization is as Efficient as Smooth Nonconvex Optimization, ICML 2023. https://proceedings.mlr.press/v202/chen23v.html

## 关联模板与本地证据

- [T02：给辅助状态误差记账，让联合势函数下降。](T02-lyapunov.md)
- [T03：用同一随机样本的梯度差，把估计误差绑定到移动路径。](T03-variance-reduction.md)
- [T15：曲率随梯度变化时，先证明局部下降和轨迹闭合。](T15-generalized-smoothness.md)
- [T16：把裁剪梯度分成 centered martingale 与 clipping bias。](T16-heavy-tail-clipping.md)

通用证明工具：P01、P02；见 [证明原语](../../通用证明原语.md)。

- [Convex Optimization: Algorithms and Complexity](../../proof_ref/foundations-2026-09/convex-optimization-algorithms-and-complexity-1405.4980/README.md) · [官方 arXiv](https://arxiv.org/abs/1405.4980)
- [Optimization Methods for Large-Scale Machine Learning](../../proof_ref/foundations-2026-09/optimization-methods-for-large-scale-machine-learning-1606.04838/README.md) · [官方 arXiv](https://arxiv.org/abs/1606.04838)

## 专项证明接口（2026-10-02）

- [T40：用负曲率下降补一阶驻点，并显式区分 Hessian oracle 与一阶逃逸复杂度。](T40-second-order-stationarity.md)
- [T47：分解 local training 的位置偏差并控制客户端分歧、通信与输出。](T47-local-training-client-drift.md)

## 经典与近期证明蒸馏

- [经典下降证明的偏差与方差接口](../../extensions/%E7%BB%8F%E5%85%B8%E4%B8%8B%E9%99%8D%E8%AF%81%E6%98%8E%E7%9A%84%E5%81%8F%E5%B7%AE%E4%B8%8E%E6%96%B9%E5%B7%AE%E6%8E%A5%E5%8F%A3.md)
