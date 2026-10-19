# 论文下载与缓存

[返回首页](../README.md) · [论文总目录](../PAPERS.md)

## 数据流

`catalog/*.json → 官方 arXiv metadata → 固定版本 PDF/source → 格式与哈希校验 → 论文目录与运行报告`。

2026-10-20 已将 42 份旧未锁版缓存补为确切版本：依据本地 PDF 的 arXiv 标记，并重新下载该固定版本源码，与旧包逐字节哈希匹配。[版本核验报告](../reports/legacy_version_verification.json) 记录了每条证据；本轮结束时全部 101 篇均有 resolved_id。旧未锁版保护逻辑仍保留，用于以后导入的未知版本资料。

脚本只接受官方 arXiv ID/链接，避免把博客、HTML 登录页或错误页当成论文。全新条目首次下载从官方 abstract 页读取题目、作者和版本号，对照清单中的预期题目；题目显著不匹配时停止该条目的下载，并报告错误。已有 `metadata.resolved_id` 必须是带 `vN` 的版本，与 catalog 的基础 ID 及显式版本一致；身份冲突时不联网，也不改写原 metadata 或缓存。

## 常用命令

```bash
python3 scripts/download_papers.py --dry-run
python3 scripts/download_papers.py --topic optimization --limit 3
python3 scripts/download_papers.py --ids 1405.4980 2110.11216
python3 scripts/download_papers.py --no-sources
python3 scripts/download_papers.py --reindex
python3 scripts/check_library.py
python3 -m unittest discover -s tests -v
```

默认同时下载 PDF 与源码并解包，等价于 `--sources --extract`。`--no-extract` 保留源码包但不解包。`--refresh-metadata` 检查版本；发现更新版时会报告，而不会替换旧版并悄悄破坏页码引用。

`--ids` 只接受基础 ID（如 `1405.4980`），用于筛选已有清单；传入 `1405.4980v2` 会报错，不会悄悄丢掉版本。若需固定版本，应先核对论文并在 catalog 的 `arxiv_id` 中明确写入 `vN`，保持 metadata 一致，再用基础 ID 选择。这个操作不能替代对已有文件和引用位置的版本核查。

## 清单格式

```json
{
  "schema_version": 1,
  "papers": [
    {
      "arxiv_id": "1405.4980",
      "title": "Convex Optimization: Algorithms and Complexity",
      "topic": "optimization",
      "templates": ["T01", "T02", "T08"],
      "why": "学习一阶下降与复杂度证明。"
    }
  ]
}
```

文件名默认成为 collection 名；也可以显式写 `collection` 和仓库相对 `path`。arXiv 基础 ID 在整个 catalog 中唯一，带 `vN` 的同一论文也不能重复入库。跨主题通过模板映射与阅读目录关联，不重复下载二进制。

## 续跑与失败

脚本以临时文件接收数据，格式与已有 expected SHA-256 均验证成功后才原子替换目标。已有完整 PDF/source 且 SHA-256 一致时不重复下载。损坏文件会尝试重新下载；失败不会覆盖原来的文件。若固定版本返回的字节与 metadata 已记录的 hash 不同，脚本保留原文件与 expected hash，报告差异；不能通过一次下载把已引用的字节身份悄悄更新掉。维护者应另行核对版本、内容和引用后，明确记录确有必要的 hash 迁移。

每个 HTTP 请求有超时；429/部分 5xx 有有限重试，并尊重数值型 `Retry-After`。单进程串行请求，默认间隔 3.1 秒。它支持“从已完成论文继续”的断点续跑，不支持对一个未完成的大文件进行 HTTP Range 字节续传。

每篇完成后写入 checkpoint。正常结束时：

- `reports/download_report.json`：本次尝试的条目与分别列出的 PDF/source/metadata/extract 错误；
- `reports/NEEDS_MANUAL_DOWNLOAD.md`：仍需重试的具体 URL；
- `reports/inventory.json`：整个 catalog 当前在本机的缓存状态；
- `PAPERS.md`：可点击的论文总目录。

`--reindex` 离线更新全库 inventory、`PAPERS.md` 和逐篇 `LINKS.md`，不会覆盖上一次网络运行的错误报告。人工 README 只在缺少时追加一条返回 `LINKS.md` 的链接，正文和核验卡不覆盖。单篇失败仍继续处理余下论文，最终退出码为 1；完整成功时为 0。未知主题、重复 ID、不安全路径会直接报错。

## 源码与版本边界

arXiv 可能不提供某篇论文的源码，即使 PDF 可下载。报告分别记录两者。解包拒绝路径穿越、绝对路径、软硬链接、设备文件、过大的成员数与展开体积；不会执行论文中的代码，也不会编译 TeX。

每次默认下载流程还会将当前源码包解到临时目录，再逐文件比较已有 `source/` 的原归档内容。缺文件、字节变化、额外 `.tex` 或软链接均会报错，保留用户文件；看到一个 `.tex` 文件不再等同于解包验证成功。独立的非 TeX 备注允许保留，但它们不是原归档证据。成功后 metadata 的 `source_extraction` 记录该次核对的 bundle hash、归档文件数和时间；这是一次检查快照，后续编辑后应重跑下载命令重新核对。`--reindex` 的 PDF/source 数量仅表示压缩包缓存，不表示已重新检查所有解包文件。

迁入资料曾有 42 篇缺少可靠 `vN` 的记录；每篇是否已补齐版本，以当前 metadata 和核验记录为准。仍为 `legacy-unpinned` 的完整缓存可以离线核对，脚本不会给旧字节追认“最新版本”。只要本地存在旧工件，或 metadata 仍记录着旧工件 hash，补缺下载与 metadata refresh 都会停止，要求先确认该批字节的确切版本。这个规则也适用于携带旧 hash、尚无 PDF 的新 clone，避免沿用原核验卡却换成另一版本。确认版本后显式补齐 pin；若字节也需更换，应另行复核并记录迁移。

PDF 检查包含文件头、结尾与 SHA-256；源码检查包含归档结构和 TeX。它们不证明数学结论正确。可另用系统 `pdfinfo` / `pdftotext` 做完整解析检查。
