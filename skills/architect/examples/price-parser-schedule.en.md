# Example: collecting prices from a website into a table, daily

Mode **New**, short path, platform Gemini CLI with a single model. A full walk from
stage 0 to stage 6.

Lines marked **A** are the Architect, lines marked **P** are the person.

---

## First question: is an automation needed

**A:** Is this something that comes back, or a one-off?

**P:** Every day. I check it every morning and I keep forgetting.

**A:** Then it is worth automating.

---

## Stage 0. What you work with

**A:** Which program do you use to talk to an AI assistant, and which plan are you
on? I ask so I can pick helpers that fit what you have.

**P:** Gemini CLI. There is one model in the menu.

**A:** Good to know, and it changes one thing I will be honest about later. Where does
the material live that this should work with?

**P:** A competitor's website. It is open, no login. I want the prices in a table on
my computer.

**A:** Then nothing needs to be handed over.

State file, workspace lines: Gemini CLI, one model, task folder and a scheduler on
this computer — a scheduler is the thing that starts a job at a set hour. Source: an
open website. Destination: a file on this computer.

---

## Stage 1. What you want to get

**A:** When this is all working, what do you see, and how often?
*My guess: one table on your computer, a new line per day.*

**P:** Once a day I want their prices collected into a table.

**A:** Which pages?
*My guess: a fixed list you give me once, so the table always has the same rows.*

**P:** A list. About thirty of them.

**A:** Which things off each page?
*My guess: the name and the price — anything else is a column you will stop reading
by week two.*

**P:** Name and price is enough.

**A:** And when a price changes — do you want only today's number, or the old one
kept too?
*My guess: keep the old ones. A price history costs nothing to store and cannot be
recovered later if you skip it.*

**P:** Keep them.

**A:** Now the one I cannot fill in for you. Pick three of those pages and tell me
what the right price is on each one today. That is how we tell later whether this is
doing the right thing.

**P:** These three, and the prices are these.

**A:** Short way here. We read an open page and write into your own file — nothing is
sent anywhere and nothing is changed on their side. One line goes into the spec
though: if fewer pages come back than usual, it has to say so rather than quietly
writing a shorter table. A page that silently disappears is how a price history turns
wrong without anyone noticing.

---

## Checkpoint 1 and 2 together: the brief

```
01-brief.md

What I want, and who it is for
  Once a day, a table on my computer with the current prices of about thirty pages
  on a competitor's site, keeping the earlier prices. For me.

What comes in
  The list of pages I gave you. They are open, no login.

What should come out
  One table: one row per page, one column per day, the name of the item beside it.

How often
  Once a day.

How we will know it works
  Page 1 → this price today. Page 2 → this price. Page 3 → this price.

What we are not doing
  No other sites. Nothing is sent to anyone. No alerts when a price moves — just the
  table.

What I assumed
  A page that does not open today leaves an empty cell for today, not a repeat of
  yesterday's price.
  If fewer pages than usual come back, the table says so at the top.

How it works
  1. Once a day a script — a small program that runs on its own — opens every page
     on the list.
  2. It takes the name and the price off each one.
  3. It writes today's column into the table, leaving earlier columns untouched.
  4. If fewer pages answered than usual, it writes that at the top of the table.

How we will check it
  The three pages you picked, an ordinary day, a page that does not open, a page
  whose layout changed, and running it twice on the same day.

Even simpler
  Only today's prices, with no history kept.
```

**A:** Here is what I understood you want, and here is how I would build it, with a
simpler version underneath. Is this what you wanted, and which version do you want?
*My guess: the simpler one, unless the history is the reason you asked.*

**P:** The history is the point. The full one.

**A:** Then your part is done until the plan.

---

## Stage 3. The spec

**A:** The spec for the agents is ready. It is not written for you, you do not have
to read it.

One thing was different here, and it is the honest part I promised: with one model,
the helpers cannot be started blind. They take turns in the same session instead, so
the one checking the work has seen how the work was done. I make up for it by
switching roles properly, re-reading the files each time instead of trusting memory,
and one extra full run at the end. I am not going to call that an independent check,
because it is not one.

The Composer wrote the spec, then the Critic and the Tester went over it in turn. The
Tester found a gap: a page that does not open had no rule, so no check could be
written for it. The Composer added it — an empty cell for that day and a line at the
top of the table. The watchdog checks one page a week against the table.

---

## Stage 4. The plan

```
04-plan.md

Step 1  Read the pages and take name and price
  Builder    a Builder in a clean context
  Model      the one model
  In         the list of thirty page addresses
  Out        a name and a price for every page that opened
  Done when  the three control pages come out with the prices you named
  Checks     the three control pages, a page that does not open, a page whose layout
             changed
Step 2  Write today's column, keep the earlier ones, and the daily schedule
  Builder    a Builder in a clean context
  Model      the one model
  In         the names and prices from step 1
  Out        today's column in the table, the earlier columns untouched, the daily
             run registered
  Done when  a second run the same day overwrites today's column instead of adding
             a second one, and yesterday's column is untouched
  Checks     a second run the same day, yesterday's column, the schedule forced by
             hand
Step 3  Watchdog
  Builder    a Builder in a clean context
  Model      the one model
  In         the finished script and the table
  Out        the watchdog, its weekly report and its observations file
  Done when  it compares one page against the table and writes its line
  Checks     one page compared against the table, the watchdog run once
Roles taken in turn in one session, one model throughout.
```

No question about models was asked: there is one, so there is nothing to choose.

**A:** Here is the whole plan. Shall we build now, or pause and pick it up tomorrow
from the finished spec?

**P:** Now.

**A:** Then I am not going to need you again until it is ready.

---

## Stage 5. The build

Three steps. Step 1 came back once: a page whose price was written with a space
inside the number was being read as a much smaller figure. The finding named the
page, what had to change, and that the same page must come back with the right price
to close it. Fixed, re-run, closed. The extra care the single model called for showed
up here — the checking pass was run twice, from the files, not from memory.

---

## Stage 6. The full run and the finish

```
Ready to use.

Checked:      the three pages you picked, all three at the prices you named. An
              ordinary day, all thirty pages. A page that does not open — empty cell
              and a line at the top. A page whose layout changed — same result, empty
              cell and a line. Two runs on the same day — one column, not two. The
              daily schedule, forced by hand. The watchdog. Then everything a second
              time, because the checks here were not independent.
Not checked:  the site blocking automated reading — it has not done so, and I did not
              want to provoke it into doing so.
If it breaks: the table stops filling → run it by hand, the guide says how. The
              watchdog says the price does not match → the site has changed how its
              pages are built, say "improve this".
```

**Watchdog line, in a file beside the table every week:**

> Working. Checked: one control page matches the table, last run today, thirty pages
> of thirty.

**A:** Last thing. Beside the table there is an observations file the watchdog adds
to — a page that has been empty for three weeks, fewer pages answering than usual,
the site getting slower. When you have time, say "some improvements have piled up,
let us talk" and I will read it first.
