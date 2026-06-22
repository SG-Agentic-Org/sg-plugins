# Adapter — tasks as markdown files in folders

The simplest possible loop: no integrations, no API tokens. Tasks are markdown files, and a
task's state is **the subfolder it sits in**. Moving a file from one folder to another is a
state change. Works with any LLM host that can read and write local files. This is the best
first loop for a non-technical user.

## Identity

- **Task system:** a local folder of markdown task files
- **LLM host:** any host that can read/write files
- **Automation level:** assisted by default (the human moves files between folders unless the
  host can run on a schedule and move files itself, which makes it full)

## Folder layout

```
loop/
  queued/         # you drop a task file here to queue it
  in-progress/    # the agent moves it here while working
  review/         # the agent moves it here when done; you review
  blocked/        # the agent moves it here if it needs you
  rework/         # you move it here to send it back
  closed/         # (optional) closed/recorded tasks
  results/        # finished work lands here
```

A task file is plain markdown: a title line, a description, and optional notes. Example:

```markdown
# Summarize the Q3 vendor list

Read vendors.csv in results/inputs/ and write a two-paragraph summary of the top 5 by spend.
```

## Operations

| Abstract operation | Concrete operation |
|--------------------|--------------------|
| List `QUEUED` / `REWORK` | list files in `queued/` and `rework/` |
| Read a task | read the markdown file (and any linked files) |
| Claim → `IN_PROGRESS` | move the file from `queued/` (or `rework/`) to `in-progress/` |
| Set `REVIEW` | move the file to `review/` |
| Set `BLOCKED` | move the file to `blocked/` |
| Set `CLOSED` | move the file to `closed/` |
| Marker replacement | a file lives in exactly one folder, so moving it IS the replacement — no double markers possible |
| Comment / hand-back note | append a `## Agent note` section to the task file, and/or write a README in the result folder |
| Accepted signal | you move the reviewed file into `closed/` yourself (or, with closure off, just delete/archive it) |
| Write a result | create a human-named, dated subfolder in `results/` and write the output there |
| Trigger | manual (you start the agent), or a scheduler that runs the agent and lets it move files |

## State representation

State = subfolder. Because a file can only be in one folder at a time, the "exactly one marker"
invariant is automatic — there is nothing to get wrong.

## Credentials

None. This adapter needs no API tokens.

## Hand-check before going live

Drop one tiny task in `queued/`, run the worker prompt, and confirm the file ends up in
`review/` with a result in `results/`. If it does, the loop works.
