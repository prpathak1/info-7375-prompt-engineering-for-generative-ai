# Sampling report (Chapter 1)

> **These are dated Claude responses (judgments), not facts.** The run was on 2026-10-31, 14:22:21–14:23:01 EDT. The model, as
> reported by the CLI, was `claude-opus-5-5`. The prompt was `prompts/judge_v1.md` (baseline v1, sha256 `f55c7c68cf04c36ecd3300c8dacd48b1243644fd47e051604557e5927f946272`).

## Method
- There were 5 dev postings. #8 and #6 were required by Prathamesh. The other 3 were drawn with `random.Random(20261031).sample` from the remaining 8 dev postings, as recorded in
  `experiment/sampling_selection.json`.
- Each posting was asked about **4 times, each in a fresh conversation**: a separate `claude -p --no-session-persistence` process with its own `--session-id`, no tools,
  and an empty working directory. That makes 20 calls, run by `experiment/run_judge_batch.py` with 4 in parallel.
- Every raw output is in `experiment/raw-judgments/sampling/`. Each output went through `validate_judgment` (the same validator as the watch).
- Labels come from `experiment/labels.json`. They were drafted by Claude in claude.ai and reviewed and approved by Prathamesh before any judge output on these postings existed.

## Variation per posting

| # | Posting | Label (Prathamesh-approved) | 4 verdicts | Unanimous | Agree with label |
|---|---|---|---|---|---|
| 8 | Staff Network Security Architect | not_fit | relevant×4 | yes | 0/4 |
| 6 | Software Engineer - Road Network Tools | not_fit | not_relevant×4 | yes | 4/4 |
| 5 | Senior/Staff Software Engineer - SRE, GitHub & CI/CD Infrastructure | not_fit | not_relevant×4 | yes | 4/4 |
| 7 | Staff Compute Systems Engineer | not_fit | not_relevant×4 | yes | 4/4 |
| 10 | Wireless Firmware Validation Engineer | not_fit | not_relevant×4 | yes | 4/4 |

Validator outcome: **20/20 accepted, 0 rejected.**

## Every call

| # | Posting | Repeat | Status | Verdict | Session ID | Requested → finished (EDT) |
|---|---|---|---|---|---|---|
| 8 | Staff Network Security Architect | 1 | accepted | relevant | `4637b740-a071-40cb-8c98-ef9d95f1ad08` | 14:22:21 → 14:22:33 |
| 8 | Staff Network Security Architect | 2 | accepted | relevant | `aa78bd1d-5176-41c9-893a-f4dda3f68fe8` | 14:22:21 → 14:22:35 |
| 8 | Staff Network Security Architect | 3 | accepted | relevant | `31593b63-f73a-4e6e-8cc2-650cb479db7e` | 14:22:21 → 14:22:35 |
| 8 | Staff Network Security Architect | 4 | accepted | relevant | `aef0236d-d56e-42cb-b5c8-bf0a84fad377` | 14:22:21 → 14:22:34 |
| 6 | Software Engineer - Road Network Tools | 1 | accepted | not_relevant | `c6ff036d-1c0b-4376-9d61-d692050bcd7f` | 14:22:33 → 14:22:40 |
| 6 | Software Engineer - Road Network Tools | 2 | accepted | not_relevant | `1f0a0405-664f-4317-bdf0-82d76e563484` | 14:22:34 → 14:22:40 |
| 6 | Software Engineer - Road Network Tools | 3 | accepted | not_relevant | `42b61fbc-8f45-4a16-8bf0-72b413bb184e` | 14:22:35 → 14:22:40 |
| 6 | Software Engineer - Road Network Tools | 4 | accepted | not_relevant | `ccdd74c8-1c8a-4c29-a4ab-1b84cf4c8f7f` | 14:22:35 → 14:22:41 |
| 5 | Senior/Staff Software Engineer - SRE, GitHub & CI/CD Infrastructure | 1 | accepted | not_relevant | `add75e72-906d-4d01-9fdb-01bae19989a7` | 14:22:40 → 14:22:46 |
| 5 | Senior/Staff Software Engineer - SRE, GitHub & CI/CD Infrastructure | 2 | accepted | not_relevant | `834a9ab0-2abd-4ac0-ad55-34300cbc2e73` | 14:22:40 → 14:22:46 |
| 5 | Senior/Staff Software Engineer - SRE, GitHub & CI/CD Infrastructure | 3 | accepted | not_relevant | `6872de15-a76c-4fe6-a1d2-3b371f2d3b94` | 14:22:40 → 14:22:46 |
| 5 | Senior/Staff Software Engineer - SRE, GitHub & CI/CD Infrastructure | 4 | accepted | not_relevant | `fb9cdd3c-4a88-483e-ae9d-08645e7ce736` | 14:22:41 → 14:22:46 |
| 7 | Staff Compute Systems Engineer | 1 | accepted | not_relevant | `ec9e5092-c829-4ffb-a96b-c3adf8f34c4a` | 14:22:46 → 14:22:52 |
| 7 | Staff Compute Systems Engineer | 2 | accepted | not_relevant | `e3712492-a0e4-4184-b8af-66b7228d5837` | 14:22:46 → 14:22:53 |
| 7 | Staff Compute Systems Engineer | 3 | accepted | not_relevant | `76052034-4b1f-416b-b51a-2c3ddf71e073` | 14:22:46 → 14:22:53 |
| 7 | Staff Compute Systems Engineer | 4 | accepted | not_relevant | `7d80c385-5139-4611-bfda-3eeae036b27d` | 14:22:46 → 14:22:54 |
| 10 | Wireless Firmware Validation Engineer | 1 | accepted | not_relevant | `a65ac542-52c3-4c4b-9f1b-f7ccaf6d2a1c` | 14:22:52 → 14:23:01 |
| 10 | Wireless Firmware Validation Engineer | 2 | accepted | not_relevant | `cb97a140-3a76-454e-95af-4e552756b579` | 14:22:53 → 14:23:01 |
| 10 | Wireless Firmware Validation Engineer | 3 | accepted | not_relevant | `76aa3307-201b-47d7-afbe-f845c36b9780` | 14:22:53 → 14:23:01 |
| 10 | Wireless Firmware Validation Engineer | 4 | accepted | not_relevant | `40dbd19b-9afd-4545-87c1-5ed4879047f3` | 14:22:54 → 14:23:00 |

## What this shows and does not show
- **Repeatability:** each of the 5 postings received the same verdict in all 4 fresh conversations, so 0 of 5 postings varied. This shows repeatability **on these 5 postings,
  with this prompt and model, on this date**, and nothing more.
- **Repetition is not correctness.** #8 "Staff Network Security Architect" was judged `relevant` 4 of 4 times, and the approved label is **not fit** (Staff, 10+ years).
  The judge was consistently wrong on it under v1, which has no seniority criterion. The CONTRACT rule (the record) also marks it relevant.
- Four repeats per posting cannot reveal a rare disagreement. A verdict that flips 1 time in 10 could easily show 4 of 4 here.
- The citations' wording varied between calls. That was not analyzed beyond validation.
