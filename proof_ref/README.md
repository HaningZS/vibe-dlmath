---
type: index
status: active
reviewed: 2026-09-01
---

# Proof Reference Library

独立仓库论文总入口：[PAPERS](../PAPERS.md)。原有两个 collection 保留为历史核验材料；基础扩充的下载清单位于 [catalog/foundations-2026-09.json](../catalog/foundations-2026-09.json)，共 42 条，按数学工具与研究问题分组。

本地 PDF/source 是下载脚本生成的缓存。克隆仓库后执行首页中的下载命令恢复；人工核验卡与 metadata 保存在 Git 中。

此目录保存证明模板对应的原论文 PDF、arXiv source bundle、解压后的 LaTeX 和逐篇核验笔记。

## Collection

- [Core and Recent Theory 2026-09](core-theory-2026-09/INDEX.md)
- [下载清单与模板映射](core-theory-2026-09/REFS.md)
- [Recent Accepted Theory 2025–2026](recent-accepted-2025-2026/INDEX.md)
- [近期正式收录论文清单](recent-accepted-2025-2026/REFS.md)
- [按证明模板浏览已核验论文](%E6%A0%B8%E9%AA%8C%E5%AF%BC%E8%88%AA.md)
- [下载与校验报告](VALIDATION.md)
- [证明模板核验状态](../%E8%AF%81%E6%98%8E%E6%A8%A1%E6%9D%BF%E6%A0%B8%E9%AA%8C%E7%8A%B6%E6%80%81.md)
- [证明模板库](../proofs/README.md)
- [数学前置 ↔ 模板 ↔ PDF 页码](../%E6%95%B0%E5%AD%A6%E5%89%8D%E7%BD%AE%E4%B8%8E%E8%AE%BA%E6%96%87%E8%AF%81%E6%98%8E%E5%AF%BC%E8%88%AA.md)
- [证明阅读的数学学习路线](../Math%20%E5%9F%BA%E7%A1%80/%E8%AF%81%E6%98%8E%E5%B7%A5%E5%85%B7/AI%20%E7%90%86%E8%AE%BA%E8%AF%81%E6%98%8E%E5%89%8D%E7%BD%AE%E5%AD%A6%E4%B9%A0%E8%B7%AF%E7%BA%BF.md)

## 链接约定

- 下载器生成的逐篇 `README.md` 只记录文件清单；人工核过的论文另有 `核验笔记.md`。
- 模板先链接到 `核验笔记.md`，核验笔记再反链模板，并直接链接 `paper.pdf#page=N` 与 `source/` 下的具体 TeX 文件。
- PDF 页码链接写法如下；Obsidian 是否精确跳页取决于当前 PDF viewer：

```md
[[某论文目录/paper.pdf#page=12|PDF：Theorem 3.1, p.12]]
```

- TeX 使用真实的 `source/` 目录，例如：

```md
[[某论文目录/source/appendix.tex|TeX：Appendix proof]]
```

- `INDEX.md` 是下载器生成的机器清单，可能在重新索引时覆盖；人工导航和双向链接维护在 [核验导航](%E6%A0%B8%E9%AA%8C%E5%AF%BC%E8%88%AA.md) 与逐篇 `核验笔记.md`。
- 数学前置的人工映射统一维护在 [数学前置与论文证明导航](../%E6%95%B0%E5%AD%A6%E5%89%8D%E7%BD%AE%E4%B8%8E%E8%AE%BA%E6%96%87%E8%AF%81%E6%98%8E%E5%AF%BC%E8%88%AA.md)，不要写入可能被 reindex 覆盖的机器 `INDEX.md`。

## 数据边界

- `paper.pdf` 与 `source.tar.gz` 均来自相同 arXiv identifier，但 arXiv 版本仍可能与 conference camera-ready 有定理编号差异。
- 录用信息只由 venue 官方页面确认；arXiv 链接只用于缓存 PDF/TeX，不作为录用证据。
- ICML 2026 条目如缺稳定 proceedings/camera-ready crosswalk，暂留在“近期框架/待复核”，不晋级为逐式 verified。
