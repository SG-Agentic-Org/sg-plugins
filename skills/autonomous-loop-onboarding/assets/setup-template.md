# Setup — install, configure, uninstall

> Generated for the user during onboarding. Keep only the steps that apply to their stack;
> resolve the `{{placeholders}}` and remove this quote block.

## Part A — Install the onboarding skill (one time)

The onboarding skill is what builds your loop. Install it wherever your AI host loads skills
from.

1. Copy the `autonomous-loop-onboarding/` folder into your host's skills directory.
   - Many command-line agents read skills from a `skills/` or `.<host>/skills/` folder.
   - Some hosts let you point at a skill folder directly or install a packaged skill file.
   - If you are unsure where that is for your host, check your host's documentation for
     "skills" or "custom skills"; do not guess a path.
2. Start a new session and confirm the host can see a skill named `autonomous-loop-onboarding`.
3. Ask it to "set up my autonomous task loop". That runs the onboarding interview.

## Part B — Configure your loop

Onboarding writes these into your loop folder (default `my-autonomous-loop/`):

- `loop-config.yaml` — your settings. Edit this to change tools, storage, schedule, or limits.
- `worker-prompt.md` — per-task instructions (regenerated if you change the config materially).
- the optional `acceptance-closure-prompt.md` and `orchestrator-prompt.md`.

### Credentials (only if your task system needs an API token)

Your loop references credentials **by name**, never by value.

1. Put the secret in your environment or secret store — for example, an environment variable:
   ```bash
   export {{auth_env_var}}="your-token-here"
   ```
   …or your OS keychain / your host's secret manager.
2. The name `{{auth_env_var}}` is recorded in `loop-config.yaml`; the value is not.
3. If your loop folder is a git repo, make sure secrets are ignored:
   ```bash
   echo ".env" >> .gitignore
   ```
4. Request least privilege when you authorize the connector: only the project the loop needs.

### Schedule

{{schedule_setup}}
<!-- HOST-AWARE (Phase 6): replace this with the REAL activation steps for the user's
environment, not a generic stub. Identify the host class (CLI agent / desktop app / cloud
agent / self-hosted) and where the scheduler runs, then write the concrete steps for the
mechanism the user chose — e.g.:
  - "Run it manually with <command>." (on-demand)
  - "Add a daily run at 9am in <desktop app>'s scheduler, pointing at orchestrator-prompt.md."
  - "Create a cloud/cron agent that invokes <command> on a schedule."
  - "Add a system cron line: 0 9 * * * <command>."
ALSO include the feasibility note + fallback: if the scheduler runs in a cloud/headless
environment, confirm it can reach the task connector and these prompt files; if not, run the
scheduler locally or move the prompt files where the cloud agent can fetch them. Do not promise
an unattended loop that cannot reach its connectors/files. -->

> Feasibility check before relying on a schedule: confirm the scheduled run can actually reach
> your task system (connector authorized in *that* environment) and these prompt files. A
> cloud/headless run often cannot — if so, use the local-run or fetch-the-files fallback above.

## Part C — Test it

```bash
python3 scripts/smoke_test.py {{loop_folder}}
```

This checks your config parses, the required files exist, no setup placeholders were left
unresolved, and no secret values were inlined. Then queue one tiny throwaway task and run the
worker once to confirm a result lands in {{result_storage}}.

## Part D — Change or update

- To change tools, storage, schedule, or limits: edit `loop-config.yaml`, then re-run
  onboarding (or ask your host to "regenerate my loop prompts from the config") so the prompt
  files match.
- To swap the task system later: pick or build a new adapter (see the skill's
  `references/adapters.md`) and update `task_system` in the config. The core does not change.

## Part E — Uninstall

1. Stop any schedule/trigger you set up in Part B.
2. Delete the loop folder (default `my-autonomous-loop/`). Nothing else depends on it.
3. Revoke the connector token you created, and remove the `{{auth_env_var}}` value from your
   environment / secret store.
4. To remove the onboarding skill too, delete the `autonomous-loop-onboarding/` folder from
   your host's skills directory.

Removing the loop has no side effects beyond stopping the automation — your tasks and results
stay where they are.
