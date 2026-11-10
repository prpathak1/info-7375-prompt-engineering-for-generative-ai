# GATE: Job-Search Agent 2, The Loop, the Tools, and the Diff

> **Status: APPROVED by Prathamesh on Tue Nov 10 08:17:25 EST 2026** (time from `date`). D-1 to D-16 were approved as drafted, with no amendments.
> Drafted by Claude Code (Opus 5.5, CLI 2.1.322) on 2026-11-10 at about 08:10 EST, at Prathamesh's request. No JS2 code existed at approval.
> Each decision is marked **[D-n approved]**. Changes from here on go only through section 10 (Amendments). Nothing here
> describes a run. Every "will" is a promise the code and tests must keep.
> Starting point: JS1, `fall-2026/prathamesh-p/js1-contract-and-watch/` at commit `a4f7165`. JS1's CONTRACT.md
> (copied here unchanged) still governs the **record** rule. This GATE governs the loop, the tools and the permissions.

## 0. Scope in one line

One run is a bounded loop over a fixed list of public boards (3 real ones plus 1 deliberate failure). It makes
one GET per board (plus at most one retry), saves each raw response, computes new IDs and records against the
fictional résumé, and ends with exactly one exit status. A separate checker then verifies the result.

**[D-1 approved] Boards** (each was reached with one GET on 2026-11-10; see `raw/2026-11-10/`):

| Board | Platform | Endpoint | Postings on 2026-11-10 |
|---|---|---|---:|
| `zoox` | Lever | `https://api.lever.co/v0/postings/zoox?mode=json` | 234 |
| `cloudflare` | Greenhouse | `https://boards-api.greenhouse.io/v1/boards/cloudflare/jobs?content=true` | 466 |
| `openai` | Ashby | `https://api.ashbyhq.com/posting-api/job-board/openai` | 826 |

**[D-2 approved] The Claude judge stays off in the loop.** JS2 loops compute the **record** only. The JS1 `judge`
subcommand remains, but the loop never calls `claude -p`. The budgets below are about HTTP, and a model call
inside the loop would add a second budget that nobody asked for.

## 1. Exits

Every run ends in exactly one of four statuses. Each status writes `runs/<timestamp>-<status>.json` and prints a
one-line summary. **Stopping does not imply success.** A `finished` status means only "every planned board reached a terminal
outcome inside budget." It does not mean the result is right. Acceptance requires `verify.py` to PASS (section 7).

| Status | Exit code | When | Report must contain |
|---|---:|---|---|
| `finished` | 0 | Every planned board reached outcome `ok` or `ok_empty`, inside every budget | per-board outcome, posting count, new-ID count, records, requests used, seconds used, a reminder that `verify.py` has not run yet |
| `incomplete` | 3 | The loop reached its end, but at least one board ended `failed_*` or `escalated` | everything above, plus for each failed board: error type, HTTP status if any, attempts, and why it stopped (the policy rule it followed). The state of failed boards is untouched. |
| `budget_exhausted` | 4 | The next action would exceed a budget, so it was not taken | everything above, plus which budget ran out, the value at the moment it ran out, and the boards **not attempted** |
| `error` | 2 | A permission refusal, an internal fault, or a fault before any board was attempted | the refused action or the exception type and message, the step it happened at, and what had already been written. State writes stop at that point. |

**[D-3 approved]** Per-board outcomes are: `ok`, `ok_empty` (HTTP 200 with zero postings), `failed_http_<code>`,
`failed_timeout`, `failed_network`, `failed_parse`, `escalated`, and `not_attempted`. **[D-4 approved]** `ok_empty` counts
as finished, on purpose. That is the trap the "finished but wrong" demonstration in section 7 relies on. The agent does not
second-guess it. The independent checker catches it.

## 2. Budgets

**[D-5 approved]**

| Budget | Value | Enforced how |
|---|---:|---|
| Max boards per run | **4** (3 real + 1 deliberate failure) | A board list longer than 4 is refused before any request. Exit `error`. |
| Max HTTP requests per run | **6** (4 first attempts + 2 retries) | The counter is checked **before** each request. If the next one would exceed it, exit `budget_exhausted`. |
| Max wall-clock seconds per run | **120** | Checked before each request. Per-request timeout is **30 s**, so one request cannot pass the cap by more than 30 s. |

**Who may change them: only Prathamesh, by a dated amendment to this table** (date, old value, new value, reason), in the
same style as JS1 CONTRACT.md amendments. **[D-6 approved]** The code reads the values from constants, and a test parses this
table and fails if the constants and this table disagree. That way Claude Code cannot change a budget silently in the code.
A command-line flag can only **lower** a budget, never raise it.

## 3. Repeat rule

**[D-7 approved]** *The same action* means the same `(method, normalized URL)` within one run. The URL is normalized like this:
scheme and host lowercased, default port dropped, query parameters sorted, and no fragment.

- A second request for the same action is **refused and not sent**, unless it is the single retry allowed by section 4.
  A refused repeat is logged as an observation and does not count against the request budget, because nothing was sent.
- Each action gets at most **one** retry. A retry counts against the request budget.
- A board listed twice in the input is collapsed to one before the loop starts, and the collapse is logged.
- Writing a raw file whose path already exists (same board, same day) is refused, as in JS1. Overwriting it needs approval (section 5).

## 4. Error policy

**[D-8 approved]** The rationale for the one bounded retry: timeouts, 429 and 5xx responses are often transient on public APIs, so one retry
is cheap. More than one retry hammers a free endpoint and burns a 6-request budget. Nothing else is retried, because a
retry cannot fix a wrong name, a changed format, or a policy violation.

| Error type | Action | Board outcome | Run effect |
|---|---|---|---|
| Host outside allow-list, off-host redirect, non-https, userinfo, non-443 port | **Stop the whole run.** No retry. | — | `error` |
| Path or permission refusal (section 5) | **Stop the whole run.** No retry. | — | `error` |
| Timeout (>30 s), connection reset | **One retry** after 2 s | `failed_timeout` / `failed_network` if the retry also fails | continue → `incomplete` |
| HTTP 429, 500, 502, 503, 504 | **One retry**, after `Retry-After` if it is ≤10 s, otherwise 2 s. If `Retry-After` >10 s, no retry. | `failed_http_<code>` | continue → `incomplete` |
| HTTP 404 / 410 (bad board name) | **No retry** | `failed_http_404` | continue → `incomplete` |
| HTTP 401 / 403, or a redirect to a login page on an allowed host | **No retry. Human escalation.** The agent never logs in. | `escalated` | continue → `incomplete` |
| HTTP 200 but not JSON, or JSON without the platform's expected shape | **No retry. Human escalation** (the format may have changed) | `escalated` (raw body still saved as evidence, marked unparsed) | continue → `incomplete` |
| DNS failure | **No retry** (a retry in 2 s will not fix it) | `failed_network` | continue → `incomplete` |
| Budget would be exceeded | Do not take the action | remaining boards `not_attempted` | `budget_exhausted` |
| Any other exception, or a state write failure | **Stop** | — | `error` |

**Human escalation** means an entry in the report's `escalations` list with the evidence path. The agent never pauses for input and never
tries to fix the problem itself. Prathamesh reads the list after the run. **No value is ever invented.** A failed board reports no
count, no IDs and no records, and its previous state is left as it was.

## 5. Permission policy (enforced in code, not prompts)

**[D-9 approved] Hosts.** `api.lever.co`, `boards-api.greenhouse.io`, `api.ashbyhq.com`. Only https on port 443, with no userinfo.
The allow-list is checked again on every redirect before it is followed (as in JS1). The only method is **GET**.

**[D-10 approved] Folders.** `ROOT` = this folder, `js2-loop-tools-diff/`, resolved once at start-up.

| Request | Allowed paths (after full resolution) | Everything else |
|---|---|---|
| Read | `fixtures/`, `raw/`, `state/`, `prompts/`, `GATE.md` | refused |
| Write (new file) | `raw/`, `state/`, `runs/`, `traces/` | refused |
| Write that needs Prathamesh's approval | overwriting or deleting any existing file under `raw/` (evidence); deleting or resetting `state/` | refused unless the run was started with `--approve <exact relative path>` for that path |

- **Writes outside the project folder are refused.** So are writes inside it but outside the writable folders, such as `jobwatch.py`, `GATE.md`, `fixtures/` and `tests/`.
- **[D-11 approved] How paths are checked.** The policy resolves the path fully (`os.path.realpath`, which follows symlinks and junctions;
  for a file that does not exist yet, it resolves the parent and then appends the name). It then compares path **components** with
  `Path.is_relative_to` after `os.path.normcase`. It never compares string prefixes. This defeats `..` escapes, the
  sibling-prefix trick (`raw-evil/` beside `raw/`, or `js2-loop-tools-diff-evil/` beside the root), and symlink or junction escapes.
- **Never:** apply, email, message, post, log in, or send credentials. There is no POST/PUT/PATCH/DELETE, no `Authorization` or `Cookie`
  header, and no `smtplib`. A static test checks the source for all of these. The agent opens no URL that is not a board endpoint.

## 6. The deliberate board failure

**[D-12 approved]** The fourth board is the Greenhouse slug **`cloudflare-js2-does-not-exist`**. Predicted before any request: HTTP **404**,
no retry (section 4), board outcome `failed_http_404`, the other three boards still processed, and run status **`incomplete`** (exit 3).
If the real response differs from this prediction (for example, 200 with an empty list), the actual response is reported as observed, and
the prediction is not edited after the fact.

## 7. The "finished but wrong" case and the independent check

**[D-13 approved] The case.** This is a day-2 run where the `openai` board returns HTTP 200 with `{"jobs": [], ...}`. The agent counts zero postings,
reports **zero new jobs**, writes state as an empty set, and exits **`finished` (0)**. Each step is "correct" on its own terms, but the
result is wrong. An empty board on a board that had 826 postings yesterday is almost certainly an outage or a format change, not
zero hiring. Worse, the empty state makes the next real run report all 826 as "new".
Unless a real endpoint returns this naturally, the empty response is a **SEEDED** local fixture (`seeded/SEEDED-openai-empty.json`), injected
through the fetcher with no network involved, and it is labeled SEEDED in its filename, the trace and the README.

**The independent check: `verify.py`.** It **does not import** the loop or `jobwatch.py`, and it **does not read the agent's run report as truth**.
It reads only `raw/<day>/*.json`, the `.fetch.txt` files and the previous state snapshot, using its own small per-platform ID extractor. It then:
1. recomputes, from raw data, each board's posting count and new-ID count, and FAILs if the agent's report disagrees;
2. FAILs any board whose posting count is 0 while the previous snapshot had at least 1, or whose count fell by more than **50%** **[D-14 approved]**;
3. FAILs if a raw file's SHA-256 does not match its `.fetch.txt`.

Exit 0 means PASS, and 1 means FAIL with the reasons. The README reports the agent's status and verify.py's verdict side by side.

## 8. Wrong versions the tests must catch

**[D-15 approved]**

| # | Wrong version (plausible) | Caught by |
|---|---|---|
| W3 | **Prefix check.** `str(p).startswith(str(ROOT))` or `startswith(ROOT/"raw")`. This accepts `js2-loop-tools-diff-evil/x` and `raw-evil/x`. | Boundary tests B3 and B4 |
| W4 | **Lexical check without resolving.** `normpath` and then compare. This accepts a junction or symlink under `raw/` that points outside. | Boundary test B5 |
| W5 | **Unbounded or uncounted retry.** It retries a 404, retries more than once, or does not count retries against the request budget. | A fake fetcher counts calls: 404 means exactly 1 call; 503 then 503 means exactly 2 calls; budget 6 is never exceeded |
| W6 | **Status conflation.** Any run that reaches the end of the loop returns `finished`/0, even if a board failed. | The deliberate-failure test asserts `incomplete`/3 |
| W7 | **Empty means success, trusted** (section 7). | A verify.py test on the SEEDED empty fixture asserts FAIL |
| W8 | **Allow-list on the first URL only.** A redirect to another host is followed. | A redirect test, kept from JS1 and extended to all three hosts |

(JS1's W1 and W2, about uncited justification and verdicts attached to the wrong posting, stay covered by the inherited tests.)

## 9. Predicted boundary cases (each expected result is stated before the test exists)

**[D-16 approved]** These are predictions, not results.

| # | Case | Request | Expected |
|---|---|---|---|
| B1 | Host outside the allow-list (`https://example.com/jobs`) | GET | refused, run `error` |
| B2 | Lookalike host (`api.lever.co.evil.example`) | GET | refused |
| B3 | Sibling-prefix root (`../js2-loop-tools-diff-evil/x.json`) | write | refused |
| B4 | Sibling-prefix folder (`raw-evil/x.json` inside ROOT) | write | refused (not a writable folder) |
| B5 | Directory **junction** (`mklink /J`) under `raw/` pointing outside ROOT. *A true symlink needs admin or Developer Mode on this machine (`mklink /D` was refused on 2026-11-10, FRICTIONAL F8), so a true-symlink escape is **not tested**.* | write | refused |
| B6 | `..` escape (`raw/../../js1-contract-and-watch/x`) | write | refused |
| B7 | `fixtures/resume.fictional.json` | read | allowed |
| B8 | `fixtures/resume.fictional.json` | write | refused (readable, not writable) |
| B9 | New file `raw/2026-11-10/x.json` | write | allowed |
| B10 | Overwrite an existing `raw/2026-11-10/zoox.json` without `--approve` | write | refused, approval required |
| B11 | Same as B10, with `--approve raw/2026-11-10/zoox.json` | write | allowed |
| B12 | Absolute path outside the project (scratchpad or `C:\Windows\...`) | write | refused |
| B13 | Method other than GET | request | refused (no code path; static test) |

## 10. Amendments

*(none yet. Format: date and time, old → new, reason, "Prathamesh".)*
