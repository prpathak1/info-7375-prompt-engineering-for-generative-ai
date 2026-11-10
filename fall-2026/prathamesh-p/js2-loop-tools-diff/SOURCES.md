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
| 2026-11-10 | Created the branch and folder and copied the JS1 files. Ran the inherited tests. Chose the cloudflare and openai boards and fetched all three (one GET each), hashing and counting them. Tested symlink and junction creation. Drafted GATE.md, FRICTIONAL.md, this file and review/PLAN.md. | Wrote the task instructions, chose zoox and the review-packet defect (JS1 NOT-CHECKED #7). Approving the GATE decisions is still pending. |

*(Prathamesh: add rows as work continues, and correct anything above you disagree with.)*
