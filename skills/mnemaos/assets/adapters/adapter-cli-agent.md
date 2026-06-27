# Adapter — coding-agent CLI on the user's machine

> Example adapter for a command-line coding agent (a CLI that reads/writes local files and
> can run shell commands). One of the most capable hosts for MnemaOS.

## Environment

- **LLM host:** coding-agent CLI on the user's machine
- **File access:** full read/write to the vault
- **Runs unattended:** usually yes — via a host routine, or a system cron invoking the CLI
- **Sub-agents:** usually yes — an independent reviewer pass in closure is available

## How the four skills install

- Install startup / closure / distillation / hygiene as **skills the agent discovers** (in
  the agent's skills directory), each resolved with the absolute `vault_path` and the user's
  limits. The agent triggers startup at session start and the others by their phrases.

## How routines fire

- **closure-after-task:** the user says the trigger phrase after a task, or a host hook fires
  closure on task completion if available.
- **hygiene-weekly:** a host routine on a weekly schedule, or a system cron entry that invokes
  the CLI agent with the hygiene skill weekly.
- **index-refresh:** the first sub-step of hygiene; `python3 scripts/index_vault.py <vault>`.

## Feasibility note

The scheduler runs on the same machine as the vault, so it can reach the files — the common
failure (a cloud run that cannot see local files) does not apply here. Confirm the cron/host
routine actually has the agent's credentials and the vault path at run time.

## What this mode does and does not do

Full file access and (usually) real scheduling — the richest mode. The agent reads and writes
the vault directly; routines can run unattended. No copy-paste needed.
