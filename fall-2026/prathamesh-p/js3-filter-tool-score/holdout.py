"""Build the held-out label sample (PLAN.md section 1). Offline. It shows NO filter output.

  python -I holdout.py --seed 20261125

Selection:
- stratum A: 20 of the postings whose title has whole-word network/networks/networking
- stratum B: 10 of all other postings
Each stratum is drawn with random.Random(seed).sample over a list sorted by (board, id). The 30 are then shuffled
with the same generator, so the network titles aren't grouped together. The title regex is the only rule shared
with the filter. It decides the stratum, not a verdict.

Writes holdout/HOLDOUT.json (seed + ids) and LABEL-SHEET.md. It refuses to overwrite either file, so the sample
can't be silently redrawn.
"""
import argparse
import datetime
import json
import random
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import postings  # noqa: E402

TITLE_NETWORK = re.compile(r"\bnetwork(s|ing)?\b", re.I)

# Line finders for the sheet. They pick which lines to SHOW. They never decide anything.
FINDERS = {
    "Years / level words": re.compile(r"\b\d+\s*(\+|plus)?\s*(-|to|–)?\s*\d*\s*\+?\s*years?\b|\b(entry[- ]level|new grad|early career|junior)\b", re.I),
    "Authorization / sponsorship": re.compile(r"\bauthoriz|sponsor|citizen|visa\b|green card|permanent resident|U\.S\. person|export|ITAR", re.I),
    "Clearance": re.compile(r"clearance", re.I),
}
DUTY_HEAD = re.compile(r"(responsibilit|what you('ll| will) do|you will:|in this role|about the role|the role|what you'll be doing|day to day|what you'll work on)", re.I)
DUTY_STRONG = re.compile(r"(responsibilit|what you('ll| will) do|you will:|in this role, you will|what you'll be doing)", re.I)
MAX_LINES, MAX_CHARS = 3, 240


def sentences(body: str) -> list[str]:
    out = []
    for ln in body.splitlines():
        out.extend(s.strip() for s in re.split(r"(?<=[a-z0-9)][.!?])\s+(?=[A-Z])", ln) if s.strip())
    return out


def clip(s: str) -> str:
    s = s.replace("|", "/")
    return s if len(s) <= MAX_CHARS else s[:MAX_CHARS].rstrip() + " ..."


def key_lines(body: str) -> dict:
    sents = sentences(body)
    out = {}
    for name, rx in FINDERS.items():
        hits = []
        for s in sents:
            if rx.search(s) and clip(s) not in hits:
                hits.append(clip(s))
        out[name] = hits[:MAX_LINES]
    lines = [ln.strip() for ln in body.splitlines() if ln.strip()]
    duties = []
    for head in (DUTY_STRONG, DUTY_HEAD):     # prefer a "responsibilities / you will" heading over "about the role"
        for i, ln in enumerate(lines):
            if head.search(ln) and len(ln) < 80:
                body_lines = [x for x in lines[i + 1:] if len(x) >= 40 and not x.endswith(":")]
                duties = [clip(x) for x in body_lines[:MAX_LINES]]
                break
        if duties:
            break
    if not duties:
        duties = [clip(body.replace("\n", " ")[:MAX_CHARS])] if body else []
    out["Main duties"] = duties
    return out


def build(seed: int, n_network: int = 20, n_other: int = 10):
    allp = postings.load_all()
    net = [p for p in allp if TITLE_NETWORK.search(p["title"] or "")]
    other = [p for p in allp if not TITLE_NETWORK.search(p["title"] or "")]
    rng = random.Random(seed)
    pick = [("A", p) for p in rng.sample(net, n_network)] + [("B", p) for p in rng.sample(other, n_other)]
    rng.shuffle(pick)
    return allp, net, other, pick


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--seed", type=int, required=True)
    ap.add_argument("--out-json", default=str(HERE / "holdout" / "HOLDOUT.json"))
    ap.add_argument("--out-sheet", default=str(HERE / "LABEL-SHEET.md"))
    a = ap.parse_args(argv)
    oj, osh = Path(a.out_json), Path(a.out_sheet)
    for f in (oj, osh):
        if f.exists():
            print(f"[refused] {f} exists; the held-out sample is drawn once. Delete it by hand only with Prathamesh's approval.")
            return 2
    allp, net, other, pick = build(a.seed)
    now = datetime.datetime.now().astimezone().strftime("%Y-%m-%d %H:%M:%S %Z")

    rows = []
    for i, (stratum, p) in enumerate(pick, 1):
        rows.append({"hid": f"H{i:02d}", "stratum": stratum, "board": p["board"], "platform": p["platform"],
                     "id": p["id"], "title": p["title"], "captured": p["captured"]})
    oj.parent.mkdir(parents=True, exist_ok=True)
    oj.write_text(json.dumps({
        "seed": a.seed, "created": now, "command": f"python -I holdout.py --seed {a.seed}",
        "population": {"unique_postings": len(allp), "network_titles": len(net), "other": len(other)},
        "strata": {"A": "title has whole-word network/networks/networking; 20 drawn", "B": "all others; 10 drawn"},
        "rule": "Held-out: never used to tune any rule, weight or prompt. Labels by Prathamesh, blind to filter output.",
        "postings": rows}, indent=2) + "\n", encoding="utf-8")

    L = [f"# LABEL-SHEET: held-out sample (30 postings)", "",
         f"- **Drawn:** {now} with `python -I holdout.py --seed {a.seed}`. The IDs are in `holdout/HOLDOUT.json`.",
         f"- **Population:** {len(allp)} unique postings. {len(net)} have a network title (20 drawn); {len(other)} others (10 drawn). The order is shuffled.",
         "- **No filter output is on this sheet.** The lines below were picked by plain text search (years, authorization, clearance, duties) only to save reading time.",
         "  A section with no lines means the search found nothing. It does **not** mean the posting is silent: open the URL when it matters.",
         "- **Label for the fictional persona** (F-1 MS networking student who needs sponsorship, entry level, target: network engineering). Is it worth her time?",
         "- **Fill in:** `fit` / `not_fit` / `unsure`, plus a short reason. You can fill in the table, or reply with lines like `H01 not_fit: 8+ years`.", "",
         "| HID | Title | Board | fit / not_fit / unsure | reason |", "|---|---|---|---|---|"]
    for r in rows:
        L.append(f"| {r['hid']} | {clip(r['title'] or '')} | {r['board']} |  |  |")
    L.append("")
    for (stratum, p), r in zip(pick, rows):
        kl = key_lines(p["body"])
        L += [f"## {r['hid']}: {p['title']}", "",
              f"- **Board:** {p['board']} ({p['platform']}), captured {p['captured']}.  **Location:** {p['location'] or '(not given)'}",
              f"- **URL:** {p['url'] or '(not given)'}"]
        for name in ("Years / level words", "Authorization / sponsorship", "Clearance", "Main duties"):
            L.append(f"- **{name}:**" + ("" if kl[name] else " (no line found by search)"))
            L += [f"  - \"{s}\"" for s in kl[name]]
        L += ["", f"**{r['hid']} fit / not_fit / unsure:** ______  **reason:** ______", ""]
    osh.write_text("\n".join(L), encoding="utf-8")
    print(f"[holdout] seed={a.seed} wrote {oj} and {osh}: {len(rows)} postings "
          f"(A={sum(1 for r in rows if r['stratum']=='A')}, B={sum(1 for r in rows if r['stratum']=='B')})")
    return 0


if __name__ == "__main__":
    sys.exit(main())
