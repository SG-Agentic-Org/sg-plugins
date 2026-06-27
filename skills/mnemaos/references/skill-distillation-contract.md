# Distillation skill — contract (template)

This is the contract for the **distillation** skill: how the agent turns raw material (a long
session, a pile of notes, a document) into clean cards. Resolve the `{{placeholders}}` and
install it. On by default; the user may switch it off.

Lineage: distilled from an "inventory → selection → cards" ingest flow plus a pattern-
extractor. One generalized "distill into cards" skill, not separate book/pattern skills.
Dedup is by `id`/title heuristic, not vector search — infrastructure-free.

---

## Resolved skill body (fill the placeholders)

```markdown
---
name: memory-distillation
description: >
  Turn raw material — a long session, a batch of notes, a document, a transcript —
  into clean, linked cards in the memory vault. Use when the user says "distill this",
  "turn this into cards", "add this to my memory properly", or after ingesting a source
  worth keeping.
---

# Memory distillation

Two beats: inventory, then selection — do not card everything.

1. **Inventory.** Read the raw material and list the distinct entities it contains:
   people, projects, concepts, decisions worth a card. Note for each whether it is
   durable (worth a card) or just an episode (belongs in `inbox.md`).
2. **Dedup before creating.** For each entity that deserves a card, check the vault first:
   - exact: does `{{vault_path}}/{people|projects|cards}/<slug>.md` already exist (the
     `id` matches)? → update it.
   - similar: is there a card whose `title` or `aliases` is a near-match (case-insensitive,
     punctuation-insensitive, or a known alias)? → treat it as the same entity; merge,
     don't make a near-twin. Use `{{vault_path}}/_index.md` to scan titles cheaply.
3. **Write the cards.** Create/update each card with the required frontmatter (id, type,
   title, created, updated, status, tags, links). Set `links` to `[[wikilinks]]` of related
   cards. Write the body in plain prose — claims, examples, distinctions.
4. **Provenance (optional).** {{provenance_block}}
5. **Trust (optional).** {{trust_block}}
6. **Leftovers → inbox.** Material that is a fresh fact but not a durable entity goes as a
   one-line episode in `{{vault_path}}/inbox.md`, not a card.
7. Tell the user which cards you created/updated and which entities you skipped as episodes.
```

---

## How to resolve

- `{{vault_path}}` → the absolute path to the user's vault.
- `{{provenance_block}}` →
  - If the source library / `source_refs` is on: "Record where each card came from in its
    `source_refs` frontmatter (page-level: the source file or URL, not every sentence)."
  - If off: "Skip `source_refs` unless a card clearly distills an identifiable source."
- `{{trust_block}}` →
  - If trust is on: "Set `trust` on cards that are the user's own ideas or unverified
    (`speculative`/`emerging`); leave it off for cards distilled from a solid source
    (`established` is implied)."
  - If off: "Skip the `trust` field."
- Web-only host with no file access: distillation outputs the card text for the user to
  paste; say so.
