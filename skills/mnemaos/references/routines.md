# Routines — catalog and automation-level mapping

A routine is a periodic automation. Which ones to turn on depends on the **automation level**
the user's environment supports (dimension 5). The mechanism is the adapter's job (Phase 6);
this file is the catalog and the mapping rule.

## The catalog

| Routine | Suggested schedule | What it does | Manual fallback |
|---------|-------------------|--------------|-----------------|
| **closure-after-task** | on a task finishing | Run the closure skill | The user says a trigger phrase ("close this out") after a task |
| **hygiene-weekly** | weekly | Run hygiene: refresh index (first sub-step), broken links, duplicates, budgets | The user runs it by hand once a week |
| **index-refresh** | sub-step of hygiene-weekly | Run `index_vault.py`, regenerate `_index.md` | Always part of hygiene; separate only if the host gives a cheap daily trigger |
| **profile-refresh** (optional) | monthly | Fold recent episodes/decisions into a compact `profile.md` / `_start-here.md` | The user runs it when context grows stale |

Index-refresh is **the first sub-step of hygiene-weekly**, not its own routine — unless the
host offers a cheap daily trigger and the user wants the index fresher than weekly.

## Mapping automation level → routines

Every routine **degrades to a manual trigger**. That is the honest floor: the minimum
viable system is closure + hygiene run by a trigger phrase, with no scheduler at all.

- **Unattended scheduling available** (the host can run on a schedule and reach the vault
  files): offer hygiene-weekly on a schedule and closure on the task-finish event. Confirm
  the schedule can actually reach the local vault (Phase 6, step 3) before promising it.
- **Manual only** (the host runs only when the user opens it, or it is a web chat with no
  file access): do not promise a schedule. Generate the routines as trigger phrases the user
  says, and document them in the README and SETUP. Be explicit that they are manual.

Never promise an unattended routine that will silently fail because the scheduler cannot see
the user's files. An honest manual trigger beats a broken automation.
