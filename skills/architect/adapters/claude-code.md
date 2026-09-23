# Adapter: Claude Code

Open this when the person works in Claude Code. Mechanics only — the norms stay in
`references/`.

## The platform and its limits

A terminal agent with the person's files, its own shell, and subagents that run in
their own context window. Everything the skill's core assumes — a task folder on
disk, separate runs per role, a model per role — exists here, so nothing has to be
substituted.

One limit matters: no scheduler is documented for the CLI itself. What runs the
automation on a schedule is `unknown, ask the person` — see "Schedule and watchdog".

## Roles with a clean context

Roles are subagents. "Each subagent starts with a fresh, isolated context window. It
doesn't see your conversation history, the skills you've already invoked, or the
files Claude has already read." That is exactly the separation `references/roles.md`
asks for, so on this platform the honest one-session warning is not needed.

A subagent is a Markdown file with YAML frontmatter; `name` and `description` are
required and the body becomes its system prompt. It can live in:

| Path | Scope |
|---|---|
| `.claude/agents/` | this project |
| `~/.claude/agents/` | every project on this machine |

Dispatch one by naming it, or pin it with `@"<name> (agent)"` when the run must go to
that role and not be re-decided.

Write one file per role — Composer, Builder, Tester, Critic — into `.claude/agents/`
of the person's project, and hand the Builder its step package the way
`references/roles.md` describes: its criteria, its checks, its paths, nothing else.
A subagent that is handed the conversation is no longer a clean context, whatever
the platform guarantees.

Source: https://code.claude.com/docs/en/sub-agents

## Setting a model

The `model` field in the subagent's frontmatter. Accepted values are aliases
(`sonnet`, `opus`, `haiku`, `fable`), full model IDs, or `inherit` for the main
session's model. Resolution order: the per-invocation model, then the frontmatter
field, then the `CLAUDE_CODE_SUBAGENT_MODEL` environment variable, then the main
session's model.

Which tier goes to which step is the rule in `references/build-plan.md`. Which
aliases actually resolve depends on the person's own account, so before writing the
tiers into the plan, ask which models they see in their own model menu rather than
assuming a list.

Source: https://code.claude.com/docs/en/sub-agents

## The task folder

Real, on disk, exactly the layout in `references/state.md`. Put it inside the
person's project unless they name another place. Agents read and write it directly,
so no document has to be copied into the chat.

## Schedule and the watchdog

Nothing in the documented CLI runs a job on a timer, so the schedule comes from
outside it: the operating system (`cron`, `launchd`, Task Scheduler), or the service
that already hosts the person's data. Which of these they can use is `unknown, ask
the person` — ask at stage 0 with the other workspace questions, because the answer
decides how the plan's schedule step is written.

A non-interactive run is `claude -p "<prompt>"`, with `--model` to pin the model, so
whatever scheduler the person has can call the automation and the watchdog that way.

The watchdog report goes into `watchdog/` in the task folder, and the line the person
actually sees goes wherever they already look — `references/watchdog.md` decides
what the report contains, this adapter only says the file has a real home here.

Source: https://code.claude.com/docs/en/headless

## Where the skill lives

| Path | Scope |
|---|---|
| `~/.claude/skills/<name>/SKILL.md` | every project on this machine |
| `.claude/skills/<name>/SKILL.md` | this repository |

The directory name is what the person types after `/`, and the skill is also picked
up on its own when the task matches its `description`.

Source: https://code.claude.com/docs/en/skills

## The finish

Full **ready to use**: the automation runs where it will live, the watchdog has had
one real run of its own, and the guide is in the task folder in the person's
language. Nothing is left for the person to install by hand. What "ready to use"
requires is in `references/verify.md`.
