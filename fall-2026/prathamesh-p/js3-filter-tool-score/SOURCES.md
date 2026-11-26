# SOURCES

## Starting code

| What | From | Commit |
|---|---|---|
| `loop.py`, `adapters.py`, `policy.py`, `verify.py`, `GATE.md`, tests | JS2 `fall-2026/prathamesh-p/js2-loop-tools-diff/` | `f8a7af8` |
| `jobwatch.py`, `CONTRACT.md`, `fixtures/resume.fictional.json` (fictional persona), title regexes | JS1 via JS2; regexes from `scripts/contrib/2026fa/prpathak1-network-sponsorship-text/filter_titles.py` | `f3ea8b7` |
| `raw/2026-10-30`, `raw/2026-11-10` | JS1/JS2 captures (public board APIs) | as above |

## Data collected in JS3

| Board | Endpoint | Date | Result |
|---|---|---|---|
| Fastly (Greenhouse) | `https://boards-api.greenhouse.io/v1/boards/fastly/jobs?content=true` | 2026-11-25 18:40 EST | 200, 50 postings |
| Datadog (Greenhouse) | `https://boards-api.greenhouse.io/v1/boards/datadog/jobs?content=true` | 2026-11-25 18:40 EST | 200, 392 postings |
| Tailscale (Ashby) | `https://api.ashbyhq.com/posting-api/job-board/tailscale` | 2026-11-25 18:40 EST | 404 |

## Assignment and prior evidence

- The brief: `05_job_search_agent_3_filter_tool_score.md` (course materials, read 2026-11-25).
- The seniority evidence: JS1 `ACTION-SURFACES.md` (Claude.ai chat experiment, 2026-10-31) and JS1 `FRICTIONAL.md` F13.

## Claude's contributions (dated)

- **2026-11-25, about 18:39–18:43 EST, Claude Code CLI (Opus 5.5, `claude-opus-5-5`):**
  - created the branch and folder and copied the files,
  - ran the tests and the 3-board check (choosing the boards),
  - counted the inventory,
  - drafted `FILTER.md` v0.1, `PLAN.md`, this file and the factual entries in `FRICTIONAL.md`.
- **2026-11-25 18:46:08 EST:** Prathamesh reviewed and approved FILTER.md v0.1 (all rules) and PLAN.md.
- **2026-11-25, about 18:46–18:53 EST, Claude Code CLI (Opus 5.5):**
  - wrote `postings.py`, `holdout.py`, `LABEL-SHEET.md` (generated), `tests/test_filter.py` (tests first) and `filter.py`,
  - recorded F9–F12.
  - The held-out labels will be Prathamesh's alone. *(Superseded 19:21 EST: Claude drafted them and Prathamesh approved them; see "JS3 build" below.)*

## JS3 build, 2026-11-25 19:01–19:21 EST

**Held-out labels** (`holdout/LABELS.json`):
- Drafted by **Claude (claude.ai chat)** at Prathamesh's request, from the LABEL-SHEET text Claude Code printed. Reviewed and approved by Prathamesh, made blind to any filter output on the held-out set.
- The score test is therefore partly Claude judging Claude.

**Audit verdicts** (`audit/AUDIT-VERDICTS.json`): drafted by **Claude (claude.ai chat)** from the printed rows; reviewed and approved by Prathamesh.

**FILTER v0.2 decisions:** Prathamesh's (changes 1–2, and the K1 limit recorded unchanged).

**Claude Code CLI (Opus 5.5)** wrote:
- the v0.2 tests and code, the config switches, `audit_sheet.py`, `shortlist.py`, `score_test.py`, `mcp_server.py`, `mcp_probe.py` and `probes/`;
- `audit/AUDIT.md`, `GROUNDING.md`, `TOOL-EVAL.md`, `SCORE.md`, and FRICTIONAL F17–F25.

**Claude Code 2.1.332 as the real MCP client** (`claude -p`, model claude-opus-5-5): one session, 2026-11-25 19:14:55–19:15:13 EST. Transcript: `transcripts/claude-client-20261125T191455.jsonl`.

**Third-party software evaluated:** `@modelcontextprotocol/server-filesystem` **2.2.0** (npm, published 2026-11-04), run with npx against a scratch sandbox outside the repo. Its source code was not reviewed.

## JS3 finish, 2026-11-25 19:26–19:35 EST

**Verbatim inserts by Prathamesh:**
- What: the two trust decisions (TOOL-EVAL.md), the 7 "My take" lines (FRICTIONAL F9, F17, F19, F21, F23, F24, F25) and the 7 "Why this stays mine" cells (README driver's-seat table).
- Provenance: all were **drafted by Claude (claude.ai chat)** at his request. He reviewed them and edited them where he disagreed. Claude Code inserted them verbatim and did not change their wording.

**Prathamesh's decisions:** FILTER v0.3 (the A2 export-license exception) and the redaction of the Windows user folder.

**Claude Code CLI (Opus 5.5):**
- wrote the v0.3 tests and code, `redact_paths.py`, README.md (including the sign-off sections; signed by Prathamesh on 2026-11-25, his words recorded verbatim), and FRICTIONAL F26–F28;
- updated FILTER.md, SCORE.md, AUDIT.md, GROUNDING.md, TOOL-EVAL.md and SHORTLIST.md (regenerated for v0.3).
