# JS2: The Loop, the Tools, and the Diff (Prathamesh P.)

> Drafted by Claude Code (Opus 5.5, CLI 2.1.322) on 2026-11-10. **Status: signed by Prathamesh on 2026-11-10** (see "Signed or withheld").
> The "Why this part stays mine" column and the FRICTIONAL "My take:" lines were drafted by Claude (claude.ai chat) at Prathamesh's request.
> He reviewed them and edited them in his own words where he disagreed (SOURCES.md). The sign-off sentence is his.

**Starting point:** JS1, `fall-2026/prathamesh-p/js1-contract-and-watch/` at commit **`a4f7165`**. The JS1 folder is unchanged; `git diff a4f7165` on it is empty (`review/04-scope.txt`).
JS2 lives in `fall-2026/prathamesh-p/js2-loop-tools-diff/` on branch `prathamesh-p-js2-loop-tools-diff`.
**The rules, written before any code:** [GATE.md](GATE.md). It was approved by Prathamesh on 2026-11-10 at 08:17:25 EST, with one dated amendment (A1, 09:30:10 EST).
JS1's [CONTRACT.md](CONTRACT.md) still governs the record rule.

## Language, toolchain, exact commands

- **Language and libraries:** Python **3.13.1**, standard library only. No `pip install` is needed.
- **Other tools:** git 2.55.0.windows.3 on Windows 11 Home 10.0.26300, and Claude Code CLI 2.1.322. Claude Code was only the development assistant here; the JS2 loop never calls `claude -p` (GATE D-2).
- **The morning reachability GETs** used curl 8.21.0.

**Fresh clone.** On Windows, **clone into a short path such as `C:\js2fc`**. Other folders in this repository have paths that exceed the 260-character limit when the
clone sits deep in the tree. JS1 found this on 2026-10-31 ("Filename too long" from a 164-character temp prefix).

```bat
git clone --branch prathamesh-p-js2-loop-tools-diff https://github.com/prpathak1/info-7375-prompt-engineering-for-generative-ai.git C:\js2fc
cd C:\js2fc\fall-2026\prathamesh-p\js2-loop-tools-diff

:: 1. all tests (offline; no keys; about 4 s)
python -I -m unittest discover -s tests -v

:: 2. LIVE run: the four GATE boards (4 GETs, inside the 6-request budget), then the independent check
python -I loop.py run
python -I verify.py runs\<the new run id>-incomplete.json

:: 3. SEEDED "finished but wrong" demo (no network)
python -I loop.py seed-state --board ashby:openai --from-raw raw/2026-11-10/openai.json --state-dir state/SEEDED --label SEEDED
python -I loop.py run --board ashby:openai --replay ashby:openai=seeded/SEEDED-openai-empty.json --state-dir state/SEEDED --label SEEDED
python -I verify.py runs\SEEDED-<the new run id>-finished.json
```

- **Run from the project folder.** All reads and writes are confined to it by `policy.py`, and relative paths resolve against the current folder.
- **A new live run is not a replay.** It writes new files under `raw/`, `state/`, `runs/` and `traces/`, and it compares against the committed state, so its new-ID counts will differ from the run below.
- **Fresh-clone check (real, run by Claude Code on 2026-11-10, 10:20:48–10:22:06 EST):**
  - `git clone --branch prathamesh-p-js2-loop-tools-diff` of the pushed fork into `C:\js2fc` gave exit 0. It checked out 4,506 files at `896018698603…` (`8960186`, the pre-sign-off backup commit, later folded into the final commit by a history rewrite; see FRICTIONAL F41) with no "Filename too long" errors, and `git status` was clean.
  - In `C:\js2fc\fall-2026\prathamesh-p\js2-loop-tools-diff`, `python -I -m unittest discover -s tests` gave **`Ran 120 tests … OK`**, exit 0. It left no changed or untracked files.
  - The saved raw bodies hash the same as in `SHA256SUMS` (zoox 7ebca330…, cloudflare 6c092ea5…, openai 7cdd73d3…).
  - *Only the test suite was run in the clone.* The live and SEEDED commands were not run there.
  - *Two facts this check found:*
    1. **41 text files differ from the working copy by line endings only.** These are the files written by Python on Windows, such as `jobwatch.py`, the `demo/` and `review/` outputs, state, traces and `.fetch.txt`. Git stores them with LF, so a hash of one of them recorded in the logs (for example `jobwatch.py` b04377ec… in `demo/00`) matches the clone only after CRLF → LF. The raw response bodies are byte-identical.
    2. **Run reports store absolute paths** (`C:\info7375\…`). `verify.py` on a committed report therefore reads the original folder on this machine, and would find the files missing on another machine. verify.py was not run in the clone.
  - `C:\js2fc` was left in place, as Prathamesh asked.

## What actually ran: REAL vs SEEDED

Every run below has a saved output file. "via `!`" means Prathamesh ran it himself in this Claude Code session, so the transcript marks it as user-run.

| # | When (EST, 2026-11-10) | Who | REAL or SEEDED | What | Result | Evidence |
|---|---|---|---|---|---|---|
| 1 | 08:07:13–08:07:17 | Claude Code (curl) | **REAL** | one reachability GET each: zoox (Lever), cloudflare (Greenhouse `?content=true`), openai (Ashby) | all HTTP 200: 234, 466 and 826 postings | [raw/2026-11-10/](raw/2026-11-10/) `zoox.*`, `cloudflare.*`, `openai.*`, `SHA256SUMS`; FRICTIONAL F4 |
| 2 | 09:51:45–09:51:49 | **Prathamesh** via `!` | REAL code run | full test suite | **`Ran 120 tests … OK`**, exit 0 | [demo/00-my-full-suite.txt](demo/00-my-full-suite.txt) |
| 3 | 09:52:31–09:52:40 | **Prathamesh** via `!` | **REAL** (live network) | `python -I loop.py run` (the four GATE boards), then `verify.py` | **`incomplete`, exit 3**, 4/6 requests, 8.757/120 s. zoox `ok` 234 postings, **31 new** against the 227 IDs carried from JS1's 2026-10-31 state (all 31 records `not_relevant`). cloudflare `ok` 466 and openai `ok` 826 (baselines, 0 new). `cloudflare-js2-does-not-exist`: **`failed_http_404`, 1 attempt, no retry, no counts** (as GATE D-12 predicted). verify.py: **PASS** | [demo/01-live-run.txt](demo/01-live-run.txt), [runs/20261110T095231-e3cc74-incomplete.json](runs/20261110T095231-e3cc74-incomplete.json), [traces/20261110T095231-e3cc74.jsonl](traces/20261110T095231-e3cc74.jsonl), `raw/2026-11-10/*.20261110T095231-e3cc74.*`; F36 |
| 4 | 09:53:54–09:53:55 | **Prathamesh** via `!` | **SEEDED** (constructed; no network) | state seeded with the 826 real openai IDs, then a run on `seeded/SEEDED-openai-empty.json` (`{"jobs": []}`), then `verify.py` | agent: **`finished`, exit 0**, `ok_empty`, 0 new. That is clean, and it is wrong. verify.py: **FAIL**, "posting count is 0 but the previous snapshot had 826 ids", exit 1 | [demo/02-seeded-finished-but-wrong.txt](demo/02-seeded-finished-but-wrong.txt), [runs/SEEDED-20261110T095355-c5b9fa-finished.json](runs/SEEDED-20261110T095355-c5b9fa-finished.json), [traces/SEEDED-20261110T095355-c5b9fa.jsonl](traces/SEEDED-20261110T095355-c5b9fa.jsonl), [seeded/](seeded/); F37 |

- **The SEEDED file is not a real OpenAI response.** The real openai state after run 3 still holds 826 IDs (`state/ashby-openai.json`). Only `state/SEEDED/` was emptied.
- **The review-packet runs by Prathamesh** are listed under "Review packet" below. Claude Code's own development runs are labelled `CLAUDE-DEV-*` in `demo/`, and are never the primary evidence for a claim.

## Artifacts

- **Rules:**
  - [GATE.md](GATE.md): exits, budgets, repeat rule, error policy, permission policy, the deliberate failure, the finished-but-wrong case, wrong versions W3–W8, and predicted boundary cases B1–B13. Amendment A1 is in its section 10.
  - [CONTRACT.md](CONTRACT.md): the JS1 record rule, unchanged.
- **Code:**
  - [loop.py](loop.py): the bounded loop and its CLI.
  - [adapters.py](adapters.py): Lever, Greenhouse and Ashby, mapped to one posting shape.
  - [policy.py](policy.py): the read/write policy.
  - [verify.py](verify.py): the independent checker; it imports nothing from the agent.
  - [jobwatch.py](jobwatch.py): JS1, with every write routed through the policy.
- **Tests:**
  - [tests/test_loop.py](tests/test_loop.py)
  - [tests/test_policy.py](tests/test_policy.py)
  - [tests/test_revision_fetch.py](tests/test_revision_fetch.py)
  - [tests/test_written_reset.py](tests/test_written_reset.py)
  - [tests/test_jobwatch.py](tests/test_jobwatch.py) (JS1; only two temp-folder locations changed, by Prathamesh's decisions F18 and F26)
- **Boundary-test table:** [BOUNDARY-TESTS.md](BOUNDARY-TESTS.md). It covers B1–B13 plus four extra cases, each with GATE's prediction, the test, and the actual result from Prathamesh's run. It also holds the wrong-version table.
- **Review packet** (one non-trivial Claude Code change: the write-confinement patch for JS1 NOT-CHECKED item 7):
  1. Reproduce the defect: [review/01-reproduce.txt](review/01-reproduce.txt) (Prathamesh: exit 0, two files written outside the project).
  2. Test before the patch: [review/02-test-red.txt](review/02-test-red.txt) (Prathamesh: C1–C3 FAIL, 12 ERROR because there was no policy yet). The test was committed alone as `b6c78ae`.
  3. Read the diff as a behavior change: [review/03-patch.diff](review/03-patch.diff), [review/03-behavior.md](review/03-behavior.md).
  4. Check scope: [review/04-scope.txt](review/04-scope.txt).
  5. Run the commands yourself: [review/05-my-runs.txt](review/05-my-runs.txt) (Prathamesh: 66 OK; the reproduction is now refused, exit 2, nothing written).
  6. Accept, revise or reject: [review/06-decision.md](review/06-decision.md) (**REVISE**: the check must come before the GET).
     - [review/06-revision-red.txt](review/06-revision-red.txt) is Claude Code's red run of the revision test.
     - [review/06-revision.diff](review/06-revision.diff) is the revision on its own.
     - [review/06-after-revision.txt](review/06-after-revision.txt) is Prathamesh's run: 69 OK.
  7. One case the test still misses: [review/07-still-missed.md](review/07-still-missed.md) (the NTFS hard link), [review/07-still-missed.txt](review/07-still-missed.txt) (Prathamesh's demo run), [review/07_hardlink_demo.py](review/07_hardlink_demo.py).

  The plan is [review/PLAN.md](review/PLAN.md). The packet was committed and pushed as `6dc2abb`.
- **Evidence folders:**
  - [demo/](demo/): Prathamesh's runs `00`–`02`, and Claude Code's `CLAUDE-DEV-01`…`04`.
  - [runs/](runs/): run reports.
  - [traces/](traces/): one JSON line per observation.
  - [raw/](raw/): every saved response, each with its `.fetch.txt` and SHA-256.
  - [state/](state/): per-board ID sets. Previous snapshots are in `state/history/`; JS1's zoox state is carried in `state/history/lever-zoox.before-20261110T095231-e3cc74.json`.
  - [seeded/](seeded/): the SEEDED fixture.
- **Logs:**
  - [NOT-CHECKED.md](NOT-CHECKED.md)
  - [FRICTIONAL.md](FRICTIONAL.md) (F1–F37)
  - [SOURCES.md](SOURCES.md)

## Sign-off

### Checked properties, named tests, method

Methods used:
- **(T)** Tests written by Claude Code from GATE.md **before** the code they test, and shown red first. Prathamesh accepted the review-packet test interface. He did not hand-review each loop test before the code existed.
- **(P)** Prathamesh's own run: [demo/00-my-full-suite.txt](demo/00-my-full-suite.txt) (120 OK) and the `review/` runs listed above.
- **(L)** Prathamesh's LIVE run (run 3) or SEEDED run (run 4), compared against the prediction GATE wrote before any request.
- **(M)** Wrong versions planted by Claude Code in scratchpad copies, to show that the tests fail on them. These were not re-run by Prathamesh.
- **(I)** The independent check: `verify.py` recomputes the results from saved files, without importing the agent.

| Property | Named tests / evidence | Method |
|---|---|---|
| Writes are confined to the project's writable folders (JS1 NOT-CHECKED item 7) | `test_policy` C1–C4, P1–P10; `review/01` vs `review/05` | T (red `review/02`), P, reproduction before and after |
| Every permission check happens **before** the action (no request, no write) | `test_revision_fetch` V1–V3; `test_loop` H_4, H_5, H_7, H_8 (each asserts 0 transport calls) | T (red `06-revision-red`), P |
| Reads go through `policy.check_read`; `seeded/` is readable but not writable | `test_loop` H_7, H_9; `test_policy` R1, R2 | T, P |
| Only the three GATE hosts, https on port 443, redirects re-checked (W8) | `test_loop` H_1, H_2, H_3, E5; JS1 `AllowList` | T, P, M (W8). The live run used only the three hosts (report `url` fields) |
| GET only, with no send or login paths (B13) | `test_loop` H_6; JS1 `test_source_has_one_get_and_no_send_paths` | T (static), P |
| Four exits with their GATE section 1 fields; stopping is not success (W6) | `test_loop` E1–E8 | T, P, M (W6), L (live `incomplete`/3; SEEDED `finished`/0) |
| Budgets equal the GATE table; checked before each request; flags can only lower them | `test_loop` B_1–B_5, E3, E4, P_11 | T, P, M (W5). L: 4/6 requests |
| Repeat rule: same normalized action refused, one retry at most, duplicate boards collapsed | `test_loop` R_1–R_4 | T, P |
| Error policy per type: one retry only for timeout, reset, 429 or 5xx; 404/410 not retried; 401/403, login or format change escalated | `test_loop` P_1–P_12 | T (fake transport), P, M (W5). L: real 404, 1 attempt |
| No invented values for failed or unattempted boards | `assert_no_invented_values` in E2, E3, P_1, P_9, P_10; `test_loop` V_7 | T, P, I. L: the live report's 404 board has no count keys |
| "Finished but wrong" is caught by an independent check, not by the agent (W7) | `test_loop` V_1 (verify imports nothing from the agent), V_2–V_7 | T, P, M (W7), **L+I** (run 4: agent `finished`, verify **FAIL**) |
| Adapters parse the real captures | `test_loop` A_1 (234 / 466 / 826 from the saved raw files), A_2, A_3 | T, P |
| State, new IDs and records; SEEDED label everywhere | `test_loop` A_4, A_5 | T, P. L: zoox 31 new against the carried JS1 state |
| A refusal reports only its own writes (the defect found in the accepted patch `6dc2abb`) | `test_written_reset` W_1 | T (red `demo/CLAUDE-DEV-03`), P |
| Path traps: sibling prefix (W3), lexical check (W4), `..`, junction | `test_policy` P1–P3, P6; `test_loop` H_4, H_5 | T, P, M (W3, W4) |
| JS1 behavior is kept (record rule, W1, W2, allow-list, validator) | `tests/test_jobwatch.py`, 50 tests | P |

### Not checked

From [NOT-CHECKED.md](NOT-CHECKED.md). Items 1–4 were added on Prathamesh's instruction; items 5–14 were proposed by Claude Code and confirmed by Prathamesh.
1. The Gate-1 title rule makes questionable calls on the new boards (for example, "RTL Design Engineer, Networking / NoC" → include). There are no hand labels for these boards.
2. A true symlink escape: it needs admin or Developer Mode here, so only a junction was tested.
3. A hard-link escape passes the policy. A plain write through one changed an outside file (`review/07-still-missed.txt`).
4. A check-then-write race.
5. The real network transport: only 200 and 404 have happened for real (run 3). Timeouts, resets and DNS failures have only happened against fakes.
6. verify.py is independent code, not independent data. It finds files through the report and trusts the agent's `.fetch.txt` hashes.
7. Login-redirect detection is a path heuristic.
8. *(fixed, kept for the record)* `jobwatch.WRITTEN` was process-wide. It is now checked by `test_written_reset` W_1.
9. 410 is reported as `failed_http_410` (D-3), not as the `failed_http_404` that the GATE section 4 row shows.

10. Whether each ATS's terms permit this use was not reviewed. Only public, unauthenticated endpoints were used, with one GET per board per run.
11. Whether each board's public API lists only open postings.
12. `demo/00-my-full-suite.txt` is not valid UTF-8 (the console wrote "résumé" in its code page). It was read with replacement characters.
13. Logged hashes of 41 text files match a fresh clone only after line-ending normalization: they differ from the working copy only in CRLF vs LF. The raw bodies are byte-identical.
14. Run reports store absolute paths, so `verify.py` on a committed report only works on this machine.

*(Items 10–14 were proposed by Claude Code and confirmed by Prathamesh. Former item (a), the fresh clone, was then checked; see "Fresh-clone check" above.)*

### Claims not made

- That the loop is correct in general. `finished` means only that every board reached a terminal outcome inside budget (GATE section 1).
- That any posting fits the persona. The 31 zoox records are rule outputs (`record`), all `not_relevant`, and JS2 makes no Claude judgments (D-2).
- That timeout, reset, 429, 5xx, 401/403, login-redirect and format-change handling has been seen against the real network. It has been seen only against fake responses.
- That the SEEDED result reflects a real OpenAI outage. It is a constructed body.
- That `policy.py` closes hard-link or race escapes, or that a true symlink escape is refused. It was not tested.
- That verify.py is independent of the agent's data. It is independent only of the agent's code.
- That the 404 behavior generalizes to other bad board names or other ATS platforms. One Greenhouse slug was tested live.
- That the planted wrong-version results were reproduced by Prathamesh. They are Claude Code's runs only.
- That the live and SEEDED commands work from a fresh clone, or that `verify.py` works on another machine. Only the test suite was run in the fresh clone (120 OK), and run reports hold absolute paths.

### Signed or withheld

I have read this README and I stand behind it. Signed, Prathamesh, 2026-11-10.

### Driver's seat (the loop and the review)

| Decision / work | What Claude did | What Prathamesh did | Why this part stays mine | Evidence |
|---|---|---|---|---|
| The rules before code (GATE) | Drafted GATE.md with 16 decisions; later found the `seeded/` read gap (A1) | Approved D-1 to D-16 (08:17:25) and decided amendment A1 (09:30:10) | Budgets decide how much the agent may do on my behalf, so only I change them. | GATE.md header and section 10; FRICTIONAL F9, F10, F30 |
| Boards | Picked cloudflare and openai, made one GET each, counted them | Named zoox; accepted the other two | Only I know which employers are worth watching for my situation. | `raw/2026-11-10/`; F4, F5 |
| Choosing the defect and reproducing it | Proposed JS1 NOT-CHECKED item 7; drafted the reproduction command | Chose the defect; ran the reproduction himself | I picked a gap from my own JS1 limits, so I had to see it happen myself before trusting any fix. | `review/PLAN.md`, `review/01-reproduce.txt`; F14 |
| Test before the patch | Wrote `tests/test_policy.py` from GATE, with predictions | Accepted the interface; ran it red | The test has to come from what I asked for, before Claude's code exists, or it just checks Claude's code against itself. | `review/02-test-red.txt`, commit `b6c78ae`; F12, F15 |
| Patch scope | Wrote the patch; **stopped** when it conflicted with "don't change tests"; wrote the diff, the behavior table and the scope file | Chose "enforce inside, move temps"; checked the behavior rows | It decides what the agent can touch on my machine, and I'm the one affected if it's wrong. | `review/03-*`, `review/04-scope.txt`; F17–F19 |
| Running the commands | Drafted each command; labelled its own runs `CLAUDE-DEV` | Ran steps 1, 2 and 5, `06-after-revision`, `07`, and demos `00`, `01` and `02` via `!` | If Claude runs the checks on its own change, I'm only taking its word. Running them myself is the evidence. | the `!` entries in the transcript; file headers saying "run by Prathamesh" |
| Accept, revise or reject | Presented the evidence and flagged the "GET before refusal" row | Decided **REVISE**, with reasons and follow-ups | Claude wrote the patch, so Claude can't be the one who accepts it. | `review/06-decision.md`; F23 |
| The revision | Test first and red; then the change; **stopped** at a second JS1-test conflict | Decided to move that test's temp folder | I decided "it works" wasn't enough. When the check happens mattered to me. | `review/06-revision-red.txt`, `review/06-revision.diff`; F24–F26 |
| A case the test still misses | Proposed candidates; demonstrated the hard link in a scratchpad copy | Picked the hard link; approved the claim (drafted by Claude in claude.ai chat); ran the demo | Claude can find gaps, but deciding which one matters and how to state it honestly is my call. | `review/07-*`; F27, F28 |
| The loop: tests and code | Wrote `tests/test_loop.py` before the code (red), then adapters, loop and verify; planted wrong versions | Decided A1 and the zoox carry; accepted the 410 naming and verify's extra checks; ran the suite | Claude wrote the code. I decide whether its tests check what GATE says, not just what the code happens to do. | `demo/CLAUDE-DEV-01`, `demo/CLAUDE-DEV-02`, `demo/00`, `BOUNDARY-TESTS.md`; F30–F33 |
| The deliberate failure (live run) | Predicted it in GATE D-12 before any request; built the command | Ran it; compared the result with the prediction | I predicted it before running it, so the result tests my understanding, not just the code. | `demo/01-live-run.txt`, `runs/…-incomplete.json`; F36 |
| Finished but wrong | Built the SEEDED fixture and verify.py; dry-ran in a scratchpad copy only | Ran the demo | A checker that shares the agent's code would share its mistakes. | `demo/02-seeded-finished-but-wrong.txt`; F37 |
| The defect in the accepted patch (WRITTEN) | Found it in its own dev run; fixed it test-first | Ordered the fix before the demos, and its order | Accepting the patch was my decision, so the bug that slipped through is mine to own and to get fixed. | `demo/CLAUDE-DEV-03`, `demo/CLAUDE-DEV-04`; F34 |
| What is not checked, and the sign-off | Proposed NOT-CHECKED items 5–14; ran the fresh-clone check (former item (a)); drafted "claims not made" | Confirmed items 5–14; asked for the fresh-clone check; approved "claims not made" as written; signed on 2026-11-10 | My name is on it, so I'm accountable. | NOT-CHECKED.md; README "Fresh-clone check"; this section; F40 |
