# SOURCES: JS2, The Loop, the Tools, and the Diff

## Starting point
- **JS1**: `fall-2026/prathamesh-p/js1-contract-and-watch/` at commit `a4f7165` ("JS1: final real fetch (run 3) and submission"),
  branch `prathamesh-p-js1-contract-and-watch`. Files copied unchanged are listed in FRICTIONAL F1–F2. JS1's own SOURCES.md covers their origins,
  including the Gate-1 title filter from `prpathak1/the-reallocation-engine` commit `f3ea8b7`.
- **Brief**: `04_job_search_agent_2_loop_tools_diff.md` (Job-Search Agent 2, due 2026-11-10 23:59 ET), from Canvas
  https://northeastern.instructure.com/courses/264628/assignments/3522372
- **Course AI policy**: https://github.com/nikbearbrown/info-7375-prompt-engineering-for-generative-ai/blob/main/prerequisites/ai-policy.md and https://youtu.be/8Ut0Cdl6vMw?si=9w3aEpt1ZyAR4Kiz

## Public endpoints (no login, no key; each fetched once on 2026-11-10 at 08:07 EST)
| Board | Endpoint | Raw evidence |
|---|---|---|
| zoox (Lever) | https://api.lever.co/v0/postings/zoox?mode=json | `raw/2026-11-10/zoox.*` |
| cloudflare (Greenhouse Job Board API) | https://boards-api.greenhouse.io/v1/boards/cloudflare/jobs?content=true | `raw/2026-11-10/cloudflare.*` |
| openai (Ashby public posting API) | https://api.ashbyhq.com/posting-api/job-board/openai | `raw/2026-11-10/openai.*` |

## Tools
- Python 3.13.1 (standard library only), curl 8.21.0 (Git for Windows), git 2.55.0.windows.3, Windows 11 Home 10.0.26300.
- Claude Code CLI 2.1.322, model Opus 5.5 (`claude-opus-5-5`).

## Claude Code's contribution (dated)
| Date | What Claude Code did | What Prathamesh did |
|---|---|---|
| 2026-11-10 | Created the branch and folder and copied the JS1 files. Ran the inherited tests. Chose the cloudflare and openai boards and fetched all three (one GET each), hashing and counting them. Tested symlink and junction creation. Drafted GATE.md, FRICTIONAL.md, this file and review/PLAN.md. | Wrote the task instructions, chose zoox and the review-packet defect (JS1 NOT-CHECKED #7). Approved the GATE decisions at 08:17:25 (next row). |
| 2026-11-10 08:17–09:18 | **Review packet:** drafted the step-1 and step-2 commands and `tests/test_policy.py` (from GATE). Wrote `policy.py` and the `jobwatch.py` patch, `review/03-patch.diff`, the `03-behavior.md` draft, `04-scope.txt`, `06-revision-red.txt` (its own run, labelled), the step-6 revision and `tests/test_revision_fetch.py`, `06-revision.diff`, and `07_hardlink_demo.py` (dry-run in a scratchpad copy only). Made the commits and the push after Prathamesh asked. | Approved GATE (08:17:25). Chose the defect. Ran steps 1, 2 and 5, `06-after-revision` and `07-still-missed` via `!`. Decided enforce-inside (F18), REVISE (F23), the temp move (F26) and the step-7 pick. Approved the step-7 claim, which was drafted by Claude (claude.ai chat) |
| 2026-11-10 09:28–09:54 | **Loop:** found the two GATE gaps (A1, zoox state). Wrote `tests/test_loop.py` before any loop code (red run `demo/CLAUDE-DEV-01`). Wrote `adapters.py`, `loop.py` and `verify.py`, the `seeded/` fixture and the carried zoox state. Planted wrong versions in scratchpad copies. Wrote `BOUNDARY-TESTS.md`. Found the WRITTEN defect and fixed it test-first (`tests/test_written_reset.py`, `demo/CLAUDE-DEV-03/04`). Dry-ran the SEEDED demo in a scratchpad copy only. | Decided A1 and the zoox carry. Accepted the 410 naming, verify's extra checks and NOT-CHECKED 5–9. Ordered the WRITTEN fix. Ran `demo/00` (suite), `demo/01` (LIVE) and `demo/02` (SEEDED) via `!` |
| 2026-11-10 ~09:55–10:05 | Trimmed the FRICTIONAL "My take:" lines to the nine decision entries Prathamesh listed. Pointed BOUNDARY-TESTS "Actual" at Prathamesh's run. Ran the privacy scan. Drafted README.md, including the sign-off, the claims-not-made draft and the driver's-seat table, with "Why this part stays mine" left blank. | Writes "Why this part stays mine" and every "My take:", and signs or withholds |
| 2026-11-10 ~10:17–10:30 | Inserted the nine "My take" lines, the 14 "Why this part stays mine" lines and the sign-off sentence verbatim. Ran the fresh-clone check (`C:\js2fc`). Added NOT-CHECKED 10–14. Ran the final suite and privacy scan, and made the final commit, the push and the ZIP. | Gave the texts (drafted by Claude in claude.ai chat; reviewed and edited by him), confirmed items 10–14, and signed |

The Claude (claude.ai chat) contribution: it drafted the step-7 claim from Claude Code's findings, and Prathamesh approved it (review/07-still-missed.md).
The FRICTIONAL "My take:" lines (F5, F6, F8, F18, F23, F28, F34, F36, F37) and the README "Why this part stays mine" lines were, in Prathamesh's words, "drafted by Claude (claude.ai chat) at my request; I reviewed them and edited them in my own words where I disagreed." (recorded Tue Nov 10 10:17:42 EST 2026; the "Why" lines were inserted verbatim on Tue Nov 10 10:27:46 EST 2026, and for them Prathamesh's words were: "drafted by Claude in claude.ai chat at my request; I reviewed them and edited them in my own words where I disagreed").

*(Prathamesh: correct anything above you disagree with.)*
