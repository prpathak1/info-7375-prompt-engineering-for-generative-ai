"""Build the reject-audit sheet from out/decisions.jsonl (PLAN.md section 2). Offline. Held-out postings are never in it.

  python -I audit_sheet.py --seed 7375

Selection, in this order (no posting appears twice):
  1. RANDOM REJECTS: 30 drawn with random.Random(seed).sample from all rejects, sorted by (board, id).
  2. NEAR-THRESHOLD (target 5), from the rejects not drawn in 1. Categories defined before looking at the verdicts' correctness:
       a. S3 rejects whose smallest stated years equals the reject cut (5)
       b. K1 rejects (skills below the threshold of 2)
       c. T2a rejects (new rule; its boundary is the engineer-word exception)
       d. A1/A6 rejects decided by exactly one occurrence of one phrase
     All of a, b and c are taken. Seeded draws from d fill up to 5 (if a+b+c already reach 5, none from d).
  3. ACCEPTS: 5 drawn with the same generator, or all of them if fewer than 5 exist.
"""
import argparse
import datetime
import json
import random
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import filter as flt  # noqa: E402
import holdout  # noqa: E402
import postings  # noqa: E402


def phrase_hits(body: str) -> int:
    return sum(len(list(flt.ww(p).finditer(body))) for p in flt.A1_PHRASES + flt.A6_PHRASES)


def key_line(dec: dict, rec: dict = None) -> str:
    gate = dec["gate"] or ""
    claim = {"T": "title", "A": "authorization", "S": "seniority", "K": "skills"}.get(gate[:1])
    if dec["outcome"] == "accept":
        c = dec["claims"]["skills"]
        return f"skills: {', '.join(dec['skills_matched'])}"
    if claim:
        c = dec["claims"][claim]
        if c["quote"] and c["field"] == "body" and rec is not None:     # show the whole sentence, not just the phrase
            i = rec["body"].find(c["quote"])
            if i >= 0:
                return flt._sentence_around(rec["body"], i, i + len(c["quote"]))
        return c["quote"] or c["note"]
    return dec["reason"]


def cell(s, n=220) -> str:
    s = (s or "").replace("|", "/").replace("\n", " ")
    return s if len(s) <= n else s[:n].rstrip() + " ..."


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--decisions", default=str(HERE / "out" / "decisions.jsonl"))
    ap.add_argument("--out", default=str(HERE / "audit" / "AUDIT-SHEET.md"))
    a = ap.parse_args(argv)
    out = Path(a.out)
    if out.exists():
        print(f"[refused] {out} exists; the audit sample is drawn once.")
        return 2
    decs = [json.loads(l) for l in Path(a.decisions).read_text(encoding="utf-8").splitlines() if l.strip()]
    held = flt.holdout_ids()
    assert not any((d["board"], d["id"]) in held for d in decs), "held-out posting in decisions"
    recs = {(r["board"], r["id"]): r for r in postings.load_all()}
    key = lambda d: (d["board"], d["id"])
    rejects = sorted([d for d in decs if d["outcome"] == "reject"], key=key)
    accepts = sorted([d for d in decs if d["outcome"] == "accept"], key=key)
    rng = random.Random(a.seed)

    rand = rng.sample(rejects, 30)
    taken = {key(d) for d in rand}
    rest = [d for d in rejects if key(d) not in taken]
    cat_a = [d for d in rest if d["gate"] == "S3" and d["min_years"] == flt.YEARS_REJECT_MIN]
    cat_b = [d for d in rest if d["gate"] == "K1"]
    cat_c = [d for d in rest if d["gate"] == "T2a"]
    cat_d = [d for d in rest if d["gate"] in ("A1", "A6") and phrase_hits(recs[key(d)]["body"]) == 1]
    near = [("a", d) for d in cat_a] + [("b", d) for d in cat_b] + [("c", d) for d in cat_c]
    need = max(0, 5 - len(near))
    near += [("d", d) for d in rng.sample(cat_d, min(need, len(cat_d)))]
    acc = rng.sample(accepts, min(5, len(accepts)))

    now = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    gates = {}
    for d in decs:
        gates[d["gate"] or "accept"] = gates.get(d["gate"] or "accept", 0) + 1
    L = ["# AUDIT-SHEET: filter v0.1 decisions for Prathamesh to judge", "",
         f"- **Drawn:** {now} with `python -I audit_sheet.py --seed {a.seed}` from `out/decisions.jsonl` "
         f"(`python -I filter.py run`, FILTER v0.1, N1-N6).",
         f"- **Population:** {len(decs)} postings (the 30 held-out postings are excluded): {len(rejects)} rejects, {len(accepts)} accepts, "
         f"{sum(1 for d in decs if d['outcome']=='flag')} flags, {sum(1 for d in decs if d['outcome']=='abstain')} abstains.",
         f"- **Deciding rule counts:** {', '.join(f'{k} {v}' for k, v in sorted(gates.items(), key=lambda x: -x[1]))}.",
         f"- **Near-threshold pools** (after the random draw): a={len(cat_a)}, b={len(cat_b)}, c={len(cat_c)}, d={len(cat_d)}. "
         "The definitions are in the `audit_sheet.py` docstring.",
         f"- **Accepts:** {len(accepts)} exist, so {len(acc)} shown (target was 5).",
         "- **Key line** = the exact text the deciding rule quoted (or its note). **Context** = the first duty line found by the "
         "LABEL-SHEET line search, so you can judge a title-only reject.",
         "- **Fill in:** `agree` / `disagree` (with the filter's decision) and a short why. You can also reply with lines like `R07 disagree: ...`.", ""]

    def table(title, rows, prefix):
        L.extend([f"## {title}", "", "| # | Board | Title | Decided by | Key line | Context | agree / disagree | why |",
                  "|---|---|---|---|---|---|---|---|"])
        for i, (tag, d) in enumerate(rows, 1):
            r = recs[key(d)]
            duty = (holdout.key_lines(r["body"])["Main duties"] or [""])[0]
            by = f"{d['outcome']} {d['gate'] or ''}".strip() + (f" ({tag})" if tag else "") + f": {d['reason']}"
            L.append(f"| {prefix}{i:02d} | {d['board']} | {cell(d['title'], 90)} | {cell(by, 90)} | {cell(key_line(d, r), 300)} | "
                     f"{cell(duty, 160)} |  |  |")
        L.append("")

    table(f"1. Random rejects (30, seed {a.seed})", [("", d) for d in rand], "R")
    table("2. Near-threshold cases", near, "N")
    table("3. Accepts", [("", d) for d in acc], "A")
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text("\n".join(L), encoding="utf-8")
    (out.parent / "AUDIT-SAMPLE.json").write_text(json.dumps({
        "seed": a.seed, "created": now, "random_rejects": [key(d) for d in rand],
        "near_threshold": [(t, *key(d)) for t, d in near], "accepts": [key(d) for d in acc]}, indent=1), encoding="utf-8")
    print(f"[audit] seed={a.seed} random_rejects={len(rand)} near={len(near)} accepts={len(acc)} -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
