# SCRIPT: Honest Shortlist, final project film (approved 2026-11-23)

> Drafted by Claude Code (Opus 5.5) on 2026-11-23 from Prathamesh's own files only (SOURCES.md has the fact list).
> **Approved by Prathamesh 2026-11-23** (after the decisions below). First person, as Prathamesh. Read by a synthetic voice (Kokoro `af_bella`), disclosed on screen in B00.
> Tense rule: past tense only for things that exist and ran (file cited); future tense for everything else.

**Length.** 592 narrated words. `af_bella`'s measured rate on the pitch film was **154 words/min** (506 words over 197.09 s of
generated audio, `beat_sheet.json` on branch `prathamesh-p-final-project-film`, commit `65ff4a0`). Estimate: **about 3:51**.
The real duration is only known after audio generation.

**Tags on each line**
- `[SRC n]` = fact n in SOURCES.md (each with its file).
- `[MY TAKE?]` = an opinion or decision. It stays only if Prathamesh says it is his.
- `[DECISION]` = a threshold or plan no file states. Prathamesh must set it or cut it.
- `[UNBACKED]` = no file backs it (all were resolved before audio).

Short names: **JS1** = `fall-2026/prathamesh-p/js1-contract-and-watch/` (`a4f7165`); **JS2** = `fall-2026/prathamesh-p/js2-loop-tools-diff/`
(`f8a7af8`); **Mode** = Reallocation mode, PR #59 (`the-reallocation-engine`, `f4eab3a`); **Pitch** = `final-project-film/` (`65ff4a0`).

---

## Part 1. Executive summary: what I'm doing, and why anyone should care (no "how")

**B00.** I'm Prathamesh Pathak, and this is the film for my final project, Honest Shortlist. This synthetic voice is reading my script.
`[SRC 1]`

**B01.** Honest Shortlist will give an international network engineering student a short daily list of new jobs. Every claim about a posting will point to the sentence it rests on, or say the posting doesn't say.
`[SRC 1]` (future: none of this exists as one product yet)

**B02.** Why care? Sponsorship. On October twentieth, I checked seven network engineering postings at three employers. None offered sponsorship. Two required a security clearance, which, by inference, rules a visa holder out. Five said nothing at all.
`[SRC 2]` (Mode `WORKED-RUN.md` executive summary; "by inference" is the file's own wording, and `DOMAIN-JUSTIFICATION.md` gives the 32 CFR § 117.10(k) basis)

**B03.** Company history doesn't settle it. Zoox had one thousand three hundred sixty-four H one B approvals, yet all three of its network postings were silent.
`[SRC 3]`

## Part 2. What other people have done, and why mine still matters

**B04.** What exists already? LinkedIn alerts send new matching postings. When I looked at LinkedIn's search results on October thirty-first, the match reasoning sat behind a click, a no-sponsorship requirement wasn't flagged, and closed postings still showed up.
`[SRC 4]` first sentence is **documented behaviour, not hands-on** (retrieved by Claude in claude.ai; Claude Code never opened the URLs). `[SRC 5]` for the rest. Prathamesh looked at **search results, not a saved alert**, and the line says so.

**B05.** A chat assistant, given one pasted posting, did better: it caught "eight plus years" and said the posting was silent on sponsorship. But it only knows what I paste. My own first version called that posting relevant.
`[SRC 6]`, `[SRC 7]`

**B06.** And the Reallocation Engine's existing fetcher silently dropped six hundred thirty-one of Shield AI's six hundred fifty-three postings, including every network posting with clearance wording. Its output still looked clean.
`[SRC 8]`

**B07.** So why mine? It will watch the boards itself, like an alert, show its evidence, like a careful reader, and say "silent" when a posting is silent.
`[SRC 1]` (future) · framing confirmed by Prathamesh as drafted (2026-11-23)

## Part 3. Methods: how I'm going to do it

**B08.** Here's how. The data will be public Greenhouse, Lever, and Ashby job feeds. No logins, no LinkedIn or Indeed scraping, and it will never apply, email, or message anyone.
`[SRC 1]`, `[SRC 9]` (all three platforms were already read in JS2)

**B09.** Step one already ran in JS2, on November tenth: one fetch per board, inside a budget. Four boards took four of six requests, and a deliberately bad board got a four-oh-four error, with no retry.
`[SRC 9]` (JS2 `demo/01-live-run.txt`: 4/6 requests, `failed_http_404 attempts=1`)

**B10.** Step two ran too: keep only new postings. Zoox had thirty-one new ones against my saved October state, and a title rule screens for network roles.
`[SRC 9]`, `[SRC 10]`

**B11.** Step three exists in my Reallocation mode, not yet in the agent: pull every sentence about sponsorship, authorization, or clearance. Step four is still to build: label each claim supported, contradicted, or insufficient, with a verbatim quote.
`[SRC 11]` (step 3, `extract_auth_sentences.py`), `[SRC 1]` (step 4, future)

**B12.** My JS1 validator already rejects any quote that isn't in the posting. Then a fresh fetch will confirm the posting is open, and I'll approve the final list.
`[SRC 12]` (exists) · fresh fetch and approval are future `[SRC 1]`

**B13.** Do I have what I need? The boards need no account. The code is standard-library Python on my laptop. My Claude Code subscription handled the fifty judge calls in JS1. I haven't measured how far it stretches for daily runs across many boards.
`[SRC 13]` (JS1 `experiment/REPORT.md`: calls via `claude -p`, one fresh session each; 30 there + 20 in `SAMPLING-REPORT.md` = 50) · wording decided by Prathamesh 2026-11-23 · second sentence is Prathamesh's own statement (no file needed)

## Part 4. Evaluation: how I'll know it did a good job

**B14.** How will I know it worked? JS1 left a warning. All twenty test postings were not a fit, so always answering "not relevant" scored a hundred percent. Pass rate alone proved nothing.
`[SRC 14]`

**B15.** So I'll measure false positives, a "supported" label whose quote doesn't back the claim, and false negatives. For evaluation, I'll build a new held-out set of about forty postings from more boards, labelled by me before I see any output, including real entry-level fits and false friends.
`[SRC 15]` (JS1 lesson: label myself; false negatives were unmeasurable) · held-out plan decided by Prathamesh 2026-11-23 (future)

**B16.** It worked if it finds most real fits without calling any clearance- or citizenship-only posting relevant, beats the always-insufficient baseline on those fits, and verify catches every planted failure.
success bar decided by Prathamesh 2026-11-23 (future) · on screen, the real **SEEDED** catch `[SRC 16]` is the worked example

**B17.** Zero tolerance for calling a posting relevant when it rules out sponsorship. Missing a real fit is a rate I'll report, not a pass or fail. Every claim will carry its evidence, and silence will be called silence.
failure bar decided by Prathamesh 2026-11-23 · closing line reused from the pitch B14 `[SRC 1]`

---

## Flags: cleared 2026-11-23

Prathamesh decided B13, B15, B16 and B17. Claude (claude.ai chat) drafted the wording at Prathamesh's request, and Prathamesh
reviewed it and edited it where they disagreed. Prathamesh then read the whole script and said it "says what I'd say". The message
gave no replacement line for B07. After watching the review cut, Prathamesh confirmed that B07 stays as drafted. No UNBACKED lines remain.

**Deliberately left out** (true, but they would muddy the four parts): JS1's SEEDED new-posting run, the hard-link escape that JS2 left open,
the NBSP rejection on held-out, and the schedule. **JS3 does not exist** as of 2026-11-23 (no folder or branch), although the pitch planned it
for today. The script therefore makes no JS3 claim.
