# Host snippets — registering mnemaos-mcp with common LLM hosts

Resolve `<MCP>` to the absolute path of the `mnemaos-mcp` folder and `<VAULT>` to the
absolute vault path before handing any snippet to the user. For remote mode, resolve
`<URL>` to `https://memory.<their-domain>/mcp` and remind them the token comes from
their password manager, not from a file in the vault.

## Coding-agent CLIs (stdio)

Most coding-agent CLIs register an MCP server with a command + args. The general shape:

```
name:    memory
command: python3
args:    ["<MCP>/server.py", "--vault", "<VAULT>"]
```

Claude Code:

```bash
claude mcp add memory -- python3 <MCP>/server.py --vault <VAULT>
```

Codex CLI (`~/.codex/config.toml`):

```toml
[mcp_servers.memory]
command = "python3"
args = ["<MCP>/server.py", "--vault", "<VAULT>"]
```

## Desktop AI apps (stdio via JSON config)

Claude Desktop (`claude_desktop_config.json` → `mcpServers`):

```json
{
  "mcpServers": {
    "memory": {
      "command": "python3",
      "args": ["<MCP>/server.py", "--vault", "<VAULT>"]
    }
  }
}
```

Other desktop apps with an "MCP servers" JSON section (Cursor, Windsurf, LM Studio and
similar) accept the same `command`/`args` object under their own config key.

## Remote (HTTP + bearer token)

For clients that accept a URL-based MCP server with custom headers:

```
url:     <URL>
headers: Authorization: Bearer <TOKEN>
```

Claude Code:

```bash
claude mcp add --transport http memory <URL> --header "Authorization: Bearer <TOKEN>"
```

**Consumer web-chat connectors — check first.** Some web products (connector UIs)
accept only OAuth-secured MCP servers and cannot send a static bearer header. If the
user's web client is one of those, the honest options are: use that vendor's desktop
or API surface (both take headers), or front the server with an OAuth-providing proxy
— that is an advanced setup, do not promise it casually. This limitation belongs in
the user's SETUP.md so they are not surprised later.

## After registering — the 60-second check

In a fresh session of the host:

1. The tools `memory_context` … `memory_health` appear in the host's tool list.
2. Ask: "what do you know about me?" → the host calls `memory_context` and answers
   from the vault.
3. `memory_health` shows the expected vault path and `0 files changed since last index`
   (or run `indexer.py` if not).
