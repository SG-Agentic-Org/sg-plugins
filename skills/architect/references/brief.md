# Brief and solution

Open this when writing the brief or the solution.

These two are the only documents the person is ever asked to approve. Everything
built afterwards is measured against them, and nothing may appear in the automation
that is not here. So they are written in the person's own words, at one page each,
and shown whole.

## The brief

One page, plain language, seven parts in this order:

```
What I want, and who it is for
What comes in          — the sources, named the way the person names them
What should come out   — the shape of the result, and where it appears
How often
How we will know it works — the control set, each case with the answer the person named
What we are not doing  — the things ruled out on purpose
What I assumed         — everything filled in that the person did not say
```

Write it in their words. A brief in your vocabulary gets a polite yes from someone
who did not follow it, and that yes is worthless at the finish.

"What we are not doing" is not padding. It is the line an agent is later told not to
cross, and anything not written here will eventually be built by someone being
helpful.

"What I assumed" holds only your fills, never the expected results — those are the
person's, as `interview.md` says.

## The solution

On the deep path the solution is its own document and its own checkpoint:

```
What the code does     — everything countable and every fixed rule
What the model does    — only the parts that need wording or judgement
What comes out
How we will check it
What we are not doing
How it works           — the diagram in sentences, below
Even simpler           — the smaller version, below
```

Numbers and rules belong to the code, always. A model asked to add up figures gives
a different total on a different day, and nobody notices for weeks.

### The diagram in sentences

No pictures, no arrows, no boxes. Three to six numbered sentences, each one a thing
that happens and what it leaves behind:

```
1. Every Monday at 9 the script opens the public page of the channel and reads the
   last two weeks of posts.
2. It writes one row per post into the sheet: date, first line, views.
3. It works out the average and marks every post that beat it by half again.
4. The model reads the marked posts and writes three ideas, each tied to one of them.
5. The ideas go into the second sheet, under that week's date.
```

A person reads five sentences and says "no, not the last two weeks, the last month".
The same thing drawn as a picture gets nodded at.

## Even simpler

Every solution is shown together with a smaller version of itself: the same result
with one part taken out — the part that the six questions in `simplicity.md` found
hardest to justify. It is presented, not argued for:

> **Choosing between the two** (translate to the person's language)
> "Here is what I would build, and here is a simpler version without the ideas —
> just the table. Which one do you want?"
> Recommended answer: the simpler one, unless the part it drops is the reason you
> asked for this at all.

Show it as a real option you would happily build, not as a strawman. If you only
ever offer the big version, you are deciding for someone who asked you not to.

## The short path

On the short path there is one document, not two: the brief, with "How it works",
"Even simpler" and "How we will check it" added to the end of it. One checkpoint,
one approval, both questions in one breath:

> **The merged checkpoint** (translate to the person's language)
> "Here is what I understood you want, and here is how I would build it, with a
> simpler version underneath. Is this what you wanted, and which version do you
> want?"
> Recommended answer: confirm the brief first, then take the simpler version if you
> can live without what it drops.

Which path you are on is decided by the rule in `depth.md`, not by how big the
document turned out.

After this approval the person's part is done. They are met again at the plan, and
after that only at a stop.
