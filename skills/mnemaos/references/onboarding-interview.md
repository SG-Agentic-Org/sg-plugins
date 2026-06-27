# Onboarding interview — the question bank for Phase 1

Use this to discover how the user works with their LLM. Ask in small batches (2–3),
reflect each answer back in plain language, confirm, then record into `mnemaos-config.yaml`.
Adapt vocabulary to the person — explain a term the first time you use it.

The goal is not to fill every field. The goal is to learn *enough to build a memory system
that actually works for them*. If a dimension does not apply, mark it `none` and move on.

## How to run the interview

1. **Start with the outcome, not the tools:** "When we're done, you'll have a folder your AI
   reads at the start of every session — so it remembers who you are and what you're working
   on — and writes the results of your work back into. Let's build it around you."
2. **Phase 0 first — the mode.** Ask: start fresh, or adopt an existing folder? (See the
   SKILL and `adopt-existing-folder.md`.) This changes how Phase 3 runs, not the questions.
3. Go dimension by dimension. After each batch, reflect back and confirm before recording.
4. If an answer reveals a blocker (e.g. "my AI runs only in a web chat and can't touch local
   files"), name it now and note the honest consequence, rather than discovering it at
   smoke-test time.

## Dimension 1 — Who you are and your projects

- What do you do? In a sentence or two.
- What are your 3–7 active projects or contexts right now?
- Who are the key people around them (clients, colleagues, partners)?

Why it matters: this fills `profile.md` and `_start-here.md`, and seeds the first cards in
`people/` and `projects/`. This is the content that makes the agent "already know you" on
the first run.

## Dimension 2 — Where you work with the LLM

- Where does your AI run? (a command-line coding agent, a desktop AI app, a self-run model
  with a tool-calling harness, etc.)
- Can it run on its own — on a schedule or a trigger — or only when you open it?
- Does it support sub-agents (one agent starting helper agents)? *(Needed for an automatic
  independent-reviewer pass in closure; if not, the same agent reviews in a second pass.)*

Why it matters: this picks the adapter and decides whether routines can be scheduled or are
manual. **Web-only chat with no file access is a real constraint** — say so, and build the
copy-paste manual mode rather than promising automation that cannot run.

## Dimension 3 — Where you keep files

- Which folder should hold the vault? (A new folder, or one you already have.)
- Greenfield (start empty) or adopt an existing folder? *(Phase 0 already asked; confirm.)*
- Is it under Git, or would you like it to be? (Optional; the vault is Git-friendly either
  way.)

Why it matters: sets `vault.path` and the mode. If adopting, switch to
`adopt-existing-folder.md` — the vault is built by migrating their files, not from empty.

## Dimension 4 — Obsidian or plain Markdown

- Do you use Obsidian? (If yes, turn on `[[wikilinks]]` and a graph-friendly format.)
- If not, are plain Markdown files fine? (They are — the vault opens in any editor.)

Why it matters: sets the vault format flag. Both produce plain Markdown; Obsidian mode just
leans on wikilinks and tags so the graph view is useful.

## Dimension 5 — Automation level

- What may the agent do without asking you? What must it *never* do without asking?
- Can anything run on a schedule (closure after a task, weekly hygiene), or is everything
  manual?
- Any hard limits? (Never publish, never message/email as you, never delete files, never
  spend money.)

Why it matters: these become explicit "stop and ask" rules inside the generated skills, and
they decide which routines you offer. Defaults are conservative (no publishing / no outbound
messages / no deleting without asking); the user loosens a specific one only by saying so.

## Dimension 6 — Depth of memory

- Do you want just the basics (profile + projects + episodes in the inbox), or also:
  - **distillation** — turning messy sessions/notes into clean cards?
  - **regular hygiene** — a weekly pass that finds broken links, duplicates, and oversized
    files?
  - an **independent reviewer pass** in closure (a fresh agent critiques the result before
    it is recorded)?
  - the optional **source library** (a RAW/Wiki/Outputs frame) for distilling external
    sources with provenance, and the **question-report habit** (a weighty question to your
    memory produces a short saved report, not just a chat answer)?

Why it matters: this sizes the system. Offer the full shape (startup + closure +
distillation + hygiene + optional modules); let the user take a smaller shape if that is all
they need. Do not force depth.

> **Six dimensions, deliberately — not seven.** A task-automation loop centers on a "task
> system / queue"; MnemaOS centers on the **memory itself**, so "task system" is not a
> dimension here, and "depth of memory" is added instead.

## After the interview

Summarize the chosen setup back in plain language — the LLM host and automation level, the
vault path and mode (greenfield/adopt), Obsidian or plain, the limits, and which of the four
skills and optional modules are on. Get a yes before generating. Then proceed to Phase 2.

## Worked example — answers → config

Illustrative, not a template to copy. The user's real answers drive the values.

> **User says:** "I'm a freelance email marketer. My active stuff: a B2B client newsletter,
> a personal list, and a course I'm building. I only use ChatGPT in the browser — I don't
> want to install anything. Start me from scratch in a new folder; I don't use Obsidian. The
> AI should never send emails or post anything as me. I want the basics plus the ability to
> turn a session into notes; weekly hygiene I'll run by hand. No second-reviewer pass."

Resulting `mnemaos-config.yaml` (key lines):

```yaml
mode: greenfield
profile:     { role: "freelance email marketer",
               projects: ["B2B client newsletter", "personal list", "course build"] }
environment: { host: "web chat (ChatGPT, browser)", file_access: false,
               unattended: false, subagents: false, adapter: "web-chat-manual" }
vault:       { path: "~/marketing-memory", format: "plain-markdown" }
automation:  { schedule: "manual",
               hard_limits: ["never send email or messages as me", "never publish"] }
skills:      { startup: true, closure: true, distillation: true, hygiene: true,
               independent_review: false }
optional:    { source_library: false, question_reports: false }
```

What gets generated: a clean vault in `~/marketing-memory`; the four skills as **copy-paste
instructions** (because the host has no file access and no scheduler — manual mode), with the
limits baked in; a README that explains how to paste her context in and how the agent reads
it; SETUP.md with the honest "run these by hand, here's how" steps. No automation promised.
