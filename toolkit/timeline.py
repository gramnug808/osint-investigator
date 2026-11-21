#!/usr/bin/env python3
"""timeline.py — build a dated timeline from verified events.

Usage:
  python3 timeline.py --events events.jsonl --dry-run
  python3 timeline.py --events events.jsonl --out timeline.md

Events file: one JSON object per line:
  {"date": "2026-11-13", "raw_timestamp": "2026-11-13T09:41:00-10:00",
   "timezone": "Pacific/Honolulu", "event": "First post live",
   "source": "https://www.instagram.com/p/...", "confidence": "High"}

Rules:
- Events are sorted by date, then raw_timestamp.
- An event with no raw_timestamp, or no timezone, is flagged
  UNVERIFIED-TIME in the output — its timing is not asserted.
  (Instagram likes have no timestamps: those events must be
  flagged, never given an invented time.)
- Confidence is carried through unchanged; the timeline does not
  upgrade it. A cluster is not a cause — the output says so.
"""
import argparse, json, os, sys

EXAMPLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples", "events.jsonl")


def load_events(path):
    events = []
    with open(path) as f:
        for i, line in enumerate(f, 1):
            line = line.strip()
            if not line:
                continue
            try:
                e = json.loads(line)
            except json.JSONDecodeError as ex:
                print(f"line {i}: bad JSON, skipped ({ex})", file=sys.stderr)
                continue
            e["_line"] = i
            events.append(e)
    return events


def render(events):
    def key(e):
        return (e.get("date") or "9999", e.get("raw_timestamp") or "9999")
    events = sorted(events, key=key)
    lines = ["# Timeline — verified events only", "",
             "A cluster is not a cause. Events flagged UNVERIFIED-TIME have no",
             "raw timestamp / timezone — their timing is not asserted.", ""]
    for e in events:
        raw, tz = e.get("raw_timestamp"), e.get("timezone")
        flag = "" if (raw and tz) else "  **UNVERIFIED-TIME**"
        lines.append(f"- **{e.get('date', '?')}** {raw or 'no raw timestamp'}"
                     f" ({tz or 'no timezone'}) — {e.get('event', '?')}{flag}")
        lines.append(f"  Source: {e.get('source', 'not recorded')} | Confidence: {e.get('confidence', 'Unverified')}")
    unverified = sum(1 for e in events if not (e.get("raw_timestamp") and e.get("timezone")))
    lines += ["", f"Total events: {len(events)} | UNVERIFIED-TIME: {unverified}"]
    return "\n".join(lines) + "\n"


def main():
    ap = argparse.ArgumentParser(description="Build a dated timeline from verified events.")
    ap.add_argument("--events", help="JSONL events file")
    ap.add_argument("--out", help="Write timeline Markdown here")
    ap.add_argument("--dry-run", action="store_true", help="Use bundled example events, write nothing")
    a = ap.parse_args()
    path = EXAMPLE if (a.dry_run or not a.events) else a.events
    if not os.path.exists(path):
        print(f"events file not found: {path}", file=sys.stderr)
        return 2
    events = load_events(path)
    if a.dry_run:
        print("DRY-RUN — bundled example events")
    text = render(events)
    print(text)
    if a.out and not a.dry_run:
        with open(a.out, "w") as f:
            f.write(text)
        print(f"Saved: {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
