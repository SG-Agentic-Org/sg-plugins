# Adopt an existing folder — the migration flow

Many people will not start from an empty folder. They already have a messy work folder —
hundreds of subfolders, a mix of projects, content, plans, contractors, briefs, reports,
spreadsheets, archive, and junk. This mode turns that folder into a MnemaOS memory layer
**without losing anything and without touching a file before the user approves the plan**.

Use this **instead of** SKILL Phase 3 when the user chose "adopt an existing folder" in
Phase 0. Run SKILL Phase 1 (the interview) first for the environment questions; this file
replaces the generation step.

## The one rule that overrides everything

> **Read-only until the user approves the restructuring plan. Nothing is written into the
> adopted folder before approval — not even the migration map. Then back up the whole folder
> before moving a single file. Copy into the new structure — never delete the originals as
> part of the move.**

If you are ever unsure whether an action is allowed yet, it is not. No move, no rename, no
delete, and no new file inside the adopted folder happens before approval. The backup is
non-negotiable and happens before the first move.

## Step 1 — Read-only audit

Walk the folder **read-only**. Do not write, move, rename, or delete anything.

- Build a count: total files, total subfolders, depth, file types (`.md`, `.docx`, `.xlsx`,
  `.pdf`, images, etc.).
- Sample-read enough files to understand what is there. Do not read every file in a huge
  folder — sample by folder and type.
- Note obvious sensitive content (credentials, private documents) so the plan handles it
  carefully. Never copy a secret into a generated file.

## Step 2 — Build the folder map

Produce a map of the folder's documents and subfolders, classifying each cluster into the
material types MnemaOS understands:

| Material type | Goes toward | Examples |
|---------------|-------------|----------|
| **Projects** | `projects/` | a folder per initiative, with its working files |
| **People** | `people/` | folders/files about clients, colleagues, contractors |
| **Decisions** | `decisions.md` (or cards) | recorded choices, approvals |
| **Sources** | source library `RAW/` (if on) or `cards/` | reference docs, articles, research |
| **Working files** | inside the relevant `projects/<slug>/` | briefs, reports, spreadsheets |
| **Archive** | `archive/` (kept, not deleted) | finished/old material |
| **Junk / duplicates** | flagged, NOT auto-deleted | temp files, obvious dupes |

The map is a table the user can read: source path → proposed destination → material type.

**Do not write this map into the adopted folder before approval.** Show it inline in chat so
the user can review it. If it is too large to show comfortably, write it to a temp location
**outside** the adopted folder (e.g. the host's temp dir, or a sibling
`<folder>-mnemaos-plan/` next to — not inside — the adopted folder) and link to it. The
adopted folder stays untouched until step 4, after approval. This rule is absolute: a draft
file in the source folder before approval is a contract violation, even though it edits no
existing file.

## Step 3 — Propose the new structure and wait

Show the user:

1. The proposed MnemaOS vault structure (the standard skeleton, plus `archive/` and the
   optional source library if they want it).
2. The migration map (step 2): what goes where.
3. What you will flag rather than move (junk, duplicates) — for them to decide.

Then **stop and wait for explicit approval.** Do not proceed on a vague "looks fine"; confirm
they approve the plan. Adjust the map on their feedback and re-show it. Nothing moves yet.

## Step 4 — Full backup (before any move)

Once approved, **first** make a complete backup of the original folder:

```
<folder>/_mnemaos_backup/original-YYYYMMDD-HHMMSS/
```

The backup lives *inside* the adopted folder, so a naive "copy the whole folder into the
backup" recurses into itself. Do it deterministically:

1. **Manifest first.** List the original top-level entries of the adopted folder and record
   the file count (this is the verification baseline). Capture this list *before* creating the
   backup directory so the backup folder itself is not in the manifest.
2. **Create** `_mnemaos_backup/original-YYYYMMDD-HHMMSS/`.
3. **Copy each top-level entry from the manifest** into the backup — explicitly **excluding**
   `_mnemaos_backup` itself and any temp/draft files. Never copy the adopted folder as a single
   whole into a subfolder of itself; iterate the manifest entries instead.
4. **Verify**: the file count under the backup must equal the manifest baseline. If it does not
   match, stop and report — do not migrate without a verified backup.

This is the safety net: if the migration goes wrong, the original is intact and recoverable.

## Step 5 — Deploy the MnemaOS structure

Create the standard vault skeleton (the `assets/vault-template/` files: `_start-here.md`,
`profile.md`, `projects/`, `people/`, `cards/`, `decisions.md`, `lessons.md`, `inbox.md`,
`_index.md`, `README.md`), plus `archive/` and the optional source library if chosen. Fill
`_start-here.md` and `profile.md` from the Phase-1 interview answers.

## Step 6 — Lay the material into the new structure

Following the approved map, **copy** the user's files from the backup into the new structure.
Copy, do not move-by-delete: the backup stays whole. Create a project card/README for each
project folder (`projects/<slug>.md`, with valid frontmatter) and a person card for each
person folder (`people/<slug>.md`). Put the project's **working files** (briefs, reports,
spreadsheets, raw docs) inside `projects/<slug>/files/` — these are working files, not cards,
so they keep their original content and need no frontmatter (see the cards-vs-working-files
rule in `memory-model.md`). Where a file is a source worth distilling, place it (or a pointer)
per the chosen module.

Do not silently rewrite the user's file contents. Restructure where things live; preserve
what they say.

## Step 7 — Index the new structure (required)

After laying things out, index the result:

1. Run `python3 {{package_path}}/scripts/index_vault.py {{vault_path}}` to build `_index.md`
   and report broken links and cards missing frontmatter.
2. Create the first cards for projects/people/decisions/sources surfaced by the migration
   (those not already carded in step 6).
3. Run the structural smoke test (`scripts/smoke_test.py {{vault_path}}`).

## Step 8 — Write the migration report

Produce, in the vault:

- **`migration-report.md`** — what was found (audit summary), what moved where, what was
  flagged as junk/duplicate (and left for the user), what was backed up and where, and what
  to check. Written for the user, in plain language.
- **`migration-map.csv`** (or `.json`) — the machine-readable source→destination map, one row
  per file/folder, with the material type and the action taken (copied / flagged / archived).

## Step 9 — Explain what changed and how to work now

Walk the user through: the new structure, where their old folder is backed up, how the agent
now reads the memory (startup), how to close work into it (closure), and what you flagged for
them to decide. End with the smoke-test result and a `computer://` link to the migration
report if the host renders it (otherwise the absolute path).

## How to resolve placeholders

- `{{package_path}}` → where the MnemaOS package lives (so `scripts/` resolves).
- `{{vault_path}}` → the folder being adopted (it becomes the vault in place; the backup is
  a subfolder of it).
- If the host cannot run Python: do the index and smoke checks by reading the vault directly,
  and say which mode applies.

## Failure handling

- If the user does not approve, stop. Nothing has been written into the adopted folder at all
  (the map was shown in chat or kept outside the folder).
- If the backup cannot be verified (file count mismatch, no disk space), stop and report —
  do not migrate without a verified backup.
- If a move would overwrite something, stop and ask; never clobber silently.
