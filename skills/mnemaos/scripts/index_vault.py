#!/usr/bin/env python3
"""
index_vault.py — deterministic indexer for a MnemaOS vault.

Standard library only. No network, no third-party packages. Walks a vault, reads card
frontmatter, regenerates _index.md, and reports problems: cards missing required frontmatter
fields, and broken [[wikilinks]] that point at no existing card.

Usage:
    python3 index_vault.py <path-to-vault>

Exit code is 0 on a clean index, 1 if problems were found (the index is still written).
"""

import os
import re
import sys

REQUIRED_FIELDS = ["id", "type", "title", "created", "updated", "status"]
VALID_TYPES = {"person", "project", "concept", "decision", "note"}

# Folders whose .md files are cards we index. Top-level single files (decisions.md etc.)
# are logs, not cards, and are listed separately without frontmatter requirements.
CARD_DIRS = ("people", "projects", "cards", "Wiki")
LOG_FILES = ("decisions.md", "lessons.md", "inbox.md")
ENTRY_FILES = ("_start-here.md", "profile.md", "README.md")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def parse_frontmatter(text):
    """Return a dict of top-level scalar/list frontmatter, or {} if none. Minimal parser."""
    if not text.startswith("---"):
        return {}
    end = text.find("\n---", 3)
    if end == -1:
        return {}
    block = text[3:end].strip("\n")
    data = {}
    for line in block.splitlines():
        if not line.strip() or line.lstrip().startswith("#"):
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip()
        if val.startswith("[") and val.endswith("]"):
            inner = val[1:-1].strip()
            data[key] = [x.strip().strip("'\"") for x in inner.split(",") if x.strip()]
        else:
            data[key] = val.strip("'\"")
    return data


def is_card_path(vault, sub, p):
    """A card is a .md file DIRECTLY in people/, cards/, or Wiki/, OR a project card file
    directly in projects/ (projects/<slug>.md). Files nested deeper (e.g.
    projects/<slug>/files/working.md) are WORKING FILES, not cards, and are not validated."""
    parent = os.path.dirname(os.path.relpath(p, os.path.join(vault, sub)))
    return parent == ""  # directly inside the card dir, not in a subfolder


def find_cards(vault):
    cards = []  # (relpath, frontmatter, basename_no_ext)
    for sub in CARD_DIRS:
        d = os.path.join(vault, sub)
        if not os.path.isdir(d):
            continue
        for root, _dirs, files in os.walk(d):
            for fn in files:
                if not fn.endswith(".md"):
                    continue
                p = os.path.join(root, fn)
                if not is_card_path(vault, sub, p):
                    continue  # working file inside a project subfolder, not a card
                fm = parse_frontmatter(read(p))
                cards.append((os.path.relpath(p, vault), fm, fn[:-3]))
    return cards


def main():
    if len(sys.argv) != 2:
        print("usage: python3 index_vault.py <path-to-vault>")
        return 2
    vault = os.path.abspath(os.path.expanduser(sys.argv[1]))
    if not os.path.isdir(vault):
        print(f"FAIL: not a directory: {vault}")
        return 1

    problems = []
    cards = find_cards(vault)

    # all known card ids (by frontmatter id and by basename) for link resolution
    known_ids = set()
    for _rel, fm, base in cards:
        known_ids.add(base)
        if fm.get("id"):
            known_ids.add(fm["id"])

    # Obsidian semantics: a [[wikilink]] may target ANY .md file in the vault by basename,
    # not only a MnemaOS card. Add every .md basename so overlay-on-existing-vault links
    # (e.g. a bridge card pointing into the user's own notes/) resolve and are not flagged.
    for root, _dirs, files in os.walk(vault):
        if "_mnemaos_backup" in root:
            continue
        for fn in files:
            if fn.endswith(".md"):
                known_ids.add(fn[:-3])

    # validate frontmatter
    for rel, fm, base in cards:
        if not fm:
            problems.append(f"{rel}: no frontmatter")
            continue
        for field in REQUIRED_FIELDS:
            if field not in fm or fm[field] == "":
                problems.append(f"{rel}: missing required field '{field}'")
        if fm.get("type") and fm["type"] not in VALID_TYPES:
            problems.append(f"{rel}: invalid type '{fm['type']}'")
        if fm.get("id") and fm["id"] != base:
            problems.append(f"{rel}: id '{fm['id']}' != filename '{base}'")

    # broken wikilinks across all markdown
    for root, _dirs, files in os.walk(vault):
        if "_mnemaos_backup" in root:
            continue
        for fn in files:
            if not fn.endswith(".md"):
                continue
            p = os.path.join(root, fn)
            # _index.md is generated output, not user content — don't scan it for links
            if os.path.relpath(p, vault) == "_index.md":
                continue
            for m in WIKILINK_RE.finditer(read(p)):
                target = m.group(1).split("|")[0].split("#")[0].strip()
                if target and target not in known_ids:
                    rel = os.path.relpath(p, vault)
                    problems.append(f"{rel}: broken link [[{target}]]")

    # group cards by type for the index
    by_type = {}
    for rel, fm, base in cards:
        t = fm.get("type", "unknown")
        by_type.setdefault(t, []).append((fm.get("title", base), rel))

    lines = ["# Index", "", "> Auto-generated by index_vault.py. Do not edit by hand.", ""]
    for t in sorted(by_type):
        lines.append(f"## {t} ({len(by_type[t])})")
        for title, rel in sorted(by_type[t]):
            lines.append(f"- [[{os.path.splitext(os.path.basename(rel))[0]}]] — {title}")
        lines.append("")

    present_logs = [f for f in LOG_FILES if os.path.isfile(os.path.join(vault, f))]
    if present_logs:
        lines.append("## logs")
        for f in present_logs:
            lines.append(f"- {f}")
        lines.append("")

    if problems:
        lines.append("## problems found")
        for p in problems:
            lines.append(f"- {p}")
        lines.append("")

    with open(os.path.join(vault, "_index.md"), "w", encoding="utf-8") as f:
        f.write("\n".join(lines).rstrip() + "\n")

    total = len(cards)
    print(f"Indexed {total} card(s) in {vault}")
    if problems:
        print(f"RESULT: {len(problems)} problem(s) found (index written with a 'problems' section):")
        for p in problems:
            print(f"  - {p}")
        return 1
    print("RESULT: clean — no missing frontmatter, no broken links.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
