---
id: T15
type: proof-template
refined: 2026-09-28
status: "refined + claim-checked"
---

# T15. Generalized smoothness / unbounded smoothness

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

曲率随梯度变化时，先证明局部下降和轨迹闭合。

## 复用契约

**输入对象**：具体 smoothness 定义、更新线段、安全区与停止时间。

**输出结论**：该 smoothness 定义下的局部 descent 框架；rate 依赖 ℓ、算法和额外条件。

**必需假设**：

- 曲率控制在相关线段上成立，不只在端点成立。
- 移动半径/步长确保局部引理可用。
- 证明安全区不退出，避免循环假设梯度有界。

**失败例子**：端点梯度有限，线段仍可能经过高曲率区域。

## 实例化时必须完成

- [ ] 固定定义域与正则性。
- [ ] 积分线段或应用已核对局部引理。
- [ ] 闭合 stopped process 并再求和。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [Lipschitz constant](../../Math%20%E5%9F%BA%E7%A1%80/%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/Lipschitz%20constant.md) · [Hölder/Young](../../Math%20%E5%9F%BA%E7%A1%80/%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/%E9%87%8F%E8%AF%8D%E3%80%81%E5%BD%92%E7%BA%B3%E3%80%81%E4%B8%8D%E5%8F%98%E9%87%8F%E4%B8%8E%E6%9C%9B%E8%BF%9C%E9%95%9C%E6%B1%82%E5%92%8C.md#4-cauchyschwarzh%C3%B6lder-%E4%B8%8E-young%E6%80%8E%E6%A0%B7%E6%8B%86%E4%BA%A4%E5%8F%89%E9%A1%B9) · [Grönwall、Duhamel 与稳定性误差传播](../../Math%20%E5%9F%BA%E7%A1%80/%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/Gr%C3%B6nwall%E3%80%81Duhamel%20%E4%B8%8E%E7%A8%B3%E5%AE%9A%E6%80%A7%E8%AF%AF%E5%B7%AE%E4%BC%A0%E6%92%AD.md)

## 适用场景

大模型训练、Transformer optimization、Adam、bilevel、multi-objective optimization。传统 global L-smooth 假设不可信时使用。

## 核心假设例子

`(L0,L1)`-smoothness：

$$
\|\nabla^2 f(x)\|
\le
L_0 + L_1\|\nabla f(x)\|.
$$

更一般的 `ell`-smoothness：

$$
\|\nabla^2 f(x)\|
\le
\ell(\|\nabla f(x)\|),
$$

其中 `ell` 是非下降函数。

## 核心证明变化

T01 的 standard descent lemma 改成 generalized descent lemma。局部曲率可能随 gradient norm 增大，因此要用：

- normalized step；
- clipping；
- adaptive step；
- Polyak step；
- trajectory gradient bound。

为避免“先假设 gradient 有界才能证明 descent，再用 descent 证明 gradient 有界”的循环，可使用 localization。给定安全阈值 $G$，定义

$$
\tau_G=\inf\{t\ge0:\|\nabla f(x_t)\|>G\}.
$$

先只在 stopped process $x_{t\wedge\tau_G}$ 上使用局部 generalized descent；再用目标下界、一步 movement bound 或联合归纳证明在目标时间内 $\tau_G>T$。只有完成这个 closure，才能把 stopped bound 还原为原始 trajectory bound。

<a id="t15-localization"></a>

^t15-localization

## 逐步证明模板

### 为什么要控制整条更新线段

以 $C^2$ 且 $\|\nabla^2f(z)\|_{\mathrm{op}}\leq L_0+L_1\|\nabla f(z)\|$ 为例。若该条件在从 $x$ 到 $x+h$ 的线段上成立，沿弧长积分并使用 Grönwall，可得

$$
L_0+L_1\|\nabla f(x+s u)\|
\leq (L_0+L_1\|\nabla f(x)\|)e^{L_1s},
\quad u=h/\|h\|,\quad 0\leq s\leq\|h\|.
$$

于是，当 $\|h\|\leq r$ 时，一个方便但较松的局部下降式为

$$
f(x+h)\leq f(x)+\langle\nabla f(x),h\rangle
+\frac12(L_0+L_1\|\nabla f(x)\|)e^{L_1r}\|h\|^2.
$$

$h=0$ 可直接处理， $L_1=0$ 退化为标准光滑形式。这段计算说明步长为什么需要与移动半径和当前梯度一起选择；只有端点曲率信息并不足够。

```text
Step 1. 用 generalized smoothness 写出局部二阶上界。
Step 2. 推出 generalized descent lemma。
Step 3. 设计 step size / clipping threshold，并定义 safe region 或 stopping time。
Step 4. 在 stopped process 上证明 one-step descent 与 movement bound。
Step 5. 用目标下界/联合归纳闭合 localization，证明目标时间内没有离开 safe region。
Step 6. telescope objective 或 Lyapunov。
Step 7. 根据具体 $\ell$、凸性和算法整理 rate；不能预设一定与 smooth case 相同。
```

## 常见坑

- 不能直接套 L-smooth descent lemma。
- 要证明 trajectory 不会跑进曲率过大的区域。
- generalized smoothness 假设要与具体模型/损失有关，否则只是换了个名字。
- Hessian 形式通常要求 $C^2$；gradient-difference 形式与 Hessian 形式的等价需在具体定义域和正则性下证明。

## 来源论文 / 参考

- Generalized-Smooth Nonconvex Optimization is as Efficient as Smooth Nonconvex Optimization, ICML 2023. https://proceedings.mlr.press/v202/chen23v.html
- Convex and Non-convex Optimization Under Generalized Smoothness, NeurIPS 2023. https://proceedings.neurips.cc/paper_files/paper/2023/hash/7e8bb8d17bb1cb24dfe972a2f8ff2500-Abstract-Conference.html
- Methods for Convex `(L0,L1)`-Smooth Optimization: Clipping, Acceleration, and Adaptivity, ICLR 2025. https://openreview.net/forum?id=0wmfzWPAFu
- MGDA Converges under Generalized Smoothness, Provably, ICLR 2025. https://openreview.net/forum?id=wgDB1QuxIA
- 本地核验：[核验笔记](../../proof_ref/core-theory-2026-09/generalized-smooth-nonconvex-optimization-is-as-efficient-as-2303.02854/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md) · [PDF](../../proof_ref/core-theory-2026-09/generalized-smooth-nonconvex-optimization-is-as-efficient-as-2303.02854/paper.pdf#page=5)

## 关联模板与本地证据

- [T01：把单步目标下降累积成平均梯度平方界。](T01-descent.md)
- [T02：给辅助状态误差记账，让联合势函数下降。](T02-lyapunov.md)
- [T16：把裁剪梯度分成 centered martingale 与 clipping bias。](T16-heavy-tail-clipping.md)

通用证明工具：P02、P07；见 [证明原语](../../通用证明原语.md)。

- [Generalized-Smooth Nonconvex Optimization is As Efficient As Smooth Nonconvex Optimization](../../proof_ref/core-theory-2026-09/generalized-smooth-nonconvex-optimization-is-as-efficient-as-2303.02854/README.md) · [官方 arXiv](https://arxiv.org/abs/2303.02854)
