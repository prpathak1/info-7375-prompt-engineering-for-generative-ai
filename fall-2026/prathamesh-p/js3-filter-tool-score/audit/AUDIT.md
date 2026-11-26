# Reject audit: FILTER v0.1, 2026-11-25 (with the measured effect of v0.2 and v0.3)

- **Sheet:** `AUDIT-SHEET.md`. Seed 7375; the sample is in `AUDIT-SAMPLE.json`.
- **Verdicts:** `AUDIT-VERDICTS.json`.
- **Who judged:** Claude (claude.ai chat) drafted the verdicts from the rows Claude Code printed. Prathamesh reviewed and approved them (2026-11-25). These are therefore not independent human judgments. They are Claude-drafted verdicts that a human approved.

## What was judged

| Group | Rows | Agree | Disagree |
|---|---:|---:|---:|
| Random rejects (seed 7375, from 1,963 rejects) | 30 | 29 | 1 (R16) |
| Near-threshold (definitions in `audit_sheet.py`) | 5 | 3 | 2 (N02, N05) |
| Accepts (only 1 existed) | 1 | 1 | 0 |
| Extra: 9th A1 reject, found by the 19:0x printout, not sampled | 1 | 0 | 1 (X01) |

## Observed mistakes

1. **X01: false friend "ears".** The A1 phrase `EAR`, with plural allowed and case ignored, matched "the eyes and ears of Cloudflare". The posting was rejected for export control on a figure of speech. This is the **false friend** the brief asks for: it matched for the wrong reason.
2. **R16 and N05: ambiguous sentence treated as an exclusion.** "This position may require access to information protected under U.S. export control laws" doesn't say an F-1 holder is excluded. 8 of the 9 v0.1 A1 rejects came from this one Cloudflare boilerplate sentence. So one sentence decided almost every authorization reject.
3. **N02: the skills list misses phrasings.** The title "Software Engineer, Core Network Engineering" (T4 flag) has duties about "networking systems", but it matched 0 of the 10 listed skills. K1 rejected it before a human could see the T4 flag.

## Rule changes after measurement (FILTER.md changelog v0.2)

- **Added or changed:**
  - A1 now matches `EAR` only in exact uppercase.
  - A7 (new): "may require access ... export control" → flag.
- **Recorded, not changed:** the K1 known limit (N02).
- **Rejected:** none.
- **Measured effect of v0.2:** 0 outcomes changed out of 1,964.
  - All 9 also contain "...export laws **without sponsorship** for an export license.", and A2 rejects that.
  - So R16 and N05 are still rejected, now by A2, on a phrase about export licenses, not visas.
  - This was open for Prathamesh, who then decided v0.3.
- **v0.3 (Prathamesh, 2026-11-25):** `without sponsorship` directly followed by `for an export license` no longer counts as A2; it falls to A7 (flag).
  - Measured on the same 1,964 postings (`demo/08-v02-to-v03-diff.txt`), 3 outcomes changed, reject → flag:
    - **N05** (8159206), now flag A7: the audit's intent is met.
    - **X01**, the "ears" posting (8081027), now flag A7 + S3.
    - 8088751 "Software Engineer, Cloudflare Network Interconnect", now flag T4 + A7.
  - **R16 (8188468) is still rejected, now by K1** (1 networking term). The audit verdict "should flag" isn't met. The reason is now the skills list, the same known limit as N02, not the export-control sentence.

## Limits of inference from this sample

- **Random rejects:** 29 of the 30 were decided by T1, the title having no "network". The judges agreed with all 29.
  - That gives 0 observed misses in 29 draws from about 1,944 T1 rejects.
  - It is **not** a measured miss rate for all rejects. By the rule of three, 0 in 29 is still consistent with a true miss rate up to about 10% (95%), which could be up to about 190 postings.
  - The sample can't distinguish "no network jobs behind non-network titles" from "few enough that 29 draws missed them".
- **The other gates:** only 1 random reject came from them. They are seen mostly through the 5 near-threshold cases, which were chosen by definition, not at random, so their disagreement count (2 of 5) is not a rate either.
- **Accepts:** 1 of 1 agreed. That says nothing about the precision of accepts in general.
- **Who judged:** both the judging and the filter's rules came from Claude-assisted drafts. Shared blind spots wouldn't show up as disagreements.
