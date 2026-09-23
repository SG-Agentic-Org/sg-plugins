# Verifying

Open this when accepting a built step (stage 5), for the full run (stage 6), and
whenever a finding is written or closed.

Checkers never fix. A defect goes back to the Builder who owns the step, a gap goes
back to the Composer.

## Accepting a step

A step is accepted by the Tester and the Architect, and on the deep path by the
Critic too.

- **Tester.** Runs the checks it wrote for this step before the build. Then breaks
  the result on purpose once and confirms the check catches it — a check that passes
  on broken work was never a check. Writes what broke and how to fix it.
- **Critic.** Only one question: is there anything here that the spec does not ask
  for.
- **Architect.** Is what the spec asked for actually done, and has it drifted from
  the brief.

The simplicity rules apply to every piece — `references/simplicity.md`.

Wanting to build something that is not in the brief is not a finding. It is leaving
the frame, so it is not built. A wish worth keeping waits until the watchdog exists
and is written there by the watchdog — `references/watchdog.md`.

## Form of a finding

Every finding, from a step or from the full run, is written the same way:

```
What happened:          <the observed behaviour, not a guess at the cause>
On which input:         <the exact case that produced it>
How to fix:             <what has to change>
How we will know it is
  fixed:                <the scenario that must be re-run and what it must show>
Severity:               breaks | hinders | cosmetic
```

"Something is wrong with the export" cannot be sent to anyone. The four fields are
what turns an observation into work somebody can pick up and finish.

Severity is by consequence, not by topic: an unreadable main result is **breaks**, a
small technical flaw is **cosmetic**.

## Closing a finding

A finding is closed only by re-running the same scenario on the fixed version and
getting the right result. Nothing else closes it — not a fix that looks right, not a
Builder saying it is done.

Where the result is free text — a bot's reply, ideas from a model — the scenario runs
three times in a row and the answer must satisfy the expected-result list every time
(`references/interview.md`). One good run is one good run, not a working automation.

## The full run

When every step is accepted, the Tester runs the whole automation. The person is not
here.

1. The person's control set, each against the result they named.
2. One deliberately ordinary task, where nothing should have to be handled.
3. The failure scenarios: empty input, extra input, source unavailable, a second run.
4. The schedule, by forcing a run and reading back that the task is registered. A
   schedule nobody triggered is a line in a config, not a schedule.
5. External actions against the test target, and then, last, one control scenario on
   the live target — the step the person confirmed by name at checkpoint 3.
6. The watchdog, once.

**Not run is not passed.** A scenario that was possible to run and was not leaves
the finish unwritten. There is no third column: a result is what was observed, and
everything else is unknown.

## The finish

One finish per task, and which one depends on what was built. A build finishes with
**ready to use**: every control-set task returned the result the person named, every
scenario was run, none broke and none is "not run". If the Architect cannot write that
sentence, the build is not finished.

A sprint finishes with **plan ready**: the plan is the result, so there is nothing
built to run through the scenarios above (`references/state.md`). Web chat finishes
with **ready to install** — see `adapters/web-chat.md`.

A defect in what the task itself built is fixed inside. Something outside blocking us is the stop in
`references/state.md`: write what is needed, set the step to waiting, and the session
can close. On return, check whether it cleared, run the scenario that was waiting,
and go to the finish. An obstacle that will never clear uses the same form, with the
three options and the letter described there.

## The report

The report opens with the finish, then three lists and nothing else:

```
Ready to use.

Checked:      <every scenario that ran and what it showed>
Not checked:  <what was not run, and why — a reason, never a blank>
If it breaks: <symptom → what to do, pointing at the guide>
```

On the deep path, where the automation acts outside, the last list also names the kill
switch and the action cap: where both live in the guide, and how to switch the
automation to the test target or stop it acting at all. The person reads this report on
the day something goes wrong, and hunting for the off switch is the worst moment to
meet it (`references/user-guide.md`).

"Not checked" that is empty when something was skipped is the one line that turns a
truthful report into a false one, because the person reads its absence as coverage.
