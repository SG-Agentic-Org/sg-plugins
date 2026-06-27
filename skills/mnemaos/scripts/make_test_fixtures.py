#!/usr/bin/env python3
"""
make_test_fixtures.py — generate the three sanitized test scenarios from TEST-RESULTS.md so a
reviewer can reproduce Вика / Катя / advanced-user end to end.

Standard library only. No network, no third-party packages. Produces, under an output dir:

  vika/           — Scenario 1 (greenfield, web-only): a clean generated vault, as MnemaOS would
                    produce it for an email marketer who only uses web-chat ChatGPT.
  katya-src/      — Scenario 2 INPUT: a messy work folder (content + SEO lead) BEFORE migration.
  katya-migrated/ — Scenario 2 EXPECTED OUTPUT: the same folder AFTER a simulated approval +
                    backup + copy + report. This is what adopt-existing-folder produces once the
                    human approves; generated here without the interactive gate so a reviewer can
                    run index + smoke on a reproducible reference result.
  advanced/       — Scenario 3: an existing Obsidian vault with MnemaOS overlaid non-destructively.

The adopt-existing-folder flow itself has a human approval gate by design, so this script does
NOT run the real interactive migration. `katya-src/` is the honest input; `katya-migrated/` is a
faithful simulation of the post-approval result (backup verified, files copied, report written)
so the expected output is reproducible and verifiable.

Usage:
    python3 make_test_fixtures.py <output-dir>

Then verify (all three vaults index clean and pass smoke):
    python3 index_vault.py  <output-dir>/vika
    python3 smoke_test.py   <output-dir>/vika
    python3 index_vault.py  <output-dir>/advanced
    python3 smoke_test.py   <output-dir>/advanced
    python3 index_vault.py  <output-dir>/katya-migrated
    python3 smoke_test.py   <output-dir>/katya-migrated

All content is invented and sanitized — no real person, no private-stack name, no secret.
"""

import os
import sys

DATE = "2026-06-27"


def w(path, content):
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, "w", encoding="utf-8") as f:
        f.write(content.lstrip("\n"))


def keep(path):
    os.makedirs(path, exist_ok=True)
    with open(os.path.join(path, ".keep"), "w", encoding="utf-8") as f:
        f.write("")


def card(id_, type_, title, status="active", extra=""):
    return f"""
---
id: {id_}
type: {type_}
title: {title}
created: {DATE}
updated: {DATE}
status: {status}
tags: []
{extra}---

# {title}

"""


# --------------------------------------------------------------------------------------------
# Scenario 1 — Вика: greenfield, web-only ChatGPT, email marketer.
# A clean vault as onboarding would generate it. No automation promised (web-only).
# --------------------------------------------------------------------------------------------
def build_vika(base):
    v = os.path.join(base, "vika")
    w(os.path.join(v, "_start-here.md"), """
# Start here

> The agent reads this first every session. It says who I am and what I'm working on now.

I'm an email marketer. I run newsletters and lifecycle campaigns and want my AI to remember
my projects, my tone of voice, what I've tried, and what worked — so I stop re-explaining.

I work only in web-chat ChatGPT. My AI cannot run on a schedule or touch files on my computer,
so the routines here are **manual**: I paste the startup block at the start of a session and the
closure block at the end.

- Active projects: see `projects/`.
- People: see `people/`.
- How to use this: `README.md`.
""")
    w(os.path.join(v, "profile.md"), """
# Profile

- Role: email marketer (newsletters, lifecycle, win-back).
- Tone of voice: warm, concrete, no hype; short subject lines; one idea per email.
- How I work with AI: web-chat only, manual copy-paste, no local files or scheduling.
- What I want remembered: campaigns, hypotheses, results, reusable ideas, tone, lessons.
""")
    w(os.path.join(v, "inbox.md"), "# Inbox\n\n> Raw episodes land here from closure, newest first.\n")
    w(os.path.join(v, "decisions.md"), "# Decisions\n\n> Choices worth remembering, with the why.\n")
    w(os.path.join(v, "lessons.md"), "# Lessons\n\n> Things learned the hard way.\n")
    w(os.path.join(v, "README.md"), """
# My memory vault

This folder is my memory. My AI reads `_start-here.md` first, then whatever project I'm working
on. When I finish something, I run closure and it saves what's worth keeping.

Because I work in web-chat only, the routines are manual:
- **Startup:** paste the startup block (in my saved prompts) at the start of a session.
- **Closure:** paste the closure block at the end; copy what it produces back into `inbox.md`.
- **Weekly hygiene:** once a week, ask the AI to scan for stale or duplicate notes.

Nothing here needs an app or an account. It's just Markdown.
""")
    w(os.path.join(v, "projects", "spring-newsletter.md"),
      card("spring-newsletter", "project", "Spring newsletter relaunch"))
    w(os.path.join(v, "projects", "winback-flow.md"),
      card("winback-flow", "project", "Win-back lifecycle flow"))
    w(os.path.join(v, "projects", "subject-line-tests.md"),
      card("subject-line-tests", "project", "Subject-line A/B testing"))
    w(os.path.join(v, "people", "client-bakery.md"),
      card("client-bakery", "person", "Bakery client (newsletter owner)"))
    keep(os.path.join(v, "cards"))
    # _index.md is generated by index_vault.py — leave a minimal valid stub so smoke passes
    # before the indexer runs; running index_vault.py regenerates it properly.
    w(os.path.join(v, "_index.md"),
      "# Index\n\n> Auto-generated by index_vault.py. Do not edit by hand.\n")
    return v


# --------------------------------------------------------------------------------------------
# Scenario 2 — Катя: a messy work folder BEFORE migration (content + SEO lead).
# This is the INPUT to adopt-existing-folder. Mixed content, SEO, contractors, briefs,
# reports, tables, archive, junk. No frontmatter — it's raw working material.
#
# KATYA_SRC_FILES is the single source of truth for the original content, so the migrated
# fixture can both back it up byte-for-byte and lay copies into the new structure.
# --------------------------------------------------------------------------------------------
KATYA_SRC_FILES = {
    os.path.join("blog redesign", "brief.md"): "# Blog redesign brief\n\nGoals, scope, deadline.\n",
    os.path.join("blog redesign", "draft-second-version.docx.md"): "Draft copy for the new blog hub page.\n",
    os.path.join("blog redesign", "wireframe notes.txt"): "Hero, category grid, author bios.\n",
    os.path.join("seo audit Q2", "audit.md"): "# Q2 SEO audit\n\nCrawl issues, thin pages, internal links.\n",
    os.path.join("seo audit Q2", "keywords.csv"): "keyword,volume,difficulty\nbest crm,4400,42\n",
    os.path.join("seo audit Q2", "report.md"): "# Q2 report\n\nTraffic up 12%, fixed 30 thin pages.\n",
    os.path.join("contractors", "anna writer.md"): "Anna — freelance writer, blog + landing copy.\n",
    os.path.join("contractors", "max seo.md"): "Max — SEO contractor, technical audits.\n",
    os.path.join("content calendar", "2026 plan.csv"): "month,topic,owner\nJan,CRM guide,Anna\n",
    os.path.join("old campaigns", "2024 black friday.md"): "Finished. Kept for reference.\n",
    os.path.join("old campaigns", "2023 webinar.md"): "Finished. Old.\n",
    "Untitled.md": "asdf scratch note\n",                 # junk
    "copy of copy of brief.md": "duplicate of blog brief\n",  # duplicate
    "notes.md": "random misc notes\n",
    "decisions log.md": "We chose Ghost over WordPress in March.\n",
    "readme.txt": "My work folder. Years of stuff.\n",
}


def build_katya_src(base):
    s = os.path.join(base, "katya-src")
    for rel, content in KATYA_SRC_FILES.items():
        w(os.path.join(s, rel), content)
    return s


# --------------------------------------------------------------------------------------------
# Scenario 2 EXPECTED OUTPUT — Катя AFTER a simulated approval + backup + copy + report.
# This is what references/adopt-existing-folder.md produces once the human approves the plan.
# Generated here without the interactive gate so the post-migration result is reproducible and
# can be verified with index_vault.py + smoke_test.py (must PASS).
#
# What the adopt flow does, modelled faithfully:
#   - full timestamped backup of the ORIGINAL folder in _mnemaos_backup/original-.../ (verbatim)
#   - the MnemaOS vault skeleton (the 7 required files + card dirs)
#   - cards (project / person / decision) DIRECTLY in projects/ people/ cards/ — frontmatter,
#     kebab-case ids — that summarise the clusters found in the source
#   - the user's raw material COPIED into working-file locations nested under each project's
#     files/ (no frontmatter required there) and an archive/ for finished campaigns
#   - junk/duplicates FLAGGED in the migration report, not deleted
#   - migration-report.md (human) + migration-map.csv (machine)
# --------------------------------------------------------------------------------------------
def build_katya_migrated(base):
    m = os.path.join(base, "katya-migrated")

    # 1) Full backup of the original folder, byte-for-byte, under a timestamped dir.
    backup = os.path.join(m, "_mnemaos_backup", "original-20260627-120000")
    for rel, content in KATYA_SRC_FILES.items():
        w(os.path.join(backup, rel), content)

    # 2) Vault skeleton — the 7 required files.
    w(os.path.join(m, "_start-here.md"), """
# Start here

> The agent reads this first every session: who I am, active projects, key people, where to write.

I lead a content team and an SEO project. My AI should remember my projects, the people I work
with, the decisions we've made, and the lessons from past campaigns.

This vault was built by adopting my existing work folder. The original is backed up verbatim in
`_mnemaos_backup/original-20260627-120000/`. Nothing was deleted; my files were copied into this
structure. See `migration-report.md` for what moved where and what was flagged as junk.

- Projects: `projects/`   - People: `people/`   - Decisions: `decisions.md` and `cards/`
- What changed: `migration-report.md`
""")
    w(os.path.join(m, "profile.md"), """
# Profile

- Role: content team lead + SEO project owner.
- How I work with AI: desktop coding agent (can run scripts and touch files).
- What I want remembered: projects, contractors, decisions, campaign lessons.
- Source: this vault was adopted from an existing work folder (see migration-report.md).
""")
    w(os.path.join(m, "inbox.md"), "# Inbox\n\n> Fresh episodes from closure, newest first.\n")
    w(os.path.join(m, "decisions.md"), """
# Decisions

> Important choices, dated, with the why. Migrated from `decisions log.md`.

- 2026-03 — Chose Ghost over WordPress for the blog platform. See `cards/blog-platform-choice.md`.
""")
    w(os.path.join(m, "lessons.md"), "# Lessons\n\n> Rules learned the hard way. Filled as campaigns close.\n")
    w(os.path.join(m, "README.md"), """
# My memory vault (adopted from an existing folder)

This memory was built by adopting my existing work folder with MnemaOS. The original is backed up
in `_mnemaos_backup/` and nothing was deleted. My raw files were copied into `projects/*/files/`
and `archive/`; the cards in `projects/`, `people/`, and `cards/` summarise them for the AI.

How I work now: startup reads `_start-here.md`; closure saves what's worth keeping; weekly hygiene
refreshes the index and flags rot. See `migration-report.md` for the full before/after map.
""")

    # 3) Cards (directly in card dirs — frontmatter, kebab-case ids).
    w(os.path.join(m, "projects", "blog-redesign.md"),
      card("blog-redesign", "project", "Blog redesign",
           extra="aliases: [blog hub]\n")
      + "Redesign of the blog hub. Brief, draft copy, and wireframe notes are in `files/`.\n"
        "People: [[anna-writer]]. Decision: [[blog-platform-choice]].\n")
    w(os.path.join(m, "projects", "seo-audit-q2.md"),
      card("seo-audit-q2", "project", "Q2 SEO audit")
      + "Quarterly SEO audit. Audit, keyword data, and report are in `files/`.\n"
        "People: [[max-seo]].\n")
    w(os.path.join(m, "projects", "content-calendar.md"),
      card("content-calendar", "project", "Content calendar")
      + "Editorial calendar. Plan is in `files/`.\n")
    w(os.path.join(m, "people", "anna-writer.md"),
      card("anna-writer", "person", "Anna (freelance writer)")
      + "Freelance writer — blog and landing copy. Works on [[blog-redesign]].\n")
    w(os.path.join(m, "people", "max-seo.md"),
      card("max-seo", "person", "Max (SEO contractor)")
      + "SEO contractor — technical audits. Works on [[seo-audit-q2]].\n")
    w(os.path.join(m, "cards", "blog-platform-choice.md"),
      card("blog-platform-choice", "decision", "Blog platform: Ghost over WordPress")
      + "March decision to use Ghost instead of WordPress for the blog. Logged in `decisions.md`.\n")

    # 4) The user's raw material COPIED into working-file locations (nested = no frontmatter).
    #    Project working files under projects/<slug>/files/ ; finished campaigns under archive/.
    w(os.path.join(m, "projects", "blog-redesign", "files", "brief.md"),
      KATYA_SRC_FILES[os.path.join("blog redesign", "brief.md")])
    w(os.path.join(m, "projects", "blog-redesign", "files", "draft-second-version.docx.md"),
      KATYA_SRC_FILES[os.path.join("blog redesign", "draft-second-version.docx.md")])
    w(os.path.join(m, "projects", "blog-redesign", "files", "wireframe-notes.txt"),
      KATYA_SRC_FILES[os.path.join("blog redesign", "wireframe notes.txt")])
    w(os.path.join(m, "projects", "seo-audit-q2", "files", "audit.md"),
      KATYA_SRC_FILES[os.path.join("seo audit Q2", "audit.md")])
    w(os.path.join(m, "projects", "seo-audit-q2", "files", "keywords.csv"),
      KATYA_SRC_FILES[os.path.join("seo audit Q2", "keywords.csv")])
    w(os.path.join(m, "projects", "seo-audit-q2", "files", "report.md"),
      KATYA_SRC_FILES[os.path.join("seo audit Q2", "report.md")])
    w(os.path.join(m, "projects", "content-calendar", "files", "2026-plan.csv"),
      KATYA_SRC_FILES[os.path.join("content calendar", "2026 plan.csv")])
    w(os.path.join(m, "archive", "2024-black-friday.md"),
      KATYA_SRC_FILES[os.path.join("old campaigns", "2024 black friday.md")])
    w(os.path.join(m, "archive", "2023-webinar.md"),
      KATYA_SRC_FILES[os.path.join("old campaigns", "2023 webinar.md")])
    w(os.path.join(m, "archive", "misc-notes.md"),
      KATYA_SRC_FILES["notes.md"])

    # 5) Migration report (human) + map (machine). Junk/duplicates are FLAGGED, not deleted.
    w(os.path.join(m, "migration-report.md"), """
# Migration report

Source: an existing work folder (content + SEO lead). Adopted into this MnemaOS vault on
2026-06-27 after the plan was approved. The original is backed up verbatim in
`_mnemaos_backup/original-20260627-120000/`. Files were **copied**, never deleted.

## What moved where

- `blog redesign/` → project `projects/blog-redesign.md` + raw files in
  `projects/blog-redesign/files/`.
- `seo audit Q2/` → project `projects/seo-audit-q2.md` + raw files in `projects/seo-audit-q2/files/`.
- `content calendar/` → project `projects/content-calendar.md` + plan in `files/`.
- `contractors/anna writer.md`, `contractors/max seo.md` → people cards `people/anna-writer.md`,
  `people/max-seo.md`.
- `decisions log.md` → `decisions.md` + decision card `cards/blog-platform-choice.md`.
- `old campaigns/`, `notes.md` → `archive/` (finished / low-signal, kept for reference).

## Flagged for your review (NOT deleted)

- `Untitled.md` — scratch/junk. Left in the backup only; not copied into the structure.
- `copy of copy of brief.md` — duplicate of the blog brief. Left in the backup only.
- `readme.txt` — folder readme; superseded by this vault's `README.md`. Left in the backup only.

You decide whether to delete the flagged items from the backup. MnemaOS did not.
""")
    w(os.path.join(m, "migration-map.csv"), """
source,destination,action
blog redesign/brief.md,projects/blog-redesign/files/brief.md,copy
blog redesign/draft-second-version.docx.md,projects/blog-redesign/files/draft-second-version.docx.md,copy
blog redesign/wireframe notes.txt,projects/blog-redesign/files/wireframe-notes.txt,copy
seo audit Q2/audit.md,projects/seo-audit-q2/files/audit.md,copy
seo audit Q2/keywords.csv,projects/seo-audit-q2/files/keywords.csv,copy
seo audit Q2/report.md,projects/seo-audit-q2/files/report.md,copy
content calendar/2026 plan.csv,projects/content-calendar/files/2026-plan.csv,copy
contractors/anna writer.md,people/anna-writer.md,card
contractors/max seo.md,people/max-seo.md,card
decisions log.md,decisions.md + cards/blog-platform-choice.md,card
old campaigns/2024 black friday.md,archive/2024-black-friday.md,copy
old campaigns/2023 webinar.md,archive/2023-webinar.md,copy
notes.md,archive/misc-notes.md,copy
Untitled.md,(backup only),flag-junk
copy of copy of brief.md,(backup only),flag-duplicate
readme.txt,(backup only),flag-superseded
""".lstrip("\n"))

    # _index.md stub — regenerated by index_vault.py.
    w(os.path.join(m, "_index.md"),
      "# Index\n\n> Auto-generated by index_vault.py. Do not edit by hand.\n")
    return m


# --------------------------------------------------------------------------------------------
# Scenario 3 — advanced user: an existing Obsidian vault with MnemaOS overlaid non-destructively.
# The user's own notes/ daily/ refs/ are untouched; MnemaOS adds its entry point, an index,
# and a bridge card that LINKS INTO an existing note rather than duplicating it.
# --------------------------------------------------------------------------------------------
def build_advanced(base):
    a = os.path.join(base, "advanced")
    # --- the user's existing Obsidian vault (pre-existing, MnemaOS must not touch) ---
    w(os.path.join(a, "notes", "deep-work.md"), """
---
tags: [productivity]
---

# Deep work

My own note on focused work blocks. MnemaOS must not edit this.
""")
    w(os.path.join(a, "notes", "second-brain.md"), "# Second brain\n\nMy method. Pre-existing.\n")
    w(os.path.join(a, "daily", "2026-06-20.md"), "Daily log. Pre-existing.\n")
    w(os.path.join(a, "refs", "atomic-habits.md"), "Book notes. Pre-existing.\n")
    os.makedirs(os.path.join(a, ".obsidian"), exist_ok=True)
    w(os.path.join(a, ".obsidian", "app.json"), "{}\n")

    # --- MnemaOS overlay (added non-destructively) ---
    w(os.path.join(a, "_start-here.md"), """
# Start here (MnemaOS overlay)

> Added by MnemaOS over an existing Obsidian vault. It does not replace your system — it adds
> startup/closure protocols, hygiene, an index, and migration safety on top of it.

Your notes in `notes/`, `daily/`, `refs/` are untouched. MnemaOS links into them rather than
duplicating them — see `cards/bridge-deep-work.md`, which points at your own `[[deep-work]]`.

What MnemaOS adds over your current setup: a session startup protocol, a closure protocol that
saves episodes, a weekly hygiene/index pass, and (in adopt mode) safe migration with backup.
""")
    w(os.path.join(a, "profile.md"), """
# Profile

Advanced LLM user. Already keeps an Obsidian vault and a personal graph. Uses desktop coding
agents. Wants startup/closure/hygiene protocols and indexing without rebuilding the vault.
""")
    w(os.path.join(a, "inbox.md"), "# Inbox\n\n> Episodes from closure, newest first.\n")
    w(os.path.join(a, "decisions.md"), "# Decisions\n")
    w(os.path.join(a, "lessons.md"), "# Lessons\n")
    w(os.path.join(a, "README.md"), """
# MnemaOS overlay on an existing vault

MnemaOS was added on top of an existing Obsidian vault. Your notes are unchanged. You can adopt
the protocols you want (startup, closure, hygiene, indexing) and ignore the rest.
""")
    # bridge card linking into the user's own note (Obsidian basename link)
    w(os.path.join(a, "cards", "bridge-deep-work.md"),
      card("bridge-deep-work", "note", "Bridge: deep work",
           extra="") + "Links into my own note: [[deep-work]].\n")
    keep(os.path.join(a, "people"))
    keep(os.path.join(a, "projects"))
    w(os.path.join(a, "_index.md"),
      "# Index\n\n> Auto-generated by index_vault.py. Do not edit by hand.\n")
    return a


def main():
    if len(sys.argv) != 2:
        print("usage: python3 make_test_fixtures.py <output-dir>")
        return 2
    out = os.path.abspath(os.path.expanduser(sys.argv[1]))
    os.makedirs(out, exist_ok=True)
    vika = build_vika(out)
    katya_src = build_katya_src(out)
    katya_mig = build_katya_migrated(out)
    adv = build_advanced(out)
    here = os.path.dirname(__file__) or "."
    print(f"Fixtures written under: {out}")
    print(f"  vika/            (greenfield, web-only)        -> {vika}")
    print(f"  katya-src/       (adopt-existing INPUT)        -> {katya_src}")
    print(f"  katya-migrated/  (adopt-existing EXPECTED OUT) -> {katya_mig}")
    print(f"  advanced/        (Obsidian overlay)            -> {adv}")
    print("\nReproduce (each must index clean + smoke PASS):")
    for name, path in (("vika", vika), ("advanced", adv), ("katya-migrated", katya_mig)):
        print(f"  python3 {here}/index_vault.py {path}")
        print(f"  python3 {here}/smoke_test.py  {path}")
    print("  # katya-src/ is the INPUT to adopt-existing-folder (human approval gate). To migrate")
    print("  # it for real, run that flow per references/adopt-existing-folder.md; katya-migrated/")
    print("  # is the reproducible reference of what that flow produces after approval.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
