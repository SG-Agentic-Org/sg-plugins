# Modes Check and Revise

Open this when the first line says Check ("is my script safe to use") or Revise
("add a column", "change this without breaking it", watchdog observations).

Both modes reuse everything from mode New: the depth rule, the interview, the
Composer writing the spec, checks before the build, acceptance, the full run. Only
what is different is here.

## Check

The person shows what they already have and wants to know whether they can rely on
it. Nothing is changed in Check.

**1. What it does now.** If there is no description, the Architect writes half a page
of "what this does now" from the thing itself. Confirmation happens one of three
ways, in this order:

- The person confirms the text.
- They cannot, because the script is someone else's: the Architect shows what comes
  out on two or three examples and asks whether that is how it should be. This is
  confirmation by fact and counts the same.
- They cannot do that either: the behaviour is recorded as observed, and it goes
  into "not checked" in the report with that reason.

The third way is honest and the first two are better, because an automation measured
against its own output can only ever agree with itself.

**2. The run.** The Tester runs it on test data. External actions go to the test
target only, or are established by reading the code — never by doing them. The
person asked whether this is safe to use, and finding out by sending real messages
answers the question in the worst possible way.

**3. The verdict.** One of exactly three words, and this is the only mode with three:

| Verdict | When |
|---|---|
| **Ready to use** | Everything checked came out right |
| **Usable, but careful with…** | It works, and there are named cases where it does not |
| **Not ready yet, because…** | Something it is supposed to do, it does not |

The report has the same three lists as any other (`references/verify.md`).

**4. Fixes.** Nothing is fixed in Check. If the person asks for a fix, the work moves
into Revise from that point.

## Revise

There is an automation and it has to change without breaking.

**What it does now.** The old behaviour is established the same three ways as in
Check above, including the third one when the person cannot confirm even by fact.

**Depth by the same rule.** "Add a column" is the short path. The rule is in
`references/depth.md` and the existing automation does not make it deeper by itself.

**Observations first.** If the person arrives with the watchdog's observations, read
that file before anything else and say which of them are worth doing and which are
not. They brought a list they did not write; sorting it is the Architect's job.

**Where the work happens.** In the original task folder. The brief starts from "what
is wrong now" or "what to add", and the Composer writes a spec for the change only,
not for the whole automation.

Someone else's automation has no task folder and no watchdog. The folder is started
the same way as in Check, with the copy of the original in `original/`, and the
watchdog is built as an ordinary plan step, because the finish requires one either
way (`references/build-plan.md`).

**The copy.** Before the first edit, a Builder puts a copy of the original into
`original/` in the task folder. That copy is the rollback, and it is made while the
original still works, because nobody makes a backup after they need one.

**The control set.**

| | What it holds | Where the expected result comes from |
|---|---|---|
| Old behaviour | two or three tasks | the actual output before the edit, confirmed by fact — for free text, a list taken from it |
| New behaviour | one or two tasks | the person names it |

After the edit the old tasks must return the same as before, and the new ones must
return what the person named.

**Regression.** An old task that came out worse means roll back to the copy and try
again, with a sharper spec through the Composer. Two attempts. If the second also
regresses, the root is in the spec and the review loop in
`references/spec-for-agents.md` repeats. The person is not involved unless an answer
only they have is needed.

**Blind comparison.** On the deep path the Tester compares before and after without
being told which is which, and writes its conclusion. A Tester who knows which one
is the new version finds it better.

**After acceptance.** The watchdog and the guide are both updated. An automation that
changed while its watchdog still checks the old behaviour reports "working" about
something that no longer exists, and a guide that describes the old behaviour sends
the person looking for a screen that is gone.
