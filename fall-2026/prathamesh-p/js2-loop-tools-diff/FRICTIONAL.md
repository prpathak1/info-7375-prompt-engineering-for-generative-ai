# FRICTIONAL: JS2, The Loop, the Tools, and the Diff

These are facts with timestamps, written as they happened. Times are from `date` on this machine (EST, UTC−5).
Entries marked *(Claude Code)* were written by Claude Code (Opus 5.5, CLI 2.1.322).

My take lines appear on entries where I made a decision. Entries with one: F5 (board choice), F6 (title-rule limitation), F8 (junction instead of symlink), F18 (enforce inside vs CLI-only), F23 (step-6 REVISE), F28 (step-7 hard-link case), F34 (WRITTEN defect in my accepted patch), F36 (live run), F37 (SEEDED demo).

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
- My take: Three platforms meant three different JSON shapes, all mapped onto one posting shape. Using only Lever would have hidden whether the loop really works across boards.

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
- My take: "RTL Design Engineer, Networking / NoC" counting as a network role shows the rule matches words, not meaning. I kept it unchanged because JS2 is about the loop, but I wouldn't trust its "relevant" without reading the posting.

## F7. Raw size for today is 24 MB (2026-11-10 08:08 EST) *(Claude Code)*
- `du -sh raw/2026-11-10` = 24M (openai 13.8 MB, cloudflare 8.3 MB). JS1 kept its 10.5 MB ShieldAI capture out of git (gitignored, hash tracked).
  Whether to commit these, or to gitignore the big bodies and commit the headers, `.fetch.txt` and `SHA256SUMS`, is not decided. It also affects the Canvas ZIP size.
- **Decision (Prathamesh, Tue Nov 10 08:17:25 EST 2026):** commit the raw/2026-11-10 files (the brief requires saved raw responses; each is under 100 MB).

## F8. Symlinks need admin on this machine, but junctions do not (2026-11-10 08:07:35 EST) *(Claude Code)*
- The test ran in the scratchpad (`...\scratchpad\linktest`) from a non-elevated shell (`IsInRole(Administrator)` = False).
- The registry value `HKLM\...\AppModelUnlock\AllowDevelopmentWithoutDevLicense` read back empty, which suggests Developer Mode is off. That is not confirmed in Settings.
- `mklink /D symdir target` → "You do not have sufficient privilege to perform this operation." rc=1
- `mklink symfile.txt target\f.txt` → same message, rc=1
- `mklink /J junc target` → "Junction created for junc <<===>> target", rc=0
- No system setting was changed.
- What this means for the symlink-escape test: `os.symlink` will raise here. GATE.md B5 proposes a junction instead. Another option is to enable Developer Mode yourself.
- **Decision (Prathamesh, Tue Nov 10 08:17:25 EST 2026):** use a directory junction for the escape test, and state in the boundary table that a true symlink needs admin or Developer Mode here and was not tested (GATE B5 updated).
- My take: The junction test still proves the policy resolves links before comparing paths, but it isn't a symlink. I'd rather name that gap than pretend it's covered.

## F9. GATE.md drafted, not approved (2026-11-10 ~08:10 EST) *(Claude Code)*
- `GATE.md` was written with 16 `[DRAFT D-n]` decisions. No JS2 code exists. The review-packet plan is in `review/PLAN.md` (draft).
- **Decision (Prathamesh, Tue Nov 10 08:17:25 EST 2026):** GATE D-1 to D-16 approved as drafted; review/PLAN.md approved (defect = JS1 NOT-CHECKED item 7).

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

## F18. Decision on the F17 conflict (2026-11-10 ~08:47 EST)
- Prathamesh chose "Enforce inside, move temps". `run()`, `fetch()` and `claude_judge()` check every write by default. In `tests/test_jobwatch.py`, **only** `Base.setUp`
  changes: the temp folder moves from `%TEMP%` to `state/_test_tmp_*` inside the project, and no assertion changes. This is an approved exception to "do not change any existing test".
- My take: A command-line-only check would have protected nothing the loop does, because the loop calls the functions directly. The rule has to live where the write happens.

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

## F20. Claude Code's own development runs of the suite (2026-11-10 08:50–08:51 EST) *(Claude Code)*
- These were not saved to `review/`. Step 5 is Prathamesh's independent run.
- 08:50:49: `python -I -m unittest discover -s tests` → **Ran 66, FAILED (errors=1)**. The error was P9 (B11): `check_write(raw/2026-11-10/zoox.json, approve=("raw/2026-11-10/zoox.json",))` raised
  ApprovalRequired. The cause was a bug in the first `policy.py`. `os.path.normcase` on Windows lower-cases **and** turns `/` into `\`, so the approve key `raw\2026-11-10\zoox.json` never
  matched the computed `raw/2026-11-10/zoox.json`. Fix: normalize both sides the same way (normcase, then split into components, then join with `/`).
- 08:51:05: the same command → **Ran 66, OK** (50 JS1 + 16 policy). No `state/`, `runs/`, `traces/` or `%TEMP%\js2-outside-*` / `js2-junction-*` folders were left afterwards.
- The step-1 reproduction was **not** re-run by Claude Code.

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

## F22. Step 5 run by Prathamesh on the patched code (2026-11-10 09:00:13–09:00:15 EST)
- Prathamesh ran the command via `!`. Output: `review/05-my-runs.txt`.
- The file hashes in the output match the files on disk afterwards: `jobwatch.py` ad2f3388…, `policy.py` 9a59c17a…, `tests/test_policy.py` fc917421… (unchanged since F12), `tests/test_jobwatch.py` b146bcb9….
- Full suite: **Ran 66 tests, OK**, `suite_exit_code=0`.
- Step-1 reproduction on the patched code: `[error] write refused: …\Temp\js2-repro-zbio\run.json resolves to C:\Users\Prathamesh P\AppData\Local\Temp\js2-repro-zbio\run.json, outside the project folder …`,
  then `[error] status=error step=run; files written before the refusal: none`, and **`repro_exit_code=2`**. `ls` of the temp folder shows it **empty**.
- Observed: the 8.3 short name `PRATHA~1` in the input was expanded to the long name `Prathamesh P` in the resolved path. This bears on review/PLAN.md step-7 candidate (c).
- No `state/`, `runs/` or `traces/` folder was left in the project afterwards.

## F23. Step 6 decision: REVISE (2026-11-10, Prathamesh)
- The decision, evidence, revision, accepted scope extras (`9051e0d`, F18 setUp move) and follow-ups (reads through `check_read`, an `--approve` CLI flag) are in `review/06-decision.md`.
  Claude Code transcribed it from Prathamesh's message, signed "Prathamesh, 2026-11-10".
- My take: The fix worked, but the agent still sent the request before checking whether it was allowed to save the result. A permission check after the action isn't really a permission check.

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

## F26. Decision on F25, and the revision applied (2026-11-10 ~09:08 EST)
- Prathamesh chose "Move its temp folder". In `tests/test_jobwatch.py`, `AllowList.test_refuses_redirect_off_host_and_writes_nothing` now uses `TemporaryDirectory(dir=ROOT/"state")`.
  The location is the only change, and no assertion changed. It still checks that an off-host redirect raises HostRefused and writes no files.
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
- My take: A passing suite tells me the cases I thought of are handled, not that the policy is safe. My tests check where a path points, not which file it is.

## F29. Commit 2 made and pushed (2026-11-10 09:18 EST) *(Claude Code)*
- `6dc2abb` "JS2 review: policy patch, revision, still-missed case", 17 files.
  - Code: `policy.py`, `jobwatch.py`.
  - Tests: `tests/test_jobwatch.py` (the two location-only moves) and `tests/test_revision_fetch.py`.
  - Review: every `review/` file except `_probe.txt`.
  - Logs: `FRICTIONAL.md` and `NOT-CHECKED.md`. Prathamesh's list did not name these two; Claude Code included them so that the pushed branch carries the logs and the step-7 NOT-CHECKED items.
- `git push -u fork prathamesh-p-js2-loop-tools-diff` created a new branch on `prpathak1/info-7375-prompt-engineering-for-generative-ai`.
- `git ls-remote fork refs/heads/prathamesh-p-js2-loop-tools-diff` → `6dc2abb0b5a8d4557e6947a415e17fe1814fc7d5`, equal to local HEAD (09:18:57 EST).
- This entry (F29) itself is not yet committed.

## F30. Loop build: two GATE gaps found before any test; both decided by Prathamesh (2026-11-10 ~09:28–09:30 EST)
- Gap 1: GATE section 7 names `seeded/SEEDED-openai-empty.json`, but the section 5 read list did not include `seeded/`. Prathamesh chose to add `seeded/` as read-only. It is recorded as **amendment A1**
  in GATE section 10 (09:30:10 EST), and the section 5 Read row is marked.
- Gap 2: no JS2 state existed, so the live run would be a baseline everywhere. Prathamesh chose to carry JS1's zoox state.

## F31. Tests written first, then run red (2026-11-10 09:30–09:33 EST) *(Claude Code)*
- `tests/test_loop.py`: 50 tests, each with an EXPECTED docstring, written before any of `adapters.py`, `loop.py` or `verify.py` existed. It fixes the interface (`run_loop`, `main`, `Ledger`, `check_url`,
  `normalize_url`, `Response`, `DNSFailure`, `raw_path`, `today`, `DEFAULT_BOARDS`, `adapters.parse/board_url/FormatChanged/ALLOWED_HOSTS`, `verify.py` exit codes). That choice is Claude Code's.
- Data added before the red run (not loop code):
  - `seeded/SEEDED-openai-empty.json` (`{"jobs": [], "apiVersion": "1"}`, with apiVersion copied from the real capture), plus `seeded/README.md` labelling it constructed;
  - `state/lever-zoox.json`: 227 IDs carried from JS1 `state/seen_ids.after-run3-2026-10-31.json` (SHA-256 54a6a3cd…), with a `carried_from` note.
- Red run by Claude Code: `demo/CLAUDE-DEV-01-loop-tests-red.txt`, `Ran 50 … FAILED (errors=56)`. Of these, 41 + 12 were `ModuleNotFoundError` (adapters, loop), 2 were `FileNotFoundError` (loop.py and verify.py sources),
  and H_9 failed with `read refused … seeded` (the policy did not yet allow it). No test was found to contradict GATE.
  Two interpretations are noted for Prathamesh: 410 is named `failed_http_410` (D-3) although the section 4 row shows `failed_http_404`; and verify.py has two checks beyond GATE section 7 (invented values, and a "finished" status with a failed board).

## F32. Implementation (2026-11-10 09:33–09:37 EST) *(Claude Code)*
- `policy.py`: `READ_DIRS` gains `"seeded"` (A1). That is the only change.
- `adapters.py` (new): `board_url` for the three GATE endpoints and `parse` to one posting shape. Greenhouse `content` is unescaped and tag-stripped; ids become str; `FormatChanged` covers not-JSON and wrong shape.
- `loop.py` (new): `run_loop` and the CLI (`run`, `seed-state`).
  - **Order of checks:** budgets are checked before every request, and every raw/meta path is permission-checked before every request.
  - **Repeat rule:** `Ledger`, with one retry, only for timeout, reset, 429 or 5xx. Retry-After is honoured up to 10 s, and above 10 s there is no retry. 404/410 fail without a retry; 401/403, a login-path redirect, or a format change escalate.
  - **Files:** every body is saved with a `.fetch.txt`. Per-board state is written atomically, with the previous snapshot archived under `state/history/`, and records come from `jobwatch.decide`. A JSONL trace goes under `traces/` and the report under `runs/<run_id>-<status>.json`.
  - **Reads and transports:** reads go through `policy.check_read`. `--approve` passes exact paths to `policy.check_write`. `--replay` is an offline transport for SEEDED runs.
- `verify.py` (new): imports none of the agent's modules. It recomputes counts and new IDs from the saved raw files and the previous snapshot with its own ID extractor, applies the empty and >50%-drop rule, and checks SHA-256 against `.fetch.txt`.
  Two checks go beyond GATE section 7: it flags invented values on failed boards, and a "finished" status with a failed board.

## F33. Claude Code's development runs after implementation (2026-11-10 09:37–09:40 EST) *(Claude Code)*
- 09:37:03: `test_loop.py` → `Ran 50 … OK` on the first implementation.
- Full suite → `Ran 119 … OK` (50 JS1 + 16 policy + 3 revision + 50 loop). It is saved as `demo/CLAUDE-DEV-02-full-suite.txt` (09:38:46–09:38:50 EST).
- Wrong versions were planted one at a time in scratchpad copies (the real folder was untouched). The results are in `BOUNDARY-TESTS.md`.
  - W3, W4, W5 (two variants), W6, W7 and W8 were all caught.
  - A first W7 variant (removing only the `count == 0` branch) was **not caught**. It is not a real wrong version, because the >50% drop rule still fails 3 → 0. The proper W7 (both checks removed) was caught.
- A defect was found in the committed patch `6dc2abb`. `jobwatch.WRITTEN` is process-wide, so in the in-process test V2 the refusal message listed judge-log files written by an earlier test. It was not fixed, and is proposed as NOT-CHECKED item 8.
- The seeded demo (b) was dry-run **only in a scratchpad copy** (09:40:02).
  - `seed-state` gave 826 IDs.
  - The SEEDED run gave `finished`, exit 0, `ok_empty`, with no network.
  - verify.py gave **FAIL**: "posting count is 0 but the previous snapshot had 826 ids", `verify_exit=1`.
  - The copy was deleted. The live run (a) was **not** run or dry-run.
- `BOUNDARY-TESTS.md`: B1–B13 plus 4 extra cases and the wrong-version table. Its "Actual" column comes from Claude Code's dev run and says so.
- NOT-CHECKED.md: items 5–9 were added under "Proposed by Claude Code … NOT yet confirmed by Prathamesh".
- Nothing is committed.

## F34. Decisions; then the WRITTEN defect in Prathamesh's accepted patch 6dc2abb was fixed test-first (2026-11-10 09:48–09:49 EST)
- Prathamesh accepted the following:
  - 410 is reported as `failed_http_410`;
  - verify.py's two checks beyond GATE section 7;
  - NOT-CHECKED items 5–9, which were moved under a "CONFIRMED by Prathamesh (Tue Nov 10 09:48:38 EST 2026)" heading.
- Prathamesh also ordered: fix the WRITTEN defect before the demo runs, test first, with no other change.
- **This is a defect found in the patch Prathamesh had accepted in step 6** (committed as `6dc2abb`). `jobwatch.WRITTEN` was never reset, so a refusal reported files written by earlier `main()` calls
  in the same process. Neither the review packet nor its tests caught it, because every CLI test ran one call per process. It was found by Claude Code in `demo/CLAUDE-DEV-02-full-suite.txt` (F33).
- *(Claude Code)* The test came first: `tests/test_written_reset.py` W_1 (SHA-256 584dd0df…, the same hash as recorded in `demo/CLAUDE-DEV-03-written-red.txt`; jobwatch.py after the fix: b04377ec…). Call A writes inside the project; calls B and C are then refused, and each must report "none".
- *(Claude Code)* The red run (Claude Code's, before the fix), `demo/CLAUDE-DEV-03-written-red.txt`: `FAILED (failures=2)`. B and C each listed A's `a-out.json` and `a-state.json`.
- *(Claude Code)* The fix is one line in `jobwatch.main()`, `WRITTEN.clear()` at the start. The diff is `demo/CLAUDE-DEV-04-written-fix.diff`, and nothing else changed.
  Claude Code's run at 09:49:11 EST: W_1 OK, and the full suite **Ran 120 … OK**. NOT-CHECKED item 8 is marked FIXED and kept for the record.
- My take: I accepted a patch that still had a bug. "Accept" meant the evidence I looked at was good, not that the code was correct.

## F35. Prathamesh's full-suite run (2026-11-10 ~09:51 EST)
- Run via `!`, output in `demo/00-my-full-suite.txt` (SHA-256 59f866db…): **Ran 120 tests, OK**, `suite_exit_code=0`.

## F36. LIVE run by Prathamesh: the deliberate failure, as predicted (2026-11-10 09:52:31–09:52:40 EST)
- Run via `!`, output in `demo/01-live-run.txt` (SHA-256 983c253d…). Code hashes: loop.py 7ba1890d…, adapters.py a50714fb…, policy.py d7e0a03b…, verify.py 5fd58d78…, jobwatch.py b04377ec….
- `status=incomplete exit=3`, `requests=4/6`, `seconds=8.757/120`. Report: `runs/20261110T095231-e3cc74-incomplete.json`. Trace: `traces/20261110T095231-e3cc74.jsonl` (14 lines).
  - `lever-zoox`: ok, 234 postings, **31 new** against the 227 IDs carried from JS1 run 3 (2026-10-31); 24 IDs have gone. All 31 records are `not_relevant`, with 0 `needs_human`.
  - `greenhouse-cloudflare`: ok, 466 postings, 0 new (baseline).
  - `ashby-openai`: ok, 826 postings, 0 new (baseline).
  - `greenhouse-cloudflare-js2-does-not-exist`: **failed_http_404**, 1 attempt (no retry), why "HTTP 404: bad board name or removed board; no retry (GATE section 4)". There is no count, ID or record. The 38-byte 404 body is saved as `.body` evidence.
  - This matches the GATE D-12 prediction (404, no retry, the other three processed, `incomplete`/3).
- Escalations: none. Refused repeats: none.
- verify.py on that report: **PASS**, `verify_exit_code=0`.
- This was the first real exercise of `loop.urllib_transport` (NOT-CHECKED item 5). It handled real 200s and a real 404. Timeouts, resets and DNS failures have still only been exercised with fakes.
- `raw/2026-11-10/` is now 47 MB: the morning's three captures plus this run's three bodies and the 404 body.
- My take: 31 real new Zoox postings is the first real change the agent has caught, after JS1 saw none. All 31 being "not relevant" fits an entry-level network student at Zoox, but it proves the watch works, not that the filter finds good jobs.

## F37. SEEDED "finished but wrong" demo by Prathamesh, caught by verify.py (2026-11-10 09:53:54–09:53:55 EST)
- Run via `!`, output in `demo/02-seeded-finished-but-wrong.txt` (SHA-256 96b24383…). **SEEDED**: a constructed response, not a real board response. No network was used (replay transport).
- `seed-state`: 826 IDs from the real `raw/2026-11-10/openai.json` (7cdd73d3…) went into `state/SEEDED/ashby-openai.json`.
- The SEEDED run with `seeded/SEEDED-openai-empty.json` (5e344d1d…) gave `*** SEEDED *** status=finished exit=0`, `ashby-openai ok_empty postings=0 new=0`. Report: `runs/SEEDED-20261110T095355-c5b9fa-finished.json`.
- verify.py gave **FAIL**: "ashby-openai: posting count is 0 but the previous snapshot had 826 ids…", `verify_exit_code=1`.
  The agent's clean "finished" was caught by the independent check, not by the agent's own report (GATE section 7, W7).
- Claude Code checked at 09:54:03 EST: the real `state/ashby-openai.json` still holds 826 IDs (label none). The SEEDED state `state/SEEDED/ashby-openai.json` now holds 0 IDs (label SEEDED), showing the "empty state" harm GATE section 7 describes, confined to `state/SEEDED/`.
- My take: The agent said "finished, exit 0" on an empty board, and only the separate checker said FAIL. "It stopped cleanly" and "it's right" are different questions, and the agent can't answer the second one about itself.

## F38. Pre-sign-off clean-up, privacy scan, README (2026-11-10 ~09:55–10:05 EST)
- FRICTIONAL: "My take:" lines kept only on F5, F6, F8, F18, F23, F28, F34, F36 and F37 (Prathamesh's list), and removed from 20 other entries. A note at the top lists them.
- BOUNDARY-TESTS.md: "Actual" now cites Prathamesh's run `demo/00-my-full-suite.txt` (120 OK) as primary, with Claude Code's `CLAUDE-DEV-02` as secondary.
  Claude Code parsed that file and found all 120 tests `ok`. The file is not valid UTF-8 ("résumé" was written in the console code page, byte 0xe9), so it was read with replacement characters.
  The wrong-version table is marked as Claude Code's runs only.
- Privacy scan of the JS2 folder (09:59:50 EST):
  - Résumés: the only one is `fixtures/resume.fictional.json` (`fictional: true`, `tanvi.kulkarni@example.com`, `(617) 555-0192`).
  - Emails: Prathamesh's own email address appears nowhere (searched for its local part and its domain). Outside `raw/`, the only addresses are posting text (`accommodations@zoox.com`) and test strings.
  - Credentials: no tokens or private keys.
  - **12 files contain the Windows account path `C:\Users\Prathamesh P` / `PRATHA~1`** (run reports, traces, review outputs). It was left as is, because these are evidence files.
- SOURCES.md: three dated rows added for Claude Code's and Prathamesh's work from 08:17 onward. The stale "approval pending" note was corrected.
- README.md drafted:
  - starting point, toolchain, the fresh-clone commands with the short-path note, and the REAL/SEEDED run table;
  - links to the artifacts (every relative link checked to exist);
  - checked properties with methods, "not checked", and a draft of the claims not made;
  - a blank "Signed / withheld" line and a driver's-seat table with "Why this part stays mine" left blank.
  - It lists four extra not-checked items, (a)–(d), as proposed and not yet confirmed.

## F39. "My take" lines inserted; provenance stated by Prathamesh (Tue Nov 10 10:17:42 EST 2026)
- Prathamesh's "My take:" texts were inserted verbatim into F5, F6, F8, F18, F23, F28, F34, F36 and F37. Each text was checked to be present character for character.
- Provenance, in Prathamesh's words (verbatim): "drafted by Claude (claude.ai chat) at my request; I reviewed them and edited them in my own words where I disagreed." This covers the nine "My take" lines and the "Why this part stays mine" lines for the README driver's-seat table.
- The "Why this part stays mine" lines are **not inserted yet**. Prathamesh asked to see the row mapping first, and the pasted list was cut off mid-line ("Board choice: Only I know which employers are").

## F40. NOT-CHECKED (b)–(d) confirmed; fresh-clone check run (2026-11-10 10:20–10:23:04 EST) *(Claude Code)*
- Prathamesh kept (b), (c) and (d). They became NOT-CHECKED items 10–12, with a dated "CONFIRMED by Prathamesh" heading. For (a), he asked for a real fresh-clone check.
- `C:\js2fc` did not exist beforehand (checked at 10:20:38). `git clone --branch prathamesh-p-js2-loop-tools-diff https://github.com/prpathak1/info-7375-prompt-engineering-for-generative-ai.git C:/js2fc`
  gave `clone_exit=0`: 4,506 files at `8960186`, with no path-length errors, and `git status` was clean.
- A first suite run in the clone was captured badly: `tail -4` showed the loop's printed lines, not the unittest summary, and `suite_exit` was `tail`'s exit code. It was re-run at
  10:22:03–10:22:06 with the output to a file: **`Ran 120 tests … OK`, `suite_exit=0`**, and the clone was still clean afterwards.
- Found by the comparison:
  - 41 of the 83 tracked JS2 files differ from the working copy **only** by CRLF vs LF (the files written by Python on Windows). Git stores LF, so a recorded hash of such a file
    (for example `jobwatch.py` b04377ec… working copy vs c6ef3c99… clone) matches only after normalization. The raw response bodies are byte-identical.
  - Run reports store **absolute** paths, so `verify.py` on a committed report reads the original folder on this machine. It was not run in the clone. This is reported to Prathamesh and not added to NOT-CHECKED.
- README: the "not run" note was replaced with the clone result; former item (a) was removed; items 10–12 were added under Not checked; the "claims not made" fresh-clone line was narrowed.
- `C:\js2fc` was left in place, as Prathamesh asked. Nothing was committed.

## F41. Final texts, sign-off, final checks, and a privacy fix that rewrote history (2026-11-10 10:27–10:29:40 EST) *(Claude Code)*
- Prathamesh's 14 "Why this part stays mine" lines and his sign-off sentence were inserted verbatim into README.md. A string-for-string check found all of them present.
  Their provenance is recorded in SOURCES.md in his words: drafted by Claude in claude.ai chat at his request, then reviewed and edited by him where he disagreed.
- The README header no longer says "pre-sign-off draft"; it says signed by Prathamesh on 2026-11-10.
- NOT-CHECKED items 13 (line endings) and 14 (absolute paths in run reports) were added from the F40 fresh-clone findings, as confirmed by Prathamesh (10:27:46 EST).
- Final suite run by Claude Code at 10:28:05 EST: **Ran 120 tests … OK**, exit 0.
- **Privacy finding, caused by Claude Code.** The final privacy scan flagged FRICTIONAL.md itself. A line in F38 named the two search patterns of the earlier scan, which together reconstruct
  Prathamesh's university email address. That line was in the already-pushed backup commit `8960186`. It was reworded so that it names neither pattern.
  Prathamesh chose to rewrite history. `8960186` and the final changes are folded into one commit, "JS2: sign-off and submission", on top of `6dc2abb`, and the fork branch is force-pushed.
  `8960186` is then no longer on the branch, although GitHub may still serve it by hash for a while. The fresh-clone check in F40 ran against `8960186`. The files changed after it are the logs and the README.
