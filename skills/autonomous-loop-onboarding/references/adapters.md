# Adapters — translating the core into a specific stack

The loop core (`loop-core.md`) is abstract on purpose. An **adapter** maps the abstract
concepts to concrete operations in one user's tools. This is the only place tool names
belong. Pick an adapter that matches the user's task system, or compose a new one from
`assets/adapters/adapter-template.md`.

## What an adapter must define

For a given task system + LLM host, the adapter answers these:

| Abstract concept | What the adapter must specify |
|------------------|-------------------------------|
| The queue | How to list tasks in `QUEUED` / `REWORK` |
| Claim a task | How to set `IN_PROGRESS` |
| The five states | The real label / column / status / field for each |
| Marker replacement | How to remove the old marker and set the new one in one update |
| Read a task | How to read title, description, comments, attachments |
| Comment on a task | How to record the hand-back note |
| The accepted signal | What human action means "approved" (complete, label, move) |
| Storage | How the agent writes results to the destination |
| Trigger | Manual start, scheduler, or platform automation |

## Choosing the automation level

The adapter is bounded by what the connector allows (Interview Dimension 3):

- **Full** — the host can read and write the task system programmatically. The orchestrator
  and workers run hands-off.
- **Assisted** — the host can write results but not move task states. The agent does the work
  and saves; the human moves states by hand.
- **Manual handoff** — no task-system integration. The human pastes the task and saves the
  result; the agent only does the work. The "states" become a lightweight checklist the human
  follows, and result storage is a plain folder.

Always tell the user which level you built and what would unlock the next one.

## Two worked example adapters (in `assets/adapters/`)

These are concrete, copyable examples — not the only options. They are intentionally generic
(no specific vendor required) so they work in almost any environment.

### 1. `adapter-generic-files.md` — tasks as markdown files in folders

Zero integrations needed. Tasks are markdown files; the state is the subfolder they sit in
(`queued/`, `in-progress/`, `review/`, `blocked/`, `rework/`, `closed/`). Moving a file
between folders is a state change. Works with any LLM host that can read/write local files —
the lowest-common-denominator setup, and a great first loop for a non-technical user.

### 2. `adapter-generic-board.md` — tasks on a labeled board / tracker

For any task system that exposes tasks with **labels/tags** or **columns/statuses** through a
connector or API. States map to labels or columns; marker replacement removes the old label
and adds the new one in a single update. Filling in the two or three real API calls (list,
update, comment) for the specific tool turns this into a full adapter for that tool.

## Composing a new adapter

If neither example fits, copy `assets/adapters/adapter-template.md` and fill every row of the
table above with the user's real operations. Test each operation once by hand (can you list,
claim, read, comment, set each state, and write a result?) before wiring it into the loop. A
half-working adapter produces tasks stuck mid-state, which is the most common failure mode.

## Keep the core clean

Never edit `loop-core.md`, `execution-contract.md`, or `acceptance-closure-contract.md` to add
a tool name. Those stay abstract. All tool-specific detail lives in the adapter and in the
generated `loop-config.yaml`. This is what lets the same loop be re-pointed at a different tool
later by swapping only the adapter.
