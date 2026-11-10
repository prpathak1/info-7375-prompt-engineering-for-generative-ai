# Step 3: the diff read as a behavior change (DRAFT by Claude Code, 2026-11-10 ~08:53 EST, for Prathamesh to check row by row)

Diff: `review/03-patch.diff` (`jobwatch.py`, the new `policy.py`, and `tests/test_jobwatch.py` setUp only), against commit `b6c78ae`.
"Covered by" names the test that pins the row. **"Reading only"** means no test checks that row; the claim comes from reading the code, and Prathamesh should check it against the diff.
"Refused" output on stderr is: `[error] write refused: <path> …` and then `[error] status=error step=<cmd>; files written before the refusal: none|[…]`, with exit code **2**.

## A. `jobwatch.py run` (the defect)

| # | Input | Before (JS1 code at b6c78ae) | After (patched) | Covered by |
|---|---|---|---|---|
| A1 | `--state` and `--out` both outside the project (`%TEMP%\…`) | writes both files; exit 0 (review/01-reproduce.txt) | refused, naming `--out` (checked first); **nothing written**; the raw file is not even read; exit 2 | C1 |
| A2 | `--out` outside, `--state` inside `state/` | writes both; exit 0 | refused, naming `--out`; state not created; exit 2 | C2 |
| A3 | `--state` outside, `--out` inside `runs/` | writes both; exit 0 | refused, naming `--state`; **`--out` is not written either**, because both are checked before any write | C3 (C3 does *not* assert the "out not written" part; **reading only** for that half) |
| A4 | both inside writable folders (`state/…`, `runs/…`) | writes both; exit 0 | unchanged: writes both; exit 0 | C4 |
| A5 | `--out` inside the project but outside a writable folder (`report.json` at ROOT, `fixtures/x.json`, `tests/x.json`) | written | refused; exit 2 | policy level P7 only; the CLI path is **reading only** |
| A6 | **Relative paths run from another folder**, such as running `python …\jobwatch.py run --out runs/x.json` from the parent folder | written relative to the cwd (outside the project) | refused, because relative paths resolve against the cwd. **New behavior: the CLI must be run from the project folder.** | **reading only** |
| A7 | `--state` path through a junction under `state/` that points outside | writes through the junction | refused (realpath follows the junction) | policy level P6 (junction under `raw/`); the `state/` variant is **reading only** |
| A8 | Overwriting an existing `state/seen_ids.json` (a normal second run) | allowed | unchanged: allowed (`state/` is not an approval folder) | C4 writes a new state file only; overwriting is **reading only** |

## B. `jobwatch.py fetch`

| # | Input | Before | After | Covered by |
|---|---|---|---|---|
| B1 | `--raw-dir raw` (normal) | one GET; writes `<board>.json`, `.headers.txt`, `.fetch.txt` under `raw/<date>/` | same three files, but all three paths are checked **before the first write**, and the text files are still written in text mode (CRLF on Windows, as before) | **reading only** (no live-fetch test) |
| B2 | `--raw-dir` outside the project | GET, then writes outside | the **GET still happens**, then refused before any write; exit 2. The policy check comes after the host check and the request, not before the request. | **reading only** |
| B3 | `raw/<date>/<board>.json` already exists | `FileExistsError` (refuses to overwrite) | unchanged: `FileExistsError` comes first, so `ApprovalRequired` never shows up in `fetch`. **There is no `--approve` CLI flag yet**, so overwriting through the CLI is impossible, even with approval. | **reading only** |
| B4 | Redirect to a non-allowed host | `HostRefused`, no files | unchanged | JS1 AllowList test (it still uses `%TEMP%`, and passes because the host check runs first) |

## C. `judge` and `run --judge claude`

| # | Input | Before | After | Covered by |
|---|---|---|---|---|
| C1j | default `--judge-log` | `judgments/` at ROOT | **`traces/judgments/`**. The default changed because `judgments/` is not a GATE-writable folder. | **reading only** |
| C2j | `--judge-log judgments` or any outside folder | written | refused **before any `claude -p` call**; exit 2 | **reading only** (JudgeHarness tests use a folder under `state/`) |

## D. Library callers (the coming loop, and the tests)

| # | Input | Before | After | Covered by |
|---|---|---|---|---|
| D1 | `run()`, `fetch()` or `claude_judge()` called from Python with an outside path | written | raises `policy.PermissionRefused`; it is an exception, not an exit code | the 14 JS1 tests now pass only with temp folders under `state/` (F18) |
| D2 | Any write's `.tmp` sibling | not checked separately | checked separately | **reading only** |

## E. What did NOT change

- **Reads are not enforced.** `--raw`, `--resume`, `--prompt` and the previous `--state` are still read from anywhere. `policy.check_read` exists (R1, R2) but is not called by `jobwatch.py`. GATE D-10's read rule is **not yet enforced** in jobwatch.
- GATE section 5 also says "deleting or resetting `state/` needs approval". There is no deletion code path, so nothing enforces it and nothing needs to.
- Host allow-list, record rule, judgment validator: unchanged (the diff does not touch them, and the 50 JS1 tests still pass).

*Prathamesh: tick, correct or strike each row after reading `review/03-patch.diff`.*
