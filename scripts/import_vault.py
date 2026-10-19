#!/usr/bin/env python3
"""One-time, non-destructive export of the proof library and math prerequisites."""
from __future__ import annotations

import argparse
import json
import os
import re
import shutil
import subprocess
from pathlib import Path
from urllib.parse import quote

from download_papers import atomic_write, base_id, safe_slug, write_json


def github_anchor(heading):
    heading = re.sub(r"\[([^\]]+)\]\([^)]*\)", r"\1", heading)
    heading = heading.replace("`", "").lower()
    return re.sub(r"[^\w\- ]", "", heading, flags=re.UNICODE).replace(" ", "-")


def convert_links(text, source, source_root, mapping, files, revision, external):
    # Skip fenced examples: a sample Wiki link is not a live dependency.
    parts = re.split(r"(^(?:```|~~~)[^\n]*\n.*?^(?:```|~~~)[ \t]*$)", text, flags=re.M | re.S)

    def replace(match):
        inner = match.group(1)
        target, _, alias = inner.partition("|")
        name, marker, anchor = target.partition("#")
        candidates = []
        if not name:
            candidates = [source]
        else:
            for base in (source.parent, source_root):
                for suffix in ("", ".md"):
                    candidate = (base / (name + suffix)).resolve()
                    if candidate.is_file():
                        candidates = [candidate]
                        break
                if candidates:
                    break
            if not candidates:
                names = {name, name + ".md"}
                candidates = [p for p in files if p.name in names or any(p.as_posix().endswith("/" + n) for n in names)]
        if len(candidates) != 1:
            raise ValueError(f"Unresolved/ambiguous Wiki link in {source.name}: {target}")
        original = candidates[0]
        label = alias or name.split("/")[-1] or anchor
        fragment = ""
        if marker:
            fragment = "#" + (anchor if original.suffix.lower() == ".pdf" else github_anchor(anchor))
        if original in mapping:
            relative = os.path.relpath(mapping[original], mapping[source].parent)
            url = quote(relative, safe="/") + quote(fragment, safe="#=^-")
        else:
            relative = original.relative_to(source_root).as_posix()
            url = f"https://github.com/HaningZS/HaningZS_Notes/blob/{revision}/" + quote(relative, safe="/") + quote(fragment, safe="#=^-")
            external.add(relative)
        label = label.replace("[", "\\[").replace("]", "\\]")
        return f"[{label}]({url})"

    for index in range(0, len(parts), 2):
        parts[index] = re.sub(r"\[\[([^\]]+)\]\]", replace, parts[index])
    converted = "".join(parts)
    return "\n".join(line if line.strip() else "" for line in converted.splitlines()).rstrip() + "\n"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--vault", type=Path, required=True)
    parser.add_argument("--out", type=Path, required=True)
    args = parser.parse_args()
    vault, out = args.vault.resolve(), args.out.resolve()
    library = vault / "写论文prompt/证明模板库"
    if (out / "reports/import.json").exists():
        parser.error("Already imported; refusing to overwrite a maintained repository")
    revision = subprocess.check_output(["git", "rev-parse", "HEAD"], cwd=vault, text=True).strip()
    files = [p.resolve() for p in vault.rglob("*") if p.is_file() and ".git" not in p.parts]
    selected = [p for p in files if p.is_relative_to(library) or (p.is_relative_to(vault / "Math 基础") and p.suffix == ".md")]
    mapping = {p: out / (p.relative_to(library) if p.is_relative_to(library) else p.relative_to(vault)) for p in selected}
    external = set()
    for source, destination in mapping.items():
        destination.parent.mkdir(parents=True, exist_ok=True)
        if source.suffix == ".md" and "source" not in source.relative_to(vault).parts:
            text = source.read_text(encoding="utf-8")
            atomic_write(destination, convert_links(text, source, vault, mapping, files, revision, external))
        else:
            shutil.copy2(source, destination)
    papers = []
    for metadata_path in sorted((out / "proof_ref").glob("*/*/metadata.json")):
        metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
        review = metadata_path.parent / "核验笔记.md"
        status = "imported-binary-validated"
        if review.exists():
            match = re.search(r"^status:\s*(.+)$", review.read_text(encoding="utf-8"), re.M)
            status = "imported-" + (match.group(1).strip() if match else "review-card")
        papers.append({"arxiv_id":metadata["identifier"], "title":metadata["title"],
                       "topic":"legacy-reviewed" if review.exists() else "legacy-intake",
                       "collection":metadata_path.parent.parent.name,
                       "path":metadata_path.parent.relative_to(out).as_posix(),
                       "review_status":status, "templates":[], "why":"原库已有关联与核验边界；保留原文。"})
        metadata["imported_from"] = {"repository":"HaningZS/HaningZS_Notes", "commit":revision}
        metadata["edition_status"] = "legacy-unpinned; preserve bytes and existing page references"
        for field in ("directory", "pdf_path", "source_path", "extracted_source_dir"):
            metadata.pop(field, None)
        write_json(metadata_path, metadata)
    write_json(out / "catalog/legacy.json", {"schema_version":1,"papers":papers})
    write_json(out / "reports/import.json", {"source_repository":"HaningZS/HaningZS_Notes","source_commit":revision,
              "proof_files":sum(p.is_relative_to(library) for p in selected),
              "math_notes":sum(p.is_relative_to(vault / "Math 基础") for p in selected),
              "papers":len(papers),"external_context_links":sorted(external)})
    print(f"Imported {len(papers)} papers and {len(selected)} files; preserved source vault")


if __name__ == "__main__":
    main()
