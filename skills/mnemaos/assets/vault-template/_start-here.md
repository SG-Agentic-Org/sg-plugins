---
id: start-here
type: note
title: Start here — vault entry point
created: {{date}}
updated: {{date}}
status: active
tags: [meta, entry-point]
links: []
---

# Start here

> This is the first file the agent reads at the start of a session. Keep it compact — it is
> a map, not the whole memory. Detail lives in the linked files; pull it on demand.

## Who I am

{{profile_one_liner}}   <!-- e.g. "Freelance email marketer, building a course on the side." -->

## Active projects

{{active_projects}}      <!-- a short list; each links to projects/<slug>.md -->

## Key people

{{key_people}}          <!-- a short list; each links to people/<slug>.md -->

## How this memory works (rules for the agent)

- At session start, read this file. Do not load the whole vault — open specific cards on demand.
- After finishing work, run closure: record an episode in `inbox.md`, route durable items
  (decisions → `decisions.md`, lessons → `lessons.md`, entities → `people/`/`projects/`/`cards/`).
- Before creating a card, check for an existing one (same `id`, then similar title) and update
  instead of duplicating.
- Safety: {{safety_limits}}
- The full map of what exists is in `_index.md`.

## Links

- `profile.md` — who I am, in more detail
- `_index.md` — everything that exists in this vault
- `README.md` — how I (the human) use this memory
