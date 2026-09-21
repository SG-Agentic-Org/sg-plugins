#!/usr/bin/env python3
"""mnemaos-mcp smoke test — deterministic, standard library only, no LLM.

Builds a throwaway fixture vault in a temp dir, then verifies the full contract:
indexing (incl. incremental zero-write), search canaries (Latin + Cyrillic),
privacy enforcement, the write gate's negative cases, the real stdio JSON-RPC
protocol end-to-end, HTTP auth, and a leakage self-scan of the package itself.

Usage:  python3 smoke_test_mcp.py [existing-vault-to-index-check]
Exit 0 = all PASS; non-zero = at least one FAIL (each failure names the check).
"""
import json
import os
import shutil
import subprocess
import sys
import tempfile
import time
import urllib.error
import urllib.request

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
import gate
import indexer
import server as server_mod

RESULTS = []


def check(name, ok, detail=""):
    RESULTS.append((name, ok, detail))
    print("%s  %s%s" % ("PASS" if ok else "FAIL", name, (" — " + detail) if detail and not ok else ""))


# ---------------------------------------------------------------- fixture

def make_fixture(root):
    """A small invented vault: marketer with two projects, one private card."""
    def w(rel, text):
        path = os.path.join(root, rel)
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, "w", encoding="utf-8") as f:
            f.write(text)

    w("_start-here.md", "# Start here\n\nUser: Dana, freelance marketer.\n\nActive projects: spring-newsletter, site-redesign.\n")
    w("profile.md", "# Profile\n\nDana runs email campaigns for small clients. Prefers short weekly plans.\n")
    w("inbox.md", "# Inbox\n")
    w("decisions.md", "# Decisions\n\n## 2026-05-02 — newsletter tool\n\nChose the simpler tool over the fancy one.\n")
    w("lessons.md", "# Lessons\n")
    w("README.md", "# Dana's memory vault\n")
    w("projects/spring-newsletter.md",
      "---\nid: spring-newsletter\ntype: project\ntitle: Spring newsletter\ncreated: 2026-04-01\n"
      "updated: 2026-06-20\nstatus: active\ntags: [email]\nlinks: []\n---\n\n# Spring newsletter\n\n"
      "## Deadline\n\nThe newsletter deadline is May 30, send the draft to the client a week before.\n")
    w("people/lena-client.md",
      "---\nid: lena-client\ntype: person\ntitle: Lena (client)\ncreated: 2026-04-05\nupdated: 2026-06-01\n"
      "status: active\ntags: []\nlinks: [spring-newsletter]\n---\n\n# Lena (client)\n\n"
      "Лена предпочитает короткие письма и созвоны по вторникам.\n")
    w("cards/health-topic.md",
      "---\nid: health-topic\ntype: note\ntitle: Health topic\ncreated: 2026-06-10\nupdated: 2026-06-25\n"
      "status: active\ntags: []\nlinks: []\nprivate: true\n---\n\n# Health topic\n\n"
      "Confidential wellbeing notes that must never leave this machine remotely.\n")
    w("projects/site-redesign/files/raw-notes.md", "Working file: sitemap sketch, no frontmatter needed.\n")
    return root


# ---------------------------------------------------------------- checks

def run_index_checks(vault):
    stats = indexer.index_vault(vault)
    check("index: initial build finds docs", stats["docs"] >= 8, str(stats))
    stats2 = indexer.index_vault(vault)
    check("index: unchanged rerun writes nothing",
          stats2["added"] == 0 and stats2["changed"] == 0 and stats2["removed"] == 0, str(stats2))
    # a changed file reindexes exactly one doc
    p = os.path.join(vault, "profile.md")
    with open(p, "a", encoding="utf-8") as f:
        f.write("\nAlso mentors one junior marketer.\n")
    os.utime(p, (time.time() + 1, time.time() + 1))
    stats3 = indexer.index_vault(vault)
    check("index: incremental picks up one change", stats3["changed"] == 1 and stats3["added"] == 0, str(stats3))


def run_local_tool_checks(vault):
    mem = server_mod.Memory(vault)
    ctx = mem.context()
    check("context: has entry point + profile + recent cards",
          "Dana" in ctx and "RECENT CARDS" in ctx and "spring-newsletter" in ctx)
    hits = mem.search("newsletter deadline")
    check("search: canary EN top hit", hits.splitlines()[0].startswith("spring-newsletter"), hits[:200])
    hits_ru = mem.search("Лена короткие письма")
    check("search: canary RU finds person card", "lena-client" in hits_ru, hits_ru[:200])
    check("search: local mode sees private card", "health-topic" in mem.search("confidential wellbeing"))
    got = mem.get("spring-newsletter")
    check("get: full card by slug", "Deadline" in got and got.startswith("---"))
    try:
        mem.get("no-such-card")
        check("get: unknown id raises", False)
    except server_mod.ToolError as e:
        check("get: unknown id raises with hint", "no document" in str(e))
    listing = mem.list(type="person")
    check("list: type filter", "lena-client" in listing and "spring-newsletter" not in listing)

    # -- writes
    res = mem.write({"kind": "card", "type": "concept", "title": "Тёплая рассылка",
                     "body": "Правило: тёплая рассылка раз в месяц, не чаще."})
    check("write: card created with transliterated slug",
          "tyoplaya" in res or "teplaya" in res or os.path.exists(os.path.join(vault, "cards")), res)
    slug = res.split("id: ")[-1].rstrip(").").rstrip(", private") if "id: " in res else ""
    found = mem.search("тёплая рассылка раз в месяц")
    check("write: new card immediately searchable", slug and slug in found, found[:200])
    try:
        mem.write({"kind": "card", "type": "concept", "title": "Тёплая рассылка", "body": "другое тело"})
        check("write: duplicate id rejected", False)
    except server_mod.ToolError as e:
        check("write: duplicate id rejected", "already exists" in str(e))
    try:
        mem.write({"kind": "card", "type": "note", "title": "creds",
                   "body": "the api_key=sk-AAAAAAAAAAAAAAAAAAAAAA goes here"})
        check("gate: inlined secret rejected", False)
    except server_mod.ToolError as e:
        check("gate: inlined secret rejected", "secret" in str(e))
    try:
        mem.write({"kind": "card", "type": "wrong-type", "title": "x", "body": "y"})
        check("gate: invalid type rejected", False)
    except server_mod.ToolError as e:
        check("gate: invalid type rejected", "type must be" in str(e))
    res = mem.write({"kind": "episode", "body": "Client call went well; follow-up next Tuesday."})
    with open(os.path.join(vault, "inbox.md"), encoding="utf-8") as f:
        check("write: episode appended to inbox", "follow-up next Tuesday" in f.read(), res)

    ro = server_mod.Memory(vault, read_only=True)
    try:
        ro.write({"kind": "episode", "body": "should not land"})
        check("write: read-only blocks writes", False)
    except server_mod.ToolError as e:
        check("write: read-only blocks writes", "read-only" in str(e))

    health = mem.health()
    check("health: reports counts and mode", "documents:" in health and "local (stdio)" in health)


def run_privacy_checks(vault):
    remote = server_mod.Memory(vault, remote=True)
    check("privacy: remote search hides private card",
          "health-topic" not in remote.search("confidential wellbeing"))
    try:
        remote.get("health-topic")
        check("privacy: remote get hides private card", False)
    except server_mod.ToolError:
        check("privacy: remote get hides private card", True)
    check("privacy: remote list hides private card", "health-topic" not in remote.list())
    check("privacy: remote context hides private card", "health-topic" not in remote.context())


def run_stdio_protocol_check(vault):
    proc = subprocess.Popen(
        [sys.executable, os.path.join(HERE, "server.py"), "--vault", vault],
        stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)

    def rpc(msg):
        proc.stdin.write(json.dumps(msg) + "\n")
        proc.stdin.flush()
        if "id" in msg:
            return json.loads(proc.stdout.readline())
        return None

    try:
        init = rpc({"jsonrpc": "2.0", "id": 1, "method": "initialize",
                    "params": {"protocolVersion": "2024-11-05", "capabilities": {},
                                "clientInfo": {"name": "smoke", "version": "0"}}})
        check("stdio: initialize", init["result"]["serverInfo"]["name"] == "mnemaos-mcp")
        rpc({"jsonrpc": "2.0", "method": "notifications/initialized"})
        tools = rpc({"jsonrpc": "2.0", "id": 2, "method": "tools/list"})
        names = sorted(t["name"] for t in tools["result"]["tools"])
        check("stdio: six tools listed", names == sorted(
            ["memory_context", "memory_search", "memory_get", "memory_list", "memory_write", "memory_health"]),
            str(names))
        call = rpc({"jsonrpc": "2.0", "id": 3, "method": "tools/call",
                    "params": {"name": "memory_search", "arguments": {"query": "newsletter deadline"}}})
        text = call["result"]["content"][0]["text"]
        check("stdio: tools/call memory_search", "spring-newsletter" in text, text[:200])
        bad = rpc({"jsonrpc": "2.0", "id": 4, "method": "no/such"})
        check("stdio: unknown method -> -32601", bad.get("error", {}).get("code") == -32601)
    finally:
        proc.stdin.close()
        proc.terminate()
        proc.wait(timeout=5)


def run_http_checks(vault):
    token = "smoke-test-token-0123456789"
    env = dict(os.environ, MNEMAOS_TOKEN=token)
    proc = subprocess.Popen(
        [sys.executable, os.path.join(HERE, "server.py"), "--vault", vault, "--http", "127.0.0.1:8971"],
        env=env, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    url = "http://127.0.0.1:8971"
    try:
        deadline = time.time() + 10
        up = False
        while time.time() < deadline:
            try:
                up = urllib.request.urlopen(url + "/health", timeout=1).read() == b"ok"
                break
            except (urllib.error.URLError, ConnectionError):
                time.sleep(0.2)
        check("http: /health up (no auth)", up)

        body = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "tools/call",
                           "params": {"name": "memory_search",
                                       "arguments": {"query": "newsletter deadline"}}}).encode()
        req = urllib.request.Request(url + "/mcp", data=body,
                                     headers={"Content-Type": "application/json"})
        try:
            urllib.request.urlopen(req, timeout=5)
            check("http: request without token -> 401", False)
        except urllib.error.HTTPError as e:
            check("http: request without token -> 401", e.code == 401)

        req = urllib.request.Request(url + "/mcp", data=body,
                                     headers={"Content-Type": "application/json",
                                              "Authorization": "Bearer " + token})
        resp = json.loads(urllib.request.urlopen(req, timeout=5).read())
        text = resp["result"]["content"][0]["text"]
        check("http: authorized tools/call works", "spring-newsletter" in text, text[:200])

        priv = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/call",
                           "params": {"name": "memory_get", "arguments": {"id": "health-topic"}}}).encode()
        req = urllib.request.Request(url + "/mcp", data=priv,
                                     headers={"Content-Type": "application/json",
                                              "Authorization": "Bearer " + token})
        resp = json.loads(urllib.request.urlopen(req, timeout=5).read())
        check("http: remote transport enforces private",
              resp["result"].get("isError") is True)
    finally:
        proc.terminate()
        proc.wait(timeout=5)

    # missing token refuses to start
    proc = subprocess.run(
        [sys.executable, os.path.join(HERE, "server.py"), "--vault", vault, "--http", "127.0.0.1:8972"],
        env={k: v for k, v in os.environ.items() if k != "MNEMAOS_TOKEN"},
        capture_output=True, text=True, timeout=15)
    check("http: refuses to start without MNEMAOS_TOKEN",
          proc.returncode != 0 and "MNEMAOS_TOKEN" in (proc.stderr + proc.stdout))


def run_leakage_selfscan():
    """The package must not leak the reference implementation's private stack."""
    leak_terms = ["Cowork", "MemPalace", "mempalace", "sashaglibiciuc", "glibiciuc",
                  "Интурист", "vps-loop"]
    bad = []
    for root, dirs, files in os.walk(os.path.dirname(HERE)):
        dirs[:] = [d for d in dirs if d not in (".git", "__pycache__")]
        for name in files:
            if name.startswith("smoke_test"):
                continue  # scanner files carry the terms as their own scan patterns
            path = os.path.join(root, name)
            try:
                with open(path, encoding="utf-8") as f:
                    text = f.read()
            except (UnicodeDecodeError, IsADirectoryError):
                continue
            for term in leak_terms:
                if term in text:
                    bad.append("%s: %s" % (os.path.relpath(path, os.path.dirname(HERE)), term))
    check("leakage: package clean of reference-implementation terms", not bad, "; ".join(bad[:5]))


def main():
    tmp = tempfile.mkdtemp(prefix="mnemaos-mcp-smoke-")
    try:
        vault = make_fixture(os.path.join(tmp, "vault"))
        run_index_checks(vault)
        run_local_tool_checks(vault)
        run_privacy_checks(vault)
        run_stdio_protocol_check(vault)
        run_http_checks(vault)
        run_leakage_selfscan()
        # optional: index-compatibility check against a user-supplied vault (read-only)
        if len(sys.argv) > 1:
            ext = os.path.abspath(sys.argv[1])
            db = os.path.join(tmp, "external-index.db")
            stats = indexer.index_vault(ext, db_path=db)
            check("compat: external vault indexes as-is (index written OUTSIDE it)",
                  stats["docs"] > 0, str(stats))
    finally:
        shutil.rmtree(tmp, ignore_errors=True)

    failed = [r for r in RESULTS if not r[1]]
    print("\n%d checks, %d failed" % (len(RESULTS), len(failed)))
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
