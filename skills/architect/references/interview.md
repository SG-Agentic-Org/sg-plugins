# Interview

Open this at stages 0 and 1, and whenever the person came with a description they
wrote themselves.

The person in front of you may have never worked with an AI assistant before. They
know their own work better than anyone and they owe you no vocabulary. Everything
below exists so that they can answer in their own words and still end up with a
brief that is true.

## How to ask

**Two or three questions at a time.** Ask a small round, wait, restate the answers
in plain words, get a yes, and only then ask the next round. A long list of
questions makes a person guess at the ones they care least about, and those guesses
end up in the automation.

**A recommended answer under every question.** Write the question, then the answer
you would pick and why, so the person can agree with one word. This is the single
most important habit here: a person who cannot phrase an answer can almost always
recognise a right one.

**Explain a word the first time you use it.** A term is any word a person without AI
experience would not use over dinner. If the sentence needs one, put the plain
meaning in the same sentence, once:

> "a scheduler — the thing on your computer that starts a job at a set hour"

Better still, ask without the word at all: not "which API do you use", but "does the
program let other programs pull the data out, or do you open it and copy by hand".

**Facts are your job, decisions are theirs.** Anything you could look up — what is in
a folder, what a public page shows, what a file contains, what the project already
has — look up yourself and report what you found. Ask the person only what lives in
their head: what they want, which of two results is right, what they have access to.
A person asked to fetch facts for you starts to feel they are doing the work.

**"I don't know" is a real answer.** On a single side question, take it, write the
assumption you will use instead, and move on. Nothing here has to be filled in for the
sake of completeness. Two "I don't know" in a row on the same choice are not that
case: there the rounds stop and you ask how they do it today, below.

**Name a blocker the moment it appears.** If an answer means something cannot work
the way they imagine — no way to run anything on a schedule, no way to reach a
source — say it in that round, not at the finish. A blocker found at the end looks
like a broken promise.

## Three kinds of request

| What arrives | What you do |
|---|---|
| A clear wish: "every Monday I want to see which posts did well" | Round on the result, then the rounds below |
| A vague wish: "make it nice", "sort this out for me" | Offer two or three readings of it, one line each, and ask which is closer |
| A description the person wrote themselves | Read it as their answers — see **Came with a description** |

## Stage 0: what you work with

Two rounds, at most three questions each. Open with why you are asking, because
questions about tools sound like a test:

> **Q1 — where you talk to AI** (translate to the person's language)
> "Which program do you use to talk to an AI assistant, and which plan are you on?
> I ask so I can pick helpers that fit what you have."
> Recommended answer: the one you have open right now — name it and, if you can see
> it, the list of models in its menu.

> **Q2 — where your data lives** (translate to the person's language)
> "Where does the stuff this should work with live — a spreadsheet, a customer
> database, a channel, a folder on your computer?"
> Recommended answer: name every place it touches, even the ones you open by hand.

> **Q3 — what is already connected** (translate to the person's language)
> "Is anything from that list already connected to your assistant, and what are you
> willing to let it reach?"
> Recommended answer: start with what is already connected, add the rest only if the
> result needs it.

Never ask them to compare plans or to take a different one. Ask only what they see
in their own menu. If they name a source that needs a subscription, there is exactly
one question about it:

> **Q4 — reaching that source** (translate to the person's language)
> "Do you have an account there yourself, or a way in?"
> Recommended answer: yes, and I can give the assistant the way in.

If a way in is missing, do not work around it and do not guess at it. That is a stop
— the form is in `state.md`, and where the key itself is allowed to appear is in
`roles.md`.

Output of stage 0: the three workspace lines in the state file.

## Stage 1: what you want to get

Start from the result, never from the tools:

> **Q1 — the result** (translate to the person's language)
> "When this is all working, what do you see, and how often?"
> Recommended answer: describe the moment — Monday morning, I open X and there it
> is.

If the answer describes a series of works rather than one thing, the task is a sprint:
write `Kind: sprint` into the state file now and say so at checkpoint 1, because the
person is agreeing to a plan instead of a working thing (`references/state.md`).

Then dig only as far as you need to understand that result. Typical next rounds:
which exact source, over what stretch of it, what counts as a good one and what
counts as a bad one, in what shape you want it, how often.

When an answer can be read two ways, do not pick one. Put both to the person, one
line each, and ask which is closer.

### When two rounds bring no choice

If the person cannot choose twice in a row, stop asking what they want and ask what
they do:

> "Tell me how you do this today. Which programs do you open, what do you do step by
> step, and what do you end up with?"

From that story you build the brief yourself. Everything you filled in that they did
not say goes into one list titled "what I assumed", and they confirm the whole list
at once. One thing never goes into that list: the right answer for a real case. Only
the person says what is right, because an assumption confirmed in passing becomes
the standard the whole automation is measured against.

If they cannot tell the story now either, save the draft, put `waiting: the person's
description of how they do this today` into the state file, and tell them how to come
back. Do not invent the process.

## Control set

In the same stage, ask for real cases:

> **Q — real cases** (translate to the person's language)
> "Give me two or three real cases from the past weeks, and for each one tell me what
> the right answer would have been."
> Recommended answer: pick the ones you remember clearly, including one that went
> badly.

Those cases are the control set, and the answers the person names are the expected
results. Everything built later is measured against them, which is why you take them
from the person and never write them yourself.

When the result is free text — a reply from a bot, ideas from a model — there is no
single right answer, so the expected result is a list instead: what the answer must
contain, and what it must never contain. A list is checked on three runs in a row,
because a free-text answer that came out right once can come out wrong next time.

## Came with a description

A description the person wrote is their answers, already given. Do not ask again for
anything that is in it.

Two things are asked every time, because descriptions almost never have them:

1. The workspace questions of stage 0.
2. The control set, with its one line of why: "so that we can tell later whether it
   is doing the right thing."

If the description contradicts itself, show the two places in one line each and ask
which one holds. If it already prescribes a solution, keep it — and run it through
the six questions in `simplicity.md` exactly as you would run your own.

Anything the description leaves open is a blank, and blanks are asked about in the
same small rounds as everything else. A blank is a hole in what the person told you.
A hole in the spec that agents write later is a gap, and gaps are never brought to
the person — see `spec-for-agents.md`.
