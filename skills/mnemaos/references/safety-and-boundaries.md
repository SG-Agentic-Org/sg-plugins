# Safety and boundaries

Apply this in Phase 4, before handing the system over. MnemaOS writes to the user's own
files, so the risk surface is small — but two things still matter: keeping the agent inside
limits, and never leaking secrets or a reference implementation.

## Limits the generated skills must carry

The default limit set, carried into the closure, distillation, and hygiene skills as explicit
"stop and ask" rules:

- No publishing anything.
- No sending messages or email as the user.
- No payments.
- No deleting significant data — and in particular, **hygiene flags, it never deletes**.
- No permission/access changes.
- No significant external action on the user's behalf.

How to apply:

1. Start from the default set. The user may **explicitly loosen** one in dimension 5 (e.g.
   "the agent may delete files in the inbox folder"). Only a limit the user named may be
   relaxed; everything else stays a hard stop.
2. Add user-specific caps from the interview (e.g. "never touch folder X").
3. When an action would cross a limit, the agent **prepares a draft or stops and flags the
   work with a concrete reason** — it never performs the action silently.

## No secrets in files

MnemaOS needs no credentials — memory is plain notes. Still:

- Never write a secret value into any generated file. If a credential is ever needed,
  reference it **by name** (an env var name), never by value.
- If the user pastes a secret into chat during onboarding, do not write it anywhere; tell
  them where it belongs (env var / secret store) and reference it by name.
- The smoke test flags inlined secret patterns; treat any hit as a bug.

## No reference-implementation leakage

The generated system must be about **this user only**. Do not put any other person's tool
names, file paths, project names, internal-product names, or domains into the generated vault
or skills. Adapt to the user's setup; never paste another setup's specifics.

The smoke test scans generated files for a leak-pattern list and exits non-zero on a hit.
Treat a leak as a release-blocking bug, not a style nit: it both confuses the user and
exposes details of a system they have nothing to do with.

## Why these matter

A memory system the user trusts is one that never surprises them — never deletes a note they
wanted, never posts on their behalf, never carries a stranger's project names. The cost of
these guards is tiny; the cost of skipping them is a deleted file, an unwanted post, or a
confusing leak. Build them in from the start.
