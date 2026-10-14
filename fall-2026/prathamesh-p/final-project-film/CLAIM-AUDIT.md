# CLAIM-AUDIT.md: PROJECT-BRIEF.md

First run by Claude Code on 2026-10-14 at about 16:30 EDT (first logged as "16:40", a guessed time;
corrected). Re-run at 16:36 EDT after the trim and the recipe-records check. **Final re-run at 16:39 EDT** on the finalized brief. Every factual claim and every past-tense statement in
`PROJECT-BRIEF.md` is listed, with how it was checked. Future-tense design claims are listed only when
they must agree with a course brief.

Verdicts: **VERIFIED** (checked against a primary file or command) · **PARTIAL** (only part could be
verified) · **PENDING** (only Prathamesh can confirm it) · **DESIGN** (a future claim, checked for
consistency with the briefs, not for truth).

| # | § | Claim | Verdict | How it was checked / source |
|---|---|---|---|---|
| 1 | 7 | I ran the Brutalist toolkit on native Windows, diagnosed failures, and reviewed and approved fixes that Claude wrote; commit `ce1a06c`, 2026-09-27 | VERIFIED | `git log`: `ce1a06ce9aef…` 2026-09-27 22:09 −0400, author Prathamesh P; it holds 5 `brutalist-*.diff` files. Week-01 FRICTIONAL Entries 3–9 record the diagnosis and approvals, and that Claude wrote the patches. It is on `fork/prathamesh-p-week-01` and **not in `origin/main`** |
| 2 | 7, Exists | Reallocation recipe commits `100a823`, `1a3e757`, `1b5a589`, 2026-10-03, fork branch, not merged | VERIFIED | `git log`: all 3 dated 2026-10-03, author prpathak1, on `contrib/2026fa-prpathak1-network-eng-h1b-soc-15-1241`. After `git fetch upstream`, none is an ancestor of `origin/main` or `upstream/main` |
| 3 | 7 | Recipe split: "I chose the persona, SOC code, rules and dates, decided the data and honesty calls, and approved every commit. Claude Code drafted all the code, tests and text." | VERIFIED | the recipe's `course/2026fa/submissions/prpathak1/SOURCES.md` table "What AI contributed vs what the student decided"; all 6 branch commits carry `Co-Authored-By: Claude Opus 5.5`. Prathamesh approved this wording (item 4: yes) |
| 4 | 7 | Python listed under "New / will demonstrate", not "Already have" | VERIFIED (resolved) | Prathamesh chose 3b. Consistent with the records: the Week 1 Python and `normalize_names.py` were written by Claude (week-01 `SOURCES.md:25`; recipe FRICTIONAL F22 lines 337 and 363) |
| 5 | 7 | Why: "I don't know yet how common the problem is. I will measure how often sponsorship wording is missing or ambiguous in my JS1 sample." | DESIGN (resolved) | Prathamesh chose 5b. The brief makes no unmeasured frequency claim beyond "often" (#12) |
| 6 | 2 | "I haven't examined alternatives yet" | VERIFIED (as stated by Prathamesh) | Prathamesh chose 1b and 2b: neither LinkedIn alerts nor a chat assistant was checked. No claim about either product remains in the brief |
| 7 | 2 | "During JS1 I will compare against LinkedIn job alerts and pasting a posting into a chat assistant, and record what I see in FRICTIONAL" | DESIGN | future tense; nothing claimed about either product. **Q2 stays at risk**: the rubric asks for 1–2 real alternatives examined |
| 8 | Exists | Toolkit setup with passing smoke, 2026-10-14 | VERIFIED | `logs/art_smoke_2026-10-14_run2.log`: `SMOKE PASS` |
| 9 | Exists | This film folder exists | VERIFIED | `fall-2026/prathamesh-p/final-project-film/` (uncommitted, branch `prathamesh-p-final-project-film`) |
| 10 | 6 | "Public H-1B employer data" | PARTIAL | The Reallocation Engine `data/80-days-to-stay/README.md:13` says it maps SEC data against "DOL LCA Disclosure Data" and the "USCIS H-1B Employer Data Hub". That is a secondary description: no fiscal years, no dataset licence (the repo is MIT), and the CSV isn't in the local clone (only audits, dated 2026-05-28, SHA-256 `eccdee2a…6270`). **So the film will name no specifics**, as Prathamesh decided. Re-run: the recipe actually used the tracked `data/80-days-to-stay/80-days-csv/mapped_student_employment_targets_v3.csv`, whose README gives no fiscal years or licence either. Note: the CSV also has `executive_officers`, `board_directors` and `phone` columns (real people's data), which the agent will not use |
| 11 | 6 | "Visa" can be the payments company | VERIFIED (general knowledge) | Visa Inc. is a payments company. This is a keyword false friend, not a claim about any posting |
| 12 | 6 | Sponsorship wording is "often" missing or ambiguous | DESIGN / unmeasured | Not measured. Hedged as "often". It will be measured in the JS1 sample if Prathamesh chooses that as the Q7 basis |
| 13 | 1 | SOC 15-1241 for network engineering | PARTIAL | It matches Prathamesh's recipe. The SOC title is "Computer Network Architects", which network-engineer titles map to. The official SOC/O*NET page was not opened in this session |
| 14 | 5 | Public Greenhouse/Lever/Ashby JSON endpoints | DESIGN | Consistent with JS1 Step 2, which allows Greenhouse, Ashby, Lever and SmartRecruiters. The endpoints will be verified when JS1 is built |
| 15 | 5 | Never apply, email, message, or log in | DESIGN | Consistent with JS2 Step 1 and JS5 `REGISTER.md` "Never" |
| 16 | 4 | Assignment mapping (JS1 contracts/split; JS2 loop/permissions/stop; JS3 grounding/MCP; JS4 evidence matrix/memory; JS5 gate/embarrassing set/controlled failure; final 5+ failure cases) | VERIFIED against the briefs | Downloads briefs 03–07 and course `assignments/assignment-final-project.md` |
| 17 | Will exist | Dates Oct 21, Oct 31, Nov 10, Nov 23, Dec 1, Dec 13, Dec 20 | VERIFIED | due dates in briefs 02–07 and the final project brief (Dec 20) |
| 18 | Will exist | "Demo of 5 minutes or less", "stranger run" | VERIFIED | final project brief, "The demo" and "The stranger run" |
| 19 | 1–7 | No invented users, metrics or results | VERIFIED | the persona is labeled fictional; the brief has no metrics, user counts or results |
| 21 | 7 | The recipe is "sponsorship-history triage" | VERIFIED | the recipe's executive summary: it checks whether each employer has an H-1B sponsorship record and sponsored network titles; never Apply on a network match alone |
| 22 | all | Final brief: 0 `[PENDING]`; 684 words | VERIFIED | `grep -c PENDING` = 0; `wc -w` = 684, over the ~550 target because the resolved Q7 text is longer |
| 20 | header | Answers drafted by Claude (claude.ai chat, Opus 5.5) on 2026-10-14 | VERIFIED (as stated by Prathamesh) | FRICTIONAL Entry 15; SOURCES.md |

## Trim re-run (2026-10-14, between the 16:42 and 16:47 EDT `date` readings)

Q4 and "Will exist" were shortened, with Prathamesh's approval. The brief went from 684 to 630 words.
Nothing else changed. **No claim was added.** Removed from the brief: in Q4, "a handled board failure"
(JS2) and the "JS1 split / JS5 set" detail (now "held-out set"); in Will exist, "filter", "plan",
"register", "controlled failure" (still in Q4) and "evaluation" (still in Q4). Every remaining Q4 line
keeps its planned evidence. Getting to ~550 would have meant cutting that evidence, so the trim stopped
at 630.

## Narration vs brief (beat_sheet.json, 2026-10-14 16:47 EDT)

Each beat's narration was checked against PROJECT-BRIEF.md. Lines the brief does not back:
- **B00** "I'm Prathamesh Pathak": the name comes from README.md and the Canvas ZIP name, not the brief.
  "This synthetic voice is reading my script" comes from Prathamesh's decision (FRICTIONAL Entry 13).
- **B01** "A network engineering posting lists skills, city, sometimes pay": an illustrative
  description of a typical posting, not a measured or sourced claim. The drawing is labeled CONSTRUCTED.
- **B14** "silence will be called silence": a rhetorical restatement of the "insufficient" default
  (Q6). It is not a new claim.

Kept in the brief but dropped from the narration for runtime (not contradictions): "record what I see
in FRICTIONAL" (Q2); "10+" boundary tests (Q4); the controlled failure (Q4); "MCP-style tools" in Q7's
new-skills list; "false friends go into the held-out set" (Q6); "this folder" (exists today); SOC code
and "data and honesty calls" in the recipe split; "following the course rule" (Q5).

Past tense in the narration: B11 "ran / diagnosed / reviewed and approved" (Week 1 commit `ce1a06c`)
and "chose" (recipe commits); B13 "has passed" (smoke, 2026-10-14). All three are on the brief's
"Exists today" list. Everything else is future tense, or present tense for current facts ("I haven't
examined", "I don't know yet", "are new to me").

**Tense check (final, by grep):** past tense appears only in §7: "I ran / diagnosed / reviewed and approved" (#1), "Claude wrote" (#1), "I chose / decided / approved" and "Claude Code drafted" (#3). All are VERIFIED. "I haven't examined" (§2) is true by Prathamesh's statement (#6). Everything else is future tense. No metric-like numbers (a grep for %, user, posting or company counts found none).
**Contradiction check against the Dec 20 requirements:** none found. Loop, tools and policy in code,
memory, model-independent stop, gate bound to the exact proposal, held-out evaluation with 5+ failures,
controlled failure, packet, stranger run and demo ≤5 min are all promised, and none is excluded.
