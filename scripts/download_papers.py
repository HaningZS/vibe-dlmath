#!/usr/bin/env python3
"""Manifest-driven arXiv cache. Python 3.11+, standard library only.

The collection/README/report contract follows ST-OPD's paper_refs downloader;
this standalone implementation adds pinned versions, atomic verified caches,
bounded safe extraction, retries, and offline indexing.
"""
from __future__ import annotations

import argparse
import contextlib
import hashlib
import html
import json
import os
import re
import shutil
import sys
import tarfile
import tempfile
import time
from datetime import datetime, timezone
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
from urllib.error import HTTPError, URLError
from urllib.parse import quote, urlparse
from urllib.request import Request, urlopen

ROOT = Path(__file__).resolve().parents[1]
if sys.version_info < (3, 11):
    raise SystemExit("Python 3.11+ is required; select a Python 3.11 or newer interpreter.")
ID_RE = re.compile(r"(?:\d{4}\.\d{4,5}|[a-z-]+(?:\.[A-Z]{2})?/\d{7})(?:v\d+)?")
USER_AGENT = "vibe-dlmath/1.0 (+https://github.com/HaningZS/vibe-dlmath)"
MAX_DOWNLOAD = 100 * 1024 * 1024
MAX_EXTRACT = 500 * 1024 * 1024
MAX_MEMBERS = 10000


def now():
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def atomic_write(path, data):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, temp = tempfile.mkstemp(prefix=".partial-", dir=path.parent)
    try:
        with os.fdopen(fd, "wb") as handle:
            handle.write(data.encode("utf-8") if isinstance(data, str) else data)
        os.replace(temp, path)
    finally:
        if os.path.exists(temp):
            os.unlink(temp)


def write_json(path, data):
    atomic_write(path, json.dumps(data, ensure_ascii=False, indent=2) + "\n")


def sha256(path):
    with Path(path).open("rb") as handle:
        return hashlib.file_digest(handle, "sha256").hexdigest()


def normalize_id(value):
    value = value.strip()
    if value.startswith("arXiv:"):
        value = value[6:]
    if value.startswith(("https://", "http://")):
        parsed = urlparse(value)
        if parsed.hostname not in {"arxiv.org", "export.arxiv.org", "www.arxiv.org"}:
            raise ValueError("Only official arXiv references are supported")
        value = re.sub(r"^/(?:abs|pdf|src|e-print)/", "", parsed.path)
        value = value.removesuffix(".pdf")
    if not ID_RE.fullmatch(value):
        raise ValueError(f"Invalid arXiv ID: {value!r}")
    return value


def base_id(value):
    return re.sub(r"v\d+$", "", normalize_id(value))


def validate_identity(record, metadata):
    """Reject contradictory identities before using a cached pin in a URL."""
    declared = normalize_id(record["arxiv_id"])
    identifier = metadata.get("identifier")
    resolved = metadata.get("resolved_id")
    if identifier:
        identifier = normalize_id(identifier)
        if base_id(identifier) != base_id(declared):
            raise ValueError("Metadata identifier does not match the catalog arXiv ID; existing files were preserved")
    if resolved:
        resolved = normalize_id(resolved)
        if not re.search(r"v[1-9]\d*$", resolved):
            raise ValueError("Metadata resolved_id must include a positive arXiv version")
        if base_id(resolved) != base_id(declared):
            raise ValueError("Metadata resolved_id does not match the catalog arXiv ID; existing files were preserved")
        for value in (declared, identifier):
            if value and re.search(r"v\d+$", value) and value != resolved:
                raise ValueError("Explicit arXiv version conflicts with metadata resolved_id; review the cache before changing its pin")


def safe_slug(title, identifier):
    title = re.sub(r"\\[a-zA-Z]+", " ", title)
    words = re.findall(r"[a-z0-9]+", title.lower())[:8]
    return ("-".join(words)[:80].rstrip("-") or "paper") + "-" + identifier.replace("/", "-")


def repo_path(root, relative):
    path = Path(relative)
    if path.is_absolute() or ".." in path.parts:
        raise ValueError(f"Unsafe repository-relative path: {relative}")
    resolved = (root / path).resolve()
    if not resolved.is_relative_to(root.resolve()):
        raise ValueError(f"Path escapes repository: {relative}")
    return resolved


def load_catalog(root):
    records, seen = [], set()
    for path in sorted((root / "catalog").glob("*.json")):
        payload = json.loads(path.read_text(encoding="utf-8"))
        if payload.get("schema_version") != 1:
            raise ValueError(f"Unsupported schema: {path}")
        for entry in payload["papers"]:
            entry = dict(entry)
            entry["arxiv_id"] = normalize_id(entry["arxiv_id"])
            key = base_id(entry["arxiv_id"])
            if key in seen:
                raise ValueError(f"Duplicate arXiv ID across manifests: {key}")
            seen.add(key)
            if not entry.get("topic") or not entry.get("title"):
                raise ValueError(f"Missing topic/title: {key}")
            entry.setdefault("collection", path.stem)
            entry.setdefault("path", f"proof_ref/{entry['collection']}/{safe_slug(entry['title'], key)}")
            repo_path(root, entry["path"])
            records.append(entry)
    return records


class CitationParser(HTMLParser):
    def __init__(self):
        super().__init__()
        self.values = {}

    def handle_starttag(self, tag, attrs):
        attrs = dict(attrs)
        if tag == "meta" and attrs.get("name", "").startswith("citation_"):
            self.values.setdefault(attrs["name"], []).append(attrs.get("content", ""))


class Client:
    def __init__(self, timeout=35, retries=2, delay=3.1):
        self.timeout, self.retries, self.delay = timeout, retries, delay
        self.last_request = 0.0

    def open(self, url):
        remaining = self.delay - (time.monotonic() - self.last_request)
        if remaining > 0:
            time.sleep(remaining)
        self.last_request = time.monotonic()
        return urlopen(Request(url, headers={"User-Agent": USER_AGENT}), timeout=self.timeout)

    def retry(self, operation):
        for attempt in range(self.retries + 1):
            try:
                return operation()
            except (HTTPError, URLError, TimeoutError, OSError) as exc:
                if isinstance(exc, HTTPError) and exc.code not in {408, 429, 500, 502, 503, 504}:
                    raise
                if attempt == self.retries:
                    raise
                retry_after = exc.headers.get("Retry-After", "") if isinstance(exc, HTTPError) else ""
                pause = min(float(retry_after), 60) if retry_after.isdigit() else min(2 ** (attempt + 1), 30)
                time.sleep(pause)

    def text(self, url):
        def get():
            with self.open(url) as response:
                data = response.read(4 * 1024 * 1024 + 1)
                if len(data) > 4 * 1024 * 1024:
                    raise ValueError("Metadata response too large")
                return data.decode("utf-8", errors="replace")
        return self.retry(get)

    def download(self, url, destination, kind):
        def get():
            fd, temporary = tempfile.mkstemp(prefix=".partial-", dir=destination.parent)
            try:
                with os.fdopen(fd, "wb") as output, self.open(url) as response:
                    size = 0
                    while chunk := response.read(1024 * 1024):
                        size += len(chunk)
                        if size > MAX_DOWNLOAD:
                            raise ValueError("Download exceeds 100 MiB limit")
                        output.write(chunk)
                validate_artifact(Path(temporary), kind)
                os.replace(temporary, destination)
            finally:
                if os.path.exists(temporary):
                    os.unlink(temporary)
        self.retry(get)


def fetch_metadata(identifier, client):
    page = client.text(f"https://arxiv.org/abs/{identifier}")
    parser = CitationParser()
    parser.feed(page)
    meta = parser.values
    if not meta.get("citation_title"):
        raise ValueError("arXiv response has no citation_title; possibly an error page")
    identifier = normalize_id(identifier)
    versions = re.findall(r"\b" + re.escape(base_id(identifier)) + r"v(\d+)\b", page)
    resolved = identifier if re.search(r"v\d+$", identifier) else (
        base_id(identifier) + "v" + str(max(map(int, versions))) if versions else None
    )
    if not resolved:
        raise ValueError("Could not pin the arXiv version from the official abstract page")
    return {
        "title": html.unescape(meta["citation_title"][0]).strip(),
        "authors": meta.get("citation_author", []),
        "published": (meta.get("citation_date") or [None])[0],
        "resolved_id": resolved,
        "metadata_url": f"https://arxiv.org/abs/{resolved}",
        "metadata_checked_at": now(),
    }


def validate_artifact(path, kind):
    if not path.is_file() or path.stat().st_size == 0:
        raise ValueError(f"Missing or empty {kind}")
    if kind == "pdf":
        with path.open("rb") as handle:
            header = handle.read(1024)
            handle.seek(max(0, path.stat().st_size - 4096))
            tail = handle.read()
        if not header.lstrip().startswith(b"%PDF-") or b"%%EOF" not in tail:
            raise ValueError("Invalid or truncated PDF")
    elif kind == "source":
        if not tarfile.is_tarfile(path):
            import gzip
            with gzip.open(path, "rb") as handle:
                data = handle.read(MAX_EXTRACT + 1)
            if len(data) > MAX_EXTRACT or not any(token in data for token in (b"\\document", b"\\input", b"\\def")):
                raise ValueError("Source is neither a tar archive nor recognizable gzipped TeX")
        else:
            with tarfile.open(path, "r:*") as archive:
                check_members(archive.getmembers())
    else:
        raise ValueError(f"Unknown artifact kind: {kind}")


def check_members(members):
    if len(members) > MAX_MEMBERS or sum(m.size for m in members) > MAX_EXTRACT:
        raise ValueError("Archive exceeds member count or expanded size limit")
    names = set()
    for member in members:
        path = PurePosixPath(member.name)
        if not path.parts:
            if member.isdir():
                continue
            raise ValueError("Empty archive filename")
        if path.is_absolute() or ".." in path.parts or "\\" in member.name or ":" in path.parts[0]:
            raise ValueError(f"Unsafe archive path: {member.name}")
        if not (member.isdir() or member.isfile()):
            raise ValueError(f"Unsupported archive member (link/device): {member.name}")
        if path in names and member.isfile():
            raise ValueError(f"Duplicate archive member: {member.name}")
        names.add(path)


def extract_source(bundle, destination):
    """Reproduce archive contents and compare existing files without replacing them."""
    validate_artifact(bundle, "source")
    if destination.is_symlink() or (destination.exists() and not destination.is_dir()):
        raise ValueError("Existing source/ is not a regular directory; preserved for inspection")
    temporary = Path(tempfile.mkdtemp(prefix=".extract-", dir=destination.parent))
    try:
        if tarfile.is_tarfile(bundle):
            with tarfile.open(bundle, "r:*") as archive:
                members = archive.getmembers()
                check_members(members)
                for member in members:
                    target = temporary / member.name
                    if member.isdir():
                        target.mkdir(parents=True, exist_ok=True)
                    else:
                        target.parent.mkdir(parents=True, exist_ok=True)
                        with archive.extractfile(member) as source, target.open("wb") as output:
                            shutil.copyfileobj(source, output)
        else:
            import gzip
            with gzip.open(bundle, "rb") as source:
                atomic_write(temporary / "source.tex", source.read(MAX_EXTRACT + 1))
        if not any(temporary.rglob("*.tex")):
            raise ValueError("Source contains no .tex files")
        expected = {path.relative_to(temporary): path for path in temporary.rglob("*") if path.is_file()}
        if destination.exists():
            local = list(destination.rglob("*"))
            if any(path.is_symlink() for path in local):
                raise ValueError("Existing source/ contains symlinks; preserved for inspection")
            unexpected_tex = {path.relative_to(destination) for path in local
                              if path.is_file() and path.suffix.lower() == ".tex"} - set(expected)
            if unexpected_tex:
                raise ValueError("Existing source/ contains TeX absent from the current bundle; all files preserved")
            for relative, original in expected.items():
                actual = destination / relative
                if not actual.is_file() or sha256(actual) != sha256(original):
                    raise ValueError(f"Existing source/ differs from the current bundle at {relative}; all files preserved")
            state = "verified-existing"
        else:
            temporary.rename(destination)
            state = "extracted"
        return {"state": state, "bundle_sha256": sha256(bundle),
                "archive_file_count": len(expected), "checked_at": now()}
    finally:
        if temporary.exists():
            shutil.rmtree(temporary)  # Exact directory allocated by mkdtemp above.


def cached_ok(path, kind, metadata):
    try:
        validate_artifact(path, kind)
        expected = metadata.get("artifacts", {}).get(kind, {}).get("sha256")
        if expected and sha256(path) != expected:
            return False
        return True
    except (ValueError, OSError, tarfile.TarError):
        return False


def update_card(root, record, metadata):
    directory = repo_path(root, record["path"])
    readme = directory / "README.md"
    directory.mkdir(parents=True, exist_ok=True)
    relative_root = Path(os.path.relpath(root, directory)).as_posix()
    templates = ", ".join(record.get("templates", [])) or "按主题选择"
    review_status = record.get("review_status", "intake")
    review_note = ("下载完成只验证文件；定理假设与证明尚待人工复核。" if review_status == "intake"
                   else "核验范围以维护清单与同目录核验笔记为准；不代表全文证明完成。")
    rows = [f"# {metadata.get('title', record['title'])}", "",
            f"- [官方论文](https://arxiv.org/abs/{metadata.get('resolved_id', record['arxiv_id'])})",
            f"- 主题：`{record['topic']}`；关联模板：{templates}",
            f"- 阅读理由：{record.get('why', '原有证明模板库的论文证据。')}",
            f"- 核验状态：`{review_status}`。{review_note}",
            "- 本地缓存：[PDF](paper.pdf) · [源码包](source.tar.gz)；先运行仓库下载脚本。",
            f"- [返回论文总目录]({relative_root}/PAPERS.md) · [核验卡模板]({relative_root}/templates/PAPER_REVIEW.md)", ""]
    if not readme.exists():
        atomic_write(readme, "\n".join(rows))
    # A separate generated navigation file keeps all human prose untouched.
    connections = ["# 学习关联", "", f"[论文卡](README.md) · [分主题路线]({relative_root}/TOPICS.md) · [论文总目录]({relative_root}/PAPERS.md)", ""]
    if metadata.get("resolved_id"):
        connections += [f"[固定缓存版本](https://arxiv.org/abs/{metadata['resolved_id']}) · [版本与工件哈希](metadata.json)", ""]
    if (directory / "核验笔记.md").is_file():
        connections += ["[核验范围与原文位置](核验笔记.md)", ""]
    master = root / "证明模板库（待核查）.md"
    registry = root / "proofs/registry.json"
    if registry.exists():
        from proof_templates import load_registry
        for entry in load_registry(root)["templates"]:
            if entry["id"] in record.get("templates", []) or base_id(record["arxiv_id"]) in {base_id(item) for item in entry.get("sources", [])}:
                card_path = repo_path(root, entry["path"])
                relative = quote(os.path.relpath(card_path, directory), safe="/")
                connections.append(f"- [{entry['id']}：{entry['summary']}]({relative})")
    elif master.exists():
        for heading in re.findall(r"^# (T\d+\..+)$", master.read_text(encoding="utf-8"), re.M):
            if heading.split(".", 1)[0] in record.get("templates", []):
                anchor = re.sub(r"[^\w\- ]", "", heading.lower()).replace(" ", "-")
                connections.append(f"- [{heading}]({relative_root}/证明模板库（待核查）.md#{quote(anchor)})")
    extension_ids = {
        "PL条件与SGD噪声地板.md": {"1405.4980", "1606.04838", "1608.04636"},
        "矩阵Bernstein与协方差误差.md": {"1011.3027", "1004.4389", "1501.01571"},
        "Ville不等式与随时有效推断.md": {"1808.03204", "1810.08240"},
        "条件期望怎样连接CFM与FM.md": {"2210.02747", "2209.03003"},
    }
    for filename, identifiers in extension_ids.items():
        if base_id(record["arxiv_id"]) in identifiers:
            connections.append(f"- [补充推导：{filename[:-3]}]({relative_root}/extensions/{quote(filename)})")
    atomic_write(directory / "LINKS.md", "\n".join(connections).rstrip() + "\n")
    existing = readme.read_text(encoding="utf-8")
    if "[学习关联与返回路径](LINKS.md)" not in existing:
        atomic_write(readme, existing.rstrip() + "\n\n[学习关联与返回路径](LINKS.md)\n")


def download_one(root, record, client, sources=True, extract=True, refresh=False):
    directory = repo_path(root, record["path"])
    directory.mkdir(parents=True, exist_ok=True)
    metadata_path = directory / "metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
    errors, actions = {}, {}
    pdf = directory / "paper.pdf"
    bundle = directory / "source.tar.gz"
    def identity_failure(message):
        # Do not rewrite even metadata on identity failures: it is provenance.
        return {"arxiv_id": record["arxiv_id"], "title": record["title"], "path": record["path"],
                "actions": {}, "errors": {"metadata": message}, "checked_at": now()}
    try:
        validate_identity(record, metadata)
    except (TypeError, ValueError, AttributeError) as exc:
        return identity_failure(str(exc))
    # Imported binary caches retain their recorded edition; do not replace it silently.
    need_network = not cached_ok(pdf, "pdf", metadata) or (sources and not cached_ok(bundle, "source", metadata))
    existing_bytes = any(path.exists() or path.is_symlink() for path in (pdf, bundle, directory / "source"))
    recorded = metadata.get("artifacts", {})
    recorded_bytes = isinstance(recorded, dict) and any(
        isinstance(item, dict) and (item.get("sha256") or item.get("bytes")) for item in recorded.values()
    )
    if not metadata.get("resolved_id") and (existing_bytes or recorded_bytes) and (refresh or need_network):
        return identity_failure(
            "Existing or recorded legacy-unpinned artifacts cannot be assigned a new edition or mixed with newly downloaded files. "
            "Verify their exact version first; a fresh clone carrying the same unpinned hashes also needs that review. "
            "All files and metadata were preserved."
        )
    if refresh or (need_network and not metadata.get("resolved_id")):
        try:
            fetched = fetch_metadata(record["arxiv_id"], client)
            validate_identity(record, fetched)
            expected = set(re.findall(r"[a-z0-9]+", record["title"].lower()))
            actual = set(re.findall(r"[a-z0-9]+", fetched["title"].lower()))
            if len(expected & actual) / max(1, len(expected)) < 0.45:
                raise ValueError(f"Title/ID mismatch: manifest={record['title']!r}, arXiv={fetched['title']!r}")
            if metadata.get("resolved_id") and metadata["resolved_id"] != fetched["resolved_id"]:
                raise ValueError("A different edition exists; keep this cache and review the version migration separately")
            metadata.update(fetched)
        except Exception as exc:
            return identity_failure(str(exc))
    resolved = metadata.get("resolved_id") or record["arxiv_id"]
    artifacts = [("pdf", pdf, [f"https://arxiv.org/pdf/{resolved}", f"https://arxiv.org/pdf/{resolved}.pdf", f"https://export.arxiv.org/pdf/{resolved}"])]
    if sources:
        artifacts.append(("source", bundle, [f"https://arxiv.org/src/{resolved}", f"https://export.arxiv.org/e-print/{resolved}"]))
    for kind, path, urls in artifacts:
        if cached_ok(path, kind, metadata):
            actions[kind] = "cached"
        elif errors.get("metadata"):
            errors[kind] = "Skipped because paper identity/version metadata failed"
        else:
            for url in urls:
                candidate = None
                try:
                    descriptor, temporary_name = tempfile.mkstemp(prefix=".partial-check-", dir=directory)
                    os.close(descriptor)
                    candidate = Path(temporary_name)
                    client.download(url, candidate, kind)
                    validate_artifact(candidate, kind)
                    expected_hash = metadata.get("artifacts", {}).get(kind, {}).get("sha256")
                    if expected_hash and sha256(candidate) != expected_hash:
                        raise ValueError("Downloaded bytes differ from the recorded SHA-256; existing cache and expected hash preserved")
                    os.replace(candidate, path)
                    actions[kind] = "downloaded"
                    metadata.setdefault("download_urls", {})[kind] = url
                    errors.pop(kind, None)
                    break
                except Exception as exc:
                    errors[kind] = f"{url}: {exc}"
                finally:
                    if candidate is not None and candidate.exists():
                        candidate.unlink()
        if kind in actions:
            metadata.setdefault("artifacts", {})[kind] = {"sha256": sha256(path), "bytes": path.stat().st_size}
    if extract and sources and "source" in actions:
        try:
            metadata["source_extraction"] = extract_source(bundle, directory / "source")
        except Exception as exc:
            errors["extract"] = str(exc)
            metadata.pop("source_extraction", None)
    metadata.update({"identifier": record["arxiv_id"], "title": metadata.get("title", record["title"]),
                     "topic": record["topic"], "templates": record.get("templates", []),
                     "path": record["path"], "last_checked_at": now(), "errors": errors})
    # Old absolute vault paths are provenance, not live file locations.
    for field in ("directory", "pdf_path", "source_path", "extracted_source_dir"):
        metadata.pop(field, None)
    write_json(metadata_path, metadata)
    update_card(root, record, metadata)
    return {"arxiv_id": record["arxiv_id"], "title": metadata["title"], "path": record["path"],
            "actions": actions, "errors": errors, "checked_at": now()}


def artifact_state(root, record):
    directory = repo_path(root, record["path"])
    metadata_path = directory / "metadata.json"
    metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
    return {"arxiv_id": record["arxiv_id"], "title": metadata.get("title", record["title"]),
            "resolved_id": metadata.get("resolved_id"),
            "path": record["path"], "topic": record["topic"],
            "pdf": cached_ok(directory / "paper.pdf", "pdf", metadata),
            "source": cached_ok(directory / "source.tar.gz", "source", metadata),
            "tex_count": sum(1 for _ in (directory / "source").rglob("*.tex")),
            "review_status": record.get("review_status", "intake")}


def write_reports(root, records, results=None):
    # Reindex must not relabel a copied/wrong-edition metadata file or publish
    # links to a different paper. Validate all identities before any report writes.
    for record in records:
        metadata_path = repo_path(root, record["path"]) / "metadata.json"
        if metadata_path.exists():
            metadata = json.loads(metadata_path.read_text(encoding="utf-8"))
            validate_identity(record, metadata)
    for record in records:
        metadata_path = repo_path(root, record["path"]) / "metadata.json"
        metadata = json.loads(metadata_path.read_text(encoding="utf-8")) if metadata_path.exists() else {}
        catalog_fields = {"topic": record["topic"], "templates": record.get("templates", []), "path": record["path"]}
        if metadata_path.exists() and any(metadata.get(key) != value for key, value in catalog_fields.items()):
            metadata.update(catalog_fields)
            write_json(metadata_path, metadata)
        update_card(root, record, metadata)
    rows = [artifact_state(root, record) for record in records]
    inventory = {"generated_at": now(), "total": len(rows),
                 "pdf_count": sum(row["pdf"] for row in rows),
                 "source_count": sum(row["source"] for row in rows),
                 "tex_count": sum(row["tex_count"] for row in rows), "papers": rows}
    write_json(root / "reports/inventory.json", inventory)
    if results is not None:
        failed = [result for result in results if result["errors"]]
        write_json(root / "reports/download_report.json", {"generated_at": now(), "total": len(results),
                  "failed": len(failed), "results": results})
        lines = ["# 待重试下载", "", "先重跑相同命令；已验证缓存会跳过。", ""]
        for result in failed:
            lines.extend([f"## {result['title']}", "", f"https://arxiv.org/abs/{result['arxiv_id']}", ""])
            lines.extend(f"- {kind}: {error}" for kind, error in result["errors"].items())
            lines.append("")
        if not failed:
            lines.append("本次运行没有失败项。")
        atomic_write(root / "reports/NEEDS_MANUAL_DOWNLOAD.md", "\n".join(lines) + "\n")
    lines = ["# 论文总目录", "", "此表由 `scripts/download_papers.py --reindex` 生成。", "",
             "PDF/source 为本表生成时的缓存快照；新 clone 需运行下载命令并 reindex。核验等级不会因下载自动提升。", "",
             "[返回首页](README.md) · [主题阅读顺序](TOPICS.md) · [下载说明](docs/DOWNLOADING.md)", ""]
    by_id = {base_id(record["arxiv_id"]): record for record in records}
    routes = {}
    if (root / "proofs/registry.json").exists():
        from proof_templates import load_registry
        routes = {entry["id"]: quote(entry["path"], safe="/") for entry in load_registry(root)["templates"]}
    for topic in sorted({row["topic"] for row in rows}):
        lines.extend([f"## {topic}", "", "| 论文 | 模板 | PDF/source | 核验状态 |", "|---|---|---|---|"])
        for row in rows:
            if row["topic"] == topic:
                record = by_id[base_id(row["arxiv_id"])]
                path = quote(row["path"] + "/README.md", safe="/")
                title = row["title"].replace("|", " ")
                citation_id = row.get("resolved_id") or row['arxiv_id']
                links = f"[{title}]({path}) · [arXiv](https://arxiv.org/abs/{citation_id})"
                template_cell = ", ".join(f"[{identifier}]({routes[identifier]})" if identifier in routes else identifier
                                          for identifier in record.get("templates", []))
                lines.append(f"| {links} | {template_cell} | {'✓' if row['pdf'] else '—'}/{'✓' if row['source'] else '—'} | {row['review_status']} |")
        lines.append("")
    atomic_write(root / "PAPERS.md", "\n".join(lines).rstrip() + "\n")
    return inventory


@contextlib.contextmanager
def cache_lock(root):
    import fcntl
    path = root / ".download.lock"
    with path.open("a") as handle:
        try:
            fcntl.flock(handle, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            raise ValueError("Another downloader is using this cache")
        try:
            yield
        finally:
            fcntl.flock(handle, fcntl.LOCK_UN)


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--root", type=Path, default=ROOT)
    parser.add_argument("--collection", action="append", help="Select collection; repeatable")
    parser.add_argument("--topic", action="append", help="Select topic; repeatable")
    parser.add_argument("--ids", nargs="+", help="Select catalog arXiv IDs")
    parser.add_argument("--limit", type=int)
    parser.add_argument("--dry-run", action="store_true", help="List only: no network, no writes")
    parser.add_argument("--reindex", action="store_true", help="Offline: rebuild whole-library inventory")
    parser.add_argument("--sources", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--extract", action=argparse.BooleanOptionalAction, default=True)
    parser.add_argument("--refresh-metadata", action="store_true", help="Check pinned edition; never silently replace cached edition")
    parser.add_argument("--timeout", type=float, default=35)
    parser.add_argument("--retries", type=int, default=2)
    parser.add_argument("--delay", type=float, default=3.1, help="Minimum seconds between official requests")
    args = parser.parse_args(argv)
    if args.delay < 3 or args.retries < 0 or args.timeout <= 0 or (args.limit is not None and args.limit < 1):
        parser.error("Require delay >= 3, retries >= 0, timeout > 0, limit >= 1")
    root = args.root.resolve()
    records = load_catalog(root)
    normalized_ids = [normalize_id(item) for item in args.ids] if args.ids else []
    if any(re.search(r"v\d+$", item) for item in normalized_ids):
        parser.error("--ids selects base arXiv IDs only; set the reviewed vN in catalog arxiv_id, then select its base ID")
    requested = set(normalized_ids) if normalized_ids else None
    if requested and requested - {base_id(record['arxiv_id']) for record in records}:
        parser.error("Requested ID is not in catalog; add it to catalog first")
    for selected, field in ((args.collection, 'collection'), (args.topic, 'topic')):
        if selected and set(selected) - {record[field] for record in records}:
            parser.error(f"Unknown {field}: {set(selected) - {record[field] for record in records}}")
    selected = [record for record in records if (not args.collection or record['collection'] in args.collection)
                and (not args.topic or record['topic'] in args.topic)
                and (not requested or base_id(record['arxiv_id']) in requested)]
    if args.limit:
        selected = selected[:args.limit]
    if args.dry_run:
        print(json.dumps(selected, ensure_ascii=False, indent=2))
        return 0
    with cache_lock(root):
        if args.reindex:
            inventory = write_reports(root, records)
            print(json.dumps({key: value for key, value in inventory.items() if key != 'papers'}))
            return 0
        results = []
        client = Client(args.timeout, args.retries, args.delay)
        for index, record in enumerate(selected, 1):
            print(f"[{index}/{len(selected)}] {record['arxiv_id']} {record['title']}", flush=True)
            try:
                result = download_one(root, record, client, args.sources, args.extract, args.refresh_metadata)
            except Exception as exc:
                result = {"arxiv_id": record["arxiv_id"], "title": record["title"],
                          "path": record["path"], "actions": {}, "errors": {"internal": str(exc)}}
            results.append(result)
            # A checkpoint after each paper makes interrupted runs recoverable.
            write_json(root / "reports/download_checkpoint.json", {"results": results})
            print(json.dumps({"actions": result["actions"], "errors": result["errors"]}, ensure_ascii=False), flush=True)
        inventory = write_reports(root, records, results)
        failures = sum(bool(result["errors"]) for result in results)
        print(f"Attempted {len(results)}; failed {failures}; library PDFs {inventory['pdf_count']}/{inventory['total']}")
        return 1 if failures else 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError, json.JSONDecodeError) as exc:
        raise SystemExit(str(exc))
