# mnemaos-mcp — contracts

This file fixes the interfaces of the MCP layer: the tools an LLM client sees, the
index database schema, and the memory-card schema extension. Everything else
(implementation details, chunking heuristics) may change; these contracts should not
change without a version bump in `meta.schema_version`.

Compatibility promise: **any existing MnemaOS vault indexes as-is.** The MCP layer is
an overlay — it never requires editing a single vault file. The vault stays the single
source of truth; the index is derived and can always be deleted and rebuilt with one
command.

## 1. Tools

Six tools. All results are returned as plain text (Markdown) so any MCP client can
render them.

### `memory_context()`
Session bootstrap in one call: "who is the user, what is active, how to work with them".

Returns, in order:
1. `_start-here.md` (the vault entry point), truncated to a budget.
2. A compact excerpt of `profile.md`.
3. The 10 most recently updated cards (id, type, title, updated).
4. Vault stats (cards / docs / last index time).

No arguments. Intended to be called once at session start by any connected LLM.

### `memory_search(query, k=8, type=null)`
Full-text search (SQLite FTS5, BM25-ranked; title and heading weighted above body).
- `query` — free text, any language the vault is written in.
- `k` — max results (1–25).
- `type` — optional filter: `person | project | concept | decision | note | core | working`.

Returns ranked snippets with `id`, `title`, `type`, and the matched excerpt. A miss
returns "no results" plus a hint to try `memory_list` — a semantic miss never means the
memory does not exist.

### `memory_get(id)`
Read one document in full.
- `id` — card id (slug) or vault-relative path.

Returns the full Markdown content including frontmatter. Unknown id → error listing
the closest matching ids.

### `memory_list(type=null, status=null, limit=50, offset=0)`
Deterministic listing (most recently updated first). The fallback when search misses.

### `memory_write(payload)`
**The only write tool.** Validated by the gate before anything touches disk; the gate
rejects inlined secrets and schema violations. Writes plain Markdown into the vault,
then incrementally reindexes the touched file.

Payload (JSON object):

```json
{
  "kind": "card",            // "card" | "episode"
  "type": "concept",          // card only: person|project|concept|decision|note
  "title": "Quarterly pricing rule",
  "body": "Markdown body…",
  "tags": ["pricing"],       // optional
  "links": ["acme-corp"],    // optional, ids of related cards
  "private": false,           // optional, see §3
  "update": false             // card only: allow overwriting an existing id
}
```

- `kind: "card"` → creates `cards/<slug>.md` (or `people/<slug>.md` for `type: person`,
  `projects/<slug>.md` for `type: project`) with contract frontmatter. If the id already
  exists and `update` is not `true` → error (no silent overwrite).
- `kind: "episode"` → appends a dated entry to `inbox.md` (only `body` required).

Gate checks (all hard failures): secret patterns in body/title; invalid `type`; empty
title/body; id not resolvable to a lowercase-kebab slug; card body over the size budget.

Disabled entirely when the server runs with `--read-only`.

### `memory_health()`
Index freshness (last index run, files changed since), doc/chunk counts, db size,
serving mode (local/remote, read-only, private included/excluded), schema version.
Lets a client — or a monitoring cron — see silent staleness.

## 2. Index database

One SQLite file: `<vault>/.mnemaos/index.db` (override with `--db`). WAL mode.
Derived data only — safe to delete at any time; `indexer.py --rebuild` recreates it.

```sql
CREATE TABLE meta   (key TEXT PRIMARY KEY, value TEXT);
-- keys: schema_version, vault_path, last_indexed (iso ts)

CREATE TABLE docs (
  id      TEXT PRIMARY KEY,   -- card slug, or vault-relative path for non-cards
  path    TEXT NOT NULL,      -- vault-relative path
  kind    TEXT NOT NULL,      -- card | core | working
  type    TEXT,               -- person|project|concept|decision|note (cards), core, working
  title   TEXT,
  status  TEXT,               -- active | archived | (null)
  private INTEGER NOT NULL DEFAULT 0,
  created TEXT, updated TEXT, -- from frontmatter when present
  mtime   REAL NOT NULL,      -- file mtime at index time
  hash    TEXT NOT NULL       -- sha256 of file content
);

CREATE VIRTUAL TABLE chunks USING fts5(
  title, heading, content, doc UNINDEXED,
  tokenize='unicode61 remove_diacritics 2'
);
```

Indexing rules (mirrors the vault's card definition):
- **card** — a `.md` directly in `people/`, `cards/`, `Wiki/`, or `projects/<slug>.md`.
  Frontmatter is read for id/type/title/status/private/dates.
- **core** — `_start-here.md`, `profile.md`, `decisions.md`, `lessons.md`, `inbox.md`,
  `README.md`, and project `README.md`s.
- **working** — every other `.md` (nested project files, adopted archives). Indexed for
  search, never validated.
- Excluded: `_index.md` (derived), `.mnemaos/`, `_mnemaos_backup/`, hidden folders
  (`.git`, `.obsidian`, …).

Chunking: split at `##` headings, cap ~2,000 characters per chunk (long sections split
on paragraph boundaries). BM25 weights: title 4.0, heading 2.0, content 1.0.

Incremental contract: a run with no vault changes performs **zero** writes; a changed
file replaces only its own chunks; a deleted file removes its rows.

## 3. Card schema extension: `private`

One new optional frontmatter field on any card or core file:

```yaml
private: true
```

Meaning: this document never leaves the machine the vault lives on **via the remote
surface**. Enforcement is in the server, keyed by transport:

| Mode | Default |
|---|---|
| stdio (local) | private docs **included** — memory is on the user's own machine |
| HTTP (remote) | private docs **excluded** from all six tools — search, get, list, context, and stats never reveal them |

`--exclude-private` forces exclusion in any mode. There is no flag to force inclusion
over HTTP — that would silently turn a privacy promise off.

## 4. Server modes and auth

| Mode | Start | Auth |
|---|---|---|
| Local | `python3 server.py --vault <path>` (stdio) | none — same machine, same user |
| Remote | `python3 server.py --vault <path> --http 127.0.0.1:8765` | `Authorization: Bearer <token>`; token from `MNEMAOS_TOKEN` env (required — the server refuses to start over HTTP without it) |

The HTTP transport implements the JSON-request subset of MCP streamable HTTP: `POST /mcp`
with a JSON-RPC message returns a single JSON response; notifications return 202. This
covers tool calling for every tested client; SSE streaming is not needed for these
short-lived tools. `GET /health` (no auth) returns `ok` for load-balancer checks — it
exposes no vault data.

The server binds to localhost by design; TLS and the public hostname are the reverse
proxy's job (see `deploy/`). Never expose the bare HTTP port to the internet.

## 5. Failure behavior

- Missing index → the server builds it on first start (and says so in `memory_health`).
- Corrupt index → delete `.mnemaos/index.db`, restart; nothing is lost (derived data).
- Gate rejection → the error names the exact check that failed; nothing is written.
- Vault path wrong → the server exits at startup with the path it tried, it does not
  serve an empty memory silently.
