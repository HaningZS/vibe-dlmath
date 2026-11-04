# 把模板库作为 skill 使用

[首页](../README.md) · [模板目录](../proofs/README.md) · [证明工作流](PROOF_WORKFLOW.md)

Skill 的源文件位于 [skills/vibe-dlmath/SKILL.md](../skills/vibe-dlmath/SKILL.md)，随仓库版本维护。它会按问题检索模板，先核对假设与结论类型，再完成解释、推导或审阅。

## 安装

先按 [README 快速开始](../README.md#快速开始先读一张卡再提出一个可检查的问题) 克隆完整仓库并确认 Python 3.11+。单独下载 `SKILL.md` 不包含证明库、检索工具与合同文档。

在你长期保留的仓库目录里运行：

~~~bash
# Codex：链接到 CODEX_HOME/skills（未设置时为 ~/.codex/skills）。
python3 scripts/install_skill.py

# Claude Code：链接到个人 skills 目录。
python3 scripts/install_skill.py --target ~/.claude/skills/vibe-dlmath
~~~

安装器创建指向本仓库 skill 的符号链接。已有不同内容时会报错，不覆盖；重复安装同一个链接是 no-op。仓库应保留在稳定位置，移动后需要更新该链接。

Claude Code 从 `~/.claude/skills/<名称>/SKILL.md` 读取个人 skill，该目录可以是符号链接。只在某个项目中使用时，把 `--target` 换成该项目的 `.claude/skills/vibe-dlmath`。

其他支持 SKILL.md 的工具也可用 --target 链接或直接加载源目录；若复制单独的 skill 文件夹，需要用 VIBE_DLMATH_ROOT 或 helper 的 --repo 指向完整仓库。

## 使用例子

~~~text
使用 $vibe-dlmath，帮我推导带重尾噪声的 clipped SGD 收敛界，
先说明每个假设的直觉，再指出高概率保证还缺哪几步。

使用 $vibe-dlmath，审查这个证明有没有把期望泛化界写成高概率界。

使用 $vibe-dlmath，帮我区分 Transformer 构造性模拟和表达能力下界，
并用我给出的精度、深度和输入模型写清量词。
~~~

Skill 允许正常自动发现，也可以显式调用：Codex 中写 `$vibe-dlmath`，Claude Code 中写 `/vibe-dlmath`。它不会因为关键词命中就认定模板适用，也不会把下载状态改成证明核验状态。

## 独立 CLI

不使用 skill 时，同样能直接检索：

~~~bash
python3 scripts/proof_templates.py search "PAC-Bayes 泛化" --json
python3 scripts/proof_templates.py show T05
python3 scripts/proof_templates.py list --kind method-card
python3 scripts/proof_templates.py search "GNN 1-WL 消息传递" --json
python3 scripts/proof_templates.py search "交叉熵 分类风险 替代损失" --json
~~~

检索、list、show 均离线且只读。scaffold 是显式写文件的命令，输出未完成的证明工作单；这不是自动生成已经核实的定理。

专项模板 T40–T49 沿用同一 registry 自动进入 skill。学习如何从多张卡形成完整结论，可读 [已闭合的学习证明](END_TO_END_LEARNING_PROOF.md)。

T50/T51 提供近期论文蒸馏入口；skill 使用 [AI 证明合同](AI_PROOF_CONTRACT.md) 保留原命题、传播逐 Claim 状态，并区分五类证据。[行为评测](../evals/README.md) 提供可复用请求、人工审阅摘要与限制，原始运行日志未随发行版提供。
