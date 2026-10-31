# Not checked: running list for the README sign-off

Items here are things this work does **not** verify. They are carried into the README sign-off.

## Confirmed by Prathamesh

1. **Citation relation (added 2026-10-31, Prathamesh's instruction).** The validator checks that each citation's résumé side and posting side
   *exist* (the résumé value is at the named path, and the posting value is a verbatim substring of the named field). It does **not** check that
   the two sides refer to the same thing. Example from the 2026-10-30 smoke test: `target.soc_code: "15-1241"` paired with a
   sentence from `descriptionPlain` passes.

*Items 2–6 were proposed by Claude Code and confirmed by Prathamesh on 2026-10-31 (14:41 EDT).*

2. **Headless context.** Whether `claude -p` subprocesses load user-level Claude settings or memory despite the empty working directory (FRICTIONAL F16).
3. **Gate 2 matches phrases, not meaning.** "No security clearance required" is still a hit, even though it removes the requirement. Bare "clearance" is not a phrase, so "No clearance required"
   is not a hit (checked 2026-10-31; the CONTRACT §4 example was corrected the same day).
4. **Real fit.** Whether the rule (record) captures real fit. It deliberately ignores seniority (FRICTIONAL F13).
5. **Judge false negatives (v1 or v2).** All 20 experiment labels are "not fit", so a wrongly rejected fit posting could not be observed (experiment/REPORT.md limit (a)).
6. **Unicode whitespace.** Citation matching is byte-exact, so a non-breaking space quoted as an ordinary space is rejected (held-out #14). Not normalized, and not changed after held-out.
7. **Write confinement (added 2026-10-31, Prathamesh's instruction after the write-limit check).** `jobwatch.py` writes only to the paths given on the command line (`--raw-dir`, `--state`, `--out`, `--judge-log`). Confining writes to the project folder is **not enforced in code**. On 2026-10-31 at 14:55 EDT, a run with `--state`/`--out` in a scratchpad folder outside the project wrote both files (exit 0).
