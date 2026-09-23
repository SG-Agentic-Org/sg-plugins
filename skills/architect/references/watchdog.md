# Watchdog

Open this when planning, building or accepting the watchdog.

Every automation ships with a second, much smaller process next to it. The
automation tells nobody when it stops working: it simply stops, and the person finds
out weeks later from a number that was wrong all along. The watchdog is what turns
that silence into a line they will see.

## What it checks

Three things, every time, and nothing else:

1. One or two tasks from the person's control set, against the results the person
   named.
2. Whether the last scheduled run happened at all, and whether it produced a result.
3. On the deep path, the external actions — always against the test target, never
   against the live one. A watchdog that messages real people every week to prove the
   bot works is worse than no watchdog.

## How often

No more often than the automation itself. A daily watchdog over a weekly digest
reports "no new run" six days out of seven, and a report that is usually noise is a
report nobody reads.

## The report

```
Working. | Not working.
What was checked:  <the control tasks and the last run>
What to do:        <only when it is not working — the symptom line from the guide>
```

It goes where the person will actually see it, and which place that is belongs to
the platform — see the adapter. A file next to the automation, a line inside the
same dashboard or sheet, a message in their test chat. A report that lands somewhere
they never open has not been delivered.

## The observations file

Separately from the report, the watchdog appends to one file anything that could
become an improvement later: three weeks empty in a row, a model answering outside
the expected-result list, things getting slower, a source that changed its format.

Each observation uses the finding form in `references/verify.md` — what happened, on
which input, how to fix, how we will know it is fixed, severity — plus one word:

- **breakage** — something that used to work does not.
- **wish** — nothing is broken, and it could be better.

The two are kept apart because they are answered differently: a breakage is a reason
to come back now, a wish is a reason to come back when there is time. Mixed
together, either the breakages drown or every wish looks urgent.

## What the watchdog never does

- It never repairs anything. A process that both checks and fixes can hide from the
  person that anything was ever wrong.
- It never gives advice or proposes features. It records; the Architect decides.
- It never touches the live target.
- It never writes a secret value into a report or an observation, only a path —
  `references/roles.md`.

## The line for the guide

Written into the guide in the person's language, near the end:

> "Here is the observations file. When you have time, say 'some improvements have
> piled up, let us talk' and I will read it first."

That sentence is the whole mechanism by which improvements find their way back: the
person is never asked to monitor anything, and the list is waiting when they want it.

## On the short path

Even at the smallest scale the watchdog keeps all of it: one control task, the
last-run check, the report and the observations file. Dropping the observations file
is what makes it a monitor instead of a watchdog, and then nothing accumulates.

## Acceptance

The watchdog is an ordinary plan step (`references/build-plan.md`) and is accepted
like any other, including one real run of its own. There is no finish without it.
