#!/usr/bin/env python3
"""Check catalog, local Markdown links/anchors and optional paper binaries offline."""
from __future__ import annotations

import argparse
import json
import os
import re
import subprocess
from pathlib import Path
from urllib.parse import unquote, urlparse

from download_papers import ROOT, base_id, load_catalog, repo_path, sha256, validate_artifact, validate_identity
from import_vault import github_anchor


def without_code(text):
    return re.sub(r"^(?:```|~~~)[^\n]*\n.*?^(?:```|~~~)[ \t]*$", "", text, flags=re.M | re.S)


def anchors(path):
    text = without_code(path.read_text(encoding="utf-8"))
    result = set(re.findall(r'<a\s+(?:id|name)="([^"]+)"', text))
    counts = {}
    for heading in re.findall(r"^#{1,6}\s+(.+?)[ \t]*#*[ \t]*$", text, re.M):
        key = github_anchor(heading)
        count = counts.get(key, 0)
        result.add(key + (f"-{count}" if count else ""))
        counts[key] = count + 1
    return result


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--require-cache", action="store_true")
    parser.add_argument("--pdfinfo", action="store_true")
    args = parser.parse_args()
    root = args.root.resolve()
    catalog = load_catalog(root)
    errors, optional = [], set()
    template_count = 0
    if (root / "proofs/registry.json").exists():
        from proof_templates import load_registry, section
        templates = load_registry(root)["templates"]
        template_count = len(templates)
        known_templates = {entry["id"] for entry in templates}
        known_papers = {base_id(entry["arxiv_id"]) for entry in catalog}
        for entry in templates:
            text = (root / entry["path"]).read_text(encoding="utf-8")
            for heading in ("复用契约", "实例化时必须完成"):
                try:
                    section(text, heading)
                except ValueError as exc:
                    errors.append(f"{entry['id']}: {exc}")
            if {base_id(item) for item in entry.get("sources", [])} - known_papers:
                errors.append(f"Unknown paper source in {entry['id']}")
        for paper in catalog:
            if set(paper.get("templates", [])) - known_templates:
                errors.append(f"Unknown template in paper {paper['arxiv_id']}")
    count, link_count, anchor_count = 0, 0, 0
    for path in root.rglob("*.md"):
        relative = path.relative_to(root)
        # Only the repository-root archive is local-only. A nested directory
        # with the same name is still ordinary, checked library content.
        if relative.parts[0] == ".local-archive" or ".git" in path.parts or "source" in path.parts:
            continue
        count += 1
        text = without_code(path.read_text(encoding="utf-8"))
        if re.search(r"(?<!!)\[\[[^\]]+\]\]", text):
            errors.append(f"Unconverted Wiki link: {path.relative_to(root)}")
        link_text = re.sub(r"\$\$.*?\$\$", "", text, flags=re.S)
        targets = re.findall(r"\[[^\n]*?\]\((<[^>\n]+>|[^)\n]+)\)", link_text)
        targets += re.findall(r'''<(?:a|img)\b[^>]*\b(?:href|src)\s*=\s*["']([^"']+)["'][^>]*>''', link_text, re.I)
        for target in targets:
            url = target.strip("<>")
            if urlparse(url).scheme or url.startswith("//"):
                continue
            url, _, anchor = url.partition("#")
            raw_destination = path.parent / unquote(url) if url else path
            lexical_destination = Path(os.path.abspath(raw_destination))
            destination = raw_destination.resolve()
            link_count += 1
            if not destination.is_relative_to(root):
                errors.append(f"Escaping link: {path.relative_to(root)} -> {target}")
                continue
            destination_parts = destination.relative_to(root).parts
            lexical_parts = lexical_destination.relative_to(root).parts if lexical_destination.is_relative_to(root) else ()
            if any(parts and parts[0] == ".local-archive" for parts in (destination_parts, lexical_parts)):
                errors.append(f"Local-only archive link: {path.relative_to(root)} -> {target}")
                continue
            cache_link = "proof_ref" in destination.relative_to(root).parts and (
                destination.name in {"paper.pdf", "source.tar.gz"} or "source" in destination.relative_to(root).parts
            )
            if not destination.exists():
                if cache_link and not args.require_cache:
                    optional.add(destination.relative_to(root).as_posix())
                else:
                    errors.append(f"Missing: {path.relative_to(root)} -> {target}")
                continue
            if anchor and destination.suffix == ".md":
                anchor_count += 1
                decoded = unquote(anchor)
                if decoded not in anchors(destination):
                    errors.append(f"Anchor: {path.relative_to(root)} -> {target}")
    primary_pdfs, sources = 0, 0
    for record in catalog:
        directory = repo_path(root, record["path"])
        metadata = {}
        metadata_path = directory / "metadata.json"
        if metadata_path.exists():
            try:
                metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
                validate_identity(record, metadata)
            except (ValueError, TypeError, AttributeError) as exc:
                errors.append(f"Metadata identity {record['arxiv_id']}: {exc}")
                metadata = {}
        for name, kind in (("paper.pdf", "pdf"), ("source.tar.gz", "source")):
            path = directory / name
            if path.exists():
                try:
                    validate_artifact(path, kind)
                    expected = metadata.get("artifacts", {}).get(kind, {}).get("sha256")
                    if expected and sha256(path) != expected:
                        raise ValueError("Artifact differs from its recorded SHA-256")
                    if kind == "pdf":
                        primary_pdfs += 1
                        if args.pdfinfo:
                            subprocess.run(["pdfinfo", str(path)], check=True, capture_output=True)
                    else:
                        sources += 1
                except Exception as exc:
                    errors.append(f"Invalid {record['arxiv_id']} {kind}: {exc}")
            elif args.require_cache:
                errors.append(f"Cache missing: {record['arxiv_id']} {kind}")
        if not (directory / "README.md").is_file():
            errors.append(f"Paper card missing: {record['arxiv_id']}")
    result = {"markdown_files":count, "local_links":link_count, "anchors":anchor_count,
              "template_routes":template_count,
              "catalog_papers":len(catalog), "primary_pdfs":primary_pdfs, "source_bundles":sources,
              "optional_uncached_links":len(optional), "errors":errors}
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
