---
type: roadmap
domain: math/proof-tools
status: active
created: 2026-09-01
reviewed: 2026-09-01
---

# AI 理论证明前置学习路线

这条路线连接三类材料：

1. 基础数学笔记告诉你对象和公式是什么；
2. 证明前置笔记解释常见证明动作为什么成立；
3. [证明模板库（待核查）](../../proofs/README.md)、[通用证明原语](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md) 和本地 PDF 展示这些动作如何组合成真实论文证明。

先抓住一句话：

> 看懂证明，不等于能逐行抄公式；真正要看见的是“这一行使用了什么假设，把哪一种对象变成了哪一种更容易控制的对象”。

例如，论文里一句“由 Freedman 不等式可得”背后至少要检查：随机变量是否适应同一 filtration、条件均值是否为零、增量是否有界、使用的是确定方差还是 predictable quadratic variation、结论是 fixed-time 还是 time-uniform。

## 0. 进入前的最低基础

建议先能使用：

- 线性代数：[向量空间、基、秩与 SVD](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E5%90%91%E9%87%8F%E7%A9%BA%E9%97%B4%E3%80%81%E5%9F%BA%E3%80%81%E7%A7%A9%E4%B8%8E%20SVD.md)、[二次型、正定矩阵与谱](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E4%BA%8C%E6%AC%A1%E5%9E%8B%E3%80%81%E6%AD%A3%E5%AE%9A%E7%9F%A9%E9%98%B5%E4%B8%8E%E8%B0%B1.md)；
- 微积分与优化：[导数、梯度、Jacobian、Hessian 与自动微分](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E5%AF%BC%E6%95%B0%E3%80%81%E6%A2%AF%E5%BA%A6%E3%80%81Jacobian%E3%80%81Hessian%20%E4%B8%8E%E8%87%AA%E5%8A%A8%E5%BE%AE%E5%88%86.md)、[凸集、凸函数与优化直觉](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E5%87%B8%E9%9B%86%E3%80%81%E5%87%B8%E5%87%BD%E6%95%B0%E4%B8%8E%E4%BC%98%E5%8C%96%E7%9B%B4%E8%A7%89.md)、[梯度下降、学习率与收敛](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/%E6%A2%AF%E5%BA%A6%E4%B8%8B%E9%99%8D%E3%80%81%E5%AD%A6%E4%B9%A0%E7%8E%87%E4%B8%8E%E6%94%B6%E6%95%9B.md)；
- 概率统计：[概率论主干：联合、条件、期望与协方差](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%A6%82%E7%8E%87%E8%AE%BA%E4%B8%BB%E5%B9%B2%EF%BC%9A%E8%81%94%E5%90%88%E3%80%81%E6%9D%A1%E4%BB%B6%E3%80%81%E6%9C%9F%E6%9C%9B%E4%B8%8E%E5%8D%8F%E6%96%B9%E5%B7%AE.md)、[大数定律、中心极限定理与采样误差](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E5%A4%A7%E6%95%B0%E5%AE%9A%E5%BE%8B%E3%80%81%E4%B8%AD%E5%BF%83%E6%9E%81%E9%99%90%E5%AE%9A%E7%90%86%E4%B8%8E%E9%87%87%E6%A0%B7%E8%AF%AF%E5%B7%AE.md)；
- 信息论：[信息论基础：熵、交叉熵与 KL 散度](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E4%BF%A1%E6%81%AF%E8%AE%BA%E5%9F%BA%E7%A1%80%EF%BC%9A%E7%86%B5%E3%80%81%E4%BA%A4%E5%8F%89%E7%86%B5%E4%B8%8E%20KL%20%E6%95%A3%E5%BA%A6.md)；
- 随机过程：[Markov 链、随机过程与状态空间模型](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/Markov%20%E9%93%BE%E3%80%81%E9%9A%8F%E6%9C%BA%E8%BF%87%E7%A8%8B%E4%B8%8E%E7%8A%B6%E6%80%81%E7%A9%BA%E9%97%B4%E6%A8%A1%E5%9E%8B.md)。

高阶生成模型或信息几何证明还会用到 [AI Researcher 高阶数学路线：LLM、CV 与生成模型](../AI%20Researcher%20%E9%AB%98%E9%98%B6%E6%95%B0%E5%AD%A6%E8%B7%AF%E7%BA%BF%EF%BC%9ALLM%E3%80%81CV%20%E4%B8%8E%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B.md)。

## 1. 第一层：先把 theorem 读成一份合同

从 [量词、归纳、不变量与望远镜求和](%E9%87%8F%E8%AF%8D%E3%80%81%E5%BD%92%E7%BA%B3%E3%80%81%E4%B8%8D%E5%8F%98%E9%87%8F%E4%B8%8E%E6%9C%9B%E8%BF%9C%E9%95%9C%E6%B1%82%E5%92%8C.md) 开始。

阅读定理时先标出：

- **对象**：对所有数据分布、固定问题实例，还是存在某个算法？
- **随机性**：概率是对数据、算法、环境还是初始化取的？
- **结论类型**：确定性、期望、高概率、渐近还是经验观察？
- **资源**：样本数、迭代数、查询数、模型宽度怎样进入？
- **metric**：控制的是函数值、参数误差、TV、KL、Wasserstein 还是 regret？
- **失败方式**：去掉哪个假设，定理会在哪一步坏掉？

对应模板入口：[P01 定理规格](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p01-%E5%AE%9A%E7%90%86%E8%A7%84%E6%A0%BC%E5%85%88%E5%86%99%E9%87%8F%E8%AF%8D%E5%AF%B9%E8%B1%A1%E4%B8%8E%E5%A4%B1%E8%B4%A5%E6%96%B9%E5%BC%8F)、[模板使用说明](../../docs/PROOF_WORKFLOW.md)。

## 2. 第二层：递推、势函数与误差账本

大量优化、RL 和稳定性证明都可压缩为：

$$
\Phi_{t+1}
\le \Phi_t-\text{progress}_t+\text{error}_t.
$$

然后做望远镜求和：初始势能减最终势能，再加累计误差。

重点学习：

- 归纳假设为什么必须包含下一步真正需要的 invariant；
- potential/Lyapunov 函数怎样把多个变量装进一个标量账本；
- 时间变系数为什么会产生额外差分项；
- local error 为什么不能总是直接相加。

对应：[T01](../../proofs/optimization/T01-descent.md)、[T02](../../proofs/optimization/T02-lyapunov.md)、[T03](../../proofs/optimization/T03-variance-reduction.md)。

## 3. 第三层：概率空间、条件信息与“到时刻 t 为止知道什么”

读 [测度、条件期望、滤过与适应过程](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%B5%8B%E5%BA%A6%E3%80%81%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E3%80%81%E6%BB%A4%E8%BF%87%E4%B8%8E%E9%80%82%E5%BA%94%E8%BF%87%E7%A8%8B.md)。

这层回答：

- 为什么事件必须属于某个 $\sigma$-algebra；
- 条件期望为什么是“在已有信息下最好的可测预测”；
- filtration $\mathcal F_t$ 怎样表示信息随时间增长；
- adapted、predictable、stopping time 分别约束什么；
- change of measure 为何需要绝对连续与 Radon–Nikodym derivative。

它是 martingale、在线学习、RL、prefix-safety、Girsanov 和 PAC-Bayes 的共同语法。

对应：[P04](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p04-mgf-concentrationmartingale-%E4%B8%8E%E8%87%AA%E5%BD%92%E4%B8%80%E5%8C%96)、[P05](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p05-couplingchange-of-measure-%E4%B8%8E%E4%BF%A1%E6%81%AF%E9%A2%84%E7%AE%97)、[T23](../../proofs/evaluation-monitoring/T23-prefix-safety.md)。

## 4. 第四层：浓缩不等式与鞅

读 [集中不等式、MGF、鞅与自归一化过程](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E9%9B%86%E4%B8%AD%E4%B8%8D%E7%AD%89%E5%BC%8F%E3%80%81MGF%E3%80%81%E9%9E%85%E4%B8%8E%E8%87%AA%E5%BD%92%E4%B8%80%E5%8C%96%E8%BF%87%E7%A8%8B.md)。它按同一条推导链组织：

1. MGF、Chernoff、Hoeffding、Bernstein 与 variance proxy；
2. martingale difference、Azuma、Freedman 与 optional stopping；
3. confidence sequence、time-uniform 与 self-normalized；
4. 线性 bandit/RL 中随数据变化的矩阵范数、log-det 和 elliptical potential。

目标是解释“为什么能从随机噪声得到一个 confidence radius”，而不是只提供不等式公式卡。

对应：[T06](../../proofs/sequential-decision/T06-linear-bandit.md)、[T16](../../proofs/optimization/T16-heavy-tail-clipping.md)、[R03](../../%E8%BF%91%E6%9C%9F%E9%A1%B6%E4%BC%9A%E7%90%86%E8%AE%BA%E6%A1%86%E6%9E%B6%EF%BC%882025-2026%EF%BC%89.md#r03-time-uniform-self-normalized-concentration)。

## 5. 第五层：非欧氏优化与在线 regret

读 [Bregman 散度、Mirror Descent 与在线学习](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/Bregman%20%E6%95%A3%E5%BA%A6%E3%80%81Mirror%20Descent%20%E4%B8%8E%E5%9C%A8%E7%BA%BF%E5%AD%A6%E4%B9%A0.md)。

欧氏梯度下降用平方距离做势函数；Mirror Descent 换成与可行域匹配的 Bregman geometry。例如概率单纯形上，负熵势函数会导出 KL 型更新。

要分清：

- Bregman divergence 一般不对称，不是 metric；
- primal norm 与 dual norm 必须配对；
- strong convexity 是把 Bregman divergence 下界成平方范数的关键；
- FTRL、Mirror Descent、KL-regularized policy update 相关但不是无条件同一个算法。

对应：[T08](../../proofs/sequential-decision/T08-mirror-descent.md)、[P06](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p06-convex%E6%80%A7bregman-%E5%87%A0%E4%BD%95%E4%B8%8E%E5%AF%B9%E5%81%B6)、[R01](../../%E8%BF%91%E6%9C%9F%E9%A1%B6%E4%BC%9A%E7%90%86%E8%AE%BA%E6%A1%86%E6%9E%B6%EF%BC%882025-2026%EF%BC%89.md#r01-%E7%BB%93%E6%9E%84%E6%80%A7%E8%B4%A8--%E5%8F%98%E5%BA%A6%E9%87%8F%E5%8A%BF%E5%87%BD%E6%95%B0--%E7%AE%97%E6%B3%95%E7%89%B9%E5%8C%96)。

## 6. 第六层：泛化证明不是只套 Hoeffding

读 [算法稳定性、经验过程与 PAC-Bayes](../%E7%BB%9F%E8%AE%A1%E5%AD%A6%E4%B9%A0%E7%90%86%E8%AE%BA/%E7%AE%97%E6%B3%95%E7%A8%B3%E5%AE%9A%E6%80%A7%E3%80%81%E7%BB%8F%E9%AA%8C%E8%BF%87%E7%A8%8B%E4%B8%8E%20PAC-Bayes.md)。

三条常见路线回答的是不同问题：

- **algorithmic stability**：换一个训练样本，算法输出改变多少；
- **empirical process**：整个函数类的经验均值怎样同时接近总体均值；
- **PAC-Bayes**：用 posterior/prior KL 支付数据依赖 predictor 的复杂度。

需要掌握 ghost sample、symmetrization、Rademacher signs、covering number、union bound、local complexity 和 change-of-measure 的角色。

对应：[T04](../../proofs/generalization/T04-stability.md)、[T05](../../proofs/generalization/T05-pac-bayes-information.md)、[P09](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p09-empirical-processsymmetrizationcovering-%E4%B8%8E-local-complexity)。

## 7. 第七层：证明“不可能”

读 [统计距离、Le Cam、Fano、Assouad 与 Yao 下界](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E7%BB%9F%E8%AE%A1%E8%B7%9D%E7%A6%BB%E3%80%81Le%20Cam%E3%80%81Fano%E3%80%81Assouad%20%E4%B8%8E%20Yao%20%E4%B8%8B%E7%95%8C.md)。

下界证明通常不直接攻击任意算法，而是：

1. 构造多个彼此足够远、观测上又难区分的实例；
2. 把估计或优化成功归约为 testing 成功；
3. 用 KL、TV、Hellinger 或 mutual information 控制可辨识性；
4. 用 Le Cam、Fano、Assouad 或 Yao 把 testing error 变回风险下界。

交互算法还要对 transcript 使用 KL chain rule，并证明 algorithm kernel 在两环境中如何抵消。

对应：[T12](../../proofs/lower-bounds-expressivity/T12-information-lower-bounds.md)、[P10](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p10-reductiontesting-lower-bound-%E4%B8%8E-yao-principle)、[R02](../../%E8%BF%91%E6%9C%9F%E9%A1%B6%E4%BC%9A%E7%90%86%E8%AE%BA%E6%A1%86%E6%9E%B6%EF%BC%882025-2026%EF%BC%89.md#r02-oracle-lower-bound%E5%9B%B0%E9%9A%BE%E6%97%8F--%E8%AF%86%E5%88%AB--divergence-decomposition)。

## 8. 第八层：矩阵与子空间误差

读 [矩阵浓缩、谱扰动与子空间误差](../%E7%BA%BF%E6%80%A7%E4%BB%A3%E6%95%B0/%E7%9F%A9%E9%98%B5%E6%B5%93%E7%BC%A9%E3%80%81%E8%B0%B1%E6%89%B0%E5%8A%A8%E4%B8%8E%E5%AD%90%E7%A9%BA%E9%97%B4%E8%AF%AF%E5%B7%AE.md)。

它连接：

- scalar concentration 怎样升级到 operator norm；
- Weyl 怎样控制特征值；
- Davis–Kahan 为什么必须有 eigengap；
- Schur complement 如何处理 block PSD；
- 随机 Gram/covariance 矩阵何时接近总体对象。

对应：[P08](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p08-spectral-%E4%B8%8E%E7%9F%A9%E9%98%B5%E6%89%B0%E5%8A%A8)、[T09](../../proofs/deep-learning/T09-ntk.md)、[T25](../../proofs/generation-transport/T25-feature-localization-card.md)。

## 9. 第九层：稳定性、连续动力学与 PDE 误差传播

读 [Grönwall、Duhamel 与稳定性误差传播](../%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/Gr%C3%B6nwall%E3%80%81Duhamel%20%E4%B8%8E%E7%A8%B3%E5%AE%9A%E6%80%A7%E8%AF%AF%E5%B7%AE%E4%BC%A0%E6%92%AD.md)。

这层把三个常见结构串起来：

- contraction / Banach fixed point：每一步按固定比例缩小差异；
- Grönwall：局部增长率与外部误差怎样指数累计；
- Duhamel / variation of constants：把受迫系统解写成“自由演化 + 过去所有 forcing 的传播”。

它是 optimizer stability、mean-field/propagation of chaos、ODE/SDE 数值误差和 diffusion/flow PDE bound 的共同桥梁。

对应：[P07](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md#p07-contractiongr%C3%B6nwall-%E4%B8%8E%E7%A8%B3%E5%AE%9A%E6%80%A7%E9%80%92%E6%8E%A8)、[T10](../../proofs/deep-learning/T10-mean-field.md)、[T13](../../proofs/generation-transport/T13-sampler-error.md)、[R10](../../%E8%BF%91%E6%9C%9F%E9%A1%B6%E4%BC%9A%E7%90%86%E8%AE%BA%E6%A1%86%E6%9E%B6%EF%BC%882025-2026%EF%BC%89.md#r10-flow-error-pde--duhamel--tv-bound--trainable-surrogate)。

## 10. 第十层：交换性与有限样本覆盖保证

读 [交换性、Conformal Prediction 与覆盖保证](../%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E4%BA%A4%E6%8D%A2%E6%80%A7%E3%80%81Conformal%20Prediction%20%E4%B8%8E%E8%A6%86%E7%9B%96%E4%BF%9D%E8%AF%81.md)。

split conformal 的核心不是“残差近似高斯”，而是校准分数与测试分数在 exchangeability 下具有对称秩。它给的是边际覆盖；conditional coverage、risk control 与 distribution shift 需要额外条件和不同方法。

对应：[T18](../../proofs/statistics/T18-split-conformal.md)。

## 10.1 共同主干与方向选修

第 1–5 层是大多数理论论文都会复用的共同主干；第 6–10 层不是严格线性依赖，应按研究方向选修：

- 泛化 / AI statistics：第 6、7、10 层；
- Bandit / RL / online learning：第 4、5、7、8 层；
- Diffusion / flow / world model：第 3、4、7、9 层，再补 stochastic calculus、Girsanov 与 PDE regularity；
- Transformer construction / ICL dynamics：第 1、2、8、9 层，再补 ReLU approximation 与 linear dynamical systems；研究 T20 时还需 formal language / circuit complexity 专论。

不要把完成本路线写成“已经掌握所有 T01–T25”。它提供公共接口，方向特有工具仍需回到具体论文补齐。

## 11. 模板到 PDF 的正确学习顺序

不要从 2,600 行模板库顺序硬读。使用 [数学前置与论文证明导航](../../%E6%95%B0%E5%AD%A6%E5%89%8D%E7%BD%AE%E4%B8%8E%E8%AE%BA%E6%96%87%E8%AF%81%E6%98%8E%E5%AF%BC%E8%88%AA.md)：

1. 选择当前研究问题对应的 T/P/R 编号；
2. 先打开该行列出的数学前置笔记；
3. 再读模板的“适用场景、骨架、常见坑”；
4. 打开核验卡确认 theorem 的真实假设；
5. 最后跳到本地 `paper.pdf#page=N` 查看原文，并在需要逐式追踪时打开 TeX。

PDF 不能反向写入 Markdown 链接，因此本库采用“PDF 同目录 README/核验卡反链数学前置”的方式实现双向可达。

## 12. 建议的 10 周顺序

| 周次 | 主题 | 最低成果 |
|---|---|---|
| 1 | 定理合同、归纳、望远镜 | 能把一个 theorem 拆成量词/随机性/metric/资源 |
| 2 | 测度、条件期望、filtration | 能检查 adapted、predictable 与 stopping time |
| 3 | MGF、次高斯与 Bernstein | 能从 MGF 做一次 Chernoff 优化 |
| 4 | Martingale 与 self-normalized | 能写出 Freedman 的条件和线性 bandit confidence norm |
| 5 | Bregman 与 Mirror Descent | 能推三点恒等式和一次 regret telescope |
| 6 | Stability、Rademacher、PAC-Bayes | 能说明三条泛化路线分别控制什么 |
| 7 | Le Cam/Fano/Assouad/Yao | 能把估计问题归约成 testing 问题 |
| 8 | Matrix concentration / perturbation | 能解释 operator norm 与 eigengap 的作用 |
| 9 | Grönwall / Duhamel | 能把局部误差传播成全局界并保留指数因子 |
| 10 | Conformal / 综合复现 | 从模板、核验卡、PDF、TeX 复现一条短证明链 |

## 掌握标准

- [ ] 能说出每个工具真正需要的条件；概率不等式另检查可测性、尾部/矩或有界性假设；
- [ ] 能区分 fixed-instance / uniform、expectation / high probability；
- [ ] 能画出 proof dependency DAG，而不是只复述结论；
- [ ] 能指出一个假设删掉后的反例或失败步骤；
- [ ] 能从数学前置跳到模板、核验卡、PDF 页码，再从核验卡返回前置笔记。

## 导航

- 数学总目录：[Math 基础目录](../Math%20%E5%9F%BA%E7%A1%80%E7%9B%AE%E5%BD%95.md)
- 高阶 LLM/CV 数学：[AI Researcher 高阶数学路线：LLM、CV 与生成模型](../AI%20Researcher%20%E9%AB%98%E9%98%B6%E6%95%B0%E5%AD%A6%E8%B7%AF%E7%BA%BF%EF%BC%9ALLM%E3%80%81CV%20%E4%B8%8E%E7%94%9F%E6%88%90%E6%A8%A1%E5%9E%8B.md)
- 证明模板：[证明模板库（待核查）](../../proofs/README.md)
- 通用原语：[通用证明原语](../../%E9%80%9A%E7%94%A8%E8%AF%81%E6%98%8E%E5%8E%9F%E8%AF%AD.md)
- 近期框架：[近期顶会理论框架（2025-2026）](../../%E8%BF%91%E6%9C%9F%E9%A1%B6%E4%BC%9A%E7%90%86%E8%AE%BA%E6%A1%86%E6%9E%B6%EF%BC%882025-2026%EF%BC%89.md)
- PDF 核验导航：[核验导航](../../proof_ref/%E6%A0%B8%E9%AA%8C%E5%AF%BC%E8%88%AA.md)
- 模板—前置—PDF 映射：[数学前置与论文证明导航](../../%E6%95%B0%E5%AD%A6%E5%89%8D%E7%BD%AE%E4%B8%8E%E8%AE%BA%E6%96%87%E8%AF%81%E6%98%8E%E5%AF%BC%E8%88%AA.md)
