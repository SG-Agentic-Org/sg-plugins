#!/usr/bin/env python3
"""mnemaos-mcp indexer — builds the derived search index for a vault.

Standard library only (sqlite3 with FTS5). The index is derived data:
delete it any time; --rebuild recreates it from the vault.

Usage:
    python3 indexer.py <vault> [--db PATH] [--rebuild] [--quiet]
"""
import argparse
import hashlib
import os
import re
import sqlite3
import sys
import time

SCHEMA_VERSION = "1"
CORE_BASENAMES = {"_start-here.md", "profile.md", "decisions.md", "lessons.md", "inbox.md", "README.md"}
CARD_DIRS = {"people", "cards", "Wiki", "wiki"}
EXCLUDED_DIRS = {".mnemaos", "_mnemaos_backup", "node_modules"}
EXCLUDED_FILES = {"_index.md"}
CHUNK_MAX = 2000

_FM_RE = re.compile(r"\A---\s*\n(.*?)\n---\s*\n?", re.DOTALL)


def parse_frontmatter(text):
    """Tiny flat YAML-subset parser: 'key: value' and 'key: [a, b]'. Returns (dict, body)."""
    m = _FM_RE.match(text)
    if not m:
        return {}, text
    fm = {}
    for line in m.group(1).splitlines():
        line = line.rstrip()
        if not line or line.startswith("#") or line.startswith(" ") or ":" not in line:
            continue
        key, _, val = line.partition(":")
        key, val = key.strip(), val.strip()
        if val.startswith("[") and val.endswith("]"):
            items = [v.strip().strip("'\"") for v in val[1:-1].split(",")]
            fm[key] = [v for v in items if v]
        else:
            fm[key] = val.strip("'\"")
    return fm, text[m.end():]


def default_db_path(vault):
    return os.path.join(vault, ".mnemaos", "index.db")


def open_db(db_path):
    os.makedirs(os.path.dirname(db_path), exist_ok=True)
    conn = sqlite3.connect(db_path)
    conn.execute("PRAGMA journal_mode=WAL")
    conn.executescript(
        """
        CREATE TABLE IF NOT EXISTS meta (key TEXT PRIMARY KEY, value TEXT);
        CREATE TABLE IF NOT EXISTS docs (
          id TEXT PRIMARY KEY, path TEXT NOT NULL, kind TEXT NOT NULL,
          type TEXT, title TEXT, status TEXT,
          private INTEGER NOT NULL DEFAULT 0,
          created TEXT, updated TEXT,
          mtime REAL NOT NULL, hash TEXT NOT NULL
        );
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks USING fts5(
          title, heading, content, doc UNINDEXED,
          tokenize='unicode61 remove_diacritics 2'
        );
        """
    )
    return conn


def classify(relpath):
    """Return doc kind: card | core | working (see CONTRACTS.md §2)."""
    parts = relpath.split(os.sep)
    base = parts[-1]
    if len(parts) == 1 and base in CORE_BASENAMES:
        return "core"
    if base == "README.md" and len(parts) == 3 and parts[0] == "projects":
        return "core"  # a project's README
    if len(parts) == 2 and parts[0] in CARD_DIRS:
        return "card"
    if len(parts) == 2 and parts[0] == "projects":
        return "card"  # projects/<slug>.md
    return "working"


def walk_vault(vault):
    for root, dirs, files in os.walk(vault):
        dirs[:] = sorted(d for d in dirs if not d.startswith(".") and d not in EXCLUDED_DIRS)
        for name in sorted(files):
            if not name.endswith(".md") or name in EXCLUDED_FILES or name.startswith("."):
                continue
            full = os.path.join(root, name)
            yield os.path.relpath(full, vault), full


def chunk_body(body):
    """Split at ## headings; cap chunk size on paragraph boundaries."""
    sections, heading, buf = [], "", []
    for line in body.splitlines():
        if line.startswith("## "):
            if buf:
                sections.append((heading, "\n".join(buf).strip()))
            heading, buf = line[3:].strip(), []
        else:
            buf.append(line)
    sections.append((heading, "\n".join(buf).strip()))

    chunks = []
    for head, text in sections:
        if not text and not head:
            continue
        if len(text) <= CHUNK_MAX:
            chunks.append((head, text))
            continue
        piece = ""
        for para in text.split("\n\n"):
            if piece and len(piece) + len(para) + 2 > CHUNK_MAX:
                chunks.append((head, piece.strip()))
                piece = para
            else:
                piece = (piece + "\n\n" + para) if piece else para
        if piece.strip():
            chunks.append((head, piece.strip()))
    return [(h, t) for h, t in chunks if t]


def _truthy(val):
    return str(val).strip().lower() in ("true", "yes", "1")


def index_vault(vault, db_path=None, rebuild=False, only_paths=None, quiet=True):
    """Index the vault incrementally. Returns stats dict.

    only_paths: optional iterable of vault-relative paths to (re)index — used by
    memory_write for a single-file refresh. Deletion detection is skipped then.
    """
    vault = os.path.abspath(vault)
    if not os.path.isdir(vault):
        raise SystemExit("vault not found: %s" % vault)
    db_path = db_path or default_db_path(vault)
    if rebuild and os.path.exists(db_path):
        os.remove(db_path)
        for suffix in ("-wal", "-shm"):
            p = db_path + suffix
            if os.path.exists(p):
                os.remove(p)
    conn = open_db(db_path)
    cur = conn.cursor()

    existing = {row[0]: (row[1], row[2]) for row in cur.execute("SELECT path, mtime, hash FROM docs")}
    seen, added, changed, removed = set(), 0, 0, 0

    if only_paths is not None:
        files = [(rp, os.path.join(vault, rp)) for rp in only_paths]
    else:
        files = list(walk_vault(vault))

    for relpath, full in files:
        if not os.path.exists(full):
            continue
        seen.add(relpath)
        mtime = os.path.getmtime(full)
        with open(full, "r", encoding="utf-8", errors="replace") as f:
            text = f.read()
        digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
        prev = existing.get(relpath)
        if prev and prev[1] == digest:
            continue

        fm, body = parse_frontmatter(text)
        kind = classify(relpath)
        base = os.path.splitext(os.path.basename(relpath))[0]
        if kind == "card":
            doc_id = fm.get("id", base)
            dtype = fm.get("type", "note")
            title = fm.get("title", base)
        else:
            doc_id = relpath
            dtype = kind
            title = fm.get("title", base if base != "README" else os.path.dirname(relpath) or "README")

        cur.execute("DELETE FROM chunks WHERE doc IN (SELECT id FROM docs WHERE path=?)", (relpath,))
        cur.execute("DELETE FROM docs WHERE path=?", (relpath,))
        cur.execute(
            "INSERT OR REPLACE INTO docs (id, path, kind, type, title, status, private, created, updated, mtime, hash)"
            " VALUES (?,?,?,?,?,?,?,?,?,?,?)",
            (doc_id, relpath, kind, dtype, title, fm.get("status"),
             1 if _truthy(fm.get("private", "")) else 0,
             fm.get("created"), fm.get("updated"), mtime, digest),
        )
        for heading, content in chunk_body(body):
            cur.execute("INSERT INTO chunks (title, heading, content, doc) VALUES (?,?,?,?)",
                        (title, heading, content, doc_id))
        if prev:
            changed += 1
        else:
            added += 1

    if only_paths is None:
        for relpath in set(existing) - seen:
            cur.execute("DELETE FROM chunks WHERE doc IN (SELECT id FROM docs WHERE path=?)", (relpath,))
            cur.execute("DELETE FROM docs WHERE path=?", (relpath,))
            removed += 1

    if added or changed or removed or rebuild:
        cur.execute("INSERT OR REPLACE INTO meta VALUES ('schema_version', ?)", (SCHEMA_VERSION,))
        cur.execute("INSERT OR REPLACE INTO meta VALUES ('vault_path', ?)", (vault,))
        cur.execute("INSERT OR REPLACE INTO meta VALUES ('last_indexed', ?)",
                    (time.strftime("%Y-%m-%dT%H:%M:%S"),))
    conn.commit()

    n_docs = cur.execute("SELECT COUNT(*) FROM docs").fetchone()[0]
    n_chunks = cur.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
    conn.close()
    stats = {"added": added, "changed": changed, "removed": removed,
             "docs": n_docs, "chunks": n_chunks, "db": db_path}
    if not quiet:
        print("indexed %(docs)d docs / %(chunks)d chunks (+%(added)d ~%(changed)d -%(removed)d) -> %(db)s" % stats)
    return stats


def main():
    ap = argparse.ArgumentParser(description="Build/refresh the vault search index (derived data).")
    ap.add_argument("vault")
    ap.add_argument("--db", default=None)
    ap.add_argument("--rebuild", action="store_true", help="delete and rebuild from scratch")
    ap.add_argument("--quiet", action="store_true")
    args = ap.parse_args()
    index_vault(args.vault, db_path=args.db, rebuild=args.rebuild, quiet=args.quiet)


if __name__ == "__main__":
    main()
