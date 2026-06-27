# Adapter — <host name>

> Blank adapter. Fill it for the user's environment. The core never changes; only this does.

## Environment

- **LLM host:** <coding-agent CLI / desktop AI app / self-hosted harness / web chat>
- **File access:** <full read/write to the vault | none (copy-paste only)>
- **Runs unattended:** <yes, on a schedule/trigger | no, only when the user opens it>
- **Sub-agents:** <yes (independent reviewer possible) | no (sequential self-review)>

## How the four skills install

- **startup / closure / distillation / hygiene:** <installed as skills/commands the agent
  triggers | plain prompt files the user pastes | copy-paste blocks (no file access)>

## How routines fire

- **closure-after-task:** <host event | trigger phrase>
- **hygiene-weekly:** <host scheduler | system cron invoking the CLI | desktop app planner |
  manual trigger phrase>
- **index-refresh:** <sub-step of hygiene | cheap daily trigger if available>

## Feasibility note

<Where will the scheduler actually run, and can it reach the vault files there? If a
cloud/headless run cannot see the local vault, say so and give the fallback: run the
scheduler where the files live, or keep routines manual.>

## What this mode does and does not do

<State plainly: full file access vs copy-paste; scheduled vs manual. What would unlock the
next level.>
