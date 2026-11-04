# Release notes

[中文首页](README.md) · [English](README.en.md) · [核验范围](证明模板核验状态.md)

## Unreleased

- README 换用新封面，并加入一张卡的示例（[T32](proofs/generalization/T32-excess-risk-decomposition.md)）、检索输出示例和 Claude Code 的安装与调用方式；[Skill 使用](docs/SKILL.md)同步更新。
- 修正 390 处在 GitHub 上不渲染的行内公式：`$` 前紧贴中文、中文标点、不换行空格或英文字母时，GitHub 不识别公式。只调整空格与少量措辞，数学内容和核验状态不变。

## Initial release candidate

面向 AI researcher 的数学学习与证明复用工具，包含：

- [8 个主题、47 张模板与工具卡](proofs/README.md)：明确输入、假设、结论、反例与实例化义务。
- [56 篇数学前置](<Math 基础/Math 基础目录.md>)、[学习路线](TOPICS.md)及[完整学习证明](docs/END_TO_END_LEARNING_PROOF.md)。
- [经典证明蒸馏](extensions/README.md)、[近期论文精读](docs/RECENT_RESEARCH_2026_10.md)和 [101 篇论文的版本化清单](PAPERS.md)。论文 PDF/source 按需下载。
- [可安装的 agent skill](docs/SKILL.md)、[AI 证明合同](docs/AI_PROOF_CONTRACT.md)、逐 claim 账本与离线检查工具。
- [可复用行为评测题目](evals/cases.md)和确定性回归测试。

原创代码与原创文档采用 [MIT](LICENSE)；第三方材料保留各自许可。模板核验、来源完整性检查和软件测试分别记录，未核验范围及来源问题见[核验状态](证明模板核验状态.md)。后续面向使用者的变化从这里继续登记。
