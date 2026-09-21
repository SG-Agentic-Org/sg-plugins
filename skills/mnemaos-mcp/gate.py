#!/usr/bin/env python3
"""mnemaos-mcp gate — validation library for memory_write.

Standard library only. Every write into the vault passes through validate_write()
before anything touches disk. A rejection names the exact check that failed.
"""
import re
import unicodedata

CARD_TYPES = ("person", "project", "concept", "decision", "note")
MAX_TITLE = 200
MAX_BODY = 20000  # characters; a card is distilled state, not an archive

# Secret patterns (mirrors the structural smoke test of the base package):
# bare provider tokens, key=value assignments incl. quoted-JSON keys, cloud key ids,
# private key blocks.
SECRET_PATTERNS = [
    re.compile(r"\bsk-[A-Za-z0-9_-]{16,}"),
    re.compile(r"\bghp_[A-Za-z0-9]{20,}"),
    re.compile(r"\bxox[baprs]-[A-Za-z0-9-]{10,}"),
    re.compile(r"\bAKIA[0-9A-Z]{16}\b"),
    re.compile(r"-----BEGIN [A-Z ]*PRIVATE KEY-----"),
    re.compile(
        r"""["']?(api[_-]?key|secret|token|password|passwd|access[_-]?key)["']?\s*[:=]\s*["']?[A-Za-z0-9_\-./+]{12,}""",
        re.IGNORECASE,
    ),
]

_CYRILLIC_TRANSLIT = {
    "а": "a", "б": "b", "в": "v", "г": "g", "д": "d", "е": "e", "ё": "e",
    "ж": "zh", "з": "z", "и": "i", "й": "y", "к": "k", "л": "l", "м": "m",
    "н": "n", "о": "o", "п": "p", "р": "r", "с": "s", "т": "t", "у": "u",
    "ф": "f", "х": "h", "ц": "ts", "ч": "ch", "ш": "sh", "щ": "sch",
    "ъ": "", "ы": "y", "ь": "", "э": "e", "ю": "yu", "я": "ya",
}


def slugify(title):
    """Lowercase-kebab slug; Cyrillic transliterated so slugs stay ASCII."""
    s = title.strip().lower()
    s = "".join(_CYRILLIC_TRANSLIT.get(ch, ch) for ch in s)
    s = unicodedata.normalize("NFKD", s)
    s = "".join(ch for ch in s if not unicodedata.combining(ch))
    s = re.sub(r"[^a-z0-9]+", "-", s).strip("-")
    s = re.sub(r"-{2,}", "-", s)
    return s


def scan_secrets(text):
    """Return list of matched secret descriptions (empty = clean)."""
    findings = []
    for pat in SECRET_PATTERNS:
        m = pat.search(text)
        if m:
            token = m.group(0)
            findings.append(token[:12] + "…" if len(token) > 12 else token)
    return findings


def validate_write(payload):
    """Validate a memory_write payload. Returns (errors, normalized).

    errors: list of human-readable strings; empty list means the write may proceed.
    normalized: dict with slug etc. filled in (only meaningful when errors is empty).
    """
    errors = []
    if not isinstance(payload, dict):
        return (["payload must be a JSON object"], {})

    kind = payload.get("kind", "card")
    if kind not in ("card", "episode"):
        errors.append("kind must be 'card' or 'episode', got %r" % (kind,))

    body = payload.get("body", "")
    if not isinstance(body, str) or not body.strip():
        errors.append("body is required and must be non-empty text")
    elif len(body) > MAX_BODY:
        errors.append("body exceeds the %d-character budget (%d); distill it — a card is state, not an archive" % (MAX_BODY, len(body)))

    title = payload.get("title", "")
    norm = {"kind": kind, "body": body.strip() if isinstance(body, str) else ""}

    if kind == "card":
        if not isinstance(title, str) or not title.strip():
            errors.append("title is required for a card")
        elif len(title) > MAX_TITLE:
            errors.append("title exceeds %d characters" % MAX_TITLE)
        ctype = payload.get("type", "note")
        if ctype not in CARD_TYPES:
            errors.append("type must be one of %s, got %r" % ("|".join(CARD_TYPES), ctype))
        slug = slugify(title) if isinstance(title, str) else ""
        if title and not slug:
            errors.append("title %r does not resolve to a usable slug" % (title,))
        norm.update({
            "type": ctype,
            "title": title.strip() if isinstance(title, str) else "",
            "slug": slug,
            "tags": [t for t in payload.get("tags", []) if isinstance(t, str)],
            "links": [l for l in payload.get("links", []) if isinstance(l, str)],
            "private": bool(payload.get("private", False)),
            "update": bool(payload.get("update", False)),
        })

    secret_text = "%s\n%s" % (title if isinstance(title, str) else "", body if isinstance(body, str) else "")
    secrets = scan_secrets(secret_text)
    if secrets:
        errors.append(
            "inlined secret detected (%s) — memory stores references to credentials by name, never values"
            % ", ".join(secrets)
        )

    return (errors, norm)
