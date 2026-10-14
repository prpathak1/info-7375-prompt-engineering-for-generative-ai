# RUBRIC-CHECK.md

Each requirement in the brief "Final Project Pitch Film - Show What You Will Build" (local copy
`Downloads\01_final_project_pitch_film\01_final_project_pitch_film.md`, SHA-256 prefix
`aa82ba8e8c73a336`), with where it is met and its status. **Updated at the end of every phase.**

**Last updated:** 2026-10-14 18:27 EDT, final pre-commit update. Prathamesh watched the master and accepted the remaining at-risk rows as logged (FRICTIONAL 25). Due 2026-10-14 23:59 ET.

Status: **todo** (not started) · **done** (met, with evidence) · **at risk** (a known problem or an open decision).

## The seven questions

| Requirement | Where satisfied (file + section) | Status | Evidence |
|---|---|---|---|
| Q1 What is it? One sentence, plus the finished artifact and its form | `PROJECT-BRIEF.md` §1 | done (brief) | Python + Claude; F-1 network-engineering persona; artifact = GitHub repo + tests + held-out eval + packet. The beat is todo |
| Q2 Why would anyone care? Unique value, 1–2 real alternatives examined, a specific difference | `PROJECT-BRIEF.md` §2 | **at risk** | the value statement is done. No alternative was examined (Prathamesh, 1b/2b); the brief says so and commits to comparing against LinkedIn job alerts and a chat assistant during JS1 (CLAIM-AUDIT #6–7) |
| Q3 Who opens it, and what do they do in the first 60 seconds? Target role and reader/user | `PROJECT-BRIEF.md` §3 | done (brief) | role confirmed: AI / agent engineer (applied AI). The beat is todo |
| Q4 What does it prove about you? Skills tied to course topics, plus planned evidence | `PROJECT-BRIEF.md` §4 table | done (brief) | 7 rows mapped to JS1–JS5/final, checked against the briefs (CLAIM-AUDIT #16). The beat is todo |
| Q5 What is in, out, and first? One exclusion, the first piece to run, how to verify that it ran | `PROJECT-BRIEF.md` §5 | done (brief) | exclusion: no LinkedIn/Indeed scraping; first: the JS1 one-board watch; verify: raw responses + state diff (SEEDED label if not a real second day) |
| Q6 What could sink it? One concrete, project-specific risk and a mitigation | `PROJECT-BRIEF.md` §6 | done (brief) | H-1B data unverified, so it is named only as "public H-1B employer data" (CLAIM-AUDIT #10) |
| Q7 Why this project? New vs existing skills; existing skills backed by real evidence | `PROJECT-BRIEF.md` §7 | done (brief) | existing: debugging/verification (`ce1a06c`) and sponsorship-history triage (recipe commits, split from its own SOURCES). Python moved to "will demonstrate". Basis: "will measure in JS1" (CLAIM-AUDIT #1, #3–5) |

## Honesty rules

| Requirement | Where satisfied (file + section) | Status | Evidence |
|---|---|---|---|
| Past tense only for what exists and can be shown; future tense for proposed work | `PROJECT-BRIEF.md`; `beat_sheet.json`; `CLAIM-AUDIT.md` | done (brief) / at risk (narration awaiting approval) | narration past tense only in B11 and B13, both on the "Exists today" list |
| No invented users, employers, metrics, testimonials or results | `PROJECT-BRIEF.md`; `CLAIM-AUDIT.md` #19 | done (brief) / todo (film) | the persona is labeled fictional; no metrics or results claimed |
| Screenshots, repositories and data samples are real and dated | B11 (git log), B13 (smoke log); `FRAME-CHECK.md` | done | hash, date and subject only; fixture path elided; dates on screen |
| Mock-ups and sketches labeled **constructed** on screen | `gate-reports/FRAME-CHECK.md` | done | 12/12 mock-up beats show CONSTRUCTED in rendered frames; B00 title, B11 and B13 real lines are labeled "real" / dated |
| Any Claude response shown is one actually received, with its date | `beat_sheet.json` | done (sheet) | no beat shows a Claude response or interface |
| Real résumé, contacts, tracker and conversations kept private; synthetic or public data only | frames; whole folder | done | frames clean; Windows username removed from all committable files (only the git author name remains) |
| Narrate as yourself; no instructor name, persona or credit line | `beat_sheet.json`; `README.md` Status; `FRICTIONAL.md` Entry 13 | **at risk (interpretation)** | The narration will be Prathamesh's first-person script in a synthetic Kokoro voice (`af_bella`), disclosed on screen. Prathamesh's reading: the line rules out impersonating the instructor, not synthetic narration. A grader could read it as requiring Prathamesh's own recorded voice. |
| Free local pipeline only: no paid generation, API keys, accounts or upload | `BUILD-PROMPT.md`; `logs/` | done | Kokoro/Manim/Remotion are local; smoke cost $0.00 (`logs/art_smoke_2026-10-14_run2.log`) |

## Required files and submission

| Requirement | Where satisfied (file + section) | Status | Evidence |
|---|---|---|---|
| `README.md`: name, working title, target role, runtime, rebuild instructions | `README.md` top table, Rebuild | done | Honest Shortlist · AI / agent engineer (applied AI) · 3:17.4 · rebuild commands |
| Rendered `.mp4` | `final/honest-shortlist-pitch.mp4` (force-added); `README.md` MP4 table | done | 6,295,549 B (< 100 MB), 197.417 s, 1920×1080, SHA-256 `142e91b8…f405`; watched by Prathamesh |
| `PROJECT-BRIEF.md`: one page, all seven answers, ending with `exists today` and `will exist` lists | `PROJECT-BRIEF.md` | **at risk** | all 7 answered, both lists present; 630 words after the approved trim (~550 target not reached without cutting Q4's planned evidence) |
| `beat_sheet.json`: narration and visual plan | `beat_sheet.json` (from `make_sheet.py`) | done | 15 beats approved by Prathamesh (with changes, FRICTIONAL 20); audio fields and build stamps written back by the toolkit |
| `BUILD-PROMPT.md`: prompts and commands that rebuild the film | `BUILD-PROMPT.md` | todo | Phases 1–2 recorded; the film build is not yet |
| `SOURCES.md`: sources, self-created material, Claude contributions, third-party assets and licences | `SOURCES.md` | todo | Phases 1–2 recorded |
| Toolkit gate reports | `gate-reports/` | done | GATE T on the master: `TYPECHECK-master-1080-PASS.md`; GATE V: `gate-v-run7-1080-PASS/` (+ the run 3 FAIL and its fix history); GATE B: `layout_audit.md`; transcripts; frame check. GATE L/A/W lines are in `logs/art_run_2026-10-14_run7_1080.log` |
| `FRICTIONAL.md`: dated work log | `FRICTIONAL.md` | todo | Entries 1–11 so far; ongoing |
| Exclude caches, credentials, private data and private transcripts | `.gitignore`; privacy scan (FRICTIONAL 25) | done | 0 emails, phones, keys or résumé text; username only as the git author name (kept, by decision); `C:\info7375\…` paths kept, by decision (no username, needed to rebuild) |
| Runtime 2–4 minutes (shorter is acceptable if complete) | the final master; `README.md` | done | ffprobe 197.417 s = 3:17.4 |
| Fix render-integrity failures (gate reports) | `gate-reports/`; `FRICTIONAL.md` 20–24 | done | GATE V low-contrast B02/B09 (1 fix); GATE T B08 min-size (2 fixes); Gate A traps pre-render. No slate fallback needed |
| Canvas ZIP named `Pathak_Prathamesh_INFO7375_FinalProjectFilm.zip` | Downloads folder (built from the commit with `git archive`) | todo → done after the push | the MP4's SHA-256 inside the ZIP is checked against README |
| GitHub path `fall-2026/prathamesh-p/final-project-film/` | this folder | done | Prathamesh confirmed it: the brief names this path, which overrides the AGENTS.md `youtube/` convention (FRICTIONAL Entry 11) |
| Canvas includes the GitHub folder link and final commit hash | Canvas submission text | todo (Prathamesh) | the hash is reported after the push; it cannot be written inside its own commit |
| If the toolkit fails, log what was tried, what broke, and the alternative | `FRICTIONAL.md` | done (so far) | Entries 6, 7, 9 (patch, CMD `set`, and doc-write failures) |

## Grading criteria

| Requirement | Where satisfied (file + section) | Status | Evidence |
|---|---|---|---|
| What/who (7) | `PROJECT-BRIEF.md` §1, §3; Q1 + Q3 beats | done (brief) / todo (film) | |
| Unique value and real alternatives (5) | `PROJECT-BRIEF.md` §2; Q2 beat | **at risk** | no alternative examined yet; honest "will compare in JS1" |
| Skills and planned evidence (5) | `PROJECT-BRIEF.md` §4; Q4 beat | done (brief) / todo (film) | |
| Honest new-vs-existing skill rationale (4) | `PROJECT-BRIEF.md` §7; Q7 beat | done (brief) / todo (film) | the split is backed by the recipe's own records; Python is honestly listed as new |
| Scope / risk / exists-vs-will (5) | `PROJECT-BRIEF.md` §5, §6, lists; Q5 + Q6 beats | done (brief) / todo (film) | the exists-today items are verified (CLAIM-AUDIT #1, 2, 8, 9) |
| Visuals / labels / quality checks (4) | the film; `gate-reports/` | done | all gates pass; frame check passes on the final clips |
| Frictional honest log (5) | `FRICTIONAL.md` | todo | ongoing |
| GitHub version matching Canvas (5) | the commit; the MP4 in both places; `README.md` SHA-256 | todo | the MP4 will be committed and zipped, and the same SHA-256 checked in both (FRICTIONAL Entry 12) |
| Relative quartile (10) | the whole submission | todo | not listed in the request; included because the brief grades it |
