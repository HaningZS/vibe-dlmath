#!/usr/bin/env python3
"""Link this repository's skill into the user's Codex skills directory."""
from __future__ import annotations

import argparse
import os
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def install(source, target):
    source, target = Path(source).resolve(), Path(target).expanduser().absolute()
    if not (source / "SKILL.md").is_file():
        raise ValueError(f"Missing SKILL.md: {source}")
    if target.is_symlink() and target.resolve() == source:
        return "already-linked"
    if target.exists() or target.is_symlink():
        raise FileExistsError(f"Existing skill left untouched: {target}")
    target.parent.mkdir(parents=True, exist_ok=True)
    target.symlink_to(source, target_is_directory=True)
    return "linked"


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--target", type=Path)
    args = parser.parse_args()
    codex_directory = Path(os.environ.get("CODEX_HOME", str(Path.home() / ".codex")))
    target = args.target or codex_directory / "skills/vibe-dlmath"
    print(f"{install(ROOT / 'skills/vibe-dlmath', target)}: {target}")


if __name__ == "__main__":
    try:
        main()
    except (ValueError, OSError) as exc:
        raise SystemExit(str(exc))
