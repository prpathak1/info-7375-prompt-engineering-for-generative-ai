# JS3 plan (lean). Drafted by Claude Code (Opus 5.5) on 2026-11-25, about 18:43 EST. **APPROVED by Prathamesh, 2026-11-25 18:46:08 EST**, including the Filesystem MCP server (version pinned) as the third-party server.

Nothing in this file has run yet. Everything below is future tense.

## Data in scope

- **Collected so far:** 7 board captures, about 1,992 unique postings after merging duplicate captures.
  - Zoox (Lever): 227 on 2026-10-30 and 234 on 2026-11-10.
  - Cloudflare (Greenhouse): 466 on 2026-11-10.
  - OpenAI (Ashby): 826 on 2026-11-10.
  - Fastly (Greenhouse): 50 on 2026-11-25.
  - Datadog (Greenhouse): 392 on 2026-11-25.
- **Titles with "network":** 43. None has an entry-level word. The nearest fits are 2 OpenAI "Network Engineer" postings (San Francisco, London) that state no years requirement.

## 1. Held-out labels (build these first, before any filter output exists)

- `holdout.py --seed 20261125` will pick a stratified sample:
  - 20 of the 43 network-titled postings (because the real fits are rare), and
  - 10 random other postings.
- The seed and the selected IDs will be written to `holdout/HOLDOUT.json`.
- Prathamesh labels each one `fit` / `not_fit` / `unsure` **blind**. He sees the title and body only, never a filter verdict.
- **Never used for tuning.** The remaining 23 network titles and the rejects go to the audit.

## 2. Filter and reject audit

- `filter.py` will implement the approved FILTER.md, with tests W1–W5 plus unit tests per rule. It runs over all postings and writes `out/decisions.jsonl` (verdict, gate, quoted evidence).
- `audit_sheet.py --seed 7375` will produce `audit/AUDIT-SHEET.md`, a single table with one row per posting:
  - **Columns:** ID, board, title, the filter's reason, one quoted body line, and a blank `My verdict (ok / wrong / unsure)` column.
  - **Rows:** 30 random rejects (seeded), the about 5 nearest-threshold cases (skills = 1, years = 3–4, `flag`), and 5 random accepts.
- Claude will then tabulate the mistakes and write `audit/AUDIT.md`. It will include:
  - the observed error count with its n (no claim about the rate across all postings),
  - the false friend (candidates already seen: "Manager I", "Champion Network", "Road Network Tools"),
  - every rule added, removed or rejected, as FILTER v0.2.

## 3. Grounded shortlist

- `shortlist.py` will label 4 claims per accepted posting: `supported` / `contradicted` / `insufficient`, each with an exact quote that is checked again against the raw text.
- **Lexical ≠ entailment demo:** "security clearance not required" matches A1 in words only. It will show up in a real posting if one exists, otherwise in a labelled synthetic fixture.
- **Abstention counterexample:** OpenAI "Network Engineer" (FILTER §2.4).

## 4. Tool server (Chapter 8)

- **Proposed capability:** `score_posting`. It will be **read-only**. Input: `{board, posting_id}`. Output: the filter verdict plus the 4 evidence labels, computed from stored raw files only.
  - No network access, no writes. The server will reuse `policy.py` with a read-only root.
- **Build:** `mcp_server.py` will be written from scratch in Python's standard library and speak newline-delimited JSON-RPC 2.0 over stdio (`initialize`, `tools/list`, `tools/call`).
- **Transcripts:**
  - A real client session: Claude Code, with the server registered for the folder only. The full transcript will be logged by the server itself to `transcripts/`.
  - A tiny scripted client, as a second client.
- **Evaluation:** declared behavior vs. actual behavior. Probes: unknown tool, bad arguments, a path-traversal `posting_id`, an oversized request. Plus what a compatible client is *not* entitled to (for example, any write, any URL), and a trust decision.
- **Third-party server to evaluate the same way:** the reference **Filesystem MCP server** (`@modelcontextprotocol/server-filesystem`, pinned version), run against a scratch directory.
  - It declares directory-scoped read and write. The probes will test `..`, symlinks, and writes outside the allowed directory.
  - It needs Node/npx; check with `node -v`. Fallback if Node is missing: the reference **Time** server (`mcp-server-time`, Python). It is lower risk and less interesting.

## 5. What moves the score (Chapter 9)

- **Inventory:**
  - `SKILL_THRESHOLD=2` (inherited from JS1, hand-set),
  - the S3 years cut points 2 and 5 (new, hand-set),
  - the A3 5-word negation window (hand-set),
  - the 200-character abstain floor (hand-set),
  - the GATE budgets 4/6/120 (inherited from JS2),
  - `prompts/judge_v1.md` and `prompts/judge_v2.md` (inherited; not called in JS3 unless decided).
  - Nothing is fitted from labels.
- **Comparisons:**
  - Baseline = the JS2 rule (T + A + K only) on the held-out set.
  - Then **one change at a time:** (a) + the seniority gate S1–S5; (b) + the negation guard A3; (c) K1 threshold 2 → 3 (setting).
  - Each one reports precision, recall and the confusion counts on the held-out labels.
  - With about 2–4 true fits in 30, the numbers are tiny-n and will be reported as counts, not rates.
- **Persistence note:** the same output across sessions comes from stored files and fixed rules, not from any model training.

## 6. Sign-off

- `SIGNOFF.md`:
  - the checked properties and named tests,
  - the checking method,
  - at least 3 genuine unchecked items,
  - claims not made,
  - signed or withheld (Prathamesh).
- A driver's-seat table.
- README with the exact commands and the actual runs.
