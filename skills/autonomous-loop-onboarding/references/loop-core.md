# Loop Core — the model-agnostic engine

This is the part of an autonomous task loop that is the same for everyone, regardless
of which LLM, task manager, or storage they use. Adapters (see `adapters.md`) translate
these abstract concepts into concrete operations in a specific stack. Never put a
specific tool name in the core; keep it abstract here and resolve it in the adapter.

## The idea in one paragraph

A human queues a task. An agent claims exactly one task, raises it to "in progress",
does the work, checks its own output against the task, optionally gets an independent
review, and then hands the task back for human approval. The human approves (done) or
sends it back for rework. Optionally, an approved task is "closed" — its accepted result
is recorded somewhere durable. The human is involved only at "queue" and "approve/reject".

## The five abstract states

Every task in the loop is in exactly one state. Names are abstract here; the adapter
maps each to a real label/column/status in the user's task system.

| Abstract state | Meaning | Who sets it |
|----------------|---------|-------------|
| `QUEUED` | Human marked this task for the agent | Human |
| `IN_PROGRESS` | An agent has claimed it and is working | Agent (worker) |
| `REVIEW` | Agent finished and self-verified; awaiting human approval | Agent (worker) |
| `BLOCKED` | Agent cannot proceed without a human decision/access | Agent (worker) |
| `REWORK` | Human rejected the result; agent should try again | Human |

Plus two optional terminal markers if the user wants a closure step:

| Marker | Meaning |
|--------|---------|
| `CLOSED` | Accepted result has been recorded to durable storage/memory |
| `CLOSURE_ERROR` | Closure step failed; the result is still accepted, only the recording failed |

**Invariant:** a task carries exactly one of these markers at a time. When changing a
task's state, replace the previous marker — do not leave two on the task. If the user's
task system uses labels (where adding a label does not remove the old one), the adapter
must explicitly remove the old marker and add the new one in the same update.

## Acceptance is always needed; closure is optional

Keep these two ideas separate — conflating them is a common design hole:

- **Acceptance** = recognizing the human's approve/reject signal and moving the task to the
  right terminal state. Approve → the task is **done** (completed / terminal). Reject → the task
  goes to **`REWORK`** so the next run re-executes it with the feedback. Acceptance is needed in
  **every** loop, no matter the stack. Without it, a `REVIEW` task and the human's "looks good"
  or "try again" never turn into a state change, and the loop quietly stalls after the first
  hand-back.
- **Closure** = the OPTIONAL extra step of recording an accepted result into a memory/knowledge
  layer (sets `CLOSED`). It only exists when the user has memory and turned it on.

So: a loop with no memory still does acceptance — it just skips closure. Do not assume "no
closure" means "nothing happens after review."

## The two queues per run

A single run of the loop processes two independent queues, in order:

1. **Execution queue** — tasks in `QUEUED` or `REWORK`. For each, the orchestrator
   moves it to `IN_PROGRESS` and starts one execution worker. The worker drives the
   task to `REVIEW` or `BLOCKED`.
2. **Acceptance queue** — tasks the human has acted on after a hand-back. This queue runs in
   one of two modes depending on whether closure is enabled:
   - **Acceptance-reconciliation (closure off, the default).** For each `REVIEW` task the human
     has approved or rejected (per the configured accepted/rejected signal), set the terminal
     state: approve → completed/terminal (remove `REVIEW`), reject → `REWORK`. No memory step, no
     closure worker — a lightweight state move the orchestrator (or the human's manual pass) does
     directly.
   - **Closure (closure on).** For each task the human approved that still carries `REVIEW` and is
     not yet `CLOSED`/`CLOSURE_ERROR`, start one closure worker that records the result to memory
     and sets `CLOSED`.

An empty execution queue does not end the run — the acceptance queue may still have
work. Check both.

## Concurrency

If the environment can run agents in parallel, the orchestrator starts a bounded number
of workers at once (a sane default is 3–4), waits for that wave to finish, then starts
the next wave, until the snapshot taken at the start of the run is fully processed. New
tasks that appear mid-run wait for the next run. If the environment runs one task at a
time, there is no orchestrator — the human (or a trigger) starts one worker per task.

## Isolation

Each worker handles exactly one task in its own context. Do not let one task's context,
decisions, or working state bleed into another. This keeps an off-topic detail from one
task out of another task's result. Execution workers and closure workers are separate and
never share context.

## Report-is-a-signal, not proof

A worker's final report is a *signal* that it finished — it does not by itself prove the
work is correct. The proof is the artifact plus checkable ground truth (file contents,
test results, calculations, sources, system state). If an orchestrator must decide a
task's final state and the worker left it `IN_PROGRESS` (a crash fallback), the
orchestrator must open the artifact and verify against ground truth before promoting to
`REVIEW`; if it cannot confirm, it sets `BLOCKED` with a concrete reason.

## Safety rules (always in effect)

These are non-negotiable defaults. The user may *loosen* a specific one in Phase 1 by
explicitly allowing it; otherwise the agent must not do these without a human:

- No publishing or posting publicly.
- No sending email or messages as the user.
- No payments or purchases.
- No deleting significant data.
- No pushing to a protected/main branch.
- No changing access rights or permissions.
- No legally or reputationally significant external action.
- No editing the user's canonical/long-lived configuration or production assets directly.

When an action would cross one of these lines, the agent produces a ready-to-use **draft**
of the action instead, or sets the task `BLOCKED` with the specific reason — it never
performs the action silently.

## What the core deliberately does NOT specify

- The actual LLM or agent runtime → user's choice, captured in config.
- The actual task system and how states map to it → the adapter.
- The storage location for results → user's choice, captured in config.
- Whether memory/knowledge/skills are consulted → optional, captured in config.
- The schedule/trigger → user's environment, captured in config.

Keep the core pure. Everything tool-specific belongs in the adapter or the config.
