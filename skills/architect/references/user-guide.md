# The guide for the person

Open this at stage 6, when writing the guide.

The guide is `07-guide.md`, written in the person's own language, and it is the only
document from the whole task they will open again months later. Everything else was
for the agents.

Write it for someone who has forgotten the conversation. They will read it on the
morning something looks wrong, which is the worst moment to meet a term for the
first time.

## Form of `07-guide.md`

```
What this does        one or two sentences, the result and how often
How to run it         the normal way, and how to run it by hand right now
If something looks
  wrong               the symptom table below
Where the reports are the automation's result, the watchdog's report,
                      the observations file — each by its actual location
New accesses          where to put a new key or login when one expires
Asking for a change   "say 'improve this' and name what you want"
Turning it off        external actions only: how to switch to the test target,
                      how to stop it acting at all, and the ceiling on actions
                      per run — at the ceiling it stops and reports, which is
                      the automation working, not breaking
```

For a sprint there is nothing to run: the guide says instead how to walk the plan step
by step and how to call the Architect for the next step (`references/state.md`).

The last block exists only where the automation sends, publishes or writes into
someone else's system. It is the kill switch from the spec, written so it works
without the Architect in the room.

## Symptom to action

A table, because the person arrives with a symptom and nothing else. Every row is a
thing they could actually see, in the words they would use, and every action is
something they can do alone. Three or four rows is right for a simple automation.

| I see | What it means | What to do |
|---|---|---|
| The report is not there in the morning | The scheduled run did not happen, or it ran and found nothing | Run it by hand as above. It works — the schedule is the problem, say "improve this". It does not — say "improve this" and paste what it printed |
| The report is there but the numbers did not change | The source gave the same data, or stopped giving data | Check the source has today's data. It does — say "improve this" |
| The watchdog says "not working" | A control task stopped returning the right result | Say "improve this" and name the watchdog's line. Nothing needs to be worked out first |
| Everything is empty and the source needs a login | The access expired | Put the new one where the "new accesses" section says, then run it by hand |

No row ever ends in "check the logs" or "debug it". The person did not build this
and is not going to diagnose it: every path out of the table leads either to one small
thing they can do themselves, or to coming back and saying so.

## Terms

Any word the person would not use outside this context — parsing, dashboard, token,
repository, API — is either explained where it first appears or replaced with what it
means. "Put the key in the accesses folder" is the same instruction as "store the
API token in the credentials directory" and can be followed by someone who has never
heard of either.

## What the guide never contains

- A secret value. Only where it lives — `references/roles.md`.
- An instruction that leaves the person with work to do before the automation runs.
  There are no leftover manual steps after a session, except the install in web chat
  (`adapters/web-chat.md`), which was announced at the very beginning.
