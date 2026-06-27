# Closure skill — contract (template)

This is the contract for the **closure** skill: how the agent turns a finished piece of work
into durable memory. Resolve the `{{placeholders}}` and install it. Always install this skill.

Lineage: distilled from a session-closure flow + the "where does this go" decision tree.
Deliberately local-only: it writes to the vault, with no projection, no sync, no external
index.

---

## Resolved skill body (fill the placeholders)

```markdown
---
name: memory-closure
description: >
  After finishing a piece of work, record what is worth remembering into the user's
  memory vault. Use when the user says "close this out", "save this", "we're done",
  "record this", or when a task is finished and there is durable context to keep.
---

# Memory closure

When a piece of work is done, decide what (if anything) is worth keeping, then write it.

1. **Update the task's own file** if it has one (a project README, a working doc): note the
   outcome and the date.
2. **Record an episode.** Append a short, dated line to `{{vault_path}}/inbox.md` capturing
   the fresh fact(s) from this session. One or two lines — the raw signal, not a polished
   card.
3. **Route durable items** using the decision tree:
   - An architecture/policy choice → append one entry to `{{vault_path}}/decisions.md`.
   - A repeating mistake / anti-pattern → add a lesson to `{{vault_path}}/lessons.md`
     (respect its size budget; do not add tactical noise).
   - A durable person/project/concept appeared or changed → create or update a card in
     `{{vault_path}}/people/`, `projects/`, or `cards/`. Before creating, check for an
     existing card (exact `id`, then similar `title`/aliases) and update it instead of
     making a duplicate.
   - Nothing durable (a one-off tactical edit) → the episode in `inbox.md` is enough; do
     not manufacture a card.
4. **Respect the limits.** {{safety_limits}} If recording would require one of these, stop
   and tell the user — do not do it silently.
5. {{independent_review_block}}
6. Tell the user, in one or two lines, what you recorded and where. Do not write durable
   memory in chat only — if it matters, it goes in a file.
```

---

## How to resolve

- `{{vault_path}}` → the absolute path to the user's vault.
- `{{safety_limits}}` → the user's hard limits as a sentence, e.g. "Never publish, send
  messages/email as the user, make payments, or delete files without asking."
- `{{independent_review_block}}` →
  - If the user wants an **independent reviewer pass** *and* the host supports sub-agents:
    "Before recording anything beyond the inbox episode, spawn a fresh reviewer agent that
    did not see your reasoning; give it the work and the proposed memory writes; apply its
    corrections, then record."
  - Otherwise (no review, or no sub-agents): "Re-read your proposed memory writes once with
    fresh eyes before saving." (a sequential self-check) — or remove the step if review is off.
- If the host has **no file access** (web-only chat): closure becomes a copy-paste block —
  the agent outputs the episode/decision/card text and the user pastes it into the right
  file. Say so; do not pretend it wrote the file.
