# Acceptance & Closure Contract (template)

This covers two things:

- **Acceptance** — how the loop recognizes that a human approved a result.
- **Closure** — the OPTIONAL step that records an accepted result into durable memory.

Closure only applies if the user has a memory/knowledge layer (Interview Dimension 5) and
wants accepted results recorded. **Acceptance always applies** — even with no memory, the loop
must still turn the human's approve/reject into a terminal state.

- If closure is **off** (the common case): you do NOT generate this file as a closure-worker
  prompt. But acceptance still has to happen — see **"Acceptance without closure"** just below
  for its minimal form, which the orchestrator (Stage B, Branch B1) or the human's manual pass
  performs directly. There is no separate closure worker.
- If closure is **on**: generate `acceptance-closure-prompt.md` from the closure-worker contract
  further down, with placeholders resolved.

The `{{double-brace}}` tokens are filled from `loop-config.yaml` during Phase 3. Resolve all
of them before saving as `acceptance-closure-prompt.md`.

## Acceptance without closure (no memory layer — the minimal form)

When there is no memory step, acceptance is a tiny state move, not a worker. It still must be
specified, or approved/rejected tasks never leave `REVIEW`. The rule:

- A `REVIEW` task the human **approved** (their accepted signal) → move it to the terminal/done
  state: remove the `REVIEW` marker (mark complete or set the done state per the adapter), keep
  the user's own labels. Nothing is recorded anywhere.
- A `REVIEW` task the human **rejected** (their rejected signal, e.g. a `rework` label or a "try
  again" comment) → replace `REVIEW` with `REWORK` so the next execution pass re-runs it with the
  feedback.
- A `REVIEW` task with no approve/reject signal yet → leave it; it is still waiting for the human.

That is the whole acceptance step when closure is off. In a scheduled setup the orchestrator's
Stage B Branch B1 does exactly this; in an on-demand setup the human does it by hand (or the
adapter's accepted-signal already *is* the terminal action, e.g. completing the task).

## Acceptance — recognizing approval

The human's "accepted" signal is whatever they chose in the interview. The most robust
default is: **the human marks the task complete in their task system, and the `REVIEW`
marker is still on it.** That combination means "the result was approved; you may close it."

Distinguish carefully:

- A task that is **still active** with `REVIEW` is NOT accepted — it is waiting for the
  human to look at it. Do not close it.
- A task that is **completed/approved** AND still carries `REVIEW` IS accepted — close it.
- A task already marked `CLOSED` or `CLOSURE_ERROR` is done — do not reprocess it.

If the user picked a different signal (e.g. a `done` label), substitute that for "completed"
above; the logic is the same.

To build the acceptance queue: select tasks that carry `REVIEW`, were accepted within the
window since the loop went live ({{golive_date}} — a fixed start, not a rolling window, so a
task is not lost if the loop does not run for a few days), and are not already `CLOSED` /
`CLOSURE_ERROR`. Process one closure worker per accepted task.

## CLOSURE WORKER CONTRACT (resolve placeholders, give verbatim to the closure worker)

You are closing ONE accepted task — recording its approved result into durable memory. You
are NOT the executor and NOT an editor of the result's content. Closure is about recording,
not redoing.

1. Read the accepted task and all its comments via {{task_read_method}}. The source of truth
   is the saved result plus the task record — not any old working transcript (there is none
   to recover).
2. From the worker's hand-back comment, locate the final result folder and the accepted
   artifacts under {{result_storage}}.
3. Do NOT change the result's content. Do NOT re-run the execution work. Do NOT invent new
   durable lessons from your own reasoning.
4. Record the accepted result into the user's memory layer using {{closure_method}}
   <!-- e.g. "run the user's memory-ingest step / skill" or "append a structured entry to
   the knowledge-base index". -->. Update the result's README/notes to reflect acceptance.
5. Confirm the required closure steps actually completed (memory entry written; index/notes
   updated). An updated README alone does NOT mean closure succeeded — verify the memory
   recording step finished.
6. ONLY after every required step succeeds, in this order: (a) add a short comment that
   closure is done and what was recorded; (b) as the LAST changing action, replace `REVIEW`
   with `CLOSED` (remove old marker, add `CLOSED`, keep the user's labels). After setting
   `CLOSED`, write nothing further — `CLOSED` is the single idempotency marker of full
   success, set strictly last so a re-run never double-closes.
7. If closure fails (a step errored, an artifact is missing): leave the task accepted, set
   `CLOSURE_ERROR` instead of `CLOSED`, and comment the concrete failing step. Do NOT reopen
   the task or send it back to execution — a closure failure is a memory-recording problem,
   not a rejection of the result.

Your final message: `{ task_id, outcome (CLOSED|CLOSURE_ERROR), failing_step_if_error,
what_was_recorded }`.

## Why closure is set last and is idempotent

If a closure worker crashes without setting `CLOSED` or `CLOSURE_ERROR`, the task stays
accepted-with-`REVIEW`, and the next run safely retries it. Because `CLOSED` is the very last
action and the recording step is the gate, a retry cannot record twice or skip the marker.
This is what makes the closure queue safe to run repeatedly.

## Placeholder reference

| Placeholder | Filled from config | Example resolution |
|-------------|--------------------|--------------------|
| `{{golive_date}}` | `loop.golive_date` | "2026-07-01" |
| `{{task_read_method}}` | adapter | "the task API read call" |
| `{{result_storage}}` | `result_storage.path` | "the `~/work/ai-results/` folder" |
| `{{closure_method}}` | `memory.ingest_method` | "run your memory-ingest skill", "append to KB index" |
