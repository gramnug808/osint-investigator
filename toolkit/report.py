#!/usr/bin/env python3
"""report.py — generate a structured OSINT report for a case.

Usage:
  python3 report.py --case cases/example-sigint187/case.json \\
      --findings examples/findings.json --dry-run
  python3 report.py --case cases/example-sigint187/case.json \\
      --findings examples/findings.json --out cases/example-sigint187/report.md

Findings file: JSON {"findings": [{"finding": "...", "confidence": "High|Medium|Low|Unverified|Cannot determine",
"why": "...", "source": "...", "date": "...", "method": "..."}],
"checked_no_hit": ["..."], "cannot_determine": ["..."],
"confirm_disprove": [{"claim": "...", "would_confirm": "...", "would_disprove": "..."}],
"next_steps": ["..."]}

Structure (every report, every time):
findings -> what was checked and found nothing (exact scope) ->
what could not be determined -> what would confirm/disprove ->
next steps. Confidence is never upgraded by the report.
"""
import argparse, json, os, sys

EXAMPLE_CASE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "cases", "example-sigint187", "case.json")
EXAMPLE_FINDINGS = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples", "findings.json")


def render(case, data):
    lines = [f"# Report — {case.get('name', 'Unknown target')} ({case.get('case_id', '?')})", "",
             f"Question: {case.get('question', '')}",
             f"Scope: {case.get('scope', '')}",
             f"Case created: {case.get('created', '')} ({case.get('created_tz', '')})", "",
             "## Findings"]
    for f in data.get("findings", []):
        lines.append(f"- **{f.get('finding', '?')}** — Confidence: **{f.get('confidence', 'Unverified')}**")
        lines.append(f"  Why: {f.get('why', '')}")
        lines.append(f"  Source: {f.get('source', '')} | Date: {f.get('date', '')} | Method: {f.get('method', '')}")
    lines += ["", "## Checked and found nothing (exact scope)"]
    for item in data.get("checked_no_hit", []):
        lines.append(f"- {item}")
    lines += ["", "## Could not be determined"]
    for item in data.get("cannot_determine", []):
        lines.append(f"- {item}")
    lines += ["", "## What would confirm / disprove each key claim"]
    for item in data.get("confirm_disprove", []):
        lines.append(f"- Claim: {item.get('claim', '')}")
        lines.append(f"  Would confirm: {item.get('would_confirm', '')}")
        lines.append(f"  Would disprove: {item.get('would_disprove', '')}")
    lines += ["", "## Next steps"]
    for i, item in enumerate(data.get("next_steps", []), 1):
        lines.append(f"{i}. {item}")
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Generate a structured OSINT report.")
    ap.add_argument("--case", help="case.json")
    ap.add_argument("--findings", help="findings JSON")
    ap.add_argument("--out", help="Write report Markdown here")
    ap.add_argument("--dry-run", action="store_true", help="Use bundled example case + findings, write nothing")
    a = ap.parse_args()
    case_path = EXAMPLE_CASE if (a.dry_run or not a.case) else a.case
    findings_path = EXAMPLE_FINDINGS if (a.dry_run or not a.findings) else a.findings
    for path in (case_path, findings_path):
        if not os.path.exists(path):
            print(f"file not found: {path}", file=sys.stderr)
            return 2
    with open(case_path) as f:
        case = json.load(f)
    with open(findings_path) as f:
        data = json.load(f)
    if a.dry_run:
        print("DRY-RUN — bundled example case + findings")
    text = render(case, data)
    print(text)
    if a.out and not a.dry_run:
        with open(a.out, "w") as f:
            f.write(text)
        print(f"Saved: {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
