# Action-surface comparison (Chapter 3)

> Claude Code drafted the facts for surfaces (b) and (c) on 2026-10-31. **Prathamesh performed and described surface (a).** Its table is summarized by Claude Code.
> The choice and defense of the least autonomy that is enough is Prathamesh's (see the end of this file).

The same task is used for every surface: *give a relevant / not_relevant verdict on one Zoox posting for the fictional persona, with
cited justification.*

## (a) Paste one posting into chat

*Performed by Prathamesh. The table is summarized by Claude Code from Prathamesh's observation below (2026-10-31 14:41 EDT).*

| | |
|---|---|
| Can read | Only the text pasted into the chat (in both attempts). The account also has web search, saved memory and past-chat search, none of which was used here |
| Can write | Nothing outside the chat reply |
| Can send | Nothing. It did not fetch the job board and cannot send messages. The pasted posting goes to the chat service as model input |
| Authority needed | A logged-in Claude.ai account, and the person choosing what to paste |
| How it can fail | A copy mistake gives a guess instead of an answer (Attempt 1: ID and title only, so it gave "likely not relevant" from "Staff", labeled a guess). The pasted text may lack location, salary, date or a work-authorization line. A seniority-driven "not relevant" can be misread as "won't sponsor". Quotes can be trimmed mid-sentence (2 of 5 in Attempt 2, meaning unchanged). Senior roles sometimes still hire people with less experience |
| What actually ran (date) | 2026-10-31 ~14:30 EDT, two new Claude.ai chats: Attempt 1 (#8 Staff Network Security Architect, ID and title only); Attempt 2 (full "Senior Network Security Engineer" posting, verdict not relevant, mainly on "8+ years"; sponsorship: posting is silent) |

### (a) What I saw pasting a posting into a chat assistant

*Everything from the heading line through "What could go wrong" is Prathamesh's own hands-on observation (2026-10-31 ~14:30 EDT), inserted verbatim by Claude Code.
The final paragraph, "Compared with my agent", was drafted by Claude (claude.ai chat) from the run records and approved by Prathamesh (provenance corrected 2026-10-31 14:41 EDT).*

(a) What I saw pasting a posting into a chat assistant (Prathamesh, 2026-10-31, ~14:30)

Attempt 1 (my mistake: only the ID and title were pasted). I pasted only the posting ID and title of "Staff Network Security Architect" (experiment dev candidate #8) into a new Claude.ai chat. Claude said it couldn't give a cited answer because no posting text came through. From the title alone it leaned "likely not relevant", because "Staff" usually means 8-10+ years, but said that was a guess, not evidence, and said nothing about sponsorship. It asked me to paste the full description.

Attempt 2. I pasted the full Zoox "Senior Network Security Engineer" posting into a new Claude.ai chat and asked whether it's relevant for an F-1 network-engineering master's student who needs sponsorship.
* Its verdict: Not relevant.
* Seniority: Yes, it noticed the "8+ years" requirement, and it was the main reason for the verdict. It also quoted the ownership-level duties and said "you do not need to match every expectation" doesn't cover a gap of about eight years.
* Sponsorship: It said the posting is silent. It noted no mention of sponsorship, OPT, or work authorization, said you can't tell from the text whether Zoox would sponsor, and suggested asking a recruiter. It didn't guess.
* Citations: Five quotes, all real. Two were trimmed mid-sentence ("...and ZTNA solutions," which drops the "(Zscaler, Netskope...)" list, and "...to apply," which drops "for this position"). Neither trim changes the meaning.
* Can read / write / send: In this chat it used only the text I pasted. Correction to my assumption: this Claude.ai account does have web search, saved memory, and past-chat search. It didn't use any of them here, didn't fetch the job board, and can't send anything.
* What could go wrong: Everything rests on the pasted text (Attempt 1 shows a copy mistake gives a guess instead of an answer), and the posting has no location, salary, date, or work-authorization line. "Not relevant" is driven by seniority, so a student who reads it as "Zoox won't sponsor" would be drawing a wrong conclusion. Senior roles sometimes still hire people with less experience.

*The paragraph below was drafted by Claude (claude.ai chat) from the run records and approved by Prathamesh. It was revised 2026-10-31 14:41 EDT at Prathamesh's instruction.*

Compared with my agent: My agent already ran on this exact posting. Both its rule (record) and Claude judge v1 (both runs used the pre-fix v1 template) said "relevant": the title passes, there's no authorization phrase, and it matches 6 of my résumé's networking skills. Neither looks at seniority, so both missed the 8+ years requirement that drove the chat's "not relevant". On sponsorship, the chat said the posting is silent; my agent has no explicit 'silent' output, and its record only shows that Gate 2 found no refusal phrase. Neither guessed.

## (b) Give Claude a file

**Setup described:** Claude (Claude Code, or `claude -p` with only a file-read tool) is given one saved file, for example a single posting
extracted from `raw/2026-10-30/zoox.json` plus `fixtures/resume.fictional.json`, and asked for the judgment in the fixed schema.
**Status: not yet performed as a separate surface.** The closest thing that ran is the `jobwatch.py judge` path, where the harness inlines the
posting and résumé into the prompt rather than handing Claude a file path (F17; seeded run F24).

| | |
|---|---|
| Can read | The file(s) it is given. If the file tool is not confined, other files in the working directories too (Claude Code's Read and Glob tools are scoped to its working directories) |
| Can write | Nothing, if only Read is allowed. With Write/Edit allowed, any file in its working directories |
| Can send | The file contents go to Anthropic as model input. No network calls to job boards, and no messages to anyone |
| Authority needed | A Claude account session; permission to read that file; the user choosing which file to hand over |
| How it can fail | The wrong or stale file is handed over (no hash check unless added). Text inside the posting is treated as instructions (prompt injection). The output is free text unless a validator is run afterwards. Citations are invented or paraphrased (W1). If write tools are allowed, files are changed outside the intended scope. A real résumé is handed over by mistake, and nothing in this surface enforces `fictional: true` |
| Evidence | none yet |

## (c) Let the agent fetch and write state (`jobwatch.py`)

**What ran:** the real fetches on 2026-10-30 18:11 and 2026-10-31 13:27; run 1 (baseline) 2026-10-30 18:35; run 2 2026-10-31 13:27; SEEDED runs 2026-10-31 13:43–13:44.

| | |
|---|---|
| Can read | `https://api.lever.co/v0/postings/zoox?mode=json` (one GET per fetch); the local résumé fixture; `state/seen_ids.json`; saved raw files; `prompts/judge_v1.md` |
| Can write | `raw/<date>/` (refuses to overwrite), `state/seen_ids.json` (atomic replace, written last), `runs/`, `judgments/`, `seeded/` |
| Can send | One HTTPS GET to `api.lever.co`. With `--judge claude`, each new posting's text plus the fictional résumé goes to Anthropic through `claude -p` (no tools, no session persistence). No code path applies, emails, messages, posts, or logs in (static test) |
| Authority needed | Network egress to api.lever.co; write access to the assignment folder; permission to spawn the `claude` CLI under the user's logged-in Claude account (this incurs cost: $0.069 for one call on 2026-10-30, as reported by the CLI) |
| Guards that exist (tested) | Host allow-list, including redirects checked before they are followed; `fictional: true` plus `@example.com` résumé gate; the state is untouched on a failed run; judgment validator; judgment never alters record; SEEDED label carried in the report |
| How it can fail | Lever changes the schema or rate-limits. The board is identical across days, so there is nothing to show (it happened: run 2 new=0). Rerunning `run` on the same raw file silently advances the state (the state is "last run", by design). Posting text can try to steer the judge (tools are disabled, but the verdict can still be swayed). The judge's output is rejected because of path-format mismatch (it happened: 4 of 5 in the SEEDED run, F24). Seeded data is mistaken for real if the labels are dropped. Cost grows with the number of new postings, since there is one Claude call each |

## Least autonomy that is enough

*Prathamesh's choice and defense (2026-10-31). The "What I limited" paragraph was edited for accuracy by Claude (claude.ai chat) and approved by Prathamesh. Its last sentence was selected by Claude Code from Prathamesh's two alternatives, after the write-limit check (14:55 EDT): writes are not confined in code.*

Watching for new postings across days needs memory of what I've already seen between runs, fetching the board again on later days, and a dated log I can check. A chat only sees what I paste in at that moment. So the least autonomy that is enough is the agent, but only for watching across days. Judging a single posting needs nothing more than a chat.
What I limited: it can only fetch from https://api.lever.co (the allow-list, enforced in code and tested). It can't send anything, so no email or messages. The judge runs with tools turned off, so it sees only the posting text. It writes only to the paths I give it on the command line; confining writes to the project folder is not enforced in code.
