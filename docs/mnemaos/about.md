# About MnemaOS

A longer description for anyone deciding "should I install this or not." Plain language, no
marketing foam.

## What MnemaOS is

MnemaOS is an installable skill package for your LLM. You run it once. It interviews you about how
you actually work — who you are, your projects, where you run your AI, where you keep files — and
then it builds you a **memory system**: a local folder of plain Markdown ("a vault") plus four
small skills your agent uses to read and maintain that folder.

The package is the installer. The vault is your data. They are independent: remove the package and
your memory is still a folder of files you own.

## Who it's for

People who work with an LLM regularly and are tired of starting every session from zero. You can
be:

- a non-technical web-chat user (ChatGPT, Claude in a browser),
- someone running a coding agent or a desktop AI app,
- an advanced user who already keeps an Obsidian vault and wants protocols on top of it.

You do not need to know how any of this works under the hood. The onboarding adapts its language
to you.

## The pain it solves

Three problems, every day:

1. **Your AI forgets.** Each new chat, you re-explain who you are, your projects, your tone, what
   you already tried.
2. **Your notes are passive.** Even if you keep notes, the AI doesn't read them on its own and
   doesn't keep them tidy.
3. **There's no ritual.** Nothing captures what a finished task taught you, so it evaporates.

MnemaOS fixes all three with a folder the AI reads automatically (startup), writes back to when
work ends (closure), distills into clean linked cards (distillation), and tidies on a schedule
(hygiene).

## How it differs from the obvious alternatives

- **A plain Obsidian vault** stores notes for *you* to read. MnemaOS adds the protocols that make
  the *AI* read and maintain them. Obsidian is the filing cabinet; MnemaOS is the assistant who
  uses it. (And MnemaOS works fine without Obsidian — plain Markdown opens anywhere.)
- **A "remember this about me" prompt** is one fragile paragraph the model may drop. MnemaOS is a
  durable, structured, versionable folder with a contract the skills enforce.
- **RAG / a vector database** needs embeddings, a server, and infra. MnemaOS retrieval is
  deliberately boring: read the index, open the file. Plain text you can search and diff. No
  vector index — and none is required.
- **SaaS memory products** lock your memory inside a vendor. MnemaOS is local-first: your files,
  your machine, no account, no lock-in.

## How greenfield works

You start from an empty folder. Onboarding asks six short groups of questions (who you are and
your projects; where you run your AI; where files live; Obsidian or plain Markdown; how much the
agent may do unattended; how deep a memory you want). Then it generates:

- a vault skeleton (`_start-here.md`, `profile.md`, `projects/`, `people/`, `cards/`,
  `decisions.md`, `lessons.md`, `inbox.md`, `_index.md`, `README.md`), filled with your real
  answers and starter cards;
- the four memory skills, resolved to your setup;
- a `SETUP.md` with the install/routine steps that actually apply to your host.

It finishes with a smoke test and a tiny live dry-run so you watch the memory work before you
trust it.

## How adopt-existing-folder works

Many people don't start empty — they have a messy work folder built up over years. MnemaOS turns
that into a memory layer **without losing anything**:

1. **Read-only audit.** It walks the folder and counts what's there. It writes nothing.
2. **Folder map.** It classifies clusters into projects / people / decisions / sources / working
   files / archive / junk, and shows you a source→destination map (in chat, or in a temp location
   **outside** your folder — never inside it before you approve).
3. **Proposal + approval gate.** It proposes a structure and **stops**. Nothing moves until you
   approve.
4. **Full backup.** Once approved, it makes a complete timestamped backup
   (`_mnemaos_backup/original-YYYYMMDD-HHMMSS/`) and verifies it by file count **before** any move.
5. **Copy into the new structure.** Your files are *copied* (never deleted as part of the move).
   Junk and duplicates are *flagged* for you, not auto-deleted.
6. **Index + report.** It builds `_index.md`, runs the smoke test, and writes a `migration-report.md`
   plus a machine-readable `migration-map.csv`.
7. **Walkthrough.** It explains what changed, where the backup is, and how to work now.

The one rule that overrides everything: **read-only until you approve; back up before the first
move; copy, never delete the originals.**

## What happens to your existing files (in plain terms)

Nothing, until you say yes. After you approve: a full backup is made first, your files are copied
into the new structure, and the originals stay intact in the backup. If you don't like the result,
revert from `_mnemaos_backup/`. Junk is flagged, not deleted — the decision stays with you.

## What MnemaOS does not do — and its boundaries

- It will not publish anything, message anyone as you, make a payment, change permissions, or
  delete significant data **without your explicit consent**. When it hits such a limit it stops
  and tells you, with the reason.
- It does not run anything in the cloud you can't see. If your host can't run a routine
  unattended (e.g. web chat with no file access), it says so and gives you a manual fallback —
  it never fakes automation.
- **MnemaOS does not include:** any MCP server; vector retrieval / RAG / embeddings; a mobile
  companion; cross-device or cloud sync; a knowledge-graph export. It is a local Markdown memory
  system and works fully as one.

## Privacy and local-first

- Plain Markdown on your machine. No SaaS, no account, no telemetry.
- No vendor lock-in: the vault is portable files; the package and the vault are independent.
- No secrets in files. This package needs no credentials. The built-in smoke test flags inlined
  secrets in your text and config files (Markdown, `.env`, `.json`, etc., including the backup)
  and any leaked reference-implementation name or path.

## The three reference scenarios

**Vika — email marketer, web-only ChatGPT.** No CLI, no local files, no scheduling. MnemaOS builds
a clean vault from scratch and ships startup/closure as copy-paste blocks; routines are manual
trigger phrases. It never promises automation her setup can't run. She ends up with projects,
campaigns, hypotheses, results, tone of voice, and lessons her AI reads on demand.

**Katya — content & SEO lead, large messy folder, willing to install Codex.** MnemaOS recognises
the existing-folder case, audits read-only, maps the folder, proposes a structure, waits for her
approval, backs everything up, copies her files into the new layer, writes a migration report, and
runs the index + smoke test. She ends with a clean memory and her original folder safely backed up.

**Advanced user — already has an Obsidian vault and a personal graph.** MnemaOS does not rebuild
anything. It overlays non-destructively: adds the startup/closure/hygiene protocols, an index, and
"bridge" cards that *link into* existing notes. Existing files stay byte-for-byte unchanged. He
adopts the protocols he wants and leaves the rest of his system as-is.

## Install (short)

1. Copy the `mnemaos/` folder into your agent's skills directory.
2. Ask your agent to "set up my memory with MnemaOS."
3. Answer the six-dimension interview.
4. Watch it run the smoke test and dry-run.

That's it. The rest is your memory, growing as you work.
