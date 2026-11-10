# Step 6: Decision on the policy patch

**Decision: REVISE**

## Evidence the decision rests on
- `review/05-my-runs.txt`: my own run on 2026-11-10 at 09:00 EST. 66 tests OK. The step-1 reproduction is now refused with exit code 2, and nothing is written outside the project.
- `review/03-patch.diff`: the patch.
- `review/03-behavior.md`: I checked the rows, including the four marked "reading only".
- `review/04-scope.txt`: the scope evidence.

## Reason
The core fix is correct and in scope. However, `fetch()` with an outside `--raw-dir` still sends the GET before it refuses the write
(03-behavior.md row B2). A permission check must happen **before** the action, not after it.

## Revision requested
In `fetch()`, check all three target paths with `policy.check_write` **before** the network request. Write a test for this **first**: an outside
`--raw-dir` must be refused with exit code 2 and make **zero** requests, using a fake `urlopen` that counts calls. Show the test failing, then
make the change. No other change.

## Scope extras accepted
- The base commit `9051e0d`, which was needed so the patch diffs against real JS1 code.
- The `Base.setUp` temp-folder move in `tests/test_jobwatch.py` (my F18 decision; no assertion changed).

## Follow-ups (not blockers; for the loop build)
- Route reads through `policy.check_read`.
- Add the `--approve` CLI flag from GATE.md section 5.

Signed: Prathamesh, 2026-11-10

*(Transcribed by Claude Code from Prathamesh's message of 2026-11-10; the decision and the wording of its content are Prathamesh's.)*
