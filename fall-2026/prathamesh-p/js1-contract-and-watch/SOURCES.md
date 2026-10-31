# SOURCES: JS1, The Contract and the Watch

## External sources

| Source | Used for | Accessed |
|---|---|---|
| Assignment brief `03_job_search_agent_1_contract_watch.md` (instructor, local copy) | Requirements | 2026-10-30 |
| Lever public postings API: `https://api.lever.co/v0/postings/shieldai?mode=json` and `.../zoox?mode=json` | Raw board data, unauthenticated GET | 2026-10-30 18:11 EDT |
| `prpathak1/the-reallocation-engine`, branch `contrib/2026fa-prpathak1-mode-network-sponsorship-text`, commit `f3ea8b7`, `scripts/contrib/2026fa/prpathak1-network-sponsorship-text/filter_titles.py` | Gate 1 title rule (include/flag/exclude, false friends). This is Prathamesh's own earlier work. | 2026-10-30 |
| `the-reallocation-engine/search/examples/aarav-patel/resume.example.json` and `priya-nair/profile.yml` | Format for the fictional résumé (visa, target, and exclusion fields) | 2026-10-30 |
| BLS SOC 15-1241 Computer Network Architects, https://www.bls.gov/OES/current/oes151241.htm | Persona target occupation | cited 2026-10-31 (URL supplied by Prathamesh; not opened by Claude Code) |
| Course AI policy and video (links in brief) | Policy | reviewed by Prathamesh, 2026-10-31 |

## Prathamesh's work

- The persona concept (F-1, network engineering, SOC 15-1241) and the Reallocation-mode title filter that Gate 1 reuses.
- Board decision (zoox), two-valued verdict with flag = not relevant + needs_human, folder decision (2026-10-30).
- CONTRACT §7 Failure sentence: reviewed and approved by Prathamesh on 2026-10-30, before any implementation run. (The drafting was Claude's; see below.)
- Gate 2 whole-word decision and reason (2026-10-30 18:33). Gate 3 plural decision. State = exactly the last run.
- Hand predictions for 10 rows (`tests/hand_labels.json`): drafted by Claude (claude.ai chat) at Prathamesh's request by applying the rule by hand; reviewed and approved by Prathamesh before any implementation existed.
- Gate 2 sponsorship-refusal amendment (2026-10-31), decided from Prathamesh's own LinkedIn check.
- ALTERNATIVES.md (b): hands-on LinkedIn job-search observation, written by Prathamesh on 2026-10-31 ~14:00 EDT and inserted verbatim by Claude Code.
- Labeling-rule seniority decisions and the 20 experiment labels: drafted by Claude (claude.ai chat), reviewed and approved by Prathamesh (2026-10-31), before any judge output on those postings.
- ACTION-SURFACES.md (a): hands-on chat-assistant observation (two claude.ai attempts), written by Prathamesh on 2026-10-31 ~14:30 EDT and inserted verbatim by Claude Code, everything through "What could go wrong". The final "Compared with my agent" paragraph was drafted by Claude (claude.ai chat) from the run records and approved by Prathamesh, then revised at Prathamesh's instruction (14:41 EDT).
- Claude-written tests reviewed and approved by Prathamesh.
- Reviewed the course AI policy and the AI policy video (2026-10-31).
- Prathamesh's own writing (2026-10-31), inserted verbatim by Claude Code: the 11 FRICTIONAL "My take" lines, the README "Why this judgment stays mine" column, the least-autonomy choice and defense (ACTION-SURFACES.md), the README sign-off, and the 7 suggestions-log statuses. **Three lines were corrected for accuracy by Claude (claude.ai chat) and approved by Prathamesh:** the F9 My take, the "Labeling rule and labels" row of "Why this judgment stays mine", and the "What I limited" paragraph. In that paragraph, Claude Code selected the write-limit sentence from Prathamesh's two alternatives, based on the 14:55 EDT check.

## Claude Code's contribution (Claude Opus 5.5 in Claude Code)

| Date | What | Status |
|---|---|---|
| 2026-10-30 | Fetched and hashed the day-1 raw responses for both boards | Done, unmodified files |
| 2026-10-30 | Surveyed both boards with copied title regexes (scratch script, not committed) | Done |
| 2026-10-30 | Created branch `prathamesh-p-js1-contract-and-watch` from `origin/main` (`818e00f`) | Done, uncommitted |
| 2026-10-30 | Drafted CONTRACT.md (rule, refusals, wrong versions) | Approved by Prathamesh 2026-10-30; later amended by Prathamesh (dated) |
| 2026-10-30 | Drafted `fixtures/resume.fictional.json` (fictional persona) | In use (fictional) |
| 2026-10-30 | Drafted FRICTIONAL.md (facts only) and this file | Maintained through 2026-10-31 |
| 2026-10-30 | Applied Prathamesh's decisions to CONTRACT.md, inserted §7 verbatim, marked APPROVED | Done |
| 2026-10-30 | Wrote `tests/test_jobwatch.py` from CONTRACT.md before any implementation | Reviewed and approved by Prathamesh |
| 2026-10-30 | Amended CONTRACT Gate 3 (plurals) and §6 (state) per Prathamesh; updated the tests to match; added the state-equality test | Done |
| 2026-10-30 | Selected 10 real Zoox postings for hand prediction (`tests/hand_label_candidates.json`), no verdicts | Predictions supplied 2026-10-30 (`tests/hand_labels.json`) |
| 2026-10-30 | Claude (claude.ai chat, a separate conversation, not this Claude Code session) drafted the CONTRACT §7 Failure sentence at Prathamesh's request. Prathamesh reviewed and approved it. Claude Code inserted it verbatim. | Approved by Prathamesh 2026-10-30 |
| 2026-10-30 18:28 | Corrected the §7 provenance note in CONTRACT, FRICTIONAL F5, and SOURCES (see FRICTIONAL F8) | Done |
| 2026-10-30 | Wrote `tests/rows2-3-text.txt` (text extraction only) | Done |
| 2026-10-30 18:33 | Amended CONTRACT Gate 2 (whole word) per Prathamesh; added 2 tests; saved hand_labels.json unedited, with provenance | Done |
| 2026-10-30 18:34 | Wrote `jobwatch.py` (stdlib) against the tests; Gate 1 copied unchanged from filter_titles.py f3ea8b7 | 41/41 tests OK at 18:35:14 |
| 2026-10-30 18:35 | Ran run 1 (baseline) on saved `raw/2026-10-30/zoox.json`: 0 new / 227, state saved | Done |
| 2026-10-30 18:35 | Compared the rule against the 10 hand predictions (10/10); W1/W2 mutation check in scratchpad (W2 caught by 1 of 2 tests) | Done |
| 2026-10-30 18:38 | Strengthened the W2 test (old posting first); verified FAIL on the W2 mutant and PASS on jobwatch.py | Done |
| 2026-10-30 18:39 | Gate 2 plural "s": CONTRACT amendment, then test, then code (Prathamesh's decision) | 42/42 OK |
| 2026-10-30 18:41 | Wrote `prompts/judge_v1.md` and `claude_judge()` (headless `claude -p`); 4 offline harness tests; fixed my own new test's wrong assertion (made it stricter) | 46/46 OK at 18:41:23 |
| 2026-10-30 18:41 | Smoke-tested the judge on row 2: one dated Claude response (claude-opus-5-5, session f0dc4819-…), accepted by the validator | Done |
| 2026-10-30 18:42 | Selected 20 experiment candidates; seeded dev/held-out split (seed 20261030); no labels | Done |
| 2026-10-30 18:42 | Drafted `experiment/LABELING-RULE-DRAFT.md` | Superseded by `experiment/LABELING-RULE.md` (approved by Prathamesh 2026-10-31) |
| 2026-10-31 13:27 | Ran the day-2 fetch (one GET) and run 2 with `--judge claude`: identical response, new=0, no Claude call; state copied | Done; seeded fallback not used |
| 2026-10-31 13:28 | Held-out swap of row 2 to `e6a4bbe1…` via the same seeded procedure (Prathamesh's decision) | Done |
| 2026-10-31 13:29 | Started `NOT-CHECKED.md` (item 1 Prathamesh's; Claude-proposed items confirmed by Prathamesh 2026-10-31) | Done |
| 2026-10-31 13:30 | Generated `experiment/LABELING-SHEET.md` (20 candidates, blank label lines) | Done; labels are Prathamesh's |
| 2026-10-31 13:43 | Added SEEDED label support (test first); built the SEEDED earlier response and manifest; ran SEEDED runs 1-2 with the Claude judge | 47/47 OK; 1 accepted, 4 rejected |
| 2026-10-31 13:45 | Drafted ACTION-SURFACES.md (b, c), the experiment/REPORT.md skeleton, and the README.md draft | Completed 2026-10-31 (README signed by Prathamesh) |
| 2026-10-31 13:53 | Fixed `prompts/judge_v1.md` résumé-path rules (Prathamesh's decision); archived the pre-fix template; added a path-sync test; recorded both hashes | 48/48 OK |
| 2026-10-31 13:54 | Created ALTERNATIVES.md from Prathamesh's supplied summary (URLs not opened by Claude Code); added the blank (a) section in ACTION-SURFACES.md | Done |
| 2026-10-31 14:15 | Inserted Prathamesh's ALTERNATIVES.md (b) text verbatim (checked); noted that Gate 2 misses "without sponsorship" (no change made) | Done |
| 2026-10-31 14:17 | Gate 2 sponsorship-refusal phrases (Prathamesh's amendment): CONTRACT first, then 2 tests (failed first), then code; rule re-run on day-1 data: 0 of 227 verdicts changed | 50/50 OK |
| 2026-10-31 14:21 | Finalized LABELING-RULE.md (Prathamesh's decisions); saved labels.json unedited with provenance; wrote prompts/judge_v2.md (one change) | Done |
| 2026-10-31 14:22 | Wrote experiment/run_judge_batch.py and experiment/score.py; ran sampling (20 calls), dev v1/v2 (20 calls), held-out v2 once (10 calls) | Done |
| 2026-10-31 14:25 | Generated SAMPLING-REPORT.md and REPORT.md from summary.json | Done |
| 2026-10-31 14:36 | Inserted Prathamesh's ACTION-SURFACES.md (a) text verbatim (checked) | Done |
| 2026-10-31 14:41 | Corrected the ACTION-SURFACES (a) provenance and revised its paragraph; filled the (a) table (summary); moved NOT-CHECKED items to confirmed; corrected the CONTRACT coarseness example; restructured FRICTIONAL My-take lines and log statuses; wrote README.md | Done |
| 2026-10-31 14:55 | Ran the write-limit check (not enforced); inserted Prathamesh's writing verbatim (My takes, why column, least autonomy, sign-off, statuses); added NOT-CHECKED item 7; added the BLS citation | Done |
| 2026-10-31 14:58 | Fixed stale SOURCES statuses and the README header; privacy scan (clean); gitignored shieldai.json; backup commit and push (Prathamesh's instruction) | Done |
## Claude responses shown in this folder (dated)

| When (EDT) | What | Session | Model | File |
|---|---|---|---|---|
| 2026-10-30 18:41:32 to 18:41:43 | Judge smoke test, row 2 `8321d00e…` | `f0dc4819-b4d8-486f-9dd2-186cff30c397` | claude-opus-5-5 | `judgments/20261030T184143-…json` |
| 2026-10-31 13:43:42-13:43:48 | SEEDED run 2 judge, 48639085 | `3bac5e88-5c65-42d5-89df-e6152112393a` | claude-opus-5-5 | `seeded/SEEDED-judgments/...3bac5e88...json` (rejected) |
| 2026-10-31 13:43:48-13:43:58 | SEEDED run 2 judge, 8321d00e | `f57c3f69-536b-4346-9592-16031318b28c` | claude-opus-5-5 | `seeded/SEEDED-judgments/...f57c3f69...json` (accepted) |
| 2026-10-31 13:43:58-13:44:04 | SEEDED run 2 judge, 5de4079e | `34009517-bf54-4aac-8410-8f8ed8f85d57` | claude-opus-5-5 | `seeded/SEEDED-judgments/...34009517...json` (rejected) |
| 2026-10-31 13:44:04-13:44:09 | SEEDED run 2 judge, f62f1083 | `295e104d-b305-47d3-b65d-086f7166d597` | claude-opus-5-5 | `seeded/SEEDED-judgments/...295e104d...json` (rejected) |
| 2026-10-31 13:44:09-13:44:14 | SEEDED run 2 judge, eed5bd1e | `383038ee-dd1c-4885-83e1-cc10053512a5` | claude-opus-5-5 | `seeded/SEEDED-judgments/...383038ee...json` (rejected) |

## External sources supplied by Prathamesh (not opened by Claude Code)

| Source | Used for | Retrieved |
|---|---|---|
| https://www.linkedin.com/help/linkedin/answer/a511279 | ALTERNATIVES.md (a) LinkedIn job alerts | 2026-10-31, by Claude in claude.ai |
| https://cooper.edu/continuing-education/setting-job-alerts-linkedin | ALTERNATIVES.md (a) | 2026-10-31, by Claude in claude.ai |
| https://www.layerpath.com/learn/how-to-add-job-alerts-on-linkedin | ALTERNATIVES.md (a) | 2026-10-31, by Claude in claude.ai |
| 2026-10-31 14:22:21-14:24:11 | Sampling (20), dev v1 (10), dev v2 (10), held-out v2 once (10): 50 calls, all session IDs in experiment/results/*.json and experiment/SAMPLING-REPORT.md | 50 distinct | claude-opus-5-5 | `experiment/raw-judgments/` |
