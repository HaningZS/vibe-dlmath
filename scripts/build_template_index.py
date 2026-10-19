#!/usr/bin/env python3
"""Generate navigation from canonical template cards; never overwrite card bodies."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
from urllib.parse import quote

from download_papers import atomic_write, load_catalog, update_card
from proof_templates import ROOT, load_registry

LABELS = {"proof-template":"证明模板", "method-card":"问题特定方法卡", "project-tool":"经验代数工具", "router":"路由页"}


def table(entries, directory, root):
    lines = ["| 编号 | 适用目标 | 类型 |", "|---|---|---|"]
    for entry in entries:
        url = quote(os.path.relpath(root / entry["path"], directory), safe="/")
        lines.append(f"| [{entry['id']}]({url}) | {entry['summary']} | {LABELS[entry['kind']]} |")
    return lines


def build(root):
    data = load_registry(root)
    rows = data["templates"]
    index = ["# 可复用证明模板目录", "", "[首页](../README.md) · [如何组合证明](../docs/PROOF_WORKFLOW.md) · [Skill 使用](../docs/SKILL.md)", "",
             f"按目标进入主题，再读单张卡的复用契约。当前 {len(rows)} 张卡；T01–T25 与 T20A/T20B 保留，T32 起按 DL 核心与专项理论增量扩展。T26–T31 仍是旧 intake 占位。", "",
             "[DL 理论框架与覆盖边界](../docs/DL_THEORY_FRAMEWORK.md) · [论文级证明审查](../docs/THEORY_REVIEW.md)", "",
             "类型决定能怎样使用：证明模板须重新实例化；方法卡只覆盖特定问题；经验代数工具不提供显著性或机制保证。", ""]
    for topic, label in data["topics"].items():
        subset = [entry for entry in rows if entry["topic"] == topic]
        index += [f"## {label}", "", *table(subset, root / "proofs", root), ""]
        topic_rows = [f"# {label}", "", "[全部模板](../README.md) · [证明工作流](../../docs/PROOF_WORKFLOW.md)", "",
                      *table(subset, root / "proofs" / topic, root), ""]
        atomic_write(root / "proofs" / topic / "README.md", "\n".join(topic_rows).rstrip()+"\n")
    atomic_write(root / "proofs/README.md", "\n".join(index).rstrip()+"\n")
    compatibility = ["---", "type: compatibility-index", "status: active", f"refined: {data['refined']}", "---", "",
                     "# 证明模板库：旧链接兼容入口", "",
                     "正文已按主题拆分，当前入口为 [模板目录](proofs/README.md)。此文件由 registry 生成，用于保留原编号、章节链接和 block ID；不要在这里维护第二份证明。", "",
                     "## 0. 如何使用这份文档", "",
                     "从 [证明工作流](docs/PROOF_WORKFLOW.md) 固定对象与保证类型，再选模板。旧速记区已由条件完整的独立卡替代。", ""]
    for entry in rows:
        if not entry.get("legacy_anchor"):
            continue
        compatibility += [f"# {entry['id']}. {entry['title']}", "",
                          f"[打开当前模板：{entry['summary']}]({quote(entry['path'], safe='/')})", "",
                          f"类型：{LABELS[entry['kind']]}。适用假设、推导与反例以当前模板卡为准。", ""]
        for block in entry.get("legacy_blocks", []):
            compatibility += [f'<a id="{block}"></a>', "",
                              f"[原公式块 {block}]({quote(entry['path'], safe='/')}#{block})", f"^{block}", ""]
    atomic_write(root / "证明模板库（待核查）.md", "\n".join(compatibility).rstrip()+"\n")
    # Companion navigation follows the registry, without reindexing absent caches.
    import json
    for record in load_catalog(root):
        metadata_file = root / record["path"] / "metadata.json"
        metadata = json.loads(metadata_file.read_text(encoding="utf-8")) if metadata_file.exists() else {}
        update_card(root, record, metadata)
    print(f"Built {len(data['topics'])} topic indexes, {len(rows)} template routes, and paper backlinks.")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    build(parser.parse_args().root.resolve())
