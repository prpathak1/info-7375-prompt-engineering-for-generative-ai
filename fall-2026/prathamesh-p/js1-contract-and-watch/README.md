# JS1: The Contract and the Watch (Prathamesh P.)

One public board (Lever, `zoox`), one **fictional** résumé, new postings only, and every verdict justified with cited résumé and posting fields.
Each new posting gets a deterministic **record**, a rule that anyone can recompute, and a Claude **judgment**, a model opinion that passes a strict validator or is stored as rejected.

> Drafted by Claude Code. Prathamesh's sections (the sign-off, the "Why this judgment stays mine" column, and the least-autonomy choice in ACTION-SURFACES.md) were written by Prathamesh (see SOURCES.md for the three lines Claude edited). Signed by Prathamesh on 2026-10-31.

## Language, toolchain, exact commands

- **Language:** Python 3.13.1, standard library only (`urllib`, `json`, `re`, `hashlib`, `subprocess`, `unittest`). No third-party packages.
- **Model access:** Claude Code CLI 2.1.314 (`claude -p`), logged in to the user's Claude account. Only the `--judge claude` and `experiment/run_judge_batch.py` paths need it.
  Tests and the rule run offline.
- **Network:** only `https://api.lever.co`, for one GET per `fetch`.

Fresh clone (the branch must be pushed first; nothing is committed as of this draft):

```bash
git clone https://github.com/prpathak1/info-7375-prompt-engineering-for-generative-ai.git
cd info-7375-prompt-engineering-for-generative-ai
git checkout prathamesh-p-js1-contract-and-watch
cd fall-2026/prathamesh-p/js1-contract-and-watch
python -I -m unittest discover -s tests -v          # 50 tests, offline
python -I jobwatch.py run --raw raw/2026-10-30/zoox.json --state /tmp/js1-state.json --out /tmp/js1-run.json   # recompute a baseline without touching state/
```

Live commands (these make network or Claude calls):

```bash
python -I jobwatch.py fetch --board zoox --raw-dir raw                       # one GET; refuses to overwrite raw/<date>/
python -I jobwatch.py run --raw raw/<date>/zoox.json --state state/seen_ids.json --out runs/<name>.json --judge claude
python -I jobwatch.py judge --raw raw/2026-10-30/zoox.json --posting-id <id>  # one posting; never touches state
python -I experiment/run_judge_batch.py --prompt prompts/judge_v2.md --split dev --out experiment/results/<new>.json
python -I experiment/score.py                                                 # recompute every experiment number
```

*What was checked about the fresh-clone path:* on 2026-10-31 at 14:42 EDT, the folder was copied without `__pycache__` and without the ShieldAI raw file, and the 50 tests passed (`OK`) in that copy.
A real `git clone` of the pushed branch has **not** been run yet.

## What actually ran: REAL vs SEEDED

| Run | When (EDT) | Input | Result | Kind |
|---|---|---|---|---|
| Fetch day 1 | 2026-10-30 18:11:44 | one GET api.lever.co/zoox | HTTP 200, 227 postings, sha256 `45a795df…17eeb6` | **REAL** |
| Run 1 (baseline) | 2026-10-30 18:35:23 | `raw/2026-10-30/zoox.json` | new=0 / 227; state saved (`54a6a3cd…`) | **REAL** |
| Fetch day 2 | 2026-10-31 13:27:48 | one GET api.lever.co/zoox | HTTP 200, 227 postings, **identical** sha256 and ETag; new server `Date` | **REAL** |
| Run 2 | 2026-10-31 13:27:58 | `raw/2026-10-31/zoox.json` | new=0, removed=0 (correct on an identical response) | **REAL** |
| SEEDED run 1 | 2026-10-31 13:43:41 | `seeded/SEEDED-earlier-response-zoox-2026-10-30-minus-5.json` (**constructed**: day 1 minus 5 postings) | new=0 / 222 | **SEEDED** |
| SEEDED run 2 | 2026-10-31 13:43:42–13:44:14 | real `raw/2026-10-31/zoox.json` vs SEEDED state, `--judge claude` | new=5; judgments: 1 accepted, 4 rejected (résumé-path format, pre-fix prompt) | **SEEDED** |
| Judge smoke test | 2026-10-30 18:41:32–43 | `8321d00e` | accepted, relevant | Claude judgment |
| Sampling | 2026-10-31 14:22:21–14:23:01 | 5 dev × 4 fresh calls, v1 | 20/20 accepted; all unanimous | Claude judgments |
| Experiment | 2026-10-31 14:23:09–14:24:11 | dev v1, dev v2, held-out v2 once | 9/10, 10/10, 9/10 (1 rejected) | Claude judgments |

The SEEDED files live only under `seeded/`, every file name starts with `SEEDED-`, and every SEEDED report starts with `"label": "SEEDED"`. They exist because the real board did not change
between the two days, and they **do not** show a real board change. A final real fetch on 2026-10-31 evening is planned *(not yet run)*.

## Artifacts

| What | Where |
|---|---|
| Contract (APPROVED, with dated amendments) | [CONTRACT.md](CONTRACT.md) |
| Code | [jobwatch.py](jobwatch.py), [experiment/run_judge_batch.py](experiment/run_judge_batch.py), [experiment/score.py](experiment/score.py) |
| Tests | [tests/test_jobwatch.py](tests/test_jobwatch.py), with hand predictions in [tests/hand_labels.json](tests/hand_labels.json) ([provenance](tests/hand_labels.PROVENANCE.md)) |
| Fictional résumé | [fixtures/resume.fictional.json](fixtures/resume.fictional.json) |
| Raw responses | [raw/2026-10-30/](raw/2026-10-30/), [raw/2026-10-31/](raw/2026-10-31/) (body, headers, fetch metadata, SHA-256) |
| State from both runs | [state/seen_ids.after-run1-2026-10-30.json](state/seen_ids.after-run1-2026-10-30.json), [state/seen_ids.after-run2-2026-10-31.json](state/seen_ids.after-run2-2026-10-31.json) |
| Run reports | [runs/](runs/), with SEEDED material in [seeded/](seeded/) ([manifest](seeded/SEEDED-MANIFEST.json)) |
| Judge prompts | [prompts/judge_v1.md](prompts/judge_v1.md), [prompts/judge_v2.md](prompts/judge_v2.md), [prompts/archive/](prompts/archive/), [hashes](prompts/PROMPT-HASHES.md) |
| Raw Claude responses | [judgments/](judgments/), [seeded/SEEDED-judgments/](seeded/SEEDED-judgments/), [experiment/raw-judgments/](experiment/raw-judgments/) |
| Sampling report | [experiment/SAMPLING-REPORT.md](experiment/SAMPLING-REPORT.md) |
| Prompt experiment | [experiment/REPORT.md](experiment/REPORT.md), [labeling rule](experiment/LABELING-RULE.md), [labels](experiment/labels.json), [candidates](experiment/candidates.json), [results](experiment/results/) |
| Action-surface comparison | [ACTION-SURFACES.md](ACTION-SURFACES.md) |
| Alternatives (LinkedIn) | [ALTERNATIVES.md](ALTERNATIVES.md) |
| Not checked | [NOT-CHECKED.md](NOT-CHECKED.md) |
| Sources and Claude's contribution | [SOURCES.md](SOURCES.md) |
| Frictional log | [FRICTIONAL.md](FRICTIONAL.md) |

## Sign-off

### Checked properties, named tests, method

Methods used:
- **(T)** Tests written by Claude Code from CONTRACT.md *before* the implementation existed, then approved by Prathamesh (and amended only through dated contract changes). The tests were written by Claude Code, not by Prathamesh.
- **(H)** Hand predictions, drafted by Claude (claude.ai chat) by applying the rule by hand, and approved by Prathamesh before the implementation existed.
- **(M)** Mutation check: the tests were run against deliberately broken copies of the code.
- **(R)** Recomputation of the rule over saved raw data.

| Property | Named tests / evidence | Method |
|---|---|---|
| Only `https://api.lever.co` is fetched; lookalikes, userinfo, http, odd ports and off-host redirects are refused, and nothing is written on refusal | `AllowList.test_refuses_off_list_hosts`, `test_refuses_non_https_and_odd_ports`, `test_refuses_redirect_off_host_and_writes_nothing`, `test_accepts_lever_https` | T |
| One GET and no send paths in the source | `AllowList.test_source_has_one_get_and_no_send_paths` | T |
| Only a résumé with `"fictional": true` and an `@example.com` address loads | `ResumeLoader.*` (3 tests) | T |
| Rule Gate 1 (title, reused from the Reallocation-mode filter), including the false friend "Road Network Tools" in real data | `Rule.test_road_network_tools_is_not_relevant_in_real_day1_data`, `_synthetic`, `test_other_false_friends_and_no_network`, `test_flag_*`, `test_verdict_is_two_valued` | T |
| Gate 2 phrases: whole word, plural, hyphen boundary, sponsorship refusal; "sponsorship available" is not a hit | `Rule.test_auth_*`, `test_sponsorship_available_is_not_a_hit` | T |
| Gate 3 skills: threshold 2, whole word with plural, reads lists with HTML stripped; location ignored | `Rule.test_skills_*`, `test_location_is_not_a_criterion` | T |
| The rule agrees with the hand predictions on 10 real postings (10/10) | `Rule.test_hand_labels_if_present`; `runs/2026-10-30-hand-label-comparison.json` | H, R |
| **W1**: no uncited or fabricated justification | `W1UncitedJustification.*` (3), `Validator.test_rejects_uncited_or_fabricated_justification` | T, M (the W1 mutant failed 20 assertions across 9 tests) |
| **W2**: each verdict belongs to its own posting | `Watch.test_W2_verdict_attached_to_correct_posting` (strengthened after M), `test_W2_many_new_postings_each_carry_their_own_verdict` | T, M (the W2 mutant fails both after strengthening) |
| Baseline = 0 new; second run = unseen IDs only; state = exactly the last run; failed run leaves state untouched | `Watch.test_baseline_*`, `test_second_run_reports_only_unseen_ids`, `test_state_equals_exactly_current_run_ids`, `test_failed_run_leaves_state_untouched`, `test_rerun_same_day_reports_zero_new` | T; also REAL runs 1 and 2 |
| Claude output must match the fixed schema, otherwise it is rejected and never repaired | `Validator.test_rejects_off_schema` (14 cases), `Watch.test_rejected_judgment_is_stored_as_rejected_not_repaired`, `JudgeHarness.test_fenced_output_is_rejected_and_kept_verbatim` | T |
| Judgment never changes the record | `Watch.test_judgment_never_changes_record` | T |
| Each judge call is fresh (`-p --no-session-persistence`, new session ID, no tools) and the raw output is saved before validation | `JudgeHarness.*` (5 tests); 50 distinct session IDs in `experiment/results/` | T, R |
| The prompt's allowed résumé paths equal what the validator resolves | `JudgeHarness.test_prompt_allowed_resume_paths_match_what_validator_resolves` | T |
| SEEDED output is labeled in the report | `Watch.test_seeded_label_is_carried_in_report` | T |
| Experiment numbers | `experiment/score.py` → `experiment/results/summary.json` | R |

### Not checked
From [NOT-CHECKED.md](NOT-CHECKED.md), all confirmed by Prathamesh:
1. **Citation relation.** The validator checks that each citation's sides *exist*, not that they refer to the same thing.
2. **Headless context.** Whether `claude -p` loads user-level settings or memory despite the empty working directory.
3. **Gate 2 matches phrases, not meaning.** "No security clearance required" is a hit; "No clearance required" is not.
4. **Real fit.** Whether the rule captures real fit. It ignores seniority by design.
5. **Judge false negatives.** All 20 experiment labels are "not fit", so these were unmeasurable.
6. **Unicode whitespace.** A non-breaking space quoted as an ordinary space is rejected.

7. **Write confinement.** Writes are not confined to the project folder; they go to the paths given on the command line (checked 2026-10-31 14:55 EDT).

Also not checked: a real `git clone` of the pushed branch, and whether Lever's public endpoint lists only open postings.

### Claims not made
- Not that the rule (record) captures real fit for the persona. It deliberately ignores seniority, and it marked #8 "Staff Network Security Architect" relevant against the label.
- Not that the Claude judge is correct. Agreement with the labels is partly Claude against Claude, because the labels were Claude-drafted and human-reviewed.
- Not that v2 is better than doing nothing. The trivial "always not_relevant" baseline scored 100% on both splits, and the dev improvement rests on one posting.
- Not that 4-of-4 agreement in sampling means correctness or stable behavior on other postings.
- Not that the watch detected a real board change. The real day-2 response was identical, and the 5 "new" postings are **SEEDED**.
- Not that any result generalizes beyond Zoox's Lever board, beyond this fictional persona, past 2026-10-31, or to other Claude models or versions.
- Not that LinkedIn behaves as documented generally. ALTERNATIVES.md (b) is one hands-on look on one date.
- Not that the agent applies, emails, messages or logs in. There is no such code path, and that absence is all that is claimed.

### Signed or withheld

I have read this README and I stand behind it.

Signed. Prathamesh, 2026-10-31.

### Driver's seat

| Decision / work | What Claude did | What Prathamesh did | Why this judgment stays mine | Evidence |
|---|---|---|---|---|
| Board and scope | Captured both boards; surveyed them; recommended zoox | Chose zoox; chose the two-valued verdict and the folder | Only I know which boards and roles fit my situation and my visa status. | FRICTIONAL F1, F3, F5; CONTRACT §1.1 |
| Contract and Failure sentence | Drafted CONTRACT.md; Claude (claude.ai) drafted the §7 sentence | Reviewed and approved the contract and §7; made every dated amendment (Gate 2 whole word, plural, sponsorship; Gate 3 plural; state; coarseness example) | The harm happens to me, so I decide what counts as failure. | CONTRACT §§4, 6, 7; FRICTIONAL F5, F8, F9, F15, F29, F34 |
| Tests | Claude Code wrote the tests from the contract before the code; ran mutation checks; proposed the W2 strengthening | Approved the tests; required that none be weakened; ordered the W2 strengthening | Claude can write tests that its own code passes, so I decide what the tests must catch. | `tests/test_jobwatch.py`; FRICTIONAL F6, F7, F11, F14 |
| Hand predictions (rule) | Claude (claude.ai) drafted 10 predictions; Claude Code selected the 10 postings | Reviewed and approved the predictions before the code existed | They only mean something if I commit to them before seeing the output. | `tests/hand_labels.json` + PROVENANCE; F10, F13 |
| Implementation and runs | Claude Code wrote `jobwatch.py`, ran the fetches and runs, built the SEEDED fallback | Scheduled day 2; kept the real new=0 run; authorized SEEDED and set its constraints | I'm responsible for what runs on my machine and what it touches. | `raw/`, `runs/`, `seeded/`; F12, F20, F23, F24 |
| Judge prompt | Claude Code wrote judge_v1 and the harness; diagnosed the path-format rejections | Decided to fix the prompt, not loosen the validator; set v2 = one seniority change | The prompt's wording decides what "relevant" means, so I decide that wording. | `prompts/`, PROMPT-HASHES.md; F16, F24, F26, F32 |
| Labeling rule and labels | Claude Code drafted the rule; Claude (claude.ai) drafted the seniority decisions and the 20 labels | Reviewed and approved both before any judge output; refused to rebalance | The labels are the answer key. Here Claude drafted them and I only reviewed them, so the experiment is partly Claude grading Claude. That's the weakest part of this work, and next time I'll write the labels myself. | `experiment/LABELING-RULE.md`, `labels.json`; F30 |
| Sampling and experiment | Claude Code selected, ran (50 calls), scored, and wrote the reports | Specified the design (5×4, v1 vs v2, held-out once, no tuning after); named the limits | I decide how much evidence is enough to switch versions. | `experiment/`; F31, F32 |
| Hands-on comparisons | Claude Code inserted the texts verbatim and summarized the (a) table; Claude (claude.ai) drafted the "Compared with my agent" paragraph | Did the LinkedIn check and both chat-paste attempts, and wrote those observations | Only I can say what I actually saw on my own screen. | ALTERNATIVES.md (b), ACTION-SURFACES.md (a); F28, F33 |
| Least autonomy | Drafted the facts for surfaces (b) and (c); checked the write limit | Chose and defended the least autonomy that is enough (ACTION-SURFACES.md) | I decide how much the agent can do, because I deal with the consequences. | ACTION-SURFACES.md |
| Sign-off | Drafted this README | Read it and signed it (2026-10-31) | My name is on the README, so I'm the one accountable for it. | this file |
