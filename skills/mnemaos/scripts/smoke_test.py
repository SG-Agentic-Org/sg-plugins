#!/usr/bin/env python3
"""
smoke_test.py — structural check for a GENERATED MnemaOS vault.

Runs in a clean environment with only the Python standard library. No network, no
third-party packages. Point it at a vault that onboarding generated for a user — NOT at the
package's own template/reference files (those legitimately contain {{placeholders}}).

Usage:
    python3 smoke_test.py <path-to-generated-vault>

Checks:
  1. Required vault files exist (_start-here.md, profile.md, _index.md, inbox.md,
     decisions.md, lessons.md, README.md).
  2. Every card under people/ projects/ cards/ Wiki/ has valid frontmatter (required
     fields present; id == filename; type is valid).
  3. No unresolved {{placeholder}} tokens remain in any generated file.
  4. No leaked reference-implementation names/paths (a configurable leak list).
  5. No inlined secret VALUES (sk-..., Bearer ..., long assigned tokens) in any text/config file
     ANYWHERE in the vault, including the _mnemaos_backup/ folder and common credential files
     (.env, .json, .ini, .cfg, .toml). Binaries (.docx/.pdf/images) are out of scope (stdlib grep).
  6. No broken [[wikilinks]]: every link target resolves to an existing card id or .md basename.
     This is checked directly (the indexer does NOT have to run first).
  7. _index.md, if present, is consistent: no 'problems found' section and no link to a
     non-existent card.

Exits 0 if all pass, 1 otherwise. Prints a human-readable report.

The leak list defaults to a set of reference-implementation markers. Override or extend it
with --leak-terms "term1,term2" (comma-separated). Use --no-default-leaks to start empty.
"""

import argparse
import os
import re
import sys

REQUIRED_FILES = [
    "_start-here.md", "profile.md", "_index.md", "inbox.md",
    "decisions.md", "lessons.md", "README.md",
]
REQUIRED_FIELDS = ["id", "type", "title", "created", "updated", "status"]
VALID_TYPES = {"person", "project", "concept", "decision", "note"}
CARD_DIRS = ("people", "projects", "cards", "Wiki")

PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")
WIKILINK_RE = re.compile(r"\[\[([^\]]+)\]\]")

# Default reference-implementation leak markers. Case-insensitive substrings that must NOT
# appear in a GENERATED user vault — they would mean a private reference setup leaked in.
# Keep this list to markers that uniquely identify the private stack, NOT generic third-party
# tools a real user might legitimately use (e.g. Todoist, Obsidian, ChatGPT). Generic tools
# would false-positive on the user's own migrated content. Extend with --leak-terms for a
# specific build's private markers.
DEFAULT_LEAK_TERMS = [
    "Cowork", "MemPalace", "mempalace",
    "/Users/sashaglibiciuc", "Интурист", "glibiciuc",
]

# In adopt-existing-folder mode, these subpaths hold the USER'S OWN migrated content (working
# files, archive, raw sources) — not generated files. The leak/placeholder scan skips them
# (the secret scan still covers everything). A path matches if any of these segments appears.
USER_CONTENT_SEGMENTS = ("_mnemaos_backup", "/files/", "/archive/", "archive/", "RAW/")

SECRET_VALUE_RES = [
    re.compile(r"sk-[A-Za-z0-9]{16,}"),
    re.compile(r"\bBearer\s+[A-Za-z0-9._\-]{16,}"),
    re.compile(r"\bghp_[A-Za-z0-9]{16,}"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"AKIA[0-9A-Z]{16}"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
]
ASSIGN_SECRET_RE = re.compile(
    # key, then an optional closing quote + whitespace (so a quoted JSON key like
    # "api_key": "<token>" matches, not only bare api_key=<token>), then : or =, then value.
    r"(?i)\b(token|secret|api[_-]?key|password|passwd|access[_-]?key)\b['\"]?\s*[:=]\s*"
    r"['\"]?([A-Za-z0-9._\-]{20,})['\"]?"
)
SAFE_VALUE_HINTS = ("your-token", "your_token", "example", "changeme", "placeholder", "xxxx")


def read(path):
    # Tolerant read: config files in a migrated folder may not be valid UTF-8. Replace bad
    # bytes rather than crash — the secret regexes still match on the readable parts.
    with open(path, "r", encoding="utf-8", errors="replace") as f:
        return f.read()


def parse_frontmatter(text):
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
        data[key.strip()] = val.strip().strip("'\"")
    return data


# Text/markdown files the leak + placeholder + link scans look at (vault content is Markdown).
SCAN_EXTS = (".md", ".yaml", ".yml", ".txt")

# The SECRET scan is broader: it also covers the config/env file types that most often carry a
# real credential in a migrated work folder (.env, .json, .ini, .cfg, .toml). A leaked key in
# any of these is the exact case the backup-scan must guard. Kept to text-readable types only;
# binaries (.docx/.pdf/images) are out of scope for a stdlib-only grep and are not claimed.
SECRET_SCAN_EXTS = SCAN_EXTS + (".env", ".json", ".ini", ".cfg", ".conf", ".toml", ".properties")


def _is_secret_scannable(fn):
    # .endswith covers dotfiles like ".env" and "prod.env"; also catch a bare "env" config file.
    return fn.endswith(SECRET_SCAN_EXTS) or fn == "env"


def iter_md(folder):
    """Generated-content files: skips the backup (user's own pre-migration content)."""
    for root, _dirs, files in os.walk(folder):
        if "_mnemaos_backup" in root:
            continue
        for fn in files:
            if fn.endswith(SCAN_EXTS):
                yield os.path.join(root, fn)


def iter_all(folder):
    """EVERY text/config file in the vault, including _mnemaos_backup — for the secret scan,
    which must cover the backup and common credential files (.env/.json/...) too."""
    for root, _dirs, files in os.walk(folder):
        for fn in files:
            if _is_secret_scannable(fn):
                yield os.path.join(root, fn)


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("vault")
    ap.add_argument("--leak-terms", default="")
    ap.add_argument("--no-default-leaks", action="store_true")
    args = ap.parse_args()

    vault = os.path.abspath(os.path.expanduser(args.vault))
    failures = []
    notes = []

    if not os.path.isdir(vault):
        print(f"FAIL: not a directory: {vault}")
        return 1

    leak_terms = [] if args.no_default_leaks else list(DEFAULT_LEAK_TERMS)
    if args.leak_terms:
        leak_terms += [t.strip() for t in args.leak_terms.split(",") if t.strip()]
    leak_lower = [t.lower() for t in leak_terms]

    # 1. required files
    for name in REQUIRED_FILES:
        if not os.path.isfile(os.path.join(vault, name)):
            failures.append(f"missing required file: {name}")

    # 2. card frontmatter
    known_ids = set()
    cards = []
    for sub in CARD_DIRS:
        d = os.path.join(vault, sub)
        if not os.path.isdir(d):
            continue
        for root, _dirs, files in os.walk(d):
            for fn in files:
                if not fn.endswith(".md"):
                    continue
                p = os.path.join(root, fn)
                # A card is a .md DIRECTLY in the card dir; files nested deeper (e.g.
                # projects/<slug>/files/working.md) are working files, not cards.
                if os.path.dirname(os.path.relpath(p, d)) != "":
                    continue
                base = fn[:-3]
                fm = parse_frontmatter(read(p))
                cards.append((os.path.relpath(p, vault), fm, base))
                known_ids.add(base)
                if fm.get("id"):
                    known_ids.add(fm["id"])

    for rel, fm, base in cards:
        if not fm:
            failures.append(f"{rel}: card has no frontmatter")
            continue
        for field in REQUIRED_FIELDS:
            if not fm.get(field):
                failures.append(f"{rel}: missing required frontmatter field '{field}'")
        if fm.get("type") and fm["type"] not in VALID_TYPES:
            failures.append(f"{rel}: invalid type '{fm['type']}'")
        if fm.get("id") and fm["id"] != base:
            failures.append(f"{rel}: id '{fm['id']}' != filename '{base}'")
        # slug must be lowercase kebab-case (the contract mandates it); catches Cyrillic /
        # spaces / uppercase slugs even when id == filename.
        if base and not re.fullmatch(r"[a-z0-9][a-z0-9-]*", base):
            failures.append(f"{rel}: card slug '{base}' is not lowercase kebab-case")

    # 3 + 4: leak + placeholder checks apply to GENERATED files only (skip the backup and the
    # user's own migrated content, which legitimately mention generic tools / had placeholders).
    for p in iter_md(vault):
        rel = os.path.relpath(p, vault)
        relslash = "/" + rel.replace(os.sep, "/")
        is_user_content = any(seg in relslash for seg in USER_CONTENT_SEGMENTS)
        if is_user_content:
            continue
        content = read(p)
        for m in PLACEHOLDER_RE.finditer(content):
            failures.append(f"unresolved placeholder {m.group(0)} in {rel}")
        for term, low in zip(leak_terms, leak_lower):
            if low in content.lower():
                failures.append(f"leaked reference-implementation term '{term}' in {rel}")

    # 5: secret scan covers EVERY text file in the vault, including _mnemaos_backup.
    for p in iter_all(vault):
        rel = os.path.relpath(p, vault)
        content = read(p)
        for rx in SECRET_VALUE_RES:
            m = rx.search(content)
            if m:
                failures.append(f"possible inlined secret value in {rel}: {m.group(0)[:12]}...")
        for m in ASSIGN_SECRET_RE.finditer(content):
            val = m.group(2)
            low = val.lower()
            if any(h in low for h in SAFE_VALUE_HINTS):
                continue
            if re.fullmatch(r"[A-Z][A-Z0-9_]+", val):
                continue
            failures.append(f"looks like an inlined secret in {rel}: {m.group(1)}=...")

    # 6: broken wikilinks — checked DIRECTLY, no prior index_vault.py run required. Resolution
    # follows Obsidian semantics: a [[link]] may target any card id OR any .md basename in the
    # vault. Build the full basename set first (mirrors index_vault.py), then scan every
    # generated .md file's links. _index.md and user-content paths are skipped as sources.
    link_targets = set(known_ids)
    for p in iter_md(vault):
        if p.endswith(".md"):
            link_targets.add(os.path.basename(p)[:-3])
    for p in iter_md(vault):
        if not p.endswith(".md"):
            continue
        rel = os.path.relpath(p, vault)
        if rel == "_index.md":
            continue  # generated output, validated separately in step 7
        relslash = "/" + rel.replace(os.sep, "/")
        if any(seg in relslash for seg in USER_CONTENT_SEGMENTS):
            continue  # user's own migrated notes may link anywhere; not our contract to enforce
        for m in WIKILINK_RE.finditer(read(p)):
            target = m.group(1).split("|")[0].split("#")[0].strip()
            if target and target not in link_targets:
                failures.append(f"{rel}: broken link [[{target}]]")

    # 7: index consistency
    idx_path = os.path.join(vault, "_index.md")
    if os.path.isfile(idx_path):
        idx = read(idx_path)
        if "problems found" in idx.lower():
            failures.append("_index.md contains a 'problems found' section — re-run index_vault.py and fix")
        for m in WIKILINK_RE.finditer(idx):
            target = m.group(1).split("|")[0].split("#")[0].strip()
            if target and target not in known_ids:
                failures.append(f"_index.md references non-existent card [[{target}]]")

    # report
    print(f"Smoke test: {vault}")
    print(f"  leak terms checked: {len(leak_terms)}; cards checked: {len(cards)}")
    for n in notes:
        print(f"  note: {n}")
    if failures:
        print(f"\nRESULT: FAIL ({len(failures)} issue(s))")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\nRESULT: PASS — structure, frontmatter, placeholders, leak, secret, links, index all clear.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
