#!/usr/bin/env python3
"""mnemaos-mcp server — serves a vault's memory over MCP.

Standard library only. Two transports from one code base:
  stdio (local):   python3 server.py --vault <path>
  HTTP  (remote):  MNEMAOS_TOKEN=... python3 server.py --vault <path> --http 127.0.0.1:8765

See CONTRACTS.md for the tool contract and privacy rules.
"""
import argparse
import datetime
import json
import os
import re
import sqlite3
import sys
import threading

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
import gate
import indexer

PROTOCOL_VERSION = "2024-11-05"
SERVER_INFO = {"name": "mnemaos-mcp", "version": "1.0.0"}
CONTEXT_FILE_BUDGET = 4000  # chars per core file in memory_context


# ---------------------------------------------------------------- tool schemas

TOOLS = [
    {
        "name": "memory_context",
        "description": ("Session bootstrap: who the user is, what is active, how to work with them. "
                        "Call once at the start of a session. Returns the vault entry point, a profile "
                        "excerpt, the most recently updated cards, and vault stats."),
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
    {
        "name": "memory_search",
        "description": ("Full-text search over the memory vault (BM25). A miss does not mean the memory "
                        "does not exist — fall back to memory_list."),
        "inputSchema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "free-text query"},
                "k": {"type": "integer", "minimum": 1, "maximum": 25, "default": 8},
                "type": {"type": "string",
                          "enum": ["person", "project", "concept", "decision", "note", "core", "working"]},
            },
            "required": ["query"],
        },
    },
    {
        "name": "memory_get",
        "description": "Read one memory document in full by its id (card slug) or vault-relative path.",
        "inputSchema": {
            "type": "object",
            "properties": {"id": {"type": "string"}},
            "required": ["id"],
        },
    },
    {
        "name": "memory_list",
        "description": "List memory documents (most recently updated first). The deterministic fallback when search misses.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "type": {"type": "string",
                          "enum": ["person", "project", "concept", "decision", "note", "core", "working"]},
                "status": {"type": "string", "enum": ["active", "archived"]},
                "limit": {"type": "integer", "minimum": 1, "maximum": 200, "default": 50},
                "offset": {"type": "integer", "minimum": 0, "default": 0},
            },
        },
    },
    {
        "name": "memory_write",
        "description": ("Write durable memory into the vault (the only write tool; gated). "
                        "kind='card' creates an entity card; kind='episode' appends a dated entry to inbox.md. "
                        "Never put secret values in memory."),
        "inputSchema": {
            "type": "object",
            "properties": {
                "kind": {"type": "string", "enum": ["card", "episode"], "default": "card"},
                "type": {"type": "string", "enum": list(gate.CARD_TYPES), "default": "note"},
                "title": {"type": "string"},
                "body": {"type": "string"},
                "tags": {"type": "array", "items": {"type": "string"}},
                "links": {"type": "array", "items": {"type": "string"}},
                "private": {"type": "boolean", "default": False},
                "update": {"type": "boolean", "default": False,
                            "description": "allow overwriting an existing card with the same id"},
            },
            "required": ["body"],
        },
    },
    {
        "name": "memory_health",
        "description": "Index freshness, document counts, and serving mode. Use to detect a stale or empty index.",
        "inputSchema": {"type": "object", "properties": {}, "additionalProperties": False},
    },
]


# ---------------------------------------------------------------- memory core

class Memory:
    def __init__(self, vault, db_path=None, exclude_private=False, read_only=False, remote=False):
        self.vault = os.path.abspath(vault)
        if not os.path.isdir(self.vault):
            raise SystemExit("vault not found: %s — pass --vault with the folder that holds your memory" % self.vault)
        self.db_path = db_path or indexer.default_db_path(self.vault)
        self.read_only = read_only
        self.remote = remote
        # Privacy: remote transport always excludes private docs (no override up).
        self.exclude_private = exclude_private or remote
        self.write_lock = threading.Lock()
        if not os.path.exists(self.db_path):
            indexer.index_vault(self.vault, db_path=self.db_path)
            self.built_on_start = True
        else:
            self.built_on_start = False

    def _conn(self):
        conn = sqlite3.connect(self.db_path)
        conn.row_factory = sqlite3.Row
        return conn

    def _privacy_sql(self):
        return " AND private=0" if self.exclude_private else ""

    # -- tools ---------------------------------------------------------------

    def context(self):
        parts = []
        for name, label in (("_start-here.md", "ENTRY POINT"), ("profile.md", "PROFILE")):
            path = os.path.join(self.vault, name)
            if os.path.exists(path):
                if self.exclude_private and self._is_private_path(name):
                    continue
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    text = f.read().strip()
                if len(text) > CONTEXT_FILE_BUDGET:
                    text = text[:CONTEXT_FILE_BUDGET] + "\n…(truncated — memory_get('%s') for the rest)" % name
                parts.append("=== %s (%s) ===\n%s" % (label, name, text))
        conn = self._conn()
        rows = conn.execute(
            "SELECT id, type, title, updated FROM docs WHERE kind='card'%s "
            "ORDER BY COALESCE(updated, created, '') DESC, mtime DESC LIMIT 10" % self._privacy_sql()
        ).fetchall()
        if rows:
            lines = ["- %s [%s] — %s%s" % (r["id"], r["type"], r["title"],
                                            (" (updated %s)" % r["updated"]) if r["updated"] else "")
                     for r in rows]
            parts.append("=== RECENT CARDS ===\n" + "\n".join(lines))
        n_cards = conn.execute("SELECT COUNT(*) FROM docs WHERE kind='card'%s" % self._privacy_sql()).fetchone()[0]
        n_docs = conn.execute("SELECT COUNT(*) FROM docs WHERE 1=1%s" % self._privacy_sql()).fetchone()[0]
        last = conn.execute("SELECT value FROM meta WHERE key='last_indexed'").fetchone()
        conn.close()
        parts.append("=== VAULT ===\n%d cards, %d documents indexed. Last indexed: %s.\n"
                     "Details on demand: memory_search / memory_list / memory_get."
                     % (n_cards, n_docs, last[0] if last else "never"))
        if not parts:
            return "The vault is empty or has no entry point yet. Use memory_write to start it."
        return "\n\n".join(parts)

    def _is_private_path(self, relpath):
        conn = self._conn()
        row = conn.execute("SELECT private FROM docs WHERE path=?", (relpath,)).fetchone()
        conn.close()
        return bool(row and row["private"])

    @staticmethod
    def _fts_query(query):
        tokens = re.findall(r"\w+", query, re.UNICODE)
        return " ".join('"%s"' % t for t in tokens) if tokens else None

    def search(self, query, k=8, type=None):
        fts = self._fts_query(query)
        if not fts:
            return "Empty query."
        k = max(1, min(int(k or 8), 25))
        conn = self._conn()
        params = {"q": fts, "k": k}
        sql = (
            "SELECT c.doc, d.type, d.title, c.heading, "
            "snippet(chunks, 2, '>>', '<<', ' … ', 18) AS snip, "
            "bm25(chunks, 4.0, 2.0, 1.0) AS rank "
            "FROM chunks c JOIN docs d ON d.id = c.doc "
            "WHERE chunks MATCH :q%s%s ORDER BY rank LIMIT :k"
        ) % ((" AND d.private=0" if self.exclude_private else ""),
             (" AND d.type=:t" if type else ""))
        if type:
            params["t"] = type
        try:
            rows = conn.execute(sql, params).fetchall()
        except sqlite3.OperationalError as e:
            conn.close()
            return "Search error: %s" % e
        if not rows:
            # AND miss -> OR retry
            or_q = " OR ".join('"%s"' % t for t in re.findall(r"\w+", query, re.UNICODE))
            params["q"] = or_q
            rows = conn.execute(sql, params).fetchall()
        conn.close()
        if not rows:
            return ("No results for %r. A search miss does not mean the memory is absent — "
                    "try memory_list or different words." % query)
        seen, out = set(), []
        for r in rows:
            key = (r["doc"], r["heading"])
            if key in seen:
                continue
            seen.add(key)
            head = (" › %s" % r["heading"]) if r["heading"] else ""
            out.append("%s [%s] — %s%s\n  %s" % (r["doc"], r["type"], r["title"], head,
                                                  r["snip"].replace("\n", " ")))
        return "\n\n".join(out)

    def get(self, doc_id):
        conn = self._conn()
        row = conn.execute("SELECT * FROM docs WHERE (id=? OR path=?)%s" % self._privacy_sql(),
                           (doc_id, doc_id)).fetchall()
        if not row:
            near = conn.execute(
                "SELECT id FROM docs WHERE id LIKE ?%s LIMIT 5" % self._privacy_sql(),
                ("%" + doc_id.strip().replace(" ", "-").lower() + "%",)).fetchall()
            conn.close()
            hint = (" Closest ids: " + ", ".join(r["id"] for r in near)) if near else ""
            raise ToolError("no document with id or path %r.%s" % (doc_id, hint))
        conn.close()
        path = os.path.join(self.vault, row[0]["path"])
        with open(path, "r", encoding="utf-8", errors="replace") as f:
            return f.read()

    def list(self, type=None, status=None, limit=50, offset=0):
        limit = max(1, min(int(limit or 50), 200))
        offset = max(0, int(offset or 0))
        conn = self._conn()
        where, params = ["1=1"], {}
        if self.exclude_private:
            where.append("private=0")
        if type:
            where.append("type=:t")
            params["t"] = type
        if status:
            where.append("status=:s")
            params["s"] = status
        params.update({"lim": limit, "off": offset})
        rows = conn.execute(
            "SELECT id, kind, type, title, status, updated, path FROM docs WHERE %s "
            "ORDER BY COALESCE(updated, created, '') DESC, mtime DESC LIMIT :lim OFFSET :off"
            % " AND ".join(where), params).fetchall()
        total = conn.execute("SELECT COUNT(*) FROM docs WHERE %s" % " AND ".join(where), params).fetchone()[0]
        conn.close()
        if not rows:
            return "No documents match the filter."
        lines = ["%s [%s/%s] — %s%s" % (r["id"], r["kind"], r["type"], r["title"],
                                         (" (%s)" % r["status"]) if r["status"] else "")
                 for r in rows]
        return "%d of %d:\n" % (len(rows), total) + "\n".join(lines)

    def write(self, payload):
        if self.read_only:
            raise ToolError("this server runs read-only (--read-only); writes are disabled")
        errors, norm = gate.validate_write(payload)
        if errors:
            raise ToolError("gate rejected the write: " + "; ".join(errors))
        with self.write_lock:
            if norm["kind"] == "episode":
                relpath = "inbox.md"
                path = os.path.join(self.vault, relpath)
                stamp = datetime.date.today().isoformat()
                entry = "\n## %s\n\n%s\n" % (stamp, norm["body"])
                with open(path, "a", encoding="utf-8") as f:
                    f.write(entry)
                indexer.index_vault(self.vault, db_path=self.db_path, only_paths=[relpath])
                return "Episode appended to inbox.md (%s)." % stamp

            slug = norm["slug"]
            folder = {"person": "people", "project": "projects"}.get(norm["type"], "cards")
            relpath = os.path.join(folder, slug + ".md")
            path = os.path.join(self.vault, relpath)
            if os.path.exists(path) and not norm["update"]:
                raise ToolError(
                    "a card with id %r already exists (%s). Read it with memory_get('%s'); "
                    "pass update=true to overwrite deliberately." % (slug, relpath, slug))
            today = datetime.date.today().isoformat()
            created = today
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8", errors="replace") as f:
                    old_fm, _ = indexer.parse_frontmatter(f.read())
                created = old_fm.get("created", today)
            fm_lines = [
                "---",
                "id: %s" % slug,
                "type: %s" % norm["type"],
                "title: %s" % norm["title"],
                "created: %s" % created,
                "updated: %s" % today,
                "status: active",
                "tags: [%s]" % ", ".join(norm["tags"]),
                "links: [%s]" % ", ".join(norm["links"]),
            ]
            if norm["private"]:
                fm_lines.append("private: true")
            fm_lines.append("---")
            content = "\n".join(fm_lines) + "\n\n# %s\n\n%s\n" % (norm["title"], norm["body"])
            os.makedirs(os.path.dirname(path), exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            indexer.index_vault(self.vault, db_path=self.db_path, only_paths=[relpath])
            return "Card written: %s (id: %s)%s." % (relpath, slug,
                                                      ", private" if norm["private"] else "")

    def health(self):
        conn = self._conn()
        meta = {r["key"]: r["value"] for r in conn.execute("SELECT key, value FROM meta")}
        n_docs = conn.execute("SELECT COUNT(*) FROM docs").fetchone()[0]
        n_cards = conn.execute("SELECT COUNT(*) FROM docs WHERE kind='card'").fetchone()[0]
        n_chunks = conn.execute("SELECT COUNT(*) FROM chunks").fetchone()[0]
        n_private = conn.execute("SELECT COUNT(*) FROM docs WHERE private=1").fetchone()[0]
        stale = 0
        for relpath, full in indexer.walk_vault(self.vault):
            row = conn.execute("SELECT hash, mtime FROM docs WHERE path=?", (relpath,)).fetchone()
            if row is None or os.path.getmtime(full) > row["mtime"] + 1e-6:
                stale += 1
        conn.close()
        db_size = os.path.getsize(self.db_path) if os.path.exists(self.db_path) else 0
        return "\n".join([
            "vault: %s" % self.vault,
            "index: %s (%.1f MB, schema %s)" % (self.db_path, db_size / 1e6, meta.get("schema_version", "?")),
            "last indexed: %s%s" % (meta.get("last_indexed", "never"),
                                     " (built on this start)" if self.built_on_start else ""),
            "documents: %d (%d cards, %d private), chunks: %d" % (n_docs, n_cards, n_private, n_chunks),
            "files changed since last index: %d%s" % (stale, " — run indexer.py to refresh" if stale else ""),
            "mode: %s%s%s" % ("remote (HTTP)" if self.remote else "local (stdio)",
                               ", private excluded" if self.exclude_private else ", private included",
                               ", read-only" if self.read_only else ""),
        ])


class ToolError(Exception):
    pass


# ---------------------------------------------------------------- JSON-RPC

def handle_message(memory, msg):
    """Handle one JSON-RPC message. Returns a response dict or None (notification)."""
    method = msg.get("method")
    msg_id = msg.get("id")
    params = msg.get("params") or {}

    def ok(result):
        return {"jsonrpc": "2.0", "id": msg_id, "result": result}

    def err(code, message):
        return {"jsonrpc": "2.0", "id": msg_id, "error": {"code": code, "message": message}}

    if method == "initialize":
        client_proto = params.get("protocolVersion") or PROTOCOL_VERSION
        return ok({"protocolVersion": client_proto,
                   "capabilities": {"tools": {}},
                   "serverInfo": SERVER_INFO})
    if method in ("notifications/initialized", "notifications/cancelled"):
        return None
    if method == "ping":
        return ok({})
    if method == "tools/list":
        return ok({"tools": TOOLS})
    if method == "tools/call":
        name = params.get("name")
        args = params.get("arguments") or {}
        try:
            if name == "memory_context":
                text = memory.context()
            elif name == "memory_search":
                text = memory.search(args.get("query", ""), args.get("k", 8), args.get("type"))
            elif name == "memory_get":
                text = memory.get(args.get("id", ""))
            elif name == "memory_list":
                text = memory.list(args.get("type"), args.get("status"),
                                   args.get("limit", 50), args.get("offset", 0))
            elif name == "memory_write":
                text = memory.write(args)
            elif name == "memory_health":
                text = memory.health()
            else:
                return err(-32602, "unknown tool: %r" % name)
            return ok({"content": [{"type": "text", "text": text}], "isError": False})
        except ToolError as e:
            return ok({"content": [{"type": "text", "text": "Error: %s" % e}], "isError": True})
        except Exception as e:  # defensive: a tool bug must not kill the server
            return ok({"content": [{"type": "text", "text": "Internal error: %s" % e}], "isError": True})
    if msg_id is None:
        return None  # unknown notification — ignore per JSON-RPC
    return err(-32601, "method not found: %r" % method)


def serve_stdio(memory):
    for line in sys.stdin:
        line = line.strip()
        if not line:
            continue
        try:
            msg = json.loads(line)
        except ValueError:
            sys.stdout.write(json.dumps({"jsonrpc": "2.0", "id": None,
                                         "error": {"code": -32700, "message": "parse error"}}) + "\n")
            sys.stdout.flush()
            continue
        resp = handle_message(memory, msg)
        if resp is not None:
            sys.stdout.write(json.dumps(resp, ensure_ascii=False) + "\n")
            sys.stdout.flush()


def serve_http(memory, host, port, token):
    from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer

    class Handler(BaseHTTPRequestHandler):
        def log_message(self, fmt, *args):
            sys.stderr.write("%s - %s\n" % (self.address_string(), fmt % args))

        def _send(self, code, body=b"", ctype="application/json"):
            self.send_response(code)
            self.send_header("Content-Type", ctype)
            self.send_header("Content-Length", str(len(body)))
            self.end_headers()
            if body:
                self.wfile.write(body)

        def do_GET(self):
            if self.path == "/health":
                self._send(200, b"ok", "text/plain")
            else:
                self._send(404, b"not found", "text/plain")

        def do_POST(self):
            if self.path not in ("/mcp", "/"):
                self._send(404, b"not found", "text/plain")
                return
            auth = self.headers.get("Authorization", "")
            if auth != "Bearer %s" % token:
                self._send(401, b'{"error":"unauthorized"}')
                return
            try:
                length = int(self.headers.get("Content-Length", 0))
                msg = json.loads(self.rfile.read(length).decode("utf-8"))
            except (ValueError, KeyError):
                self._send(400, json.dumps({"jsonrpc": "2.0", "id": None,
                                            "error": {"code": -32700, "message": "parse error"}}).encode())
                return
            resp = handle_message(memory, msg)
            if resp is None:
                self._send(202)
            else:
                self._send(200, json.dumps(resp, ensure_ascii=False).encode("utf-8"))

    httpd = ThreadingHTTPServer((host, port), Handler)
    sys.stderr.write("mnemaos-mcp serving %s on http://%s:%d/mcp (private docs %s)\n"
                     % (memory.vault, host, port,
                        "EXCLUDED" if memory.exclude_private else "included"))
    httpd.serve_forever()


def main():
    ap = argparse.ArgumentParser(description="Serve a memory vault over MCP (stdio or HTTP).")
    ap.add_argument("--vault", required=True, help="path to the memory vault folder")
    ap.add_argument("--db", default=None, help="index path (default: <vault>/.mnemaos/index.db)")
    ap.add_argument("--http", default=None, metavar="HOST:PORT",
                    help="serve over HTTP instead of stdio (requires MNEMAOS_TOKEN)")
    ap.add_argument("--exclude-private", action="store_true",
                    help="exclude private:true docs even over stdio")
    ap.add_argument("--read-only", action="store_true", help="disable memory_write")
    ap.add_argument("--reindex", action="store_true", help="refresh the index before serving")
    args = ap.parse_args()

    remote = args.http is not None
    memory = Memory(args.vault, db_path=args.db, exclude_private=args.exclude_private,
                    read_only=args.read_only, remote=remote)
    if args.reindex:
        indexer.index_vault(memory.vault, db_path=memory.db_path)

    if remote:
        token = os.environ.get("MNEMAOS_TOKEN", "")
        if len(token) < 16:
            raise SystemExit("HTTP mode requires MNEMAOS_TOKEN (>=16 chars). "
                             "Generate one: python3 -c \"import secrets; print(secrets.token_urlsafe(32))\"")
        host, _, port = args.http.partition(":")
        serve_http(memory, host or "127.0.0.1", int(port or 8765), token)
    else:
        serve_stdio(memory)


if __name__ == "__main__":
    main()
