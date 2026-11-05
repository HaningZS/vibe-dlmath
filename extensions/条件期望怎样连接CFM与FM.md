# 条件期望怎样连接 CFM 与 FM

[返回专题目录](README.md) · [原证明模板](../proofs/README.md)

前置：[条件期望](<../Math 基础/概率统计/测度、条件期望、滤过与适应过程.md>)、[ODE/SDE](<../Math 基础/微积分与分析/ODE、SDE 与连续时间生成模型.md>)、[最优传输](<../Math 基础/概率统计/最优传输与 Wasserstein 距离.md>)。

## 1. 同一路口，为什么会有不同训练箭头

训练时可以采样一对端点 $(X_0,X_1)$，用路径把它们连起来。例如

$$
X_t=(1-t)X_0+tX_1,\qquad U_t=X_1-X_0.
$$

每一对端点都有自己的速度标签 $U_t$。但部署模型 $v_\theta(x,t)$ 只看到当前位置和时间，看不到采样端点的“身份证”。

所以两对端点若在同一时空位置给出不同箭头，模型必须在它们之间做统计汇总。平方回归的最优汇总就是条件平均。

## 2. 先固定概率空间与目标

令 $T$ 是训练时间， $(X_T,U_T)$ 由选定 coupling 与条件路径产生。假设速度二阶矩有限，且所有训练分布不依赖参数 $\theta$。

定义

$$
\bar u(x,t)=\mathbb E[U_T\mid X_T=x,T=t].
$$

Conditional Flow Matching 的目标是

$$
L_{\mathrm{CFM}}(\theta)
=\mathbb E\Vert v_\theta(X_T,T)-U_T\Vert^2.
$$

理想 marginal Flow Matching 目标为

$$
L_{\mathrm{FM}}(\theta)
=\mathbb E\Vert v_\theta(X_T,T)-\bar u(X_T,T)\Vert^2.
$$

这里的 $\bar u$ 是总体条件期望，不是“把 minibatch 所有速度随意平均”。

## 3. 关键证明只有一个正交交叉项

把误差拆成两段：

$$
v_\theta-U_T=(v_\theta-\bar u)+(\bar u-U_T).
$$

展开平方并取期望，唯一需要解释的是交叉项：

$$
\mathbb E\langle v_\theta-\bar u,\bar u-U_T\rangle.
$$

条件于 $(X_T,T)$ 后，第一因子已经确定，而

$$
\mathbb E[\bar u-U_T\mid X_T,T]=0.
$$

因此交叉项为零，得到

$$
L_{\mathrm{CFM}}(\theta)
=L_{\mathrm{FM}}(\theta)
+\underbrace{\mathbb E\Vert U_T-\bar u(X_T,T)\Vert^2}_{C}.
$$

$C$ 是看不到端点身份造成的剩余不确定性，不依赖网络参数。只要可合法交换微分与期望，

$$
\nabla_\theta L_{\mathrm{CFM}}=\nabla_\theta L_{\mathrm{FM}}.
$$

这说明总体梯度相同，而不是每个样本的速度标签相同，也不保证两个 minibatch 梯度恰好一致。

## 4. 条件平均为什么能移动整片概率云

对一个光滑且适当可积的测试函数 $\varphi$，条件路径满足 $\dot X_t=U_t$ 时，

$$
\frac{d}{dt}\mathbb E[\varphi(X_t)]
=\mathbb E[\nabla\varphi(X_t)^\top U_t]
=\mathbb E[\nabla\varphi(X_t)^\top \bar u(X_t,t)].
$$

第二步用了全期望。若进一步有密度、可交换微分与积分、合适边界条件，这个弱形式对应

$$
\partial_t p_t+\nabla\cdot(p_t\bar u_t)=0.
$$

因此条件平均场与所选概率路径具有一致的分布输运关系。要把它提升为唯一 ODE flow 的结论，还需向量场/连续性方程的存在唯一性等正则条件。

## 5. 这个结论没有保证什么

- 条件路径是直线，不代表边缘 ODE 轨迹也直。
- 学到总体最优场，不等于有限数据与有限容量训练已经到达最优。
- 改变 coupling 会改变条件方差和学习难度，尽管端点 marginal 可以不变。
- 如果路径或 coupling 自身含可训练参数， $C$ 对这些参数未必是常数。
- 高阶 solver 只能减少给定场的积分误差，不能自动修复 field fitting error。

## 6. 一个离散的数值检查

~~~python
# 同一位置 x=0，训练标签可以是 -1 或 +3；其他位置只有一种标签。
xs = [0, 0, 1, 1]
us = [-1.0, 3.0, 2.0, 2.0]
means = {0: 1.0, 1: 2.0}

def losses(theta):
    predictions = [theta * x for x in xs]
    cfm = sum((v - u)**2 for v, u in zip(predictions, us)) / len(xs)
    fm = sum((v - means[x])**2 for v, x in zip(predictions, xs)) / len(xs)
    return cfm, fm

for theta in [-2.0, 0.0, 1.0, 4.0]:
    cfm, fm = losses(theta)
    assert abs((cfm - fm) - 2.0) < 1e-12
    print(theta, cfm, fm, "常数差", cfm - fm)
~~~

即使换参数，两种目标之差都保持 2。这个剩余项来自 $x=0$ 处无法仅靠位置确定端点标签。

自测：如果目标分布随着 $\theta$ 改变，是否仍可直接写梯度相同？不能；必须把分布与 $C$ 的参数依赖一起求导。

## 论文

- Lipman et al.：[Flow Matching for Generative Modeling](https://arxiv.org/abs/2210.02747)；
- Liu et al.：[Rectified Flow](https://arxiv.org/abs/2209.03003)。

本地阅读卡见 [generative 论文目录](../PAPERS.md#generative)。
