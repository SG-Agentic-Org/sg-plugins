# Architect

A skill that turns what you say about your own work into an automation that runs.

You talk, in your own words, about what you do and what you would rather not do any
more. Architect asks a few small questions, writes down what it understood on one
page, and shows it to you. Once you say that is right, it puts its own agents to
work: one writes the spec, one writes the checks before anything is built, one
builds, one tries to break it. You are not part of that. You come back once to
approve the plan, and after that only if something is missing that only you can
give — an access, a test chat, an answer nobody else has.

At the end you get three things: the automation, a watchdog that checks every week
that it still works and writes down anything worth improving, and a guide in your
own language.

## Who it is for

People who want to automate a piece of their work and do not know how to brief an
AI. No experience with AI is assumed and no terms are required: any word you would
not use over dinner gets explained the first time it appears, or is not used at all.

It also works for people who do know. The same path covers checking an automation
you already have, changing one without breaking it, and running a sprint where the
plan itself is the result.

## What it can build

Anything an assistant with your accesses can build: a script that collects numbers
into a page every week, an export from a customer database into a spreadsheet, a
site read on a schedule, a bot, a skill for your assistant, a chain of agents.

## Install

Download or clone this folder, then put it where your tool looks for skills.

**Claude Code** — copy the `architect/` folder into `.claude/skills/` in your project,
or into `~/.claude/skills/` to have it everywhere. Start a new session and say
"architect".

**Codex** — copy the `architect/` folder into your project, then point Codex at it in
the instructions file it reads at start-up (`AGENTS.md`), with one line saying that
work on automations goes through `architect/SKILL.md`.

**Gemini CLI** — copy the `architect/` folder into your project, then add one line to
the context file Gemini reads at start-up (`GEMINI.md`) saying the same thing.

**Web chat** — no install. Open a new chat, paste in `SKILL.md`, and say what you
want to automate. Architect will read the other files as it needs them, so keep the
folder open. In a web chat there are no files and nothing runs on a timer, so the
session ends with a finished package and step-by-step instructions to install it and
start it once yourself. Architect says this at the very start, not at the end.

## How to call it

Say what you want in your own words:

> "I want to automate this"
> "help me work out how to make this happen by itself"
> "check my script, can I rely on it"
> "improve my automation, without breaking it"
> "here is my description, turn it into an automation"
> "some improvements have piled up, let us talk"

Or just say "architect".

## What you get

- **The automation**, built and run against your own real cases.
- **A watchdog** next to it, which runs no more often than the automation itself,
  checks a couple of your control cases and whether the last run happened, and puts
  its line where you will see it. It also keeps an observations file — things that
  could become improvements later. When you have time, you say so and it gets read
  first.
- **A guide** in your language: how to run it, what to do for each thing that could
  look wrong, where the reports are, where to put a new access, and how to switch it
  off if it sends anything anywhere.

There is one finish, "ready to use", and it is written only when every control case
returned the answer you named and every scenario was actually run. Nothing is ever
counted as passed because nobody tried it.

## What it will not do

It will not write your content, explain terms as a lesson, or quietly do the one-off
task instead of automating it — if a thing happens once, it says so and does it. It
will not send, publish, pay or delete anything without an access you handed over. It
will not put a secret value into any document. It will not tell you to move to
something bigger when a small script does the job.

## Examples

Three full walks, from the first question to the finish, in `examples/` — in English
and in Russian.

## Author and licence

Author: Alexander Glibichuk · Telegram channel @glibichuk_pro

Based on skill-architect by Timur Ugulava — https://github.com/TimurUgulava/skill-architect

MIT, see `LICENSE`.
