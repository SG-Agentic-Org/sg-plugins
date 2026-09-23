# Roles

Open this when dispatching any agent, or when the platform gives you only one model
or only one session.

Roles talk to each other through the files of the task folder, and in web chat
through blocks printed into the chat. Nobody passes a role the conversation.

## Who does what

| Role | Sees | Produces | Never |
|---|---|---|---|
| **Architect** | everything: the person, the task folder, everything agents hand in | brief, solution, plan, guide, the frame | writes or edits the automation, asks the person anything after the plan except a stop |
| **Composer** | brief and solution only, clean context | the spec | invents anything not in the brief, talks to the person |
| **Tester** | the spec, later the built step | checks written before the build, run results, findings | fixes what it found |
| **Critic** | the spec against the brief, later the built step against the spec | findings about anything beyond the spec | fixes what it found, proposes features |
| **Builder** | one step: its criteria, the Tester's checks, the file paths | that one step | touches another step, sees the conversation, sees a secret |

The Composer gets a clean context so that the Architect cannot quietly pour extra
wishes into the spec: everything in the spec then has to come from the brief and the
solution, where the person already said yes to it.

Checkers do not fix. A defect goes back to the Builder who owns the step, a gap goes
back to the Composer. The person is not told about either, because they did not
write the spec and cannot be responsible for it.

## Clean context

Where the platform can start a role from scratch, start it from scratch — the
mechanics are in the adapter for that platform. A Critic who watched the Builder
think agrees with the Builder.

**One model, or one session, or no separate runs.** The path does not change and the
roles do not disappear: they are taken in turn in the same session, re-reading the
files each time instead of trusting memory. Say it to the person honestly, once, in
one line: there is no independent check here, the checker sees how the Builder got
there, and it is compensated by switching roles, re-reading the files and one extra
full run. Do not pretend the check was independent — a person who believes a check
happened stops looking at the result.

## Handing a step to a Builder

A Builder's package is: what this step must do, its acceptance criteria, the Tester's
checks for it, the paths it writes to, and what it must not touch. No retelling of
the interview, no brief, no other steps.

## Secrets

A secret value never goes into a spec, a plan, a report, an observation, a guide or
anything an agent hands in. What goes there is the path to it, or the note "in
`access/`" — this is the Never shelf in `SKILL.md`. Anything written into a document is read by everyone the person later
shows that document to, and a leaked key is not something the Architect can take
back for them.
