---
type: validation-report
status: active
reviewed: 2026-09-01
---

# Proof reference 下载与校验报告

本页保留 2026-09-01 原笔记库的历史验证结果。独立仓库 2026-09-26 的当前统计与错误状态见 [全库 inventory](../reports/inventory.json) 和 [下载报告](../reports/download_report.json)；旧 collection 报告中的路径是当时的 vault 相对路径。

- 返回：[Proof Reference Library](README.md) · [核验导航](%E6%A0%B8%E9%AA%8C%E5%AF%BC%E8%88%AA.md) · [证明模板核验状态](../%E8%AF%81%E6%98%8E%E6%A8%A1%E6%9D%BF%E6%A0%B8%E9%AA%8C%E7%8A%B6%E6%80%81.md)

## 结果摘要

| collection | primary PDF | source bundle | extracted TeX | PDF pages | 下载失败 |
|---|---:|---:|---:|---:|---:|
| [Core and Recent Theory](core-theory-2026-09/INDEX.md) | 26 | 26 | 209 | 947 | 0 |
| [Recent Accepted Theory](recent-accepted-2025-2026/INDEX.md) | 16 | 16 | 100 | 702 | 0 |
| 合计 | 42 | 42 | 309 | 1,649 | 0 |

这里的 PDF 数只统计每篇目录根部的 `paper.pdf`，不把 LaTeX source 内的插图 PDF 重复计数。

## 自动完整性检查

- 42/42 `paper.pdf` 通过 `%PDF-` magic、`pdfinfo` 页数检查和 `pdftotext` 非空检查。
- 42/42 `source.tar.gz` 通过 gzip/tar 完整性检查；每篇均解压出至少一个非空 `.tex`。
- 16 篇 recent collection 的 archive 成员与 `source/` 解压结果逐项一致，且未发现绝对路径或 `../` 归档成员。
- 两个 collection 的 `REFS.md` arXiv identifier 与下载器生成 `INDEX.md` 一致；每个索引目录均有 `paper.pdf`、`source.tar.gz`、`source/`、`metadata.json` 和 `README.md`。
- JSON 下载报告与逐篇 metadata 均可解析；两个报告均为 `failed: 0`。
- 18 篇高优先论文已建立人工 `核验笔记.md`，并完成模板/近期框架 ↔ 核验卡 ↔ PDF/TeX 的双向导航；其余 24 篇保留为 `binary-validated` 语料。

## 数学前置导航校验

- 新增 10 篇 [证明前置/路线笔记](../Math%20%E5%9F%BA%E7%A1%80/%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/AI%20%E7%90%86%E8%AE%BA%E8%AF%81%E6%98%8E%E5%89%8D%E7%BD%AE%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)，8 个 NumPy 示例实际运行通过。
- [数学前置与论文证明导航](../%E6%95%B0%E5%AD%A6%E5%89%8D%E7%BD%AE%E4%B8%8E%E8%AE%BA%E6%96%87%E8%AF%81%E6%98%8E%E5%AF%BC%E8%88%AA.md) 覆盖 42/42 主 PDF；PDF 本体不可写 Markdown，18 张核验卡通过 companion backlink 返回数学导航。
- T01–T25、P01–P10、R01–R14 的数学前置 callout 覆盖分别为 25/25、10/10、14/14。
- Math 与证明库相关范围的 Wiki、章节锚点和 PDF 页码专项扫描均无缺失、无歧义、无越界；原始出现次数会随索引更新变化，因此不把它作为稳定契约。
- 两个下载器生成的 `INDEX.md` 未加入人工内容，重新索引不会覆盖本轮数学映射。

## 视觉抽检

按 PDF 技能的 render-and-review 流程，已把代表性页面渲染为 PNG 并人工检查版面与正文可读性。抽检覆盖：统计可评估性、split conformal、线性 RL、error feedback，以及 recent collection 的优化/Transformer 理论文档。未发现下载到 HTML 错当 PDF、空白页或字体不可读问题。

## 已知异常与处理

1. `2309.16858/source/symbol_tit.tex` 有一个上游源码注释的非 UTF-8 损坏引号；tar 与解压文件一致，正文 LaTeX 非空，故保留原始字节而不擅自改写上游源。
2. arXiv PDF/TeX 与 conference camera-ready 可能有标题、作者顺序或 theorem numbering 差异。核验卡分别记录 arXiv 源位置和正式 venue；两者没有完成 crosswalk 时，状态不得标成 `verified-camera-ready`。
3. COLT 2025 的 Time-Uniform Self-Normalized 会议 PDF 是 extended abstract；完整证明应以本地 arXiv/AoAP 长版源为准，并在引用时说明版本。
4. `2309.16858` 的 arXiv 长版标题与 ICML 2025 子结果标题不同；本库按 arXiv metadata 命名目录，不把两套 theorem number 混用。

## 核验状态词

| 状态 | 含义 |
|---|---|
| `binary-validated` | PDF/source 可打开、可提取、归档完整；尚未逐式审计 |
| `claim-checked-arxiv` | 已对照 PDF 与 TeX 定位具体 theorem/lemma，并核对模板中的结论边界 |
| `claim-checked-long-version` | 已使用 arXiv/AoAP 等完整长版核对 theorem/lemma；会议版可能只是摘要，引用时必须说明版本 |
| `crosswalk-needed` | arXiv 与 camera-ready 的定理编号或标题尚未逐项对齐 |
| `method-card-only` | 只作为单篇论文方法卡，不晋级为普适证明模板 |
| `intake` | 近期条目，录用或稳定 camera-ready 仍待确认 |

^proof-ref-validation
