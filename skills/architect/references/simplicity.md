# Simplicity

Open this at stage 2, and whenever the person brings a solution of their own.

## Six questions

You ask these of yourself, not of the person. They show up in the conversation only
as conclusions, and as the smaller version in `brief.md`. A person walked through six
design questions ends up designing the thing, which is exactly what they came here
not to do.

Each question has an answer you can point at, not a feeling.

**1. Is an AI needed here at all, or does a script and a sheet do it?**
Go through the result line by line. Everything that is counting, sorting, comparing
or following a fixed rule is a script. If nothing is left over, there is no AI in
this build, and saying so out loud is the most useful thing you will do all session.

**2. What does the code work out, and what does the model put into words?**
Anything with a number or a rule in it belongs to the code. The model gets what
needs wording or judgement. Split them explicitly, because a model handed the
arithmetic returns a different total tomorrow on the same data.

**3. What does the person keep doing themselves, because it is a decision and not
labour?**
Which of three ideas to run with, whether to send the message, which customer to
call. Automating a decision does not save work, it moves the choice to something
that cannot be held to it.

**4. If this part were removed, what would break?**
Take each part out on paper and name the thing in "what should come out" that stops
arriving. Nothing breaks — the part goes. This is the fastest of the six and it
usually removes something.

**5. What is here for the future and serves no real case in the control set?**
A second source "in case", a setting nobody will change, a general version of
something used once. One real case means build it. Two would mean build for both.
None means it is imagined, and imagined needs are always described more confidently
than real ones.

**6. Can one line do what a hundred do?**
A ready-made feature of a program the person already uses beats a script. A sheet
formula beats a script. A script beats a chain of agents. Take the smallest thing
that produces the result the brief describes.

## What the person hears

Conclusions, in one or two lines, in their words:

> **Reporting the outcome** (translate to the person's language)
> "There is no AI needed for most of this — the counting is all code. The one place
> a model helps is writing the ideas. I dropped the year of history, nothing in what
> you asked for needs it."
> Recommended answer: agree, and say so if something you dropped actually mattered
> to me.

Never report the six questions as a list, and never ask the person to answer them.

## A solution the person brought

If the person arrived with a solution already in mind — their own description, an
approach they read about, something they half-built — it goes through these same six
questions, unchanged and with the same honesty. It is their solution, so say the
outcome plainly and let them keep it if they want to:

> **When their solution loses a part** (translate to the person's language)
> "Your version keeps a copy of everything in a second place. Nothing you asked to
> see needs it, so I would leave it out. Do you want it anyway?"
> Recommended answer: leave it out, and add it back the day something actually needs
> it.

A solution accepted without these questions because the person wrote it is the one
that shows up at the finish as a part nobody can explain.

## Simplicity inside the build

These hold for every piece built later, and the Tester and the Critic check them
when they accept a step:

- **One file, one responsibility.** A file edited for two unrelated reasons is two
  files that have not been separated yet.
- **A piece fits on one screen.** Something you cannot see all of at once is
  something nobody will read before changing it.
- **Dependencies point one way.** If A uses B, B knows nothing of A. Two pieces that
  reach into each other can only ever be understood together, and from then on they
  are one piece with two names.
- **Every rule in the spec has at least one check.** A rule nobody checks is a rule
  that quietly stopped being true — and `verify.md` is where that is enforced.

## Rechecking

These questions are asked once at stage 2 and again whenever the spec grows a part
that was not in the brief. Growth is where the imagined needs arrive, and they
arrive one line at a time.
