# Build plan

Open this at stage 4: steps, models, checkpoint 3, the pause — and again whenever a
step gets stuck during the build.

The plan turns the spec into steps. It is the last document the person sees before
the result, so it is written for them to read, not for the agents.

## Form of `04-plan.md`

```
Step 1  <name>
  Builder    <which agent>
  Model      <tier>
  In         <what it starts from>
  Out        <what exists when it is done>
  Done when  <the acceptance criterion from the spec>
  Checks     <the Tester's checks for this step>
Step 2  ...
Step N  watchdog
Step N+1  switch to the live target      (external actions only)

Resume prompt: <the short prompt for a new session>
```

All six fields are written for every step. When the plan is shown to the person at
checkpoint 3, Builder and Checks may be left out of the shown copy: they are addressed
to the agents. The file keeps them, because Checks is what ties the plan to the checks
written before the build.

## Vertical steps

Each step cuts a narrow but complete path from trigger to a result the person could
look at. One step that collects, counts and writes one row end to end beats three
steps that each finish half of everything.

- A finished step can be shown or checked on its own.
- A step fits in one fresh context for one Builder.
- If something has to be reshaped before the change is easy, that reshaping is its
  own first step.

A horizontal step — "write all the data handling" — is finished only in the sense
that nothing can be run. Nobody finds out it is wrong until the end, when all of it
is wrong at once.

## The watchdog is a step

The watchdog is an ordinary plan step with its own Builder, criteria and checks —
what it must do is in `references/watchdog.md`. There is no finish without it.

## Existing tests in the person's project

If the person's project already has its own tests, the plan includes running them as
one command, as a step of its own. Their tests encode what their project must not
break, and the Architect does not know what that is.

## Models

Pick tiers from what the person actually has, which came out of the workspace
questions at stage 0.

| What they have | How the steps are assigned |
|---|---|
| Three models | Three tiers: cheap for mechanical steps, middle for the build, strongest for acceptance |
| Two models | Acceptance on the stronger one, everything else on the weaker |
| One model | Everything on it, roles taken in turn — say the honest line from `references/roles.md` |

The mechanics of setting a model are in the adapter for the platform.

**When not to ask about models.** With one model there is no choice, so the question
is never asked — a question with one answer only teaches the person that this skill
asks pointless questions. With two or three, the choice is shown once at checkpoint 3
and never revisited.

## Checkpoint 3: the plan

Show the whole plan. Then, in this order, only the lines that apply:

- **Live target, if the plan has one:** "the last step will send one real message to
  the live target — here is to whom and what." Confirming the plan confirms this
  step, and it is not asked about again.
- **A test target that does not exist yet:** ask for it here, with the plan, so the
  person waits once instead of twice.
- **More than one model:** "I picked models by how hard each step is. If that is
  fine, confirm. If you want one changed, say which."
- **More than one step:** "Shall we build now, or pause and pick it up tomorrow from
  the finished spec?" On a pause, hand over the resume prompt —
  `references/state.md`.

A confirmed plan means the person is not needed again until the result is ready.
Every question after this point takes from them the thing they were promised: that
the rest is not their job. The only thing that reaches them is a stop.

## A sprint

When the result is a series of works rather than one thing, the plan is the result —
see the skill's own page. The steps that belong to the person are written the same
way as the steps that belong to Builders, with their own "done when", and checkpoint
3 is the last checkpoint. The state file says `Kind: sprint` (`references/state.md`).
The finish of a sprint is **plan ready**: the plan is handed over and there is nothing
built here to run (`references/verify.md`).

## A stuck step

A step that came back twice with the same defect, came back empty, or whose Builder
is going in circles. The Architect looks for the root and fixes it inside. The person
is never part of this — they did not write the spec.

| Root | What happens |
|---|---|
| The defect is in the step | Split the step in two, or raise its model one tier |
| The defect is in the spec | Send the spec back to the Composer with the finding — the review loop in `references/spec-for-agents.md` repeats for this piece |

This should happen zero times, because the checks were written before the build. A
stuck step is evidence about the spec, not about the Builder.
