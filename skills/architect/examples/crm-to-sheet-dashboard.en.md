# Example: from a CRM into a sheet, every morning

Mode **New**, short path, platform Codex. A full walk from stage 0 to stage 6, with a
pause after the plan and a return the next day.

Lines marked **A** are the Architect, lines marked **P** are the person.

---

## First question: is an automation needed

**A:** Is this something that comes back, or a one-off?

**P:** Every morning. I do it by hand now and it takes the first part of my day.

**A:** Then it is worth automating.

---

## Stage 0. What you work with

**A:** Which program do you use to talk to an AI assistant, and which plan are you
on? I ask so I can pick helpers that fit what you have.

**P:** Codex. I see two models in the menu.

**A:** Two is fine — the stronger one checks, the other one builds. Where does the
material live that this should work with?

**P:** The deals are in our CRM, and I keep the summary in Google Sheets.

**A:** One question about the CRM. Does it let other programs pull the data out on
their own, or do you have to open it and copy by hand?

**P:** There is a way for programs — I have the key for it somewhere.

**A:** That is all I needed. That key is the one thing I will ask you to hand over,
and it goes into the accesses folder of this task, not into any document — I will
write out exactly where to put it. And your sheets — is the assistant already allowed
to reach them?

**P:** Yes, that is connected.

State file, workspace lines: Codex, two models, task folder on disk. Sources: the
CRM through its programmatic way in, key going into `access/`. Destination: Google
Sheets, already connected.

---

## Stage 1. What you want to get

**A:** When this is all working, what do you see, and how often?
*My guess: you open one sheet in the morning and the whole picture is there.*

**P:** I want the funnel by salesperson every morning on one screen — how many deals
each of them has at each stage.

**A:** Which fields should come across from a deal?
*My guess: the salesperson, the stage, the amount, and the date it last moved — that
is enough for a funnel and nothing more to keep clean.*

**P:** That is the four.

**A:** Which stages count as a closed deal? You could mean only the one marked won,
or won plus anything invoiced.
*My guess: only the one marked won, so the number means the same thing in every
report.*

**P:** Only won.

**A:** Over what stretch?
*My guess: the current month, reset on the first.*

**P:** The current month.

**A:** Now the one I cannot fill in for you. Take yesterday: tell me what the row for
one of your people should have said. That is how we tell later whether this is doing
the right thing.

**P:** Yesterday, for this person: eleven deals in progress, three won, one lost.

**A:** Two more like that and we are set.

**P:** Here are two more.

**A:** Short way here. We read out of your CRM and write into your own sheet — nothing
leaves, nothing is sent to anyone, and a wrong number is in front of you the same
morning.

---

## Checkpoint 1 and 2 together: the brief

```
01-brief.md

What I want, and who it is for
  Every morning, one screen with the funnel by salesperson: how many deals each
  person has at each stage this month. For me, and later for the team.

What comes in
  The deals from our CRM, through the way in that programs use.

What should come out
  One sheet with a row per deal (salesperson, stage, amount, date it last moved),
  and a second sheet with the funnel by person and its charts.

How often
  Every morning.

How we will know it works
  Yesterday, for the first person → 11 in progress, 3 won, 1 lost. Second person →
  as given. Third person → as given.

What we are not doing
  Nothing is written back into the CRM. Nothing is sent to anyone. No forecasting.

What I assumed
  "Closed" means only the stage marked won.
  A deal with a field left empty still becomes a row, with that field left blank and
  counted in a separate line so it is not silently lost.

How it works
  1. Every morning a script — a small program that runs on its own — asks the CRM
     for this month's deals.
  2. It writes one row per deal into the first sheet, replacing yesterday's rows.
  3. It counts the deals per person per stage and fills the second sheet.
  4. The second sheet draws the funnel from those counts.

How we will check it
  The three days you gave me, an ordinary day, a deal with an empty field, the CRM
  not answering, and running it twice on the same day.

Even simpler
  The same two sheets without the charts — just the counts.
```

**A:** Here is what I understood you want, and here is how I would build it, with a
simpler version underneath. One thing I want to say plainly: there is no AI in this
at all. Everything here is counting, and counting belongs to the code — a model asked
to add up figures gives a different total on a different day. Is this what you
wanted, and which version do you want?

**P:** Keep the charts. On one screen means I want to see it, not read it.

**A:** Then your part is done until the plan.

---

## Stage 3. The spec

**A:** The spec for the agents is ready. It is not written for you, you do not have
to read it.

The Composer wrote a page: how the deals are pulled, the shape of both sheets, what
happens when a field is empty, when the CRM does not answer, when it runs twice on
the same day, and the watchdog comparing the number of rows against the number of
deals. The Tester wrote a check per criterion and found a gap: a deal with no phone
number had no rule at all, so no check could be written for it. The Composer added
the rule — the row is kept, the field stays blank, and the count of such rows appears
on the second sheet. No gaps on the second round.

---

## Stage 4. The plan

```
04-plan.md

Step 1  Pull the deals and fill the first sheet
  Builder    a Builder in a clean context
  Model      weaker
  In         the CRM access and the address of the sheet
  Out        the first sheet, one row per deal for yesterday
  Done when  yesterday's three people come out with the counts you named
  Checks     yesterday's three people, a deal with no phone number, the CRM not
             answering
Step 2  Counts and the funnel sheet
  Builder    a Builder in a clean context
  Model      weaker
  In         the first sheet from step 1
  Out        the funnel sheet with the counts and the blank-field rows
  Done when  the funnel matches the first sheet, and a second run the same day
             leaves one row per deal, not two
  Checks     the funnel against the first sheet, a second run the same day
Step 3  Morning schedule and watchdog
  Builder    a Builder in a clean context
  Model      weaker
  In         the finished script from steps 1 and 2
  Out        the morning run registered, the watchdog with its report and its
             observations file
  Done when  the morning run is registered, the watchdog writes its line into the
             second sheet
  Checks     the schedule forced by hand, the watchdog comparing rows against deals
Acceptance on every step: the stronger model

Resume prompt: <calls the skill by name and names this task folder>
```

**A:** Here is the whole plan. I picked models by how hard each step is — if that is
fine, confirm, and if you want one changed, say which. And: shall we build now, or
pause and pick it up tomorrow from the finished spec?

**P:** Pause. Tomorrow.

**A:** Here is a short prompt to paste into a new session tomorrow. It calls me and
names this folder, and I pick up from the build without asking you anything again.
In the state file: stages 0 to 4 accepted, next action is step 1 of the build.

---

## The next day

The person pastes the prompt. The Architect reads the state file, then the plan, then
the spec, then the brief — in that order — and starts the build. Nothing is asked
again.

---

## Stage 5. The build

Three steps, one Builder each. Step 1 came back once: on a second run the same day the
rows were being added instead of replaced, so one deal appeared twice. The finding
named the day it happened on, what had to change, and that the same day must be run
twice again to close it. Fixed, re-run, closed. The person was not told.

---

## Stage 6. The full run and the finish

```
Ready to use.

Checked:      the three days you gave me, every person's counts as you named them.
              An ordinary day. A deal with an empty field — kept, counted on its own
              line. The CRM not answering — the sheet says so instead of going blank.
              Two runs on the same day — one row per deal. The morning schedule,
              forced by hand. The watchdog.
Not checked:  a month boundary — the month has not turned since we built it. The
              rule is written and will hold on the 1st, but I have not watched it.
If it breaks: no new rows in the morning → the key has most likely expired, the
              guide says where to put the new one. The watchdog says "not working" →
              say "improve this" and quote its line.
```

**Watchdog line, at the top of the funnel sheet every morning:**

> Working. Checked: two control days came out as expected, row count matches the
> deal count, last run today 7:15.

**A:** One last thing. Next to the sheets there is an observations file the watchdog
adds to — a day with far fewer deals than usual, the CRM slowing down, a field that
changed shape. When you have time, say "some improvements have piled up, let us talk"
and I will read it first.
