---
id: T10
type: proof-template
refined: 2026-09-28
status: "bounded-scope"
---

# T10. Mean-field / propagation of chaos

[主题目录](README.md) · [模板总目录](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

分开控制极限动力学优化误差与有限粒子近似误差。

## 复用契约

**输入对象**：经验测度 ρ_t^m、极限 ρ_t、风险泛函、宽度/时间/步长 scaling。

**输出结论**：有限宽风险误差的分解；全局收敛与维度/时间 rate 需分别证明。

**必需假设**：

- 极限动力学适定，矩条件与 coupling 合法。
- 风险对分布距离有足够连续性。
- 有限时间粒子极限与无限时间优化不能自动交换。

**失败例子**：e^(Ct)/sqrt(m) 的有限时间误差不提供任意长时间的统一保证。

## 实例化时必须完成

- [ ] 固定参数化和极限对象。
- [ ] 分别证明优化与逼近。
- [ ] 保留时间依赖及离散化项。

**核验口径**：本轮统一检查使用条件与结论范围；原论文逐式核验等级沿用对应核验卡。模板在新问题中必须重新实例化，数值示例也不替代证明。

> [!warning] 方向专修
> 前置可从 [测度、条件期望、滤过与适应过程](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%B5%8B%E5%BA%A6%E3%80%81%E6%9D%A1%E4%BB%B6%E6%9C%9F%E6%9C%9B%E3%80%81%E6%BB%A4%E8%BF%87%E4%B8%8E%E9%80%82%E5%BA%94%E8%BF%87%E7%A8%8B.md)、[Grönwall、Duhamel 与稳定性误差传播](../../Math%20%E5%9F%BA%E7%A1%80/%E5%BE%AE%E7%A7%AF%E5%88%86%E4%B8%8E%E5%88%86%E6%9E%90/Gr%C3%B6nwall%E3%80%81Duhamel%20%E4%B8%8E%E7%A8%B3%E5%AE%9A%E6%80%A7%E8%AF%AF%E5%B7%AE%E4%BC%A0%E6%92%AD.md)、[最优传输与 Wasserstein 距离](../../Math%20%E5%9F%BA%E7%A1%80/%E6%A6%82%E7%8E%87%E7%BB%9F%E8%AE%A1/%E6%9C%80%E4%BC%98%E4%BC%A0%E8%BE%93%E4%B8%8E%20Wasserstein%20%E8%B7%9D%E7%A6%BB.md) 开始；这些不等于完整掌握 propagation of chaos。

## 适用场景

想解释宽网络的 feature learning，而不只是 NTK lazy regime。常用于两层网络、mean-field neural network、Langevin dynamics、particle approximation。

## 核心表示

把有限宽网络看成粒子经验分布：

$$
\rho_m = \frac{1}{m}\sum_{i=1}^m \delta_{\theta_i}.
$$

网络函数写成：

$$
f_{\rho_m}(x)=\int \sigma(x;\theta)d\rho_m(\theta).
$$

在指定参数化、时间尺度、初始化、正则性与适定性条件下，才可证明 $m\to\infty$ 的训练动态由分布空间上的 PDE / Wasserstein gradient flow 描述。

## 逐步证明模板

```text
Step 1. 把参数集合写成 empirical measure。
Step 2. 定义 infinite-width population risk functional。
Step 3. 推导 measure dynamics，例如 Wasserstein gradient flow / McKean-Vlasov PDE。
Step 4. 证明 infinite-width dynamics 的 risk descent 或 global convergence。
Step 5. 证明 finite particle system 接近 limiting distribution。
Step 6. 用 propagation of chaos / Wasserstein distance 控制近似误差。
Step 7. 合并 optimization error + finite-width approximation error。
```

## 常见 theorem 形状

$$
\mathrm{Risk}(\rho_t^m)-\mathrm{Risk}(\rho^\star)
\le
\left|\mathrm{Risk}(\rho_t^m)-\mathrm{Risk}(\rho_t)\right|
+\left[\mathrm{Risk}(\rho_t)-\mathrm{Risk}(\rho^\star)\right].
$$

第一项才是有限粒子逼近误差，第二项是极限动力学的优化误差。若要用 Wasserstein 控制第一项，还需风险泛函对该距离的连续性。粒子误差一般也依赖 $t$、维度与矩；若算法离散执行，还应增加时间离散项。不能先取无限宽再无条件交换到无限训练时间。

## 常见坑

- 数学门槛比 NTK 高，需要 measure/PDE/Wasserstein 工具。
- 非凸 landscape 在 measure space 可能更好，但有限粒子近似仍需证明。
- propagation of chaos 的维度依赖可能很差。

## 来源论文 / 参考

- A mean field view of the landscape of two-layer neural networks, PNAS 2018. https://www.pnas.org/doi/10.1073/pnas.1806579115
- Mean-field theory of two-layers neural networks: dimension-free bounds and kernel limit, COLT 2019. https://proceedings.mlr.press/v99/mei19a.html

## 关联模板与本地证据

- [T09：闭合初始谱、核稳定、下降与参数移动的联合归纳。](T09-ntk.md)
- [T13：在同一度量中组合连续过程、学习与离散采样误差。](../generation-transport/T13-sampler-error.md)
- [T19：先指定 joint/label 条件，再把 transport cost 连接到风险差。](../generation-transport/T19-transport-risk.md)

通用证明工具：P01、P07；见 [证明原语](../../通用证明原语.md)。

- [A Mean Field View of the Landscape of Two-Layers Neural Networks](../../proof_ref/foundations-2026-09/a-mean-field-view-of-the-landscape-of-1804.06561/README.md) · [官方 arXiv](https://arxiv.org/abs/1804.06561)

## 专项证明接口（2026-10-02）

- [T42：精确跟踪时变核、参数移动与冻结核近似，不把核变化当下游收益。](T42-feature-drift-kernel-dynamics.md)
