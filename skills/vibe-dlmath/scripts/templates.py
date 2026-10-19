#!/usr/bin/env python3
"""Locate the checked-out library without hard-coded local paths."""
from __future__ import annotations

import argparse
import os
from pathlib import Path
import sys


def locate(explicit=None):
    override = explicit or os.environ.get("VIBE_DLMATH_ROOT")
    candidates = [Path(override)] if override else [
        *Path(__file__).resolve().parents,
        Path.cwd(), *Path.cwd().parents,
    ]
    for candidate in candidates:
        candidate = candidate.expanduser().resolve()
        if (candidate / "proofs/registry.json").is_file() and (candidate / "scripts/proof_templates.py").is_file():
            return candidate
    raise ValueError("Cannot find vibe-dlmath. Pass --repo /path/to/vibe-dlmath or set VIBE_DLMATH_ROOT.")


def main():
    parser = argparse.ArgumentParser(add_help=False)
    parser.add_argument("--repo", "--root")
    args, remaining = parser.parse_known_args()
    root = locate(args.repo)
    sys.path.insert(0, str(root / "scripts"))
    from proof_templates import main as library_main
    return library_main(["--root", str(root), *remaining])


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except (ValueError, OSError) as exc:
        raise SystemExit(str(exc))
