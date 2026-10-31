# FRICTIONAL: JS1, The Contract and the Watch

An honest log covering what was tried, what happened, and what changed. Timestamps come from `date` (EDT).
Claude Code drafts the facts in each entry. **"My take:" lines are Prathamesh's alone, and Claude Code leaves them blank.**

**My take lines appear on entries where I made a decision.** (Prathamesh, 2026-10-31.) They are on: F5 (Failure sentence), F9 (Gate 2 whole word), F13 (seniority observation), F15 (Gate 2 plural), F20 (day 2 = no change), F24 (SEEDED fallback), F28 (LinkedIn observation), F29 (sponsorship gap amendment), F31 (sampling), F32 (experiment), F33 (chat-paste observation).

---

## F1. Day-1 raw capture of both Lever boards, done before anything else

- **Tried (Fri Oct 30 18:11:42 EDT 2026):** One `curl` GET each to
  `https://api.lever.co/v0/postings/shieldai?mode=json` and `https://api.lever.co/v0/postings/zoox?mode=json`.
  The body was saved unmodified with `-o`, and the response headers were saved separately.
- **Happened:** Both requests returned HTTP 200.
  - shieldai: 654 postings, 10,458,915 bytes, SHA-256 `3a3a428a6816cef22e4d331fbfe64158eb27d6c65d4b9370ddc4b9bbde3304a1` (18:11:42).
  - zoox: 227 postings, 2,306,248 bytes, SHA-256 `45a795dff755fc7839cbe7593a6fcb1ca48719eb8fcd3e4ecd883a238417eeb6` (18:11:44).
  - Files: `raw/2026-10-30/{board}.json`, `{board}.headers.txt`, `{board}.fetch.txt`, `SHA256SUMS`.
- **Changed:** The capture happened before the branch existed, so the files sat untracked under the
  folder path and carried over intact when the branch was created (F2). The capture was not repeated.
- **Unresolved:** The ShieldAI raw file is 10.5 MB. Whether to commit it depends on the board choice.
- **Traceability:** This session's transcript, plus `raw/2026-10-30/*.fetch.txt`.

---

## F2. Branch created from upstream main

- **Tried (around 18:13 EDT):** Checked the remotes. `origin` is `nikbearbrown/...` (upstream) and `fork` is `prpathak1/...`.
  Ran `git fetch origin`, then `git switch -c prathamesh-p-js1-contract-and-watch --no-track origin/main`.
- **Happened:** Upstream main moved `0a0376b..818e00f` in the fetch. The branch is at `818e00f`. The untracked
  `fall-2026/prathamesh-p/final-project-film/` also shows up on this branch because upstream main lacks it.
  Claude Code did not touch it.
- **Changed:** Nothing yet. Nothing is committed and nothing is pushed.
- **Open conflict (not resolved by Claude):** The repo `AGENTS.md` says "keep assignment implementations in
  learning-artifacts/", and `.gitignore` ignores `learning-artifacts/`. The brief and Prathamesh's instruction
  both say `fall-2026/prathamesh-p/js1-contract-and-watch/`. The work follows the brief. Prathamesh decides.

---

## F3. Board survey and recommendation (Claude suggestion, pending decision)

- **Tried (18:12 to 18:14 EDT):** Ran the Reallocation-mode title regexes, copied into a scratch script outside the repo,
  over both raw files. Counted citizenship/clearance/ITAR mentions and `createdAt` within 1, 3, and 7 days.
- **Happened:**
  - ShieldAI has 5 "network" titles (4 include, 1 flag), all with ITAR or clearance text, and 295/654 postings mention citizen or clearance.
  - Zoox has 3 "network" titles (2 include, plus the false friend "Software Engineer - Road Network Tools"), and 7/227 postings mention citizen or clearance.
  - Postings created within 3 days: ShieldAI 8, Zoox 10.
- **Changed:** CONTRACT.md recommends `zoox`. That is a Claude suggestion, and it has not been accepted yet.
- **Unresolved:** The second run lands on a Saturday, so zero new postings is possible. The seeded fallback is defined in CONTRACT §6.

---

## F4. Headless Claude check for the sampling report

- **Tried (18:14 EDT):** Ran `which claude`, `claude --version`, and `claude --help`. No prompt was sent.
- **Happened:** `claude` is at `~/.local/bin/claude`, version `2.1.314 (Claude Code)`. `-p/--print`,
  `--output-format`, `--json-schema`, `--no-session-persistence`, `--session-id`, `--tools`, `--model`, and
  `--bare` are all listed.
- **Changed:** Nothing has run. A new `claude -p` process without `--continue` or `--resume` should start a fresh
  conversation. That is an inference from `--help`, not a verified fact, so the plan is to record each session ID as evidence.

---

## F5. Decisions on the draft; section 7 approved by Prathamesh; contract APPROVED

- **Decisions (Prathamesh, 2026-10-30):** The board is **zoox**, with `raw/2026-10-30/zoox.json` as the day-1 input. The verdict stays
  two-valued, and a flag title gives `not_relevant` plus `needs_human: true` with the reason. The folder is
  `fall-2026/prathamesh-p/js1-contract-and-watch/`.
- **Folder conflict and resolution:** The repo `AGENTS.md` says "keep assignment implementations in learning-artifacts/",
  but `.gitignore` ignores `learning-artifacts/`, so that folder cannot meet the brief's GitHub-folder requirement.
  Prathamesh decided to follow the brief and use `fall-2026/prathamesh-p/js1-contract-and-watch/`.
- **Tried (Fri Oct 30 18:17:42 EDT 2026):** Claude Code checked CONTRACT §7. It was still the blank placeholder, and
  Claude stopped and reported that without making any other change.
- **Happened (Fri Oct 30 18:21:29 EDT 2026):** Prathamesh supplied the Failure sentence in chat and asked for it to be
  inserted verbatim. Claude Code inserted it unchanged, dated it 2026-10-30 18:21:29 EDT, and marked the contract
  APPROVED with that time. **Provenance (corrected in F8):** the sentence was drafted by Claude (claude.ai chat) at Prathamesh's request, and reviewed and approved by Prathamesh on 2026-10-30 before any implementation run. Claude Code applied the three decisions above to CONTRACT §§0, 1, 1.1, and 4.
- **Changed:** CONTRACT.md status moved from DRAFT to APPROVED.

My take: Partly. The failure I predicted did happen, but the one that mattered more was the sponsorship gap I hadn't predicted. That taught me my Failure sentence should describe the harm to me, not just a bug in the code.

---

## F6. Tests written first, from CONTRACT.md only

- **Tried (around 18:22 to 18:23 EDT):** Claude Code wrote `tests/test_jobwatch.py` (stdlib `unittest`) before any implementation
  file existed. The docstring fixes the interface the tests assume, which the implementation does not define yet.
  Coverage: the allow-list (including lookalike, userinfo, http, port, and off-host redirect cases), the single GET with no send paths,
  the résumé loader, the hand-predictable rule cases (including the real "Software Engineer - Road Network Tools" from
  the day-1 Zoox file), W1 (uncited or fabricated justification), the judgment schema validator, baseline = 0 new,
  second run = unseen IDs only, a failed run leaving state untouched, W2 (verdict attached to the wrong posting), judgment never
  changing the record, and rejected judgments stored as rejected.
- **Happened (Fri Oct 30 18:23:52 EDT 2026):** `python -I -m unittest discover -s tests -v` gave
  `ModuleNotFoundError: No module named 'jobwatch'` and `FAILED (errors=1)`. That was expected, because no implementation exists.
- **Choices Claude made that the contract did not fully pin down (flagged for review):** "firewalls" does not match
  the résumé term "firewall" (a literal whole-word reading of Gate 3). The state file shape is `{"ids": [...]}`, and the tests only
  assert that today's IDs are a subset of it. `hand_labels.json` is skipped until Prathamesh writes it.
- **Changed:** Nothing has been implemented. The tests are waiting for Prathamesh's approval.

---

## F7. Test changes from Prathamesh's decisions; hand-prediction candidates

- **Decisions (Prathamesh, 2026-10-30):** For Gate 3, plurals count: a term matches if the term or the term + "s" appears as a whole word,
  because "firewalls" should match "firewall". The state holds exactly the last successful run's IDs.
- **Changed (around 18:24 to 18:26 EDT):** CONTRACT Gate 3 was amended first, with the reason logged in the contract, and §6 now states the state shape.
  In the tests, `test_skills_match_whole_word_case_insensitive` (which locked in the literal behavior) was replaced by
  `test_skills_match_whole_word_case_insensitive_plural_s` (firewalls → firewall, relevant). A new test,
  `test_skills_plural_rule_still_requires_whole_word`, checks that firewalling, BGPx, eBGP, DNSSEC, and rerouting do not match. Another new test,
  `test_state_equals_exactly_current_run_ids`, checks that the state is exactly the current run's ID set. No other test was removed or weakened.
- **Tried (Fri Oct 30 18:26:29 EDT 2026):** Claude Code selected 10 real titles from `raw/2026-10-30/zoox.json`: the Road Network
  Tools title, both other network-titled postings, and 7 others chosen as near-misses (wireless, connectivity, security,
  infrastructure) plus one non-technical control. Each title was checked against its ID in the raw file. They are saved without verdicts in
  `tests/hand_label_candidates.json`.
- **Happened:** No implementation exists. The rule has not been run on these postings.
- **Unresolved:** Prathamesh's predictions are pending.

---

## F8. Correction: who drafted the §7 Failure sentence

- **What was wrong:** CONTRACT §7, FRICTIONAL F5, and SOURCES.md said the Failure sentence's wording was Prathamesh's.
  Claude Code wrote that note at 18:21 EDT on the basis that the sentence arrived in Prathamesh's chat message. That inference was wrong.
- **Correct provenance (stated by Prathamesh, 2026-10-30):** The sentence was drafted by Claude (claude.ai chat) at Prathamesh's request,
  and reviewed and approved by Prathamesh on 2026-10-30 before any implementation run.
- **Changed (Fri Oct 30 18:28:43 EDT 2026):** The §7 note, the F5 heading and text, and the SOURCES.md entries were corrected. The sentence itself and
  its date (2026-10-30 18:21:29 EDT) were not changed.

---

## F9. Gate 2 changed to whole-word matching for every phrase

- **Decision (Prathamesh, 2026-10-30):** Every Gate 2 phrase must match as a whole word, case-insensitive, not only "EAR". Reason:
  substring matching gives false hits, such as "ITAR" inside "military" and "EAR" inside "years", and rows 2 and 3 both contain "years".
- **Changed (Fri Oct 30 18:33:42 EDT 2026):** The CONTRACT §4 Gate 2 amendment came first, dated and with its reason. Then two tests were added before any code:
  `test_auth_phrases_all_whole_word` ("military", "years", "Dear", and "US citizenry" produce no hit) and
  `test_auth_phrase_hyphen_is_a_boundary` ("ITAR-controlled" is a hit). The hyphen case was Claude Code's reading of
  "whole word", and the amendment states it explicitly.
- **Unresolved (observation, not changed):** Because of the whole-word rule, the plural forms "U.S. citizens" and "security clearances"
  do **not** match the phrases "U.S. citizen" and "security clearance". Gate 3 allows a plural "s" but Gate 2 does not. No test covers either
  reading. This needs Prathamesh's decision.

My take: Matching parts of words would have caused false alarms. "Years" contains "EAR," so substring matching would have made the export-control gate fire on nearly every posting that mentions years of experience. I switched to whole-word matching before writing any code, because a gate that always fires is a gate I'd learn to ignore.

---

## F10. Hand predictions saved

- **Happened (Fri Oct 30 18:33:42 EDT 2026):** Prathamesh's 10 predictions were saved unedited to `tests/hand_labels.json`, with
  provenance in `tests/hand_labels.PROVENANCE.md`. Provenance as stated by Prathamesh: Claude (claude.ai chat) drafted them at
  Prathamesh's request by applying the CONTRACT rule by hand to the titles and to `tests/rows2-3-text.txt`. Prathamesh reviewed and
  approved them before any implementation existed. They are hand applications of the rule, not Prathamesh's independent judgment of fit.
- **Format:** The file is a plain JSON list so that the existing `test_hand_labels_if_present` reads it unchanged. The provenance note sits in a sibling file.

---

## F11. Implementation and first full test run

- **Tried (around 18:34 EDT):** Claude Code wrote `jobwatch.py` (stdlib only) against `tests/test_jobwatch.py`. No test was edited
  during implementation. Gate 1 is `decide()` copied unchanged from `filter_titles.py` (commit f3ea8b7). Redirects are checked
  against the allow-list *before* they are followed, by a custom `HTTPRedirectHandler`, and checked again on the final URL.
- **Happened (Fri Oct 30 18:35:14 EDT 2026):** `python -I -m unittest discover -s tests -v` gave `Ran 41 tests in 0.191s`, `OK`.
  The tests passed on the first run.
- **Mutation check (Fri Oct 30 18:35:49 EDT 2026, scratchpad copies, not in the repo):**
  - A W1 mutant that cites every résumé skill whether or not the posting mentions it failed 20 assertions across 9 tests, including
    `test_every_record_citation_is_grounded` and `test_one_skill_posting_cites_exactly_that_one_term`.
  - A W2 mutant that takes the verdict by list position from the unfiltered list failed **only 1 test**
    (`test_W2_many_new_postings_each_carry_their_own_verdict`). `test_W2_verdict_attached_to_correct_posting` **did not catch it**:
    in that fixture the one new posting is also at index 0 of the full list, so the positional bug happens to pick the right posting.
    W2 is still caught by the suite, but one of the two W2 tests is weaker than intended.
- **Not yet built:** the Claude judge (`claude -p`). `run()` stores `{"label": "judgment", "status": "not_run"}` when no judge is given.

---

## F12. Run 1 (baseline) on the saved day-1 Zoox response

- **Tried (Fri Oct 30 18:35:23 EDT 2026):** `python -I jobwatch.py run --raw raw/2026-10-30/zoox.json --state state/seen_ids.json
  --out runs/2026-10-30-run1-baseline.json --resume fixtures/resume.fictional.json`. No fetch: it used the file captured at 18:11:44.
- **Happened:** `baseline=True total=227 new=0 removed=0`, exit 0. The raw sha256 `45a795df…17eeb6` matches the 18:11 capture.
  `state/seen_ids.json` holds 227 IDs, equal to the raw file's ID set (sha256 `54a6a3cd3c92f70da4d90ed2be36f4d755252e6b0429f5a3b2b9901a3e3676e3`).
  The state directory did not exist before this run.
- **Evidence copy (Fri Oct 30 18:43 EDT 2026):** `state/seen_ids.json` was copied to `state/seen_ids.after-run1-2026-10-30.json` (identical sha256), because run 2 will overwrite the live state and the brief asks for state from both runs.

---

## F13. Rule verdicts against hand predictions on the 10 rows

- **Happened (Fri Oct 30 18:35:32 EDT 2026):** 10/10 agree. Saved to `runs/2026-10-30-hand-label-comparison.json`. The Gate 3 matches for
  rows 2 and 3 are exactly the predicted sets (BGP, OSPF, TCP/IP, VLAN, VPN, firewall), and Gate 2 had no hits on either row.
  Agreement shows that the code implements the rule as the rule was hand-applied. It does not show that the rule captures real fit.
- **Observation (Prathamesh, for later):** Rows 2 and 3 are Senior/Staff roles (8+ / 10+ years) that the rule marks relevant,
  because seniority is deliberately not a criterion. A human judging real fit for a pre-OPT master's student would likely disagree.
- **Observation (Claude Code, factual):** Row 4 "Embedded Software Engineer, Wireless Technologies" matched 4 résumé skills
  (TCP/IP, VLAN, firewall, routing) but is excluded at Gate 1 only because its title lacks "network".

My take: It bothered me. A Staff role asking for 10+ years isn't realistic for a master's student, and the rule only called it relevant because it doesn't look at seniority. I kept the rule as it is but documented seniority as a known gap, so I don't read "relevant" as "I should apply."

---

## F14. W2 test strengthened (not weakened)

- **Decision (Prathamesh, 2026-10-30):** Make `test_W2_verdict_attached_to_correct_posting` stricter by putting an old posting first in the day-2 data.
- **Changed (Fri Oct 30 18:38:37 EDT 2026):** Day-2 data went from `[R(new), N(old)]` to `[N(old), R(new)]`. No assertion was removed or loosened.
- **Happened (Fri Oct 30 18:38:45 EDT 2026):** On the scratchpad W2 mutant, the strengthened test **FAILED** (`AssertionError: 'not_relevant' != 'relevant'`).
  On `jobwatch.py` it **passed**. The full suite against the W2 mutant now fails 2 tests (both W2 tests) instead of 1.

---

## F15. Gate 2 allows a trailing "s"

- **Decision (Prathamesh, 2026-10-30):** Gate 2 phrases may be followed by a single "s", as in Gate 3. Reason: postings often say
  "must be U.S. citizens", and missing that would wrongly mark a citizenship-only job relevant.
- **Order:** CONTRACT §4 amendment first (18:38:50 EDT, dated, with the reason). Then the new test `test_auth_phrases_allow_plural_s`
  ("U.S. citizens", "security clearances", "U.S. persons"), which **failed on all 3 subtests** before the code change. Then the code change
  (`whole_word(p, plural=True)` for `AUTH_PATTERNS`).
- **Happened (Fri Oct 30 18:39:15 EDT 2026):** `Ran 42 tests`, `OK`. Across all 227 day-1 Zoox postings, Gate 2 has **0** hits.
  (The 18:12 survey's "7 of 227 mention citizen/clearance" was a plain substring search over the whole JSON, not the Gate 2 rule.)

My take: Missing "U.S. citizens" means I could spend hours on an application I'm legally not eligible for, while a false alarm costs me a minute to check. So I'd rather the gate fire too often than miss a citizenship requirement.

---

## F16. Claude judge built (prompt contract plus headless harness)

- **Prompt contract:** `prompts/judge_v1.md` defines the task (SOC 15-1241 role, no authorization blocker, skills overlap; **no
  seniority criterion**) and a fixed output schema that matches `validate_judgment` exactly (3 keys; citations with exactly 4 keys).
- **Tests first (around 18:40 EDT):** 4 offline tests in `JudgeHarness` with a faked CLI. They check that the prompt names the schema; that each call is
  `-p --no-session-persistence` with no `--continue`/`--resume` and `--tools ""`; that the raw output is saved with its session ID and timestamps;
  that fenced output is rejected and kept verbatim; that each call gets a new session ID; and that the record is unchanged.
- **Code:** `claude_judge()` in `jobwatch.py` runs `claude -p --no-session-persistence --session-id <uuid4> --output-format json
  --tools "" --strict-mcp-config` with the prompt on stdin, in an empty temporary working directory. The raw envelope is saved to
  `judgments/` **before** validation, and the result text goes through `validate_judgment`. A rejection is stored as `rejected`.
  New CLI: `run --judge claude` and `judge --posting-id` (single posting, no state change).
- **Test bug (Claude Code's own, in a test written minutes earlier):** At 18:41:06, `Ran 46`, `FAILED (failures=1)`.
  `test_fresh_headless_call_and_raw_saved_with_session_id` searched for the result text inside `stdout`, but `stdout` is
  the CLI's JSON envelope, where that text is escaped. Claude Code **replaced it with a stricter assertion**:
  `json.loads(saved["stdout"])["result"] == good`. The code was not changed for this. At 18:41:23: `Ran 46 tests`, `OK`.
- **Side change:** `strip_tags` now collapses runs of spaces and tabs left by removed tags, so the "lists" text Claude sees and the text
  the validator checks are the same and readable. All tests and the 10 hand labels still pass.
- **Limits (not checked):** The validator checks each side of a citation independently. It does not check that the résumé value and the
  posting value are *about the same thing*. For example, `target.soc_code: 15-1241` paired with a sentence from the description passes. User-level Claude
  settings and memory may still load in the `claude -p` subprocess; this was not verified.

---

## F17. Smoke test: one dated Claude response (row 2)

- **Tried (Fri Oct 30 18:41:32 EDT 2026):** `python -I jobwatch.py judge --raw raw/2026-10-30/zoox.json --posting-id 8321d00e-9e2b-4947-a37e-fdbad7dcd637`.
- **Happened (finished 18:41:43 EDT):** Exit 0, empty stderr. Session ID `f0dc4819-b4d8-486f-9dd2-186cff30c397` (requested = reported).
  The reported model was `claude-opus-5-5`, the CLI-reported cost was $0.0690, and `is_error` was false. The validator **accepted** it: verdict `relevant`, 8 citations,
  every one with both sides found. The record (rule) verdict was `relevant` and was not affected.
  Raw: `judgments/20261030T184143-8321d00e-…-f0dc4819-….json`. Labeled copy: `runs/2026-10-30-judge-smoke-row2.json`.
- **Note:** This is one dated Claude judgment. It is not evidence of correctness or repeatability.

---

## F18. Prompt-experiment candidates selected (no labels, no Claude output)

- **Happened (Fri Oct 30 18:42:21 EDT 2026):** 20 postings saved to `experiment/candidates.json`: all 3 network-titled postings (including the
  false friend), 11 near-misses hand-picked by Claude Code, and 6 drawn with `random.Random(20261030).sample`. Split: `sorted(ids)`, then
  `random.Random(20261030).shuffle`, with the first 10 as dev and the last 10 as held-out. Each entry has its ID, title, location, and a truncated requirements excerpt.
- **Exposure issue (decision for Prathamesh):** Held-out contains `8321d00e` (row 2, Senior Network Security Engineer). That posting has
  already been examined: its full text is in `tests/rows2-3-text.txt`, it was hand-applied in claude.ai chat, and it was the Claude smoke test in F17.
  Four more held-out IDs (`8af192a0`, `7522162e`, `bf983498`, `6320b978`) and four dev IDs appear in `tests/hand_labels.json`.
  That exposure was under the CONTRACT rule, not the experiment prompt. The split was **not** changed after seeing this.

---

## F19. Draft labeling rule for "real fit"

- **Happened (around 18:42 EDT):** Claude Code wrote `experiment/LABELING-RULE-DRAFT.md`, marked DRAFT and pending Prathamesh's edits, separate from
  CONTRACT §4. It covers network-role fit (by duties), work authorization (read in context), and seniority (more than about 3 years, or a Senior/Staff/
  Principal/Lead/Manager/Director title, is not fit). It ends with three open points for Prathamesh.

---

## F20. Day-2 fetch and run 2 (2026-10-31): no change on the board

- **Tried (Sat Oct 31 13:27:35 EDT 2026):** `python -I jobwatch.py fetch --board zoox --raw-dir raw`, one GET.
- **Happened:** HTTP 200, final URL unchanged (`https://api.lever.co/v0/postings/zoox?mode=json`), fetched 13:27:48 EDT (17:27:48Z).
  2,306,248 bytes, sha256 `45a795dff755fc7839cbe7593a6fcb1ca48719eb8fcd3e4ecd883a238417eeb6`. That is **identical to the 2026-10-30 capture**.
  The server `Date` header is new (`Sat, 31 Oct 2026 17:27:46 GMT` vs `Fri, 30 Oct 2026 22:11:44 GMT`), so this was a fresh response.
  The `ETag` is unchanged (`W/"2330c8-heSJ2Bqg0cqPQH6sszfhA2uYSco"`). The newest `createdAt` in the file is 2026-10-30 17:55 EDT, before the day-1 fetch.
- **Tried (Sat Oct 31 13:27:58 EDT 2026):** `python -I jobwatch.py run --raw raw/2026-10-31/zoox.json --state state/seen_ids.json --out runs/2026-10-31-run2.json --judge claude`.
- **Happened:** `baseline=False total=227 new=0 removed=0`, exit 0. No Claude call was made, because there were no new postings. The state was rewritten with the same 227 IDs
  (sha256 `54a6a3cd…3676e3`, unchanged) and copied to `state/seen_ids.after-run2-2026-10-31.json`.
- **Stopped:** Per Prathamesh's instruction, the seeded fallback (CONTRACT §6) was **not** used. It waits for Prathamesh's go-ahead.

My take: Only partly. Finding nothing is what should happen when nothing changed, but on its own that result can't tell "no change" apart from "the watch is broken." That's why I also needed a seeded test.

---

## F21. Held-out swap: row 2 removed

- **Decision (Prathamesh, 2026-10-31):** Row 2 (`8321d00e`, Senior Network Security Engineer) cannot be held-out. It was examined before tuning:
  hand-applied in claude.ai chat, full text in `tests/rows2-3-text.txt`, and the Claude smoke test (F17).
- **Changed (Sat Oct 31 13:28:35 EDT 2026):** It was replaced by `e6a4bbe1-20ab-4f1f-af07-f06fabedeabd` "Mechatronics Engineer - Closures" (held-out). That is
  the next draw from the same seeded procedure, `random.Random(20261030).sample(others, k)` at k = 7. The script first reproduced the original 6 fill draws exactly
  and verified that the sample prefix is stable. The first new draw was neither a candidate nor examined (examined = IDs in `tests/hand_labels.json` plus rows 2–3),
  so nothing was skipped. The swap is recorded under `"swaps"` in `experiment/candidates.json`. The split is now 10 dev / 10 held-out.
- **Still open (from F18, unchanged):** Four other held-out IDs (`8af192a0`, `7522162e`, `bf983498`, `6320b978`) appear in `tests/hand_labels.json`.
  They were examined by title only, under the CONTRACT rule, and were not swapped.

---

## F22. "Not checked" list started

- **Changed (Sat Oct 31 13:29 EDT 2026):** Created `NOT-CHECKED.md`. Item 1 is Prathamesh's: the validator checks that each citation's sides exist, but not
  that they refer to the same thing. Three further items proposed by Claude Code are listed separately, as pending Prathamesh's confirmation.

---

## F23. Decisions after run 2; SEEDED label support

- **Decisions (Prathamesh, 2026-10-31):** Keep the real run 2 (new=0) as evidence that the watch correctly reported nothing new on an identical response.
  Apply the CONTRACT §6 seeded fallback, labeled SEEDED everywhere, with no experiment candidate among the seeded-new postings and no Claude output shown
  on the 20 candidates. One final real fetch around 21:00 EDT, on request only. No rebalancing of the 20; the report states the class balance and the
  always-not_relevant baseline as a named limit.
- **Changed (Sat Oct 31 13:42:55 to 13:43:13 EDT 2026):** Test first: `test_seeded_label_is_carried_in_report` failed (`TypeError: run() got an unexpected
  keyword argument 'label'`). Then `run(..., label=None)` and `--label` were added. A labeled report starts with `"label": "SEEDED"`, and the CLI
  prints `*** SEEDED ***`. Result: `Ran 47 tests`, `OK`.

---

## F24. SEEDED fallback run with the Claude judge

- **Constructed (Sat Oct 31 13:43:32 EDT 2026):** `seeded/SEEDED-earlier-response-zoox-2026-10-30-minus-5.json` is the real day-1 response with 5
  postings removed (222 left; sha256 `6be09bb7…5c1e63`). The manifest is in `seeded/SEEDED-MANIFEST.json`. `8321d00e` (Senior Network Security Engineer) was removed
  **deliberately**, as the only Gate-1 include posting outside the 20. The 4 others were drawn with `random.Random(20261031).sample` from the IDs outside the 20. None of the 20 candidates
  was removed. The seeded runs used a separate state file, `seeded/SEEDED-state.json`. The real `state/seen_ids.json` stayed at sha256 `54a6a3cd…` before and after.
- **Ran:** SEEDED run 1 (13:43:41): `baseline=True total=222 new=0`. SEEDED run 2 (13:43:42 to 13:44:14), real `raw/2026-10-31/zoox.json` against the SEEDED
  state, with `--judge claude`: `new=5 removed=0`. There were 5 `claude -p` calls (claude-opus-5-5), one session each, and the raw output is in `seeded/SEEDED-judgments/`.
- **Result (record vs judgment):**
  - 8321d00e Senior Network Security Engineer: record relevant; judgment **accepted**, relevant (9 citations), session `f57c3f69…`
  - 48639085 Senior Director, Head of Talent Acquisition: record not_relevant; judgment **rejected**, session `3bac5e88…`
  - 5de4079e Senior Signal Integrity and EMC Engineer: record not_relevant; judgment **rejected**, session `34009517…`
  - f62f1083 Senior Software Engineer - Robot Software Infrastructure: record not_relevant; judgment **rejected**, session `295e104d…`
  - eed5bd1e Team Lead, Ground Operations (3rd Shift): record not_relevant; judgment **rejected**, session `383038ee…`
- **Why the 4 were rejected (validator errors, verbatim in the report):** Each cited a résumé path the CONTRACT path convention does not support. Two used a list
  index (`education.0.degree`), and two used a list of objects with a bullet or title as the value (`experience`). The quoted values do occur in the résumé, but `resume_value_at`
  follows only dict keys. Nothing was repaired. `prompts/judge_v1.md` gives examples of paths but does not forbid numeric indices.
- **Also seen (not a validator failure):** In the not_relevant answers, Claude paired résumé values with unrelated posting text (for example `skills.networking: BGP` with
  "15+ years of TA leadership experience"). Those citations pass, because each side exists. This is a live example of NOT-CHECKED item 1.
- **Open (decision for Prathamesh):** Whether to forbid indices in the prompt, teach the validator indices, or leave it as is. This could be the "one change"
  in the prompt experiment, but changing it now would touch the baseline prompt before the experiment.

My take: Less convincing. I built the change myself, so it tests what I expected to happen, not what the board actually does. It proves the mechanism works, not that the watch catches real changes.

---

## F25. Experiment report skeleton, action-surface facts, README draft

- **Changed (Sat Oct 31 around 13:45 EDT 2026):** `experiment/REPORT.md` is a skeleton with no numbers. It has the class-balance and always-not_relevant table, and limits that name
  the non-rebalanced set and the 10-case held-out sample. `ACTION-SURFACES.md` drafts the facts for (b) "give Claude a file" (**not yet performed**) and (c) "agent
  fetches and writes state" (what ran, with dates). (a) is left blank for Prathamesh, as is the least-autonomy choice. `README.md` is a draft with a REAL vs SEEDED runs table.

---

## F26. Pre-experiment prompt fix: résumé paths (validator not loosened)

- **Decision (Prathamesh, 2026-10-31):** The 4 SEEDED rejections (F24) were a format bug, not a difference in judgment. Fix the prompt and do not loosen the validator.
  The edited file becomes the experiment's baseline v1.
- **Changed (Sat Oct 31 13:52:57 to 13:53:20 EDT 2026), before any sampling or experiment call:** `prompts/judge_v1.md` now says `resume_field` must be a dotted
  path of dictionary keys only. List indexes such as `education.0.degree` are forbidden, and so are lists of objects (`experience`, `education`, `projects`). It lists the exact 28
  paths the validator can resolve in `fixtures/resume.fictional.json`. `jobwatch.py` was not changed.
- **Hashes:** pre-fix template `3be1ef3b7a0752b002ca5d6395459f9daf1016b745dac188379f0725ac70bb98`, kept verbatim as
  `prompts/archive/judge_v1.PRE-FIX-used-2026-10-30-and-SEEDED-2026-10-31.md`. **Baseline v1 template
  `f55c7c68cf04c36ecd3300c8dacd48b1243644fd47e051604557e5927f946272`.** Both are recorded in `prompts/PROMPT-HASHES.md`.
- **Test added:** `test_prompt_allowed_resume_paths_match_what_validator_resolves` checks that the prompt's allowed list equals the set of résumé paths the validator
  resolves, and that `education.0.degree` and `experience` are still rejected. Result: `Ran 48 tests`, `OK` (13:53:20).
- **Evidence kept:** The SEEDED run 2 report and the 5 raw judgments in `seeded/SEEDED-judgments/` are unchanged. They were produced with the pre-fix template.
- **Not tested yet:** whether the fixed prompt actually stops index paths. No Claude call has been made with it.

---

## F27. ALTERNATIVES.md and the action-surface (a) placeholder

- **Changed (Sat Oct 31 around 13:54 EDT 2026):** Created `ALTERNATIVES.md`. Section (a) holds the documented LinkedIn job-alert behavior and the 3 source URLs, exactly as
  Prathamesh supplied them (retrieved 2026-10-31 by Claude in claude.ai). Claude Code did **not** open or verify these URLs. Section (b), hands-on, is blank for Prathamesh.
  Added a blank "(a) What I saw pasting a posting into a chat assistant" section to `ACTION-SURFACES.md`.

---

## F28. Prathamesh's hands-on LinkedIn observation recorded

- **Happened (Sat Oct 31 14:15 EDT 2026):** Claude Code inserted Prathamesh's own hands-on observation (written by Prathamesh, 2026-10-31 ~14:00 EDT) **verbatim**
  into `ALTERNATIVES.md` section (b). A programmatic check confirmed that the supplied text appears in the file unchanged. **The wording and the observation are Prathamesh's.**
  Claude Code did not visit LinkedIn and has not verified anything in it.
- **Factual cross-check against the current agent (Claude Code, 14:15:17 EDT, no change made):** The three things the observation says the agent should do are
  **not implemented**:
  - checking that a posting is still open (not verified: whether the Lever public postings endpoint lists only open postings);
  - quoting the sponsorship line, or labeling it "posting is silent";
  - flagging experience requirements.
  Also, the Gate 2 phrase list returns **no hit** on the quoted Parallel Wireless wording "authorized to work in the U.S. without sponsorship"
  (tested on the sentence "Candidates must be authorized to work in the U.S. without sponsorship."). The CONTRACT phrase list contains no "sponsorship" phrase.
  None of this has been changed. Any change needs a CONTRACT amendment by Prathamesh first.

My take: What surprised me most was that LinkedIn still showed postings marked "No longer accepting applications" in search results. I assumed a job board would at least filter out closed jobs.

---

## F29. Gate 2 amended: sponsorship-refusal phrases

- **Decision (Prathamesh, 2026-10-31, from the hands-on LinkedIn check in ALTERNATIVES.md (b)):** Add 8 sponsorship-refusal phrases to Gate 2
  ("without sponsorship", "without visa sponsorship", "no sponsorship", "not sponsor", "will not sponsor", "unable to sponsor", "cannot sponsor",
  "does not sponsor"), using the same whole-word, case-insensitive, optional-"s" rules. Do not add a bare "sponsorship".
- **Order (all on Sat Oct 31 2026):**
  - 14:16:53: snapshot of all 227 rule verdicts on `raw/2026-10-30/zoox.json` (2 relevant) with the existing code.
  - 14:16:58: CONTRACT §4 amendment, dated, with the reason.
  - Tests: `test_auth_sponsorship_refusal_phrases` (8 sentences, including the Parallel Wireless wording) **failed on all 8 subtests** at 14:17:13.
    `test_sponsorship_available_is_not_a_hit` ("Visa sponsorship available", "H-1B sponsorship", "Sponsorship: yes") passed before the change, as it should.
  - Code: 8 phrases added to `AUTH_PHRASES`.
  - 14:17:33: `Ran 50 tests`, `OK`.
- **Citation choice (Claude Code; stated in the amendment):** No `constraints.excluded` entry names sponsorship refusal, so a hit cites `visa.needs_sponsorship` and
  `visa.type` instead. The fictional résumé was not changed.
- **Re-run of the rule only (14:17:33):** 227 postings, **0 verdicts changed**, 0 Gate 2 hits, and still 2 relevant. Only 1 of the 227 postings mentions "sponsor" at all
  ("Staff Vehicle Attributes Engineer": "Company visa sponsorship and relocation assistance details will be pro[vided]"), which is not a refusal phrase.
  The watch was not re-run. `state/seen_ids.json` is unchanged (sha256 `54a6a3cd…`).
- **Not done:** The other two items in ALTERNATIVES.md (b) are still not implemented: the open-posting check and flagging experience requirements.

My take: My tests checked what I thought to test, not what actually matters to me. Passing 48 tests proved the code did what I wrote, not that I wrote the right thing.

---

## F30. Labeling rule finalized; labels saved

- **Decisions (drafted by Claude in claude.ai chat, reviewed and approved by Prathamesh, 2026-10-31):** "3+ years required" is acceptable; 4 or more required years is not fit; a
  Senior/Staff/Principal/Lead/Manager/Director title is not fit even with no years stated; only required years count.
- **Changed (Sat Oct 31 14:21 EDT 2026):** The decisions were added to the rule. DRAFT was removed, and the file was renamed `experiment/LABELING-RULE-DRAFT.md` → `experiment/LABELING-RULE.md` (the draft file was deleted).
  References in `LABELING-SHEET.md` and `REPORT.md` were updated.
- **Labels saved (recorded_at 2026-10-31T14:21:32-0400):** `experiment/labels.json` holds 20 labels with reasons verbatim, **all 20 "not fit"**. Provenance as stated: drafted by Claude (claude.ai chat)
  from the sheet excerpts, then reviewed and approved by Prathamesh before seeing any Claude judge output on these postings. The numbering was checked against `candidates.json` order.

---

## F31. Sampling: 5 dev postings × 4 fresh `claude -p` calls (baseline v1)

- **Selection (14:22:14 EDT):** #8 and #6 (required), plus 3 drawn with `random.Random(20261031).sample` from the other 8 dev postings: #5, #7, #10. Recorded in `experiment/sampling_selection.json`.
- **Ran (Sat Oct 31 14:22:21 to 14:23:01 EDT 2026):** `experiment/run_judge_batch.py` (new, stdlib, reusing `jobwatch.claude_judge` and the validator; never overwrites a results file)
  with `prompts/judge_v1.md` (sha256 `f55c7c68…`). 20 calls, 20 distinct session IDs, **20/20 accepted** by the validator (0 path rejections after the F26 fix).
- **Result:** All 5 postings were unanimous across 4 calls. #8 "Staff Network Security Architect" was `relevant` 4/4, against the label not fit. The other 4 were `not_relevant` 4/4, matching the label.
  Report: `experiment/SAMPLING-REPORT.md`, with every verdict, session ID and timestamp.

My take: Getting the same answer every time isn't the same as being right. Sampling tells me how stable the answers are, not whether they're accurate, so I still need labels I checked myself.

---

## F32. Prompt experiment: v1 vs v2 on dev, then v2 once on held-out

- **Change (14:21:45 EDT):** `prompts/judge_v2.md` (sha256 `99ff0126…`) is v1 plus criterion 4 (seniority, matching LABELING-RULE.md). `diff` shows only those 3 added lines.
- **Ran (Sat Oct 31 2026, one call per posting):**
  - dev v1, 14:23:09 to 14:23:28: **9/10**, 1 false positive (#8), 0 rejected.
  - dev v2, 14:23:28 to 14:23:45: **10/10**, 0 false positives, 0 rejected.
  - **held-out v2, run ONCE**, 14:23:54 to 14:24:11: **9/10**, 0 false positives, **1 rejected** (#14 IAM Manager).
  - The trivial "always not_relevant" baseline scores 10/10 on both splits, because all labels are not fit.
- **Held-out rejection, investigated after the run:** Claude quoted "…SCIM, Kerberos…" with an ordinary space, and the posting has U+00A0 (a non-breaking space) before "Kerberos", so the verbatim check failed.
  Its verdict was `not_relevant`, matching the label, but it is counted as a fail. Nothing was repaired, and **no prompt or validator change was made after seeing held-out**.
- **Scoring:** `experiment/score.py` (new) computes everything into `experiment/results/summary.json`. `experiment/REPORT.md` is generated from it, with the limits Prathamesh specified:
  (a) all labels are not fit, so the trivial baseline is 100% and false positives are the measure; (b) Claude-drafted labels make this partly Claude against Claude. The report adds limits on the 10-case sample,
  single runs, exposure, and false negatives being unmeasurable.
- **Totals:** 50 Claude calls today for sampling and the experiment (20 + 10 + 10 + 10). Raw outputs are under `experiment/raw-judgments/`.
- **Correction (14:26 EDT):** Claude Code's CONTRACT §4 "known coarseness" note says "no clearance required" trips Gate 2. Checked: it does **not** (bare "clearance" is not a phrase), but "No security clearance required" does. NOT-CHECKED.md was corrected. The CONTRACT sentence was left unchanged for Prathamesh to amend.
- **NOT-CHECKED.md:** Claude Code proposed 2 more items (judge false negatives; Unicode whitespace in citation matching). They are pending Prathamesh's confirmation.

My take: Not yet. I'd trust v2 more if it did better on postings it hadn't seen before, judged against labels I wrote before seeing its output, across more examples than one small run.

---

## F33. Prathamesh's hands-on chat-assistant observation recorded (action surface (a))

- **Happened (Sat Oct 31 14:36:37 EDT 2026):** Claude Code inserted Prathamesh's own hands-on observation (written by Prathamesh, 2026-10-31 ~14:30 EDT) **verbatim** into
  `ACTION-SURFACES.md` under "(a) What I saw pasting a posting into a chat assistant". A programmatic check confirmed that the supplied text appears in the file unchanged.
  **Provenance (corrected 2026-10-31 14:41 EDT):** everything through "What could go wrong" is Prathamesh's own observation and wording. The final paragraph, "Compared with my agent", was drafted by Claude (claude.ai chat) from the run records and approved by Prathamesh. Claude Code did not see those chats.
- **Revised at Prathamesh's instruction (14:41 EDT):** In that final paragraph, "(both runs used the pre-fix v1 template)" was added after "Claude judge v1", and the last sentence was replaced with Prathamesh's wording about the agent having no explicit 'silent' output. The (a) table was filled, marked "summarized by Claude Code from Prathamesh's observation".
- **Factual cross-references (Claude Code; Prathamesh's text not edited):**
  - The agent's two Claude judgments on "Senior Network Security Engineer" (`8321d00e`) were both accepted as `relevant`: the smoke test on 2026-10-30 18:41 (F17) and the SEEDED run on 2026-10-31 13:43 (F24).
    Both used the **pre-fix** v1 template (sha256 `3be1ef3b…`), not the experiment baseline v1 (`f55c7c68…`). The record (rule) is also `relevant`, with 6 skills matched (F13).
  - The agent produces no explicit "posting is silent" output on sponsorship. Its record only shows that Gate 2 had no hits (see ALTERNATIVES.md (b) and F28).
  - Attempt 1 involved dev candidate #8. It is a dev posting, not held-out.

My take: For a one-off check of a single posting I've already found. When I pasted the Zoox posting into a chat, it caught the 8+ years requirement, said the posting was silent on sponsorship, and quoted real text. I'd use the agent when I need to repeat the check, keep a record, or compare across days.

---

## F34. Provenance split for action surface (a); NOT-CHECKED confirmed; CONTRACT example corrected; FRICTIONAL restructured; README

- **Changed (Sat Oct 31 14:41 EDT 2026), at Prathamesh's instruction:**
  - ACTION-SURFACES.md (a): provenance split recorded (see F33); final paragraph revised; table filled (summarized by Claude Code).
  - NOT-CHECKED.md: Prathamesh confirmed all 5 Claude-proposed items (2026-10-31), moved under "Confirmed by Prathamesh" as items 2–6.
  - CONTRACT §4 "known coarseness": the example was corrected ("No security clearance required" is a hit; bare "clearance" is not), dated, with the reason that the earlier example was wrong.
  - FRICTIONAL: "My take:" lines kept only on Prathamesh's decision entries (list at the top). The empty lines were removed from the others, and the suggestions-log Status was filled where the record shows a decision.
  - README.md written per the brief. Signed/withheld and "Why this judgment stays mine" are left blank for Prathamesh.

---

## F35. Write-limit check; Prathamesh's writing inserted; sign-off

- **Tried (Sat Oct 31 14:55:01 EDT 2026):** Searched `jobwatch.py` for path-confinement code (resolve/relative_to/commonpath/ROOT): none was found. Then ran
  `python -I jobwatch.py run --raw raw/2026-10-30/zoox.json --state <scratchpad>/state.json --out <scratchpad>/out.json`. It exited 0 and wrote both files **outside the project folder**.
  The real `state/seen_ids.json` was unchanged (`54a6a3cd…`).
- **Changed:** Per Prathamesh's instruction for this outcome, the "not enforced" sentence went into ACTION-SURFACES.md, and NOT-CHECKED.md item 7 was added. Prathamesh's writing was inserted verbatim:
  11 My take lines, 7 suggestion statuses, the "Why this judgment stays mine" column (11 rows), the least-autonomy choice, and the README sign-off ("Signed. Prathamesh, 2026-10-31.").
  The three lines Claude (claude.ai) edited are recorded in SOURCES.md, and the ⟨edited⟩ markers were removed when inserting. The BLS SOC 15-1241 citation was added.

---

## F36. Stale-status cleanup, privacy scan, backup commit

- **Changed (Sat Oct 31 14:58 EDT 2026):** SOURCES records the course AI policy as reviewed by Prathamesh (2026-10-31). The README header now says it was drafted by Claude Code, Prathamesh's sections were written by Prathamesh, and it was signed by Prathamesh on 2026-10-31.
  The stale-wording scan (not written yet / to be completed / DRAFT / pending / awaiting / not yet / skeleton / placeholder / TODO) found outdated **current-status** wording only in the SOURCES status column, which was fixed (9 rows).
  Left as is: the dated FRICTIONAL entries (historical log), ACTION-SURFACES (b) "not yet performed" (still true), the README note that the final fetch is not yet run (still true), and a test skip message (shown only if hand_labels.json is missing).
- **Privacy scan (14:58:55 EDT, folder excluding shieldai.json):**
  - Emails: only `accommodations@zoox.com` (814 occurrences, all in raw or seeded postings) and the fictional `tanvi.kulkarni@example.com`. The test-only negative cases `someone@gmail.com`, `x@example.com.evil.org` and `api.lever.co@evil.example` are inputs the tests expect to be refused.
  - No local paths or Windows username in any file. The only match was the README title "(Prathamesh P.)", the course name format.
  - No tokens. The token-pattern hits were posting text ("bearer tokens, JWT validation") and "Work authorization:". The headers contain no set-cookie.
  - The only résumé file is `fixtures/resume.fictional.json`.
- **.gitignore:** `raw/2026-10-30/shieldai.json` (10.5 MB) was added. Its fetch metadata, headers and SHA256SUMS stay tracked.
- **Tests before commit:** 50/50 OK (14:58:55 EDT). Staged: 111 files under this folder only, with no shieldai.json, pycache or resume.json.

---

## Claude suggestions log

| When | Suggestion | Status (Prathamesh) |
|---|---|---|
| 2026-10-30 18:14 | Board = zoox | accepted (Prathamesh, 2026-10-30) |
| 2026-10-30 18:14 | flag → not_relevant with needs_human | accepted (Prathamesh, 2026-10-30) |
| 2026-10-30 18:14 | Gate 2 phrase list and Gate 3 threshold of 2 | accepted in the approved CONTRACT (2026-10-30); Gate 2 later modified by Prathamesh (whole word, plural, sponsorship phrases); threshold 2 kept |
| 2026-10-30 18:14 | Wrong versions W1 (uncited justification) and W2 (mis-joined verdicts) | accepted in the approved CONTRACT (2026-10-30) |
| 2026-10-30 18:23 | Gate 3 whole-word literal ("firewalls" ≠ "firewall"); state shape `{"ids": [...]}` | modified: plurals count; state = exactly the last run (Prathamesh, 2026-10-30) |
| 2026-10-30 18:26 | The 10 hand-prediction candidates (7 chosen as near-misses) | accepted (used: Prathamesh supplied predictions for all 10, 2026-10-30) |
| 2026-10-30 18:33 | Hyphen counts as a word boundary in Gate 2 ("ITAR-controlled" is a hit) | accepted (Prathamesh, 2026-10-31) |
| 2026-10-30 18:35 | Strengthen `test_W2_verdict_attached_to_correct_posting` so the new posting is not at index 0 (mutation check) | accepted (Prathamesh, 2026-10-30) |
| 2026-10-30 18:40 | Judge prompt v1 without a seniority criterion | modified: kept as the baseline; seniority added as the v2 change (Prathamesh, 2026-10-31) |
| 2026-10-30 18:40 | Judge CLI isolation: `--tools ""`, `--strict-mcp-config`, empty cwd | accepted (Prathamesh, 2026-10-31) |
| 2026-10-30 18:42 | The 11 near-miss picks for the experiment | accepted ("Keep the 20 as they are", Prathamesh, 2026-10-31) |
| 2026-10-30 18:42 | Labeling-rule draft (seniority more than about 3 years, or a Senior+ title, is not fit) | modified: 3+ OK, 4+ not fit, Senior+ title not fit, required years only (Prathamesh, 2026-10-31) |
| 2026-10-31 13:43 | Deliberately include 8321d00e among the SEEDED removals (the only rule-relevant non-candidate) | accepted (Prathamesh, 2026-10-31) |
| 2026-10-31 13:45 | Address index paths in the judge prompt or the validator (open) | resolved by Prathamesh: fix the prompt, not the validator (2026-10-31) |
| 2026-10-31 13:53 | Test that the prompt's allowed-path list equals the validator-resolvable paths | accepted (Prathamesh, 2026-10-31) |
| 2026-10-31 14:17 | Sponsorship-refusal hits cite visa.needs_sponsorship and visa.type (no constraints.excluded entry) | accepted (Prathamesh, 2026-10-31) |
| 2026-10-31 14:22 | Sampling extras #5, #7, #10 by seeded draw; 4 parallel workers | accepted (Prathamesh, 2026-10-31) |
| 2026-10-31 14:24 | Scoring: a rejected output counts as a fail; false positive = accepted relevant on not fit | accepted (Prathamesh, 2026-10-31) |
