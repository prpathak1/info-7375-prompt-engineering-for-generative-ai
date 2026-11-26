# FILTER.md: what reaches me, and why

- **Version:** **v0.3** (recorded 2026-11-25 19:28:46 EST). v0.1 was drafted by Claude Code (Opus 5.5) at about 18:43 EST and all 23 rules were APPROVED by Prathamesh at 2026-11-25 18:46:08 EST. The v0.2 and v0.3 changes are Prathamesh's decisions after measurement (changelog).
- **Status:** the v0.1 rules are APPROVED. v0.2: A1 CHANGED (EAR), A7 NEW, K1 known limit recorded. v0.3: A2 CHANGED (export-license exception, which falls to A7). The older wording is kept in the changelog.
- **Persona:** the fictional `fixtures/resume.fictional.json` (Tanvi Kulkarni: F-1 student, MS in networking, needs sponsorship, target SOC 15-1241). It is not a real resume.
- **Origin tags:** `[JS1]` = from JS1 CONTRACT §4 or `jobwatch.py` (title regexes from `filter_titles.py` @ f3ea8b7). `[JS2]` = from JS2 GATE. `[NEW]` = proposed for JS3.
- **Versioning rule:** any change after measurement makes a new version (v0.2, ...). The old wording stays in the changelog at the bottom with a date and the measurement that caused it. Rules are never edited silently.

## 0. Decision shape

Each posting goes through these gates, in order. The first gate that fails decides the outcome.

| Outcome | Meaning |
|---|---|
| `accept` | Passed every gate. It goes on the shortlist with labelled evidence (section 2). |
| `reject` | One gate failed. The reason is recorded with the quoted text. |
| `flag` | A human decides. Used when a rule explicitly hands the decision to me. It counts as neither accept nor reject in the metrics. |
| `abstain` | There isn't enough posting text to judge (section 2.4). |

## 1. Rules

### Gate 1: title, role and topic

| ID | Rule | Origin | Reasoning (one line) | Status |
|---|---|---|---|---|
| T1 | The title must contain whole-word `network`, `networks` or `networking`. Case is ignored. | [JS1] | The target is SOC 15-1241, and the title is the cheapest and most reliable signal of what the job is. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| T2 | Reject if the title has a false-friend phrase: `road / social / neural / sales / partner / retail / distribution` + network. | [JS1] | Here "network" means a road map, a model or a sales channel, not IP networks. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| T2a | Add these false friends: `champion network`, `network-on-chip` / `NoC`, `network strategy` when the title has no engineer word. | [NEW] | Seen on 2026-11-25 in the OpenAI and Cloudflare titles: a community program, chip RTL, and a business-strategy role. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| T3 | Accept only if the title also has a role word: `engineer, engineering, architect, administrator, admin, security, infrastructure`. | [JS1] | "Network" alone appears in manager, strategy and program titles. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| T3a | Treat `technician` and `operations` as role words that send the posting to `flag`, not `accept`. | [NEW] | "Datacenter Networking Technician" is real network work but may sit outside 15-1241. That's my call, not the filter's. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| T4 | If the title has `software`, send it to `flag`. | [JS1] | A software engineer on a network team may be SOC 15-1252. A human decides. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| T5 | If the title has `network` but no role word, send it to `flag`. | [JS1] | An unknown shape shouldn't be silently rejected. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |

### Gate 2: work authorization (searched in the body text, not the title)

| ID | Rule | Origin | Reasoning | Status |
|---|---|---|---|---|
| A1 | Reject on any whole-word phrase (with optional plural `s`): `U.S. citizen, US citizen, U.S. citizenship, U.S. person, security clearance, active clearance, ITAR, EAR, export control`. **v0.2:** `EAR` matches only as exact uppercase `EAR`, whole word, no plural. | [JS1] | Each phrase breaks a `constraints.excluded` entry for an F-1 holder. | APPROVED 18:46:08 EST; **CHANGED v0.2** (Prathamesh, 2026-11-25) |
| A2 | Reject on a sponsorship refusal: `without sponsorship, without visa sponsorship, no sponsorship, not sponsor, will not sponsor, unable to sponsor, cannot sponsor, does not sponsor`. **v0.3:** `without sponsorship` does **not** count when the same sentence continues `for an export license` (that is export-license sponsorship, not visa sponsorship); such sentences fall to A7. | [JS1, amended 2026-10-31] | The persona needs sponsorship, so a refusal ends the case. | APPROVED 18:46:08 EST; **CHANGED v0.3** (Prathamesh, 2026-11-25) |
| A3 | **Negation guard:** if an A1 phrase sits within 5 words after `no`, `not` or `without` (for example "security clearance **not required**", "no clearance needed"), send it to `flag`, not `reject`. | [NEW] | Matching the words is not the same as the posting meaning them. JS1 would reject these postings for the wrong reason. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| A4 | Treat `must be authorized to work in the U.S.` as **not** a refusal. Record it as "authorization stated, sponsorship unknown", which means `insufficient`. | [NEW] | F-1/OPT holders are authorized to work, so this phrase is a false friend for "no sponsorship". | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| A5 | If no A1, A2 or A4 phrase appears, the authorization claim is labelled **"posting is silent"**. It is never labelled "sponsors". | [NEW; gap seen in JS1 ACTION-SURFACES] | Silence is not a yes. JS1 had no explicit "silent" output. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| A6 | Also add `green card`, `permanent resident`, `U.S. persons only` to A1. | [NEW] | These are common exclusion phrasings that JS1 lacked. Still unmeasured. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| A7 | **v0.2.** An `export control` hit inside a sentence that says `may require access` → `flag` (sponsorship unknown), not reject. **v0.3:** also an A2 `without sponsorship` hit directly followed by `for an export license` → `flag`. Explicit exclusions (every other A1, A2 or A6 hit) still reject. | [NEW v0.2] | The audit (R16, N05) found Cloudflare's "may require access to information protected under U.S. export control laws" is ambiguous for an F-1 holder, not an exclusion. | **NEW v0.2** (Prathamesh, 2026-11-25) |

### Gate 3: seniority (all new)

Source: my JS1 experiment on 2026-10-31. The chat judged Zoox "Senior Network Security Engineer" not relevant mainly because of "8+ years", while my JS1 rule and the judge both said "relevant" (JS1 FRICTIONAL F13). The final film makes the same point.

| ID | Rule | Origin | Reasoning | Status |
|---|---|---|---|---|
| S1 | Reject if the title has a whole-word `Senior, Sr., Staff, Principal, Lead, Manager, Director, Head of, VP`. | [NEW] | These levels assume years the persona doesn't have, and JS1 accepted one of them. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| S2 | A level numeral (`I`, `II`, `1`) counts as entry level **only** directly after `Engineer`, `Technician` or `Administrator`. `Manager I` is still a manager (S1). | [NEW] | Seen on 2026-11-25: a quick regex matched "Manager I" at Datadog as junior. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| S3 | Read years from the body only when the pattern is `<N>+ years` / `<N> or more years` / `minimum of <N> years` with `experience` within 6 words. Take the **smallest** stated N. Then: N ≤ 2 → fits; N = 3–4 → `flag` (near the threshold); N ≥ 5 → reject. | [NEW] | "Years" also appears in "2 years ago" and in benefits text. The smallest N is the posting's floor, and a "preferred" larger N shouldn't count against the persona. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| S4 | No years stated and no S1 title word → the seniority claim is `insufficient`, and the posting still passes Gate 3. | [NEW] | Most postings don't state years. Rejecting on silence would empty the list (OpenAI "Network Engineer" ×2 state none). | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| S5 | `new grad`, `entry level`, `early career`, `junior`, `associate`, `0-2 years` in the title or body → the seniority claim is `supported`. | [NEW] | These are the explicit fit signals I'm looking for. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |

### Gate 4: skills

| ID | Rule | Origin | Reasoning | Status |
|---|---|---|---|---|
| K1 | Accept only if at least **2** distinct `skills.networking` terms match as whole words (plural allowed) in the body. | [JS1] `SKILL_THRESHOLD = 2` | One term can be a coincidence. Two suggests real network work. The threshold was hand-set in JS1, never fitted. **Known limit (v0.2):** the skills list misses phrasings such as "networking systems" (audit N02). Recorded, not changed. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| K2 | Don't count `switching` in `context switching`, `routing` in `call / ticket / request routing`, or `DNS` inside a URL. | [NEW] | These are lexical false friends for skills (predicted; to check in the audit). | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| K3 | Only `skills.networking` counts toward K1. Security, cloud and automation terms are shown but don't count. | [JS1] | This keeps the threshold comparable with JS1 and JS2. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |

### Ranking of accepted postings

| ID | Rule | Origin | Reasoning | Status |
|---|---|---|---|---|
| R1 | Order by seniority evidence first (`supported` fit > `insufficient` > `flag`), then by the K1 match count, then by newest posting date. | [NEW] | Fit level matters more than keyword density. A Staff role with 9 skills must not outrank an entry role with 2. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |
| R2 | No numeric score beyond these counts. Any weight added later must be listed in the Chapter 9 inventory as hand-set, fitted or inherited. | [NEW] | Every number has to be accountable. | APPROVED (Prathamesh, 2026-11-25 18:46:08 EST) |

## 2. Evidence rules (shortlist claims)

Each accepted posting carries 4 claims: **title fit**, **authorization**, **seniority**, **skills**. Each claim gets exactly one label:

- **supported:** a verbatim quote from a named posting field (section 3) asserts the claim. A word appearing isn't enough: the sentence has to say it. Example: "0-2 years of experience" supports the seniority claim.
- **contradicted:** a verbatim quote asserts the opposite. Example: "8+ years" against the seniority claim, or "unable to sponsor" against the authorization claim. A contradicted claim on authorization or seniority turns the posting into a reject, with the quote.
- **insufficient:** no quote either way, or the only match is lexical without meaning. Examples: "BGP" in a list of the company's products, "security clearance" in "no security clearance required", "network" in "our partner network".
- Every quote must be found again in the stored raw text by exact substring match. A label whose quote can't be found again becomes `insufficient` (the inherited citation check, [JS1]).

**2.4 Abstain** (outcome `abstain`, which never counts as accept or reject) when:
1. the body text is missing or shorter than 200 characters after stripping HTML, or
2. **both** authorization and seniority are `insufficient` **and** the title has no T3 role word.

**Known limit of the abstention rule (counterexample to show in the build):** OpenAI "Network Engineer" states no years and no sponsorship line, so authorization and seniority are both `insufficient`. It still passes, because its title has a role word. The rule doesn't abstain, yet the two facts that matter most are unknown. Rule 2 catches thin titles, not thin evidence.

## 3. Expected sources

| Board (platform) | Collected | Title field | Body fields searched | Other fields used |
|---|---|---|---|---|
| Lever (`zoox`) | 2026-10-30, 2026-11-10 | `text` | `descriptionPlain`, `lists[].content` (HTML stripped), `additionalPlain` | `categories.commitment`, `categories.location`, `hostedUrl`, `createdAt` |
| Greenhouse (`cloudflare`, `fastly`, `datadog`) | 2026-11-10, 2026-11-25 | `title` | `content` (HTML entity-escaped: unescape, then strip) | `location.name`, `updated_at`, `first_published`, `absolute_url` |
| Ashby (`openai`) | 2026-11-10 | `title` | `descriptionPlain` | `location`, `employmentType`, `isRemote`, `publishedAt`, `jobUrl` |

**Missing data:**
- A missing title → `abstain`.
- A missing or short body → `abstain` (2.4).
- A missing date → rank last within its tier; never invent a date.
- A field with an unexpected type → `FormatChanged` for that board (inherited from JS2), and the board is skipped and logged.
- Duplicate captures of the same board and ID (Zoox 10-30 and 11-10, the Cloudflare and OpenAI double files) → judge the newest capture once.
- No value is ever filled in from outside the posting.

## 4. Wrong versions the tests must catch

| ID | Wrong filter or ranking | Why it looks plausible | Named test (to write) |
|---|---|---|---|
| W1 | Substring instead of whole-word matching for Gate 2 | Simpler code | `test_years_does_not_trigger_EAR`: a body with "5 years of experience" is not rejected for export control |
| W2 | Level numeral read anywhere | "I" = level 1 | `test_manager_I_is_not_entry_level`: "Manager I, Engineering - Zero Trust Networking" is rejected by S1 |
| W3 | Rank by skill-match count only | More keywords = better fit | `test_entry_role_outranks_staff_role`: a 2-skill "Network Engineer, 0-2 years" ranks above a 9-skill "Staff Network Engineer" |
| W4 | Gate 2 without a negation guard | The phrase list worked in JS1 | `test_clearance_not_required_is_flag_not_reject` |
| W5 | Treating authorization silence as a pass ("sponsors") | Nothing negative was found | `test_silent_posting_labelled_silent_not_supported` |

## Changelog

- v0.1 (2026-11-25): drafted 18:43 EST by Claude; all 23 rules approved by Prathamesh 2026-11-25 18:46:08 EST. It brings in T1–T5, A1, A2, K1 and K3 from JS1, and proposes T2a, T3a, A3–A6, S1–S5, K2, R1 and R2 as new.

- **v0.2 (2026-11-25 19:11:37 EST), Prathamesh's decisions after the reject audit** (verdicts in `audit/AUDIT-VERDICTS.json`: 37 rows judged, 4 disagreements):
  1. **A1 changed:** `EAR` matches only as exact uppercase, no plural. *Measurement:* 1 of 9 v0.1 A1 rejects (Cloudflare "Network Security Engineer", 8081027) matched the text "ears" ("the eyes and ears of Cloudflare"). v0.1 wording: "`EAR`" in the whole-word, plural-allowed, case-insensitive list.
  2. **A7 new:** "may require access ... export control" sentences → flag, sponsorship unknown. *Measurement:* 8 of 9 v0.1 A1 rejects came from one Cloudflare sentence. The audit disagreed on R16 and N05.
  3. **K1 known limit recorded, not changed:** *measurement:* N02 "Software Engineer, Core Network Engineering" was rejected with 0 skills, while its duties say "networking systems".
  - **Rejected (not adopted):** none.
  - **Measured effect on the 1,964 non-held-out postings** (`demo/06-v01-to-v02-diff.txt`): 9 postings changed their deciding rule (A1 → A2), and **0 changed outcome**. All 9 also contain "...export laws without sponsorship for an export license.", which A2 ("without sponsorship") rejects. R16 and N05 therefore still don't reach a human under v0.2. Whether A2 should change is open, for Prathamesh.

- **v0.3 (2026-11-25 19:28:46 EST), Prathamesh's decision after measuring v0.2:**
  - **A2 changed:** `without sponsorship` followed by `for an export license` in the same sentence no longer counts as a refusal. It falls to A7 (flag, sponsorship unknown).
  - *Measurement that caused it:* v0.2 changed 0 outcomes. All 9 postings it touched were still rejected, now by A2, on "...U.S. export laws without sponsorship for an export license." (`demo/06-v01-to-v02-diff.txt`).
  - *Tests first:* `demo/07-v03-tests-red.txt`: 2 new-behavior tests failed and 2 guards passed before the change. After the change: 181 tests, OK.
  - **Measured effect on the 1,964 non-held-out postings** (`demo/08-v02-to-v03-diff.txt`): the same 9 postings changed. **3 now reach a human** (flag): 8159206 "Network Security Engineer" (audit N05), 8081027 "Network Security Engineer" (the "ears" posting; A7 + S3) and 8088751 "Software Engineer, Cloudflare Network Interconnect" (T4 + A7).
    - The other 6 are now rejected by a later gate: S1 ×2, S3 ×1, K1 ×3. **R16 (8188468) is still rejected, now by K1 (1 skill).**
  - **On the held-out set** (SCORE.md, run C7): accepts unchanged. "Reaches me" rose from 2 to 4 (H06 and H15 now flag; both labelled not_fit).
