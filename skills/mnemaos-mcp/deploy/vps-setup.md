# Hosting your memory on a VPS — step by step

This guide takes a small Linux server (any $5-class VPS: Debian/Ubuntu assumed) from
zero to "my LLM on the web/phone knows me". Every command is copy-pasteable. Where a
value is yours to choose, it looks like `<THIS>`.

**What you end up with:**

- your vault on the server, synced through Git (which doubles as your backup),
- `mnemaos-mcp` running as a systemd service on localhost,
- Caddy in front of it with automatic HTTPS on your (sub)domain,
- a bearer token that every client must present.

**Read this first — the honest part.** Your memory will live on that server in plain
Markdown. Whoever controls the server can read it. That is the deal you are making for
remote access. Three rules follow:

1. Never store secret values (passwords, API keys) in memory — the write gate blocks
   the obvious patterns, but the rule is yours to keep.
2. Mark anything you would not want served remotely with `private: true` **before**
   pushing the vault to the server — private docs are never served over HTTP, but they
   are still *on disk* there; if even that is too much, keep them in a folder that you
   do not push at all.
3. Keep the token secret and rotate it if in doubt (step 6).

---

## Step 0 — What you need

- A VPS with SSH access (`ssh <user>@<server>`), Debian or Ubuntu.
- A domain or subdomain you control, e.g. `memory.<your-domain>`, with an **A record**
  pointing at the VPS IP.
- Your vault in a Git repository (private!) that the server can pull from — any Git
  host with a deploy key works. No Git? See "Variant: rsync instead of Git" at the end.

## Step 1 — Server basics

```bash
ssh <user>@<server>
sudo apt update && sudo apt install -y python3 git caddy
python3 --version   # needs 3.9+
```

Create a dedicated system user so the memory does not run as root:

```bash
sudo useradd --system --create-home --shell /usr/sbin/nologin mnemaos
```

## Step 2 — Put the vault and the server code on the VPS

```bash
sudo -u mnemaos -H bash -c '
  cd ~
  git clone <YOUR-VAULT-REPO-URL> vault
  git clone <THIS-PACKAGE-REPO-URL> app
'
```

(For a private vault repo, add a read-write deploy key for the `mnemaos` user first:
`sudo -u mnemaos ssh-keygen -t ed25519` and register `~mnemaos/.ssh/id_ed25519.pub`
with your Git host. Read-write matters: `memory_write` commits new cards back.)

Build the index once and run the self-test:

```bash
sudo -u mnemaos -H bash -c '
  python3 ~/app/mnemaos-mcp/indexer.py ~/vault
  python3 ~/app/mnemaos-mcp/smoke_test_mcp.py ~/vault
'
```

The last line must end with `0 failed`.

## Step 3 — Generate the token

```bash
python3 -c "import secrets; print(secrets.token_urlsafe(32))"
```

Save the output somewhere safe (a password manager). Then put it in an environment
file only root and the service can read:

```bash
sudo tee /etc/mnemaos.env >/dev/null <<'EOF'
MNEMAOS_TOKEN=<PASTE-THE-TOKEN-HERE>
EOF
sudo chmod 600 /etc/mnemaos.env
```

## Step 4 — Run it as a service

Copy the unit file from this folder and enable it:

```bash
sudo cp ~mnemaos/app/mnemaos-mcp/deploy/mnemaos-mcp.service /etc/systemd/system/
sudo systemctl daemon-reload
sudo systemctl enable --now mnemaos-mcp
systemctl status mnemaos-mcp     # should be: active (running)
curl -s http://127.0.0.1:8765/health   # should print: ok
```

## Step 5 — HTTPS with Caddy

Copy the Caddyfile and put your domain in:

```bash
sudo cp ~mnemaos/app/mnemaos-mcp/deploy/Caddyfile.example /etc/caddy/Caddyfile
sudo nano /etc/caddy/Caddyfile     # replace memory.example.com with your domain
sudo systemctl reload caddy
```

Caddy fetches the TLS certificate automatically. Verify from your own computer:

```bash
curl -s https://memory.<your-domain>/health
# -> ok

curl -s https://memory.<your-domain>/mcp \
  -H "Authorization: Bearer <YOUR-TOKEN>" \
  -H "Content-Type: application/json" \
  -d '{"jsonrpc":"2.0","id":1,"method":"tools/call","params":{"name":"memory_health","arguments":{}}}'
# -> a JSON answer with your vault stats
```

And the negative check — **without** the token the same request must return HTTP 401.

## Step 6 — Connect your clients

Any MCP client that speaks HTTP with a bearer header can now use
`https://memory.<your-domain>/mcp`. Concrete per-client snippets are in
`../../mnemaos/assets/host-snippets.md`. Two notes:

- **Coding-agent CLIs / API-based clients** — URL + `Authorization: Bearer <token>`
  header. This is the widest-supported path.
- **Consumer web-app connectors** — some web chat products only accept OAuth-secured
  connectors and will not send a static bearer token. Check your client's connector
  documentation; if it requires OAuth, front this server with an OAuth-providing proxy
  or use that client from its API/desktop side instead. This guide does not pretend
  otherwise.

To rotate the token: generate a new one (step 3), update `/etc/mnemaos.env`,
`sudo systemctl restart mnemaos-mcp`, update your clients.

## Step 7 — Keep the vault fresh (sync + reindex)

New cards written remotely are committed by the sync timer below; edits you make at
home arrive with `git pull`. Add a timer that does both and refreshes the index:

```bash
sudo tee /etc/systemd/system/mnemaos-sync.service >/dev/null <<'EOF'
[Unit]
Description=mnemaos vault sync + reindex
[Service]
Type=oneshot
User=mnemaos
WorkingDirectory=/home/mnemaos/vault
ExecStart=/bin/bash -c 'git add -A && (git diff --quiet --cached || git commit -m "memory: remote writes") && git pull --rebase && git push && python3 /home/mnemaos/app/mnemaos-mcp/indexer.py /home/mnemaos/vault'
EOF

sudo tee /etc/systemd/system/mnemaos-sync.timer >/dev/null <<'EOF'
[Unit]
Description=mnemaos vault sync every 15 min
[Timer]
OnBootSec=2min
OnUnitActiveSec=15min
[Install]
WantedBy=timers.target
EOF

sudo systemctl daemon-reload
sudo systemctl enable --now mnemaos-sync.timer
```

On your home machine, `git pull` whenever you want the cards your remote sessions
wrote. Git history doubles as the backup and the audit trail of what the LLM wrote.

## Checklist — you are done when

- [ ] `systemctl status mnemaos-mcp` → active
- [ ] `https://…/health` → `ok`
- [ ] tools/call **with** token → JSON answer; **without** token → 401
- [ ] a card marked `private: true` is NOT returned by remote search/get
- [ ] `mnemaos-sync.timer` listed in `systemctl list-timers`
- [ ] token stored in your password manager, nowhere else

## Troubleshooting

| Symptom | Check |
|---|---|
| service fails at start | `journalctl -u mnemaos-mcp -n 30` — usually a wrong vault path or missing token |
| 401 with the right token | trailing space/newline in `/etc/mnemaos.env`; re-paste, restart |
| search returns nothing | index built? `sudo -u mnemaos python3 ~mnemaos/app/mnemaos-mcp/indexer.py ~mnemaos/vault --rebuild` |
| stale answers | did the sync timer run? `systemctl list-timers`, then `journalctl -u mnemaos-sync` |
| cert errors | DNS A record not propagated yet, or port 80/443 blocked by the VPS firewall |

## Variant: rsync instead of Git

No Git host? Push from home instead: `rsync -av --delete ~/vault/ mnemaos@<server>:vault/`
then `ssh <server> 'python3 ~mnemaos/app/mnemaos-mcp/indexer.py ~mnemaos/vault'`.
Trade-off: remote `memory_write` cards live only on the server until you rsync them
*back*, and you lose the Git history/backup. Git is the better default.

## Variant: Docker

`docker-compose.yml` in this folder runs the same server in a container (vault mounted
as a volume). Use it if your VPS is already Docker-managed; otherwise systemd is
simpler and one less moving part.
