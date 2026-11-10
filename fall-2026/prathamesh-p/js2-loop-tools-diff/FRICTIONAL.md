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
