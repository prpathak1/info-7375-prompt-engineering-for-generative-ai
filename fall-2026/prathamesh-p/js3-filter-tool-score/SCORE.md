# What moves the score: inventory and the one-change-at-a-time test

- **Drafted by:** Claude Code (Opus 5.5), 2026-11-25 about 19:19 EST.
- **Numbers:** from `python -I score_test.py`: first run 2026-11-25 19:18:42 EST (C0–C6); re-run 19:27:52 EST with C7 (v0.2 → v0.3) added. C0–C6 were unchanged in the re-run.
- **Default filter:** now FILTER **v0.3**. Full tables are in `SCORE-RESULTS.md`, raw results in `out/score_results.json`.

> **Provenance of the labels: read this first.** The 30 held-out labels (`holdout/LABELS.json`) were **drafted by Claude (claude.ai chat)** at Prathamesh's request, from the sheet text Claude Code printed. He reviewed and approved every one. They were made blind to any filter output on the held-out set.
>
> The filter's rules were also drafted by Claude (Claude Code), so **this score test is partly Claude judging Claude**. Agreement between filter and labels can come from a shared reading, not from the filter being right. A blind spot common to both would not show up here.

## 1. Inventory: every number, threshold and prompt

| Object | Value | Where | Source |
|---|---|---|---|
| K1 skill threshold | 2 | `filter.SKILL_THRESHOLD` | **inherited** (JS1 CONTRACT); hand-set there, never fitted |
| Abstain body floor | 200 characters | `filter.ABSTAIN_MIN_BODY` | **hand-set** (FILTER 2.4, v0.1) |
| A3 negation window | 5 words | `filter.NEGATION_WINDOW` | **hand-set** (FILTER A3) |
| S3 "experience" window | 6 words | `filter.YEARS_EXPERIENCE_WINDOW` | **hand-set** (FILTER S3) |
| S3 cut points | ≤2 fit, 3–4 flag, ≥5 reject | `filter.YEARS_FIT_MAX`, `YEARS_REJECT_MIN` | **hand-set** (FILTER S3) |
| R1 ranking | seniority tier, then skill count, then date | `filter.rank` | **hand-set** (FILTER R1); no numeric weights |
| Phrase lists (T, A, S, K) | see FILTER.md | `filter.py` | **inherited** (JS1: T1–T5, A1, A2, K1) or **hand-set** (JS3); the v0.2 changes were set **after the audit** (not from held-out labels) |
| Held-out sample | 20 network + 10 other, seed 20261125 | `holdout.py` | **hand-set** design |
| Audit sample | 30 random + about 5 near-threshold + up to 5 accepts, seed 7375 | `audit_sheet.py` | **hand-set** design |
| Label-sheet display | 3 lines, 240 characters | `holdout.py` | **hand-set**; it changes what a labeller sees, not any verdict |
| Tool server limits | 64 KiB per message, 64-character id and board | `mcp_server.py` | **hand-set** |
| Collector budgets | 4 boards, 6 requests, 120 s, 30 s timeout, 2 s retry delay, Retry-After cap 10 s | `loop.py` | **inherited** (JS2 GATE) |
| Claude prompt: judge | `prompts/judge_v1.md` (sha256 f55c7c68…), `judge_v2.md` (99ff0126…) | `prompts/` | **inherited** (JS2). **Not called in JS3**; no JS3 number depends on them |
| Claude prompt: real-client request | the `claude -p` text in `transcripts/claude-client-20261125T191455.jsonl` | Chapter 8 | **hand-set** (written by Claude Code). It changes no score |
| Claude prompts: label and verdict drafts | claude.ai chat, by Prathamesh | not in this folder | the conversation is not recorded here; only its output (approved labels and verdicts) is |

**Fitted from labels: nothing.** No number in this folder was fitted or tuned on the held-out labels, or on any labels.

## 2. The test

- **Data:** the 30 held-out postings. Labels: 1 `fit` (H03), 28 `not_fit`, 1 `unsure` (H02, left out of the counts).
- **Positive class:** `fit`.
- **Two readings of the filter's output:** "accepted" (outcome accept) and "reaches me" (accept or flag).
- **Rule of the test:** each run changes **one object** relative to the run named in "vs".

| Run | One change | Object | vs | Accepted TP/FP/FN/TN | Reaches me TP/FP/FN/TN |
|---|---|---|---|---|---|
| C0 | JS2 baseline (inherited rules only) | – | – | 1/1/0/27 | 1/3/0/25 |
| C1 | + seniority gate S1–S5 | filter rule | C0 | 1/1/0/27 | **1/1/0/27** |
| C2 | + negation guard A3 | filter rule | C0 | 1/1/0/27 | 1/3/0/25 |
| C3 | + title false friends T2a | filter rule | C0 | 1/1/0/27 | 1/3/0/25 |
| C4 | FILTER v0.1 | filter version | C0 | 1/1/0/27 | 1/1/0/27 |
| C5 | v0.1 → v0.2 | filter version | C4 | 1/1/0/27 | 1/1/0/27 |
| C6 | K1 threshold 2 → 3 | setting | C5 | **1/0/0/28** | **1/0/0/28** |
| C7 | v0.2 → v0.3 (A2 export-license sentence → A7 flag) | filter version | C5 | 1/1/0/27 | 1/3/0/25 |

**What the counts show:**
- **Seniority (C1) is the only rule change that moved "reaches me".** H19 "Senior SRE - Networks" and H26 "Datacenter Networking Technician" (7+ years) were flags under the JS2 rule. Seniority rejects them, which matches the labels (not_fit). That is 2 fewer postings for a human to read, and the one `fit` is kept.
- **A3 (C2) and T2a (C3) changed no outcome.**
  - A3 changed no outcome on these 30. Whether it fired at all wasn't separately checked.
  - T2a only changed **which rule** rejected H07 and H27: they were already rejected by A1 and K1.
- **v0.1 → v0.2 (C5) changed no outcome on the held-out set either.** 9 postings moved from A1 to A2, the same export-license sentence as in GROUNDING.md.
- **The threshold change (C6) removed the last false positive, for the wrong reason.**
  - H08 (London) has 2 skills (routing, switching); H03 has 7.
  - Prathamesh labelled H08 `not_fit` because it is a **UK role**, not for its skills.
  - Raising the threshold "fixes" the count by accident. It would also drop any real entry-level fit that lists only two of the persona's skills.
  - Adopting C6 because it scores best here would be **tuning on the held-out labels**. **Not adopted.** The location gap is recorded in GROUNDING.md 3(b).

- **v0.2 → v0.3 (C7) made the filter send more to a human, and on this sample those extra postings are not fits.**
  - Accepts are unchanged (H03, H08).
  - "Reaches me" rose from 2 to 4: H06 "Data Center Network Operations Engineer" (flags S3 for 4 years, plus A7) and H15 "Software Engineer, Network Performance & Reliability (Argo)" (flags T4 and A7) now flag. Prathamesh labelled both not_fit ("minimum 4 years required"; "software role ... (15-1252)").
  - The other 7 Cloudflare held-out postings moved from A2 to a later reject (S1 ×5, S3 ×1, K1 ×1 for H02, labelled unsure).
  - This is the expected price of v0.3: the export-license sentence no longer decides anything, so the next rule or a human does.
  - v0.3 was decided from the **non-held-out** measurement (`demo/06`, `demo/08`), not from these labels.

**Limits:**
- With **one** positive label, recall is 0/1 or 1/1. None of the runs lost H03, so no run can be told apart on recall.
- Differences of 1–2 postings in 30 are anecdotes, not rates.
- The labels were partly drafted by the same model family that drafted the rules (see the box above).

**Objects not varied:**
- **Prompt:** the filter calls no Claude prompt.
- **Context and tool list:** no model is in the scoring loop.
- So "prompt", "context" and "tool list" changes have no effect on these numbers by construction. They would matter only if the JS2 Claude judge were re-enabled, which it is not.

## 3. Persistent behavior is not training

- The filter gives the same answers in every session (and the MCP tool gives Claude the same answers) because the **rules are code and the postings are files**. Re-running reads the same `filter.py` and `raw/` and gets the same output; `cmp` showed the default config reproduces the v0.2 decisions byte for byte.
- Nothing about Claude changed:
  - no weights were updated;
  - no example was learned;
  - the Claude Code client in `transcripts/` had to call the tool to know the answer.
- If Claude "remembered" a verdict in a later session, the cause would be context: a file it read, a memory note, or a pasted transcript. That would show the context, not that the model was trained.
