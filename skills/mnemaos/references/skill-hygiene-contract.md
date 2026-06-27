# Hygiene skill — contract (template)

This is the contract for the **hygiene** skill: how the agent keeps the memory from rotting.
Resolve the `{{placeholders}}` and install it. On by default; the user may switch it off.

Lineage: distilled from a deterministic lint+index maintainer + a long-lived-doc auditor + a
batch candidate-reviewer. The deterministic part runs as a script (`index_vault.py`); the
judgement part is an LLM pass over the flags. **It flags; it does not silently rewrite.**

---

## Resolved skill body (fill the placeholders)

```markdown
---
name: memory-hygiene
description: >
  Periodically tend the memory vault: refresh the index, find broken links, find
  duplicate cards, find stale or oversized files, and flag them. Use weekly, or when
  the user says "tidy my memory", "run hygiene", "check the vault", or "audit my notes".
---

# Memory hygiene

Run these in order. Flag findings; do not silently rewrite the user's memory.

1. **Refresh the index (deterministic, first).** Run:
   `python3 {{package_path}}/scripts/index_vault.py {{vault_path}}`
   This regenerates `{{vault_path}}/_index.md` and reports broken `[[wikilinks]]`,
   cards missing required frontmatter, and orphan files. This step needs no judgement.
2. **Duplicates.** Scan card titles/aliases for near-matches (the same heuristic
   distillation uses). List likely duplicate pairs for the user to merge — do not merge
   automatically.
3. **Stale / contradictory.** Flag cards not updated in a long time whose `status` is
   still `active`, and any pair of cards that plainly contradict each other.
4. **Budgets.** If `{{vault_path}}/lessons.md` (or another budgeted file) has grown past
   its budget, flag it and suggest which entries to cut or promote — do not cut silently.
5. **Report.** Write a short findings list (in chat, or to a dated note if the user wants a
   record). Each finding is a flag plus a suggested fix the user can accept or decline.
6. **Respect the limits.** {{safety_limits}} Hygiene never deletes a file on its own.
```

---

## How to resolve

- `{{vault_path}}` → the absolute path to the user's vault.
- `{{package_path}}` → where the MnemaOS package (with `scripts/`) lives, so the script
  path resolves. If the host cannot run Python, drop step 1's script call and have the agent
  rebuild `_index.md` by reading the vault directly (slower, but works); say which mode applies.
- `{{safety_limits}}` → the user's hard limits as a sentence.
- Scheduling: hygiene is the natural weekly routine. Index-refresh is its first sub-step, not
  a separate routine, unless the host offers a cheap daily trigger and the user wants it. See
  `routines.md`.
- Web-only host: hygiene becomes a manual "read the vault and flag issues" pass; the script
  step is skipped; say so.
