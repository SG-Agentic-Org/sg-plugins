# Startup skill — contract (template)

This is the contract for the **startup** skill: how the agent reads memory at the beginning
of a session so it "already knows" the user. Resolve the `{{placeholders}}` to the user's
real values and install it where their agent finds skills. Always install this skill.

Lineage: distilled from a "read the compact profile + entry point, pull detail on demand"
pattern. Deliberately simpler than a session-start hook or a retrieval search — startup is a
**skill the agent applies**, reading plain files. No injection, no vector search.

---

## Resolved skill body (fill the placeholders)

```markdown
---
name: memory-startup
description: >
  At the start of a working session, load the user's memory so you act as if you
  already know them. Use at the beginning of any session, or when the user says
  "load my context", "what are we working on", or starts work without giving context.
---

# Memory startup

At the start of a session, before doing the user's task:

1. Read `{{vault_path}}/_start-here.md`. It tells you who the user is, their active
   projects, the key people, and the rules for this vault. This is your map.
2. Do NOT load the whole vault. Read only `_start-here.md` now. Pull detail on demand:
   when the task touches a project or person, open that specific file
   (`{{vault_path}}/projects/<slug>.md`, `{{vault_path}}/people/<slug>.md`), using
   `{{vault_path}}/_index.md` to find what exists.
3. Briefly confirm you have the context — e.g. one line: "Loaded: you're <role>, active
   on <projects>." — so the user sees the memory worked. Keep it short.
4. Then do the task, using the loaded context. When relevant detail is missing from
   `_start-here.md`, open the specific file rather than guessing.

Do not invent facts about the user. If `_start-here.md` does not cover something the task
needs, open the relevant card; if it still is not there, ask — do not fabricate.
```

---

## How to resolve

- `{{vault_path}}` → the absolute path to the user's vault (`vault.path` in config).
- If the host has **no file access** (web-only chat): the "skill" becomes a **copy-paste
  block** the user pastes at the start of a chat, with the contents of `_start-here.md`
  pasted in (or attached). Say so plainly; do not pretend the agent reads the file.
- If the host supports installed skills/commands: install this as a skill the agent triggers
  at session start (or that the user invokes with a phrase like "load my context").
