# FRICTIONAL: JS2, The Loop, the Tools, and the Diff

These are facts with timestamps, written as they happened. Times are from `date` on this machine (EST, UTC−5).
Entries marked *(Claude Code)* were written by Claude Code (Opus 5.5, CLI 2.1.322). Prathamesh fills in "My take:" only on entries where a decision is his.

## F1. Branch and folder created (2026-11-10 08:06 EST) *(Claude Code)*
- `git checkout -b prathamesh-p-js2-loop-tools-diff a4f7165` (the HEAD was already `a4f7165` on `prathamesh-p-js1-contract-and-watch`).
- Created `fall-2026/prathamesh-p/js2-loop-tools-diff/`.
- Copied unchanged from JS1: `jobwatch.py`, `CONTRACT.md`, `.gitignore`, `tests/test_jobwatch.py`, `tests/hand_labels.json`,
  `tests/hand_label_candidates.json`, `tests/hand_labels.PROVENANCE.md`, `tests/rows2-3-text.txt`, `fixtures/resume.fictional.json`, and `prompts/` (including `archive/`).
- `git diff --stat a4f7165 -- fall-2026/prathamesh-p/js1-contract-and-watch` is empty, so the JS1 folder is unmodified. Nothing is committed.
- The pre-existing untracked folder `fall-2026/prathamesh-p/final-project-film/` came along into the working tree, untouched.

## F2. An extra file was copied that the instruction did not list (2026-11-10 08:06 EST) *(Claude Code)*
- `tests/test_jobwatch.py` reads `raw/2026-10-30/zoox.json` (line 43) for real-data tests. Without it, those tests fail.
- So I also copied `raw/2026-10-30/zoox.json`, `zoox.fetch.txt` and `zoox.headers.txt` from JS1 (2.3 MB). They are byte-identical copies, not new evidence.
- **Decision (Prathamesh, Tue Nov 10 08:17:25 EST 2026):** accept the copy, because the inherited tests need it.
- My take:

## F3. Inherited tests pass in the new folder (2026-11-10 08:06 EST) *(Claude Code)*
- `python -I -m unittest discover -s tests` in `js2-loop-tools-diff/`: **Ran 50 tests, OK** (Python 3.13.1). This is the baseline before any JS2 change.

## F4. Three boards reached with one GET each (2026-11-10 08:07:13–08:07:17 EST) *(Claude Code)*
- curl 8.21.0, single GET, no retry, no auth, User-Agent `info7375-js2-watch`. The raw bodies are saved unmodified, with headers, `.fetch.txt` (start and end times from `date`, HTTP status, bytes, SHA-256) and `SHA256SUMS`, in `raw/2026-11-10/`.

| Board | Platform | HTTP | Bytes | Postings | SHA-256 (first 12) |
|---|---|---:|---:|---:|---|
| zoox | Lever | 200 | 2,413,171 | 234 | 7ebca330474c |
| cloudflare | Greenhouse (`?content=true`) | 200 | 8,275,126 | 466 (`meta.total` = 466) | 6c092ea57d1b |
| openai | Ashby posting API | 200 | 13,794,881 | 826 (none with `isListed: false`) | 7cdd73d3ac3d |

- Zero redirects on all three. These were the only network requests made today.

## F5. Board choice was Claude Code's and was not compared against alternatives (2026-11-10 08:07 EST) *(Claude Code)*
- zoox was named by Prathamesh. Claude Code picked cloudflare (Greenhouse) and openai (Ashby) because it expected network-engineering titles there.
  It made no probing requests to other candidates, so there was no comparison. GATE.md D-1 records this choice for approval.
- **Decision (Prathamesh, Tue Nov 10 08:17:25 EST 2026):** accept cloudflare (Greenhouse) and openai (Ashby), with zoox (Lever).
- My take:

## F6. Network titles and JS1 Gate-1 outcomes on today's data (2026-11-10 08:07 EST) *(Claude Code)*
- These counts come from `jobwatch.title_decision()` (the JS1 Gate 1, unchanged) run over the saved titles.
  - zoox: 3 network titles, 2 include, 1 exclude ("Software Engineer - Road Network Tools", the known false friend from JS1).
  - cloudflare: 20 network titles, 12 include, 8 flag.
  - openai: 12 network titles, 8 include, 4 flag.
- Claude Code's reading, which is not a hand label: these Gate-1 outcomes look questionable.
  - openai "RTL Design Engineer, Networking / NoC" → **include** (NoC is network-on-chip, which is chip design).
  - openai "Community Programs Manager, Champion Network" → **flag**, not exclude.
  - cloudflare "Senior Engineering Manager, Cloudflare Network Interconnect" → **include**, because "Engineering" counts as a role word.
- Gate 1 is governed by JS1 CONTRACT.md, so changing it would be a dated amendment by Prathamesh. Nothing was changed.
- **Decision (Prathamesh, Tue Nov 10 08:17:25 EST 2026):** leave the JS1 title rule unchanged (CONTRACT governs it; JS2 is about the loop). The odd calls are recorded as a known limitation in NOT-CHECKED.md item 1.
- My take:

## F7. Raw size for today is 24 MB (2026-11-10 08:08 EST) *(Claude Code)*
- `du -sh raw/2026-11-10` = 24M (openai 13.8 MB, cloudflare 8.3 MB). JS1 kept its 10.5 MB ShieldAI capture out of git (gitignored, hash tracked).
  Whether to commit these, or to gitignore the big bodies and commit the headers, `.fetch.txt` and `SHA256SUMS`, is not decided. It also affects the Canvas ZIP size.
- **Decision (Prathamesh, Tue Nov 10 08:17:25 EST 2026):** commit the raw/2026-11-10 files (the brief requires saved raw responses; each is under 100 MB).
- My take:

## F8. Symlinks need admin on this machine, but junctions do not (2026-11-10 08:07:35 EST) *(Claude Code)*
- The test ran in the scratchpad (`...\scratchpad\linktest`) from a non-elevated shell (`IsInRole(Administrator)` = False).
- The registry value `HKLM\...\AppModelUnlock\AllowDevelopmentWithoutDevLicense` read back empty, which suggests Developer Mode is off. That is not confirmed in Settings.
- `mklink /D symdir target` → "You do not have sufficient privilege to perform this operation." rc=1
- `mklink symfile.txt target\f.txt` → same message, rc=1
- `mklink /J junc target` → "Junction created for junc <<===>> target", rc=0
- No system setting was changed.
- What this means for the symlink-escape test: `os.symlink` will raise here. GATE.md B5 proposes a junction instead. Another option is to enable Developer Mode yourself.
- **Decision (Prathamesh, Tue Nov 10 08:17:25 EST 2026):** use a directory junction for the escape test, and state in the boundary table that a true symlink needs admin or Developer Mode here and was not tested (GATE B5 updated).
- My take:

## F9. GATE.md drafted, not approved (2026-11-10 ~08:10 EST) *(Claude Code)*
- `GATE.md` was written with 16 `[DRAFT D-n]` decisions. No JS2 code exists. The review-packet plan is in `review/PLAN.md` (draft).
- **Decision (Prathamesh, Tue Nov 10 08:17:25 EST 2026):** GATE D-1 to D-16 approved as drafted; review/PLAN.md approved (defect = JS1 NOT-CHECKED item 7).
- My take:

## F10. GATE.md marked APPROVED (2026-11-10 08:17–08:19 EST) *(Claude Code)*
- The header now reads "APPROVED by Prathamesh on Tue Nov 10 08:17:25 EST 2026". All 16 `[DRAFT D-n]` tags became `[D-n approved]` (a sed replace; `grep` counted 16 and no DRAFT tag remains).
- Boundary row B5 now says a true symlink needs admin or Developer Mode on this machine and is **not tested**. No other GATE text changed. review/PLAN.md is marked approved.
- NOT-CHECKED.md was created with item 1 (the Gate-1 odd calls, from F6) and item 2 (true symlink not tested, from F8).

## F11. Review step 1: reproduction command drafted, NOT run (2026-11-10 08:19 EST) *(Claude Code)*
- Claude Code wrote one CMD line for Prathamesh to run. It records the start time, the SHA-256 of `jobwatch.py` and of JS1's `jobwatch.py`,
  runs `jobwatch.py run` with `--state` and `--out` in a new `%TEMP%\js2-repro-<random>` folder, then records the exit code, a `dir` of that folder and the end time,
  all redirected to `review\01-reproduce.txt`.
- Before the run, the SHA-256 of `jobwatch.py` (js2) is 26c858b391fb… and is identical to JS1's, so the code under reproduction is unpatched JS1.
- Claude Code did not run the reproduction. It checked only the CMD wrapper, with harmless stand-ins (`python -I -m no_such_module_x`) in its scratchpad.
  The first wrapper had a bug: `set D=... &` kept a trailing space in the folder name ("The system cannot find the path specified."). Writing it as `set D=...&`
  fixed it, and a re-test wrote a file and reported `exit_code=1` correctly. The stand-in temp folders were deleted.
- My take:

## F12. Review step 2: test written before any patch, NOT run (2026-11-10 08:19 EST) *(Claude Code)*
- `tests/test_policy.py` has 16 tests (SHA-256 fc917421b62d… at 08:19:48 EST), written from GATE.md sections 1, 4 and 5 and the interface named in review/PLAN.md.
  `policy.py` does not exist, and `jobwatch.py` is unchanged.
- Each test's docstring opens with EXPECTED, written before the body, and also predicts the result on the unpatched code:
  C1–C3 FAIL (exit 0 and files written outside), C4 PASS (control), and P1–P10, R1–R2 ERROR (ModuleNotFoundError: policy).
- The test chooses an interface that GATE.md does not specify: `policy.check_write/check_read`, `PermissionRefused`, `ApprovalRequired`, and the CLI message containing
  "refused" plus the file name. The patch must satisfy it. That choice is Claude Code's.
- C3 deliberately does **not** assert whether `runs/...` was written before the refusal, because GATE section 1 allows a reported partial write.
- Checked only with `ast.parse` (syntax OK, 16 test functions). It was not executed.
- The C-tests run the real CLI on the unpatched code, so running them writes into `%TEMP%\js2-outside-*` (removed in tearDown) and into `state/` and `runs/` inside the project (removed in tearDown).
- My take:

## F13. First attempt at steps 1–2 left no evidence (2026-11-10 08:35–08:37 EST) *(Claude Code)*
- At 08:35, `review/` held only `PLAN.md`. Neither `01-reproduce.txt` nor `02-test-red.txt` existed anywhere under `C:\info7375`, and no `%TEMP%\js2-repro-*` folder existed.
  Claude Code stopped and reported this. The cause was not established.
- At 08:37, a probe line typed as a chat message also produced no file, because a chat message is not executed.
- Prathamesh then ran the probe with the `!` prefix (Git Bash, from his session). It printed `ok` and created `review/_probe.txt`. That file is not committed.
- Claude Code rewrote the step-1 and step-2 commands for Bash and dry-ran the wrapper with harmless stand-ins (08:39). It did not run the reproduction or the test.

## F14. Step 1 run by Prathamesh: defect reproduced (2026-11-10 08:44:04 EST)
- Prathamesh ran the command via `!`. Output: `review/01-reproduce.txt`.
- `jobwatch.py` SHA-256 is `26c858b3…`, identical to JS1's, so the code is unpatched.
- `run --state …\Temp\js2-repro-dGz8\seen_ids.json --out …\Temp\js2-repro-dGz8\run.json` printed `baseline=True total=234 new=0`, and the exit code was **0**.
- The listing shows `run.json` (266 bytes) and `seen_ids.json` (10,550 bytes) **written outside the project folder**.
- My take:

## F15. Step 2 run by Prathamesh: test red as predicted (2026-11-10 08:44:27–08:44:28 EST)
- Prathamesh ran the command via `!`. Output: `review/02-test-red.txt`.
- `tests/test_policy.py` SHA-256 is `fc917421…`, the same as at drafting (F12). `ls policy.py` → "cannot access".
- Result: `Ran 16 tests … FAILED (failures=3, errors=12)`, exit code 1.
  - C1, C2, C3 FAIL with `AssertionError: 0 != 2 : exit code`. This is the defect.
  - C4 ok (control).
  - P1–P10, R1, R2 ERROR with `ModuleNotFoundError: No module named 'policy'`.
  - This matches every prediction in F12.
- Afterwards, no `state/`, `runs/` or `traces/` folder and no `%TEMP%\js2-outside-*` folder remained, so tearDown cleaned up.
  `%TEMP%\js2-repro-dGz8` from step 1 still exists (outside the project; left as evidence).
- Prathamesh accepted the interface choice from F12 (`policy.check_write/check_read`, the refusal errors, and the message containing "refused" plus the file name).
- My take:

## F16. Two commits made (2026-11-10 ~08:45 EST) *(Claude Code)*
- `9051e0d` "JS2: base copied unchanged from JS1 a4f7165, plus raw board captures 2026-11-10". This holds the JS1 copies from F1–F2 and `raw/2026-11-10/` (F7 decision).
  Prathamesh did not ask for this commit. Claude Code made it so that the step-3 patch diffs against committed JS1 code, and so that commit 1 holds only the listed files.
- `b6c78ae` "JS2 review step 2: test before patch". It holds `tests/test_policy.py`, `GATE.md`, `review/PLAN.md`, `review/01-reproduce.txt`, `review/02-test-red.txt`, `FRICTIONAL.md`, `SOURCES.md` and `NOT-CHECKED.md`. There is no patch, and `review/_probe.txt` is excluded.
- Checks after committing:
  - The committed raw JSON blobs have the same SHA-256 as `SHA256SUMS` (zoox 7ebca330…, cloudflare 6c092ea5…, openai 7cdd73d3…).
  - The committed `jobwatch.py` blob equals JS1's committed blob.
  - `core.autocrlf=input`, so `*.headers.txt` (and other CRLF text files) are stored with LF in git. For example, the committed `raw/2026-11-10/zoox.headers.txt` has a different SHA-256 from the on-disk file (2f94e826… vs 4748bcea…). The JSON bodies are unaffected.

## F17. Step 3 blocked: the patch as specified conflicts with "do not change any existing test" (2026-11-10 ~08:50 EST) *(Claude Code)*
- `tests/test_jobwatch.py` (JS1) calls `jobwatch.run()` and `jobwatch.claude_judge()` with `--state`, `--out` and log paths inside `tempfile.TemporaryDirectory()`, which is under `%TEMP%`, **outside** the project.
  GATE section 5 refuses those writes. So if every write inside `jobwatch.py` goes through the policy, those tests error.
- A throwaway probe in the scratchpad (a copy of the folder with a global write guard; not a patch) had 22 test errors. 8 of these are ResumeLoader subtests that error because the probe also blocked the
  **tests' own** fixture writes, an artifact of the probe. The tests that write through `jobwatch` code are **14**: 11 in `Watch` and 3 in `JudgeHarness`.
- No patch was written. Claude Code stopped to ask Prathamesh.
- My take:

## F18. Decision on the F17 conflict (2026-11-10 ~08:47 EST)
- Prathamesh chose "Enforce inside, move temps". `run()`, `fetch()` and `claude_judge()` check every write by default. In `tests/test_jobwatch.py`, **only** `Base.setUp`
  changes: the temp folder moves from `%TEMP%` to `state/_test_tmp_*` inside the project, and no assertion changes. This is an approved exception to "do not change any existing test".
- My take:

## F19. Step 3: the patch was written (2026-11-10 08:47–08:51 EST) *(Claude Code)*
- New `policy.py`: `ROOT`, `PermissionRefused`, `ApprovalRequired`, `check_read`, `check_write`, written against GATE.md section 5 / D-10 and D-11 and the interface accepted in F15.
- `jobwatch.py`: every write goes through `policy.check_write`.
  - `fetch()`: three evidence files, all checked before the first write.
  - `claude_judge()`: the log folder is checked before any `claude -p` call, and each log file before it is written.
  - `_write_atomic()`: the target and its `.tmp` file.
  - `run()`: `--out` and `--state` are checked before anything is read or written.
  - Two helpers were added: `_write()` (the single non-atomic write path) and `WRITTEN` (a list of files written, printed on refusal).
  - `main()` catches `PermissionRefused`, prints `[error] write refused: …` and `[error] status=error step=…; files written before the refusal: …` to stderr, and returns **2**.
  - The `--judge-log` default changed from `judgments` to `traces/judgments`, because `judgments/` is not a GATE-writable folder.
  - `policy.py` is loaded by file path, because `python -I` does not put the script's folder on `sys.path`.
- `tests/test_jobwatch.py`: the `Base.setUp` temp location only (F18). `tests/test_policy.py` is unchanged.
- An intermediate draft wrote headers, fetch metadata and judge logs as bytes, which would have changed them from CRLF to LF on Windows. Claude Code reverted that to text mode, as in JS1, before any run.
- My take:

## F20. Claude Code's own development runs of the suite (2026-11-10 08:50–08:51 EST) *(Claude Code)*
- These were not saved to `review/`. Step 5 is Prathamesh's independent run.
- 08:50:49: `python -I -m unittest discover -s tests` → **Ran 66, FAILED (errors=1)**. The error was P9 (B11): `check_write(raw/2026-11-10/zoox.json, approve=("raw/2026-11-10/zoox.json",))` raised
  ApprovalRequired. The cause was a bug in the first `policy.py`. `os.path.normcase` on Windows lower-cases **and** turns `/` into `\`, so the approve key `raw\2026-11-10\zoox.json` never
  matched the computed `raw/2026-11-10/zoox.json`. Fix: normalize both sides the same way (normcase, then split into components, then join with `/`).
- 08:51:05: the same command → **Ran 66, OK** (50 JS1 + 16 policy). No `state/`, `runs/`, `traces/` or `%TEMP%\js2-outside-*` / `js2-junction-*` folders were left afterwards.
- The step-1 reproduction was **not** re-run by Claude Code.
- My take:

## F21. Steps 3–4 evidence saved; step-5 command drafted, NOT run (2026-11-10 08:51–08:54 EST) *(Claude Code)*
- `review/03-patch.diff`: 240 lines, `git diff -- jobwatch.py policy.py tests/` against `b6c78ae`. `policy.py` is marked intent-to-add (`git add -N`) so that it shows in the diff. Nothing is committed.
- `review/03-behavior.md`: a DRAFT before/after table with 17 rows. Rows not pinned by a test are marked "reading only".
  It also records behavior the diff did not change: reads are still not enforced in `jobwatch.py`; `fetch` with an outside `--raw-dir` still sends the GET before refusing;
  there is no `--approve` CLI flag; and the CLI must now be run from the project folder.
- `review/04-scope.txt`, gathered at 08:51:57 EST:
  - code diff limited to `jobwatch.py` (66 lines changed), `policy.py` (+80) and `tests/test_jobwatch.py` (5 lines, setUp temp location only, with 0 changed `self.assert*` lines);
  - `tests/test_policy.py` diff empty;
  - JS1 folder diff vs `a4f7165` empty;
  - `raw/` diff empty, and `raw/2026-11-10/SHA256SUMS` all OK;
  - remaining write calls exist only inside `_write()` and `_write_atomic()`.
- The first version of `04-scope.txt` had two mistakes in Claude Code's evidence script: the "assert" count matched the word "assertion" in the new comment (it reported 1), and `sha256sum -c`
  ran from the wrong folder ("No such file"). Both were fixed and the file regenerated, and only the corrected version is kept.
- Step 5: Claude Code drafted one Bash command (to run via `!`) for the full suite and the step-1 reproduction on the patched code, writing to `review/05-my-runs.txt`. It was not run.
- My take:

## F22. Step 5 run by Prathamesh on the patched code (2026-11-10 09:00:13–09:00:15 EST)
- Prathamesh ran the command via `!`. Output: `review/05-my-runs.txt`.
- The file hashes in the output match the files on disk afterwards: `jobwatch.py` ad2f3388…, `policy.py` 9a59c17a…, `tests/test_policy.py` fc917421… (unchanged since F12), `tests/test_jobwatch.py` b146bcb9….
- Full suite: **Ran 66 tests, OK**, `suite_exit_code=0`.
- Step-1 reproduction on the patched code: `[error] write refused: …\Temp\js2-repro-zbio\run.json resolves to C:\Users\Prathamesh P\AppData\Local\Temp\js2-repro-zbio\run.json, outside the project folder …`,
  then `[error] status=error step=run; files written before the refusal: none`, and **`repro_exit_code=2`**. `ls` of the temp folder shows it **empty**.
- Observed: the 8.3 short name `PRATHA~1` in the input was expanded to the long name `Prathamesh P` in the resolved path. This bears on review/PLAN.md step-7 candidate (c).
- No `state/`, `runs/` or `traces/` folder was left in the project afterwards.
- My take:

## F23. Step 6 decision: REVISE (2026-11-10, Prathamesh)
- The decision, evidence, revision, accepted scope extras (`9051e0d`, F18 setUp move) and follow-ups (reads through `check_read`, an `--approve` CLI flag) are in `review/06-decision.md`.
  Claude Code transcribed it from Prathamesh's message, signed "Prathamesh, 2026-11-10".
- My take:

## F24. Revision test written first and shown red (2026-11-10 09:02:59–09:03:00 EST) *(Claude Code)*
- New file `tests/test_revision_fetch.py` (SHA-256 cfc85354…). It is a separate file so that the committed step-2 test `tests/test_policy.py` stays byte-identical.
  - V1: library `fetch()` with an outside folder must raise PermissionRefused with 0 calls to a counting fake `urlopen`.
  - V2: CLI `main(["fetch", …, "--raw-dir", <outside>])` must return 2 with 0 calls. The test swaps `fetch.__defaults__` for the fake and restores it, so no real request can happen.
  - V3: control. An inside folder gives exactly 1 call.
- Claude Code ran it before the revision (not Prathamesh). Output in `review/06-revision-red.txt`: V1 and V2 **FAIL with `AssertionError: 1 != 0`**, and V3 ok. This matches the stated predictions.
  V2 also shows the current stderr: refused, `files written before the refusal: none`.

## F25. The revision conflicts with one JS1 test; stopped to ask (2026-11-10 ~09:05 EST) *(Claude Code)*
- The revision (move the three `policy.check_write` calls above the request; `FileExistsError` left where it was) was applied **only in a scratchpad copy** first.
  The full suite there gave **Ran 69, FAILED (errors=1)**. The error was the JS1 test `AllowList.test_refuses_redirect_off_host_and_writes_nothing`. It fetches into a `%TEMP%` folder and
  expects `HostRefused` from a fake off-host redirect. With the path check now before the request, it gets `PermissionRefused` first, and the redirect check is never reached.
- The real `jobwatch.py` is unchanged (still ad2f3388…). Claude Code stopped to ask, because fixing this needs a change to an existing test, and the revision said "No other change".
- My take:

## F26. Decision on F25, and the revision applied (2026-11-10 ~09:08 EST)
- Prathamesh chose "Move its temp folder". In `tests/test_jobwatch.py`, `AllowList.test_refuses_redirect_off_host_and_writes_nothing` now uses `TemporaryDirectory(dir=ROOT/"state")`.
  The location is the only change, and no assertion changed. It still checks that an off-host redirect raises HostRefused and writes no files.
- My take:
- *(Claude Code)* `jobwatch.py` `fetch()`: the three `policy.check_write` calls (and the `day`/`raw` path computation they need) moved above the request. `FileExistsError` stays after the
  request, as before. Nothing else changed. `review/06-revision.diff` holds the revision alone. Its base was reconstructed in the scratchpad by reversing the change, and the reconstructed hashes
  equal those in `05-my-runs.txt` (jobwatch ad2f3388…, test_jobwatch b146bcb9…).
  New hashes: jobwatch.py 56679bcf…, tests/test_jobwatch.py 99ac0136…, tests/test_revision_fetch.py cfc85354…; tests/test_policy.py still fc917421….
- *(Claude Code)* Development check by Claude Code (not saved to review/): the full suite gave **Ran 69, OK**.

## F27. Step 7 proposal: the NTFS hard link, demonstrated only in a scratchpad copy (2026-11-10 09:10:41 EST) *(Claude Code)*
- `review/07_hardlink_demo.py` was run by Claude Code **only in a scratchpad copy of the project** (its own ROOT), not in the real project folder.
  - Case A: a hard link `state/_demo_hardlink_plain_*.json` → a throwaway file in `%TEMP%`. `os.stat(...).st_nlink` = 2, and `policy.check_write` → **ALLOWED**.
    `jobwatch._write` through it changed the outside file to "OVERWRITTEN through state/ hard link".
  - Case B: the same set-up with `jobwatch._write_atomic` (temp file + `os.replace`). The outside file was **unchanged**, because the replace swaps the directory entry and breaks the link.
  - Cleanup: the links and the victim folder were removed.
- My take:

## F28. Steps 6 and 7 runs by Prathamesh (2026-11-10 09:13–09:18 EST)
- At 09:13:46, neither `review/06-after-revision.txt` nor `review/07-still-missed.txt` existed, and no `%TEMP%\js2-hardlink-victim-*` folder existed. Claude Code stopped and reported this.
  Prathamesh then ran both commands via `!` in this session.
- `review/06-after-revision.txt` (SHA-256 1eba1f58…): **Ran 69 tests, OK**, `suite_exit_code=0`.
- `review/07-still-missed.txt` (SHA-256 61eb00a4…, 09:17:59 EST), run in the real project folder:
  - case A (`_write`): `check_write` ALLOWED, and the outside file changed to "OVERWRITTEN through state/ hard link";
  - case B (`_write_atomic`): ALLOWED, and the outside file was unchanged;
  - cleanup True for both, and exit code 0.
- Claude Code checked at 09:18:10: no `state/` folder in the project, and no `js2-hardlink-victim-*` folder in `%TEMP%`.
- Prathamesh's step-7 pick: the NTFS hard link. The claim was drafted by Claude (claude.ai chat) from Claude Code's findings and approved by Prathamesh, and is quoted verbatim in `review/07-still-missed.md`.
  NOT-CHECKED.md items 3 (hard link) and 4 (check-then-write race) were added.
- My take:
