# Review packet plan (APPROVED by Prathamesh, Tue Nov 10 08:17:25 EST 2026)

**Defect (proposed):** JS1 NOT-CHECKED item 7, which says writes are not confined. `jobwatch.py` writes wherever `--raw-dir`, `--state`, `--out` or `--judge-log` point.
On 2026-10-31 at 14:55 EDT, a run with `--state` and `--out` in a scratchpad folder wrote both files and exited 0.
**Change under review:** Claude Code adds `policy.py` (GATE.md section 5) and routes every write in `jobwatch.py` through it.
**Why it is non-trivial:** it touches every write site (`fetch`, `run`, `claude_judge`, `_write_atomic`) and introduces path resolution
with junction handling on Windows.

**Order matters.** The packet happens **before** the loop is built, against the copied JS1 `jobwatch.py`. That way the test is
provably written before the patch, and the git history shows it. That needs separate commits (test, then patch), each made only after you approve.

| # | Step | Evidence it leaves | Who |
|---|---|---|---|
| 1 | **Reproduce the defect** on the unpatched copy: `run --state <outside>/s.json --out <outside>/o.json` | `review/01-reproduce.txt`: `date`, the command, exit code, and `ls` of the outside folder showing both files | **Prathamesh runs it** (Claude Code drafts the command) |
| 2 | **Write the test before the patch**: `tests/test_policy.py` with B3, B4, B5, B6, B10 and B12, plus "`run()` with an outside `--state` is refused" | The test file in its own commit. `review/02-test-red.txt` shows it **failing** on unpatched code, with `date` | Claude Code drafts; Prathamesh approves the predicted results first and runs it red |
| 3 | **Read the diff as a behavior change** | `review/03-patch.diff` (`git diff`) and `review/03-behavior.md`: before/after for each input, such as "outside `--state`: before, it wrote the file and exited 0; after, PermissionRefused and exit 2, with no file" | Claude Code produces the diff and drafts the table. **Prathamesh checks each row against the code** |
| 4 | **Check scope** | `review/04-scope.txt`: `git diff --stat` (only `jobwatch.py`, `policy.py` and the new test), an empty diff for `tests/test_jobwatch.py` (no test weakened), and an empty diff for the JS1 folder | Claude Code gathers it; Prathamesh confirms |
| 5 | **Run the commands yourself**: the full suite and the step-1 repro again | `review/05-my-runs.txt`, pasted from **your** terminal (or run via `! <cmd>` in Claude Code so the transcript marks it as user-run), with `date` | **Prathamesh only** |
| 6 | **Accept, revise or reject** based on the evidence | `review/06-decision.md`: the decision, which evidence files it rests on, any revision requested, and a dated name | **Prathamesh only** |
| 7 | **One case the test still misses** | `review/07-still-missed.md`, with a demonstration if possible. Candidates: (a) an NTFS **hard link** under `raw/` pointing to an outside file (`realpath` cannot see hard links, and `mklink /H` needs no admin); (b) a check-then-write race (TOCTOU: a junction swapped in between check and write); (c) 8.3 short names such as `PRATHA~1`, versus long-path comparison | Claude Code proposes; **Prathamesh picks** and words the claim |
