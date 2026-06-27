# SETUP — install, activate, uninstall

> This is the package-level setup reference. During onboarding the agent generates a
> setup tailored to your host (with only the steps that apply). This file is the master
> version that explains every step.

## Install the package

1. Copy the `mnemaos/` folder into your agent's skills directory — the place your LLM host
   discovers skills. (CLI coding agents: the agent's skills folder. Desktop AI apps: the
   app's skill/command catalog import.)
2. Confirm the agent can see the `mnemaos` skill (it should appear in its skill list).

## Run onboarding

1. Ask the agent to "set up my memory with MnemaOS" or invoke the `mnemaos` skill.
2. Choose the mode: greenfield (start fresh) or adopt-existing-folder.
3. Answer the 6-dimension interview. The agent writes `mnemaos-config.yaml` and generates
   your vault and the four memory skills.
4. The agent runs the structural smoke test and a tiny live dry-run.

## Verify (anytime)

```bash
# structural check of your vault (stdlib Python, no install needed)
python3 <package>/scripts/smoke_test.py <your-vault-path>

# rebuild the index and report broken links / missing frontmatter
python3 <package>/scripts/index_vault.py <your-vault-path>
```

A passing smoke test means: required files exist, card frontmatter is valid, no leftover
placeholders, no leaked reference names, no inlined secrets in any text/config file (including
the backup folder and `.env`/`.json`/etc.), no broken `[[wikilinks]]` (checked directly — no
need to run the indexer first), and the index is consistent.

To reproduce the three reference scenarios (Вика / Катя / advanced user) for review:

```bash
python3 <package>/scripts/make_test_fixtures.py <output-dir>
python3 <package>/scripts/index_vault.py <output-dir>/vika
python3 <package>/scripts/smoke_test.py  <output-dir>/vika
```

## Activate routines (host-aware)

How routines run depends entirely on your host. The agent picks the mechanism that fits
during onboarding (Phase 6) and writes the exact steps here. Classes:

- **Coding-agent CLI on your machine:** a host routine or a system cron entry invoking the
  agent weekly with the hygiene skill; closure on a trigger phrase.
- **Desktop AI app with a scheduler:** the app's built-in planner runs hygiene weekly.
- **Web chat / no file access / no scheduler:** routines are **manual trigger phrases** —
  say "run hygiene" weekly, "close this out" after a task. This is a fully valid mode.

The agent confirms the scheduler can actually reach your vault files before promising an
unattended routine. If it cannot, it falls back to manual triggers and tells you.

## Uninstall

- Remove the `mnemaos/` skill folder from your agent's skills directory.
- Your vault is just a folder of Markdown — keep it, move it, or delete it as you wish. The
  package and the vault are independent; removing the package does not touch your memory.
- If you used adopt-existing-folder and want to revert, your original folder is in
  `<vault>/_mnemaos_backup/original-YYYYMMDD-HHMMSS/`.
