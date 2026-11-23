# SOURCES: final project film (Honest Shortlist)

> Drafted by Claude Code (Opus 5.5, 2026-11-23). Every fact in SCRIPT.md comes from Prathamesh's own committed work, listed below.
> No web sources were opened for this film. Where a file itself relays a web source, that is stated.

## Where the facts come from

| Short name | Location | Commit / branch |
|---|---|---|
| Pitch | `fall-2026/prathamesh-p/final-project-film/` | `65ff4a0`, branch `prathamesh-p-final-project-film` |
| JS1 | `fall-2026/prathamesh-p/js1-contract-and-watch/` | `a4f7165`, branch `prathamesh-p-js1-contract-and-watch` |
| JS2 | `fall-2026/prathamesh-p/js2-loop-tools-diff/` | `f8a7af8`, branch `prathamesh-p-js2-loop-tools-diff` |
| Mode (PR #59) | `the-reallocation-engine`: `course/2026fa/submissions/prpathak1/network-sponsorship-text/` and `scripts/contrib/2026fa/prpathak1-network-sponsorship-text/` | `f4eab3a`, branch `contrib/2026fa-prpathak1-mode-network-sponsorship-text`; PR https://github.com/nikbearbrown/the-reallocation-engine/pull/59 |
| JS3 | **does not exist** (no folder, no branch, checked 2026-11-23 10:4x EST) | none |

## Fact list (SCRIPT.md tags `[SRC n]`)

| # | Fact | File | Tense in script |
|---|---|---|---|
| 1 | Honest Shortlist is planned as a Python + Claude agent. It watches public job boards and gives a fictional F-1 network-engineering student (SOC 15-1241) a short daily list. Claims are labeled supported / contradicted / insufficient against the posting text, with "insufficient" as the default. Liveness comes from a fresh fetch, and a human approval gate signs off. Out of scope: LinkedIn/Indeed scraping, and any applying, emailing, messaging or logging in. A stranger should be able to check it within 60 seconds. Closing line: "every claim will carry its evidence, and silence will be called silence." | Pitch `PROJECT-BRIEF.md` §1, §3, §5, §6; pitch `beat_sheet.json` B14 | future |
| 2 | On 2026-10-20 the mode ran on three employers' boards (shieldai, zoox, palantir). It found 7 in-scope postings: 2 ruled out by inference (required security clearance), 5 don't say, 0 offer sponsorship. A clearance limits a job to citizens through 32 CFR § 117.10(k). | Mode `WORKED-RUN.md` exec summary; `DOMAIN-JUSTIFICATION.md` | past |
| 3 | 80 Days to Stay (2026-10-20): Zoox had 1,364 H-1B approvals, yet all 3 Zoox network postings were silent | Mode `DOMAIN-JUSTIFICATION.md` "The information asymmetry" | past |
| 4 | LinkedIn job alerts deliver new postings matching a saved search, daily, weekly or in real time. The sources consulted don't describe citing posting text or flagging sponsorship. **Documented, not hands-on.** Claude in claude.ai retrieved it, and Claude Code did not open the URLs. | JS1 `ALTERNATIVES.md` (a) | present (documented) |
| 5 | Prathamesh's hands-on look on 2026-10-31 at ~14:00, at **LinkedIn search results, not a saved alert**: the match reasoning was hidden behind "Show match details"; the "authorized to work in the U.S. without sponsorship" requirement was not flagged; both postings said "No longer accepting applications" yet still appeared | JS1 `ALTERNATIVES.md` (b) | past |
| 6 | Pasting the full "Senior Network Security Engineer" posting into a new Claude.ai chat (2026-10-31, ~14:30) gave "Not relevant", mainly because of "8+ years", and "the posting is silent" on sponsorship, with 5 real quotes. A title-only paste got a labeled guess. It reads only pasted text. | JS1 `ACTION-SURFACES.md` (a) | past |
| 7 | On that same posting, Prathamesh's agent (rule and judge v1) said "relevant" and missed the 8+ years | JS1 `ACTION-SURFACES.md` (a), "Compared with my agent" | past |
| 8 | The repo's existing fetcher silently rejected 631 of Shield AI's 653 postings, including every network posting with clearance wording, and dropped the bullet-list field. The output looked clean. Console: `[lever] Shield AI: found 22 jobs` vs `[lever-full] shieldai: 653 postings` | Mode `DOMAIN-JUSTIFICATION.md` failure mode 1; `WORKED-RUN.md` Cmd 1 and Cmds 3–5 | past |
| 9 | JS2 live run (Prathamesh via `!`, 2026-11-10 09:52:31–09:52:40 EST). Four boards on Lever, Greenhouse and Ashby used 4/6 requests in 8.757/120 s. zoox `ok` 234 postings, 31 new against the JS1 state; cloudflare 466; openai 826. The bad board got `failed_http_404 attempts=1`, with no retry. Status `incomplete`, exit 3, verify.py PASS. | JS2 `demo/01-live-run.txt`; JS2 `README.md` "What actually ran" row 3 | past |
| 10 | The title rule (Gate 1, reused from the Reallocation filter) screens for network roles. "Road Network Tools" is a tested false friend. | JS1 `README.md` sign-off table (`Rule.test_road_network_tools_is_not_relevant_in_real_day1_data`); JS1 `CONTRACT.md` | past |
| 11 | `extract_auth_sentences.py` pulls sponsorship, authorization and clearance sentences from every posting field, lists included. It ran on 2026-10-20 (e.g. `has-sentences 2 sentence(s) shieldai Network Engineer (R4843) fields=additionalPlain,descriptionPlain,lists`). It is not in the agent yet. | Mode `WORKED-RUN.md` Cmds 3–5; mode scripts folder | past (mode) / future (agent) |
| 12 | The JS1 validator rejects uncited or fabricated justifications (a quote must be a verbatim substring of the named posting field). 50 tests OK. | JS1 `README.md` sign-off (W1, `Validator.test_rejects_uncited_or_fabricated_justification`) | past |
| 13 | Resources actually used: public, unauthenticated board endpoints; Python standard library only; Windows 11 laptop; Claude Code CLI `claude -p` "logged in to the user's Claude account" (no API key); 50 experiment Claude calls (20 sampling + 30 experiment) on 2026-10-31 with `claude-opus-5-5` | JS1 `README.md` (toolchain; driver's seat "50 calls"); JS1 `experiment/REPORT.md`; JS2 `README.md` toolchain and NOT-CHECKED item 10 | past |
| 14 | JS1 experiment: all 20 labels "not fit", so "always not_relevant" scored 100% on both splits and pass rate cannot show improvement. False positives are the meaningful measure. | JS1 `experiment/REPORT.md` "Limits (a)" | past |
| 15 | False negatives were unmeasurable (no fit postings). The labels were Claude-drafted ("Claude grading Claude"), and "next time I'll write the labels myself". "Visa" can be the payments company. | JS1 `experiment/REPORT.md`; JS1 `README.md` driver's seat; Pitch `PROJECT-BRIEF.md` §6; mode `fixtures/BROKEN-visa-false-friend.json` | past / future |
| 16 | **SEEDED** demo (2026-11-10 09:53:54): a constructed empty openai body after 826 real IDs. The agent said `status=finished exit=0`; verify.py said `FAIL … posting count is 0 but the previous snapshot had 826 ids` | JS2 `demo/02-seeded-finished-but-wrong.txt` | past, labelled SEEDED |
| 17 | Brutalist toolkit smoke: **SMOKE PASS** on 2026-11-23 (log written 10:40:54 EST), exit 0 | `logs/art_smoke_2026-11-23.log` (this folder) | past |

## Lines no file backs (resolved 2026-11-23)

There are no UNBACKED lines left.
- **B13**: the first sentence is backed by JS1 `experiment/REPORT.md` (30 calls through `claude -p`, one fresh session each) plus `SAMPLING-REPORT.md` (20 calls), which makes 50. JS1 `README.md` says the calls ran on the logged-in Claude account. No file names the plan type, so "subscription" is Prathamesh's wording. The second sentence is Prathamesh's own statement.
- **B15, B16 and B17** are Prathamesh's decisions (future-tense plans and bars), not facts from files.
- **B07** is framing that Prathamesh kept.

## Who did what

- **Claude Code (Opus 5.5)** ran the smoke test, created the branch and folder, read the files above, and drafted SCRIPT.md, beat_sheet.json, this file, README.md and FRICTIONAL.md.
- **Prathamesh** set the brief (four parts, toolkit, voice, no persona, disclosure, CONSTRUCTED labels, facts only from Prathamesh's work).
- **Script decisions (2026-11-23):** the wording for B13, B15, B16 and B17 was **drafted by Claude in claude.ai chat at Prathamesh's request**. Prathamesh reviewed it and edited it where they disagreed, then read the whole SCRIPT.md and confirmed it "says what I'd say". B07 stays as Claude Code drafted it, as Prathamesh confirmed after watching the review cut.
- **Claude Code** placed those lines in SCRIPT.md (FRICTIONAL F5). It then regenerated `beat_sheet.json` and wrote `scenes.py` (reusing the pitch film's shared components), FACTCHECK.md, SHOTLIST.md and PROMPTS.md. It also generated the audio, ran the transcription check, rendered the review cut and did the frame check.

## Toolkit and licences

Same as the pitch film: brutalist.art (https://github.com/nikbearbrown/brutalist.art), local clone `C:\info7375\brutalist.art-latest` at `519fcbb`
with Prathamesh's Windows patches (pitch `toolkit-patches/`). Voice: Kokoro `af_bella` (local, $0.00 per the smoke log). No paid generation, no API keys.
