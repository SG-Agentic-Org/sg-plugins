# mnemaos-mcp

Serve your MnemaOS memory vault to **any** LLM client over MCP — locally on your
machine, or from your own server so web and mobile clients can reach it too.

Your vault stays what it always was: a folder of plain Markdown files you own and can
read with your eyes. This server adds a fast search index and six memory tools on top.
The index is derived data — you can delete it any time and rebuild it with one command.
Nothing about your vault changes; a vault that worked without this layer keeps working
without it.

**No dependencies.** Pure Python 3.9+ standard library. No pip install, no database
server, no embeddings model. If you have `python3`, you have everything.

## What the connected LLM gets

| Tool | What it does |
|---|---|
| `memory_context` | One call at session start: who you are, active projects, recent cards |
| `memory_search` | Full-text search over the whole vault (any language) |
| `memory_get` | Read one card or file in full |
| `memory_list` | Deterministic listing — the fallback when search misses |
| `memory_write` | The only write tool: gated, writes plain Markdown into the vault |
| `memory_health` | Index freshness and serving mode — catches silent staleness |

Full contract: [CONTRACTS.md](CONTRACTS.md).

## Quick start — local (same machine)

```bash
# 1. Build the index (also happens automatically on first serve)
python3 indexer.py /path/to/your/vault

# 2. Try it
python3 - <<'EOF'
import sys; sys.path.insert(0, ".")
import server
mem = server.Memory("/path/to/your/vault")
print(mem.search("whatever you remember writing"))
EOF
```

Connect it to your LLM host (stdio transport, command + args):

```
command: python3
args:    /path/to/mnemaos-mcp/server.py --vault /path/to/your/vault
```

Host-specific snippets (coding-agent CLIs, desktop AI apps) are in
`../mnemaos/assets/host-snippets.md`.

## Quick start — remote (your own server)

This is for reaching your memory from web/mobile clients or from machines that do not
hold the vault. Full walkthrough: [deploy/vps-setup.md](deploy/vps-setup.md).

```bash
export MNEMAOS_TOKEN="$(python3 -c 'import secrets; print(secrets.token_urlsafe(32))')"
python3 server.py --vault /srv/memory/vault --http 127.0.0.1:8765
```

- The server **refuses to start** over HTTP without a token.
- It binds to localhost; TLS and the public hostname belong to a reverse proxy
  (Caddy/nginx examples in `deploy/`). Never expose the bare port.
- Clients authenticate with `Authorization: Bearer <token>`.

## Privacy: the `private` flag

Add one line to any card's frontmatter:

```yaml
private: true
```

Over the **remote** (HTTP) transport that document does not exist: search, get, list,
context, and stats all exclude it — enforced by the transport, with no flag to turn it
off. Locally (stdio) your memory is on your own machine, so private docs are included
(use `--exclude-private` if you want them hidden locally too).

## Options

```
--vault PATH         the memory folder (required)
--db PATH            index location (default: <vault>/.mnemaos/index.db)
--http HOST:PORT     serve over HTTP (requires MNEMAOS_TOKEN)
--read-only          disable memory_write entirely
--exclude-private    hide private docs even locally
--reindex            refresh the index before serving
```

Rebuild the index from scratch at any time:

```bash
python3 indexer.py /path/to/vault --rebuild
```

## Verifying

```bash
python3 smoke_test_mcp.py                 # full self-test on a throwaway fixture
python3 smoke_test_mcp.py /path/to/vault  # + prove your own vault indexes as-is
```

The self-test covers indexing (including that an unchanged rerun writes nothing),
search in Latin and Cyrillic, the privacy rules, every gate rejection, the real stdio
protocol end-to-end, and HTTP auth. It exits non-zero on any failure.

## Files

```
mnemaos-mcp/
  server.py           the MCP server (stdio + HTTP)
  indexer.py          builds/refreshes the derived search index
  gate.py             validation for memory_write (secret scan, schema, slugs)
  smoke_test_mcp.py   deterministic self-test
  CONTRACTS.md        the tool/DB/privacy contract
  deploy/             server deployment: walkthrough, systemd, Caddy, Docker
```
