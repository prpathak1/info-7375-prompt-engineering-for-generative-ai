# Step 7: a case the tests still miss (the NTFS hard link)

**Picked by:** Prathamesh, 2026-11-10.

## Claim
*Drafted by Claude (claude.ai chat) from Claude Code's findings, and approved by Prathamesh:*

> My tests check where a path points, not what file it is. A hard link inside raw/ or state/ to a file outside the project passes the policy, because a hard link is a second name for the same file, not a pointer to follow. My demo showed a plain write going through it to the outside file, while an atomic write did not. Today's call sites are hard to exploit (run() writes atomically, fetch() refuses existing raw files, judge logs use random names), but policy.py itself does not close this hole, and a check-then-write race is also untested.

## Evidence
- **Demo script:** `review/07_hardlink_demo.py` (SHA-256 dcd48795…). It makes no network requests. It creates a throwaway "victim" file in a new `%TEMP%` folder, hard-links it from `state/` with a random name, and removes both at the end.
- **Run by Prathamesh via `!`** on 2026-11-10 at 09:17:59 EST, in the real project folder. Output: `review/07-still-missed.txt` (SHA-256 61eb00a4…), exit code 0.

| Case | Write path | `st_nlink` | `policy.check_write(link)` | Outside file afterwards |
|---|---|---:|---|---|
| A | `jobwatch._write` (plain write; used by `fetch`, `claude_judge`) | 2 | **ALLOWED** | `'OVERWRITTEN through state/ hard link\n'`, so **changed** |
| B | `jobwatch._write_atomic` (temp file + `os.replace`; used by `run`) | 2 | **ALLOWED** | `'ORIGINAL outside content\n'`, so **unchanged** (the replace breaks the link) |

- **Cleanup:** the links and the victim folder were removed (`cleanup: links removed: True | victim folder removed: True`). Afterwards, no `state/` folder and no `%TEMP%\js2-hardlink-victim-*` folder remained (checked by Claude Code at 09:18:10 EST).
- **Earlier dry-run:** Claude Code had run the same script only in a scratchpad copy of the project first, at 09:10:41 EST (FRICTIONAL F27), with the same outcome.
- **Exposure reading:** the claim that today's call sites are hard to exploit comes from reading the code. **No test checks it.**

## Possible fixes (not made; for later)
1. **Refuse existing targets with more than one name.** In `policy.check_write`, refuse any existing target whose `os.stat(...).st_nlink > 1`.
2. **Make every write atomic.** Route every write through the temp-file + `os.replace` path, so that a write replaces the directory entry and never writes into a shared file.

Neither fix closes the **check-then-write race** (TOCTOU), where a link or junction is swapped in between `check_write` and the write. That case is untested.
