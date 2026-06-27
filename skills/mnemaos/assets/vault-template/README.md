# Your memory

> Generated for you during onboarding. Resolve the `{{placeholders}}` from
> `mnemaos-config.yaml` and remove this quote block before handing it over. Written for a
> non-technical reader.

## What this is

This folder is your AI's memory. Your AI reads it at the start of a session so it already
knows who you are and what you're working on — and writes the results of your work back into
it when you finish. You stop re-explaining your context every time you open a new chat.

Everything here is plain text files you can open and edit yourself. Nothing is locked in a
service. You can move this folder, back it up, or walk away with it any time.

## The pieces

- `_start-here.md` — the map your AI reads first: who you are, your active projects, the rules.
- `profile.md` — more detail about you.
- `projects/` — one file per project.
- `people/` — one card per person you work with.
- `cards/` — notes on concepts, ideas, and decisions worth keeping.
- `decisions.md` — a log of important choices.
- `lessons.md` — "don't do this again" rules.
- `inbox.md` — fresh notes from recent sessions, before they're filed.
- `_index.md` — an auto-generated list of everything in here.

## How to use it day to day

1. **Start a session.** {{startup_plain}}  <!-- "Your AI reads _start-here.md automatically"
   OR "Paste the contents of _start-here.md at the top of your chat" -->
2. **Do your work** as usual, with your AI.
3. **Close it out.** {{closure_plain}}  <!-- "Say 'close this out' and your AI records what
   matters" OR "Ask your AI for a closure note and paste it into inbox.md" -->
4. **Tend it weekly.** {{hygiene_plain}}  <!-- "Hygiene runs automatically every week" OR
   "Once a week, say 'run hygiene' to tidy up" -->

## What your AI will NOT do on its own

For your safety, your AI will never do these without asking first:

{{safety_limits_plain}}

If something would need one of these, it stops and tells you, so you stay in control.

## If something looks wrong

- **The AI forgets your context:** make sure it read `_start-here.md` first. See `SETUP.md`.
- **Nothing lands in `inbox.md`:** run closure (say the trigger phrase). Check `SETUP.md`.
- **Duplicate cards or broken links:** run hygiene, or `_index.md` is stale — re-index.
- **Anything else:** open `SETUP.md`, or re-run onboarding to adjust your setup.
