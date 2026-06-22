# Onboarding Interview — the question bank for Phase 1

Use this to discover the user's stack. Ask in small batches (2–3 questions), confirm
what you heard, and record answers into `loop-config.yaml`. Adapt vocabulary to the
person — explain a term the first time you use it if they may not know it.

The goal is not to fill every field. The goal is to learn *enough to build a loop that
actually works in their environment*. If a dimension does not apply, mark it `none` and
move on.

## How to run the interview

1. Start with the outcome, not the tools: "When this is done, you'll put a task somewhere,
   and an AI will do it and hand it back for your OK. Let's figure out the pieces."
2. Go dimension by dimension below. After each batch, reflect the answer back in plain
   language and confirm before recording.
3. If an answer reveals a blocker (e.g. "the AI can't see my task app"), name it now and
   note the fallback (manual handoff) rather than discovering it at smoke-test time.

## Dimension 1 — LLM / agent environment

- Where does your AI run today? (a command-line coding agent, a desktop AI app, a hosted
  agent service, a self-run model, etc.)
- Can it run on its own — on a schedule or a trigger — or only when you start it?
- Can it run more than one task at the same time?
- Does it support sub-agents (one agent starting helper agents)? *(Needed for an
  automatic independent-reviewer pass; if not, the same agent self-reviews in two passes.)*

Why it matters: this decides whether you build an orchestrator (scheduled, parallel) or a
single manual-start worker, and whether an independent reviewer is automatic or sequential.

## Dimension 2 — Task system

- Where do your tasks live? (task-manager app, issue tracker, kanban board, spreadsheet,
  a folder of notes, email, etc.)
- Can your AI read tasks from it and update them — through an official connector/API, or
  would you paste tasks in by hand?
- How do you mark a task for the AI today, or how would you like to? (a tag/label, a
  column, a keyword in the title)

Why it matters: this is the queue. The adapter maps the five abstract states to whatever
this system supports (labels, columns, statuses, or "task in folder X").

## Dimension 3 — Connectors / API access

- Which integrations are connected and authenticated *right now*?
- For the task system specifically: read-only, read-write, or none?
- For the result destination: can the AI write there directly?

Why it matters: this decides the loop's automation level:
- **Full**: AI reads the queue, works, updates status, saves result — hands-off.
- **Assisted**: AI works and saves, but the human moves task states.
- **Manual handoff**: the human pastes the task and saves the result; the AI just works.

Build for the real level. Tell the user which one you built and what would unlock the
next level.

## Dimension 4 — Result storage

- Where should finished work end up? (a folder, a repository, a notes app, a drive,
  attached back onto the task)
- Is that location writable by the AI?
- Any naming convention you want for result files? (default: human-readable names,
  dated folders — never internal IDs as the only name)

Why it matters: the worker needs exactly one clear, writable destination, or results get
lost.

## Dimension 5 — Memory / knowledge base / skill catalog (OPTIONAL)

- Do you keep notes, a knowledge base, or a memory/RAG layer the AI should consult before
  working?
- Do you have a library of reusable AI skills/prompts it should pick from?
- Should accepted results be recorded back into that memory (the "closure" step)?

Why it matters: this is purely optional enrichment. If yes, the worker gets a "load
relevant context first" step and you may enable the closure step. If no, the loop works
fine without any of it — do not invent a memory system the user does not have.

## Dimension 6 — Permissions, schedule, limits

- What is the AI allowed to do without asking you? What must it *never* do without asking?
- How often should the loop run — only when you start it, hourly, daily, on a trigger?
- Any hard caps? (no outbound email/messages, no publishing, no payments, spend limit,
  time limit per task)

Why it matters: these become explicit rules inside the worker prompt and the schedule in
the config. Defaults are the conservative safety rules in `loop-core.md`; the user can
loosen a specific one only by saying so here.

## Dimension 7 — Loop shape

- Do you want the AI to check its own work before handing it back? (recommended yes)
- Do you want an independent reviewer pass (a fresh agent critiquing the result)?
- Do you want a closure step that records accepted results to memory? (only if Dimension 5
  has memory)
- How do you want to approve or reject? (e.g. completing the task = approved; a "rework"
  label = send back)

Why it matters: this sizes the loop. Offer the full shape (self-check → independent review
→ approve → closure) but let the user pick a smaller shape if that is all they need.

## After the interview

Summarize the chosen setup back to the user in plain language — the LLM host, the task
system and automation level, where results go, whether memory/closure is on, the schedule,
the limits, and the loop shape. Get a yes before generating files. Then proceed to Phase 2.

## Worked example — answers → config

A short end-to-end example, so you can see how spoken answers become the config. (Illustrative;
not a template to copy — the user's real answers drive the values.)

> **User says:** "My AI is a coding-agent CLI on my laptop. Tasks live in a kanban board I can
> reach through its connector, read and write. I tag a card `@ai` to hand it over. Finished work
> should go in a `~/ai-results/` folder. I keep notes but I don't want anything written back to
> them. Run it once a day. It must never email anyone or post anything. I want it to check its own
> work and have a second agent review it. I approve by completing the card; if I want changes I add
> a `rework` label."

Resulting `loop-config.yaml` (key lines):

```yaml
llm:        { host: "coding-agent CLI", unattended: true, parallel: true, subagents: true }
task_system:{ name: "kanban board", adapter: "generic-board", access: "full" }
result_storage: { path: "~/ai-results" }
memory:     { enabled: false }                 # notes exist but not consulted; closure off
permissions:{ schedule: "daily",
              hard_limits: ["no sending email or messages as me", "no publishing"] }
loop:       { self_check: true, independent_review: true, closure_enabled: false,
              accepted_signal: "card completed", rejected_signal: "label: rework" }
```

What gets generated: `worker-prompt.md` (self-check + independent reviewer, board adapter, board
operations resolved), `orchestrator-prompt.md` (daily, parallel, **Stage B Branch B1** — approve→
done, reject→rework, since no memory/closure), `README.md`, `SETUP.md` (Phase-6 schedule steps for
a daily CLI run + feasibility note). No `acceptance-closure-prompt.md` (closure is off).
