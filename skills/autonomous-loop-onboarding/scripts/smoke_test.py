#!/usr/bin/env python3
"""
smoke_test.py — structural check for a generated autonomous-loop folder.

Runs in a clean environment with only the Python standard library. No personal
paths, no network, no third-party packages required (PyYAML is used if present,
otherwise a minimal built-in parser handles the simple config).

Usage:
    python3 smoke_test.py <path-to-generated-loop-folder>

It checks:
  1. loop-config.yaml exists and parses.
  2. Required prompt files exist (worker-prompt.md always; closure/orchestrator
     only when the config asks for them).
  3. README.md and SETUP.md exist.
  4. No unresolved {{placeholder}} tokens remain in any generated file.
  5. No inlined secret VALUES (long tokens, sk-..., Bearer ...) in any file.

Exits 0 if all checks pass, 1 otherwise. Prints a human-readable report.
"""

import os
import re
import sys

REQUIRED_ALWAYS = ["loop-config.yaml", "worker-prompt.md", "README.md", "SETUP.md"]

PLACEHOLDER_RE = re.compile(r"\{\{[^}]+\}\}")

# Patterns that look like a real secret VALUE (not a NAME reference).
SECRET_VALUE_RES = [
    re.compile(r"sk-[A-Za-z0-9]{16,}"),                       # OpenAI-style keys
    re.compile(r"\bBearer\s+[A-Za-z0-9._\-]{16,}"),           # bearer tokens
    re.compile(r"\bghp_[A-Za-z0-9]{16,}"),                    # GitHub PATs
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),            # Slack tokens
    re.compile(r"AKIA[0-9A-Z]{16}"),                          # AWS access key id
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),        # private keys
]

# A bare long random-looking token assigned to something. We try not to flag
# obvious placeholders / env-var names.
ASSIGN_SECRET_RE = re.compile(
    r"(?i)\b(token|secret|api[_-]?key|password|passwd|access[_-]?key)\b\s*[:=]\s*"
    r"['\"]?([A-Za-z0-9._\-]{20,})['\"]?"
)
# Substrings that, when present IN THE VALUE, mark it as an obvious placeholder/example
# rather than a real secret. Kept short and value-appropriate; the all-caps env-var-name
# check below handles "referenced by name" cases.
SAFE_VALUE_HINTS = (
    "your-token", "your_token", "example", "changeme", "placeholder", "xxxx",
)


def load_yaml(path):
    """Load YAML with PyYAML if available, else a minimal parser for flat key/values."""
    text = read(path)
    try:
        import yaml  # type: ignore
        return yaml.safe_load(text), None
    except Exception:
        pass
    # Minimal fallback: parse top-level and one-level-nested "key: value" pairs only.
    # List items ("- ...") are skipped — this parser is structure-only and is used just to
    # read the few scalar flags the smoke test checks (loop.closure_enabled,
    # permissions.schedule, llm.unattended). Install PyYAML for full fidelity.
    data = {}
    stack = [(-1, data)]
    for raw in text.splitlines():
        if not raw.strip() or raw.lstrip().startswith("#"):
            continue
        indent = len(raw) - len(raw.lstrip(" "))
        line = raw.strip()
        # strip inline comments (best-effort; ignores '#' inside quotes)
        if "#" in line and not (line.count('"') >= 2 and line.index("#") > line.rfind('"')):
            # only strip if '#' is not within quotes
            in_q = False
            for i, ch in enumerate(line):
                if ch == '"':
                    in_q = not in_q
                elif ch == "#" and not in_q:
                    line = line[:i].strip()
                    break
        if line.startswith("- "):
            # list item — attach to nearest dict under a list key; we keep it simple
            continue
        if ":" not in line:
            continue
        key, _, val = line.partition(":")
        key = key.strip()
        val = val.strip().strip('"').strip("'")
        while stack and indent <= stack[-1][0]:
            stack.pop()
        parent = stack[-1][1] if stack else data
        if val == "":
            child = {}
            parent[key] = child
            stack.append((indent, child))
        else:
            parent[key] = val
    return data, "minimal-parser"


def read(path):
    with open(path, "r", encoding="utf-8") as f:
        return f.read()


def main():
    if len(sys.argv) != 2:
        print("usage: python3 smoke_test.py <path-to-generated-loop-folder>")
        return 2
    folder = os.path.abspath(os.path.expanduser(sys.argv[1]))
    failures = []
    notes = []

    if not os.path.isdir(folder):
        print(f"FAIL: not a directory: {folder}")
        return 1

    # 1 + 2 + 3: required files
    for name in REQUIRED_ALWAYS:
        if not os.path.isfile(os.path.join(folder, name)):
            failures.append(f"missing required file: {name}")

    # config-driven conditional files
    cfg_path = os.path.join(folder, "loop-config.yaml")
    cfg = {}
    if os.path.isfile(cfg_path):
        cfg, parser = load_yaml(cfg_path)
        if cfg is None:
            failures.append("loop-config.yaml did not parse")
            cfg = {}
        elif parser == "minimal-parser":
            notes.append("PyYAML not installed — used built-in minimal parser")
    else:
        failures.append("missing loop-config.yaml")

    loop = cfg.get("loop", {}) if isinstance(cfg, dict) else {}

    def truthy(v):
        return str(v).strip().lower() in ("true", "yes", "1", "on")

    if truthy(loop.get("closure_enabled", False)):
        if not os.path.isfile(os.path.join(folder, "acceptance-closure-prompt.md")):
            failures.append("closure_enabled is true but acceptance-closure-prompt.md is missing")

    llm = cfg.get("llm", {}) if isinstance(cfg, dict) else {}
    perms = cfg.get("permissions", {}) if isinstance(cfg, dict) else {}
    scheduled = str(perms.get("schedule", "manual")).strip().lower() != "manual"
    if scheduled and truthy(llm.get("unattended", False)):
        if not os.path.isfile(os.path.join(folder, "orchestrator-prompt.md")):
            notes.append("scheduled+unattended but no orchestrator-prompt.md "
                         "(generate it from references/orchestrator-contract.md, "
                         "or ignore if the host runs one task at a time)")

    # 4 + 5: scan every generated file for placeholders and secrets
    for root, _dirs, files in os.walk(folder):
        for fn in files:
            if not fn.endswith((".md", ".yaml", ".yml", ".txt")):
                continue
            fpath = os.path.join(root, fn)
            try:
                content = read(fpath)
            except Exception as e:
                failures.append(f"cannot read {fn}: {e}")
                continue
            rel = os.path.relpath(fpath, folder)

            # The example config legitimately documents placeholders; skip it.
            is_example = fn.endswith(".example.yaml") or "example" in rel.split(os.sep)

            for m in PLACEHOLDER_RE.finditer(content):
                if is_example:
                    continue
                failures.append(f"unresolved placeholder {m.group(0)} in {rel}")

            for rx in SECRET_VALUE_RES:
                m = rx.search(content)
                if m:
                    failures.append(f"possible inlined secret value in {rel}: {m.group(0)[:12]}...")

            for m in ASSIGN_SECRET_RE.finditer(content):
                val = m.group(2)
                low = val.lower()
                # Hints must appear in the VALUE itself (a placeholder/example value),
                # not merely somewhere on the line — otherwise a real token on a line
                # that happens to contain "example" would be skipped.
                if any(h in low for h in SAFE_VALUE_HINTS):
                    continue
                # an all-caps env-var-looking name is a reference, not a value
                if re.fullmatch(r"[A-Z][A-Z0-9_]+", val):
                    continue
                failures.append(f"looks like an inlined secret in {rel}: {m.group(1)}=...")

    # report
    print(f"Smoke test: {folder}")
    for n in notes:
        print(f"  note: {n}")
    if failures:
        print(f"\nRESULT: FAIL ({len(failures)} issue(s))")
        for f in failures:
            print(f"  - {f}")
        return 1
    print("\nRESULT: PASS — structure, placeholders, and secret checks all clear.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
