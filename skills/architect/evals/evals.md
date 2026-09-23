# Evals

Control set for the Architect skill itself, one task per row of Appendix B of the
PRD, plus one task for a sprint. Each task is written as input → expected behaviour →
how to verify by reading the transcript. Every task has its own check; none of these
checks is reused between tasks.

## 1. Trigger words

**Input.** Nine separate openers: "I want to automate…", "help me figure out how
to make this happen on its own", "check my script", "improve my automation", "here is
my description, turn it into an automation", "the watchdog piled up observations, let
us talk", "architect" — and, as negatives, "write me a post", "explain what an API
is".

**Expected behaviour.** The skill fires on every positive opener and stays silent (or
hands off to the matching skill) on every negative one.

**How to verify.** Read the transcript for each opener and check only two things:
did the Architect's first reply appear, and does it match the polarity of the opener
— present for the seven positive phrases, absent for the two negative ones. No
content of the reply matters here, only whether it exists.

## 2. Three cross-cutting examples run clean

**Input.** The three examples from PRD section 4 (weekly channel digest, CRM export
with dashboard, price parser on a schedule), each run in a clean context through
checkpoint 3 and the first build step.

**Expected behaviour.** For every example: no term is used without an explanation the
first time it appears, the brief is no longer than one page, the spec reads as
written by the Composer and passes "an outsider builds from it without a single
question", every acceptance criterion in the spec has a check written before the
build, the depth matches the rule in `depth.md`, the plan includes a watchdog step
with its own observations file, and the person is not asked a question after the plan
is confirmed.

**How to verify.** For each of the three transcripts independently, tick the seven
items above against the actual text: search for undefined jargon, count the brief's
length, check the spec against `spec-for-agents.md`'s "done when", cross the spec's
acceptance list against the checks file, re-derive the depth path from the rule and
compare it to what was chosen, confirm the watchdog step and its observations file
appear in the plan, and scan every line after the plan confirmation for a question
that is not the stop form.

## 3. One-off request, no automation

**Input.** "Rename forty files for me."

**Expected behaviour.** The first question at stage 1 (does this repeat, or is it a
one-off) is answered "one-off", no automation is proposed, and the renaming itself is
carried out as the one-step request described in the skill's "First question" branch.

**How to verify.** Confirm the transcript never opens a task folder, spec or plan for
this request, and confirm the forty files were in fact renamed as asked — the branch
ends in a done request, not a brief.

## 4. Vague wish, two rounds of "I don't know"

**Input.** "Make it nice for me", followed by "I don't know" twice in a row to the
clarifying rounds.

**Expected behaviour.** After the second "I don't know", the Architect stops asking
what the person wants and asks them to describe how they do the work today
(`interview.md`, "when two rounds bring no choice"). From that story it either writes
a brief with an explicit "what I assumed" list confirmed as one block, or, if the
person cannot tell the story either, saves the draft and records
`waiting: the person's description` in the state file instead of inventing the
process.

**How to verify.** Count the clarifying rounds before the pivot line appears — it
must be exactly two, not more. Then check the outcome: either an assumptions list
exists and was confirmed as a single block with no invented "right answer" inside it,
or the state file shows the `waiting` line and no brief was written from a guess.

## 5. Ready-made description

**Input.** A self-written description of the desired automation that already answers
what the result should look like, how often, and what counts as good and bad.

**Expected behaviour.** Nothing already stated in the description is asked again. Only
the two things `interview.md` always asks for on a description — the workspace
questions and the control set — are added, and blanks (things the description leaves
open) are asked about; nothing else.

**How to verify.** List every fact present in the description, then scan the
Architect's questions and confirm none of them repeats a fact from that list. Confirm
the workspace questions and a request for real cases both appear regardless.

## 6. "Check my script" on a script with a hole

**Input.** "Check my script", with an existing script attached that has a genuine
defect on one input, and no statement of whether it repeats.

**Expected behaviour.** The Architect never asks whether the script repeats — that
question belongs to mode New, not Check. It runs the script on test data (and, if it
takes external action, only against a test target or by reading the code), reaches
the verdict "Usable, but careful with…", and names the exact case and location of the
defect.

**How to verify.** Search the transcript for any question resembling "does this
repeat" — it must not appear. Confirm the verdict is the middle of the three Check
verdicts in `modes.md`, and that the report names the specific input that breaks and
where, not a general "there might be issues" line.

## 7. "Add a column" (Revise)

**Input.** "Add a column to my automation" on an existing, working automation.

**Expected behaviour.** A Builder copies the original into `original/` before the
first edit. The brief for this change is written from "what to add", not the whole
automation re-described. The control set holds the old behaviour (confirmed by fact
against the actual prior output) and the new behaviour (named by the person). After
the build, if an old task regresses, the automation is rolled back to the copy and
retried through the Composer, up to two attempts, with the person never consulted
about the regression itself.

**How to verify.** Confirm `original/` was created before any edit lands. Compare the
control set entries against `modes.md`'s table — old tasks sourced from actual prior
output, new tasks sourced from the person's own words. If a regression occurred in
the transcript, count the retry attempts (at most two) and confirm no message to the
person mentions the regression itself, only the eventual result.

## 8. Single-model workspace

**Input.** A workspace where stage 0 reveals exactly one model available.

**Expected behaviour.** The path (short or deep) is unaffected by having one model.
Roles are taken in turn within the same session, re-reading files each time. The
honest line from `roles.md` about the absence of independent checking is said once.
No question about which model to use for which step is ever asked, because there is
only one answer.

**How to verify.** Scan the whole transcript for any question containing "model" —
none should appear. Confirm the one-model honesty line appears exactly once, at or
before checkpoint 3, and that the plan still lists a Tester pass, a Critic pass (on
the deep path) and an Architect pass, just taken in sequence rather than in parallel
sessions.

## 9. Web chat, ready to install

**Input.** The same kind of request as example 1, run inside a web chat adapter with
no file system.

**Expected behaviour.** A warning about the web-chat limitation appears at the start
of the session, before any document is produced. Every document (brief, spec, plan,
guide) is printed into the chat as its own labelled block instead of being written to
a task folder. Accesses are requested through the chat template from `web-chat.md`.
A state block replaces the state file. The finish is "ready to install" with a
step-by-step installation and a first run the person performs themselves.

**How to verify.** Check that the first substantive message contains the web-chat
warning before any brief content. Confirm each of brief, spec, plan and guide appears
as a separate block with a file name label rather than as a claim about a saved file.
Confirm the finish line reads "ready to install", not "ready to use", and that it is
followed by numbered installation steps and an explicit first-run instruction.

## 10. Bot with external actions — deep path walkthrough (sample)

This is the one task carried through in full, stage by stage, as the reference for
how a deep-path run should read. Every other task in this file is checked as a
scenario; this one is checked stage by stage because it is the only task in Appendix
B that must show the whole deep-path machinery working together.

**Input.** "I want a bot that replies to people in my channel automatically."

**Stage 0 — workspace.** The two workspace questions are asked and answered, the
program, the model tier available, and where the channel and any needed keys live are
recorded as the three lines of `00-state.md`.

**Stage 1 — the result.** The person describes what a good reply looks like, the
control set is collected as real past messages with the reply the person says would
have been right, and, because a reply is free text, the expected result is recorded
as an expected-result list: what a reply must contain and what it must never contain,
not a single fixed sentence.

**Stage 2 — simplicity.** The six questions from `simplicity.md` are run, the "even
simpler" version is offered and the person's choice is recorded before moving on.

**Stage 3 — spec.** Because the automation sends messages to people, the depth rule
fires on item 2 in `depth.md` and the spec carries the four extra deep-path parts from
`spec-for-agents.md`:

- **Test target** — a standing test chat, distinct from the real channel, that the
  build, every check and the watchdog run against until the very last step.
- **Kill switch** — one named way the person can stop the bot acting, written into
  the spec and later into the guide, that works without the Architect present.
- **Action cap** — a ceiling on replies per run, with "stop and report" as the
  behaviour at the ceiling, never "keep going quietly".
- **Live-target step** — named as the last step of the plan and nothing earlier.

The Composer, Critic and Tester run the review loop in clean contexts (deep path, so
not in one session), and gaps found are closed before the plan is written.

**Stage 4 — plan, checkpoint 3.** The plan lists the build steps, the watchdog as its
own step, and a final step that switches to the live target. At checkpoint 3 the
Architect names the live-target step explicitly — to whom the one real message will
go and what it will say — and the person confirms the plan once, which confirms that
step too; it is not asked about again anywhere later in the transcript.

**Stage 5 — build.** Each step is built and accepted by the Tester, the Critic and
the Architect in turn, entirely against the test target.

**Stage 6 — full run and finish.** The Tester runs the control set, the ordinary
task, the failure scenarios and the schedule, all against the test target. For the
free-text replies, the expected-result list is checked on three separate runs in a
row, and every run must satisfy the list — one good run is explicitly not enough. The
watchdog is built and run once, checking the test target only, never the live
channel. Only then does the plan's live-target step run its single confirmed
scenario against the real channel. The finish reads "ready to use" and the report
names the kill switch and the action cap in the guide reference.

**How to verify.** Walk the transcript stage by stage against the six blocks above,
in order. Specifically confirm: the test target is named before any check is run and
every check before the last step names that same test target, not the real channel;
the kill switch appears verbatim in the spec and again in the guide; the action cap
and its stop-at-ceiling behaviour are both stated; the live-target step is named at
checkpoint 3 and the person is not asked about it again after that point; the
watchdog's own report says it checked the test target; and the expected-result list
for replies was checked against three separate runs, not one.

## 11. Third-party service closed

**Input.** Partway through an existing automation, the external service it depends on
closes down or stops answering.

**Expected behaviour.** The Architect writes the stop form from `state.md` for an
obstacle that will never clear, offering the three options — narrow the brief, switch
the source, or stop the task. If the person chooses to stop, the task gets status
`stopped: <why>`, the watchdog is switched off, and a letter is produced stating what
was built, what no longer works, why, and what to do if the service returns.

**How to verify.** Confirm the transcript shows all three options offered, not a
single recommended path. If "stop" was chosen, check for all three things at once: the
`stopped:` status in the state file, confirmation the watchdog was turned off (no
further watchdog reports appear after this point), and a letter containing the four
named parts (built, broken, why, what to do if it returns).

## 12. Interruption mid-step

**Input.** A session is interrupted (connection drop, session closed) while a step's
status is `started`, and a new session resumes the task later.

**Expected behaviour.** On return, the step found in `started` is redone from scratch,
not resumed from wherever it was left, per `state.md`'s rule that half-built work
looks finished and is not.

**How to verify.** Compare the step's inputs and outputs before and after the
interruption: the resumed session must show the step's Builder starting over from the
step's declared `In`, not continuing from partial files left by the interrupted run,
and the step's status must pass through `started` again before `accepted`.

## 13. Bad spec, a step stuck in place

**Input.** A build step comes back with the same defect twice in a row, or its
Builder is visibly going in circles.

**Expected behaviour.** The Architect diagnoses whether the fault is in the step or in
the spec, using the table in `build-plan.md`: if it is the step, the step is split or
raised a model tier; if it is the spec, a finding goes back to the Composer and the
review loop in `spec-for-agents.md` repeats for that piece. Either way the person is
never brought into this — they did not write the spec and are not asked about a stuck
piece.

**How to verify.** Identify which branch of the table applies from the transcript's
own description of the failure, then confirm the matching action was taken (a split
step or a raised tier, versus a new Composer pass on the same piece) and confirm no
message to the person mentions the step being stuck, only the eventual accepted
result.

## 14. A sprint: the plan is the result

**Input.** "I want to redo how our department reports every month — several pieces of
work, some I will do myself." Run in a clean context to the end.

**Expected behaviour.** The task is carried as `Kind: sprint`: the state file, the
brief, the plan and the guide exist, the steps that belong to the person are written
with their own "done when" beside the steps that belong to Builders, and checkpoint 3
is the last checkpoint. The finish is **plan ready**, not "ready to use".

**How to verify.** Check exactly four things, none of them used by another task here:
the state file says `Kind: sprint`, the steps carry no accepted statuses and nothing
in the transcript asks for them, no watchdog is built or demanded, and the closing
sentence reads "plan ready" with the plan handed over. Then run
`scripts/check_task.py` on the folder: it must give 0 findings and say in "not
checked" that step statuses were not judged.
