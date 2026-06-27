# MnemaOS

Give your AI a memory. MnemaOS is an installable skill package that interviews you about how
you work with an LLM, then generates a personal **memory system** — a local folder of plain
Markdown your AI reads at the start of every session and writes back to when you finish work.
No SaaS, no database, no vendor lock-in. The memory is yours: plain files you can read, edit,
back up, and walk away with.

## What you get

After onboarding you have two things:

1. **Four memory skills** installed where your agent finds them:
   - **startup** — your AI reads your context at the start of a session, so it already knows you.
   - **closure** — after a task, your AI records what's worth keeping into the right file.
   - **distillation** — turns messy sessions and sources into clean, linked cards.
   - **hygiene** — a weekly tidy: refresh the index, find broken links and duplicates, flag rot.
2. **A vault** — a folder of Markdown: `_start-here.md`, `profile.md`, `projects/`, `people/`,
   `cards/`, `decisions.md`, `lessons.md`, `inbox.md`, `_index.md`.

## Two ways to start

- **Greenfield** — start from an empty folder; onboarding builds a clean vault around you.
- **Adopt an existing folder** — already have a messy work folder? MnemaOS audits it
  read-only, proposes a structure, waits for your approval, backs everything up, and then lays
  your files into a clean memory layer — with a migration report. Nothing moves before you
  approve, and the original is always backed up first.

## Install

1. Copy the `mnemaos/` folder into your agent's skills directory (where it discovers skills).
2. Start onboarding by asking your agent to "set up my memory with MnemaOS" (or invoke the
   `mnemaos` skill).
3. Answer the interview (6 short dimensions). The agent generates your vault and skills.
4. It runs a smoke test and a tiny live dry-run so you see the memory working.

Full steps, including how routines are scheduled on your specific host, are in `SETUP.md`
(generated for your setup during onboarding).

## Optional add-ons (off by default)

- **Source library** (RAW / Wiki / Outputs) — for distilling external sources with provenance.
- **Question reports** — a weighty question to your memory produces a short saved report.
- **Provenance / trust fields** — page-level source tracing and content-confidence labels.

Offered during onboarding; take them only if you work with external sources and want them.

## What's in the package, and what it does not include

**In the package:** the onboarding skill, the generated vault, the four memory skills, one
memory layer (the vault is the truth; retrieval = read the index + open the file), Markdown +
frontmatter, routines that degrade to manual triggers, a structural smoke test and a
deterministic indexer, and safety limits.

**Not included:** any MCP server; vector retrieval / RAG / embeddings; a mobile projection;
cross-device or cloud sync; a knowledge-graph export. MnemaOS is a local Markdown memory system
and works fully as one.

## How it stays honest

- **No leaked reference implementation.** The generated system is about you only — no other
  setup's tool names, paths, or projects. The smoke test enforces this.
- **No secrets in files.** Memory is plain notes; the package needs no credentials.
- **No destructive action without consent**, especially in adopt mode: read-only until you
  approve, backup before any move, nothing deleted.

## Files

```
mnemaos/
  SKILL.md         — the onboarding orchestrator (start here)
  references/      — the model-agnostic core + the four skill contracts + adopt + optional modules
  assets/          — the vault template, card templates, adapters, example config, docs/
  scripts/         — smoke_test.py + index_vault.py + make_test_fixtures.py (all stdlib-only)
```

> This README and `SETUP.md` live in `assets/docs/` so the skill root stays clean
> (`SKILL.md` + `references/` + `assets/` + `scripts/`) for skill-auditor. The public-facing
> README and full "about" docs for this repo live at `docs/mnemaos/` in the repository root.
