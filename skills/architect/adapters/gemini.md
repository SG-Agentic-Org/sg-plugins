# Adapter: Gemini CLI

Open this when the person works in Gemini CLI. Mechanics only — the norms stay in
`references/`.

## The platform and its limits

A terminal agent with the person's files, custom subagents of its own, and a headless
mode. The task folder is real and the roles can be genuinely separate.

One documented quirk shapes the model rule: "The `/model` command (and the `--model`
flag) does not override the model used by sub-agents." A tier chosen for the session
does not reach the roles, so each role carries its own model — see below.

## Roles with a clean context

Roles are custom subagents: Markdown files with YAML frontmatter, where the body is
the system prompt. They go in:

| Path | Scope |
|---|---|
| `.gemini/agents/*.md` | this project |
| `~/.gemini/agents/*.md` | this user |

Required frontmatter is `name` and `description`; `tools`, `model`, `max_turns` and
`timeout_mins` are optional. "Each subagent runs in its own isolated context loop" —
its history stays out of the main agent's context, which is the separation
`references/roles.md` asks for, so the honest one-session warning is not needed here.

Send a task to a named role with `@<name>` at the start of the prompt, which bypasses
the main agent's own choice. Two constraints to plan around: subagents cannot call
other subagents, so the Architect dispatches every role itself and no role dispatches
another; and a subagent inherits all of the parent's tools unless `tools` is listed,
so list them when a role must not write.

Headless runs use `-p` / `--prompt`, with `--output-format json` when a run's result
has to be read back by something other than a person.

Sources: https://github.com/google-gemini/gemini-cli/blob/main/docs/core/subagents.md
and https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/headless.md

## Setting a model

The `model` field in the subagent file, which "Defaults to `inherit` (uses the main
session model)". Because `/model` and `--model` do not reach subagents, write the
model into each role's file explicitly whenever the plan gives roles different tiers
— otherwise every role silently runs on one model and the tier rule in
`references/build-plan.md` exists only on paper.

Which models the person can pick is their account's business: the model menu offers
Auto and Manual choices, so ask which models they see in their own menu rather than
naming any list.

If it turns out there is only one, follow the one-model line in
`references/build-plan.md` and say the honest sentence from `references/roles.md`.

Sources: https://github.com/google-gemini/gemini-cli/blob/main/docs/core/subagents.md
and https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/model.md

## The task folder

Real, on disk, exactly the layout in `references/state.md`, inside the person's
project unless they name another place. Roles exchange work through it, not through
the conversation.

## Schedule and the watchdog

No scheduler is documented for the CLI. The schedule comes from the operating system
(`cron`, `launchd`, Task Scheduler) or from the service hosting the person's data,
and which of those they can use is `unknown, ask the person` — ask at stage 0 with
the other workspace questions, because the answer decides how the schedule step of
the plan is written. Whatever it is, it calls the automation and the watchdog as a
headless run.

The watchdog report goes into `watchdog/` in the task folder, and the line the person
actually sees goes wherever they already look. What the report contains is
`references/watchdog.md`.

Source: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/headless.md

## Where the skill lives

Skills are discovered, lowest precedence to highest:

| Path | Scope |
|---|---|
| bundled and extension skills | shipped with the CLI or an installed extension |
| `~/.gemini/skills/` or `~/.agents/skills/` | this user |
| `.gemini/skills/` or `.agents/skills/` | this workspace |

Within a tier the `.agents/skills/` alias wins over the `.gemini/skills/` directory.
On first activation the person is shown a consent prompt naming the skill and the
directory it will be allowed to read, so warn them that one click is expected.
`/skills list` shows what the session can see.

Source: https://github.com/google-gemini/gemini-cli/blob/main/docs/cli/skills.md

## The finish

Full **ready to use**: the automation runs where it will live, the watchdog has had
one real run of its own, and the guide sits in the task folder in the person's
language. What "ready to use" requires is in `references/verify.md`.
