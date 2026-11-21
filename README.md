# OSINT Investigator — a purpose-built AI investigator

Built 2026-11-14 for Kevin / Pip. Target-agnostic, lawful public OSINT only.

## What it is

A complete investigator system, not a single script:

- **Directives** — what the investigator may and may not do (`DIRECTIVES.md`)
- **Agent spec** — persona + workflow (`INVESTIGATOR.md`)
- **Verification** — 6-gate fail-closed checklist, with a worked example (`VERIFICATION.md`)
- **Toolkit** — 6 new stdlib-Python tools in `toolkit/`, plus the existing
  `~/workspace/osint-tools/` tools they complement (not replace)
- **Case system** — one folder per target, baseline → snapshots → timeline →
  correlation → report (`CASE_TEMPLATE.md`, `cases/`)
- **Skill** — `~/workspace/custom-skills/osint-investigator/SKILL.md`, so Pip
  can invoke this system as a skill

Tagline: *when killing robots is just a hobby* — evidence first, no fluff,
never call a clue a fact.

## Quick start — first case (10 minutes)

```bash
cd ~/workspace/osint-investigator/toolkit

# 1. Intake — creates cases/<slug>/, no live checks, no writes in dry-run
python3 target.py --name "Example Target" --handle example-handle \
  --platforms instagram,facebook,x --dry-run
python3 target.py --name "Example Target" --handle example-handle \
  --platforms instagram,facebook,x

# 2. Handle enumeration — public search plan first, live only if asked
python3 handle_enum.py --handle example-handle --dry-run
python3 handle_enum.py --handle example-handle --live --max-queries 5

# 3. Snapshot diff — compare two snapshot JSONs, show only what changed
python3 snapshot_diff.py --before examples/snapshot-before.json \
  --after examples/snapshot-after.json

# 4. Timeline — build a dated timeline from verified events only
python3 timeline.py --events examples/events.jsonl --dry-run
python3 timeline.py --events examples/events.jsonl \
  --out ../../cases/example-sigint187/timeline.md

# 5. Correlation — verified overlaps only, weak clues are NOT edges
python3 correlate.py --overlaps examples/overlaps.json --dry-run

# 6. Report — structured findings, confidence, sources, gaps, next steps
python3 report.py --case ../../cases/example-sigint187/case.json \
  --findings examples/findings.json --dry-run
```

Full workflow, gates, and advanced techniques: see `INVESTIGATOR.md`.
Lawful-use rules: see `DIRECTIVES.md`. Verification: see `VERIFICATION.md`.

## Existing tools this system uses (do not duplicate)

In `~/workspace/osint-tools/` — snapshot, like-sweep, monitoring, breach,
leak-search, dark-web monitor. See that folder's `README.md` / `toolkit.md`.

| Existing tool | Use in this system |
|---|---|
| `snapshot.py` | Profile snapshot, timestamped JSON |
| `like_sweep.py` | Like/comment sweep, ≤5 posts, ≥5s spacing, stop on 429 |
| `monitor_courtney.py` | 6-hour monitor for one named case (example, not the system) |
| `breach_check.py` | HIBP + DeHashed, redacted, keys in env only, `--dry-run` default |
| `leak_search.py` | Public leak-mention search plan, `--live` = DuckDuckGo HTML only |
| `darkweb_monitor.py` | Breach monitor stub, watchlist = accounts Kevin owns / is authorised to check only |

New tools in `toolkit/` do the jobs those do not: intake, diff, handle
enumeration, timeline, correlation, reporting. They are target-agnostic —
no target is hard-coded in any of them.

## Test results (2026-11-14, build day)

All tests run with `--help` / `--dry-run` only. **No live check was run on
any real person during the build.**

| Tool | py_compile | --help | --dry-run |
|---|---|---|---|
| target.py | PASS | PASS | PASS — creates no files in dry-run |
| snapshot_diff.py | PASS | PASS | PASS — example before/after: following 685 → 686, CHANGED; masked 0 counts reported UNKNOWN, not a drop |
| handle_enum.py | PASS | PASS | PASS — query plan only, no network |
| timeline.py | PASS | PASS | PASS — example events sorted, 1 event flagged UNVERIFIED-TIME (no raw timestamp / zone) |
| correlate.py | PASS | PASS | PASS — 2 verified edges kept, 2 weak clues rejected as edges |
| report.py | PASS | PASS | PASS — example report generated to stdout in dry-run |

```bash
# Re-run the tests yourself:
cd ~/workspace/osint-investigator/toolkit
for f in target.py snapshot_diff.py handle_enum.py timeline.py correlate.py report.py; do
  python3 -m py_compile "$f" && python3 "$f" --help >/dev/null && python3 "$f" --dry-run >/dev/null && echo "$f PASS"
done
```

## Limits — read before trusting a result

- **Instagram 429 / rate limits.** Like sweeps hit 429 on the first call
  repeatedly since 2026-11-13. A sweep that stops on 429 is a *blocked*
  sweep, not a negative finding. 0 posts checked = 0 hits, not "no likes".
- **Private accounts.** Posts, likers, commenters, follower/following
  lists are not visible. A follow that is still "Requested" changes
  nothing. Do not bypass, do not guess who was followed.
- **No HIBP / DeHashed keys set** (as of build). `breach_check.py` reports
  `skipped_no_key` until `HIBP_API_KEY` / `DEHASHED_EMAIL` +
  `DEHASHED_API_KEY` are set in the environment only. Never hard-code a key.
- **No mobile app.** Stories, reels, and many live Instagram checks need
  the mobile app — desktop web / CLI cannot do them.
- **No Tor / onion crawling, no marketplaces, no stolen-DB downloads,
  no password checking.** Lawful breach APIs + public leak search only.
  See `DIRECTIVES.md`.
- **A "no hit" means no hit in the queries actually run**, not "nothing
  exists anywhere". A name search cannot rule out an account under a
  different name/handle.
- **Browser-only steps.** Canary tokens (canarytokens.org), live Instagram
  browser checks, and any sign-in / form / click work need the browser
  agent. This system never claims a website visit it only fetched as text.

## File map

```
~/workspace/osint-investigator/
  README.md            — this file
  DIRECTIVES.md        — core directives, lawful-use only
  INVESTIGATOR.md      — agent spec: persona, workflow, advanced techniques
  VERIFICATION.md      — 6-gate fail-closed checklist + worked example
  CASE_TEMPLATE.md     — case folder template
  toolkit/
    target.py          — intake, creates a case folder + baseline
    snapshot_diff.py   — compare two snapshots, only what changed
    handle_enum.py     — public handle/username search across platforms
    timeline.py        — dated timeline from verified events
    correlate.py       — cross-platform overlap finder, verified only
    report.py          — structured report generator
    examples/          — example snapshots / events / overlaps / findings
  cases/
    example-sigint187/ — worked example case (Kevin's own public account)
  ../custom-skills/osint-investigator/SKILL.md — skill entry point
```

## Related work (do not re-do)

- `~/workspace/custom-skills/sigint-osint/SKILL.md` — SIGINT/OSINT principles
- `~/workspace/custom-skills/osint-teacher/SKILL.md` + `~/workspace/osint-teacher/curriculum.md` — 7-level teaching curriculum, 6-gate checklist source
- `~/workspace/monitoring/courtney-gibo/` — real case files (baseline, patterns, digital-footprint, snapshots). Examples only; this system is target-agnostic.
- `~/workspace/sigint-app-marketing/` — SigInt187 content, canary log, OPSEC checklist
