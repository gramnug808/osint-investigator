# Case Template

Copy this file into a new case folder as `case.json` + `baseline.md` +
`exclusions.md`. Create a case with `toolkit/target.py` — it writes
these files for you. Do not hand-edit a case folder's structure.

## case.json

```json
{
  "case_id": "slug-of-target",
  "name": "Full Name",
  "handles": [
    {"platform": "instagram", "handle": "@handle", "status": "confirmed|suspected|excluded"}
  ],
  "platforms": ["instagram", "facebook", "x", "tiktok", "linkedin", "youtube"],
  "question": "What the user wants to know, in one sentence",
  "scope": "Read-only public collection / monitoring / etc.",
  "authorisation": "What the user explicitly allowed, with date. No authorisation = read-only.",
  "created": "2026-11-14T00:00:00Z",
  "created_tz": "Pacific/Honolulu",
  "exclusions": [],
  "evidence_dir": "evidence/",
  "status": "open"
}
```

Rules:
- No phone numbers, addresses, DOBs, passwords, or codes in `case.json`
  or anywhere in a case folder. If the user supplies one, do not store
  it; note "supplied, not stored".
- Handles are `confirmed` only after the identity gates pass.
  Anything else is `suspected` or `excluded`.

## baseline.md

```markdown
# Baseline — <Name> (<handle>)
Checked: <date> <time> <timezone>
Method: browser / CLI / search — which, and as which account

| Field | Value |
|---|---|
| Handle | @handle |
| Display name | |
| Bio | |
| Website / link | |
| Posts | |
| Followers | |
| Following | |
| Private / public | |
| Verified | |
| Profile pic | description, or hash (URL path only) |

Changes since last check: none / <field>: <before> → <after>
```

## exclusions.md

```markdown
# Exclusions — similar names / handles checked and excluded

| Name / handle | Where found | Why excluded | Date |
|---|---|---|---|
| Cortney Gibson @cortneycgibson | Instagram search | Different person, different handle / context | |
| Courtney Gibson @courtneygibson449 | Instagram search | Different person | |

# Near-misses (not excluded, not confirmed)
| Name / handle | Why it is a near-miss | What would confirm / disprove it |
|---|---|---|
```

A near-miss that is not logged will be re-found as a "discovery" later.
Log it now.

## Folder layout

```
cases/<slug>/
  case.json
  baseline.md
  exclusions.md
  timeline.md        — from toolkit/timeline.py
  graph.md           — from toolkit/correlate.py
  report.md          — from toolkit/report.py
  evidence/          — raw snapshots, sweep JSON, search results (timestamped)
  snapshots/         — profile snapshots (or link to the shared snapshots dir)
```

## Report structure (see toolkit/report.py)

Findings (confidence + why + source + date + method) → What was checked
and found nothing (exact scope) → What could not be determined →
What would confirm / disprove each key claim → Next steps.
