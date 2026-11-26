# JS3: The Filter, the Tool, and the Score (Prathamesh P.)

- **Drafted by:** Claude Code (Opus 5.5, CLI 2.1.332) on 2026-11-25.
- **Status:** **SIGNED by Prathamesh on 2026-11-25** (see "Signed or withheld"; recorded 19:44 EST).
- **Who wrote what:** see `SOURCES.md`. The trust decisions, the "My take" lines and the "Why this stays mine" column below were drafted by Claude (claude.ai chat) at Prathamesh's request. He reviewed them and edited where he disagreed.
- **Due:** 2026-11-25 23:59 ET (extended by the TA; the brief says Nov 23; FRICTIONAL F1).
- **Starting point:** JS2, `fall-2026/prathamesh-p/js2-loop-tools-diff/` at commit **`f8a7af8`**. JS3 lives in `fall-2026/prathamesh-p/js3-filter-tool-score/` on branch `prathamesh-p-js3-filter-tool-score`, created from `f8a7af8`. The JS1 and JS2 folders are unchanged.
- **The rules, written before any filter code:** [FILTER.md](FILTER.md).
  - v0.1: 23 rules, approved 2026-11-25 18:46:08 EST.
  - v0.2 and v0.3: changed after measurement, each with a changelog entry.

## What this does

It takes the postings JS1 and JS2 collected, plus 2 boards added today, through a **written filter**:
- 1,994 unique postings from Zoox, Cloudflare, OpenAI, Fastly and Datadog;
- gates for title, work authorization, seniority and skills;
- every claim labelled `supported`, `contradicted` or `insufficient` with an exact quote.

On top of the filter:
- a **reject audit**;
- a **source-grounded shortlist**;
- a from-scratch **MCP-style tool server** (`score_posting`, read-only), used by a real client (Claude Code) and probed with a scripted client;
- the same probe method applied to a **third-party server** (the reference Filesystem MCP server 2.2.0);
- a **one-change-at-a-time score test** on 30 held-out labels.

The agent never applies, emails, messages or logs in. The tool server exposes nothing that sends or changes data outside this folder.

## Language, toolchain

- **Language and libraries:** Python **3.13.1**, standard library only. No `pip install`.
- **Other tools:** git 2.55.0.windows.3 on Windows 11 Home 10.0.26300; Claude Code CLI **2.1.332** (the development assistant, and the real MCP client in one recorded session).
- **For the third-party evaluation only:** Node **v24.19.0** and npx **11.17.0**, running `@modelcontextprotocol/server-filesystem@2.2.0`.
- **No API keys are needed.** Everything except the live board check and the two MCP client sessions runs offline from the files in this folder.

## Exact commands (from this folder)

```bat
:: Fresh clone: use a short path (long paths elsewhere in this repo exceed 260 characters on Windows; JS1 FRICTIONAL)
git clone --branch prathamesh-p-js3-filter-tool-score https://github.com/prpathak1/info-7375-prompt-engineering-for-generative-ai.git C:\js3fc
cd C:\js3fc\fall-2026\prathamesh-p\js3-filter-tool-score

:: 1. all tests: 120 inherited + 61 filter tests, offline
python -I -m unittest discover -s tests -v

:: 2. the filter over every posting except the 30 held-out ones (the audit population)
python -I filter.py run
:: ... and over all 1,994, which is allowed only because holdout/LABELS.json exists
python -I filter.py run --include-holdout --labels holdout/LABELS.json --out out/decisions.all.v0.3.jsonl

:: 3. samples (each refuses to overwrite an existing sample; they were drawn once)
python -I holdout.py --seed 20261125
python -I audit_sheet.py --seed 7375

:: 4. the grounded shortlist and the score test
python -I shortlist.py
python -I score_test.py

:: 5. my tool server: scripted probes, then a real client
python -I mcp_probe.py --probes probes/own.json --out transcripts/probe-own.jsonl -- python -I mcp_server.py
claude -p "<request>" --mcp-config probes/claude-mcp-config.json --strict-mcp-config --allowedTools mcp__js3__score_posting --output-format stream-json --verbose

:: 6. the third-party server, in a throwaway sandbox OUTSIDE the repo (see probes/make_fs_probes.py for its layout)
python -I probes/make_fs_probes.py <sandbox>
python -I mcp_probe.py --timeout 60 --probes probes/fs.json --out transcripts/probe-fs.jsonl -- npx -y @modelcontextprotocol/server-filesystem@2.2.0 <sandbox>\allowed

:: 7. privacy: scan (default) or redact the Windows user folder in transcripts and logs
python -I redact_paths.py
```

`probes/claude-mcp-config.json` holds an absolute path to `mcp_server.py`; edit it for your clone.

## What actually ran (2026-11-25, EST)

| Time | Run | Result | Evidence |
|---|---|---|---|
| 18:40:06 | Inherited tests | 120, OK | `demo/00-inherited-tests.txt` |
| 18:40:34 | **Live** loop, 3 new boards (one GET each, JS2 allow-list) | Fastly 50, Datadog 392, Tailscale 404 (no retry); `incomplete`, exit 3 | `demo/01-board-check-live.txt`, `runs/20261125T184034-139103-incomplete.json`, `raw/2026-11-25/` |
| 18:48:28 | Held-out sample, seed 20261125 | 30 postings (20 network titles + 10 others) | `holdout/HOLDOUT.json`, `LABEL-SHEET.md` |
| 18:50–18:52 | Filter tests red, then green | red: `No module named 'filter'`; then 172 OK | `demo/02`, `demo/03` |
| 19:01:47 | Filter v0.1 on 1,964 non-held-out postings | 1,963 reject, 1 accept | `out/decisions.v0.1.jsonl` |
| 19:03:44 | Audit sheet, seed 7375 | 30 random rejects, 5 near-threshold, 1 accept (only 1 existed) | `audit/AUDIT-SHEET.md`, `AUDIT-SAMPLE.json` |
| 19:10–19:11 | v0.2: tests red (3 fail), code, rerun | 9 changed rule, **0 changed outcome** | `demo/04`, `demo/05`, `demo/06-v01-to-v02-diff.txt` |
| 19:14:34 | Own server, 18 scripted probes | all refusals as designed | `transcripts/probe-own.jsonl`, `server-20261125T191434-2620.jsonl` |
| 19:14:55 | **Real client:** Claude Code 2.1.332 → `score_posting` | one call, success | `transcripts/claude-client-20261125T191455.jsonl`, `server-20261125T191459-33532.jsonl` |
| 19:17:00 | Filesystem server 2.2.0, 20 probes | boundary held on every escape probe | `transcripts/probe-fs.jsonl` (the 19:16 run is kept, marked INVALID) |
| 19:18:42 | Score test C0–C6 on held-out | see SCORE.md | `SCORE-RESULTS.md` |
| 19:26:49–19:27:38 | v0.3: tests red (2 fail), code, rerun | same 9 changed; **3 reject → flag** | `demo/07-v03-tests-red.txt`, `demo/08-v02-to-v03-diff.txt` |
| 19:27:52 | Score test re-run with C7 (v0.2 → v0.3) | C0–C6 unchanged; C7: reaches-me 2 → 4 | `SCORE-RESULTS.md`, `out/score_results.json` |
| 19:30:33 | Redaction of the user folder | 148 replacements in 8 files; rescan 0 | FRICTIONAL F27 |
| see F28 | Final full suite and privacy scan | see FRICTIONAL F28 | `demo/09-final-suite.txt` |

## Artifacts

| Brief item | File |
|---|---|
| Versioned filter, written first | [FILTER.md](FILTER.md) (v0.1 → v0.3, changelog with measurements) |
| Plan | [PLAN.md](PLAN.md) |
| Code | `postings.py`, `filter.py`, `holdout.py`, `audit_sheet.py`, `shortlist.py`, `score_test.py`, `mcp_server.py`, `mcp_probe.py`, `redact_paths.py`; inherited from JS2: `loop.py`, `adapters.py`, `policy.py`, `jobwatch.py`, `verify.py` |
| Tests | `tests/test_filter.py` (61, written before the code each time); inherited `tests/test_*.py` (120) |
| Held-out labels | [LABEL-SHEET.md](LABEL-SHEET.md), `holdout/HOLDOUT.json`, `holdout/LABELS.json` (with provenance) |
| Reject audit with verdicts and false friend | [audit/AUDIT.md](audit/AUDIT.md), `audit/AUDIT-SHEET.md`, `audit/AUDIT-VERDICTS.json` |
| Grounded shortlist, entailment example, abstention | [SHORTLIST.md](SHORTLIST.md), [GROUNDING.md](GROUNDING.md) |
| Tool server, transcripts, two evaluations, trust decisions | [TOOL-EVAL.md](TOOL-EVAL.md), `transcripts/`, `probes/` |
| Score inventory and one-change test | [SCORE.md](SCORE.md), [SCORE-RESULTS.md](SCORE-RESULTS.md) |
| Honest log | [FRICTIONAL.md](FRICTIONAL.md) |
| Sources and Claude's contributions | [SOURCES.md](SOURCES.md) |
| Inherited rules | [GATE.md](GATE.md) (JS2), [CONTRACT.md](CONTRACT.md) (JS1) |

## Driver's seat

| Decision | What Claude does | What Prathamesh does | Why this stays mine |
|---|---|---|---|
| FILTER rules | Drafted v0.1 and the code and tests; proposed wording | Approved all 23 rules; decided the v0.2 and v0.3 changes | The rules encode what I can accept as an F-1 student, and I carry that risk. |
| Labels | **This time Claude (claude.ai chat) drafted the 30 held-out labels** from the printed sheet; Claude Code built the blind sample | Reviewed and approved every label | Labels define "fit"; if the model sets them, it sets its own pass mark. |
| Audit verdicts | Built the seeded sheet; claude.ai drafted the verdicts | Reviewed and approved them, including the 4 disagreements | Judging a wrong reject means judging my own situation, not just the text. |
| Rule changes after measurement | Measured each change (rule changes and outcome changes) and reported when a fix did nothing (v0.2) | Decided v0.2 and v0.3, and rejected adopting the threshold change C6 | Changing a rule after seeing results can overfit to what I saw; deciding when that's justified is on me. |
| Trust decisions | Wrote the servers and probes; recorded declared vs. actual | Wrote the trust decisions (drafted in claude.ai, edited by him) | A tool's access becomes my access, so I decide what it may touch. |
| Whether a posting is worth my time | Returns a decision with quoted evidence; never applies or contacts anyone | Decides | Deciding to spend hours on an application is a life decision, not a classification. |
| Sign-off | Drafted this README and the sign-off sections | Signs or withholds | My name on it means I answer for every claim. |

## Sign-off

### Checked properties, with named tests and methods

| Property | How it was checked | Named test or evidence |
|---|---|---|
| Each FILTER rule does what FILTER.md says (T, A, S, K, ranking, abstain) | unit tests written before the code, each docstring stating the expected result | `tests/test_filter.py`, e.g. `test_T2a_new_false_friends_reject`, `test_A4_authorized_to_work_is_not_refusal`, `test_S3_smallest_N_wins`, `test_K2_lexical_false_friends_do_not_count`, `test_rule2_no_role_word_and_both_insufficient_abstains` |
| The 5 wrong versions are caught | unit tests | `test_W1_years_military_dear_do_not_trigger_A1`, `test_W2_S2_manager_I_is_not_entry_level`, `test_W3_entry_role_outranks_keyword_dense_role`, `test_W4_A3_negated_clearance_flags_not_rejects`, `test_W5_A5_silent_is_insufficient_never_supported` |
| v0.2 and v0.3 changes | red before the code change, green after | `test_v02_*` (`demo/04`), `test_v03_*` (`demo/07`) |
| Every evidence quote is in the posting | exact-substring re-check | `test_every_quote_is_found_again`, `test_tampered_quote_is_reported`; `shortlist.py` reported 0 quote errors |
| Held-out postings never tuned on | lock in code, plus tests | `test_held_out_postings_excluded_by_default`, `test_held_out_locked_until_labels_exist`, `test_real_fixture_is_not_held_out` |
| Config switches don't change results | `cmp` byte comparison; record-by-record comparison | default = saved v0.2 run (byte-identical, 19:19); V02 config = saved v0.2 records, V01 = v0.1 run (19:2x) |
| Tool server refuses what it doesn't declare | 18 scripted probes, full transcript | `transcripts/probe-own.jsonl` |
| Third-party server boundary | 20 probes, including a junction; disk state checked after | `transcripts/probe-fs.jsonl`, TOOL-EVAL.md B |
| Inherited JS2 behavior intact | inherited suite | 120 inherited tests in the final run |
| No user folder in transcripts and logs | scan after redaction | `python -I redact_paths.py` → 0 matches (F27, F28) |

### Not checked (genuine gaps)

1. **The miss rate among the 1,944 title rejects.** The audit saw 0 misses in 29 random draws; that is consistent with up to about 10% (rule of three), not a measured rate.
2. **Recall, in any meaningful sense.** The held-out set has one `fit`. The labels were drafted by Claude, so they are not an independent human standard.
3. **Location.** No rule reads it. H08 (London) is accepted although it is not a fit for a US-sponsorship persona.
4. **Whether the postings are still open.** Cloudflare and OpenAI were captured 2026-11-10, Zoox 10-30 and 11-10.
5. **`verify.py` was not run on the 2026-11-25 live run, and no SHA256SUMS were written for `raw/2026-11-25/`.**
6. **The tool server at 0.3.0 was only smoke-tested**, not re-probed in full; no network monitor was run to prove it makes no network calls.
7. **The Filesystem server's MCP Roots path, swap races, 8.3 short names, UNC paths and its source code.**
8. **The v0.3 A2 exception matches one exact phrasing** ("without sponsorship for an export license"). Other wordings were not tested.

### Claims NOT made

- No sample count here is a rate for all postings.
- The filter does not decide whether a posting is worth applying to. A flag or an accept is evidence for a human.
- "Posting is silent" never means "sponsors".
- The held-out labels are not independent human judgments (they were drafted by Claude and approved by Prathamesh), so the score test is partly Claude judging Claude.
- The threshold change C6 is not an improvement, although its count is better.
- The Filesystem server is not "safe" in general; the trust decision covers one narrow setup.
- The same answers across sessions show stored rules and files, not model training (SCORE.md section 3).

### Signed or withheld

> I have read this README and I stand behind it. Signed, Prathamesh, 2026-11-25.

Name: Prathamesh  Date: 2026-11-25  Signed / withheld: **Signed** (his words above, recorded verbatim by Claude Code at 19:44 EST)
