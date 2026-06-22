# Your Autonomous Task Loop

> This README is generated for the user during onboarding (Phase 3). Resolve the
> `{{placeholders}}` from `loop-config.yaml` and remove this quote block before handing
> it over. Write it for someone who is NOT technical.

## What this is

You now have an AI helper that does tasks for you. You put a task in one place, the AI
picks it up, does the work, checks it, and hands it back for you to approve. You are only
involved twice: when you add the task, and when you say "yes, this is good" or "try again".

Think of it like a capable assistant who takes a ticket, does the job, double-checks their
own work, and leaves it on your desk for a quick sign-off.

## The pieces (in plain words)

- **Where you put tasks:** {{task_system}}.
- **How you mark a task for the AI:** {{how_to_queue}}.
- **Where finished work shows up:** {{result_storage}}.
- **How often it runs:** {{schedule_plain}}.

## How to use it day to day

1. **Add a task.** {{how_to_queue}}. Describe what you want as the result — the clearer the
   request, the better the output.
2. **Let it run.** {{run_plain}}  <!-- "It runs on its own every morning" OR "Start it
   yourself by …" -->
3. **Review.** When a task shows up as **ready for review** ({{review_plain}}), open the
   result in {{result_storage}} and the note the AI left on the task.
4. **Approve or send back.** If it is good, {{approve_plain}}. If not, {{rework_plain}} and
   the AI will try again, using your feedback.

## When the AI stops and asks ("blocked")

Sometimes the AI will mark a task **blocked** instead of finishing it. That is on purpose —
it means the task needs a decision only you can make, or it would require doing something it
is not allowed to do on its own (like sending a message as you or spending money). Read the
note it left, make the call, and re-queue the task.

## What the AI will NOT do on its own

For your safety, the AI will never do these without asking you first:

{{safety_limits_plain}}

If a task would need one of these, the AI prepares a draft and stops, so you stay in control.

## If something looks wrong

- **Nothing gets picked up:** the AI may not be running, or may not be able to see your
  task list. See `SETUP.md`.
- **A task is stuck "in progress":** it was interrupted. Re-queue it; the next run will
  pick it up again.
- **The result is in the wrong place:** check the storage location in `loop-config.yaml`.
- **Anything else:** open `SETUP.md` for troubleshooting, or re-run onboarding to adjust
  your setup.

## Files in this folder

> When generating this README, list only the files that were actually created for this
> user, and delete the lines for optional files they did not get.

- `loop-config.yaml` — your settings (what tools you use, where results go, your limits).
- `worker-prompt.md` — the instructions the AI follows for each task.
- `acceptance-closure-prompt.md` — (only if you chose the closure step) how approved tasks
  get recorded to memory.
- `orchestrator-prompt.md` — (only if your AI runs on a schedule) runs the whole queue.
- `SETUP.md` — how to install, change, and remove this loop.
