# Adapters — catalog and how to choose

The core (memory model, card contract, four skills) is the same for everyone. The **adapter**
is the part that depends on the user's environment: which LLM host runs the skills, how
routines fire, and whether the host can touch local files. Pick the matching adapter, or
compose one from the template. The core never changes; only the adapter does.

## What an adapter decides

1. **File access** — can the agent read/write the vault directly, or is it a web chat where
   the user pastes content in and out? This is the biggest fork. No file access → the four
   skills become copy-paste blocks, and no routine can be scheduled.
2. **How skills install** — as installed skills/commands the agent triggers, as plain prompt
   files the user pastes, or as a command the host registers.
3. **How routines fire** — a host scheduler, a system cron invoking the CLI, the desktop
   app's planner, or manual trigger phrases.
4. **Sub-agents** — does the host support an independent reviewer pass, or is it sequential
   self-review?

## The shipped adapters

- `assets/adapters/adapter-template.md` — blank adapter; fill it for any host.
- `assets/adapters/adapter-cli-agent.md` — a coding-agent CLI on the user's machine: full
  file access, skills as files, routines via system cron or a host routine, sub-agents
  usually available.
- `assets/adapters/adapter-desktop-app.md` — a desktop AI app with a skill catalog and a
  built-in scheduler: file access via the app, skills installed in the app, routines via the
  app's planner.

## How to choose

1. Match the user's Phase-1 dimension-2 answer to the closest shipped adapter.
2. If it is a **web-only chat with no file access**, there is no shipped adapter for full
   automation — compose the manual/copy-paste adapter from the template, and be explicit that
   the system runs by the user pasting context and saving outputs by hand. This is a fully
   valid mode; it is just honest about the constraint.
3. If no adapter fits, build one from `adapter-template.md`. Do not bend the core to the host.

Always tell the user which mode you built (full file access vs copy-paste) and what would
unlock the next level (e.g. "a host with local file access would let the agent write to the
vault itself instead of you pasting").
