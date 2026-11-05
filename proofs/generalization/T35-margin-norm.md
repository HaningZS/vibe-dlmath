---
id: T35
type: proof-template
refined: 2026-09-28
status: self-contained-core
---

# T35. Margin and norm-based generalization

[主题目录](README.md) · [一致收敛](T33-uniform-convergence.md)

## 复用契约

**输入对象**：二分类 score $f$、标签 $Y\in\lbrace-1,1\rbrace$、margin $\gamma>0$ 和预先固定的 norm-constrained class。

**输出结论**：经验低间隔比例加复杂度项的总体分类风险界。

必需假设：i.i.d. 样本；输入范数受控；函数类与 $\gamma$ 的选择满足所用统一事件；loss/Rademacher 定义一致。

**失败例子**：把所有 logits 乘以大常数会放大原始 margin，却不改变分类器。没有同步的范数归一化，不能据此宣称泛化提高。

## 实例化时必须完成

- [ ] 固定 raw margin、normalized margin 和 norm budget 的定义。
- [ ] 使用 bounded ramp 等合法 surrogate 连接 0–1 风险。
- [ ] 实际界定 loss class 的复杂度。
- [ ] 对数据后选的 $\gamma$、范数半径或网络架构支付额外选择预算。

## 1. 间隔像安全余量

正确分类只要求 $Yf(X)>0$；更大的正值意味着离当前决策边界更远。但这个量的单位依赖 score 的尺度，所以需要和模型范数一起看。

定义 ramp loss

$$
\phi_\gamma(u)=
\begin{cases}
1,&u\leq0,\\
1-u/\gamma,&0< u<\gamma,\\
0,&u\geq\gamma.
\end{cases}
$$

它在 $[0,1]$ 中，且为 $1/\gamma$-Lipschitz。保守地将边界也计为错误，有

$$
\mathbf1\lbrace Yf(X)\leq0\rbrace\leq\phi_\gamma(Yf(X))
\leq\mathbf1\lbrace Yf(X)\leq\gamma\rbrace.
$$

## 2. 线性类给出可以算清的例子

考虑 $f_w(x)=\langle w,x\rangle$、 $\Vert w\Vert_2\leq W$、 $\Vert X\Vert_2\leq B$，其中 $W,B,\gamma$ 事先固定。

对任一固定样本，margin class 的单侧 Rademacher complexity 是

$$
\begin{aligned}
\mathbb E_\sigma\sup_{\Vert w\Vert\leq W}
\frac1n\sum_i\sigma_iY_i\langle w,X_i\rangle
&=\frac Wn\mathbb E_\sigma\left\Vert\sum_i\sigma_iY_iX_i\right\Vert\\
&\leq\frac Wn\sqrt{\sum_i\Vert X_i\Vert^2}
\leq\frac{WB}{\sqrt n}.
\end{aligned}
$$

第二步用了 Jensen；随机符号使交叉项期望为零。

## 3. 从 score 复杂度到风险

采用 [T33](T33-uniform-convergence.md) 的单侧 convention。对 ramp 先减去 $\phi_\gamma(0)$，常数的符号和期望为零；在线性类对称、含零的情形，标量 Lipschitz contraction 给出

$$
\mathfrak R_n(\phi_\gamma\circ\mathcal F)
\leq\frac{WB}{\gamma\sqrt n}.
$$

再用 bounded loss 的单侧统一界：以概率至少 $1-\delta$，对所有 $\Vert w\Vert\leq W$，

$$
\Pr(Y\langle w,X\rangle\leq0)
\leq
\frac1n\sum_i\mathbf1\lbrace Y_i\langle w,X_i\rangle\leq\gamma\rbrace
+\frac{2WB}{\gamma\sqrt n}
+\sqrt{\frac{\log(1/\delta)}{2n}}.
$$

这展示了经验 margin 与类复杂度之间的交易。它不是自动紧的界；右边超过 1 时，对错误率而言就是空泛的。

## 4. 缩放为什么不能免费改善证书

取 $c>0$，将 $w$ 改成 $cw$，并将 threshold 改成 $c\gamma$，经验低间隔比例不变，且

$$
\frac{\Vert cw\Vert}{c\gamma}=\frac{\Vert w\Vert}{\gamma}.
$$

对应上一节的固定类证书，还应同步把预算 $W$ 改成 $cW$；复杂度项 $(cW)B/(c\gamma\sqrt n)$ 同样不变。不能把事后观测的 $\Vert\widehat w\Vert$ 不加说明地替换进原本事先固定的 $W$。

正齐次 ReLU 网络还存在层间重缩放，例如前层乘 $c$、后层除 $c$ 可保持函数不变。一个复杂度度量若仅因这类重新参数化变化，就需要审查它到底在控制什么。

## 5. 深网络的谱范数界怎样读

深网络论文可能使用谱范数乘积再乘结构修正项；不能把上面的 $W$ 随意替换成参数个数、Frobenius 总和或谱乘积，就宣称得到同一个 theorem。

应核对激活的 Lipschitz/齐次性、偏置、输出维数、参考矩阵、深度、覆盖数与 margin normalization。若希望用训练后观测到的 norm，需引用允许这种适应性的版本或预先分层/分配失败概率。

来源：[Spectrally-normalized margin bounds](https://arxiv.org/abs/1706.08498)。本卡完整推导线性原型，深网络的具体修正因子以固定原文版本为准。

## 本地论文与前置工具

通用工具：P04, P09，见 [证明原语](../../通用证明原语.md)。

- [Spectrally-normalized margin bounds for neural networks](../../proof_ref/dl-core-2026-09/spectrally-normalized-margin-bounds-for-neural-networks-1706.08498/README.md)

## 专项证明接口（2026-10-02）

- [T45：从 Lipschitz margin 或 Gaussian 平移事件推导指定范数的认证半径。](T45-certified-robustness.md)
