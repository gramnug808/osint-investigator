# Report — SigInt187 (example-sigint187)

Question: Worked example: is SigInt187 live, public, and growing, and what is verifiably true about it?
Scope: Read-only public collection. This is Kevin's own public account — the example case uses only public, already-verified facts from 2026-11-13. No private data.
Case created: 2026-11-14T00:00:00Z (Pacific/Honolulu)

## Findings
- **SigInt187 is a public Instagram account, 10 feed posts live as of 2026-11-13 17:13 HST, bio empty** — Confidence: **High**
  Why: Seen live in browser, verified after reload
  Source: https://www.instagram.com/SigInt187/ | Date: 2026-11-13 | Method: browser
- **SigInt187 followers went 5 to 12 when switching Private to Public** — Confidence: **High**
  Why: Counts recorded before and after; the 7 were pending follow requests clearing
  Source: browser check as SigInt187, 2026-11-13 | Date: 2026-11-13 | Method: browser

## Checked and found nothing (exact scope)
- Leak search, 2026-11-14: 5 DuckDuckGo queries each for 'Courtney Gibo' and '_courtg.5', 0 hits — scoped to those queries only
- Like sweep, 2026-11-13: blocked on Instagram 429 on first call, 0 posts checked, 0 hits — blocked, not negative

## Could not be determined
- Who a private account followed (following +1 on 2026-11-13, who is not visible)
- Like times on Instagram (platform shows no like timestamps)
- Whether a follow request has been accepted, without a browser check as the requesting account

## What would confirm / disprove each key claim
- Claim: A handle on a second platform belongs to the same person
  Would confirm: Name + handle + photo/context agreeing, with a second independent source
  Would disprove: Different photo, DOB, workplace, or mutuals; or the handle owner stating otherwise

## Next steps
1. Run handle_enum.py --dry-run for any new handle, then identity gates before claiming it
2. Re-run snapshot_diff.py at the next 6-hour window; report only on change
3. Set HIBP_API_KEY in env only, then run breach_check.py --live on an authorised target
