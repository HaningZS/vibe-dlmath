# 来源与迁出边界

[返回首页](../README.md) · [机器迁出记录](../reports/import.json)

2026-09-26 从 `HaningZS/HaningZS_Notes` 的 commit `8ced9038b7611bcb8c2b2774fb870149df8ef780` 导出：

- `写论文prompt/证明模板库/` 的完整内容，包括原有 T/P/R 编号、核验卡和历史验证报告；
- `Math 基础/` 下 56 篇 Markdown 数学前置，保持原有学科子目录；
- 42 篇论文 PDF/source 作为本地缓存，保留原始下载字节。

源笔记库未删除或移动。新仓库从独立初始提交开始，原仓库历史以此 commit 与 import report 追溯。历史核验结论标为 imported，保留原来的核验日期；此次迁出不冒充对全部旧论文重新做了数学审计。

Wiki 链接转换成标准 Markdown 相对链接，使 GitHub 可直接阅读。迁出的数学和证明内容相互可达；ML/CV/LLM 等外围应用链接指向原仓库固定 commit，不属于独立证明库的必需文件。

下载器参考并延续 ST-OPD `paper_refs` 的 collection、title-first 命名和报告约定，现已独立实现，无 `st_opd`、绝对本机路径或额外 Python 包依赖。原下载器不会固定版本、对已有缓存做哈希检查或完整保存人工 README，本版本补齐了这些行为。

2026-10-19，维护者选择对项目原创代码与原创文档统一采用 [MIT](../LICENSE)。第三方论文、源码、图片与引文的版权和许可仍归原作者/出版方，下载和蒸馏不改变其许可；范围说明见 [第三方材料说明](../THIRD_PARTY_NOTICES.md)。
