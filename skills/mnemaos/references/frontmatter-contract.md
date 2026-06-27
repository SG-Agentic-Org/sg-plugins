# Frontmatter contract — the card format

Every card in the vault carries frontmatter so the agent can index it, dedup it, and know
what it is. This contract is **fixed** — the onboarding does not redesign it. Keep it
minimal: only the fields that earn their place without a sync layer or a retrieval cache.

## Required fields (every card)

```yaml
---
id: <slug>                 # unique; = the filename without .md (kebab-case, lowercase)
type: person|project|concept|decision|note
title: <human-readable title>
created: YYYY-MM-DD
updated: YYYY-MM-DD
status: active|archived
tags: []
links: []                  # [[wikilinks]] to related cards
---
```

- **`id`** must equal the filename (without `.md`). This is what dedup keys on.
- **`type`** is one of the five values above. `note` is the catch-all for anything that is
  not a person, project, concept, or decision.
- **`title`** is for humans and for the similar-title dedup heuristic.
- **`status`** is lifecycle, not trust: `active` or `archived`.
- **`links`** are `[[wikilinks]]` by basename, so Obsidian and the indexer both resolve them.

## Optional fields

Add these only when they help; they are not required and the smoke test does not demand them.

```yaml
aliases: []                # other names this entity is known by (helps dedup)
source_refs: []            # page-level provenance: where this card's content came from
trust: established|emerging|speculative   # how much to trust this card's content
```

### `source_refs` — page-level provenance (optional)

When a card's content is distilled from a source (a document, a transcript, a web page, a
RAW file in the optional source library), record where it came from — at the **page level**,
one list per card. This is *not* claim-level tracing of every sentence; it is "this card
draws on these sources", which is enough to find your way back to the original.

```yaml
source_refs:
  - "RAW/deep-work-cal-newport.md"        # a file in the optional source library
  - "https://example.com/the-original-article"
  - "Meeting notes 2026-06-20"
```

Use it when the user turned on the optional source-library / RAW-Wiki frame
(`optional-modules.md`), or any time a card is a distillation of an identifiable source.
Skip it for cards that are just the user's own working notes — they have no external source
to trace.

### `trust` — content confidence (optional)

Lifecycle (`status`) and trust are different axes. `status` says how complete the card is;
`trust` says how much to believe its content:

- **established** — well-sourced, multiple supporting sources, low contradiction.
- **emerging** — a single source or thin evidence, but worth keeping.
- **speculative** — the user's own thinking or an unverified claim, flagged for follow-up.

`trust` is most useful for the user's **own ideas and unverified material** — exactly where
"my hypothesis" vs "from a trusted source" matters. For cards distilled straight from a
solid source it is usually `established` and adds little. Default behavior: set `trust` on
own-idea / speculative cards; leave it off elsewhere unless the user wants it everywhere.

## Why these and not more

A maximal memory card can carry sync flags, data-sensitivity classes, disclosure rules,
precision policies, source hashes, retrieval triggers, priority scores. Those exist to
serve **cross-device sync and a privacy projection** — when memory leaves the machine.
MnemaOS has no sync and no projection, so those fields would be dead weight a user has to
maintain for no benefit. They are out of scope for this package. Keep cards readable by a
human at a glance.
