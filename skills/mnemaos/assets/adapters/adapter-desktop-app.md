# Adapter — desktop AI app with a skill catalog and scheduler

> Example adapter for a desktop AI application that has a skill/command catalog, can read and
> write local files through the app, and has a built-in scheduler/routines feature.

## Environment

- **LLM host:** desktop AI app with installed skills and a built-in planner
- **File access:** read/write to the vault through the app
- **Runs unattended:** yes, via the app's built-in scheduler/routines
- **Sub-agents:** depends on the app — check before promising an independent reviewer pass

## How the four skills install

- Install startup / closure / distillation / hygiene as **skills in the app's catalog**,
  resolved with the vault path and limits. The user triggers them by phrase; startup can be
  set to run at session start if the app supports it.

## How routines fire

- **closure-after-task:** trigger phrase, or an app automation on task completion if offered.
- **hygiene-weekly:** the app's built-in scheduler runs the hygiene skill weekly.
- **index-refresh:** first sub-step of hygiene. If the app cannot run Python, the hygiene
  skill rebuilds `_index.md` by reading the vault directly instead of calling the script.

## Feasibility note

Confirm the app's scheduler can reach the local vault folder at run time (some apps sandbox
file access). If a scheduled run cannot see the vault, fall back to manual triggers and say so.

## What this mode does and does not do

File access through the app and scheduled routines via the planner. Check sub-agent support
before promising an independent reviewer pass; otherwise closure uses a sequential self-check.
