# Boundary tests: GATE.md B1–B13, plus the extra cases the brief asks for

- **"Predicted (GATE)"** is copied from GATE.md section 9 (approved 2026-11-10 08:17:25 EST). It was written before any test existed.
- **"Test"** names the test that pins the case:
  - `tests/test_policy.py` was written before the policy patch (review step 2);
  - `tests/test_revision_fetch.py` was written before the step-6 revision;
  - `tests/test_loop.py` was written before the loop code.
- **"Actual"**, primary source: **Prathamesh's own run** `demo/00-my-full-suite.txt` (run via `!`, 2026-11-10 09:51:45–09:51:49 EST, **`Ran 120 tests … OK`**, `suite_exit_code=0`).
  Every test named below is reported `ok` there (checked by Claude Code by parsing that file at ~09:57 EST; all 120 parsed tests were `ok`).
  Secondary source: Claude Code's development run `demo/CLAUDE-DEV-02-full-suite.txt` (09:38:46–09:38:50 EST, `Ran 119 … OK`, before `tests/test_written_reset.py` existed). It agrees on every row.

| # | Case | Request | Predicted (GATE) | Test | Actual (Prathamesh's run `00-my-full-suite.txt`; Claude Code's `CLAUDE-DEV-02` agrees) |
|---|---|---|---|---|---|
| B1 | Host outside the allow-list (`https://example.com/jobs`) | GET | refused, run `error` | `test_loop.Permissions.test_H_2_B1_B2_check_url_refusals` (HostRefused); run level: `test_loop.Exits.test_E5_error_exit_2_off_host_final_url_stops_run_and_lists_written` (final URL `https://evil.example/x`) | ok: HostRefused. The run ended `error`, exit 2, with 2 calls and board 3 never requested |
| B2 | Lookalike host (`api.lever.co.evil.example`) | GET | refused | `test_loop.Permissions.test_H_2_B1_B2_check_url_refusals`; also JS1 `test_jobwatch.AllowList` | ok: HostRefused |
| B3 | Sibling-prefix root (`../js2-loop-tools-diff-evil/x.json`) | write | refused | `test_policy.PolicyWriteBoundaries.test_P1_B3_sibling_prefix_root` | ok: PermissionRefused |
| B4 | Sibling-prefix folder (`raw-evil/x.json` inside ROOT) | write | refused (not a writable folder) | `test_policy…test_P2_B4_sibling_prefix_folder`; run level: `test_loop.Permissions.test_H_4_W3_sibling_prefix_dir_refused_before_any_request` (`state-evil-*`) | ok: refused. Run level: `error`, exit 2, **0 requests**, folder not created |
| B5 | Directory **junction** (`mklink /J`) under `raw/` pointing outside ROOT. *A true symlink needs admin or Developer Mode on this machine (`mklink /D` refused on 2026-11-10, FRICTIONAL F8), so a true-symlink escape is **not tested**.* | write | refused | `test_policy…test_P6_B5_junction_escape`; run level: `test_loop.Permissions.test_H_5_W4_junction_raw_dir_refused_before_any_request` | ok: refused; nothing landed in the target. Run level: `error`, exit 2, 0 requests |
| B6 | `..` escape (`raw/../../js1-contract-and-watch/x`) | write | refused | `test_policy…test_P3_B6_dotdot_escape` | ok: PermissionRefused |
| B7 | `fixtures/resume.fictional.json` | **read** | allowed | `test_policy.PolicyReadBoundaries.test_R1_B7_read_fixture_allowed` | ok: allowed; returned the resolved path |
| B8 | `fixtures/resume.fictional.json` | **write** | refused (readable, not writable) | `test_policy…test_P7_B8_inside_project_not_writable` (also `GATE.md`, `jobwatch.py`) | ok: PermissionRefused for all three |
| B9 | New file `raw/2026-11-10/x.json` | write | allowed | `test_policy…test_P10_B9_new_file_in_writable_folders_allowed` (raw/, state/, runs/, traces/) | ok: allowed; nothing written |
| B10 | Overwrite an existing `raw/2026-11-10/zoox.json` without `--approve` | write | refused, approval required | `test_policy…test_P8_B10_overwrite_evidence_needs_approval`; run level: `test_loop.Permissions.test_H_8_approve_only_exact_path` | ok: ApprovalRequired. Run level: `error`, exit 2, **0 requests**, file unchanged |
| B11 | Same as B10, with `--approve raw/2026-11-10/zoox.json` | write | allowed | `test_policy…test_P9_B11_overwrite_with_exact_approval`; run level: `test_loop…test_H_8_approve_only_exact_path` | ok: allowed **only** for the exact path. Approving a different path is still refused |
| B12 | Absolute path outside the project (scratchpad or `C:\Windows\...`) | write | refused | `test_policy…test_P4_B12_absolute_outside_temp`, `…test_P5_B12_absolute_outside_system`; CLI: `test_policy.CliWritesOutsideProject.test_C1…C3`; fetch: `test_revision_fetch…test_V1`, `…test_V2` | ok: refused. CLI exit 2 with nothing written; `fetch` makes **0 requests** |
| B13 | Method other than GET | request | refused (no code path; static test) | `test_loop.Permissions.test_H_6_B13_static_no_send_paths`; JS1 `test_jobwatch…test_source_has_one_get_and_no_send_paths` | ok: no POST/PUT/PATCH/DELETE, no credential headers or `smtplib`; every `method=` is `"GET"`; one `urlopen(` call site |

## Extra cases (not numbered in GATE section 9)

| Case | Request | Predicted | Test | Actual (Prathamesh's run `00`; Claude Code's `CLAUDE-DEV-02` agrees) |
|---|---|---|---|---|
| Read outside the project (a real temp file) | read | refused | `test_policy…test_R2_read_outside_refused` | ok: PermissionRefused |
| The loop reads its résumé from outside the project (step-6 follow-up: reads go through `check_read`) | read | run `error`, exit 2, 0 requests, message "read refused" | `test_loop.Permissions.test_H_7_reads_go_through_check_read` | ok |
| `seeded/` is readable but not writable (GATE amendment A1) | read / write | read allowed, write refused | `test_loop.Permissions.test_H_9_seeded_folder_is_readable_not_writable` | ok |
| Off-host redirect from each of the three allowed hosts (W8) | GET | HostRefused before following | `test_loop.Permissions.test_H_3_W8_redirect_handler_refuses_off_host_for_all_three` | ok for all three hosts |

## Wrong versions planted to check the tests catch them (Claude Code, scratchpad copies only, 2026-11-10 ~09:38 EST)

*These results are Claude Code's only. Prathamesh did not re-run the planted wrong versions.*

| GATE # | Wrong version planted | Caught? | Caught by |
|---|---|---|---|
| W3 | `policy`: `str(r).startswith(str(root))` instead of the component comparison | caught | `test_P1_B3_sibling_prefix_root` |
| W4 | `policy`: `abspath(normpath(...))` instead of `realpath` | caught | `test_P6_B5_junction_escape`, `test_H_5_W4_junction_raw_dir…` |
| W5 | `loop`: 404 added to the retry list | caught | `test_P_1_404_no_retry`, `test_E2_…`, `test_E8_…` |
| W5 | `loop`: request budget check disabled (retries uncounted) | caught | `test_P_11_request_budget_never_exceeded_by_retries`, `test_E3_…`, `test_B_4_…` |
| W6 | `loop`: a run with a failed board reported as `finished` | caught | `test_E2_…`, `test_E8_…`, `test_P_1_…`, `test_P_8_…` |
| W7 | `verify`: both the empty-board and the >50%-drop checks removed | caught | `test_V_2_W7_seeded_empty_finished_run_fails`, `test_V_6_…` |
| W7 (first attempt) | `verify`: only the `count == 0` branch removed | **not caught**. This is not a real wrong version: the >50% drop rule still fails a 3 → 0 board | — |
| W8 | `loop`: the final-URL allow-list check removed | caught | `test_E5_error_exit_2_off_host_final_url…` |
