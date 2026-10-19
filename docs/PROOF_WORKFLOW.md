# 怎样选择、组合和复用证明模板

[首页](../README.md) · [模板目录](../proofs/README.md) · [Skill](SKILL.md)

如果先要判断一篇 DL 工作需要哪些理论环节，读 [DL 总框架](DL_THEORY_FRAMEWORK.md)；准备写成论文时，用 [论文级审查](THEORY_REVIEW.md) 和 [定理工作档案](../templates/THEOREM_DOSSIER.md) 管理主张、假设与依赖。

想看一份实际闭合的合成证明，读 [随机特征 → projected GD → 测试风险](END_TO_END_LEARNING_PROOF.md)。其中比较解存在、算法可执行、全类泛化与输出规则都逐项证明。

由 AI 生成或审查证明时使用 [AI 证明合同](AI_PROOF_CONTRACT.md)。从论文提取新卡时按 [蒸馏流程](PROOF_DISTILLATION.md) 保存固定来源、关键推导、反例和迁移义务。

## 1. 先写问题合同

证明开始前，用一小段话固定五件事：

1. **对象**：算法更新、数据 law、随机性、维度与资源。
2. **目标量**：梯度范数、风险、regret、覆盖率、分布距离或表达能力。
3. **量词**：期望、高概率、全部时刻、所有后验、存在权重还是所有模型。
4. **条件**：独立性、smoothness、支持、coverage、范数或精度。
5. **适用范围**：常数依赖、时间/宽度/样本极限以及输出规则。

这五项没有固定时，可以给条件性的分析路线，但不能把缺少的假设悄悄加进去。

## 2. 模板有不同类型

| 类型 | 可以怎样使用 | 不能自动声称 |
|---|---|---|
| proof-template | 检查契约后重新实例化证明 | 新问题已被原文定理覆盖 |
| method-card | 复现某篇论文的问题与关键 lemma | 适用于所有 agent/LLM 的普适保证 |
| project-tool | 说明经验代数或协议关系 | 显著性、因果机制或总体改进 |
| router | 选择具体证明分支 | 路由页本身是一个定理 |

T17/T25 是方法卡，T24 是项目代数，T20 是路由页。它们不会因为与其他模板放在同一目录就变成统一理论工具。

## 3. 按问题查，再逐张确认

~~~bash
python3 scripts/proof_templates.py search "重尾 随机梯度 momentum"
python3 scripts/proof_templates.py show T16
python3 scripts/proof_templates.py list --topic generalization
~~~

检索结果只是候选。每张卡先读“复用契约”和“实例化时必须完成”，确认后才读推导与原文。P01–P10 的通用工具仍在 [证明原语](../通用证明原语.md) 中集中维护，避免把同一不等式复制成多个版本。

## 4. 组合的是接口，不是论文名字

组合两条 lemma 前检查：

- 使用同一个概率空间、filtration 和样本划分吗？
- 前一条输出的范数、距离和误差类型，满足后一条的输入吗？
- 系数和步长约束能同时满足吗？
- 两个高概率事件的失败预算如何组合？
- 是否在循环使用一个尚未证明的梯度/轨迹界？

例如，不能把 T03 的 SPIDER estimator 当成逐步条件无偏，直接接 T01 的无偏 SGD 推论。需要把 estimator error 保留下来，再与下降式联立。

## 5. 一个完整的组合接口：下降与状态误差

设 $G_t,E_t\geq0$ 在 $\mathcal F_t$ 上可测，已分别证明

$$
\mathbb E[A_{t+1}\mid\mathcal F_t]
\leq A_t-aG_t+bE_t+c_t,
$$

$$
\mathbb E[E_{t+1}\mid\mathcal F_t]
\leq(1-\kappa)E_t+dG_t+r_t,
$$

其中 $a,\kappa>0$，$b,d\geq0$，所有期望存在，残差可积。令
$\Phi_t=A_t+\lambda E_t$，则

$$
\mathbb E[\Phi_{t+1}\mid\mathcal F_t]
\leq\Phi_t-(a-\lambda d)G_t
+(b-\lambda\kappa)E_t+c_t+\lambda r_t.
$$

要吸收状态误差且保留进展，就需要
$\lambda\geq b/\kappa$ 且 $a-\lambda d>0$。
当 $d>0$ 时，可行性的关键是 $bd<a\kappa$；$d=0$ 时只需 $a>0$ 与下界条件。

若此外 $\Phi_T\geq\Phi_{\inf}$，则

$$
\frac1T\sum_{t<T}\mathbb E G_t
\leq
\frac{\mathbb E\Phi_0-\Phi_{\inf}
+\sum_{t<T}\mathbb E[c_t+\lambda r_t]}
{(a-\lambda d)T}.
$$

这段组合是可复用的，但 $a,b,\kappa,d,c_t,r_t$ 必须来自真实算法。知道噪声重尾、模型含 momentum，不足以凭空得到它们。

对应：[T02 Lyapunov](../proofs/optimization/T02-lyapunov.md)、[T03 估计误差](../proofs/optimization/T03-variance-reduction.md)、[T16 裁剪](../proofs/optimization/T16-heavy-tail-clipping.md)。

## 6. 证据分三级记录

- **代数/结构检查**：当前推导中的定义、等式、常数和量词是否一致。
- **原文核验**：固定版本的 theorem/lemma、全部假设、页码/TeX 是否对应。
- **新问题证明**：原文的条件在当前算法和数据中是否满足，新增步骤是否闭合。

下载成功只验证工件；数值示例只验证具体实例；检索命中只验证文字相关性。三者都不能自动升级为逐式证明完成。

## 7. 用工作单记录未完成义务

~~~bash
python3 scripts/proof_templates.py scaffold T02 T16 \
  --problem "分析带动量和裁剪的随机优化器" \
  --out /tmp/optimizer-proof.md
~~~

这个命令只生成明确标为“未完成证明”的工作单，保留假设、反例与原文入口；不会覆盖现有文件。若用户只要求解释或 review，skill 可以在回复中报告候选与缺口，无需创建文件。

可直接复制的结构是：问题合同 → lemma 依赖 → 各步证明义务 → 证据定位 → 尚未关闭的缺口 → 条件性或完整结论。最终写成论文时再使用 [证明笔记模板](../templates/PROOF_NOTE.md)，不把空白工作单当成完成的理论部分。
