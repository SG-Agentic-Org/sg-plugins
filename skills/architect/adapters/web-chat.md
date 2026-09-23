# Adapter: web chat

Open this before the first reply when the person works in a web chat. Mechanics only
— the norms stay in `references/`.

## Say this first

Before anything else, in the person's language, one short paragraph:

> "Here we can do everything except the last bit. I have no folder on your computer
> and nothing here runs on a timer, so I will give you a finished package and a
> step-by-step way to install it and start it once yourself. That is the only manual
> step, and I will stay with you through it."

Said at the start it is a plan. Said at the end it is a surprise, and a person
promised no manual work and then handed some stops trusting the rest.

## The platform and its limits

No files, no shell, no scheduler, no separate runs. What the other platforms keep on
disk is kept in the chat: each document is printed as its own block and the person
saves it.

## Roles with a clean context

Not possible here: one session, one thread, so a checker cannot be started blind.
Roles do not disappear — they are taken in turn in the same session, re-reading the
printed documents instead of trusting what was said earlier, and the honest one-line
warning in `references/roles.md` is said out loud once. Do not present a check made
this way as independent.

## Setting a model

No per-role model here: whatever the person selected in the chat is what every role
runs on. Treat it as the one-model case in `references/build-plan.md`, which also says why
a model question is not asked here. Which models they can pick at all is
`unknown, ask the person`, and it matters only for what the automation itself calls.

## Documents into the chat

Every document that would be a file elsewhere is printed as its own block, opened by
its file name (`01-brief.md`, then `---`, then the document), one document per
message. Names are the ones in `references/state.md`, so the person's saved copies
match what the guide and the resume prompt refer to. Never merge two documents into
one block: the person saves blocks, and a merged block is saved under one name and
lost under the other.

## The state block instead of a folder

There is no `00-state.md` to write to, so the state travels in the chat. Print it
whenever a step changes status, and again as part of the resume prompt:

```
00-state.md
---
Workspace: <program, subscription, where the data lives>
Mode:      New | Check | Revise
Depth:     short path | deep path — <the reason>
Steps:     1 <name> accepted · 2 <name> started · 3 <name> not started
Next action: <the one thing that happens next>
Documents the person is holding: 01-brief.md, 03-spec.md, 04-plan.md, ...
```

The resume prompt has this block written into it, so the person pastes the whole
thing into a new chat and the work continues without being reconstructed by
question. The statuses and their meaning stay in `references/state.md`.

## The template for accesses

There is no `access/` folder, so the person fills in a template and attaches it.
Print it as its own block, with only the lines the build actually needs:

```
access-template
---
Service:        <name>
What I have:    <account, subscription, plan — in your own words>
Where it is:    <the page or app where the setting lives>
Value:          <paste here>
```

Say in the same message that a pasted value stays in this chat and goes into no
document — the secrets rule in `references/roles.md` holds here as everywhere.

## Schedule and the watchdog

Nothing in a chat runs on a timer. The schedule belongs to whatever hosts the
automation on the person's side — their computer, a sheet's own scheduled trigger, a
service they already pay for — and which it is, is `unknown, ask the person` at stage
0: the plan cannot be written without it.

The watchdog is built and installed like the automation, with the same step-by-step.
Its report and its observations file go where the person already looks — next to the
automation, or in the same sheet. What the report contains is
`references/watchdog.md`.

## Where the skill lives

`unknown, ask the person`. Whether this chat has a place for saved instructions or a
project differs per product, so ask what they have. If there is none, the skill is
used by pasting it at the start of the chat, and the resume prompt brings it back.

## The finish: ready to install

This is the one platform where the finish is **ready to install**, not **ready to use**, and it is
reached only after everything in `references/verify.md` has been done here. `scripts/check_task.py`
does not run in a chat: the Architect checks the same list by reading and says so. In one message, opening with two lines: what was run on data inside this chat, and
what only the first run on their own machine will show. Then:

1. The package — every block printed once more in saving order, with the exact file
   name and where on their machine each one goes.
2. Installation, numbered, one action per step, in their language, with what they
   should see after each step so they can tell a finished step from a stuck one.
3. The first run, done by hand: what to type or click, what a correct result looks
   like, and what the most likely wrong result means.
4. Turning on the schedule, in the same numbered form, for the host they named.
5. The guide (`07-guide.md`), including its symptom-to-action lines.

Stay in the chat until the person reports the first run succeeded. An install handed
over and never confirmed is a package, not a working automation.
