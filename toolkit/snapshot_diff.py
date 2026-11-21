#!/usr/bin/env python3
"""snapshot_diff.py — compare two profile snapshots, show only what changed.

Usage:
  python3 snapshot_diff.py --before snap1.json --after snap2.json
  python3 snapshot_diff.py --before examples/snapshot-before.json \\
      --after examples/snapshot-after.json --dry-run

Rules (learned from real work):
- Profile-pic URLs carry rotating CDN signed tokens in the query string:
  compare the URL *path* only, otherwise every run "changes".
- A masked 0 follower/following count on a private account is UNKNOWN,
  not a drop. A 0 -> real count, or real -> 0, is reported as
  "masked/unmasked", never as a follower change.
- Output is CHANGED / NO CHANGE per field, with before -> after.
"""
import argparse, json, os, sys
from urllib.parse import urlsplit

FIELDS = ["username", "name", "is_private", "is_verified", "account_type",
          "post_count", "follower_count", "following_count", "bio", "website"]
EXAMPLE_DIR = os.path.join(os.path.dirname(os.path.abspath(__file__)), "examples")


def pic_key(url):
    return urlsplit(url or "").path if url else ""


def normalise(d):
    d = dict(d or {})
    # Accept both the snapshot.py shape and a flat shape.
    if "profile" in d and isinstance(d["profile"], dict):
        d = d["profile"]
    out = {k: d.get(k) for k in FIELDS}
    out["profile_pic_path"] = pic_key(d.get("profile_pic_url") or d.get("profile_pic_path") or "")
    return out


def diff(before, after):
    b, a = normalise(before), normalise(after)
    lines, changed = [], False
    for k in FIELDS + ["profile_pic_path"]:
        bv, av = b.get(k), a.get(k)
        if k in ("follower_count", "following_count"):
            if bv == 0 or av == 0:
                if bv != av:
                    lines.append(f"  {k}: {bv} -> {av}  (MASKED/UNKNOWN — a 0 on a private account is masked, not a real count)")
                    changed = True
                continue
        if bv != av:
            lines.append(f"  {k}: {bv!r} -> {av!r}")
            changed = True
    return changed, lines


def main():
    ap = argparse.ArgumentParser(description="Diff two profile snapshots.")
    ap.add_argument("--before", help="Before snapshot JSON")
    ap.add_argument("--after", help="After snapshot JSON")
    ap.add_argument("--dry-run", action="store_true",
                    help="Use the bundled example snapshots, write nothing")
    a = ap.parse_args()
    if a.dry_run or (not a.before and not a.after):
        a.before = os.path.join(EXAMPLE_DIR, "snapshot-before.json")
        a.after = os.path.join(EXAMPLE_DIR, "snapshot-after.json")
        print("DRY-RUN — bundled example snapshots")
    for path in (a.before, a.after):
        if not path or not os.path.exists(path):
            print(f"snapshot file not found: {path}", file=sys.stderr)
            return 2
    with open(a.before) as f:
        before = json.load(f)
    with open(a.after) as f:
        after = json.load(f)
    changed, lines = diff(before, after)
    print("CHANGED" if changed else "NO CHANGE")
    for line in lines:
        print(line)
    if not lines:
        print("  (all compared fields identical; pic path identical)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
