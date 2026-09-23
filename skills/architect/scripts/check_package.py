#!/usr/bin/env python3
"""check_package.py — machine check of the built package.

Usage:  python3 scripts/check_package.py <package folder>

Checks what a rule in prose does not hold by itself: file lengths against the
limits of the build spec, the leading words and their forbidden synonyms, words
the package must not contain, every reference and adapter present in the routes
table of SKILL.md, and a reading condition at the top of every reference.

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

LIMITS = [("SKILL.md", 250), ("references", 200), ("adapters", 120),
          ("README.md", 120), ("README.ru.md", 120)]

# Leading words of the package: each must be present somewhere.
LEADING_WORDS = [
    "stage", "New", "Check", "Revise", "review loop", "step", "brief", "solution",
    "spec", "plan", "check", "run", "finding", "gap", "blank", "watchdog",
    "observation", "stop", "checkpoint", "short path", "deep path", "depth",
    "even simpler", "control set", "expected result", "expected-result list",
    "round", "workspace", "test target", "live target", "kill switch",
    "action cap", "Composer", "Builder", "Tester", "Critic", "Architect",
    "state file", "00-state.md", "resume prompt", "ready to use", "ready to install",
]

# Synonyms of the leading words that the package must not use instead.
FORBIDDEN_SYNONYMS = [
    (r"\bbasket\b", "control set"),
    (r"\bgolden (set|answer|result|output)\b", "expected result"),
    (r"\bground truth\b", "expected result"),
    (r"\bsandbox (target|chat|bot|sheet)\b", "test target"),
    (r"\bstaging (target|environment)\b", "test target"),
    (r"\bdummy target\b", "test target"),
    (r"\bproduction target\b", "live target"),
    (r"\bphases?\b", "stage"),
    (r"\bmilestones?\b", "step"),
    (r"\bpanic button\b", "kill switch"),
    (r"\bemergency stop\b", "kill switch"),
    (r"\bthrottle\b", "action cap"),
    (r"\bgate\b", "checkpoint"),
    (r"\bbug report\b", "finding"),
    (r"\bhandoff prompt\b", "resume prompt"),
    (r"\bQA agent\b", "Tester"),
    (r"\breviewer agent\b", "Critic"),
    (r"\bworker agent\b", "Builder"),
]

# Words the package must not carry at all.
FORBIDDEN_WORDS = [
    (r"(?i)\brun (the )?tests\b", "the model runs tests by itself"),
    (r"(?i)\bthink step by step\b", "the model thinks by itself"),
    (r"(?i)\bdouble[- ]check\b", "the model checks by itself"),
    (r"(?i)\btake a deep breath\b", "the model does not need it"),
]

# The author, his companies and channels: allowed only in the two README author
# lines and in LICENSE.
AUTHOR_MARKERS = re.compile(
    r"(?i)(glibichuk|глибичук|glibiciuc|@glibichuk_pro|\bsasha\b|\bсаша\b|ugulava|"
    r"угулава|\btimur\b|\bтимур\b|intourist|интурист|cowork)")
AUTHOR_ALLOWED_FILES = {"README.md", "README.ru.md", "LICENSE"}

# Money and time: no estimates anywhere in the instructions.
MONEY_TIME = [
    (r"(?i)\bbudget\b", "money"),
    (r"(?i)\bpricing\b", "money"),
    (r"(?i)\binvoice\b", "money"),
    (r"(?i)\bcosts?\s+(about\s+|around\s+)?[$\u20ac\u20bd\d]", "money"),
    (r"(?i)\bthe costs?\b", "money"),
    (r"(?i)\bcosts? (money|a lot|extra)\b", "money"),
    (r"(?i)\bman[- ]hours?\b", "time"),
    (r"(?i)\bhours of work\b", "time"),
    (r"(?i)\bdeadline\b", "time"),
    (r"(?i)\bETA\b", "time"),
    (r"(?i)how long (it|this|the build) (will take|takes)", "time"),
    (r"[$€₽]\s?\d", "money"),
]
MONEY_TIME_SCOPE = ("SKILL.md", "references", "adapters", "evals")


def finding(what, where, fix, proof, severity):
    FINDINGS.append(
        "finding: what={what} | on input={where} | fix={fix} | "
        "fixed when={proof} | severity={sev}".format(
            what=what, where=where, fix=fix, proof=proof, sev=severity))


def read(path):
    try:
        with open(path, encoding="utf-8", errors="replace") as handle:
            return handle.read()
    except OSError:
        return None


def collect(root):
    files = []
    for base, dirs, names in os.walk(root):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__", "scripts")]
        for name in sorted(names):
            if name.endswith((".md", ".txt")) or name == "LICENSE":
                path = os.path.join(base, name)
                files.append((os.path.relpath(path, root), path))
    return sorted(files)


def limit_for(rel):
    for key, limit in LIMITS:
        if rel == key or rel.startswith(key + os.sep):
            return limit
    return None


def prose_lines(text):
    """Numbered lines outside fenced code blocks: a form is not a rule."""
    out, fenced = [], False
    for number, line in enumerate(text.splitlines(), 1):
        if line.lstrip().startswith("```"):
            fenced = not fenced
            continue
        if not fenced:
            out.append((number, line))
    return out


def check_lengths(root, files):
    for rel, path in files:
        limit = limit_for(rel)
        if limit is None:
            continue
        lines = len((read(path) or "").splitlines())
        if lines > limit:
            finding("file longer than its limit ({n} lines, limit {l})".format(n=lines, l=limit),
                    rel,
                    "cut it to the limit from the build spec, or move a topic to its own file",
                    "check_package.py counts no more than the limit",
                    "hinders")


def check_words(root, files):
    whole = {}
    for rel, path in files:
        whole[rel] = read(path) or ""
    joined = "\n".join(whole.values())

    for word in LEADING_WORDS:
        pattern = re.escape(word)
        if not re.search(pattern if word[0].isupper() else "(?i)" + pattern, joined):
            finding("leading word of the package never appears: " + word,
                    "package",
                    "use this word where the build spec's table says it belongs",
                    "check_package.py finds it in the package",
                    "hinders")

    for rel, text in whole.items():
        for number, line in prose_lines(text):
            for pattern, instead in FORBIDDEN_SYNONYMS:
                if re.search("(?i)" + pattern, line):
                    finding("a synonym is used instead of the leading word '" + instead + "'",
                            rel + ":" + str(number),
                            "write '" + instead + "', the word the whole package uses",
                            "check_package.py finds no synonym on this line",
                            "hinders")
            for pattern, why in FORBIDDEN_WORDS:
                if re.search(pattern, line):
                    finding("a forbidden instruction to the model: " + why,
                            rel + ":" + str(number),
                            "delete the line, it tells the model what it already does",
                            "check_package.py finds no such wording",
                            "breaks")
            if rel not in AUTHOR_ALLOWED_FILES:
                match = AUTHOR_MARKERS.search(line)
                if match:
                    finding("the author, his company or his channel is named outside the "
                            "two allowed places: " + match.group(0),
                            rel + ":" + str(number),
                            "remove it — the package is neutral except LICENSE and one "
                            "author line in each README",
                            "check_package.py finds no such name here",
                            "breaks")
            if rel.startswith(MONEY_TIME_SCOPE):
                for pattern, kind in MONEY_TIME:
                    if re.search(pattern, line):
                        finding("a word about " + kind + " where the package gives no estimates",
                                rel + ":" + str(number),
                                "rewrite without the estimate, or say why this is not one",
                                "check_package.py finds no such word here",
                                "cosmetic")

    for rel in AUTHOR_ALLOWED_FILES:
        text = whole.get(rel)
        if text is None:
            continue
        hits = [n for n, line in enumerate(text.splitlines(), 1) if AUTHOR_MARKERS.search(line)]
        allowed = 4 if rel == "LICENSE" else 2
        if len(hits) > allowed:
            finding("more author lines than the exception allows ({n} lines)".format(n=len(hits)),
                    rel + ":" + ",".join(str(h) for h in hits),
                    "keep one author line and one attribution line, nothing more",
                    "check_package.py counts no more than the exception",
                    "hinders")


def check_routes(root, files):
    skill = read(os.path.join(root, "SKILL.md"))
    if skill is None:
        finding("SKILL.md is missing", "SKILL.md",
                "the package has no entry point without it",
                "check_package.py reads SKILL.md",
                "breaks")
        return
    mentioned = set(re.findall(r"(?:references|adapters)/[\w.-]+\.md", skill))
    for rel, _path in files:
        rel_posix = rel.replace(os.sep, "/")
        if rel_posix.startswith(("references/", "adapters/")) and rel_posix not in mentioned:
            finding("the file is not in the routes table of SKILL.md: " + rel_posix,
                    "SKILL.md",
                    "add a row with the condition for opening it, or delete the file",
                    "check_package.py finds the file named in SKILL.md",
                    "breaks")
    for name in sorted(mentioned):
        if not os.path.isfile(os.path.join(root, name)):
            finding("SKILL.md routes to a file that does not exist: " + name,
                    "SKILL.md",
                    "create the file or remove the row",
                    "the file exists",
                    "breaks")


def check_reading_conditions(root, files):
    for rel, path in files:
        rel_posix = rel.replace(os.sep, "/")
        if not rel_posix.startswith(("references/", "adapters/")):
            continue
        lines = [line.strip() for line in (read(path) or "").splitlines()]
        first = ""
        for line in lines:
            if not line or line.startswith("#"):
                continue
            first = line
            break
        if not re.match(r"(?i)^open this\b", first):
            finding("the file does not start with its reading condition",
                    rel_posix + ":1",
                    "make the first line after the title say when this file is opened",
                    "the first line of the body starts with 'Open this'",
                    "hinders")


def main(argv):
    if len(argv) != 2:
        print("usage: python3 scripts/check_package.py <package folder>", file=sys.stderr)
        return 2
    root = os.path.abspath(argv[1])
    if not os.path.isdir(root):
        print("error: not a folder: " + root, file=sys.stderr)
        return 2

    files = collect(root)
    if not files:
        finding("the folder holds no package files", root,
                "point the script at the folder that holds SKILL.md",
                "check_package.py finds SKILL.md and the references",
                "breaks")
    check_lengths(root, files)
    check_words(root, files)
    check_routes(root, files)
    check_reading_conditions(root, files)

    NOT_CHECKED.extend([
        "whether each norm lives in the one file that owns it by the table of the build spec",
        "whether 'stage' and 'step' are each used in their own meaning",
        "whether a rule carries the reason next to it",
        "whether the examples read as a short path and hold no unexplained term",
        "whether the evals tasks each have their own criterion",
        "the frontmatter fields against the current Claude Code documentation",
        "examples/ lengths and money wording: no limit is set for them in the build spec",
    ])

    print("check_package.py — " + root)
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
