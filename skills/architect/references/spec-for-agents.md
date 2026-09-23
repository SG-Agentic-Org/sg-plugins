# Spec for agents

Open this at stage 3: briefing the Composer, judging gaps, and anything with
external actions.

The spec is the contract the Builders work from. The brief and the solution are the
context behind it; the spec is what is binding. It is written by a Composer with a
clean context from the brief and the solution, never by the Architect — see
`references/roles.md`.

Tell the person one line and move on: the spec for the agents is ready, it is not
written for you, you do not have to read it. They did not write it and are not
answerable for it.

## Form of `03-spec.md`

```
Only through the Architect skill. Do not start without it.

Purpose          what must exist when this is done, from the person's side
What it does     the behaviour, trigger by trigger, result by result
Acceptance       per piece, a criterion someone else can check
Out of scope     what we are deliberately not doing
On failure       per failure: empty input, extra input, source unavailable,
                 a second run on the same day
Two shelves      what the Builder does without asking, what it never does
Accesses         paths in access/ — never a secret value
Watchdog         what it checks, how often, where the report goes
```

**Behaviour, not procedure.** The spec says what must be true, not which function to
write. A spec that dictates the implementation freezes today's structure into a
document a Builder will read later, and the Builder then follows the frozen shape
instead of the goal.

> Good: "When a post has no view count, it is counted as zero and named in the
> report."
> Bad: "Add an if-branch in the parsing loop."

**Checkable acceptance.** A criterion that repeats the task in the task's own words
checks nothing and always passes.

> Good: "Running it twice on the same day leaves one row per deal, not two."
> Bad: "The export works correctly."

**No file paths beyond the ones in Accesses, no code.** Paths and snippets go stale
between writing and building, and a Builder trusts them.

**Size fits the task.** A simple automation is one page and three checks. A hundred
pages for a weekly digest takes the Builder's attention away from the digest itself.

## The review loop

1. The Architect reads it first, against the brief: is everything from the brief in,
   is anything in that is not.
2. The Critic looks for anything beyond the brief.
3. The Tester writes the checks: for each acceptance criterion a concrete input and
   expected output, for each failure a scenario.
4. Findings go back to the Composer, who rewrites. Repeat until there are no gaps.

The person is not part of this loop and is not told about it. The Architect goes to
them only when a gap cannot be closed without an answer only they have, and then it
is the stop in `references/state.md`.

## Gaps

A check the Tester cannot write means a gap in the spec. A gap is exactly one of
three things:

- **Off the brief** — the spec says something the brief does not, or misses
  something it does.
- **Unwritten failure behaviour** — a way this can fail with nothing in the spec
  saying what happens then.
- **Uncheckable criterion** — nobody can say from the outside whether it is met.

Anything else the Critic or the Tester dislikes is not a gap and does not reopen the
spec. Reopening a spec over taste is how a one-page spec becomes ten.

## Done when

An outsider builds the whole thing from this spec without seeing the conversation
and without asking a single question, and every acceptance criterion has a check.

## External actions

An automation that sends, publishes, writes into someone else's system, or spends,
is on the deep path (`references/depth.md`) and the spec carries four more things.

**Test target.** A standing place to act against that is not the real one: a test
chat, a test sheet, a test bot. Everything runs there — the build, the full run and
the watchdog — until the one live step. A run against the real target "just to see"
reaches real people and cannot be taken back.

**Kill switch.** One named way for the person to stop the automation acting, written
so that it works without the Architect present. It goes into the guide.

**Action cap.** A ceiling on how many external actions one run may take, and what
happens at the ceiling: stop and report, never continue quietly. A loop that sends
is a loop that keeps sending.

**Live-target step.** The last step of the plan, and only that step, switches to the
live target and runs one control scenario. The person confirmed it by name at
checkpoint 3 (`references/build-plan.md`) and is not asked again.

## New things in someone else's service

A new bot, a new account, a new key, a new sheet inside any service the task does not
own — any service where the person, not the Architect, holds the login — the person creates it themselves, following instructions the Architect writes. The
Builder only configures what already exists. This is the stop in
`references/state.md`, and when the plan needs a test target that does not exist
yet, the request goes out together with the plan so the person waits once.
