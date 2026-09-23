# Depth

Open this at stage 1, and again whenever the spec changes.

## The rule

The deep path switches on if at least one of these is true:

1. The automation changes data in someone else's system (writes to a CRM, deletes
   records).
2. It sends something to people — messages, letters, publications.
3. It spends money.
4. It passes people's personal data outside, or publishes it.
5. It is made of several agents.

Nothing else moves the path. Everything else is the short path.

## The three exceptions

These look like they qualify and do not:

- **Writing into the person's own sheet or file.** It is their data in their place.
- **Reading from several sources.** Several sources are not several agents.
- **Reading personal data out of the person's own CRM into their own sheet.** The
  data does not go outside, so exception 4 does not fire.

A failure nobody would notice does not change the path either. It adds one line to
the spec: if there is less data than usual, report it instead of passing silently.

## What differs

| | Short path | Deep path |
|---|---|---|
| Interview | two or three questions | full |
| Checkpoints | two (brief with solution, plan) | three (brief, solution, plan) |
| Documents | brief and solution in one file | brief and solution separately |
| Spec | one page, by the Composer | as long as needed, by the Composer |
| Spec review | Critic and Tester in turn in one session | each in a clean context |
| Accepting a step | Tester and Architect | Tester, Critic and Architect |
| Plan steps | one to three plus the watchdog | as many as needed, plus the watchdog, plus the switch to the live target |
| Control set | two or three examples plus one ordinary task | three to five plus one ordinary plus failure scenarios |
| Full run | Tester | Tester |
| Blind comparison in Revise | no | yes |
| Test target, kill switch, action cap | not needed | required |

## Saying it to the person

One sentence, with the reason, so the person can push back on it:

> "We will go the short way here, a mistake would show up straight away."

> "I will be more thorough here, because the bot will be writing to your clients."

The person may ask to go deeper or shorter, and that is their call to make. When they
ask to go shorter on something that qualifies by the rule, name the one item it
qualifies under and let them decide.

## Rechecking

Recheck the rule every time the spec changes. A spec that grew a "and also post it
to the channel" line crossed into the deep path, and a build that keeps running on
short-path assumptions sends real messages with no test target, no kill switch and no
action cap.
