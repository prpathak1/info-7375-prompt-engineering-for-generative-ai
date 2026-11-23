# TRANSCRIPT-CHECK.md

faster-whisper `small` (CPU, int8), language en. Compared word by word with `narration_text` after lower-casing, stripping punctuation and splitting hyphens.

| Beat | Match | Differences (expected → heard) | Heard |
|---|---|---|---|
| B00 | 95% | `prathamesh` → `prathamish` | I'm Prathamish Pathak, and this is the film for my final project, Honest Shortlist. This synthetic voice is reading my script. |
| B01 | 100% | none | Honest shortlist will give an international network engineering student a short daily list of new jobs. Every claim about a posting will point to the sentence it rests on, or say the posting doesn't say. |
| B02 | 97% | `twentieth` → `20th` | Why care? Sponsorship. On October 20th, I checked seven network engineering postings at three employers. None offered sponsorship. Two required a security clearance, which by inference rules a visa holder out. Five said nothing at all. |
| B03 | 70% | `zoox` → `zooks`; `one thousand three hundred sixty four h one b` → `1 364 h1b` | Company history doesn't settle it. Zooks had 1,364 H1B approvals, yet all three of its network postings were silent. |
| B04 | 89% | `linkedin` → `linked in`; `linkedin's` → `linked in`; `thirty first` → `31st` | What exists already? Linked-in alerts send new matching postings. When I looked at linked-in search results on October 31st, the match reasoning sat behind a click. A no sponsorship requirement wasn't flagged, and closed postings still showed up. |
| B05 | 97% | `paste` → `pasted` | A chat assistant, given one pasted posting, did better. It caught eight plus years and said the posting was silent on sponsorship. But it only knows what I pasted. My own first version called that posting relevant. |
| B06 | 83% | `six hundred thirty one` → `631`; `six hundred fifty three` → `653` | and the reallocation engine's existing fetcher silently dropped 631 of SHIELD, AI's 653 postings, including every network posting with clearance wording. Its output still looked clean. |
| B07 | 100% | none | So why mine? It will watch the boards itself like an alert, show its evidence like a careful reader and say silent when a posting is silent. |
| B08 | 100% | none | Here's how. The data will be public greenhouse, lever, and Ashby job feeds. No logins, no LinkedIn, or indeed scraping, and it will never apply, email, or message anyone. |
| B09 | 87% | `one` → `1`; `tenth` → `10th`; `one four oh four` → `1404` | Step 1 already ran in JS2 on November 10th, one fetch per board, inside a budget. Four boards took four of six requests, and a deliberately bad board got 1404 with no retry. |
| B10 | 87% | `too` → `two`; `zoox` → `zooks`; `thirty one` → `31` | Step two ran two, keep only new postings. Zooks had 31 new ones against my saved October state and a title rule screens for network roles. |
| B11 | 95% | `three` → `3`; `four` → `4` | Step 3 exists in my reallocation mode, not yet in the agent. Pull every sentence about sponsorship, authorization, or clearance. Step 4 is still to build. Label each claim supported, contradicted, or insufficient with a verbatim quote. |
| B12 | 95% | `js1` → `js one` | My JS One Validator already rejects any quote that isn't in the posting. Then a fresh fetch will confirm the posting is open, and I'll approve the final list. |
| B13 | 98% | `fifty` → `50` | Do I have what I need? The boards need no account. The code is standard library python on my laptop. My Claude code subscription handled the 50 judge calls in JS1. I haven't measured how far it stretches for daily runs across many boards. |
| B14 | 90% | `twenty` → `20`; `a hundred percent` → `100` | How will I know it worked? JS1 left a warning. All 20 test postings were not a fit, so always answering not relevant scored 100%. Pass rate alone proved nothing. |
| B15 | 96% | `forty` → `40`; `labelled` → `labeled` | So I'll measure false positives, a supported label whose quote doesn't back the claim, and false negatives. For evaluation, I'll build a new held-out set of about 40 postings from more boards, labeled by me before I see any output, including real entry-level fits and false friends. |
| B16 | 100% | none | It worked if it finds most real fits without calling any clearance or citizenship-only posting relevant, beats the always-insufficient baseline on those fits, and verify catches every planted failure. |
| B17 | 100% | none | Zero tolerance for calling a posting relevant when it rules out sponsorship. Missing a real fit is a rate I'll report, not a pass or fail. Every claim will carry its evidence, and silence will be called silence. |
