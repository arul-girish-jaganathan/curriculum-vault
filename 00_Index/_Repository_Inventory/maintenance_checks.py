#!/usr/bin/env python3
"""
Deterministic repository maintenance checks for curriculum-vault.

Usage:
    python3 00_Index/_Repository_Inventory/maintenance_checks.py [REPO_ROOT]

This script complements curriculum_tools.py with stricter deterministic checks.
"""
from __future__ import annotations

import re
import sys
from collections import defaultdict
from pathlib import Path

WIKILINK_RE = re.compile(r"\[\[([^\]|#]+)(?:#[^\]|]+)?(?:\|[^\]]+)?\]\]")


def repo_files(root: Path):
    for p in root.rglob("*"):
        if p.is_file() and ".git" not in p.parts and ".obsidian" not in p.parts:
            yield p


def markdown_files(root: Path):
    yield from (p for p in repo_files(root) if p.suffix.lower() == ".md")


def normalized_target(target: str) -> str:
    target = target.strip().replace("\\", "/")
    if target.lower().endswith(".md"):
        target = target[:-3]
    return target.lower()


def main(root_arg: str = ".") -> int:
    root = Path(root_arg).resolve()
    files = list(markdown_files(root))
    by_stem: dict[str, list[Path]] = defaultdict(list)
    by_rel: dict[str, Path] = {}

    for p in files:
        rel = p.relative_to(root).as_posix()
        by_rel[rel.lower()] = p
        by_stem[p.stem.lower()].append(p)

    broken = []
    links = []
    incoming = defaultdict(list)

    for p in files:
        text = p.read_text(encoding="utf-8", errors="ignore")
        for match in WIKILINK_RE.finditer(text):
            target = normalized_target(match.group(1))
            links.append((p, target))
            candidates = []
            if "/" in target:
                candidate = by_rel.get(target)
                if candidate:
                    candidates = [candidate]
            else:
                candidates = by_stem.get(target, [])
            if not candidates:
                broken.append((p.relative_to(root).as_posix(), match.group(0)))
            else:
                for candidate in candidates:
                    incoming[candidate].append(p)

    empty = []
    placeholder = []
    for p in files:
        text = p.read_text(encoding="utf-8", errors="ignore").strip()
        if not text:
            empty.append(p.relative_to(root).as_posix())
            continue
        body = re.sub(r"^---.*?---\s*", "", text, flags=re.S)
        body = re.sub(r"```.*?```", "", body, flags=re.S)
        non_heading = [ln.strip() for ln in body.splitlines() if ln.strip() and not ln.lstrip().startswith("#")]
        if len(non_heading) < 3 or re.search(r"\b(TODO|FIXME|placeholder|under construction|to be added|coming soon)\b", body, re.I):
            placeholder.append(p.relative_to(root).as_posix())

    duplicate_names = {
        stem: [x.relative_to(root).as_posix() for x in paths]
        for stem, paths in by_stem.items()
        if len(paths) > 1
    }

    substantive_orphans = []
    excluded = {
        "readme", "index", "chapter_index", "knowledge_map",
        "coverage_dashboard", "master_curriculum", "change_log"
    }
    for p in files:
        rel = p.relative_to(root).as_posix()
        if p.stem.lower() in excluded:
            continue
        text = p.read_text(encoding="utf-8", errors="ignore").strip()
        if len(text) < 400:
            continue
        if not incoming.get(p):
            substantive_orphans.append(rel)

    print("=== CURRICULUM-VAULT MAINTENANCE CHECKS ===")
    print(f"Markdown files: {len(files)}")
    print(f"Wikilinks: {len(links)}")
    print(f"Broken wikilinks: {len(broken)}")
    print(f"Empty Markdown: {len(empty)}")
    print(f"Placeholder candidates: {len(placeholder)}")
    print(f"Duplicate stem groups: {len(duplicate_names)}")
    print(f"Substantive orphan candidates: {len(substantive_orphans)}")

    for label, items in (("BROKEN", broken), ("EMPTY", empty), ("PLACEHOLDER", placeholder), ("ORPHAN", substantive_orphans)):
        print(f"\n[{label}]")
        for item in items[:200]:
            print(item if isinstance(item, str) else " -> ".join(item))
        if len(items) > 200:
            print(f"... {len(items)-200} more")

    print("\n[DUPLICATE STEM GROUPS]")
    for stem, paths in sorted(duplicate_names.items()):
        print(stem + ": " + " | ".join(paths))

    return 0


if __name__ == "__main__":
    raise SystemExit(main(sys.argv[1] if len(sys.argv) > 1 else "."))
