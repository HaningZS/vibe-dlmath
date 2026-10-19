---
id: T42
type: proof-template
refined: 2026-10-02
status: self-contained-core
---

# T42. 有限网络的核变化、参数移动与训练动力学

[主题目录](README.md) · [NTK T09](T09-ntk.md) · [Mean-field T10](T10-mean-field.md)

## 复用契约

**对象**：固定 $n$ 个训练样本，预测向量 $f_\theta\in\mathbb R^n$，残差 $r=f_\theta-y$；损失 $\mathcal L=\|r\|^2/(2n)$，Euclidean gradient flow $\dot\theta=-\nabla_\theta\mathcal L$。

**条件**：轨迹存在，预测沿轨迹可微，Jacobian 连续且相关积分有限。离散 GD、Adam 和非光滑参数切换需另外证明。

**结论**：精确时变核方程及其条件性收敛/漂移界；不能由“核变了”直接推得表示更适合下游任务。

**失败例子**：特征整体放大可改变核尺度，却保持全部相对方向。仅看 $\|K_t-K_0\|$ 无法排除这种情况。

## 实例化时必须完成

- [ ] 核中 $1/n$ 与 loss 的 sum/mean normalization 一致。
- [ ] 给出谱下界/轨迹区域/核 Lipschitz 界的来源，避免相互循环。
- [ ] 声称特征学习收益时，额外控制任务对齐、泛化或结构变化。
- [ ] 写清连续时间与实际离散算法的误差。

## 1. 直觉：训练不仅推动球，也会改变坡面

固定 NTK 近似把训练看成在一张基本不变的坡面上移动。有限网络的 Jacobian 可以改变，因而“参数改变一点，输出改变多少”也会改变。本卡先追踪这个精确事实，再问什么时候可用固定坡面近似。

## 2. 不取无限宽，先写精确方程

令 $J_t=\partial f_\theta/\partial\theta$，定义 $K_t=J_tJ_t^\top/n$。链式法则给出

$$
\dot\theta_t=-J_t^\top r_t/n,\qquad
\dot r_t=-K_tr_t,\qquad
\dot{\mathcal L}_t=-r_t^\top K_tr_t/n.
$$

若在 $[0,T]$ 上已证明 $K_t\succeq\mu I$，则
$\dot{\mathcal L}\le-2\mu\mathcal L$，从而
$\mathcal L_t\le e^{-2\mu t}\mathcal L_0$。正半定只能说明 loss 不增；需要正谱下界才能得到此指数速率。

## 3. 参数移动和核稳定怎样检查

又有 $\dot{\mathcal L}=-\|\dot\theta\|^2$，故

$$
\|\theta_t-\theta_0\|\le\int_0^t\|\dot\theta_s\|ds
\le\sqrt{t(\mathcal L_0-\mathcal L_t)}.
$$

若在该区域 $\|J_\theta\|_{op}\le B_J$、$\|J_\theta-J_{\theta_0}\|_{op}\le L_J\|\theta-\theta_0\|$，则

$$
\|K_t-K_0\|_{op}
\le\frac{2B_JL_J}{n}\|\theta_t-\theta_0\|.
$$

证明通常先设一个可验证的局部区域，在区域内得到这些界，再用移动界证明轨迹不退出。只有条件性谱下界却不关闭区域，就是未完成的 [T09](T09-ntk.md) 证明。

## 4. 与固定核近似比较

令 $\bar r_t=e^{-K_0t}r_0$，$E_t=K_t-K_0$。Duhamel 给出

$$
r_t-\bar r_t=-\int_0^t e^{-K_0(t-s)}E_sr_sds.
$$

若 $K_0\succeq0$，指数算子范数不超过 1；时变核也正半定，所以 $\|r_s\|\le\|r_0\|$。因此

$$
\|r_t-\bar r_t\|\le\|r_0\|\int_0^t\|E_s\|ds.
$$

固定核近似的误差看的是累计漂移，某个时刻的漂移小还不够保证长期近似。

## 5. 一个完全可解的有限参数例子

单样本模型 $f(u,v)=uv$、目标 1、初值 $u_0=v_0=a_0\in(0,1)$。对称性使 $u_t=v_t=a_t$，且
$\dot a=a(1-a^2)$。令 $b=a^2$，得到

$$
b_t=\frac1{1+(b_0^{-1}-1)e^{-2t}},\qquad K_t=u_t^2+v_t^2=2b_t.
$$

核随时间变化，残差满足 $\dot r=-K_tr$，并因 $K_t\ge2b_0$ 收敛。这展示有限网络与冻结核的差别；这里只有尺度变化，不能据此宣称学到了更丰富的特征方向或测试泛化。

## 前置、关联与证据

- [Jacobian](<../../Math 基础/微积分与分析/导数、梯度、Jacobian、Hessian 与自动微分.md>) · [Duhamel/Grönwall](<../../Math 基础/微积分与分析/Grönwall、Duhamel 与稳定性误差传播.md>)。
- [T09](T09-ntk.md) · [T10](T10-mean-field.md) · [T36 隐式偏置](T36-implicit-bias.md) · [T32](../generalization/T32-excess-risk-decomposition.md)。
- [Lazy training 原论文](https://arxiv.org/abs/1812.07956) · [本地卡](../../proof_ref/foundations-2026-09/on-lazy-training-in-differentiable-programming-1812.07956/README.md)。本卡先给精确恒等式，不把特定宽度极限条件推广到所有网络。
