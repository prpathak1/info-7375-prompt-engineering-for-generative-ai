# Prompt experiment report (Chapter 2)

> **Results are dated Claude responses (judgments), not facts.** All calls were made on 2026-10-31 with `claude-opus-5-5` (as reported by the CLI), through `claude -p`, one fresh
> session per call. The numbers are computed by `experiment/score.py` from the files in `experiment/results/`, and `summary.json` holds the full output.

## Data and labels
- There are 20 real Zoox postings from `raw/2026-10-30/zoox.json`, listed in `experiment/candidates.json`. The dev/held-out split is seeded (20261030). Row 2 (`8321d00e`) was swapped out of
  held-out on 2026-10-31 because it had been examined before tuning (see `"swaps"` there).
- The labeling rule, `experiment/LABELING-RULE.md`, was written before the labels.
- The labels are in `experiment/labels.json`. Claude (claude.ai chat) drafted them from the sheet excerpts, and Prathamesh reviewed and approved them before seeing any judge output on these
  postings.
- The set was **not rebalanced** (Prathamesh's decision, 2026-10-31).

## Class balance and trivial baseline
| Split | n | fit | not fit | "always not_relevant" passes |
|---|---:|---:|---:|---:|
| dev | 10 | 0 | 10 | 10/10 (100%) |
| held-out | 10 | 0 | 10 | 10/10 (100%) |

## The one change
- **Baseline:** `prompts/judge_v1.md`, sha256 `f55c7c68cf04c36ecd3300c8dacd48b1243644fd47e051604557e5927f946272`.
- **Change:** `prompts/judge_v2.md`, sha256 `99ff01260298a4d32e1392c0688ef6aa600fd6e8f2855f6bf3bc652752a245f7`. This is v1 plus one added criterion, number 4: a seniority rule matching LABELING-RULE.md. Up to 3 required years is OK, and 4 or more
  is not. A Senior/Staff/Principal/Lead/Manager/Director title is not OK. Only required years count. `diff` shows no other edit.

## Results
Scoring: a call **passes** when the validator accepts it and its verdict equals the label. A **rejected** call counts as not passing. A **false positive** is an accepted `relevant` on a not-fit posting.

| Run | Prompt | Passed | False positives | Rejected | Trivial baseline | Window (EDT) |
|---|---|---:|---|---|---:|---|
| dev | v1 | 9/10 | 1: #8 Staff Network Security Architect | 0 | 10/10 | 14:23:09–14:23:28 |
| dev | v2 | 10/10 | 0: none | 0 | 10/10 | 14:23:28–14:23:45 |
| **held-out (once)** | **v2** | **9/10** | **0**: none | **1**: #14 Information Security Manager - Identity and Access Management (IAM) | 10/10 | 14:23:54–14:24:11 |

- **On dev:** v1's only miss was #8, the false positive that the sampling report also shows 4 of 4 times. v2 removed it.
- **On held-out (run once, no tuning after):** v2 had 0 false positives, and 9 of the 9 accepted answers matched the label. The one non-pass was a **validator rejection**, not a wrong verdict.
  For #14 (IAM Manager), Claude quoted "…SCIM, Kerberos…" with an ordinary space, and the posting has a non-breaking space (U+00A0) before "Kerberos". The verbatim-substring check failed.
  The output was stored as rejected and not repaired. The validator was **not** changed after seeing held-out.
- **For reference, the CONTRACT rule (record) on the same 20:** dev 9/10 (false positive: #8 Staff Network Security Architect),
  held-out 10/10. The record has no seniority criterion, by design.

## Limits
- **(a) Every label is "not fit".** All 20 labels are not fit, so the trivial "always not_relevant" baseline scores **100% on both splits**. Pass rate cannot show a prompt is better than doing nothing,
  and the meaningful measure is **false positives**. With zero fit postings, this experiment cannot measure **false negatives** at all. It says nothing about whether v2 would wrongly reject a genuinely fit posting,
  which is the risk that adding a seniority filter creates.
- **(b) Claude against Claude.** The labels were drafted by Claude (claude.ai chat) and reviewed by a human. The judge is also Claude, so agreement partly measures Claude agreeing with Claude.
- **Ten cases.** One posting is 10 percentage points. The dev improvement rests on one posting (#8), and held-out has one rejection. Neither difference is statistically meaningful.
- **Single run per condition.** Dev v1, dev v2 and held-out v2 were each run once. Only the 5 sampled postings (v1) have repeat data.
- **Exposure.** Four held-out postings (#11, #13, #14, #20) were examined by title only under the CONTRACT rule in `tests/hand_labels.json` before the experiment (FRICTIONAL F18/F21).
- **The validator's strict matching makes some rejections format problems, not judgment problems.** Examples are the non-breaking space on held-out and, before the fix, the index paths in the SEEDED run.
  A rejection counts as a fail here.
