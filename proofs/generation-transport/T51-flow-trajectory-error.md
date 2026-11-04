---
id: T51
type: proof-template
refined: 2026-10-20
status: self-contained-core
---

# T51. Flow Matching：速度误差怎样变成分布误差

[主题目录](README.md) · [采样误差 T13](T13-sampler-error.md) · [CFM 条件期望](../../extensions/条件期望怎样连接CFM与FM.md)

## 复用契约

**对象**：给定训练数据后，固定真实场 $v_t$ 与学习场 $u_t$。用共同初值 $X_0=Y_0$ 耦合 $\dot X_t=v_t(X_t)$、 $\dot Y_t=u_t(Y_t)$，真实边缘 law 为 $\rho_t$，学习流 law 为 $\widehat\rho_t$。

**假设**：区间 $[0,T]$ 上两条 ODE 适定；初值有有限二阶矩；学习场的空间 Lipschitz 常数 $\gamma(t)\ge0$ 可积； $e(t)=\mathbb E_{X\sim\rho_t}\|u_t(X)-v_t(X)\|^2$ 可积。需要足够增长/可积条件使二阶矩及其求导合法；例如两场有可积的线性增长控制且对应乘积可积。

**输出**：
$$W_2^2(\widehat\rho_T,\rho_T)
\le\int_0^T\exp\!\left((T-s)+2\int_s^T\gamma(r)dr\right)e(s)ds.$$

**失败例子**：训练误差在 $\rho_t$ 下，而证明改在 $\widehat\rho_t$ 下积分，二者未必接近；对真实场的 Lipschitz 界也不能直接替换此推导所需的学习场界。

## 实例化时必须完成

- [ ] 证明真实 ODE 的边缘确实是所写的 $\rho_t$；检查时间端点与适定性。
- [ ] 核对误差 law、同起点耦合、学习场空间约束和训练事件。
- [ ] 将 population regression error 与有限样本/优化误差合法连接。
- [ ] 离散 solver、初始分布差异和目标平滑分别补相应项。

## 1. 直觉：船的方向误差会累积，也会被水流放大

速度预测误差像船每时刻偏航；Lipschitz 常数描述偏离一点后，速度又可能改变多少。两者共同决定最后的位置差，不能只看平均回归误差。

把两艘船从同一位置出发，是为了让最后的差异有可比较的来源。这个人为配对就是 coupling；它给出 Wasserstein 的一个可用运输方案。

## 2. 先分清两种概率

训练数据决定 $u_t$，先对它条件化。以下期望只对共同初值取；训练阶段的高概率事件在最后合并。若 $\gamma$ 也随训练变化，必须在相应事件内控制，才能声称一个统一 rate。

令 $R_t=\mathbb E\|Y_t-X_t\|^2$。由于这是一种 coupling， $W_2^2(\widehat\rho_t,\rho_t)\le R_t$。

## 3. 加减哪一项，决定误差在哪个 law 下

写 $D_t=Y_t-X_t$，加减 $u_t(X_t)$：
$$R_t'=2\mathbb E\langle D_t,u_t(Y_t)-u_t(X_t)\rangle
+2\mathbb E\langle D_t,u_t(X_t)-v_t(X_t)\rangle.$$
第一项用**学习场**的 Lipschitz 条件，至多 $2\gamma(t)R_t$；第二项用 $2\langle a,b\rangle\le\|a\|^2+\|b\|^2$，至多 $R_t+e(t)$。因此
$$R_t'\le(1+2\gamma(t))R_t+e(t),\qquad R_0=0.$$

这里误差恰好在真实 $X_t\sim\rho_t$ 下，所以能接训练时的 population regression error。若改为加减 $v_t(Y_t)$，就会得到另一套假设和误差 law，必须重新核对。

## 4. 积分因子给出完整结论

乘 $\exp[-\int_0^t(1+2\gamma(r))dr]$ 并积分，得到契约中的加权误差界。对 $T=1$，进一步放松为
$$W_2^2(\widehat\rho_1,\rho_1)
\le e^{1+2\|\gamma\|_{L^1(0,1)}}\int_0^1e(t)dt.$$
若初值不完全相同，同一计算还会留下 $e^{T+2\int_0^T\gamma}R_0$；不能省掉初始化误差。

在 $v=0,u=c$、同一确定初值的简单例子中，真实终点平方误差为 $\|c\|^2T^2$，上式的 $T e^T\|c\|^2$ 是合法但较松的界。这有助于理解该推导没有承诺最紧常数。

删除学习场正则性/唯一性的具体反例： $v=0$、 $u(x)=2\sqrt{|x|}$，共同初值为 0。真实轨迹恒为 0，故真实路径上的 $e(t)=0$；学习 ODE 却同时允许 $Y_t=0$ 和 $Y_t=t^2$。选后者就有正误差。此例违反本卡的 Lipschitz/适定性条件，说明这两项不能从回归误差很小自动推出。

## 5. 接训练统计率与离散采样

有限训练集的经验 FM loss 不能直接代入 $\int e$：先用 [CFM 条件期望](../../extensions/条件期望怎样连接CFM与FM.md) 确认目标，再用 [T32](../generalization/T32-excess-risk-decomposition.md)/[T33](../generalization/T33-uniform-convergence.md) 分析模型、统计与优化误差。

Euler 等数值方案另需时间正则性等条件。应先证明 $W_2(\rho_T^{num},\widehat\rho_T)$，再用同一种距离的三角不等式； $W_2^2$ 直接相加会漏交叉项或常数。

若训练目标 $\rho_T$ 本身带噪声，当前定理恢复的是带噪声目标。去噪或 $\sigma\to0$ 的极限还需目标差异与常数控制。

## 经典来源与近期证据

- [Grönwall 前置](<../../Math 基础/微积分与分析/Grönwall、Duhamel 与稳定性误差传播.md>) · [Wasserstein 前置](<../../Math 基础/概率统计/最优传输与 Wasserstein 距离.md>) · [T19](T19-transport-risk.md)。
- [Flow Matching under Noisy Latent Structure v1](https://arxiv.org/abs/2609.38918v1) 的 Theorem 5.2 使用此 coupling/Young/Grönwall 路线。它的完整统计率还要求特定 latent-noise 模型、受约束 ERM 和精确时间/辅助噪声积分；没有证明普通 SGD 已达到该 ERM。
- [本地 PDF、源码与核验范围](../../proof_ref/proof-distillation-2026-10/flow-matching-under-noisy-latent-structure-beyond-exact-2609.38918/核验笔记.md)。本卡重推连续流基础桥，不把 66 页逼近和统计证明全部标为已复核。
