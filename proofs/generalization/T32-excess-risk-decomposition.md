---
id: T32
type: proof-template
refined: 2026-09-28
status: self-contained-core
---

# T32. Approximation–estimation–optimization decomposition

[主题目录](README.md) · [DL 理论总框架](../../docs/DL_THEORY_FRAMEWORK.md)

## 复用契约

**输入对象**：总体风险 $R$、经验风险 $\widehat R_S$、假设类 $\mathcal H$、训练输出 $\widehat h\in\mathcal H$ 和比较基准 $R^\star$。

**输出结论**：把最终风险差拆成模型类的逼近误差、有限样本误差和经验优化误差。

必需假设：风险与相关 infimum 有意义；训练输出属于所分析的类；经验优化 gap 有界。分解本身是确定性代数，概率保证来自另行证明的 uniform deviation。

**失败例子**：在 $f(w)=(w^2-1)^2$ 中， $w=0$ 的梯度为零，函数值却比全局最小值高 1。小梯度不能自动充当小 optimization gap。

## 实例化时必须完成

- [ ] 指明目标是 population excess risk、经验优化 gap，还是 stationarity。
- [ ] 说明 $\mathcal H$ 是否在看数据前固定；数据依赖类需要另付复杂度。
- [ ] 分别给出 approximation、estimation 和 optimization 的合法上界。
- [ ] 检查 bound 是否非空泛，以及宽度、样本数、训练步数的条件能否同时满足。

## 1. 三种误差分别在问什么

可以把学习比作选一个工具箱并用有限样品做校准：

- **逼近**：工具箱中最好的工具能做到多好？
- **估计**：有限样品能否准确评价这个工具箱里的候选？
- **优化**：训练过程是否找到了经验上足够好的候选？

训练损失很低只回答第三个问题的一部分。Universal approximation 只讨论第一个，也没有回答训练能否找到相应参数。

## 2. 不假设最优解一定存在

令 $R^\star$ 为更大比较类中的最优风险，定义

$$
\epsilon_{\rm app}=\inf_{h\in\mathcal H}R(h)-R^\star,\qquad
\Delta_S=\sup_{h\in\mathcal H}|R(h)-\widehat R_S(h)|.
$$

假设算法满足

$$
\widehat R_S(\widehat h)
\leq\inf_{h\in\mathcal H}\widehat R_S(h)+\epsilon_{\rm opt}.
$$

使用 inf 而非随意写 argmin，可以覆盖 logistic loss 等最优参数不一定有限的情形。

如果 $R^\star$ 对全部允许的可测预测器取 inf，它是该损失下的 Bayes risk；若只对一个较小参考类取 inf，就不能称为不受限的 Bayes 最优风险。

## 3. 逐步相加

对任意 $h\in\mathcal H$，

$$
\begin{aligned}
R(\widehat h)
&\leq \widehat R_S(\widehat h)+\Delta_S\\
&\leq \widehat R_S(h)+\epsilon_{\rm opt}+\Delta_S\\
&\leq R(h)+\epsilon_{\rm opt}+2\Delta_S.
\end{aligned}
$$

再对比较函数取 inf，得到

$$
R(\widehat h)-R^\star
\leq\epsilon_{\rm app}+2\Delta_S+\epsilon_{\rm opt}.
$$

两次 $\Delta_S$ 分别支付“训练输出从经验回到总体”和“比较函数从总体回到经验”。

若以概率至少 $1-\delta$ 有 $\Delta_S\leq\epsilon_{\rm est}$，且优化条件在这个事件上成立，则对应风险界才以该概率成立。若优化也依赖另一个 good event，需要合并失败概率。

## 4. 怎样连接其他模板

- [T34](../deep-learning/T34-neural-approximation.md)：在具体函数类、范数和网络预算下界 approximation。
- [T33](T33-uniform-convergence.md)：固定函数类的 uniform deviation。
- [T35](T35-margin-norm.md)、[T38](T38-compression.md)：给出不同复杂度控制。
- [T01](../optimization/T01-descent.md)：通常只给 stationarity；若要转成 optimization gap，需要 PL、凸性、NTK 区域等额外桥梁。
- [PL 例子](../../extensions/PL条件与SGD噪声地板.md)：展示一个可明确写出的桥梁。

## 5. 这不是解释一切的公式

如果 $\mathcal H$ 是用同一数据学习出来的表示空间，上述代数仍可逐样本写出，但不能直接调用固定类的浓缩定理。若用了 surrogate loss，还要证明 surrogate risk 到真正任务风险的校准关系。

只比较训练目标不同的两个算法，也不能只比较 $\epsilon_{\rm opt}$：它们可能改变了模型类、损失或数据 law。

### 一个直接的 DL 反例

取 $X\in[0,1]$、 $Y\equiv1$，平方损失，以及

$$
f_\theta(x)=\sum_{j=1}^m a_j\mathop{\mathrm{ReLU}}(b_jx+c_j).
$$

若全部 $a_j=b_j=0,c_j=-1$，隐藏单元在一个参数邻域内都关闭，模型输出 0，经验梯度恰为 0，总体风险为 1。但一个隐藏单元就能表示常数 1，因此类内最优与 Bayes 风险均为 0。

这里模型类已经能表示正确答案，训练却停在坏驻点；扩大网络族带来的万能逼近也不会自动解决它。这不反驳 [T09](../deep-learning/T09-ntk.md)，因为该初始化没有满足其 Gram 非退化条件。

## 自测与来源

“NTK 训练误差收敛到零，因此测试误差也为零”缺哪一项？还缺所选网络类/算法的统计误差与适当比较基准。

全景来源：[The Modern Mathematics of Deep Learning](https://arxiv.org/abs/2105.04026)。本卡中的三项分解已逐步给出，具体各项 rate 由所接模板负责。

## 本地论文与前置工具

通用工具：P01, P09，见 [证明原语](../../通用证明原语.md)。

- [The Modern Mathematics of Deep Learning](../../proof_ref/dl-core-2026-09/the-modern-mathematics-of-deep-learning-2105.04026/README.md)

## 专项证明接口（2026-10-02）

- [T40：用负曲率下降补一阶驻点，并显式区分 Hessian oracle 与一阶逃逸复杂度。](../optimization/T40-second-order-stationarity.md)
- [T41：用表示范数与 Hilbert-space 方差控制高维随机特征的逼近误差。](../deep-learning/T41-barron-random-feature-approximation.md)
- [T42：精确跟踪时变核、参数移动与冻结核近似，不把核变化当下游收益。](../deep-learning/T42-feature-drift-kernel-dynamics.md)
- [T49：由 binary log-loss excess 推到分类 excess，并保留模型与裁剪误差。](T49-surrogate-bayes-risk.md)

## 经典与近期证明蒸馏

- [T51：在真实边缘分布下控制速度误差，用学习场 Lipschitz 与耦合推出 Wasserstein 界。](../generation-transport/T51-flow-trajectory-error.md)
