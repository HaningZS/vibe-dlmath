# 优化与随机估计

[全部模板](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)

| 编号 | 适用目标 | 类型 |
|---|---|---|
| [T01](T01-descent.md) | 把单步目标下降累积成平均梯度平方界。 | 证明模板 |
| [T02](T02-lyapunov.md) | 给辅助状态误差记账，让联合势函数下降。 | 证明模板 |
| [T03](T03-variance-reduction.md) | 用同一随机样本的梯度差，把估计误差绑定到移动路径。 | 证明模板 |
| [T15](T15-generalized-smoothness.md) | 曲率随梯度变化时，先证明局部下降和轨迹闭合。 | 证明模板 |
| [T16](T16-heavy-tail-clipping.md) | 把裁剪梯度分成 centered martingale 与 clipping bias。 | 证明模板 |
| [T39](T39-proximal-nonsmooth.md) | 识别 smooth-plus-convex 结构，用 gradient mapping 处理复合目标。 | 证明模板 |
| [T40](T40-second-order-stationarity.md) | 用负曲率下降补一阶驻点，并显式区分 Hessian oracle 与一阶逃逸复杂度。 | 证明模板 |
| [T47](T47-local-training-client-drift.md) | 分解 local training 的位置偏差并控制客户端分歧、通信与输出。 | 证明模板 |
