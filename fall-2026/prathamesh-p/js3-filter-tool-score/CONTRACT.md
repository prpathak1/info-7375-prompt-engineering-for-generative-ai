# CONTRACT: Job-Search Agent 1, The Contract and the Watch

> **Status:**
> Decisions made at approval: board = zoox (day-1 input `raw/2026-10-30/zoox.json`); the verdict is two-valued, with a flag
> title giving `not_relevant` plus `needs_human: true`; the folder is `fall-2026/prathamesh-p/js1-contract-and-watch/`.
> No implementation code exists yet. Nothing in this file is a result. Every "will" below is a promise
> the code and tests have to keep. It is not a report of what ran.

## 0. Scope in one line

There is one public Lever board, one fictional résumé, and only postings that are new since the last run.
Every new posting gets two verdicts, a **record** from the rule and a **judgment** from Claude, and each
verdict comes with a justification that cites named résumé fields and named posting fields.

## 1. In

| Input | Value | Notes |
|---|---|---|
| Board | **`zoox`** at `https://api.lever.co/v0/postings/zoox?mode=json` (chosen by Prathamesh 2026-10-30; see 1.1) | One GET per run. Lever public postings API. No login and no key. |
| Allowed host | `api.lever.co` only, over `https` | See section 3. |
| Résumé | `fixtures/resume.fictional.json`: fictional persona "Tanvi Kulkarni (fictional)", F-1, SOC 15-1241 | `@example.com` address and a 555 phone number. The schema follows the Reallocation Engine `search/examples/*/resume.example.json`. |
| State | `state/seen_ids.json`, the posting `id` values from the last successful run | Written only after the run's raw response is saved and hashed. |
| Requirements | Python 3.13 standard library only (`urllib.request`, `json`, `hashlib`, `re`, `unittest`). Claude Code CLI 2.1.314 (`claude -p`) for the judgment and sampling steps. | Follows the repo AGENTS.md rule of Python stdlib with Claude as the only model provider. The exact fresh-clone commands will go in README.md. |

### 1.1 Board recommendation: `zoox` over `shieldai`

Both boards were captured raw on 2026-10-30 (see `raw/2026-10-30/`). Counts below come from those files.

| | `shieldai` | `zoox` |
|---|---|---|
| Postings on 2026-10-30 | 654 | 227 |
| Raw size | 10.5 MB | 2.3 MB |
| Titles containing "network" | 5 (4 include, 1 flag) | 3 (2 include, 1 false friend) |
| Postings mentioning citizen/clearance text | 295 / 654 | 7 / 227 |
| `createdAt` within 3 days of fetch | 8 | 10 |

**Recommendation: `zoox`.** Three reasons:
- **Gate 2 has less to do.** On ShieldAI, every network title carries ITAR or clearance language. Almost every
  verdict would be "not relevant, ITAR" and would never exercise the résumé match.
- **The data already contains a real false friend.** "Software Engineer - Road Network Tools" sits in today's
  Zoox response, so a test can use real data for that case.
- **The files are smaller.** Committing two days of raw data costs about 4.6 MB instead of about 21 MB.

**Risk.** The second run lands on a Saturday, so Zoox may post nothing new. If 2026-10-31 shows no new IDs,
the fallback in the brief applies: a saved earlier response used as baseline, clearly labeled **seeded**
(see section 6). **Decision (Prathamesh, 2026-10-30):** zoox. Run 1 (baseline) uses the saved `raw/2026-10-30/zoox.json`.

## 2. Out

For each posting whose `id` is not in the previous state, the run outputs:

```json
{
  "posting_id": "<Lever id>",
  "posting_title": "<posting.text>",
  "record":   { "label": "record",   "verdict": "relevant | not_relevant", "gate_results": {...}, "citations": [...] },
  "judgment": { "label": "judgment", "verdict": "relevant | not_relevant", "citations": [...],
                "model": "<model id as reported>", "obtained_at": "<ISO timestamp>", "raw_response_file": "<path>" }
}
```

Each citation has this shape: `{ "resume_field": "skills.networking", "resume_value": "BGP", "posting_field": "descriptionPlain", "posting_value": "BGP" }`.

**Rules for any justification, record or judgment:**
- It cites at least one résumé field and at least one posting field.
- Every `resume_field` is a real JSON path in the résumé, and its `resume_value` appears at that path.
- Every `posting_value` is a case-insensitive substring of the named field in **that same posting**.
- A justification that breaks any of these is invalid. A record that breaks them is a bug that fails tests.
  A judgment that breaks them is rejected by the validator and stored as `rejected`. It is never repaired.

**Baseline behavior:** The first run against empty state saves raw data and state and reports **zero** new postings.

## 3. Refuses

| Refusal | Behavior | Test |
|---|---|---|
| Any host other than `api.lever.co`, any scheme other than `https`, or any redirect off-host | Exits non-zero before or at the request. Writes no state. | Points the URL at a different host, an `http://` URL, and a lookalike such as `api.lever.co.evil.example`. |
| Displaying or committing a real résumé | Loads only a path whose JSON has `"fictional": true` and whose email ends in `@example.com`, and refuses any other. The filename `resume.json` is gitignored in this folder. | Feeds it a résumé without `fictional: true` or with a non-example email, and expects a refusal. |
| Treating model judgment as fact | Claude output is only ever stored under `judgment` with `label: "judgment"`. It never overwrites, fills in, or breaks a tie for `record`. Reports print the two in separate labeled columns. | Checks that the record verdicts are byte-identical with the judgment step stubbed to either verdict. |
| Applying, emailing, messaging, logging in | The program has no code path for any of these. It makes one GET only. | Static check that the source contains exactly one network call site, and that it uses GET. |

## 4. Rule: hand-predictable relevance (the **record**)

Persona: a fictional F-1 network engineer targeting **SOC 15-1241 (Computer Network Architects)**.
The gates are evaluated in order. A posting is **relevant** only if it passes all three. The first failing gate
names the verdict's reason, and the results of all three gates are still recorded.

**Gate 1: Title.** This gate reuses the Reallocation-mode title filter as-is. Source:
`scripts/contrib/2026fa/prpathak1-network-sponsorship-text/filter_titles.py`, function `decide()`,
commit `f3ea8b7` on branch `contrib/2026fa-prpathak1-mode-network-sponsorship-text` of
`prpathak1/the-reallocation-engine`. It reads `posting.text`.
- **exclude**: `\bnetwork(s|ing)?\b` does not match, or the false-friend pattern
  `\b(road|social|neural|sales|partner|retail|distribution)\s+network` matches. The verdict is not relevant.
- **flag**: "network" plus "software" (it may be SOC 15-1252 rather than 15-1241), or "network" with no
  recognised role word. The verdict is **not relevant** with `needs_human: true` and the flag reason, because the
  rule cannot establish relevance. The verdict stays two-valued; there is no third value (decision: Prathamesh, 2026-10-30).
  Gates 2 and 3 are still evaluated and recorded for flagged postings.
- **include**: "network" plus a word from engineer/engineering/architect/administrator/admin/security/infrastructure,
  and no "software". The posting passes the gate. Cites `target.soc_code` and `target.title_terms`.

**Gate 2: Work authorization.** This gate searches `descriptionPlain`, every `lists[].content` with tags
stripped, and `additionalPlain`. The match is case-insensitive and uses this fixed phrase list:
`U.S. citizen`, `US citizen`, `U.S. citizenship`, `U.S. person`, `security clearance`, `active clearance`,
`ITAR`, `EAR`, `export control`. **Every phrase must match as a whole word**: no letter, digit or underscore may come
directly before or after it. Punctuation and hyphens count as boundaries, so "ITAR-controlled" is a hit and "military" is not.
*Amended 2026-10-30 18:33:42 EDT by Prathamesh, before any implementation existed. The earlier wording made only "EAR" whole-word.
Reason: substring matching gives false hits, such as "ITAR" inside "military" and "EAR" inside "years", and rows 2 and 3 both contain "years".*
**A phrase may also be followed by a single `s`, as in Gate 3**, so "U.S. citizens", "security clearances" and "U.S. persons" are hits. "US citizenry" still is not.
*Amended 2026-10-30 18:38:50 EDT by Prathamesh. Reason: postings often say "must be U.S. citizens", and missing it would wrongly mark a
citizenship-only job relevant.*
**Sponsorship-refusal phrases**, matched by the same rules (whole word, case-insensitive, optional trailing `s`): `without sponsorship`,
`without visa sponsorship`, `no sponsorship`, `not sponsor`, `will not sponsor`, `unable to sponsor`, `cannot sponsor`, `does not sponsor`.
A bare `sponsorship` is deliberately **not** a phrase, because it would reject "visa sponsorship available". A hit on one of these cites
`visa.needs_sponsorship` and `visa.type`. No `constraints.excluded` entry names sponsorship refusal, so none is cited for these phrases.
*Amended 2026-10-31 14:16:58 EDT by Prathamesh. Reason: Prathamesh's hands-on LinkedIn check (ALTERNATIVES.md (b)) found a Parallel Wireless posting
requiring candidates to "be authorized to work in the U.S. without sponsorship", and the previous Gate 2 list had no hit on that wording.*
Any hit makes the posting not relevant. The citation names
`visa.needs_sponsorship`, `visa.us_person_for_itar`, and `constraints.excluded`, along with the matched phrase and its field.
(*Known coarseness:* "EAR" as a whole word, or a posting that says "No security clearance required", will
trip this gate. Bare "clearance" is not a phrase, so "no clearance required" does not. The rule stays deliberately dumb so it remains
predictable, and the coarseness is listed under "not checked".
*Amended 2026-10-31 14:41 EDT by Prathamesh. Reason: the earlier example ("no clearance required" trips the gate) was wrong. It was checked on
2026-10-31: no hit for "No clearance required.", and a hit ("security clearance") for "No security clearance required."*)

**Gate 3: Skills overlap.** At least **2** distinct terms from `skills.networking` must appear in
`descriptionPlain` + `lists[].content` + `additionalPlain`. A term matches if the term itself, or the term followed
by `s`, appears as a whole word (case-insensitive). For example, "firewalls" matches `firewall`. Each matched
term is cited under `resume_field: skills.networking`, with `posting_value` set to the exact text found in the
posting. If fewer than 2 distinct terms match, the posting is not relevant.
*Amended 2026-10-30 by Prathamesh, after approval and before any implementation existed. The draft rule required
an exact whole word, so "firewalls" did not match `firewall`. Prathamesh changed it so that plurals count, because
"firewalls" should match "firewall".*

**Not criteria (on purpose):** location (`constraints.open_to_relocation: true`), salary, seniority, and
`workplaceType`. These are listed so that nobody adds them silently.

**Hand-prediction check:** Before the code runs on new data, Prathamesh labels at least five postings by hand with this
rule, and the tests assert that the code agrees. One example from today's raw data: "Software Engineer - Road Network Tools"
fails Gate 1 because of the false friend "road network".

## 5. Wrong versions the tests must catch

**W1: The justification does not cite the evidence.** This implementation emits the right verdict with a generic
reason ("strong match with candidate's networking background"), or cites `skills.networking: "BGP"` when
the posting never mentions BGP. This is the common failure of LLM-style justification.
*Caught by:* a test that, for every citation, checks `resume_value` exists at `resume_field` and
`posting_value` is a substring of `posting[posting_field]` for the same `posting_id`. A fixture
posting that passes Gates 1 and 2 but mentions only one résumé skill must come out not relevant, with exactly one cited term.

**W2: The verdict is attached to the wrong posting.** The verdicts are computed correctly but joined back to
postings by list position after one side was sorted or filtered. A typical cause is filtering new IDs from one
list and zipping with the unfiltered one. Every verdict then sits next to its neighbour's title.
*Caught by:* a fixture with a relevant posting next to a not-relevant one in reversed order, plus a state that
makes only the second one new. The test asserts each output's `posting_id`, `posting_title`, and citations
all come from the same source object, and that the run reports exactly one new posting.

(One more case is covered by tests rather than as a named wrong version: a naive `"network" in title` match that marks
"Road Network Tools" as relevant.)

## 6. Watch semantics

- `state/seen_ids.json` is `{"ids": [...]}`, and after each successful run it holds **exactly** that run's ID set. It is not a running
  union of every run (confirmed by Prathamesh 2026-10-30).
- **New** means `id` is in today's response and absent from the previous `state/seen_ids.json`. Removed postings
  are logged as a count only.
- Every run writes `raw/<YYYY-MM-DD>/<board>.json` unmodified, with a `.fetch.txt` holding the UTC and local
  timestamps, the HTTP status, the byte count, and the SHA-256.
- The state is updated only after the raw file is saved and hashed. A failed run leaves the state untouched.
- **Seeded fallback:** If the real second-day run shows no new IDs, the change is demonstrated by
  diffing against an earlier saved response with postings removed. Any such output is labeled **SEEDED**
  in its filename and its header. Today's real 2026-10-30 capture stays the real baseline either way.

## 7. Failure: approved by Prathamesh before any run

> Drafted by Claude (claude.ai chat) at Prathamesh's request. Reviewed and approved by Prathamesh on 2026-10-30,
> before any implementation run. Claude Code inserted the approved text verbatim and must not edit it.
> (Provenance corrected 2026-10-30 18:28:43 EDT. An earlier note said "Wording is Prathamesh's"; see FRICTIONAL F8.)

Date: 2026-10-30 18:21:29 EDT

"Failure would look like: on the 2026-10-31 run, the watch reports a Zoox posting as "new" even though its ID was already in the 2026-10-30 snapshot (or misses one that wasn't); or a verdict marks a false friend like "Software Engineer - Road Network Tools" as relevant, or Claude's justification cites a résumé skill or posting text that isn't actually there."
