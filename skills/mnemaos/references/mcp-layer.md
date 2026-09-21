# The MCP layer — onboarding reference

Read this during Phase 2 (design) **if** the user wants their memory reachable by more
clients than a file-reading agent. It extends the onboarding with one interview
dimension, one decision, and one extra install step. Everything else about the memory
system stays exactly as the core references describe: the vault of plain Markdown is
the single source of truth; the MCP layer is an optional overlay on top of it.

## What the layer is

`mnemaos-mcp` (shipped in its own folder next to this skill) is a small server —
standard-library Python, no dependencies — that indexes the vault into one derived
SQLite file and serves six tools over MCP: `memory_context`, `memory_search`,
`memory_get`, `memory_list`, `memory_write`, `memory_health`.

What it changes for the user, in plain words:

- **Without it:** memory works wherever the agent can read files (the startup skill
  reads `_start-here.md`, closure writes to the vault).
- **With it, locally:** any MCP-capable app on the same machine gets the memory —
  including apps that cannot read arbitrary files. Search gets fast and ranked.
- **With it, on a server:** web and mobile clients get the memory too. This is the
  first-class answer for the user whose only LLM is a web chat — in the file-only
  system they were limited to copy-paste; with a hosted MCP their web client simply
  *has* their memory.

## Interview: the seventh dimension

Ask after the other six, in the user's language, plainly:

> "Should your memory be reachable **only by the agent on this computer**, or also by
> **other apps and devices** — the web chat, your phone? Reaching it from everywhere
> means running a small free server program; on this machine it is a one-line setup,
> for phone/web access you would rent a tiny server (~$5/month) and I will hand you a
> step-by-step guide."

Map the answer to one of three shapes:

| Answer | Shape | What you install |
|---|---|---|
| "just this computer, files are fine" | **file-only** | nothing extra — the core system as-is. Valid and complete; do not upsell. |
| "other apps on this machine too" / "I want better search" | **local MCP** | `mnemaos-mcp` over stdio, registered in their MCP-capable hosts |
| "phone / web / other machines" | **remote MCP** | local MCP now + hand over `mnemaos-mcp/deploy/vps-setup.md`; vault under Git becomes strongly recommended (it is the sync channel and the backup) |

Feasibility honesty (same rule as routines): if the user's main client cannot attach a
custom MCP server at all, say so — do not install a server nothing will talk to. And
remote mode means the memory lives on a rented server in plain text; say that sentence
out loud before they choose it (details in the deploy guide's "honest part").

## What changes in the generated system

1. **Startup skill.** Add an "if MCP is connected" branch at the top: begin the session
   with `memory_context()` instead of manually reading `_start-here.md`; fall back to
   file reading when the tools are absent. The file stays the truth — the tool is just
   the faster door. Recall order: `memory_search` → miss → `memory_list` → `memory_get`
   (a search miss never proves absence).
2. **Closure/distillation skills.** Where the contract says "write the card into the
   vault", add: when working through MCP (no direct file access), call `memory_write`
   instead — same decision tree, same card contract; the gate enforces it.
3. **Privacy.** Teach the user the one-line rule before anything is hosted: cards with
   `private: true` in frontmatter are never served remotely. If they adopt-migrated
   sensitive material, walk the cards once together and mark what should stay home.
4. **`mnemaos-config.yaml`.** Record the choice under `mcp:`
   (`mode: none|local|remote`, `vault_db`, `hosts: [...]`, and for remote the URL —
   never the token; tokens live in a password manager and `/etc/mnemaos.env` only).
5. **SETUP.md.** Add the host registration snippets actually used (from
   `assets/host-snippets.md`) and, for remote, the link to `deploy/vps-setup.md` plus
   the checklist state ("deployed on …, token rotated: how").

## Verification additions (Phase 5)

- Run `python3 mnemaos-mcp/smoke_test_mcp.py <vault>` — must end `0 failed`.
- Live dry-run, MCP edition: in a **fresh** session of the connected client, ask "what
  do you know about me?" — the client should call `memory_context` and answer from the
  vault without being fed anything. Then `memory_write` a throwaway episode and check
  it landed in `inbox.md`.
- Remote only: the two curl checks from the deploy guide (with token → answer, without
  → 401) and one private-card negative check.

## Common mistakes (MCP edition)

1. **Installing the server for a user who only ever uses one file-capable agent.**
   File-only is a complete system. The MCP layer must earn its keep.
2. **Promising web-app connectivity without checking the client.** Some consumer web
   chats only accept OAuth connectors and will not send a static bearer token. Check
   that client's own connector docs before promising; offer its API/desktop surface as
   the fallback. Never leave the user with a hosted server nothing can talk to.
3. **Putting the token into the vault or the config.** Tokens never enter memory —
   the gate blocks the obvious shapes, but do not test it on purpose.
4. **Skipping the private-card walk before hosting an adopted vault.** Migrated
   folders often contain things the user forgot were there. One pass, together, before
   the first `git push` to the server.
5. **Treating the index as data.** It is a cache. If anything looks wrong:
   `indexer.py --rebuild`. Never "fix" the index file itself; never back it up.
