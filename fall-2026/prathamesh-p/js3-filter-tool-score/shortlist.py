"""Source-grounded shortlist (FILTER.md section 2). Offline. Reads out/decisions.all.v0.3.jsonl plus raw postings.

  python -I shortlist.py

For every accepted or flagged posting, each of the 4 claims gets supported / contradicted / insufficient with an
exact quote. Every quote is checked again as an exact substring of the posting field; a failure is printed, never hidden.
Skills: one quoted sentence per matched term. Location is shown but is not a FILTER claim (no v0.1 or v0.2 rule covers it).
"""
import datetime
import json
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import filter as flt  # noqa: E402
import postings  # noqa: E402

DEC = HERE / "out" / "decisions.all.v0.3.jsonl"
OUT = HERE / "SHORTLIST.md"
CLAIM_TEXT = {"title": "The job is network engineering work (SOC 15-1241)",
              "authorization": "Nothing in the posting excludes an F-1 holder who needs sponsorship",
              "seniority": "The level fits an entry-level candidate",
              "skills": "The work uses at least 2 of the persona's networking skills"}


def main() -> int:
    recs = {(r["board"], r["id"]): r for r in postings.load_all()}
    resume = json.loads((HERE / "fixtures" / "resume.fictional.json").read_text(encoding="utf-8"))
    decs = [json.loads(l) for l in DEC.read_text(encoding="utf-8").splitlines() if l.strip()]
    keep = [d for d in decs if d["outcome"] in ("accept", "flag")]
    pairs = flt.rank([(recs[(d["board"], d["id"])], d) for d in keep if d["outcome"] == "accept"])
    flagged = [(recs[(d["board"], d["id"])], d) for d in keep if d["outcome"] == "flag"]
    now = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")
    L = ["# SHORTLIST: FILTER v0.3, every claim labelled against the posting text", "",
         f"- **Generated:** {now} by `python -I shortlist.py` from `out/decisions.all.v0.3.jsonl`. That file came from "
         "`python -I filter.py run --include-holdout --labels holdout/LABELS.json --out out/decisions.all.v0.3.jsonl`.",
         f"- **Population:** {len(decs)} postings. **{len(pairs)} accepted, {len(flagged)} flagged.** Ranked by FILTER R1.",
         "- **Labels:** `supported` = a quoted sentence asserts the claim. `contradicted` = a quote asserts the opposite. "
         "`insufficient` = no quote either way, or a match without meaning.",
         "- Every quote below was checked again as an exact substring of the stored posting (the result is printed per posting).",
         "- **This is the filter's evidence, not a decision.** Whether a posting is worth the persona's time stays Prathamesh's call.", ""]
    errors = 0
    for rank_, (r, d) in enumerate(pairs + flagged, 1):
        errs = flt.verify_quotes(d, r)
        rows = []
        for name in ("title", "authorization", "seniority", "skills"):
            c = d["claims"][name]
            if name == "skills" and d["skills_matched"]:
                text = r["body"]
                for k2 in flt.K2_REMOVE:
                    text = k2.sub(" ", text)
                sents = []
                for term in d["skills_matched"]:
                    m = flt.ww(term).search(r["body"])
                    s = flt._sentence_around(r["body"], m.start(), m.end()) if m else None
                    if s is None or s not in r["body"]:
                        errs.append(f"skills: no sentence found again for {term}")
                    sents.append(f"**{term}**: \"{s}\"")
                quote = "<br>".join(sents)
            else:
                quote = f"\"{c['quote']}\"" if c["quote"] else "(none)"
                if c["quote"] and c["field"] == "body" and c["label"] != "contradicted":
                    i = r["body"].find(c["quote"])
                    if i >= 0 and len(c["quote"]) < 40:
                        quote = f"\"{flt._sentence_around(r['body'], i, i + len(c['quote']))}\""
            rows.append(f"| {name} | {CLAIM_TEXT[name]} | **{c['label']}** | {quote.replace('|', '/')} | {c['note']} |")
        errors += len(errs)
        L += [f"## {rank_}. {r['title'].strip()} ({r['board']}, {d['outcome']})", "",
              f"- **ID:** `{r['id']}`. **Location (shown, not a claim):** {r['location'] or '(not given)'}. **URL:** {r['url']}",
              f"- **Quote check:** {'all quotes found again' if not errs else '; '.join(errs)}", "",
              "| Claim | What is claimed | Label | Evidence (exact text) | Rule note |", "|---|---|---|---|---|", *rows, ""]
    OUT.write_text("\n".join(L), encoding="utf-8")
    print(f"[shortlist] accepted={len(pairs)} flagged={len(flagged)} quote_errors={errors} -> {OUT}")
    return 1 if errors else 0


if __name__ == "__main__":
    sys.exit(main())
