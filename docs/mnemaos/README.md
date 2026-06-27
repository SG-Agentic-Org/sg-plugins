# MnemaOS

**Give your AI a memory that belongs to you.**

MnemaOS is an installable skill package. It interviews you about how you work with an LLM, then
builds you a personal **memory system** — a local folder of plain Markdown that your AI reads at
the start of every session and writes back to when you finish work. No SaaS, no database, no
account. The memory is just files: yours to read, edit, back up, and walk away with.

→ Full descriptions: [`about.md`](about.md) (EN) · [`about.ru.md`](about.ru.md) (RU)
→ The skill itself: [`skills/mnemaos/`](../../skills/mnemaos/) (install this)

---

## Who it's for

Anyone who works with an LLM (ChatGPT, Claude, a coding agent, a local model) and is tired of
re-explaining their context every session. You don't need to be technical. It works whether you
live in a web chat or run a coding agent on your machine.

## The pain it solves

Your AI forgets everything between chats. You re-paste who you are, your projects, your tone of
voice, what you already tried. Your notes, if you have any, are scattered and the AI never reads
them on its own. MnemaOS turns that into a structured memory your agent reads automatically and
keeps tidy.

## How it's different

| | What it gives you |
|---|---|
| **vs. a plain Obsidian vault** | Obsidian stores notes. MnemaOS adds the *protocols* — startup, closure, distillation, hygiene — so your AI actually reads and maintains the notes, not just you. |
| **vs. a "remember this" memory prompt** | A prompt is one paragraph the model may or may not keep. MnemaOS is a durable, structured, versionable folder with a contract. |
| **vs. RAG / a vector database** | No embeddings, no server, no infra. Retrieval is "read the index, open the file." Plain text you can grep. |
| **vs. SaaS memory (vendor-locked)** | No vendor. Local Markdown under your control. Delete the package and your memory is still there. |

## Two ways to start

- **Greenfield** — start from an empty folder; onboarding builds a clean vault around you.
- **Adopt an existing folder** — already have a messy work folder with hundreds of files?
  MnemaOS audits it **read-only**, proposes a structure, **waits for your approval**, **backs
  everything up**, then lays your files into a clean memory layer with a migration report.
  **Nothing moves before you approve, and the original is always backed up first.**

## What happens to your existing files

In adopt mode: nothing is touched until you approve the plan. Then a full timestamped backup is
made (`_mnemaos_backup/original-…/`) **before** the first file moves. Your files are **copied**
into the new structure, never deleted as part of the move. Junk and duplicates are *flagged*, not
auto-deleted — you decide. You can always revert from the backup.

## Install

1. Copy the [`skills/mnemaos/`](../../skills/mnemaos/) folder into your agent's skills directory.
2. Ask your agent to "set up my memory with MnemaOS" (or invoke the `mnemaos` skill).
3. Answer the 6-dimension interview. The agent generates your vault and four memory skills.
4. It runs a structural smoke test and a tiny live dry-run so you see the memory working.

Host-specific routine scheduling is written into a generated `SETUP.md` during onboarding.

## What it does not do (boundaries)

- It does not publish, send messages as you, pay for anything, or delete significant data without
  your explicit consent.
- It does not require the cloud or run anything you can't see.
- MnemaOS does not include MCP, vector search, mobile apps, or cross-device sync. It is a local
  Markdown memory system, and it works fully as one.

## Privacy / local-first

Plain Markdown on your machine. No SaaS, no account, no telemetry. This package stores no
credentials — it needs none. A built-in smoke test flags any inlined secret or any leaked
reference-implementation name.

## Three quick examples

- **Vika — email marketer, web-only ChatGPT.** No CLI, no local files. MnemaOS builds her a clean
  vault from scratch and ships the startup/closure routines as **copy-paste blocks** — it never
  promises automation her web-only setup can't run.
- **Katya — content & SEO lead, big messy folder, uses Codex.** MnemaOS adopts her existing
  folder: read-only audit → folder map → proposed structure → her approval → full backup → copies
  her files into the new layer → migration report → index + smoke test.
- **Advanced user — already has an Obsidian vault.** MnemaOS overlays **non-destructively**: it
  adds protocols, an index, and bridge cards that *link into* existing notes — it does not rebuild
  the vault. Existing files are byte-for-byte untouched.

See [`about.md`](about.md) for the full version.

---

*Local-first. Transparent. The agent helps you remember — it isn't your boss.*
