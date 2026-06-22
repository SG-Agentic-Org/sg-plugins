# Adapter — tasks on a labeled board / tracker

For any task system that exposes tasks through a connector or API and supports either
**labels/tags** or **columns/statuses**. This covers most task managers, issue trackers, and
kanban boards. Fill in the two or three real API calls for the specific tool to turn this into
a full adapter for it.

## Identity

- **Task system:** a board/tracker with labels or columns, reachable via connector/API
- **LLM host:** any host that can call that connector/API
- **Automation level:** full if the API allows read + write of tasks and labels; assisted if it
  is read-only (then the human moves states)

## State representation

Choose ONE mapping that the tool supports:

- **Label mapping:** each state is a label — `queued`, `in-progress`, `review`, `blocked`,
  `rework`, `closed`. Because adding a label does not remove others, every state change must
  **remove all loop-state labels and add exactly the new one**, keeping the user's own labels.
- **Column mapping:** each state is a column/status — Queued, In Progress, Review, Blocked,
  Rework, Done/Closed. Moving the card sets the state; only one column at a time, so no double
  markers.

Pick label OR column based on what the tool models natively. Record which in `loop-config.yaml`.

### Trigger label vs. queued state (label systems only — read before you wire it)

In a label system the user usually marks a task for the AI with a single tag — call it `@ai`.
There are two valid ways to relate that trigger tag to the `queued` state, and they behave
differently. Pick one **explicitly** and write it into the config; not deciding is the source of
the classic "two state labels at once" bug and of the trigger tag silently disappearing.

- **Pattern A — trigger tag *is* the queued state.** `@ai` means QUEUED. When the worker
  claims the task it **removes `@ai`** and adds `in-progress`. Simple, but once claimed the task
  no longer shows it belongs to the AI, and "all my AI tasks" is no longer one saved filter.
- **Pattern B — trigger tag is a persistent ownership marker (recommended).** `@ai` stays on the
  task for its **whole lifecycle** and is never removed by the loop. The *stage* is carried by a
  separate state label (`in-progress`/`review`/`blocked`/`rework`/`closed`). A task is QUEUED when
  it has `@ai` **and no state label yet**. This keeps "everything the AI owns" as one stable
  filter and makes the marker-replacement rule unambiguous: replacement only ever swaps the
  **state** label and **always preserves `@ai`** (and the user's own labels).

Recommend **Pattern B** for any system where the user naturally thinks of the tag as "this one is
for the AI" (Todoist, Linear, GitHub issues, most trackers). Under Pattern B, every marker
replacement = (current labels − all loop *state* labels) + new state label, with `@ai` and the
user's labels untouched. Record the chosen pattern in `loop-config.yaml` (e.g. a note on
`task_system.states.queued`).

## Operations (fill the bracketed calls for the specific tool)

| Abstract operation | Concrete operation |
|--------------------|--------------------|
| List `QUEUED` / `REWORK` | query tasks where state-label ∈ {queued, rework} (or in those columns) |
| Read a task | read task by id: title, description, comments, attachments |
| Claim → `IN_PROGRESS` | update task: remove old state, set `in-progress` |
| Set `REVIEW` / `BLOCKED` | update task: replace state marker with `review` / `blocked` |
| Set `CLOSED` / `CLOSURE_ERROR` | update task: replace state marker with `closed` / `closure-error` |
| Marker replacement | one update call that sets the full label list = (current labels − all loop states) + new state |
| Comment / hand-back note | add a comment to the task with the hand-back summary |
| Accepted signal | the human completes the task (or applies a `done` label) while `review` is still set |
| Write a result | write to the configured storage path; link or note it in the task comment |
| Trigger | manual run, the host's scheduler, or the tool's own automation if available |

## Why marker replacement matters here

In label-based systems the classic bug is a task ending up with both `in-progress` and `review`.
The fix is to always compute the **full new label set** and replace the whole list in one update,
never to "add" a state label. Spell out that exact update call when you fill this in.

## Credentials

- Usually needs an API token. Store it as env var `TASK_API_TOKEN` (name in config; value in the
  environment/secret store, never in any file).
- Request least privilege: read-write on the one project the loop uses, not the whole account.

## Hand-check before going live

By hand, once: list a task ✓, read it ✓, set each state via the replacement call ✓ (confirm only
one state marker remains), add a comment ✓, write a result ✓. Then wire it into the loop.
