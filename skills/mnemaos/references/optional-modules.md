# Optional modules — source library, question reports, provenance, trust

These are **opt-in** add-ons offered in interview dimension 6. They are off by default —
turn them on only if the user wants them. They add value for people who work with external
sources and want their memory to compound; they add overhead for people who just want
profile + projects + episodes. Offer; do not impose. Keep them light — do not recreate a
heavy knowledge-base pipeline.

Lineage: a light reading of the Karpathy-style local knowledge-base pattern (RAW → Wiki →
Outputs), borrowed at low cost, not a full port.

## Module A — Source library (RAW / Wiki / Outputs frame)

For users who feed external sources (articles, transcripts, papers, PDFs) into their memory,
offer a three-layer frame as an alternative-or-addition to the flat `cards/`:

```
<vault>/
  RAW/        — verbatim sources, never edited (one file per source, with frontmatter)
  Wiki/       — distilled, cross-linked cards (this is `cards/` by another name; pick one)
  Outputs/    — saved answers/reports (the question-report habit, Module B)
```

Rules, kept minimal:

- **RAW is verbatim.** A source dropped in RAW is preserved word-for-word, never summarized.
  Each RAW file carries frontmatter: `title`, `author` (or `unknown`), `source_url` (or
  `unknown`), `date_added`, `type` (Book/Article/Podcast/...). Mark unknown fields `unknown`,
  never fabricate.
- **Wiki is the distillate.** Cards distilled from RAW, with `source_refs` pointing back to
  the RAW files (page-level provenance — see Module C). The distillation skill writes here.
- **Outputs is for saved answers** (Module B).

A user can take just the flat `cards/` skeleton (the default) and skip RAW/Wiki/Outputs
entirely. Only offer this frame when they work with discrete external sources worth keeping
verbatim. Do not rename a flat vault's folders just to match this shape.

## Module B — Question-report habit (light)

A weighty analytical question to the memory deserves a saved report, not just a chat answer —
so the reasoning compounds instead of scrolling away. **Light, not non-negotiable:**

- **Default for weighty questions only.** When the user asks the memory a substantial
  question whose answer is worth keeping, write a short report and save it (in `Outputs/` if
  Module A is on, else in a `reports/` folder or next to the relevant project).
- **Small questions stay in chat.** Do not file a report for every question — that is
  overhead, not value. The file is the default only for the weighty ones.
- **Report shape:** the question restated; the answer structured for re-reading; which cards/
  sources it drew on; tensions or contradictions surfaced; open questions. Name it
  `YYYY-MM-DD_query-slug.md` (append `-revision-2` on a date clash).
- **Chat-side:** end with a one-line summary and, if the host renders it, a clickable
  `computer:///absolute/path/to/report.md` link to the file (otherwise the bare absolute path).
- **Promotion:** a report that turns out to contain foundational synthesis can be promoted
  into a card.

This is deliberately the *weakened* form of the "every question is a report" rule — the file
is the default for weighty questions, the chat is fine for small ones.

## Module C — Page-level provenance (`source_refs`)

When a card distills an identifiable source, record where it came from in `source_refs`
(see `frontmatter-contract.md`). **Page-level, not claim-level:** the list says "this card
draws on these sources", enough to find the original — it does not trace every sentence. This
is on automatically when Module A is on; it can also be used standalone any time a card has a
real external source. Skip it for the user's own working notes (no source to trace).

## Module D — Trust (`trust`)

`trust: established | emerging | speculative` on a card says how much to believe its content
(distinct from `status`, which is lifecycle). Most useful on the user's **own ideas and
unverified material** — that is where "my hypothesis" vs "from a solid source" matters. For
cards distilled straight from a strong source it is usually `established` and adds little.
Default: set it on own-idea/speculative cards; leave it off elsewhere unless the user wants it
everywhere. See `frontmatter-contract.md`.
