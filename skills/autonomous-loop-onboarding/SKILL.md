---
name: autonomous-loop-onboarding
description: >
  Interview a user about their tools, then design and generate a personalized
  "autonomous task loop" — a setup where they queue a task in their task manager,
  an AI agent picks it up, does the work, self-reviews it, and hands it back for
  approval. Use when the user wants to "set up an autonomous AI loop", "make my AI
  do tasks from my task list automatically", "build an agent that takes tasks and
  returns finished work", "automate my backlog with AI", "wire my task manager to
  an AI agent", "set up an AI worker that runs tasks while I'm away", or asks how
  to turn a checklist/board/queue into an AI work queue with review. Works with any
  LLM environment and any task system via adapters. Do NOT use for one-off task
  execution (just do the task), for building a generic chatbot or assistant, for
  general task-manager tips unrelated to AI automation, or for writing a single
  cron job with no agent/review loop.
allowed-tools: Read, Write, Edit, Bash, Glob, Grep
---

# Autonomous Loop Onboarding

This skill helps a user stand up their own **autonomous task loop**: a repeatable
setup where they put a task into a task system, an AI agent claims it, does the
work, checks its own output, and returns it for human approval — with the human
involved only at "queue it" and "approve or send back".

Your job is to **interview the user about their actual stack, then generate a
personalized, working loop for it** — not to copy any one reference implementation.
Different people have different LLM hosts, task managers, storage, and permissions.
The skill ships a *model-agnostic core* plus *adapters* for the parts that vary.

> This skill is for set-up. It does not execute the user's day-to-day tasks itself —
> it produces the loop that will. After onboarding, the user's own agent runs tasks.

## When you are running this skill

Work through the phases below in order. Keep the user in the loop at each decision
point — this is a configuration task, and wrong assumptions about their tools waste
their time. Adapt your vocabulary to the user: many people setting up automation are
not engineers. Briefly explain any term you are unsure they know (e.g. "connector",
"credential", "cron").

If at any point a capability the user wants is impossible in their environment
(for example, their AI host genuinely cannot read their task system), say so plainly
and offer the closest workable alternative. Never promise support for a platform or
integration you cannot verify exists.

## Phase 1 — Discover the stack (interview)

Ask the user about each dimension below. Ask in small batches, not all at once.
Record answers in a config file (see Phase 3). The seven dimensions:

1. **LLM / agent environment** — Where does the AI run? (a coding-agent CLI, a
   desktop AI app with scheduled runs, a hosted agent platform, a self-hosted
   model with a tool-calling harness, etc.) What can it do on a schedule or on a
   trigger? Can it run unattended, or only when the user starts it?
2. **Task system** — Where do tasks live? (a task-manager app, an issue tracker, a
   kanban board, a spreadsheet, a plain folder of markdown files, email, etc.) Can
   the AI read and update it — via an official connector/API, or only by the user
   pasting tasks in?
3. **Connectors / API access** — Which integrations are actually available and
   authenticated right now? This decides whether the loop can be fully automatic or
   needs the user to hand tasks to the agent manually.
4. **Result storage** — Where should finished work land? (a folder, a repo, a notes
   app, a drive, attached back to the task.) The agent needs one clear, writable
   destination.
5. **Memory / knowledge base / skill catalog (optional)** — Does the user have a
   notes vault, a knowledge base, a memory/RAG layer, or a library of reusable AI
   skills the agent should consult? This is optional; the loop works without it.
6. **Permissions, schedule, limits** — What is the agent allowed to do without
   asking? How often does the loop run (manual, hourly, daily)? What are the hard
   limits (no sending email, no payments, no publishing, spend caps, time caps)?
7. **Loop shape** — Does the user want self-review built in? An independent reviewer
   pass? A separate "closure" step that records accepted results? How are tasks
   handed back for approval?

Read `references/onboarding-interview.md` for the full question bank, good follow-ups,
and how to interpret answers. Read it before you start interviewing.

## Phase 2 — Design the loop

Once you understand the stack, design the loop from two fixed contracts plus the
adapters their stack needs.

1. Read `references/loop-core.md` — the **model-agnostic core**: the state machine,
   the status labels, the queue model, and the safety rules. This part is the same
   for everyone.
2. Read `references/execution-contract.md` — the contract for the **execution worker**
   (the agent that does one task and self-reviews it). You will hand this to the user's
   agent, lightly adapted to their tools.
3. Read `references/acceptance-closure-contract.md` — the contract for **acceptance**
   (how an approve/reject is recognized and turned into a terminal state — needed in *every*
   loop) and **closure** (the OPTIONAL extra of recording the accepted result into memory).
   Acceptance ≠ closure: a loop with no memory still needs acceptance, it just skips closure.
4. If the user's environment runs on a schedule and can start workers in batches, read
   `references/orchestrator-contract.md` — the dispatcher that runs one full pass over
   both queues. Skip it for on-demand, one-task-at-a-time environments.
5. Read `references/adapters.md` — pick the adapter that matches the user's task
   system and LLM host, or compose a new one from the template. Adapters translate
   the abstract loop ("move task to IN_PROGRESS") into concrete operations in their
   tools ("set the `in-progress` label via the task API").

If no exact adapter exists, build one from `assets/adapters/adapter-template.md`.
The core never changes; only the adapter does.

## Phase 3 — Generate the personalized loop

Produce a self-contained setup the user can keep and run. Write it into a directory
the user chooses (default: a new `my-autonomous-loop/` folder). Generate:

1. **`loop-config.yaml`** — the user's answers from Phase 1, filled into
   `assets/examples/loop-config.example.yaml`. This is the single source of truth
   for their setup.
2. **`worker-prompt.md`** — the execution contract from
   `references/execution-contract.md`, with the placeholders resolved to the user's
   actual task system, storage path, permissions, and labels. This is the prompt
   their agent runs per task.
3. **Acceptance handling** — always specify how approve/reject becomes a terminal state.
   If the user wants **closure to memory**, generate `acceptance-closure-prompt.md` from
   `references/acceptance-closure-contract.md` (resolved). If they do **not** (the common
   case), there is no closure-worker file — instead fold the lightweight
   acceptance-reconciliation (approve → done, reject → rework) into the orchestrator's Stage B
   (Branch B1), or, for on-demand setups, document it as the user's one-step manual action in
   the README. Never leave "what happens after review" unspecified.
4. **`orchestrator-prompt.md`** (only if their environment supports scheduled or
   batch runs) — generated from `references/orchestrator-contract.md`, the dispatcher
   that scans the queues and starts one worker per task. Keep the Stage B branch that matches
   their config (B1 acceptance-reconciliation when closure is off; B2 closure when on) and
   delete the other. If their environment only runs one task at a time on demand, skip this
   file and tell the user they start the worker per task manually and do the one-step
   acceptance by hand.
5. **`README.md`** — generated from `assets/readme-template.md`, written for a
   non-technical reader: what this loop does, how to queue a task, how to approve or
   reject, and what to do if something looks wrong.
6. **`SETUP.md`** — install / configure / uninstall, generated from
   `assets/setup-template.md`, with only the steps that apply to the user's stack.

Resolve every placeholder. Do not leave `{{...}}` tokens in generated files — an
unresolved placeholder is a setup bug. A few values are not brace-tokens but still must be
set to the user's real choices (the smoke test cannot catch a forgotten one): the
`golive_date` (the acceptance window start), the `result_storage.path`, and the
`accepted_signal`. Confirm these match the user before saving.

## Phase 4 — Credentials, safety, and limits

Before handing the loop over, lock down the unsafe edges. Read
`references/credentials-and-safety.md` and apply it:

- Credentials (API keys, tokens) live in the user's environment or secret store,
  **never** pasted into prompt files or committed to a repo. The generated files
  reference a credential by name; they never contain its value.
- The generated worker prompt must carry the user's hard limits as explicit "do not
  do without asking" rules: no publishing, no outbound messages/email as the user,
  no payments, no deleting significant data, no privilege changes — unless the user
  explicitly allowed it in Phase 1.
- When the agent hits a limit or a missing permission, it must **stop and flag the
  task as blocked with a concrete reason**, not improvise around the limit.

## Phase 5 — Smoke test in a clean run

Verify the generated loop works end to end before declaring success.

1. Run the structural smoke test:
   ```bash
   python3 scripts/smoke_test.py <path-to-generated-loop-folder>
   ```
   It checks the config parses, required files exist, no unresolved `{{placeholders}}`
   remain, and no credential values are inlined. It exits non-zero on any failure.
2. Do a **dry run of one real task**: queue a tiny throwaway task in the user's task
   system, run the worker prompt against it (manually if their environment has no
   scheduler), and confirm the task moves through the states and a result lands in
   the storage destination. Use a harmless task (e.g. "write a two-line summary of
   what this loop does") so nothing risky happens on the first run.
3. Walk the user through what just happened so they understand the moving parts.

If the dry run cannot complete because of a real environment limitation, report the
specific blocker and the smallest change that would unblock it — do not fake success.

## Phase 6 — Activate the automation (host-aware)

The loop is not done when the prompt files exist. The last mile is turning it into something
that actually runs on the user's schedule — and proving it will run there. **Do not hardcode
"create a Routine like this."** You do not know the user's host in advance, so you discover the
environment and *offer the mechanism that fits it*, then verify it works before promising it.

1. **Identify the execution environment** — from the Phase 1 answers plus the host you are
   running in right now. Which class is it: a coding-agent CLI, a desktop AI app, a hosted/cloud
   agent, a self-hosted setup? Separately: **where will the scheduler itself run** (same machine,
   a cloud runner, a CI job)? These can differ, and that difference is where loops break.

2. **Offer the mechanism(s) that fit that environment** — present options, do not impose one.
   Examples of *classes* (pick what the host actually supports, do not invent one):
   - a cloud/cron agent or "Routine" the host offers, **if it can run unattended**;
   - a local "loop on an interval" that runs while a session/process is open;
   - the desktop app's built-in scheduler;
   - a system cron job that invokes the CLI agent.
   Explain the trade-off of each in plain language and let the user choose.

3. **Check feasibility before you promise it (critical).** Confirm that, *in the environment
   where the scheduler will actually run*, the loop's connectors and files are reachable. The
   classic failure: a cloud/headless/cron run has **no interactively-authorized MCP connectors**
   (e.g. the task system) and **cannot see local files** (`worker-prompt.md`, the result folder).
   If that is the case, give an honest fallback — either run the scheduler locally where the
   connectors and files live, or move the prompt files to where the cloud agent can fetch them.
   Never promise an unattended loop that will silently fail on the first run.

4. **Optionally package the orchestrator as a callable command/skill** (e.g. `/<loop-name>`) so
   the scheduler invokes a clean command instead of a raw markdown file, and the loop is portable
   between hosts. Offer this; do not require it.

5. **Record the chosen mechanism** in `loop-config.yaml` (`permissions.schedule`) and write the
   *actual* steps for that environment into `SETUP.md`'s `{{schedule_setup}}` block — the steps
   that fit the identified host, plus the feasibility note and fallback. Not a generic stub.

Done means: a working schedule (or a deliberate, verified manual trigger) — not a folder of
prompt files with "now go set up a scheduler yourself" left to the user.

## Common mistakes

1. **Copying a reference implementation verbatim.** The shipped contracts are
   templates with placeholders, not a finished setup. A loop that hardcodes someone
   else's task manager, paths, or labels will not work for this user. Always resolve
   to *their* stack.
2. **Assuming full automation when the connector is not there.** If the agent cannot
   actually read/write the task system, the loop is "user pastes task → agent works →
   user saves result", not a hands-off loop. Design for what the connectors really
   allow, and say which mode you built.
3. **Leaving placeholders unresolved.** `{{task_system}}` in a generated file means
   the agent will not know what to do. The smoke test catches these; do not skip it.
4. **Putting secrets in prompt files.** Tempting because it "just works", but it leaks
   keys into files the user may share. Always reference credentials by name.
5. **Over-building.** If the user only wants "agent does the task and shows me", do
   not force an independent-reviewer pass and a closure-to-memory step on them. Offer
   the richer loop; let them choose. Match the build to what they actually need.
6. **Promising platforms you cannot verify.** If you are unsure an integration exists
   for the user's tool, say so and offer the manual-handoff fallback instead of
   inventing a connector.
7. **Stopping at prompt files without activating the automation.** Generating the files and
   leaving the user to "go set up a scheduler yourself" is an abandoned last mile. Finish
   Phase 6: take it to a working schedule, or to an explicit, verified fallback.
8. **Forgetting acceptance when closure is off.** Closure (record to memory) is optional;
   acceptance (turn approve/reject into a terminal state) is not. A loop with no memory still
   needs the approve → done / reject → rework step, or `REVIEW` tasks pile up forever.

## Troubleshooting

| Symptom | Likely cause | Fix |
|---------|--------------|-----|
| Agent never picks up tasks | No scheduler/trigger, or no read access to the queue | Use manual start per task, or fix the connector; pick the matching adapter |
| Tasks get stuck "in progress" | Worker crashed without setting a terminal status | Add the post-run reconciliation step from the execution contract |
| Results land nowhere | Storage destination not writable or not set | Set one clear writable path in `loop-config.yaml` |
| Same task processed twice | No idempotency marker on accepted/closed tasks | Use the "closed" marker from the acceptance/closure contract |
| Agent does risky things | Limits not carried into the worker prompt | Re-run Phase 4; make limits explicit "stop and block" rules |
| Smoke test fails on placeholders | A Phase-3 file was generated with `{{...}}` left in | Resolve the placeholder from `loop-config.yaml` and re-run |
| Scheduled/cron run sees no tasks or fails on a connector | Cloud/headless env with no interactive MCP connector or no access to local files | Run the scheduler where the connectors and files live, or move the prompt files where the cloud agent can fetch them (Phase 6, step 3) |
| Approved tasks never leave "review" | Acceptance step missing (closure was off, so nothing handles approve/reject) | Add Stage B Branch B1 to the orchestrator, or document the one-step manual acceptance (approve → done, reject → rework) |

## What this skill ships

```
autonomous-loop-onboarding/
  SKILL.md                       — this file (the onboarding orchestrator)
  references/
    onboarding-interview.md      — the full question bank for Phase 1
    loop-core.md                 — model-agnostic core: states, queue, safety
    execution-contract.md        — execution-worker contract (template)
    acceptance-closure-contract.md — acceptance + closure contract (template)
    orchestrator-contract.md     — orchestrator/dispatcher contract (template, scheduled envs)
    adapters.md                  — adapter catalog + how to choose/compose
    credentials-and-safety.md    — secret handling + safety rules
  assets/
    readme-template.md           — README for the non-technical user
    setup-template.md            — install / configure / uninstall
    adapters/
      adapter-template.md        — blank adapter to fill for any stack
      adapter-generic-files.md   — example: tasks as markdown files in a folder
      adapter-generic-board.md   — example: tasks on a labeled board/tracker
    examples/
      loop-config.example.yaml   — annotated config the user fills in
  scripts/
    smoke_test.py                — clean-environment structural check
```
