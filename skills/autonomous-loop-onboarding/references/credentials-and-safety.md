# Credentials & Safety

Apply this in Phase 4, before handing the generated loop to the user. Two concerns:
keeping secrets out of files, and keeping the agent inside safe limits.

## Credentials — never inline a secret

The loop may need credentials (an API token for the task system, a key for the LLM host).
Handle them so a secret value never lands in a file the user might share.

**Rules:**

1. A generated file (config, prompt, README) references a credential **by name only**, never
   by value. Example in `loop-config.yaml`:
   ```yaml
   task_system:
     auth_env_var: TASK_API_TOKEN   # the NAME of an env var, not the token itself
   ```
2. The actual value lives in the user's environment or a secret store — an environment
   variable, the OS keychain, the host's own secret manager, or a `.env` file that is **git-
   ignored**. Tell the user which mechanism their host uses; if unsure, default to an
   environment variable.
3. If the loop folder is in a git repo, ensure `.env` and any secret file are in
   `.gitignore`. The generated `SETUP.md` includes this step.
4. Never echo a secret into a prompt, a comment, a log, or the result. If a worker needs to
   prove it authenticated, it reports "authenticated as <account name>", not the token.
5. If the user pastes a secret into the chat during onboarding, do not write it into any
   file — tell them where to put it (env var / secret store) and reference it by name.

**Quick check (also enforced by the smoke test):** no generated file should contain a string
that looks like a live key (long random tokens, `sk-...`, `Bearer <token>`, etc.). The smoke
test flags common patterns; treat any hit as a bug to fix before shipping.

## Safety limits — keep the agent inside the lines

The loop core defines conservative defaults (no publishing, no outbound messages as the user,
no payments, no deleting significant data, no protected-branch pushes, no permission changes,
no significant external action, no editing canonical config/production assets). Carry these
into the generated `worker-prompt.md` as explicit "stop and block" rules.

**How to apply:**

1. Start from the default limit set. In the interview, the user may **explicitly loosen** one
   (e.g. "yes, the agent may post to my private test channel"). Only a limit the user named
   may be relaxed; everything else stays a hard stop.
2. Add any user-specific caps from the interview: spend limit, time-per-task limit, "never
   touch folder X".
3. The worker prompt must instruct: when an action would cross a limit, produce a ready-to-use
   **draft** of that action, or set the task `BLOCKED` with the specific reason — never perform
   it silently.
4. Least privilege for connectors: request the narrowest scope that makes the loop work (e.g.
   read-write on one project, not the whole account). Note the scope in `SETUP.md` so the user
   grants only what is needed.

## Why these matter

A loop that runs unattended is exactly where a leaked key or an unbounded action does the most
damage, because no human is watching in real time. The cost of these guards is tiny; the cost
of skipping them is a public post, a charged card, or a key in someone's shared repo. Build the
guards in from the start.
