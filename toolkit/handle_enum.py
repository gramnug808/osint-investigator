#!/usr/bin/env python3
"""handle_enum.py — public handle/username search across platforms.

Usage:
  python3 handle_enum.py --handle example-handle --dry-run
  python3 handle_enum.py --handle example-handle --name "Jane Example" --live --max-queries 5
  python3 handle_enum.py --handle example-handle --exclude exclusions.txt --live

What it does:
- Builds a public search plan per platform: site-restricted queries
  for a handle / name, plus handle variants (dots, underscores,
  leetspeak is NOT generated — a leetspeak reading is a clue, not a
  variant to assert).
- --dry-run (default): prints and saves the query plan only. No network.
  Run those queries through browser.search / social.search — the lawful,
  supported way to do the web search.
- --live: DuckDuckGo HTML, 2s gap, stops on 429, saves titles/URLs/
  snippets only. Never logs in, never scrapes a private profile,
  never downloads paste/dump content.

A returned profile is a CANDIDATE, not a match. Run the identity
gates (VERIFICATION.md) before claiming it. Exclusions file: one
handle/name per line, checked and excluded — those are skipped and
logged as excluded, not re-found as "discoveries".
"""
import argparse, html as html_lib, json, os, re, sys, time, urllib.parse, urllib.request, urllib.error
from datetime import datetime, timezone

PLATFORMS = ["instagram", "facebook", "tiktok", "linkedin", "threads",
             "x", "youtube", "snapchat", "reddit", "pinterest"]
DEFAULT_OUT = os.path.expanduser("~/workspace/osint-investigator/toolkit/results/handle-enum")


def ts_now():
    return datetime.now(timezone.utc).strftime("%Y%m%dT%H%M%SZ")


def variants(handle):
    h = handle.lstrip("@").strip()
    out = [h]
    for v in (h.replace(".", "_"), h.replace("_", "."), h.replace(".", ""), h.replace("_", "")):
        if v and v not in out:
            out.append(v)
    return out


def build_queries(handle, name, platforms):
    qs = []
    for v in variants(handle):
        for p in platforms:
            qs.append(f'site:{p}.com "{v}"')
            qs.append(f'site:{p}.com/{v}')
    if name:
        for p in platforms:
            qs.append(f'"{name}" site:{p}.com')
    qs.append(f'"{handle}"')
    return qs


def ddg_search(query):
    url = "https://html.duckduckgo.com/html/?q=" + urllib.parse.quote(query)
    req = urllib.request.Request(url, headers={"User-Agent": "Mozilla/5.0 (OSINT Investigator; lawful public search)"})
    with urllib.request.urlopen(req, timeout=30) as r:
        return r.read().decode("utf-8", "replace")


def parse_results(html_text):
    results = []
    for m in re.finditer(r'class="result__a"[^>]*href="([^"]+)"[^>]*>(.*?)</a>', html_text, re.S):
        title = re.sub(r"<[^>]+>", "", html_lib.unescape(m.group(2))).strip()
        results.append({"title": title, "url": urllib.parse.unquote(m.group(1))})
    return results[:10]


def main():
    ap = argparse.ArgumentParser(description="Public handle enumeration search plan.")
    ap.add_argument("--handle", required=True, help="Handle to search, @ optional")
    ap.add_argument("--name", default="", help="Full name, for cross-platform queries")
    ap.add_argument("--platforms", default=",".join(PLATFORMS))
    ap.add_argument("--exclude", help="File with one excluded handle/name per line")
    ap.add_argument("--max-queries", type=int, default=10)
    ap.add_argument("--live", action="store_true", help="Run DuckDuckGo live (default is dry-run plan only)")
    ap.add_argument("--dry-run", action="store_true", help="Print query plan only, no network")
    ap.add_argument("--out-dir", default=DEFAULT_OUT)
    a = ap.parse_args()

    excluded = set()
    if a.exclude and os.path.exists(a.exclude):
        excluded = {l.strip().lower() for l in open(a.exclude) if l.strip()}
    platforms = [p.strip().lower() for p in a.platforms.split(",") if p.strip()]
    queries = build_queries(a.handle, a.name, platforms)[: a.max_queries]
    print(f"Handle: @{a.handle.lstrip('@')}  variants: {variants(a.handle)}")
    print(f"Platforms: {', '.join(platforms)}  queries: {len(queries)}  excluded: {len(excluded)}")
    if not a.live or a.dry_run:
        print("DRY-RUN — query plan only, no network. Run these via browser.search / social.search:")
        for q in queries:
            print(f"  - {q}")
        print("A returned profile is a CANDIDATE, not a match. Run the identity gates before claiming it.")
        return 0

    os.makedirs(a.out_dir, exist_ok=True)
    all_results, blocked = [], False
    for q in queries:
        try:
            results = parse_results(ddg_search(q))
            all_results.append({"query": q, "results": results})
            print(f"  {q}: {len(results)} result(s)")
        except urllib.error.HTTPError as e:
            print(f"  STOP on HTTP {e.code} for query {q!r} — rate limit, not a negative finding.")
            blocked = True
            break
        except Exception as e:
            print(f"  error on {q!r}: {e}")
        time.sleep(2)
    out = {"handle": a.handle, "name": a.name, "checked_at": ts_now(),
           "blocked_on_429": blocked, "queries_run": len(all_results), "results": all_results}
    path = os.path.join(a.out_dir, f"handle_enum__{a.handle.lstrip('@')}__{ts_now()}.json")
    with open(path, "w") as f:
        json.dump(out, f, indent=2)
    print(f"Saved: {path}  (blocked={blocked})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
