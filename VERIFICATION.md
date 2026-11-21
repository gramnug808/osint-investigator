# Verification — 6-Gate Fail-Closed Checklist

Use this before calling anything "verified". If any gate fails,
downgrade the claim. Never upgrade a clue to a fact to make a story better.

## The 6 gates

| # | Gate | Pass means | Fail means |
|---|---|---|---|
| 1 | **Source** | Primary, public, reachable again. URL, date, method recorded. | A screenshot with no URL, a "someone said", a fetch that hit Cloudflare. Downgrade to Unverified. |
| 2 | **Corroboration** | A second independent source agrees. | One source only = a clue, not proof. Downgrade to Medium at best. |
| 3 | **Identity** | Name + handle + photo / DOB / context match. No merging on name alone. | Same name, different person is possible. Downgrade to Unverified / Cannot determine. |
| 4 | **Time** | Timestamp from the platform, raw value + timezone recorded. | No raw timestamp, zone unverified, or Instagram like (no like timestamps). Downgrade the timing claim. |
| 5 | **Access** | You saw it yourself, in the browser / CLI, after reload where it matters. | A 200 status, a tool summary, or a Cloudflare page. Downgrade to Unverified. |
| 6 | **Exit** | You can re-check / undo it. Snapshot saved, raw output saved, what would disprove it noted. | No snapshot, no re-check path. Downgrade to Medium at best. |

## Confidence after the gates

- **All 6 pass:** High / Verified.
- **1 gate weak, rest pass:** Medium / Strong clue — say which gate is weak.
- **2+ gates fail, or identity / source fails:** Low / Weak clue, or Unverified.
- **Evidence needed is private / blocked / absent:** Cannot determine — say why.

## Worked example

**Claim:** "Courtney Gibo liked Zach Fitz's August 26, 2025 photo post, overnight."

| Gate | Result |
|---|---|
| 1. Source | PASS — Instagram post, seen in browser, URL recorded, 2026-11-13 |
| 2. Corroboration | WEAK — one platform, one viewer; no second source for a like |
| 3. Identity | PASS — liker shown as @_courtg.5, the account Kevin identifies as his wife; handle + context match |
| 4. Time | **FAIL** — Instagram shows no like timestamps. The "~00:14–02:45" times came from a tool with no raw `created_at` surviving, zone unverified. If UTC, they convert to afternoon HST the prior day. |
| 5. Access | PASS — seen in browser |
| 6. Exit | PASS — snapshot / sweep JSON saved, re-checkable |

**Verdict:** The *like* is High / Verified. The *overnight timing* is
**Unverified** — do not report it as overnight. Report: "liked the
Aug 26, 2025 post; like time not available from Instagram."

That is the discipline: split a claim into its parts, gate each part,
and let the weakest gate set the confidence for that part.

## Worked example 2 — identity, do not merge

**Claim:** "The Julian in the Facebook reel is the Julian Ian Aquino
on the Hawaii sex-offender registry."

| Gate | Result |
|---|---|
| 1. Source | PASS for each half separately — reel URL, registry mirrors with ID A6009985 |
| 2. Corroboration | PASS that a registrant by that name exists (two mirrors, same ID / offenses / date) |
| 3. Identity | **FAIL** — reel gives no middle name, age, or DOB; alias "Yuz Gonzo" is not in the registry record; registrant b. 1988, reel subject's age unknown |
| 4. Time | PASS for the registry disposition (Mar 23, 2012); N/A for the merge |
| 5. Access | WEAK — official ehawaii.gov details page returned only a search landing page in text fetch; no live official confirmation |
| 6. Exit | PASS — sources saved |

**Verdict:** High that a Hawaii registrant named Julian Ian Aquino
exists. **Unverified** that he is the reel Julian. Do not state
"the Julian in the video is a sex offender." What would confirm it:
live official registry / NSOPW check + current status, and a photo
match / DOB / handle confirmation from the user.

## Checklist — copy into a case report

```
[ ] Gate 1 Source:    URL / date / method recorded, primary + public?
[ ] Gate 2 Corroboration: second independent source?
[ ] Gate 3 Identity:  name + handle + photo/DOB/context match, no merge on name alone?
[ ] Gate 4 Time:      raw timestamp + timezone recorded, or flagged UNVERIFIED-TIME?
[ ] Gate 5 Access:    seen yourself, after reload where it matters, not a Cloudflare fetch?
[ ] Gate 6 Exit:      snapshot / raw output saved, what would disprove it noted?
Confidence: High / Medium / Low / Unverified / Cannot determine
Weakest gate: ___
Downgraded from: ___ to: ___ because: ___
```

## Common gate failures (from real work, 2026-11-13)

- **Follower jump 5 → 12 on going public:** Gate 4 / Access — the 7 were
  pending follow requests clearing, not 7 new organic discoveries.
  Always check the before-state.
- **Masked 0 follower/following counts via CLI on a private account:**
  Gate 5 — a masked 0 is not a real count. Record as UNKNOWN.
- **"No likes found" after a 429:** Gate 5 — sweep was blocked, 0 posts
  checked. That is not a negative finding.
- **Cloudflare "Just a moment":** Gate 1 / 5 — that fetch is not the page.
- **Broker middle name "Miyuki":** Gate 2 / 3 — single broker source,
  unverified, do not treat as confirmed.
- **UH West Oahu NSLS Fall 2019:** Gate 1 / 2 — not re-verified, treat
  as unconfirmed.
