# Toolkit — OSINT Investigator

New tools in this folder (stdlib Python only, `--help` + `--dry-run`):

| Tool | Job |
|---|---|
| `target.py` | Intake — creates `cases/<slug>/` with `case.json`, `baseline.md`, `exclusions.md`. Refuses sensitive intake (phone / address / DOB / password / code). |
| `snapshot_diff.py` | Compare two profile snapshots, show only what changed. Pic hash by URL path only; masked 0 counts = UNKNOWN, not a drop. |
| `handle_enum.py` | Public handle/username search plan across platforms. Dry-run first; `--live` = DuckDuckGo HTML, 2s gaps, stop on 429. A hit is a candidate, not a match. |
| `timeline.py` | Dated timeline from verified events (JSONL). Events with no raw timestamp / timezone are flagged UNVERIFIED-TIME. |
| `correlate.py` | Social graph from verified overlaps only. Weak clues (Suggested-for-you, similar names) are listed, never drawn as edges. |
| `report.py` | Structured report: findings + confidence, checked-and-found-nothing (exact scope), cannot-determine, confirm/disprove, next steps. |

Existing tools this system uses — `~/workspace/osint-tools/` (do not duplicate):
`snapshot.py`, `like_sweep.py`, `monitor_courtney.py`, `breach_check.py`,
`leak_search.py`, `darkweb_monitor.py`, `trap_monitor.py`.
See that folder's `README.md` / `toolkit.md` for breach/leak rules
(redacted output, keys in env only, no password-range API, no Tor/onion,
no stolen-DB downloads).

## Run a case

```bash
cd ~/workspace/osint-investigator/toolkit
python3 target.py --name "Jane Example" --handle jane-example --platforms instagram,facebook,x --dry-run
python3 handle_enum.py --handle jane-example --dry-run
python3 snapshot_diff.py --before examples/snapshot-before.json --after examples/snapshot-after.json
python3 timeline.py --events examples/events.jsonl --dry-run
python3 correlate.py --overlaps examples/overlaps.json --dry-run
python3 report.py --case ../cases/example-sigint187/case.json --findings examples/findings.json --dry-run
```

Tested 2026-11-14: all six compile, `--help` works, `--dry-run` works.
No live check was run on any real person during the build.
