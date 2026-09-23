# Adapter: Codex

Open this when the person works in Codex. Mechanics only — the norms stay in
`references/`.

## The platform and its limits

A terminal agent with the person's files and a non-interactive mode built for
repeatable runs. The task folder is real. Roles are separated by starting a new run
rather than by a subagent mechanism, so the separation is one command per role
instead of one dispatch.

Two things are not documented and are not guessed here: whether there is a subagent
mechanism of its own, and whether anything schedules a job. Both are handled below.

## Roles with a clean context

`codex exec` is the documented non-interactive entry point — "Use Codex
interactively or call `codex exec` from repeatable workflows and pipelines." One
role is one `codex exec` run: it starts its own session, so a Composer run cannot
have watched the Architect think and a Critic run cannot have watched the Builder.

The role's instructions go in the prompt of that run, and its material goes as paths
into the task folder. Hand the Builder its step package and nothing else —
`references/roles.md`.

Whether Codex also has an in-session subagent mechanism is `unknown, ask the person`;
separate `codex exec` runs already give clean context, so nothing depends on the
answer.

Source: https://learn.chatgpt.com/docs/codex/cli

## Setting a model

Two documented ways: the `-m` / `--model` flag on the run, or the model set in the
Codex configuration (changed inside a session with `/model`). The active model is
shown in the session header, so a run's tier can be read back rather than assumed.

Per role, pass `-m` on that role's `codex exec` run — one flag per role is what makes
the tier rule in `references/build-plan.md` real on this platform. Which model names
are available belongs to the person's own account, so ask which models they see in
their own menu instead of naming a list.

Source: https://learn.chatgpt.com/docs/codex/cli

## The task folder

Real, on disk, exactly the layout in `references/state.md`, inside the person's
project unless they name another place. Because each role is a separate run with no
memory of the previous one, the folder is the only thing carrying the work forward:
write `started` before a step and `accepted` after it, or the next run has no way to
tell a finished step from an abandoned one.

## Schedule and the watchdog

No scheduler is documented for the CLI. The schedule therefore comes from the
operating system (`cron`, `launchd`, Task Scheduler) or from the service that hosts
the person's data, and which of those they can use is `unknown, ask the person` —
ask it at stage 0 with the other workspace questions, because the answer decides how
the schedule step of the plan is written.

Whatever the scheduler turns out to be, it invokes the automation and the watchdog
the same way a person would: one non-interactive run per tick.

The watchdog report goes into `watchdog/` in the task folder, and the line the
person actually sees goes wherever they already look. What the report contains is
`references/watchdog.md`.

Source: https://learn.chatgpt.com/docs/codex/cli

## Where the skill lives

Codex scans, from narrowest to widest:

| Path | Scope |
|---|---|
| `.agents/skills/` | the repository, from the current directory up to its root |
| `$HOME/.agents/skills/` | this user |
| `/etc/codex/skills/` | this machine, set by an administrator |

A skill is a directory with `SKILL.md`, whose frontmatter carries `name` and
`description`. The person can pick one explicitly by typing `$` or running
`/skills`, and Codex can also choose it when the task matches the description.

Source: https://learn.chatgpt.com/docs/build-skills

## The finish

Full **ready to use**: the automation runs where it will live, the watchdog has had
one real run of its own, and the guide sits in the task folder in the person's
language. The one thing that may remain outside is the schedule, when the person's
scheduler is something only they can install — that is a stop in the form of
`references/state.md`, not a finish. What "ready to use" requires is in
`references/verify.md`.
