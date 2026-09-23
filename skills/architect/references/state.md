# State file

Open this when starting a task, writing a status, returning after a pause or a
break, or writing a stop.

The state file is `00-state.md` in the task folder. It is the only place that says
where the work stands, so it is written as the work moves, not at the end.

## Form of `00-state.md`

```
Workspace: <program the person talks to AI in, subscription, where the data lives>
Mode:      New | Check | Revise
Kind:      automation | sprint
Depth:     short path | deep path  — <the reason from the depth rule>

Steps
  1. <name>   accepted
  2. <name>   started
  3. <name>   not started
  4. <name>   waiting: <what is missing>
  ...

Next action: <the one thing that happens next>
Reading order on return: 00-state.md → 04-plan.md → 03-spec.md → 01-brief.md
```

## English keys, the person's language in the values

The state file is the one machine-read document of the task: `scripts/check_task.py`
reads it before the final. So the field names — `Workspace`, `Mode`, `Kind`, `Depth`,
`Steps`, `Next action` — and the statuses below stay in English in every task, whatever
language the work is in. So do the values of `Mode`, `Kind` and `Depth` themselves —
`New` / `Check` / `Revise`, `automation` / `sprint`, `short path` / `deep path` — because
the script reads those three values and not only their names. Everything else — step
names, the reason after the dash in `Depth`, what is missing — is written in the
person's language. A translated key or a translated value of those three fields reads
fine to the person and makes `check_task.py` report findings on a correct folder.

## Kind: automation or sprint

`Kind` says what the task is building, because the two end in different things and a
missing line would be read as a gap. The Architect writes the line at stage 1, the
moment it is clear that the result is a plan and not a thing, and names it to the
person at checkpoint 1 together with the brief.

`automation` — the result is a working thing. Everything in the task folder below
applies.

`sprint` — the result is the plan itself: a series of works, some done by agents and
some by the person. A brief, a plan, a guide and a state file are required. The steps
are future works, part of them the person's, so their statuses are not required at the
final: a step nobody has started yet cannot be `accepted`, and demanding it would
close the finish for ever. A check is required for every step an agent does, and when
no step is an agent's, `05-checks/` can stay empty. A spec, a watchdog, an automation
folder and `06-reports/` are not required: there may be nothing built to watch and
nothing accepted yet to report. When a sprint
step does build an automation, that step carries its own spec. The sprint's report is
written into `04-plan.md` as its last section, not into `06-reports/`. The finish of a
sprint is **plan ready**, not "ready to use" — `references/verify.md`.

A task with no `Kind` line is read as `automation`, the stricter of the two.

## Statuses

`not started` · `started` · `accepted` · `waiting: <what>` · `stopped: <why>`

Write `started` before a step begins and `accepted` after it passes acceptance. A
status written afterwards is a guess: the session that has to read it is usually not
this one.

A step found in `started` on return is redone from scratch. Half-built work whose
author is gone looks finished and is not, and finishing someone else's half takes
longer than building the whole.

## Stop: something is missing

One form, whatever is missing — an access, a test target, a service that does not
answer, an answer only the person has:

```
What is needed:    <the thing, in the person's words>
Why:               <what it unblocks, one line>
Where to put it:   <path in access/, or the template to fill in web chat>
What happens next: <what the Architect does the moment it arrives>
```

Set the step to `waiting: <what>`, write the stop to the person, and the session can
be closed. On return, check whether it is resolved, run the scenario that was
waiting, and continue.

When the obstacle will never clear, the same form carries three options under "what
happens next": narrow the brief, switch the source (a new brief in the same folder),
or stop the task. A stopped task gets status `stopped: <why>`, a switched-off
watchdog, and a letter — what was built, what does not work, why, and what to do if
the service comes back.

## Resume prompt

At checkpoint 3, if the person chooses to pause, hand them a short prompt for a new
session: it calls the skill by name and names the task folder, so the Architect
reads the folder and continues from the right step without asking anything again. In
web chat there is no folder, so the state block is written into the prompt itself and
the person pastes the whole thing — see `adapters/web-chat.md`.

## Task folder

```
<task>/
  00-state.md          workspace, mode, depth, step statuses, next action
  01-brief.md          brief (on the short path it also holds the solution)
  02-solution.md       solution (deep path)
  03-spec.md           spec for agents, with the header "only through the skill"
  04-plan.md           build plan and the resume prompt
  05-checks/           the Tester's checks, written before the build
  06-reports/          acceptance reports per step and the full run
  07-guide.md          the guide for the person
  access/              accesses
  original/            copy of the original, in mode Revise
  <automation>/
  watchdog/            the watchdog, its reports and its observations file
```

Web chat has no folder of this shape: each document is printed into the chat as its
own block with its file name, and the person keeps them.
