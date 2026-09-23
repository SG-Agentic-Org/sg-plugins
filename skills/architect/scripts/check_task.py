#!/usr/bin/env python3
"""check_task.py — machine check of a task folder before the final report.

Usage:  python3 scripts/check_task.py <task folder>

Checks the part of "Done when" that a script can hold: the folder layout from
references/state.md, step statuses in the state file, a check per acceptance
criterion, the spec header, the watchdog and its observations file, and strings
that look like secret values.

Standard library only, no network. Exit 0 when clean, 1 when there are findings,
2 when the folder cannot be read. Every finding is one line in the form from
references/verify.md. Anything the script cannot judge is listed under
"not checked" and is never reported as passed.
"""

import os
import re
import sys

FINDINGS = []
NOT_CHECKED = []

# Layout from references/state.md, per mode and kind. In Check nothing is built or
# changed, so a spec, a plan, a guide, checks and a watchdog do not exist there by
# design. In a sprint the plan is the result, so a spec, a watchdog and the reports
# folder may have nothing to describe, to watch or to report.
REQUIRED_FILES = {
    "new": ["00-state.md", "01-brief.md", "03-spec.md", "04-plan.md", "07-guide.md"],
    "check": ["00-state.md", "01-brief.md"],
    "revise": ["00-state.md", "01-brief.md", "03-spec.md", "04-plan.md", "07-guide.md"],
    "sprint": ["00-state.md", "01-brief.md", "04-plan.md", "07-guide.md"],
}
REQUIRED_DIRS = {
    "new": ["05-checks", "06-reports", "watchdog"],
    "check": ["06-reports"],
    "revise": ["05-checks", "06-reports", "watchdog"],
    "sprint": ["05-checks"],
}

STATUSES = ("not started", "started", "accepted", "waiting", "stopped")
STEP_RE = re.compile(r"^\s*(\d+)[.)]\s+(.*?)\s{2,}(not started|started|accepted|waiting:.*|stopped:.*)\s*$")
STEP_LOOSE_RE = re.compile(r"^\s*(\d+)[.)]\s+(.+)$")

SECRET_PATTERNS = [
    ("openai-style key", re.compile(r"\bsk-[A-Za-z0-9_-]{16,}")),
    ("github token", re.compile(r"\b(ghp|gho|ghs|github_pat)_[A-Za-z0-9_]{16,}")),
    ("slack token", re.compile(r"\bxox[abprs]-[A-Za-z0-9-]{10,}")),
    ("aws key id", re.compile(r"\bAKIA[0-9A-Z]{12,}")),
    ("google api key", re.compile(r"\bAIza[0-9A-Za-z_-]{30,}")),
    ("telegram bot token", re.compile(r"\b\d{8,10}:[A-Za-z0-9_-]{30,}")),
    ("bearer value", re.compile(r"\bBearer\s+[A-Za-z0-9._-]{16,}")),
    ("assigned secret", re.compile(
        r"(?i)\b(api[_ -]?key|secret|password|passwd|token|pwd)\b\s*[:=]\s*[\"']?[A-Za-z0-9/+_.-]{12,}")),
    ("private key block", re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----")),
]

PLACEHOLDER_RE = re.compile(r"(?i)(<[^>\n]{0,60}>|\{\{|xxx|your[_ -]?(key|token)|paste here|\.\.\.)")

SPEC_HEADER_RE = re.compile(r"(?i)only through the (architect )?skill|только через навык")


def finding(what, where, fix, proof, severity):
    FINDINGS.append(
        "finding: what={what} | on input={where} | fix={fix} | "
        "fixed when={proof} | severity={sev}".format(
            what=what, where=where, fix=fix, proof=proof, sev=severity))


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError as err:
        return None


def mode_key(mode, kind=""):
    """New is the default: an unreadable mode line must not soften the layout check.
    A missing Kind line is read as automation, the stricter of the two."""
    text = (mode or "").lower()
    if "check" in text:
        return "check"
    if "sprint" in (kind or "").lower():
        return "sprint"
    if "revise" in text:
        return "revise"
    return "new"


def check_layout(root, mode, depth, kind=""):
    key = mode_key(mode, kind)
    for name in REQUIRED_FILES[key]:
        if not os.path.isfile(os.path.join(root, name)):
            finding("required file of the task folder is missing: " + name,
                    os.path.join(root, name),
                    "create it as described in references/state.md",
                    "check_task.py finds the file",
                    "breaks")
    for name in REQUIRED_DIRS[key]:
        path = os.path.join(root, name)
        if not os.path.isdir(path):
            finding("required folder of the task folder is missing: " + name + "/",
                    path,
                    "create it as described in references/state.md",
                    "check_task.py finds the folder",
                    "breaks")
        elif name != "watchdog" and not (key == "sprint" and name == "05-checks") \
                and not os.listdir(path):
            finding("folder " + name + "/ is empty", path,
                    "put the files it owns there before the final",
                    "check_task.py finds at least one file in it",
                    "breaks")
    if key == "check":
        NOT_CHECKED.append(
            "mode Check: spec, plan, guide, checks and watchdog are not required and "
            "were not looked for — nothing is built or changed in this mode")
    if key == "sprint":
        NOT_CHECKED.append(
            "kind sprint: a spec, a watchdog, an automation folder and 06-reports/ are "
            "not required "
            "and were not looked for, step statuses are not required either and were "
            "not judged, and 05-checks/ may be empty when no step is an agent's — the "
            "plan is the result; whether a step that does build an automation carries "
            "its own spec, and whether every agent step has its check, is read by a "
            "person")
    if key != "check" and depth == "deep" and not os.path.isfile(os.path.join(root, "02-solution.md")):
        finding("deep path without 02-solution.md",
                os.path.join(root, "02-solution.md"),
                "write the solution, or set the depth to short path with a reason",
                "the file exists or the state file says short path",
                "breaks")
    if key == "revise" and not os.path.isdir(os.path.join(root, "original")):
        finding("mode Revise without original/",
                os.path.join(root, "original"),
                "copy the original before touching it (references/modes.md)",
                "original/ exists and holds the copy",
                "breaks")


def parse_state(root):
    """Returns (mode, kind, depth, steps) and reports what it cannot read."""
    path = os.path.join(root, "00-state.md")
    text = read(path)
    if text is None:
        finding("the state file cannot be read", path,
                "write 00-state.md in the form from references/state.md",
                "check_task.py parses it",
                "breaks")
        return "", "", "", []

    mode = kind = depth = ""
    match = re.search(r"(?im)^\s*Mode:\s*(.+)$", text)
    if match:
        mode = match.group(1).strip().lower()
    else:
        finding("the state file has no Mode line", path,
                "add Mode: New | Check | Revise",
                "check_task.py reads the mode",
                "hinders")
    match = re.search(r"(?im)^\s*Kind:\s*(.+)$", text)
    if match:
        kind = match.group(1).strip().lower()
    match = re.search(r"(?im)^\s*Depth:\s*(.+)$", text)
    if match:
        value = match.group(1).lower()
        if "deep" in value:
            depth = "deep"
        elif "short" in value:
            depth = "short"
        else:
            depth = ""
            finding("the Depth line has neither 'short path' nor 'deep path': "
                    + match.group(1).strip(), path,
                    "write the value in English — short path | deep path — and keep the "
                    "reason after the dash in the person's language (references/state.md)",
                    "check_task.py reads the depth",
                    "hinders")
    else:
        finding("the state file has no Depth line", path,
                "add Depth: short path | deep path with the reason",
                "check_task.py reads the depth",
                "hinders")
    if not re.search(r"(?im)^\s*Workspace:\s*\S", text):
        finding("the state file has no Workspace line", path,
                "add Workspace: program, subscription, where the data lives",
                "check_task.py reads the workspace",
                "hinders")
    if not re.search(r"(?im)^\s*Next action:\s*\S", text):
        finding("the state file has no Next action line", path,
                "add Next action with the one thing that happens next",
                "check_task.py reads the next action",
                "hinders")

    steps = []
    in_steps = False
    for number, line in enumerate(text.splitlines(), 1):
        if re.match(r"(?i)^\s*Steps\b", line):
            in_steps = True
            continue
        if in_steps:
            if re.match(r"(?i)^\s*(Next action|Reading order)", line) or line.startswith("#"):
                in_steps = False
                continue
            if not line.strip():
                continue
            match = STEP_RE.match(line)
            if match:
                steps.append((number, match.group(2).strip(), match.group(3).strip()))
                continue
            loose = STEP_LOOSE_RE.match(line)
            if loose:
                status = next((s for s in STATUSES if s in line.lower()), "")
                steps.append((number, loose.group(2).strip(), status))
    if not steps:
        finding("no plan steps found in the state file", path,
                "list the steps with a status each (references/state.md)",
                "check_task.py reads at least one step",
                "breaks")
    if "sprint" in (kind or "").lower():
        NOT_CHECKED.append(
            "step statuses in the state file: a sprint hands over a plan of future "
            "works, part of them the person's, so they are not accepted at the final "
            "(references/state.md)")
        return mode, kind, depth, steps
    for number, name, status in steps:
        if not status:
            finding("step without a status: " + name, path + ":" + str(number),
                    "write one of not started / started / accepted / waiting / stopped",
                    "check_task.py reads a status for this step",
                    "breaks")
        elif not status.startswith("accepted"):
            finding("step is not accepted (" + status + "): " + name,
                    path + ":" + str(number),
                    "finish and accept the step, or do not write the final yet",
                    "the state file shows accepted for this step",
                    "breaks")
    return mode, kind, depth, steps


def check_spec(root):
    path = os.path.join(root, "03-spec.md")
    text = read(path)
    if text is None:
        return []
    head = "\n".join(text.splitlines()[:6])
    if not SPEC_HEADER_RE.search(head):
        finding("the spec has no header 'only through the Architect skill'", path + ":1",
                "put that line first, so a fresh session does not start the build without the skill",
                "the first lines of 03-spec.md carry the header",
                "breaks")

    criteria = []
    in_acceptance = False
    for number, line in enumerate(text.splitlines(), 1):
        if re.match(r"(?i)^\s*#{0,4}\s*Acceptance\b", line):
            in_acceptance = True
            continue
        if in_acceptance:
            if re.match(r"(?i)^\s*#{1,4}\s+\S", line) or re.match(
                    r"(?i)^\s*(Out of scope|On failure|Two shelves|Accesses|Watchdog)\b", line):
                in_acceptance = False
                continue
            if re.match(r"^\s*([-*+]|\d+[.)])\s+\S", line):
                criteria.append((number, line.strip()))
    if not criteria:
        NOT_CHECKED.append(
            "acceptance criteria of 03-spec.md: no list found under an Acceptance heading, "
            "so the check-per-criterion count was not made")
    return criteria


def check_checks(root, criteria):
    path = os.path.join(root, "05-checks")
    if not os.path.isdir(path):
        return
    files = [name for name in sorted(os.listdir(path)) if not name.startswith(".")]
    if not files:
        return
    body = "\n".join(filter(None, (read(os.path.join(path, name)) for name in files)))
    blocks = len(re.findall(r"(?im)^\s*([-*+]|\d+[.)])\s+\S", body)) or len(files)
    if criteria and blocks < len(criteria):
        finding("fewer checks than acceptance criteria ({b} checks, {c} criteria)".format(
                    b=blocks, c=len(criteria)),
                path,
                "write a check for every criterion before the build (references/spec-for-agents.md)",
                "the count of checks reaches the count of criteria",
                "breaks")
    NOT_CHECKED.append(
        "05-checks/ against 03-spec.md: counted, not matched criterion by criterion — "
        "which check covers which criterion is read by a person")


def check_watchdog(root):
    path = os.path.join(root, "watchdog")
    if not os.path.isdir(path):
        return
    names = []
    for base, _dirs, files in os.walk(path):
        for name in files:
            names.append(os.path.relpath(os.path.join(base, name), path).lower())
    if not names:
        finding("watchdog/ is empty", path,
                "build the watchdog and run it once (references/watchdog.md)",
                "watchdog/ holds the watchdog, its report and its observations file",
                "breaks")
        return
    if not any("observation" in name or "наблюдени" in name for name in names):
        finding("no observations file in watchdog/", path,
                "create the observations file — without it the watchdog is a monitor",
                "watchdog/ holds a file with observations in its name",
                "breaks")
    if not any("report" in name or "отчёт" in name or "отчет" in name for name in names):
        finding("no watchdog report in watchdog/", path,
                "run the watchdog once and keep its report",
                "watchdog/ holds a report file",
                "breaks")


TEXT_SUFFIXES = (".md", ".txt", ".json", ".yml", ".yaml", ".py", ".js", ".ts", ".sh",
                 ".ini", ".cfg", ".toml", ".env", ".sql", ".rb", ".go", ".java")
SKIP_DIRS = {"access", ".git", "__pycache__", "node_modules", ".venv", "venv"}


def check_secrets(root):
    """The whole task folder, access/ excepted: the automation's own source is where
    a key is most likely to end up hard-coded."""
    paths = []
    for current, dirs, files in os.walk(root):
        dirs[:] = [d for d in dirs if d.lower() not in SKIP_DIRS]
        for name in files:
            if name.lower().endswith(TEXT_SUFFIXES):
                paths.append(os.path.join(current, name))
    for path in paths:
        text = read(path)
        if not text:
            continue
        for number, line in enumerate(text.splitlines(), 1):
            for label, pattern in SECRET_PATTERNS:
                match = pattern.search(line)
                if not match:
                    continue
                if PLACEHOLDER_RE.search(match.group(0)):
                    continue
                finding("a string that looks like a secret value (" + label + ")",
                        path + ":" + str(number),
                        "replace the value with a path in access/ (Never shelf in SKILL.md)",
                        "check_task.py finds no secret-like string here",
                        "breaks")
    NOT_CHECKED.append(
        "secrets: only well-known key shapes and assignments are matched, only in text "
        "files, and access/ is skipped on purpose — a value with no recognisable shape, "
        "and anything inside a binary file, is read by a person")


def main(argv):
    if len(argv) != 2:
        print("usage: python3 scripts/check_task.py <task folder>", file=sys.stderr)
        return 2
    root = os.path.abspath(argv[1])
    if not os.path.isdir(root):
        print("error: not a folder: " + root, file=sys.stderr)
        return 2

    mode, kind, depth, _steps = parse_state(root)
    check_layout(root, mode, depth, kind)
    key = mode_key(mode, kind)
    if key == "sprint":
        check_checks(root, check_spec(root))
    elif key != "check":
        criteria = check_spec(root)
        check_checks(root, criteria)
        check_watchdog(root)
    check_secrets(root)

    NOT_CHECKED.extend([
        "the control set against the results the person named: run, not read",
        "whether every scenario was actually run, and whether the run was honest",
        "the guide being in the person's language and understandable to them",
        "nothing in the automation beyond the brief",
    ])

    print("check_task.py — " + root)
    print("findings: " + str(len(FINDINGS)))
    for line in FINDINGS:
        print(line)
    print("")
    print("not checked:")
    for line in NOT_CHECKED:
        print("- " + line)
    return 1 if FINDINGS else 0


if __name__ == "__main__":
    sys.exit(main(sys.argv))
