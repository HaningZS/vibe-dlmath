---
id: T05
type: proof-template
refined: 2026-09-28
status: "refined + claim-checked"
---

# T05. PAC-Bayes / information-theoretic generalization

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

分开使用 PAC-Bayes 高概率界和互信息期望界。

## 复用契约

**输入对象**：loss、数据 S、先验 P、后验 Q 或随机学习器 W。

**输出结论**：PAC-Bayes 在同一高概率事件上对所有 Q；MI 对数据和算法随机性取期望。

**必需假设**：

- PAC-Bayes-kl：i.i.d. 数据、[0,1] loss、独立先验与 Q≪P。
- MI 版本：固定 w 的 loss 满足所引定理的统一矩条件。
- 明确 Gibbs predictor 与最终确定性网络的关系。

**失败例子**：用训练集选 P=Q(S) 后以 KL=0 宣称免费泛化，违反标准独立先验条件。

## 实例化时必须完成

- [ ] 锁定定理版本及量词。
- [ ] 检查绝对连续；连续先验下 Dirac 后验的 KL 常无穷大。
- [ ] 不在 MI 界里直接添加 delta 改成高概率。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!tip] 数学前置
> [算法稳定性、经验过程与 PAC-Bayes](../../Math%20%E5%9F%BA%E7%A1%80/%E7%BB%9F%E8%AE%A1%E5%AD%A6%E4%B9%A0%E7%90%86%E8%AE%BA/%E7%AE%97%E6%B3%95%E7%A8%B3%E5%AE%9A%E6%80%A7%E3%80%81%E7%BB%8F%E9%AA%8C%E8%BF%87%E7%A8%8B%E4%B8%8E%20PAC-Bayes.md) · [测度、条件期望、滤过与适应过程](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%B5%8B%E5%BA%A6%E3%80%81%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E3%80%81%E6%BB%A4%E8%BF%87%E4%B8%8E%E9%80%82%E5%BA%94%E8%BF%87%E7%A8%8B.md) · [统计距离、Le Cam、Fano、Assouad 与 Yao 下界](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E7%BB%9F%E8%AE%A1%E8%B7%9D%E7%A6%BB%E3%80%81Le%20Cam%E3%80%81Fano%E3%80%81Assouad%20%E4%B8%8E%20Yao%20%E4%B8%8B%E7%95%8C.md)

## 适用场景

当模型很复杂，但你可以定义：

```text
prior P: 训练前或任务无关分布
posterior Q: 训练后模型、adapter、memory、policy 的分布
```

PAC-Bayes 特别适合 compressed model、posterior over weights、Bayesian-looking algorithm、agent memory、personalization state。

## PAC-Bayes：先写可核验的 kl 形式

设 $n\ge2$、 $\delta\in(0,1)$、 $S=(Z_1,\ldots,Z_n)\sim\mathcal D^n$，损失 $\ell(h,z)\in[0,1]$。令先验 $P$ 独立于 $S$，后验 $Q=Q(S)$ 可以依赖 $S$ 且 $Q\ll P$，并定义 Gibbs risks

$$
\widehat L_S(Q)=\mathbb E_{h\sim Q}\frac1n\sum_{i=1}^n\ell(h,Z_i),
\qquad
L_{\mathcal D}(Q)=\mathbb E_{h\sim Q,Z\sim\mathcal D}\ell(h,Z).
$$

这里固定使用 Alquier 的 [2110.11216v6](https://arxiv.org/abs/2110.11216v6)，PDF 物理第 44 页 Theorem 3.2（其中引 Maurer 2004, Theorem 5），TeX `MAL-100.tex` 的 `thm:see:bound`。其 [本地核验定位](../../proof_ref/foundations-2026-09/user-friendly-introduction-to-pac-bayes-bounds-2110.11216/核验笔记.md) 记录工件 hash 与检查范围。该 PAC-Bayes-kl 版本是：以至少 $1-\delta$ 的概率，**同时对所有** $Q$，

$$
\operatorname{kl}\!\left(\widehat L_S(Q)\,\middle\|\,L_{\mathcal D}(Q)\right)
\le
\frac{\operatorname{KL}(Q\|P)+\log(2\sqrt n/\delta)}{n}.
$$

这里左侧是 Bernoulli KL。由 Pinsker 可得较易读但更松的推论

$$
L_{\mathcal D}(Q)
\le
\widehat L_S(Q)
+\sqrt{\frac{\operatorname{KL}(Q\|P)+\log(2\sqrt n/\delta)}{2n}}.
$$

不同 PAC-Bayes 定理的常数、温度、经验风险变换与允许的数据依赖先验并不相同；引用时必须锁定具体版本。

<a id="t05-pac-bayes-kl"></a>

^t05-pac-bayes-kl

## 信息论泛化：通常先是期望界

设 $S\sim\mathcal D^n$，相关风险与期望有限。若对每个固定 $w$，中心化损失 $\ell(w,Z)-\mathbb E\ell(w,Z)$ 在 $Z\sim\mathcal D$ 下以同一常数 $\sigma>0$ 满足 sub-Gaussian 矩界，则对任意随机学习算法输出 $W$，

$$
\left|\mathbb E_{S,W}\left[L_{\mathcal D}(W)-\widehat L_S(W)\right]\right|
\le
\sqrt{\frac{2\sigma^2 I(W;S)}{n}}.
$$

这是对样本和算法随机性的**期望**泛化界，不会自动给出高概率结论。更换为 binary Jensen--Shannon divergence、conditional mutual information 或其他 $f$-divergence 时，必须重新引用相应定理及其 learner symmetry、损失范围等条件。

固定来源为 Xu–Raginsky 的 [1705.07809v2](https://arxiv.org/abs/1705.07809v2)，PDF 第 4 页 Theorem 1 / Eq. (10)，TeX `nips_2017_arXiv.tex` 的 `th:gen_err_mi`。下面给出自包含证明；[本地核验笔记](../../proof_ref/foundations-2026-09/information-theoretic-analysis-of-generalization-capability-of-learning-1705.07809/核验笔记.md) 记录为什么混合不同 $w$ 时必须先按 $w$ 中心化。

### 完整推导：先减去每个模型自己的总体均值

直觉是先把不同模型的“基础难度”扣掉，只衡量每个模型在这次样本上偏离自己总体均值多少。定义

$$
G(s,w)=L_{\mathcal D}(w)-\widehat L_s(w),\qquad
\mu=P_{S,W},\quad \nu=P_S\otimes P_W.
$$

在参考分布 $\nu$ 中，样本与输出独立。固定任意 $w$，样本独立性及逐 $w$ 的中心化矩界给出，对所有 $\lambda\in\mathbb R$，

$$
\mathbb E_S e^{\lambda G(S,w)}
=\prod_{i=1}^n\mathbb E_{Z_i}
 e^{(\lambda/n)(L_{\mathcal D}(w)-\ell(w,Z_i))}
\le e^{\lambda^2\sigma^2/(2n)}.
$$

右侧与 $w$ 无关，所以对 $P_W$ 积分仍有
$\mathbb E_\nu e^{\lambda G}\le e^{\lambda^2\sigma^2/(2n)}$。这个步骤允许不同 $w$ 有不同的 $L_{\mathcal D}(w)$；直接混合未中心化的损失一般没有同样的矩界。

若 $I(W;S)=\operatorname{KL}(\mu\|\nu)<\infty$，令 $r=d\mu/d\nu$。Jensen 给出换测度不等式：

$$
\mathbb E_\mu f-\operatorname{KL}(\mu\|\nu)
=\mathbb E_\mu\log\frac{e^f}{r}
\le\log\mathbb E_\mu\frac{e^f}{r}
\le\log\mathbb E_\nu e^f.
$$

这里在 $r>0$ 上计算，最后一个不等式是补上 $\nu$ 在其余部分的非负积分；可积性不足时先截断再取极限。分别取 $f=\lambda G$ 和 $f=-\lambda G$，对任何 $\lambda>0$ 得到

$$
|\mathbb E_\mu G|
\le\frac{I(W;S)}{\lambda}+\frac{\lambda\sigma^2}{2n}.
$$

当 $0<I(W;S)<\infty$ 时取 $\lambda=\sqrt{2nI(W;S)/\sigma^2}$，便得到所列平方根界。 $I=0$ 时令 $\lambda\downarrow0$； $I=\infty$ 时该界为空泛上界。证明始终控制 $|\mathbb E G|$，没有把绝对值移入期望。

源文在 Theorem 1 前用一句话从固定 $w$ 时损失的 sub-Gaussian 性转到未逐 $w$ 中心化的混合 empirical risk。该中间推断一般需要额外条件；上面通过 $G$ 补足它，不改变所用定理的结论。这里核对的是这一确切推导，不对整篇论文作错误与否的概括判断。

<a id="t05-mi-bound"></a>

^t05-mi-bound

## 逐步证明模板：PAC-Bayes

```text
Step 1. 明确 i.i.d. 样本、[0,1] 损失，以及独立于当前训练样本的 prior P。
Step 2. 定义 posterior Q，允许依赖训练样本。
Step 3. 对固定 hypothesis h 写指数矩或 Bernoulli-kl concentration bound。
Step 4. 用 change-of-measure inequality 从 P 转到 Q。
Step 5. 得到在同一 good event 上对所有 Q 同时成立的 bound。
Step 6. 只有在具体模型建立了编码/压缩对应后，才把 KL(Q||P) 解释为复杂度或 compression cost。
```

## 逐步证明模板：information-theoretic

```text
Step 1. 把 generalization gap 写成 train/test loss 的差。
Step 2. 将算法输出 W 与样本 S 的依赖量化为 I(W;S) 或 f-divergence。
Step 3. 检查 fixed-w loss 的 sub-Gaussian 或其他矩条件，再用 variational representation / transport inequality 控制期望 gap。
Step 4. 在具体算法中上界 I(W;S)。
Step 5. 若需要 high-probability bound，另选相应定理，不能把期望界直接加上 delta。
```

## 可迁移用法

可以把 $\operatorname{KL}(Q_{\text{personalized}}\|P_{\text{base}})$ **定义为某种建模代理量**，讨论 personalization 与复杂度的 trade-off；但“memory strength 等于 KL”不是 PAC-Bayes 定理，必须另行定义并验证它与实际 memory 行为的关系。

## 常见坑

- PAC-Bayes bound 很容易松；需要结构化 prior/posterior。
- 标准 data-independent prior 不能偷看 test data，也不能依赖当前训练样本；若用 data-dependent prior，必须引用专门版本并支付额外复杂度。
- 不能把 PAC-Bayes 硬塞进本来只是 empirical method 的论文。
- PAC-Bayes 的 $Q$ 是 Gibbs predictor 的分布；若最终使用一个确定性网络，需要说明取样、反随机化或单模型证书如何完成。
- MI 期望界、PAC-Bayes 高概率界与 binary-JS 的等式刻画是三种不同结论，不能合并成一个“信息复杂度定理”。

## 来源论文 / 参考

- Compositional PAC-Bayes: Generalization of GNNs with persistence and beyond, NeurIPS 2024. https://proceedings.neurips.cc/paper_files/paper/2024/hash/c3266c14d7eb9715d9fad4306133aa4e-Abstract-Conference.html
- Exactly Tight Information-theoretic Generalization Bounds via Binary Jensen-Shannon Divergence, ICML 2025. https://proceedings.mlr.press/v267/dong25e.html
- 本地 PAC-Bayes + compression 核验：[核验笔记](../../proof_ref/recent-accepted-2025-2026/generalization-bounds-via-meta-learned-model-representations-pac-2410.13577/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md) · [PDF](../../proof_ref/recent-accepted-2025-2026/generalization-bounds-via-meta-learned-model-representations-pac-2410.13577/paper.pdf#page=5)
- 本地 information-theoretic/generalization 可证性核验：[核验笔记](../../proof_ref/core-theory-2026-09/which-algorithms-have-tight-generalization-bounds-2410.01969/%E6%A0%B8%E9%AA%8C%E7%AC%94%E8%AE%B0.md) · [PDF](../../proof_ref/core-theory-2026-09/which-algorithms-have-tight-generalization-bounds-2410.01969/paper.pdf#page=5)

## 关联模板与本地证据

- [T04：耦合相邻训练集的算法轨迹，控制期望泛化差。](T04-stability.md)
- [T12：由困难实例的不可区分性推出指定算法类的风险下界。](../lower-bounds-expressivity/T12-information-lower-bounds.md)

通用证明工具：P01、P05、P09；见 [证明原语](../../通用证明原语.md)。

- [User-friendly introduction to PAC-Bayes bounds](../../proof_ref/foundations-2026-09/user-friendly-introduction-to-pac-bayes-bounds-2110.11216/README.md) · [官方 arXiv](https://arxiv.org/abs/2110.11216)
- [Information-theoretic analysis of generalization capability of learning algorithms](../../proof_ref/foundations-2026-09/information-theoretic-analysis-of-generalization-capability-of-learning-1705.07809/README.md) · [官方 arXiv](https://arxiv.org/abs/1705.07809)
- [Generalization Bounds via Meta-Learned Model Representations: PAC-Bayes and Sample Compression Hypernetworks](../../proof_ref/recent-accepted-2025-2026/generalization-bounds-via-meta-learned-model-representations-pac-2410.13577/README.md) · [官方 arXiv](https://arxiv.org/abs/2410.13577)

## 专项证明接口（2026-10-02）

- [T46：显式计算 Gaussian RDP、条件组合和 DP 转换，区分裁剪对象与采样。](../statistics/T46-gaussian-privacy-accounting.md)
