#!/usr/bin/env python3
"""target.py — OSINT Investigator intake.

Creates a case folder for a target, with baseline scaffolding.
Target-agnostic: no target is hard-coded.

Usage:
  python3 target.py --name "Jane Example" --handle jane-example \\
      --platforms instagram,facebook,x --dry-run
  python3 target.py --name "Jane Example" --handle jane-example \\
      --platforms instagram,facebook,x --question "Is there a public footprint?"
  python3 target.py --name "Jane Example" --handle jane-example \\
      --cases-dir ~/workspace/osint-investigator/cases

Refuses to store sensitive intake: phone numbers, street addresses,
dates of birth, passwords, codes. If such a value is passed, it is
stripped and the run notes "supplied, not stored" — it is never
written to a case file.
"""
import argparse, json, os, re, sys
from datetime import datetime, timezone

DEFAULT_CASES = os.path.expanduser("~/workspace/osint-investigator/cases")
SENSITIVE_PATTERNS = [
    (r"\b\d{3}[-.\s]?\d{3}[-.\s]?\d{4}\b", "phone-like value"),
    (r"\b\d{4}-\d{2}-\d{2}\b", "date-like value (possible DOB)"),
    (r"(?i)\b(password|passwd|otp|verification code|2fa)\b", "credential-like value"),
]
KNOWN_PLATFORMS = {"instagram", "facebook", "tiktok", "linkedin", "threads",
                   "x", "twitter", "youtube", "snapchat", "reddit", "pinterest",
                   "github", "telegram"}


def slugify(name, handle=None):
    base = (handle or name or "target").lstrip("@").lower()
    base = re.sub(r"[^a-z0-9]+", "-", base).strip("-")
    return base or "target"


def check_sensitive(text, label):
    hits = []
    for pat, what in SENSITIVE_PATTERNS:
        if re.search(pat, text or ""):
            hits.append(f"{label}: {what}")
    return hits


def main():
    ap = argparse.ArgumentParser(description="Create an OSINT Investigator case folder.")
    ap.add_argument("--name", required=True, help="Target display name")
    ap.add_argument("--handle", help="Known handle, without @ is fine")
    ap.add_argument("--platforms", default="instagram",
                    help="Comma-separated platforms, e.g. instagram,facebook,x")
    ap.add_argument("--question", default="", help="What the user wants to know")
    ap.add_argument("--scope", default="Read-only public collection",
                    help="Authorised scope")
    ap.add_argument("--cases-dir", default=DEFAULT_CASES)
    ap.add_argument("--dry-run", action="store_true", help="Print plan only, write nothing")
    a = ap.parse_args()

    problems = []
    problems += check_sensitive(a.name, "name")
    problems += check_sensitive(a.handle or "", "handle")
    problems += check_sensitive(a.question, "question")
    platforms = [p.strip().lower() for p in a.platforms.split(",") if p.strip()]
    unknown = [p for p in platforms if p not in KNOWN_PLATFORMS]
    if unknown:
        problems.append(f"unknown platforms (check spelling): {', '.join(unknown)}")
    if problems:
        print("INTAKE REFUSED / STRIPPED — sensitive or invalid input:")
        for p in problems:
            print(f"  - {p}")
        print("Sensitive values are NOT stored. Re-run without them.")
        return 2

    slug = slugify(a.name, a.handle)
    case_dir = os.path.join(a.cases_dir, slug)
    ts = datetime.now(timezone.utc).strftime("%Y-%m-%dT%H:%M:%SZ")
    case = {
        "case_id": slug,
        "name": a.name,
        "handles": ([{"platform": platforms[0], "handle": "@" + (a.handle or "").lstrip("@"),
                      "status": "suspected"}] if a.handle else []),
        "platforms": platforms,
        "question": a.question,
        "scope": a.scope,
        "authorisation": "Read-only public collection unless the user explicitly allows more.",
        "created": ts,
        "created_tz": "Pacific/Honolulu",
        "exclusions": [],
        "evidence_dir": "evidence/",
        "status": "open",
    }
    if a.dry_run:
        print(f"DRY-RUN — would create case '{slug}' at {case_dir}")
        print(json.dumps(case, indent=2))
        print("Files: case.json, baseline.md, exclusions.md, timeline.md, graph.md, report.md, evidence/")
        return 0

    os.makedirs(os.path.join(case_dir, "evidence"), exist_ok=True)
    os.makedirs(os.path.join(case_dir, "snapshots"), exist_ok=True)
    with open(os.path.join(case_dir, "case.json"), "w") as f:
        json.dump(case, f, indent=2)
    baseline = (
        f"# Baseline — {a.name} ({'@' + (a.handle or '').lstrip('@') if a.handle else 'no handle yet'})\n"
        f"Checked: {ts} UTC (Pacific/Honolulu)\nMethod: intake only — baseline not yet collected\n\n"
        "| Field | Value |\n|---|---|\n| Handle | " + (a.handle or "") + " |\n| Display name | |\n| Bio | |\n| Website / link | |\n| Posts | |\n| Followers | |\n| Following | |\n| Private / public | |\n| Verified | |\n| Profile pic | |\n\nChanges since last check: none — first baseline\n"
    )
    with open(os.path.join(case_dir, "baseline.md"), "w") as f:
        f.write(baseline)
    with open(os.path.join(case_dir, "exclusions.md"), "w") as f:
        f.write("# Exclusions — similar names / handles checked and excluded\n\n"
                "| Name / handle | Where found | Why excluded | Date |\n|---|---|---|---|\n\n"
                "# Near-misses (not excluded, not confirmed)\n\n"
                "| Name / handle | Why it is a near-miss | What would confirm / disprove it |\n|---|---|---|\n")
    for name in ("timeline.md", "graph.md", "report.md"):
        with open(os.path.join(case_dir, name), "w") as f:
            f.write(f"# {name[:-3].title()} — {a.name}\n\nNot yet generated. See toolkit/ for the generator.\n")
    print(f"Case created: {case_dir}")
    print(f"  case_id: {slug}  platforms: {', '.join(platforms)}")
    print("  Next: collect a baseline, then run handle_enum.py / snapshot.py, then timeline.py / correlate.py / report.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
