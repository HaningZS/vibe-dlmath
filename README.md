<p align="center">
  <img src="assets/readme-hero.svg" alt="vibe-dlmath 封面：标题与标语“Follow the classic proof routes. Every step in the open.”，旁边是一个旋涡星系，两条旋臂是动量法的优化轨迹，沿损失等高线螺旋收敛到最优点 θ*" width="100%">
</p>

<p align="center">
  <strong>让 AI 沿着经典证明路线写证明。</strong><br>
  深度学习理论 · 从经典与近期论文蒸馏的证明路线 · Codex / Claude Code skill
</p>

<p align="center">
  简体中文 · <a href="README.en.md">English</a><br>
  <a href="proofs/README.md">路线目录</a> ·
  <a href="docs/PROOF_DISTILLATION.md">证明蒸馏</a> ·
  <a href="docs/SKILL.md">安装 Skill</a> ·
  <a href="docs/AI_PROOF_CONTRACT.md">AI 证明合同</a> ·
  <a href="Math%20基础/Math%20基础目录.md">数学前置</a>
</p>

---

**vibe-dlmath** 把深度学习理论论文里的证明拆成可复用的路线卡：每张卡写明它解决什么问题、关键步骤、每一步用到的假设，以及换了设定后哪些步骤必须重证。装成 agent skill 后，AI 先为你的问题找到最接近的路线，再沿着它逐步展开；和你的设定对不上的地方，会写成要补的引理、要加的条件，或者一个反例。

**8 个主题 · 47 张模板与工具卡 · 56 篇数学前置 · 101 篇论文条目。** 卡片、说明、清单和检索工具随 Git 提供；论文 PDF/TeX 按需下载。初次使用可以完全离线，无须先下载全部论文。

## Motivation · 为什么做这个库

**很多深度学习研究者有直觉、有实验，却不熟悉证明在这个领域通常怎么写。** 一个收敛界或泛化界该先证哪条引理、哪一步用哪个不等式、假设写到什么程度，这些写法散落在各篇论文里，很难只从结论中学到。

**直接让 AI 从零写，常常得到路线奇怪、不合惯例的证明。** 它会自创分解和记号，默认更强的假设，或者在两个公式之间跳过一段论证。例如“训练梯度趋于零，所以测试风险达到最优”：前者是优化过程的驻点性质，后者还需要泛化和函数类表达能力的论证。这样的证明读起来流畅，审稿人和合作者却很难核对。

**经典论文已经给出被反复检验的路线。** 下降引理加 telescope、ghost sample 对称化、耦合加 Grönwall，这些套路在新问题里一再出现。这个库把它们从经典与近期论文中蒸馏出来，写清每一步依赖什么，让 AI 沿着已有路线展开，而不是另起炉灶；偏离路线的地方必须明说。

路线让证明有出处、合惯例，但不保证结论成立。模板不是定理的替代品，skill 约束也不是形式化验证；重要结论仍需要研究者逐步核对。

## 一条路线长什么样

以“重尾噪声下 clipped SGD 的收敛界”为例，库里的路线由两张卡组成：

- [T01](proofs/optimization/T01-descent.md) 是非凸 SGD 分析的经典骨架：smoothness 给出单步下降不等式，取条件期望，对 $t$ 求和 telescope，最后选步长。
- [T16](proofs/optimization/T16-heavy-tail-clipping.md) 说明裁剪后这条骨架要改哪里：裁剪后的梯度 $\widetilde g_t$ 不再无偏，要拆成一个 martingale 差和一个裁剪偏差，分别控制。

$$
\widetilde g_t-\nabla f(x_t)=
\underbrace{\widetilde g_t-\mathbb E[\widetilde g_t\mid\mathcal F_t]}_{m_t}+
\underbrace{\mathbb E[\widetilde g_t\mid\mathcal F_t]-\nabla f(x_t)}_{b_t}
$$

代回 T01 的下降不等式（ $f$ 为 $L$-smooth，步长为 $\eta$，阈值 $\tau_t$ 可预测），得到可以接着 telescope 的一步界：

$$
\mathbb E[f(x_{t+1})\mid\mathcal F_t]
\le f(x_t)-\frac\eta2\Vert\nabla f(x_t)\Vert^2+\frac\eta2\Vert b_t\Vert^2+\frac{L\eta^2\tau_t^2}{2}
$$

> **失败例子**：真实梯度为 0，随机梯度以 0.1 的概率取 9、以 0.9 的概率取 $-1$，均值为零；以阈值 1 裁剪后，均值变成 $-0.8$。裁剪后的梯度不能再当作无偏估计，T01 中“用无偏性消掉一阶噪声项”的那一步必须改写。

卡片也写明路线在哪里停下：上式只是期望意义的中间式。要声称高概率收敛，还要对 $\langle\nabla f(x_t),m_t\rangle$ 用 Freedman 型 martingale 界，并在同一事件上闭合梯度上界与阈值条件。

每张卡都按同一结构组织：复用契约（输入对象、输出结论、必需假设、失败例子）、核心证明骨架、与其他卡的接口、来源论文，以及实例化时必须逐条完成的义务，例如 T16 的：

- [ ] 裁剪可观测完整梯度后重新中心化。
- [ ] 分别界 bias、波动和二阶项。
- [ ] 在同一事件上闭合阈值/梯度条件。

## 先找到你的入口

| 你现在想做什么 | 从这里开始 |
|---|---|
| 为自己的问题找证明路线 | [主题目录](proofs/README.md) → [10 个通用证明工具](通用证明原语.md) → [组合与实例化](docs/PROOF_WORKFLOW.md) |
| 让 AI 沿路线推导，并检查缺失假设与逻辑跳步 | [安装 Skill](docs/SKILL.md) → [AI 证明合同](docs/AI_PROOF_CONTRACT.md) → [论文级审查](docs/THEORY_REVIEW.md) |
| 判断一个 DL 结论需要哪些理论环节 | [理论框架与覆盖边界](docs/DL_THEORY_FRAMEWORK.md) → [从随机特征到测试风险的完整证明](docs/END_TO_END_LEARNING_PROOF.md) |
| 从经典或新论文蒸馏新路线 | [证明蒸馏流程](docs/PROOF_DISTILLATION.md) → [2026 年 10 月研究整理](docs/RECENT_RESEARCH_2026_10.md) → [论文总目录](PAPERS.md) |
| 补基础，看懂符号与直觉 | [AI Researcher 数学学习路线](Math%20基础/AI%20Researcher%20数学学习路线.md) → [证明前置路线](Math%20基础/证明工具/AI%20理论证明前置学习路线.md) |
| 查看发布内容与后续变化 | [初始发布与版本说明](CHANGELOG.md) |

## 快速开始：找到一条路线，让 AI 沿着它写

先取得完整仓库：

```bash
git clone https://github.com/HaningZS/vibe-dlmath.git
cd vibe-dlmath
python3 --version
```

确认解释器为 **Python 3.11+**；如果系统 `python3` 仍为旧版，改用已安装的 `python3.11`（或更新版本），后续所有命令使用同一个解释器。可选运行 `python3 -m venv .venv` 和 `source .venv/bin/activate` 来隔离环境；无需 `pip install`。

以下命令在仓库根目录运行，无第三方 Python 依赖：

```bash
# 离线检索候选路线：每条给出编号、一句话用途和正文位置。
python3 scripts/proof_templates.py search "重尾噪声 裁剪 SGD" --limit 2
```

```text
T16 [proof-template] 把裁剪梯度分成 centered martingale 与 clipping bias。
  proofs/optimization/T16-heavy-tail-clipping.md
T01 [proof-template] 把单步目标下降累积成平均梯度平方界。
  proofs/optimization/T01-descent.md
```

```bash
# 阅读路线卡的假设、证明骨架与失败边界。
python3 scripts/proof_templates.py show T16

# 可选：安装 skill（二选一）。Codex，链接到 ~/.codex/skills：
python3 scripts/install_skill.py
# Claude Code，链接到个人 skills 目录：
python3 scripts/install_skill.py --target ~/.claude/skills/vibe-dlmath
```

仓库应保留在稳定位置：安装器创建符号链接；已有不同内容时会保留并报错。完整说明见 [Skill 使用](docs/SKILL.md)。其他支持 `SKILL.md` 的工具可按该文档加载完整仓库。

安装后可以这样提问（Codex 用 `$vibe-dlmath` 调用，Claude Code 用 `/vibe-dlmath`）：

```text
使用 $vibe-dlmath，证明重尾噪声下 clipped SGD 的收敛界。
先找库里最接近的证明路线，说明每一步沿用哪张卡、在哪里偏离；
保留原命题的假设与量词，逐条列出证明义务和来源；
遇到缺口，写明缺的引理、需要加的条件或反例。
```

也可以生成一个待填写的工作单：

```bash
python3 scripts/proof_templates.py scaffold T01 T16 \
  --problem "重尾噪声下 clipped SGD 的收敛界" \
  --out my-proof.md
```

工作单会保留待证项，拒绝覆盖已有文件。关键词检索用于寻找候选；选择哪条路线，要由数学对象与假设决定。

## 路线从哪里来：证明蒸馏

每张卡都从论文中的证明蒸馏而来。蒸馏保留原定理的适用范围，只提取能迁移的步骤；把一篇新论文整理成新路线，也按同样五步：

1. **定位证据。** 固定论文版本、定理号、假设与证明位置，区分原文陈述和自己的推导。
2. **提取机制。** 找到下降、耦合、势函数、换测度等关键步骤，解释为什么它能解决当前困难。
3. **写明迁移条件。** 记录换模型、优化器、采样或误差度量后，哪些步骤仍成立，哪些必须重证。
4. **关闭证明义务。** 为每条 claim 写出依赖、证据与状态；将未证引理留在账本中。
5. **检验边界。** 检查量词、概率、常数、资源、反例和实际算法输出，再决定结论能说到哪里。

可以从两条具体路线开始：[经典下降如何接入偏差与方差](extensions/经典下降证明的偏差与方差接口.md)、[经典编码界如何处理数据依赖解码器](extensions/经典编码界与数据依赖解码器.md)。进一步可读 [T50：数据依赖证书](proofs/generalization/T50-data-dependent-certificate-envelope.md)，或 [T51：从 Flow Matching 速度误差到轨迹与 Wasserstein 距离](proofs/generation-transport/T51-flow-trajectory-error.md)。

详细操作见 [证明蒸馏](docs/PROOF_DISTILLATION.md)。学习完整论证可读 [端到端学习证明](docs/END_TO_END_LEARNING_PROOF.md)；撰写新定理可使用 [定理档案](templates/THEOREM_DOSSIER.md)。

## 护栏：偏离路线的地方必须说明

沿路线写不等于照抄。换一个优化器、采样方式或误差指标，原证明中看似不起眼的独立性、光滑性或量词范围，就可能不再成立。例如“训练梯度趋于零，所以测试风险趋于 Bayes 风险”跳过了两段论证；[T32](proofs/generalization/T32-excess-risk-decomposition.md) 把 excess risk 拆成三笔需要分别证明的误差：

$$
R(\widehat h)-R^\star
\leq\epsilon_{\rm app}+2\Delta_S+\epsilon_{\rm opt}
$$

其中 $\widehat h$ 是训练输出， $R^\star$ 是比较基准（对全部可测预测器取 inf 时就是 Bayes 风险）。“梯度趋于零”只是驻点性质，要借助 PL、凸性或 NTK 区域等额外桥梁才能控制优化 gap $\epsilon_{\rm opt}$；逼近误差 $\epsilon_{\rm app}$ 和估计项 $\Delta_S$ 还要另行证明。

> **失败例子**：在 $f(w)=(w^2-1)^2$ 中， $w=0$ 的梯度为零，函数值却比全局最小值高 1。

[AI 证明合同](docs/AI_PROOF_CONTRACT.md)要求 agent 逐条处理证明义务：不得暗加假设、改变原命题的量词、编造引用，或把实验、数值检查、检索命中写成已完成的数学证明。推导遇到缺口时，应返回具体的缺失条件、未证引理、反例或条件性结论。

逐 claim 账本可运行结构检查：

```bash
# 阅读一个填好的账本，并检查其结构与内部一致性。
python3 scripts/audit_proof.py examples/biased_sgd_ledger.json

# 新证明从此模板开始；未填写的模板会报告待解决问题。
python3 scripts/audit_proof.py templates/PROOF_LEDGER.json
```

这个检查器帮助发现结构和依赖问题，**不自动证明数学正确**。最终仍要核对每一步推导及其来源；通过测试或脚本检查，也不会提升论文的人工核验等级。

## 理论地图

| 主题 | 典型问题 |
|---|---|
| [优化与随机估计](proofs/optimization/README.md) | 下降、势函数、方差缩减、重尾、非光滑、二阶驻点、客户端偏差 |
| [泛化与信息论](proofs/generalization/README.md) | 风险分解、一致收敛、稳定性、PAC-Bayes、间隔、压缩、鲁棒认证 |
| [神经网络、表示与训练机制](proofs/deep-learning/README.md) | 逼近、NTK、特征动力学、隐式偏置、对比学习、等变性 |
| [生成模型与分布输运](proofs/generation-transport/README.md) | 训练误差、连续过程、离散采样、分布距离与风险 |
| [在线决策与策略几何](proofs/sequential-decision/README.md) | Bandit、Bellman 误差、mirror descent、regret |
| [统计估计与覆盖](proofs/statistics/README.md) | 双重稳健、conformal、隐私记账、因果识别 |
| [信息下界与表达能力](proofs/lower-bounds-expressivity/README.md) | 困难实例、构造性模拟、表达下界、GNN 与 1-WL |
| [评价、校准与在线监测](proofs/evaluation-monitoring/README.md) | 校准、评分规则、Bayesian filtering、适应性与停止时间 |

47 张卡包括 43 个证明模板、2 张问题特定方法卡、1 个经验代数工具和 1 个路由页。每种卡的可用范围不同；具体覆盖、未覆盖方向与学习顺序见 [DL 理论框架](docs/DL_THEORY_FRAMEWORK.md)和 [TOPICS](TOPICS.md)。

## 论文按需下载

```bash
# 预览清单；不联网、不修改文件。
python3 scripts/download_papers.py --dry-run

# 示例：只下载生成模型主题，或只取指定 arXiv 条目。
python3 scripts/download_papers.py --topic generative
python3 scripts/download_papers.py --ids 2105.04026

# 离线重建本地论文目录。
python3 scripts/download_papers.py --reindex
```

省略筛选条件会下载全部清单；`--no-sources` 可只下载 PDF。脚本支持 macOS/Linux，断点重跑时会跳过已经通过格式与 SHA-256 校验的文件。下载说明、版本与重建规则见 [DOWNLOADING](docs/DOWNLOADING.md)。

Git 保存笔记、清单、metadata、核验卡与脚本；PDF、源码压缩包和解包资源作为可重建缓存排除在 Git 外。论文卡保留官方在线入口，clone 后的本地 PDF/TeX 链接需先下载。101 是收录条目数，不代表已逐条核验论文中的定理。[库存报告](reports/inventory.json)是生成时的机器快照，并不说明新 clone 已有缓存；运行 `python3 scripts/check_library.py` 查看本机状态，或用上面的 `--reindex` 更新本机报告。

## 目录与维护

```text
proofs/                 8 个主题的正文卡与检索 registry
Math 基础/              循序渐进的数学前置与学习路线
templates/              证明工作单、claim 账本、论文核验模板
examples/               可运行示例与完整账本
catalog/ + proof_ref/    论文清单、来源记录、核验卡与可选缓存
skills/vibe-dlmath/      随仓库维护的 agent skill
scripts/ + tests/       检索、下载、结构检查与回归测试
docs/ + extensions/     证明流程、覆盖边界与补充推导
CHANGELOG.md            初始发布内容与后续用户可见变化
```

维护约定见 [CONTRIBUTING](CONTRIBUTING.md)。正文只维护一份，通过 registry 生成目录与论文反链。知识更新同步维护相关目录、来源与核验状态，并在 [CHANGELOG](CHANGELOG.md) 中说明使用者需要知道的新增、修订与限制。常用本地检查：

```bash
python3 -m unittest discover -s tests -v
python3 scripts/check_library.py
```

这些检查覆盖工具行为、链接和记录一致性，数学核验范围另见 [模板核验状态](证明模板核验状态.md)与 [论文核验导航](proof_ref/核验导航.md)。CI 示例保存在 [check-workflow.example.yml](docs/check-workflow.example.yml)，是否启用应以实际仓库配置为准。

内容来源、核验范围与可选外围笔记的访问说明见 [PROVENANCE](docs/PROVENANCE.md)。核心证明流程所需的模板、前置知识、来源记录与工具均随本库提供。

**许可：** 本库原创代码与原创文档采用 [MIT License](LICENSE)。第三方论文、源码与引用素材保留各自许可，见 [第三方内容说明](THIRD_PARTY_NOTICES.md)。维护者发布前应核对 [发布检查清单](docs/OPEN_SOURCE.md)。
