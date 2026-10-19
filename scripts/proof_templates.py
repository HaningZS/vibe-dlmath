#!/usr/bin/env python3
"""Offline template discovery and explicitly requested proof worksheets."""
from __future__ import annotations

import argparse
import json
import os
import re
from pathlib import Path
from urllib.parse import quote

ROOT = Path(__file__).resolve().parents[1]
KINDS = {"proof-template", "method-card", "project-tool", "router"}


def load_registry(root=ROOT):
    root = Path(root).resolve()
    data = json.loads((root / "proofs/registry.json").read_text(encoding="utf-8"))
    if data.get("schema_version") != 1:
        raise ValueError("Unsupported template registry schema")
    if any(not re.fullmatch(r"[a-z][a-z0-9-]*", topic) for topic in data["topics"]):
        raise ValueError("Topic names must be safe lowercase directory slugs")
    seen, paths = set(), set()
    for entry in data["templates"]:
        identifier = entry["id"]
        if not re.fullmatch(r"T\d{2}[A-Z]?", identifier) or identifier in seen:
            raise ValueError(f"Invalid or duplicate template ID: {identifier}")
        seen.add(identifier)
        path = Path(entry["path"])
        if path.is_absolute() or ".." in path.parts or not (root / path).resolve().is_relative_to(root):
            raise ValueError(f"Unsafe template path: {path}")
        if path in paths or not (root / path).is_file():
            raise ValueError(f"Duplicate or missing template path: {path}")
        paths.add(path)
        if entry["kind"] not in KINDS or entry["topic"] not in data["topics"]:
            raise ValueError(f"Invalid kind/topic: {identifier}")
        if path.suffix != ".md" or path.parts[:2] != ("proofs", entry["topic"]):
            raise ValueError(f"Template must be a Markdown card in its topic: {identifier}")
    for entry in data["templates"]:
        if set(entry["related"]) - seen:
            raise ValueError(f"Unknown related ID: {entry['id']}")
    return data


def get_template(data, identifier):
    identifier = identifier.upper()
    entry = next((row for row in data["templates"] if row["id"] == identifier), None)
    if entry is None:
        raise ValueError(f"Unknown template ID: {identifier}")
    return entry


def search(data, query, limit=5):
    if limit < 1:
        raise ValueError("limit must be positive")
    query = query.strip().casefold()
    if not query:
        return []
    explicit = set(re.findall(r"\bt\d{2}[a-z]?\b", query))
    normalized_query = re.sub(r"[-_/]", " ", query)
    words = set(re.findall(r"[a-z0-9][a-z0-9-]+", query)) - {"and","the","with","for","of","to","in","how","can","want","proof"}
    chinese_terms = {term for term in re.findall(r"[\u4e00-\u9fff]+", query) if len(term) >= 2}
    results = []
    for entry in data["templates"]:
        hits, score = [], 0
        if entry["id"].casefold() in explicit:
            hits.append(entry["id"])
            score += 100
        for keyword in entry["keywords"]:
            term = keyword.casefold()
            if re.search(r"[\u4e00-\u9fff]", term):
                matched = term in query
            else:
                normalized_term = re.sub(r"[-_/]", " ", term)
                matched = bool(re.search(r"(?<![a-z0-9])" + re.escape(normalized_term) + r"(?![a-z0-9])", normalized_query))
            if matched:
                hits.append(keyword)
                score += 4 + min(len(term), 16) / 16
        title_words = set(re.findall(r"[a-z0-9][a-z0-9-]+", entry["title"].casefold()))
        score += min(len(words & title_words), 3) * 0.25
        for term in chinese_terms:
            if term in entry["summary"] and term not in hits:
                hits.append(term)
                score += 3
        if score:
            results.append({**entry, "score":round(score, 3), "matched_terms":hits,
                            "notice":"检索候选，不是适用性证书；先读复用契约。"})
    return sorted(results, key=lambda row:(-row["score"], row["id"]))[:limit]


def section(text, heading):
    pattern = r"^## " + re.escape(heading) + r"\s*\n(.*?)(?=^## |\Z)"
    match = re.search(pattern, text, re.M | re.S)
    if not match:
        raise ValueError(f"Missing required section: {heading}")
    return match.group(1).strip()


def worksheet(root, data, identifiers, problem, output):
    entries = [get_template(data, item) for item in identifiers]
    if len({entry["id"] for entry in entries}) != len(entries):
        raise ValueError("Duplicate template IDs in worksheet")
    if any(entry["kind"] == "router" for entry in entries):
        raise ValueError("Select a concrete child (T20A or T20B), not router T20")
    output = Path(output).resolve()
    if output.exists():
        raise FileExistsError(f"Refusing to overwrite existing file: {output}")
    lines = [
        "# 证明工作单：待实例化", "", "**状态：未完成证明；本文件只整理假设与证明义务。**", "",
        "## 研究问题", "", problem, "", "## 定理合同", "",
        "- 对象、维度、随机性与样本分布：待填写。",
        "- 量词与结论：期望 / 高概率 / 对所有时刻 / 存在性 / 不可能性。",
        "- 数据访问、计算资源与输出规则：待填写。",
        "- 目标误差度量、常数依赖与适用范围：待填写。", "",
        "## 组合前检查", "",
        "- [ ] 所有模板使用一致的变量、filtration、概率空间与目标量。",
        "- [ ] 同一 good event 的失败概率已分配；期望保证未被擅自升级。",
        "- [ ] 一个 lemma 的输出确实满足下一 lemma 的输入假设。",
        "- [ ] 方法卡/项目代数没有被写成普适性能保证。", ""
    ]
    lines += [
        "## 假设与引理账本", "",
        "| 假设/引理 | 给定、已证还是待证 | 依赖与使用位置 | 来源版本或自证步骤 |",
        "|---|---|---|---|",
        "| 待填写 | 待证 | 待填写 | 待填写 |", "",
        "## 逐 Claim 状态与证据", "",
        "| Claim | 精确命题与量词/输出 | 依赖 | 证据种类、版本与位置 | 状态与缺口 |",
        "|---|---|---|---|---|",
        "| C1 | 待填写 | 待填写 | 待核对 | open：尚未完成推导 |", "",
        "新增假设标为 added；相应结论只可记 conditional。闭合 Claim 不能依赖 open/refuted；形式化证据另记实际运行和命题对应。", "",
        "## 范围与资源检查", "",
        "- [ ] 样本数、宽度、深度、训练步数、精度和失败概率的依赖完整。",
        "- [ ] 参数条件同时可满足，bound 在目标区间内非空泛。",
        "- [ ] 构造、优化、泛化与机制解释没有被互相替代。",
        "- [ ] 声称对应实现时，sum/mean、采样、裁剪、mask 和子问题误差一致。", ""
    ]
    for entry in entries:
        card = root / entry["path"]
        text = card.read_text(encoding="utf-8")
        link = quote(os.path.relpath(card, output.parent), safe="/")
        lines += [
            f"## {entry['id']}：{entry['summary']}", "",
            f"类型：{entry['kind']}；原核验状态：{entry['status']}。", "",
            f"[原模板卡]({link})", "", section(text, "复用契约"), "",
            "### 本问题中的证明义务", "", section(text, "实例化时必须完成"), ""
        ]
    lines += ["## 原文证据", "", "- 论文固定版本、theorem/lemma、页码/TeX 位置：待核对。",
              "- 已有核验卡的范围是否覆盖本次使用：待核对。", "",
              "## 尚未关闭的缺口", "", "- 缺失假设、未证 lemma 或潜在反例：逐项登记。", "",
              "## 最终结论", "", "仅在上述义务关闭后填写；否则报告条件性结论或反例。", ""]
    output.parent.mkdir(parents=True, exist_ok=True)
    with output.open("x", encoding="utf-8") as handle:
        handle.write("\n".join(lines).rstrip()+"\n")
    return output


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    sub = parser.add_subparsers(dest="command", required=True)
    listing = sub.add_parser("list")
    listing.add_argument("--topic")
    listing.add_argument("--kind", choices=sorted(KINDS))
    listing.add_argument("--json", action="store_true")
    querying = sub.add_parser("search")
    querying.add_argument("query")
    querying.add_argument("--limit", type=int, default=5)
    querying.add_argument("--json", action="store_true")
    showing = sub.add_parser("show")
    showing.add_argument("id")
    drafting = sub.add_parser("scaffold")
    drafting.add_argument("ids", nargs="+")
    drafting.add_argument("--problem", required=True)
    drafting.add_argument("--out", type=Path, required=True)
    args = parser.parse_args(argv)
    root = args.root.resolve()
    data = load_registry(root)
    if args.command == "show":
        print((root / get_template(data, args.id)["path"]).read_text(encoding="utf-8"))
        return 0
    if args.command == "scaffold":
        print(worksheet(root, data, args.ids, args.problem, args.out))
        return 0
    if args.command == "list":
        if args.topic and args.topic not in data["topics"]:
            parser.error("Unknown topic")
        rows = [entry for entry in data["templates"]
                if (not args.topic or entry["topic"] == args.topic)
                and (not args.kind or entry["kind"] == args.kind)]
    else:
        rows = search(data, args.query, args.limit)
    if args.json:
        print(json.dumps(rows, ensure_ascii=False, indent=2))
    else:
        for entry in rows:
            print(f"{entry['id']} [{entry['kind']}] {entry['summary']}\n  {entry['path']}")
        if not rows:
            print("没有匹配候选；请换用具体数学对象、目标或模板编号。")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(str(exc))
