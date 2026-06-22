# Adapter Template — fill this in for any stack

Copy this file and fill every row for the user's task system + LLM host. Test each
operation once by hand before wiring it into the loop. Keep all tool names here — never
in the core or the contracts.

## Identity

- **Task system:** <name>
- **LLM host:** <name>
- **Automation level:** full | assisted | manual  (see `references/adapters.md`)

## Operations (fill the right column)

| Abstract operation | Concrete operation in this stack |
|--------------------|----------------------------------|
| List `QUEUED` / `REWORK` tasks | <how> |
| Read a task (title, description, comments, attachments) | <how> |
| Claim a task → set `IN_PROGRESS` | <how> |
| Set `REVIEW` | <how> |
| Set `BLOCKED` | <how> |
| Set `CLOSED` (if closure enabled) | <how> |
| Set `CLOSURE_ERROR` (if closure enabled) | <how> |
| Marker replacement (remove old state, add new, keep user labels) | <how> |
| Comment on a task (hand-back note) | <how> |
| Accepted signal (what human action = approved) | <how> |
| Write a result to storage | <how> |
| Trigger a run (manual / schedule / automation) | <how> |

## State representation

How is each abstract state shown in this system? (label, column, status field, subfolder)

- `QUEUED` → ...
- `IN_PROGRESS` → ...
- `REVIEW` → ...
- `BLOCKED` → ...
- `REWORK` → ...
- `CLOSED` → ... (if enabled)
- `CLOSURE_ERROR` → ... (if enabled)

## Marker-replacement note

If this system uses labels (adding a label does not remove the old one), the update that
changes state must **remove every loop state label and add exactly the new one**, preserving
the user's own non-loop labels. Spell out the exact call here so a worker cannot leave two
state markers on one task.

## Credentials

- Credential needed: <yes/no, which>
- Stored as: env var `<NAME>` / OS keychain / host secret manager  (value never in this file)
- Least-privilege scope requested: <scope>

## Hand-check before going live

Confirm by hand, once: list ✓ · read ✓ · claim ✓ · comment ✓ · set each state ✓ · write
result ✓. A half-working adapter leaves tasks stuck mid-state — the most common failure.
