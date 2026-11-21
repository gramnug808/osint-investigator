#!/usr/bin/env python3
"""correlate.py — cross-platform overlap finder, verified overlaps only.

Usage:
  python3 correlate.py --overlaps overlaps.json --dry-run
  python3 correlate.py --overlaps overlaps.json --out graph.md

Overlaps file: JSON {"overlaps": [{"a": "X", "b": "Y", "type": "mutual_follower",
"evidence": "...", "strength": "Verified|Strong|Weak", "source": "...", "date": "..."}]}

Rules:
- Only Verified / Strong overlaps become graph edges.
- Weak clues are NOT edges: Suggested-for-you, similar names, same
  school/workplace, same town. They are listed separately as weak
  clues, never drawn as links.
- If you have to guess an edge, delete it.
"""
import argparse, json, os, sys
from collections import defaultdict

EXAMPLE = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples", "overlaps.json")
EDGE_TYPES = {"mutual_follower", "followed_by", "shared_liker", "same_comment_thread",
              "shared_follower", "mutual_follow"}
WEAK_TYPES = {"suggested_for_you", "similar_name", "same_school", "same_workplace", "same_town"}


def main():
    ap = argparse.ArgumentParser(description="Correlate verified overlaps into a graph.")
    ap.add_argument("--overlaps", help="JSON overlaps file")
    ap.add_argument("--out", help="Write graph Markdown here")
    ap.add_argument("--dry-run", action="store_true", help="Use bundled example overlaps, write nothing")
    a = ap.parse_args()
    path = EXAMPLE if (a.dry_run or not a.overlaps) else a.overlaps
    if not os.path.exists(path):
        print(f"overlaps file not found: {path}", file=sys.stderr)
        return 2
    with open(path) as f:
        data = json.load(f)
    overlaps = data.get("overlaps", [])
    edges, weak, rejected = [], [], []
    for o in overlaps:
        strength = (o.get("strength") or "").strip()
        otype = (o.get("type") or "").strip()
        if strength in ("Verified", "Strong") and otype in EDGE_TYPES:
            edges.append(o)
        elif otype in WEAK_TYPES or strength == "Weak":
            weak.append(o)
        else:
            rejected.append(o)
    nodes = sorted({n for o in edges for n in (o.get("a"), o.get("b")) if n})
    lines = ["# Social graph — verified overlaps only", "",
             "Weak clues are listed below, never drawn as links.", "",
             "## Edges (Verified / Strong)"]
    for o in edges:
        lines.append(f"- **{o.get('a')} ↔ {o.get('b')}** — {o.get('type')} ({o.get('strength')}) — {o.get('evidence', '')} — {o.get('source', '')} {o.get('date', '')}")
    lines += ["", "## Weak clues (not edges)"]
    for o in weak:
        lines.append(f"- {o.get('a')} ~ {o.get('b')} — {o.get('type')} ({o.get('strength')}) — {o.get('evidence', '')}")
    if rejected:
        lines += ["", "## Rejected (unknown type / strength — fix and re-run)"]
        for o in rejected:
            lines.append(f"- {o}")
    lines += ["", f"Nodes: {len(nodes)} | Edges: {len(edges)} | Weak clues: {len(weak)} | Rejected: {len(rejected)}"]
    text = "\n".join(lines) + "\n"
    if a.dry_run:
        print("DRY-RUN — bundled example overlaps")
    print(text)
    if a.out and not a.dry_run:
        with open(a.out, "w") as f:
            f.write(text)
        print(f"Saved: {a.out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
