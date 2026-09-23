# Example: a weekly digest of a Telegram channel

Mode **New**, short path, platform Claude Code. A full walk from stage 0 to stage 6.
The person had never set anything up with an AI assistant before.

Lines marked **A** are the Architect, lines marked **P** are the person.

---

## First question: is an automation needed

**A:** Before we build anything — is this something that comes back every week, or a
one-off you need done once?

**P:** Every week, every Monday.

**A:** Then it is worth automating. Two quick questions about what you work with, and
then I will ask what you want to see.

---

## Stage 0. What you work with

**A:** Which program do you use to talk to an AI assistant, and which plan are you
on? I ask so I can pick helpers that fit what you have.
*My guess: the one you have open right now — name it, and if you can see a list of
models in its menu, tell me what is in it.*

**P:** This one, Claude Code. The menu shows three models.

**A:** Good, three is the comfortable case — I can put the cheap one on the simple
work and the strongest one on checking. Next: where does the material live that this
should work with — a spreadsheet, a customer database, a channel, a folder on your
computer?

**P:** A Telegram channel I run. It is public, anyone can open it in a browser.

**A:** Then nothing needs to be handed over: a public channel has a web page that
opens without logging in, and that page is enough. Is there anything else it should
touch?

**P:** No.

State file, workspace lines: Claude Code, three models, files and a scheduler on this
computer — a scheduler is the thing on your computer that starts a job at a set hour.
Source: the public web page of the channel. No accesses needed.

---

## Stage 1. What you want to get

**A:** When this is all working, what do you see, and how often?
*My guess: Monday morning, you open one page and it is already there.*

**P:** Monday morning I want to see which posts did well, which flopped, and get some
ideas for what to write next.

**A:** Three rounds and we are done. First: over what stretch of the channel?
*My guess: the last two weeks — long enough to compare, short enough to still be
about now.*

**P:** Two weeks, yes.

**A:** What counts as "did well"? You could mean the top three posts, or anything
clearly above your usual.
*My guess: anything that beat your own average by half again — that way a quiet week
does not fake a winner.*

**P:** The second one.

**A:** And in what shape — a plain list, or a page with the numbers and a chart that
refreshes itself?
*My guess: the page, since you are going to look at it every week.*

**P:** The page.

**A:** Last thing, and this is the one I cannot fill in for you. Give me two or three
real posts from the past weeks and tell me, for each, whether it should come out as
a winner or a flop. That is how we tell later whether this is doing the right thing.

**P:** These two were winners, this one flopped.

**A:** The ideas are free text, so there is no single right answer for them. Instead
of one, we agree on a list of what an idea must be: three ideas, each tied to a
specific post from the list, no general advice like "post more often". Right?

**P:** Right.

**A:** Then we go the short way here — this only reads a public page and writes into
your own file, so a mistake shows up in front of you straight away.

---

## Checkpoint 1 and 2 together: the brief

On the short path the brief and the solution are one document and one approval.

```
01-brief.md

What I want, and who it is for
  Every Monday morning, one page showing which of my posts did well over the last
  two weeks and which did not, plus ideas for what to write next. For me alone.

What comes in
  The public web page of my channel — the one anyone can open without logging in.

What should come out
  A page with one row per post (date, first line, views), the strong ones marked,
  and three ideas underneath.

How often
  Monday morning.

How we will know it works
  Post from the 4th → winner. Post from the 9th → winner. Post from the 12th →
  flop. Ideas → three of them, each tied to one named post, no general advice.

What we are not doing
  No history beyond two weeks. No other channels. Nothing is posted anywhere.

What I assumed
  "Did well" means beating your own two-week average by half again.
  A post with no view count shown is counted as zero and named on the page.

How it works
  1. Every Monday morning a script — a small program that runs on its own — opens
     the public page of the channel and reads the posts of the last two weeks.
  2. It writes one row per post: date, first line, views.
  3. It works out the average and marks every post that beat it by half again.
  4. The model reads the marked posts and writes three ideas, each tied to one.
  5. The ideas go onto the same page, under this week's date.

How we will check it
  The three posts above, the idea list three times in a row, an ordinary week, the
  page not opening, fewer than ten posts, a post with no views.

Even simpler
  The same page without the ideas — just the table with the strong posts marked.
```

**A:** Here is what I understood you want, and here is how I would build it, with a
simpler version underneath. Is this what you wanted, and which version do you want?
*My guess: confirm the brief first, then take the simpler one unless the ideas are
the reason you asked.*

**P:** The ideas are the reason. The full one.

**A:** Then your part is done. I will come back once more with the plan, and after
that only if something is missing that only you can give me.

---

## Stage 3. The spec

**A:** The spec for the agents is ready. It is not written for you, you do not have
to read it.

What happened out of the person's sight: the Composer wrote a one-page spec — how the
script reads the public page, the shape of the table, the average and the margin,
what happens when a post has no views, when there are fewer than ten posts, when the
page does not open (say so on the page itself, do not fail silently), what the model
returns and what it must not do, and the watchdog on Tuesdays.

The Architect read it against the brief first. Then the Critic: "the spec keeps a
year of history, the brief says two weeks" — off the brief, the Composer cut it. Then
the Tester wrote a check per criterion and hit a gap: it could not write a check for
"the model returns four ideas instead of three", because the spec never said what
happens then. An uncheckable criterion is a gap, so it went back to the Composer, who
added the rule. Second round, no gaps left.

---

## Stage 4. The plan

```
04-plan.md

Step 1  Read the page and build the table
  Builder    a Builder in a clean context
  Model      middle
  In         the address of the channel's public page
  Out        one row per post for the last two weeks
  Done when  the three control posts appear with the right dates and views
  Checks     the three control posts, a post with no views, a page that does not open
Step 2  Averages, marking, and the page
  Builder    a Builder in a clean context
  Model      middle
  In         the table from step 1
  Out        the page with the table, the average and the marks
  Done when  the two winners are marked, the flop is not
  Checks     the two winners and the flop, a fortnight with fewer than ten posts
Step 3  Ideas
  Builder    a Builder in a clean context
  Model      middle
  In         the marked posts from step 2
  Out        three ideas under the table
  Done when  three ideas, each naming one marked post, three runs in a row
  Checks     the expected-result list three runs in a row, four ideas returned
Step 4  Schedule and watchdog
  Builder    a Builder in a clean context
  Model      cheap
  In         the finished script from steps 1 to 3
  Out        the Monday run registered, the watchdog and its observations file
  Done when  the Monday run is registered, the Tuesday watchdog writes its line
  Checks     the schedule forced by hand, the watchdog run once
Acceptance on every step: strongest model
```

**A:** Here is the whole plan. I picked models by how hard each step is — if that is
fine, confirm, and if you want one changed, say which. And: shall we build now, or
pause and pick it up tomorrow from the finished spec?

**P:** Fine, and now.

**A:** Then I am not going to need you again until it is ready.

---

## Stage 5. The build

Four steps, one Builder each, none of it reaching the person. Each finished step went
to the Tester, who ran the checks it had written before the build and then broke the
result once on purpose to be sure the check noticed, and to the Architect, who
checked it against the spec and the brief.

Step 2 came back once: a post with no views was being skipped instead of counted as
zero. The finding said what happened, on which post, what to change, and that the
same post must come back as a zero row. The Builder fixed it, the scenario was re-run,
the finding closed. The person heard none of this.

---

## Stage 6. The full run and the finish

The Tester ran the whole thing: the three control posts, the idea list three times in
a row, one ordinary week where nothing should need handling, an empty stretch, a
network drop mid-read, the schedule forced by hand and read back as registered, and
the watchdog once.

```
Ready to use.

Checked:      the three posts you gave me, all three came out as you said. Ideas:
              three runs in a row, three ideas each time, each tied to a named post.
              An ordinary week. Fewer than ten posts. A post with no views. The page
              failing to open. The Monday schedule, forced by hand. The watchdog.
Not checked:  the channel being switched to private — it has not happened, and I did
              not want to change your channel to try it.
If it breaks: the page is not there on Monday → run it by hand, the guide says how.
              The watchdog's line says "not working" → say "improve this" and quote
              that line.
```

**Watchdog line, on the page itself every Tuesday:**

> Working. Checked: two control posts came out as expected, last run Monday 9:03,
> produced a page.

**A:** One more thing, and then I am out of your way. Next to the page there is an
observations file the watchdog adds to — three weeks empty in a row, an idea that
came out outside the list, the page getting slower. When you have time, say "some
improvements have piled up, let us talk" and I will read it first.
