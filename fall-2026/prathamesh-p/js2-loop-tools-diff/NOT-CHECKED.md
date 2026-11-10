# Not checked: running list for the JS2 sign-off

1. **Gate-1 title calls on the new boards (added 2026-11-10, Prathamesh's decision on FRICTIONAL F6).** The JS1 title rule is unchanged
   (JS1 CONTRACT governs it), and on 2026-11-10 data it makes calls that Claude Code read as questionable. For example, openai "RTL Design Engineer,
   Networking / NoC" → include (network-on-chip, which is chip design); openai "Community Programs Manager, Champion Network" → flag; cloudflare
   "Senior Engineering Manager, Cloudflare Network Interconnect" → include ("Engineering" counts as a role word). No hand labels were made for these boards.
2. **True symlink escape (added 2026-11-10, Prathamesh's decision on FRICTIONAL F8).** The escape test uses a directory junction. A real symlink needs
   admin or Developer Mode on this machine (`mklink /D` was refused on 2026-11-10), so a symlink escape is not tested.
3. **Hard-link escape (added 2026-11-10, Prathamesh's step-7 pick).** `policy.check_write` checks where a path points, not which file it is. A hard link under a writable folder to a
   file outside the project passes the policy. Prathamesh's demo run (`review/07-still-missed.txt`, 09:17:59 EST) showed a plain write (`_write`) changing the outside file, while an atomic
   write (`_write_atomic`) did not. No test covers it, and `policy.py` does not close it. See `review/07-still-missed.md`.
4. **Check-then-write race (added 2026-11-10, Prathamesh's step-7 claim).** A link or junction swapped in between `check_write` and the write is not tested and not prevented.

## Items 5–9: proposed by Claude Code on 2026-11-10 (~09:41 EST); CONFIRMED by Prathamesh (Tue Nov 10 09:48:38 EST 2026)

Prathamesh also accepted, at the same time: 410 is reported as `failed_http_410` (item 9), and verify.py's two checks beyond GATE section 7.

5. **The real network transport is untested.** `loop.urllib_transport` (HTTPError → Response, timeout, reset and DNS mapping) is not exercised by any test. Only its redirect handler is (H_3).
   Every error-policy test uses a fake transport. The first real exercise is the live run.
6. **verify.py is independent code, not independent data.** It does not import the agent, and it recomputes every number. But it locates files through the report's paths, and it checks
   hashes against `.fetch.txt` files the agent wrote. An agent that wrote a wrong body and a matching hash would pass check 3.
7. **Login-redirect detection is a path heuristic.** It looks for `/login`, `/signin`, `/sso`, `/oauth` or `/auth` in the final URL path. Any other login page on an allowed host would not be detected.
8. **[FIXED 2026-11-10 09:49 EST; now checked by `tests/test_written_reset.py` W_1. Kept here for the record.]** **`jobwatch.WRITTEN` was process-wide.** It is never reset, so when `jobwatch.main()` runs more than once in one process, a refusal message lists files written by **earlier** calls
   (seen in `demo/CLAUDE-DEV-02-full-suite.txt`, test V2). A single CLI run is not affected. This is in the committed patch `6dc2abb` and is not fixed.
9. **HTTP 410 is named `failed_http_410`.** That follows D-3 (`failed_http_<code>`). The GATE section 4 row lists `failed_http_404` for "404 / 410"; the code follows D-3, not the row.

## Items 10–12: proposed by Claude Code in the README draft (~10:00 EST) as (b), (c), (d); CONFIRMED by Prathamesh (Tue Nov 10 10:23:04 EST 2026)

10. **Terms of use.** Whether each ATS's terms permit this use was not reviewed. Only public, unauthenticated endpoints were used, with one GET per board per run.
11. **Open postings only.** Whether each board's public API lists only open postings was not checked.
12. **Encoding of `demo/00-my-full-suite.txt`.** The file is not valid UTF-8: the Windows console wrote "résumé" from a test docstring in its code page (byte 0xe9). Claude Code read it with replacement characters to check the 120 results.

## Items 13–14: found by Claude Code's fresh-clone check (FRICTIONAL F40); CONFIRMED by Prathamesh (Tue Nov 10 10:27:46 EST 2026)

13. **Line endings.** 41 text files differ from the working copy only in line endings (CRLF in the working copy, LF in git and in a fresh clone). Logged hashes of those files therefore match a clone only
    after line-ending normalization. The raw response bodies are byte-identical.
14. **Absolute paths in run reports.** Run reports store absolute paths (`C:\info7375\…`), so `verify.py` on a committed report only works on this machine.

