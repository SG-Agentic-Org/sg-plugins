---
name: mnemaos
description: >
  Interview a user about how they work with an LLM, then design and generate a
  personal memory system for them — a local, plain-Markdown "vault" their AI reads
  at the start of every session and writes back to when work finishes. Use when the
  user wants to "give my AI a memory", "set up a personal memory system", "make my
  assistant remember between sessions", "build a second brain my AI can use", "turn
  my notes folder into agent memory", "stop re-explaining my context every chat", or
  "adopt my existing work folder into a memory layer". Works greenfield (from scratch)
  or by adopting an existing folder. Ships a model-agnostic core plus adapters for any
  LLM host. Do NOT use for one-off tasks (just do the task), for building a chatbot,
  for cloud/SaaS memory products, or for setting up a task-automation loop (that is a
  different skill).
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# MnemaOS — personal memory onboarding

This skill helps a person stand up their own **memory system**: a local folder of
plain Markdown files ("a vault") that their AI reads at the start of a session to
remember who they are and what they are working on, and writes back to when a piece
of work finishes — so the AI stops forgetting everything between chats.

Your job is to **interview the user about their actual setup, then design and
generate a personal memory system for it** — not to copy any one reference vault.
People have different LLM hosts, storage, and starting points. The skill ships a
*model-agnostic core* (the memory model, the card contract, four memory skills as
templates) plus *adapters* for the parts that vary (which LLM runs it, how routines
fire, plain Markdown vs Obsidian).

> This skill is for **set-up**. It does not do the user's day-to-day work. After
> onboarding, the user's own agent runs the four memory skills it generated.

The system gives the person **two artifacts**: (1) four memory skills installed where
their agent can find them, and (2) a generated **vault** in a folder they chose. The
package is the installer; the vault is the data.

## Principles you must hold (do not violate these)

1. **The memory belongs to the person.** Local Markdown, Git-friendly, no required
   SaaS. They can walk away with everything.
2. **Transparency.** The logic lives in open skill files they can read and change.
   No black box.
3. **The agent is a companion, not a boss.** It helps remember, link, and tend —
   it does not judge, pressure, or use alarmist language.
4. **Simplicity over copying complexity.** Offer the full system; let them take a
   smaller one. Do not force depth they did not ask for.
5. **Never leak a reference implementation.** Do not put another person's tool names,
   paths, project names, or domains into the generated files. Adapt to *their* setup.
   The smoke test enforces this; treat any leak as a bug.
6. **Nothing destructive without consent.** In the adopt-existing-folder mode you do
   not move, rename, or delete a single file before the user approves the plan, and you
   always back up first. (See `references/adopt-existing-folder.md`.)

## Phase 0 — Choose the mode (the first question)

Before interviewing, ask one branching question:

> "Do you want to **start a fresh memory from scratch**, or **turn a folder you already
> have into a memory layer**? If you already have a messy work folder full of projects
> and notes, I can adopt it instead of starting empty."

- **Greenfield** → continue to Phase 1, then generate a clean vault (Phase 3).
- **Adopt existing folder** → run Phase 1 (interview) for the environment questions,
  then switch to `references/adopt-existing-folder.md` for the audit → map → propose →
  approve → backup → deploy → migrate → index flow **instead of** the plain Phase 3
  generation. The hard rule there: read-only until the user approves the plan.

If unsure, default to asking — do not assume greenfield just because the folder looks empty.

## Phase 1 — Discover the setup (interview)

Ask the user about each dimension below. Ask in small batches (2–3), reflect the answer
back in plain language, confirm, then record it in `mnemaos-config.yaml`. Adapt your
vocabulary — many people are not engineers. Explain a term the first time you use it.

The six dimensions:

1. **Who you are and your projects** — what you do, your 3–7 active projects/contexts,
   the key people around them. → fills `profile.md`, `_start-here.md`, starter cards.
2. **Where you work with the LLM** — a coding-agent CLI, a desktop AI app, a self-run
   model with a harness? Can it run on a schedule, or only when you open it? Does it
   support sub-agents (for an independent reviewer pass in closure)? → picks the adapter
   and the automation level for routines.
3. **Where you keep files** — which folder should hold the vault? Greenfield or adopting
   an existing folder (Phase 0)? Under Git? → vault path + mode.
4. **Obsidian or plain Markdown** — do you use Obsidian (turn on `[[wikilinks]]`/graph-
   friendly format) or are plain files enough? → vault format. Either way it stays
   plain Markdown that opens anywhere.
5. **Automation level** — what may the agent do without asking? Can anything run on a
   schedule, or is everything manual? Hard limits (never publish, never message as you,
   never delete)? → which routines to offer + safety rules baked into the skills.
6. **Depth of memory** — just the basics (profile + projects + episodes), or also
   distillation into cards and regular hygiene? Want an independent reviewer pass in
   closure? Want the optional RAW/Wiki/Outputs source-library frame and the question-
   report habit? → how big a system to build. Offer the full shape; let them choose less.

Read `references/onboarding-interview.md` for the full question bank and how to interpret
answers. Read it before you start interviewing.

## Phase 2 — Design the system

Once you understand the setup, design from the fixed core plus the adapters their setup
needs.

1. Read `references/memory-model.md` — the **model-agnostic core**: the one-layer memory
   model (vault = truth), the memory types, and the "where does this go" decision tree.
   This is the same for everyone.
2. Read `references/frontmatter-contract.md` — the card contract (the minimal frontmatter
   every card carries) and the optional provenance/trust fields.
3. Read the four skill contracts — `references/skill-startup-contract.md`,
   `skill-closure-contract.md`, `skill-distillation-contract.md`,
   `skill-hygiene-contract.md`. These are templates you resolve to the user's vault path,
   environment, and limits.
4. Read `references/routines.md` — the routine catalog and how to map "automation level"
   to a schedule (with honest manual fallback).
5. Read `references/adapters.md` — pick the adapter that matches the user's LLM host, or
   compose one from `assets/adapters/adapter-template.md`. The core never changes; only
   the adapter does.
6. Read `references/safety-and-boundaries.md` — the limits the generated skills must carry.
7. If they chose the optional source-library frame or question-report habit, read
   `references/optional-modules.md`.

## Phase 3 — Generate the system (greenfield)

> For the adopt-existing-folder mode, follow `references/adopt-existing-folder.md` instead
> of this phase — it generates the same vault but migrates the user's files into it.

Produce a self-contained system in the folder the user chose. Generate:

1. **`mnemaos-config.yaml`** — the user's Phase-1 answers, filled into
   `assets/examples/mnemaos-config.example.yaml`. Single source of truth for the setup,
   and the recovery point if onboarding is interrupted.
2. **The vault skeleton** in the chosen folder (`assets/vault-template/`), filled in:
   - `_start-here.md` and `profile.md` with the real "who / projects / people" answers.
   - empty `inbox.md`, `decisions.md`, `lessons.md` with headings.
   - starter cards for the people/projects named in dimension 1, in `people/` and
     `projects/`, each with valid frontmatter (contract §`frontmatter-contract.md`).
   - `_index.md` generated by running `scripts/index_vault.py`.
3. **The four memory skills** (startup / closure / distillation / hygiene), resolved from
   the contracts with placeholders filled (vault path, environment adapter, limits).
   Always install startup + closure. Distillation and hygiene are on by default; the user
   may switch one off.
4. **`README.md`** for the vault — written for the person (`assets/templates/` has the
   pieces): what this is, how to feed it context, how the agent reads it, what to do if
   something is off. Adapt to their setup.
5. **`SETUP.md`** — host-aware install / routine-activation / uninstall steps for the
   identified environment, or an honest "run these by hand" if no scheduler exists.

Resolve **every** placeholder. A leftover `{{...}}` token is a setup bug — the smoke test
catches it. A few values are not brace-tokens but still must be set to real choices: the
`vault.path`, the `environment.host`, and the `automation.schedule`. Confirm these with
the user before saving.

**Idempotency.** Generation is safe to re-run. If onboarding was interrupted and the vault
is partly built, re-running **adds what is missing without overwriting** filled-in
`profile.md`/`_start-here.md`/cards. Read `mnemaos-config.yaml` first and resume from the
last unfinished step rather than re-interviewing.

## Phase 4 — Safety and limits

Before handing over, lock the unsafe edges. Read `references/safety-and-boundaries.md` and
apply it:

- The generated skills carry the user's hard limits as explicit "stop and ask" rules: no
  publishing, no outbound messages as the user, no payments, no deleting significant data,
  no permission changes — unless the user explicitly allowed it in dimension 5.
- Conservative defaults; loosen only a limit the user named.
- No secret value ever goes into a generated file. Memory is plain notes — if a credential
  is ever needed, reference it by name, never by value. The smoke test flags inlined secrets.
- When the agent hits a limit, it **stops and flags the work, with a concrete reason** —
  it does not improvise around the limit.

## Phase 5 — Smoke test and live dry-run

Verify before declaring success. These are **two different** checks — do not conflate them.

1. **Structural smoke test** (deterministic, standard-library only, no LLM):
   ```bash
   python3 scripts/smoke_test.py <path-to-generated-vault>
   ```
   It checks: required files exist; card frontmatter is valid; no unresolved `{{...}}`;
   no leaked reference-implementation names/paths; no inlined secrets in any text/config file
   (including the backup folder and `.env`/`.json`/etc.); no broken `[[wikilinks]]` (checked
   directly — you do **not** have to run
   `index_vault.py` first); `_index.md`, if present, is consistent. Exits non-zero on any
   failure. (Running `index_vault.py` first is still good practice to regenerate `_index.md`,
   but smoke no longer depends on it for link checking.)

2. **Live agent dry-run** (needs a live LLM host — this is an acceptance demo, not CI):
   (a) ask the agent to read `_start-here.md` and say back "who is the user / active
   projects" — proves *startup* works; (b) run *closure* on a tiny throwaway task (e.g.
   "write a two-line note about today") and confirm an episode landed in `inbox.md` —
   proves *closure* works. Use a harmless task so nothing risky happens on the first run.

3. **Walk the user through what happened** so they understand the moving parts.

If the dry-run cannot complete because of a real environment limit, report the specific
blocker and the smallest change that would unblock it — do not fake success.

## Phase 6 — Activate routines (host-aware)

The system is not done when the files exist. The last mile is making the routines actually
run — and proving they will. **Do not hardcode "create a scheduled task like this."** You
do not know the user's host in advance.

1. **Identify the environment** from Phase-1 answers plus the host you are in now: a
   coding-agent CLI, a desktop AI app, a self-hosted setup. Separately, **where will the
   scheduler run** (the same machine, a cloud runner)?
2. **Offer the mechanism(s) that fit** — present options, do not impose one: a cloud/cron
   routine the host offers *if it can run unattended*; the desktop app's built-in
   scheduler; a system cron invoking the CLI agent; or pure manual triggers. Explain the
   trade-off in plain language.
3. **Check feasibility before promising it.** The classic failure: a cloud/headless run
   cannot see the user's local vault files. If so, give an honest fallback — run the
   scheduler where the files live, or keep routines manual. Never promise an unattended
   routine that will silently fail.
4. **Record the chosen mechanism** in `mnemaos-config.yaml` (`automation.schedule`) and
   write the *actual* steps for that host into `SETUP.md`. Not a generic stub.

Done means: working routines (or a deliberate, verified manual trigger) — not a folder of
files with "now go set up a scheduler yourself" left to the user. The minimum viable mode
is honest: **closure and hygiene run when the user says a trigger phrase**, no scheduler
required.

## Common mistakes

1. **Copying a reference vault verbatim.** The shipped templates have placeholders, not a
   finished vault. Resolve everything to *their* setup. A vault with someone else's project
   names is not their memory.
2. **Leaving placeholders unresolved.** `{{vault_path}}` in a generated skill means the
   agent will not know where to write. The smoke test catches these; do not skip it.
3. **Leaking a reference implementation.** Another person's tool names, paths, or domains
   in the generated files is a leak. Keep the generated system about *this* user.
4. **Over-building.** If the user only wants profile + projects + episodes, do not force
   distillation, hygiene, the source-library frame, and an independent-reviewer pass on
   them. Offer the rich system; let them pick less.
5. **Promising automation the host cannot run.** If the environment cannot run unattended,
   say so and ship the manual-trigger fallback. Never invent a scheduler.
6. **Touching files before approval (adopt mode).** In adopt-existing-folder mode, moving
   or renaming anything before the user approves the plan — or skipping the backup — is the
   worst failure. Read-only until approved; back up first, always.
7. **Stopping at files without activating routines.** Generating the vault and leaving the
   user to "go set up a scheduler yourself" is an abandoned last mile. Finish Phase 6.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Agent forgets context every session | startup skill not installed, or `_start-here.md` not read first | Confirm the startup skill is in the agent's skill folder and points at the vault path |
| Nothing lands in `inbox.md` after work | closure skill not run, or wrong vault path in the skill | Run closure by its trigger phrase; check the resolved `vault_path` |
| Cards pile up as duplicates | distillation not checking for an existing card on the same entity | Use the dedup step in the distillation contract (exact `id` + similar-title heuristic) |
| `_index.md` is stale or has broken links | hygiene/index not run after adding cards | Run `scripts/index_vault.py`, or the hygiene-weekly routine |
| Smoke test fails on a placeholder | a Phase-3 file kept a `{{...}}` token | Resolve it from `mnemaos-config.yaml` and re-run |
| Smoke test flags a leaked name | a reference-implementation name slipped into a generated file | Remove it; the system must be about this user only |
| Scheduled routine sees no files | cloud/headless host cannot reach the local vault | Run the scheduler where the vault lives, or keep routines manual (Phase 6, step 3) |
| Adopt mode: user is nervous about losing files | backup step not surfaced | Show them the `_mnemaos_backup/original-…/` copy before any move; nothing is deleted |

## What this skill ships

```
mnemaos/
  SKILL.md                         — this file (the onboarding orchestrator)
  references/
    onboarding-interview.md        — the full question bank for Phase 1
    memory-model.md                — model-agnostic core: layer, memory types, decision tree
    frontmatter-contract.md        — card frontmatter contract + optional provenance/trust
    skill-startup-contract.md      — "read memory at session start" skill (template)
    skill-closure-contract.md      — "save durable memory after work" skill (template)
    skill-distillation-contract.md — "raw material → clean cards" skill (template)
    skill-hygiene-contract.md      — "audit / tend the memory" skill (template)
    routines.md                    — routine catalog + automation-level mapping
    adapters.md                    — adapter catalog + how to choose/compose
    safety-and-boundaries.md       — limits the generated skills carry
    adopt-existing-folder.md       — the adopt-an-existing-folder migration flow
    optional-modules.md            — RAW/Wiki/Outputs frame, reports, provenance, trust
  assets/
    vault-template/                — the vault skeleton copied to the user
    templates/                     — card / project-readme / closure-entry (vault README lives in vault-template/)
    adapters/                      — adapter-template + cli-agent + desktop-app examples
    examples/                      — annotated mnemaos-config.example.yaml
    docs/                          — package-internal docs (README, SETUP master) referenced by onboarding
  scripts/
    smoke_test.py                  — clean-environment structural check (stdlib-only)
    index_vault.py                 — deterministic vault indexer (stdlib-only)
    make_test_fixtures.py          — generate the three reviewer scenarios (Вика/Катя/advanced)
```
