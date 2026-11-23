# FACTCHECK.md: honest-shortlist-final

Every claim in the narration, checked against SOURCES.md (which lists each file and commit). Verdicts: PASS (backed) · CORRECTED
(reworded to match a source) · EXEMPT (a plan, a decision or framing, stated in future tense or as a decision).
Future-tense plans PASS when they match the pitch brief or Prathamesh's 2026-11-23 decisions.

| # | Beat | Claim | Verdict | Source | Fix |
|---|---|---|---|---|---|
| 1 | B00 | Speaker is Prathamesh Pathak; the voice is synthetic, reading the script | PASS | README; Kokoro af_bella | disclosed on screen |
| 2 | B01 | Honest Shortlist will give a short daily list; each claim points to its sentence or says the posting doesn't say | PASS | Pitch PROJECT-BRIEF §1–2 (SRC 1) | future tense |
| 3 | B02 | 2026-10-20: 7 network postings, 3 employers; 0 offer sponsorship; 2 require clearance (ruled out by inference); 5 silent | PASS | Mode WORKED-RUN.md exec summary (SRC 2) | "by inference" kept |
| 4 | B03 | Zoox 1,364 H-1B approvals; all 3 Zoox network postings silent | PASS | Mode DOMAIN-JUSTIFICATION.md (SRC 3) | — |
| 5 | B04 | LinkedIn alerts send new matching postings | PASS (documented) | JS1 ALTERNATIVES.md (a) (SRC 4) | on screen: "documented, not tested by me" |
| 6 | B04 | 10-31 look at LinkedIn search results: reasoning behind a click; no-sponsorship requirement not flagged; closed postings still shown | CORRECTED | JS1 ALTERNATIVES.md (b) (SRC 5) | "search results", not "alerts" |
| 7 | B05 | Chat on one pasted posting caught 8+ years and said it was silent on sponsorship; it reads only what is pasted | PASS | JS1 ACTION-SURFACES.md (a) (SRC 6) | — |
| 8 | B05 | My first version called that posting relevant | PASS | JS1 ACTION-SURFACES.md (a) "Compared with my agent" (SRC 7) | — |
| 9 | B06 | Existing fetcher dropped 631 of Shield AI's 653, including every network posting with clearance wording; output looked clean | PASS | Mode DOMAIN-JUSTIFICATION.md; WORKED-RUN.md (SRC 8) | — |
| 10 | B07 | Why mine: will watch boards, show evidence, say silent | EXEMPT | framing kept by Prathamesh 2026-11-23 | future tense |
| 11 | B08 | Data: public Greenhouse, Lever, Ashby feeds; no logins or LinkedIn/Indeed scraping; never apply, email or message | PASS | Pitch brief §5 (SRC 1); JS2 used all three (SRC 9) | future tense |
| 12 | B09 | 2026-11-10: one fetch per board inside a budget; 4/6 requests; bad board one 404, no retry | PASS | JS2 demo/01-live-run.txt (SRC 9) | — |
| 13 | B10 | Zoox 31 new against my October state; a title rule screens for network roles | PASS | JS2 demo/01, README; JS1 README (SRC 9, 10) | — |
| 14 | B11 | Step 3 exists in the Reallocation mode, not yet in the agent; step 4 still to build | PASS | Mode extract_auth_sentences.py, WORKED-RUN.md (SRC 11); Pitch brief (SRC 1) | — |
| 15 | B12 | The JS1 validator rejects any quote not in the posting; re-fetch and approval are planned | PASS | JS1 README (W1) (SRC 12) | — |
| 16 | B13 | Boards need no account; stdlib Python on my laptop | PASS | JS1/JS2 README (SRC 13) | — |
| 17 | B13 | My Claude Code subscription handled the 50 judge calls in JS1 | PASS | JS1 experiment/REPORT.md (30 calls, `claude -p`) + SAMPLING-REPORT.md (20); README: logged-in Claude account (SRC 13) | wording decided by Prathamesh |
| 18 | B13 | Haven't measured how far it stretches for daily runs | EXEMPT | Prathamesh's own statement, 2026-11-23 | — |
| 19 | B14 | All 20 test labels "not fit"; always "not relevant" scored 100% | PASS | JS1 experiment/REPORT.md Limits (a) (SRC 14) | — |
| 20 | B15 | Measure false positives and false negatives; new held-out set of about 40, labelled by me first | EXEMPT | Prathamesh's decision 2026-11-23; JS1 lesson (SRC 15) | future tense |
| 21 | B16 | Success bar | EXEMPT | Prathamesh's decision 2026-11-23 | on screen: "(planned)" next to the real SEEDED catch (SRC 16) |
| 22 | B17 | Failure bar; closing line | EXEMPT | Prathamesh's decision 2026-11-23; pitch B14 | — |
