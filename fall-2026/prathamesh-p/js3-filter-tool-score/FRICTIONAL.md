# FRICTIONAL: JS3 honest log

Facts are recorded with their timestamps (EST, from `date`, or from tool output where noted). "My take:" lines appear only where Prathamesh made a decision. Claude Code (Opus 5.5) wrote the factual entries.

**F1. 2026-11-25, about 18:39: the due date doesn't match.**
- The brief (`05_job_search_agent_3_filter_tool_score.md`) says **"Due: November 23, 2026"**.
- Prathamesh's instruction says due today, 2026-11-25 23:59 ET.
- **Resolved (recorded 2026-11-25 ~18:46 EST):** Prathamesh reports his TA extended JS3 to **2026-11-25 23:59 ET**. Nov 23 was the original date.

**F2. About 18:39: the branch.**
- Created `prathamesh-p-js3-filter-tool-score` from `f8a7af8` (JS2: README final wording).
- The checkout before that was `prathamesh-p-final-project-film-2`, with `final-project-film/` untracked.
- After switching, `final-project-film-2/` shows as untracked. It holds only work files (`_qc/`, `clips/_work/*.wav`). Its 61 tracked files are still committed on their branch. Nothing was deleted.

**F3. About 18:39: the copy from JS2.**
- Copied from `js2-loop-tools-diff/`: `loop.py`, `adapters.py`, `policy.py`, `jobwatch.py`, `verify.py`, `GATE.md`, `CONTRACT.md`, `.gitignore`, `tests/`, `fixtures/`, `raw/`, `prompts/`.
- The js1 and js2 folders were not modified.
- `raw/2026-10-30/shieldai.json` (gitignored in JS1/JS2) was not present in the JS2 working folder, so it wasn't copied.

**F4. 18:40:06: inherited tests.**
- `python -I -m unittest discover -s tests` → **Ran 120 tests, OK** (Python 3.13.1).
- Re-run and saved at 18:41:39 → `demo/00-inherited-tests.txt` (120, OK).

**F5. 18:40:34–18:40:36: one live run through the inherited loop and allow-list.**
- Command: `python -I loop.py run --board greenhouse:fastly --board greenhouse:datadog --board ashby:tailscale`.
- Result: 3/6 requests, 1.8 s, status `incomplete`, exit 3.
  - Fastly: 50 postings.
  - Datadog: 392 postings.
  - `ashby:tailscale`: HTTP 404. Wrong or absent slug; per GATE §4 there was no retry and no second guess.
- Log: `demo/01-board-check-live.txt`. Report: `runs/20261125T184034-139103-incomplete.json`.
- The boards were chosen by Claude as network-heavy companies. The Tailscale slug was a guess that failed.

**F6. About 18:42: inventory.**
- About 1,992 unique postings across Zoox, Cloudflare, OpenAI, Fastly and Datadog.
- 43 titles contain "network". 0 have an entry-level word.
- A quick level regex matched Datadog "Manager I, Engineering - Zero Trust Networking" as junior. That is a false friend, and it became FILTER rule S2 and wrong version W2.

**F7. About 18:42: the existing labels can't be held out.**
- `tests/hand_labels.json` (10 rows) holds the JS1 rule applied by hand, not independent fit judgments (see its PROVENANCE file).
- So it can't serve as held-out labels for the score test. New blind labels are needed (PLAN §1).

**F8. About 18:43: FILTER.md v0.1 drafted by Claude.** All rules are DRAFT. No filter code has been written.

**F9. 18:46:08: approval.**
- Prathamesh approved all rules of FILTER.md v0.1 and PLAN.md, including the Filesystem MCP server with a pinned version.
- The time comes from `date` and is written into each rule row.
- His message said "24 rules". The file has **23**: T1–T5 plus T2a and T3a (7), A1–A6 (6), S1–S5 (5), K1–K3 (3), R1–R2 (2). Claude's 18:43 report had said 24; that was Claude's miscount.

My take: Writing the rules down before code showed me which ones were guesses. Seniority was new, and it turned out to be the only rule that changed anything on the held-out set.

**F10. About 18:47: correction, 40 network titles, not 43.**
- `postings.py` merges captures by (board, id), newest capture wins: **1,994 unique postings**, of which **40** have a network title.
- The 18:42 count (F6) of 43 counted the three Zoox titles once per capture.
- The held-out sample therefore draws 20 of 40.
- The 18:42 "about 1,992" was an earlier rough union; 1,994 is the `postings.py` count.

**F11. 18:47:10–18:48:28: held-out sample drawn.**
- Command: `python -I holdout.py --seed 20261125`.
- It wrote `holdout/HOLDOUT.json` and `LABEL-SHEET.md`: 30 postings (20 network titles, 10 others), in shuffled order. No filter output is on the sheet.
- The sheet was regenerated 3 times because of display bugs in the line search:
  1. it split sentences at "U.S.";
  2. "Unauthorized use of AI tools" matched the authorization search;
  3. a shell-quoting mistake put a literal backspace byte (0x08) in the authorization regex, so for one draw that search matched nothing;
  4. the duties lines sometimes caught a heading instead of a duty.
- Each redraw used the same seed. A script compared the selected IDs with the first draw: the same 30 IDs, in the same order. Only the displayed lines changed.
- Final sheet: 18:48:28.
- `holdout.py` refuses to overwrite either file; the redraws deleted them by hand first.

**F12. 18:48:47–18:52:45: filter tests first, then the code.**
- `tests/test_filter.py` was written from FILTER v0.1 before `filter.py` existed: 52 tests, each docstring states the expected result, and they include W1–W5.
- **Red evidence.** The first saved red run (about 18:50) was invalid: `python -I -m unittest tests.test_filter` failed because `tests` isn't an importable package, not because `filter.py` was missing. It was replaced by a red run with `filter.py` moved aside (`demo/02-filter-tests-red.txt`: `No module named 'filter'`).
- **First run with the code:** 51/52 passed. `test_S2_engineer_I_is_entry_level` failed because the S2 regex was case-sensitive for "Engineer". The code was fixed (the word is now case-insensitive, the numeral exact); the test was unchanged.
- **Full suite:** 172 tests, OK (`demo/03-full-suite.txt`, 18:52:45).
- **Held-out rule.**
  - The filter was **not run** over the postings; there is no `out/` folder.
  - Tests use synthetic records plus two real postings that a test first checks are outside the held-out set (Zoox "Senior Network Security Engineer", Datadog "Manager I, ...").
  - `select_for_run` drops the 30 held-out IDs by default and raises `HoldoutLocked` until a labels file exists.
  - One test docstring named a held-out title as an example; it was reworded at about 18:52 (no verdict was computed).
- **Implementation readings.** The code had to pick a reading of some v0.1 wording. These are listed as N1–N6 in the `filter.py` docstring for Prathamesh to review. They are not FILTER changes.

**F13. About 19:01: the labels message arrived with no verdicts.**
- It read "H01 ", "H02 ", "H03 ", "...", "H30 ", with H04–H29 not listed at all.
- `holdout/LABELS.json` was **not** created: writing it would invent labels, and its existence unlocks the held-out postings. Nothing was guessed.
- The held-out postings stay locked.

**F14. 19:01:45: N1–N6 accepted.** Prathamesh accepted N1–N6 as written. The time from `date` is in the `filter.py` docstring.

**F15. 19:01:47: first filter run.**
- Command: `python -I filter.py run` over 1,964 postings (all except the 30 held-out).
- Result: 1,963 reject, **1 accept**, 0 flag, 0 abstain.
- Deciding rules: T1 1,944; A1 9 (8 on "export control", 1 on the text **"ears"**); S1 5; T2a 2; S3 2; K1 1.
  - *Corrected 2026-11-25 ~19:10 EST:* this line first said "1 on 'EAR'". The matched text was "ears" ("the eyes and ears of Cloudflare"): the plural rule let EAR match "ears". Found by the 19:0x printout of the A1 sentences.
- These are counts of what the filter did, not error rates.

**F16. 19:02:38–19:03:44: audit sheet.**
- Command: `python -I audit_sheet.py --seed 7375` wrote `audit/AUDIT-SHEET.md` and `audit/AUDIT-SAMPLE.json`.
- **30 random rejects:** 29 decided by T1, 1 by A1.
- **5 near-threshold cases**, defined in the `audit_sheet.py` docstring: S3 at 5 years ×1, K1 ×1, T2a ×2, and one seeded draw from 7 single-phrase A1 rejects.
- **Accepts:** only **1** exists, so 1 is shown instead of 5.
- **Redraws:** the sheet was redrawn twice with the same seed (sample identical, checked by script):
  1. to show the full sentence around an A1 phrase instead of the two words;
  2. because the filter's sentence cutter (`_sentence_around`) stopped at "U.S.", the same bug as F11.
- **The cutter fix was a code fix, not a rule change.**
  - Its first attempt, through a shell heredoc, left `filter.py` with a syntax error. It was fixed with the editor.
  - After the fix: 172 tests OK. The filter rerun at about 19:03 gave the same outcome, deciding rule and flags for all 1,964 postings, with 0 stored quotes changed.

**F17. 19:09:59: held-out labels saved.**
- File: `holdout/LABELS.json`, 30 labels: 1 fit (H03), 28 not_fit, 1 unsure (H02). A script checked they cover exactly the 30 IDs in HOLDOUT.json.
- **Provenance, as Prathamesh stated it:** drafted by Claude (claude.ai chat) at his request from the sheet text Claude Code printed; he reviewed and approved every one; made blind to any filter output on the held-out set.
- So the score test is partly Claude judging Claude (SCORE.md).

My take: I let Claude draft my labels to save time, so my score test is partly Claude grading Claude. That's the weakest part of this assignment, and it was my choice, not an accident.

**F18. 19:10:10: audit verdicts saved.**
- File: `audit/AUDIT-VERDICTS.json`, 37 rows (36 sheet rows plus X01, the "ears" reject).
- 4 disagree: X01, R16, N05, N02. Drafted by Claude (claude.ai chat), approved by Prathamesh.
- F15 corrected in place, with a dated note ("EAR" → "ears").

**F19. 19:10–19:11: FILTER v0.2, tests first.**
- 5 tests were added to `tests/test_filter.py`.
- **Red run** (`demo/04-v02-tests-red.txt`): 3 failed as expected. 2 already passed; they guard that uppercase EAR and explicit exclusions still reject.
- **Code:** `EAR_EXACT` and A7 `may require access`. After the change: 177 tests, OK.
- **Rerun on the 1,964 non-held-out postings** (`demo/06-v01-to-v02-diff.txt`): 9 postings changed their deciding rule (A1 → A2), and **0 changed outcome**.
  - All 9 contain "...U.S. export laws without sponsorship for an export license.", and A2 matches "without sponsorship" in it.
  - R16 and N05 are still rejected. A2 is not changed; that's for Prathamesh.

My take: My fix changed which rule rejected the postings, not whether they were rejected. If I'd only checked the rule I fixed, I'd have thought it worked. Checking outcomes showed the real problem.

**F20. 19:11:37: FILTER.md updated to v0.2.**
- The A1 row is marked CHANGED, A7 added, the K1 known limit recorded.
- The changelog cites each measurement and the measured effect (0 outcomes changed).

**F21. About 19:12: audit report written** (`audit/AUDIT.md`): mistakes, the false friend "ears", rule changes, limits of inference (0 misses in 29 T1 draws is not a rate).

My take: The worst error wasn't a missing rule; it was my own plural rule turning "ears" into a legal restriction. The random title rejects found nothing; the near-threshold cases found everything.

**F22. About 19:12–19:14: full run and shortlist.**
- `filter.py run --include-holdout --labels holdout/LABELS.json` over 1,994 postings: 1,991 reject, **3 accept**: H03, H08, and the WAN posting (A01).
- `shortlist.py` wrote `SHORTLIST.md` with 0 quote errors.
- `GROUNDING.md` written. One claim in it was wrong as first drafted: it said K1 "counts `routing`" in H26's cabling sentence, but H26 was rejected at S3 and never reached K1. Rechecked by calling `gate4` alone: the first `routing` match is the cabling sentence, and a second, genuine one exists. The text was corrected to say exactly that.

**F23. 19:14–19:15: own MCP server.**
- `mcp_server.py` and `mcp_probe.py` written. 18 probes at 19:14:34 (`transcripts/probe-own.jsonl`); every refusal behaved as designed.
- **Mismatch found by Claude while writing the evaluation:** the tool description said "no writes, no side effects", but the server writes its own transcript log. Description corrected at about 19:14:40; the probe transcript keeps the old wording.
- **Real client:** Claude Code 2.1.332 (`claude -p`, `--strict-mcp-config`, only `mcp__js3__score_posting` allowed), 19:14:55–19:15:13, exit 0. The client reported a cost of $0.16.
  - The client first sent `server/discover` (protocol 2026-07-28), got -32601, then fell back to `initialize` 2025-11-25.
  - It used its built-in ToolSearch despite "do not use any other tool", and said so.
- **The client transcript contains 12 paths with the Windows user folder name.** Not redacted; for Prathamesh to decide before commit. *(Resolved: Prathamesh decided to redact; done at 19:30:33, F27.)*

My take: My server's description was wrong the first time: it said "no writes" while logging every call. The transcript caught it, not my reading of my own code.

**F24. 19:15–19:17: Filesystem MCP server evaluation.**
- `npm view` listed versions; pinned **2.2.0** (published 2026-11-04). The latest was 2.4.0.
- Sandbox in the scratchpad. The first junction attempt (`cmd mklink /J` from Git Bash) failed with a syntax error; PowerShell `New-Item -ItemType Junction` worked.
- **The first probe run (19:16:25) was invalid:** a Python heredoc turned `\a` into a bell character in every `allowed` path. It is kept as `transcripts/probe-fs.INVALID-mangled-paths-191625.jsonl`.
- A probe builder was then written as a file (`probes/make_fs_probes.py`, asserts no bell byte), the sandbox rebuilt, and the run repeated at 19:17:00: 20 probes. The boundary held on all escape probes. The only new file on disk is `allowed/written-inside.txt`. Refusal messages echo full absolute paths.
- **Count corrected:** Claude first wrote "17 tools, 11 read-only" (and told Prathamesh "7 write"). The transcript says 16 tools, 10 read-only, 6 not. Fixed in TOOL-EVAL.md.

My take: A server that holds its boundary still isn't safe by default. It wrote files without asking anyone.

**F25. 19:17–19:19: score test.**
- **Config switches** were added to `filter.py`: V02 is the default, plus V01 and JS2_BASELINE. Checked: the default reproduces `out/decisions.all.v0.2.jsonl` byte for byte (`cmp`), and V01 reproduces the 19:01 v0.1 run exactly. 177 tests OK (`demo/05-full-suite-v02.txt`, 19:20:36).
- **`score_test.py`** at 19:18:42: 7 runs on the 30 held-out postings.
  - Seniority (C1) cut "reaches me" false positives from 3 to 1 (H19, H26) and kept H03.
  - A3, T2a and v0.2 changed no held-out outcome.
  - The K1 threshold 2 → 3 (C6) removed H08, which was labelled not_fit for location, not skills. **Not adopted** (that would be tuning on held-out labels).
- SCORE.md first said A3 "found no negated phrase". That wasn't checked; reworded to "changed no outcome".

My take: One fit in thirty labels makes my recall a coin flip. The threshold change looked like an improvement but removed a London job for the wrong reason, so a better number isn't the same as a better rule.

**F26. 19:26:49–19:28:46: FILTER v0.3, tests first.**
- Decision (Prathamesh): in A2, `without sponsorship` doesn't count when the same sentence continues `for an export license`; such sentences fall to A7.
- 4 tests added.
  - **Red** (`demo/07-v03-tests-red.txt`, 19:26:49): 2 new-behavior tests failed; 2 guards (visa refusal, plain "without sponsorship") passed.
  - After the code change: 181 tests, OK.
- **Checked before rerunning:** the V02 config still reproduces the saved v0.2 all-postings run record for record, and V01 reproduces v0.1. The A7 note wording also changed, but no v0.2 decision carried an A7 note.
- **Rerun on 1,964 non-held-out postings** (`demo/08-v02-to-v03-diff.txt`, 19:27:38): the same 9 postings changed.
  - **3 reject → flag:** 8159206 (N05), 8081027 (the "ears" posting), 8088751.
  - 6 are now rejected by S1 ×2, S3 ×1, K1 ×3. **R16 (8188468) is still rejected, now by K1.**
- **Score test re-run** (19:27:52) with C7 added: C0–C6 rows identical to the 19:18 run (diffed). C7: accepts unchanged; "reaches me" 2 → 4 (H06 and H15 now flag, both labelled not_fit).
- **Other updates:**
  - The full v0.3 run (1,994 postings): 1,986 reject, 5 flag, 3 accept. `SHORTLIST.md` regenerated (3 accepted + 5 flagged, 0 quote errors); the v0.2 shortlist is kept as `out/SHORTLIST.v0.2.md`.
  - The MCP server was relabelled 0.3.0 and smoke-tested (19:28:30).
  - FILTER.md changelog, SCORE.md, AUDIT.md and GROUNDING.md were updated with these numbers.
- **One edit failed silently and was redone:** the first scripted FILTER.md update changed the A2 status cell but not its rule text (the replacement string didn't match). Fixed with a direct edit.

**F27. 19:30:33: user folder redacted.**
- Decision (Prathamesh): replace the Windows user folder with `<USER_HOME>` in every transcript and log.
- **First scan attempt failed:** a scanner written as a shell heredoc reported 0 matches. The Bash tool had turned `\` into `\` in the regex, the same cause as the F11 backspace and F24 bell bugs. Rewritten as a file, `redact_paths.py` (scan by default, `--apply` to replace).
- **`--apply`:** 144 replacements in 6 files (demo/00, probes/fs.json, and 4 transcripts).
- **A raw grep then still found the path in 2 files** (`demo/03`, `demo/05`): they are Windows-1252 test logs, and the script had **silently skipped** non-UTF-8 files. The script was fixed to read those byte-for-byte as latin-1 and to say so. 4 more replacements.
- **Total: 148 replacements in 8 files.** The script rescan and a raw byte grep both found 0. Every JSON and JSONL file still parses.
- `probes/fs.json` is redacted too, so it no longer runs as is; regenerate it with `probes/make_fs_probes.py`.

**F28. 19:34:07: final run and privacy scan.**
- **Inserted verbatim** (Prathamesh's text, drafted in claude.ai and edited by him): the 2 trust decisions (TOOL-EVAL.md), 7 "My take" lines (F9, F17, F19, F21, F23, F24, F25; the empty placeholder after F8 removed) and 7 "Why this stays mine" cells (README).
- README.md written, with the sign-off sections and "Signed / withheld" left blank.
- **Final suite** (`demo/09-final-suite.txt`): 181 tests, OK. Its log contained the temp-folder path twice; redacted (2 more, 150 in total). Rescan: 0.
- **Privacy scan:**
  - no user-folder path;
  - emails only from public posting text (Zoox accommodations) and the inherited test fixtures;
  - no key, token or password pattern;
  - no `resume.json`, `.env` or credentials file; the only persona is `fixtures/resume.fictional.json` (`fictional: true`, @example.com).
- **Still in the Claude Code client transcript:** the session id, the list of installed plugin names, and Claude Code settings. Not personal data as defined above; left as captured.

**F29. 19:44:01: decisions, sign-off, stale-wording sweep.**
- **Prathamesh decided:** leave the session id and plugin list in the client transcript as captured, and commit the `out/` folder (the reports cite it).
- **Sign-off, recorded verbatim in README.md:** "I have read this README and I stand behind it. Signed, Prathamesh, 2026-11-25." The README status line was changed from "NOT YET SIGNED" to signed.
- **Stale-wording sweep** ("NOT YET", "TODO", "pending", "draft", "to be written", "for Prathamesh to decide", "unsigned"). Outdated and fixed:
  - the README status line;
  - SOURCES.md "left unsigned";
  - F23's "for Prathamesh to decide" (resolution note added; the original wording kept as a log).
- Kept as is: provenance lines ("drafted by Claude ... approved by Prathamesh"), the historical facts in F8 and F28, and the variable name `pending` in `loop.py`.

