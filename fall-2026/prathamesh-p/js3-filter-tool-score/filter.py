"""JS3 filter: FILTER.md v0.3 (v0.1 approved 2026-11-25 18:46:08 EST; v0.2 and v0.3 changes decided by Prathamesh after measurement, 2026-11-25). Standard library only.

Gate order, as FILTER.md section 0 lists it, plus the interpretations in IMPLEMENTATION NOTES below:
  missing title -> abstain
  Gate 1 title (T1, T2, T2a reject; T3a, T4, T5 add a flag)
  body under 200 characters -> abstain
  Gate 2 authorization (A1/A6 reject unless every hit is negated -> A3 flag; A2 reject; A4/A5 label only)
  Gate 3 seniority (S1 reject; S3 reject / flag / supported; S2, S5 supported; S4 insufficient)
  Gate 4 skills (K1 with K2 exclusions, K3 networking only)
  abstain rule 2, then flag if any flag was raised, else accept.

IMPLEMENTATION NOTES (readings of v0.1 wording the code had to pick). N1-N6 ACCEPTED as written by Prathamesh, 2026-11-25 19:01:45 EST:
  N1 A flag does not stop the gates: a later reject still rejects. The outcome is flag only if nothing rejects.
  N2 T3a applies only when no T3 role word is present ('Network Operations Engineer' -> T3, accept).
  N3 A3 counts a negator (no / not / without) within 5 words on either side of the A1 or A6 phrase.
  N4 S3: 'experience' within 6 words on either side of the years phrase.
  N5 Title rejects (Gate 1) can decide on a missing or short body; every other gate needs the body.
  N6 No v0.1 rule says when authorization is 'supported', so the filter never labels it supported.

  python -I filter.py run [--include-holdout --labels holdout/LABELS.json]
"""
import argparse
import datetime
import json
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import postings  # noqa: E402

HOLDOUT_JSON = HERE / "holdout" / "HOLDOUT.json"
SKILL_THRESHOLD = 2          # K1, inherited from JS1, hand-set
ABSTAIN_MIN_BODY = 200       # section 2.4, hand-set
NEGATION_WINDOW = 5          # A3, hand-set
YEARS_EXPERIENCE_WINDOW = 6  # S3, hand-set
YEARS_FIT_MAX, YEARS_REJECT_MIN = 2, 5   # S3 cut points, hand-set


# Switches for the one-change-at-a-time score test (score_test.py). V03 is the default and is FILTER v0.3 exactly.
# JS2_BASELINE keeps only the inherited JS1/JS2 rules: T1-T5 (T3a folds into T5), A1-A2 with JS1 EAR, K1 with no K2.
V03 = {"t2a": True, "t3a": True, "a3_negation": True, "a6": True, "a7_may_access": True, "ear_strict": True,
       "a2_export_license": True, "seniority": True, "k2": True, "abstain_rule2": True, "skill_threshold": SKILL_THRESHOLD}
V02 = {**V03, "a2_export_license": False}
V01 = {**V02, "a7_may_access": False, "ear_strict": False}
JS2_BASELINE = {k: False for k in V03} | {"skill_threshold": SKILL_THRESHOLD}


class HoldoutLocked(Exception):
    """The held-out postings were requested before Prathamesh's labels exist."""


def ww(term: str, plural: bool = True) -> re.Pattern:
    """Whole word, case-insensitive, optional plural s (same rule as JS1 jobwatch.whole_word)."""
    return re.compile(r"(?<!\w)" + re.escape(term) + (r"s?" if plural else "") + r"(?!\w)", re.I)


# ---------------------------------------------------------------- Gate 1
T1 = re.compile(r"\bnetwork(s|ing)?\b", re.I)
T2 = re.compile(r"\b(road|social|neural|sales|partner|retail|distribution)\s+network", re.I)
T2A_ALWAYS = re.compile(r"\bchampion\s+network|\bnetwork-on-chip\b|\bNoC\b", re.I)
T2A_STRATEGY = re.compile(r"\bnetwork\s+strategy\b", re.I)
ENGINEER_WORD = re.compile(r"\bengineer(s|ing)?\b", re.I)
T3 = re.compile(r"\b(engineer|engineering|architect|administrator|admin|security|infrastructure)\b", re.I)
T3A = re.compile(r"\b(technician|operations)\b", re.I)
T4 = re.compile(r"\bsoftware\b", re.I)

# ---------------------------------------------------------------- Gate 2
A1_PHRASES = ["U.S. citizen", "US citizen", "U.S. citizenship", "U.S. person", "security clearance", "active clearance",
              "ITAR", "EAR", "export control"]
A6_PHRASES = ["green card", "permanent resident", "U.S. persons only"]
A2_PHRASES = ["without sponsorship", "without visa sponsorship", "no sponsorship", "not sponsor", "will not sponsor",
              "unable to sponsor", "cannot sponsor", "does not sponsor"]
A4 = re.compile(r"\bauthori[sz]ed to work\b", re.I)
EAR_EXACT = re.compile(r"(?<!\w)EAR(?!\w)")          # v0.2 change 1: exact uppercase, no plural ('ears' matched in v0.1)
A7_MAY_ACCESS = re.compile(r"\bmay require access\b", re.I)   # v0.2 change 2
A2_EXPORT_LICENSE = re.compile(r"\s+for\s+an\s+export\s+license\b", re.I)   # v0.3: must directly continue the A2 match


def _phrase_re(p: str) -> re.Pattern:
    return EAR_EXACT if p == "EAR" else ww(p)
NEGATOR = re.compile(r"(?<!\w)(no|not|without)(?!\w)", re.I)

# ---------------------------------------------------------------- Gate 3
S1 = re.compile(r"(?<!\w)(senior|sr\.|staff|principal|lead|manager|director|head of|vp)(?!\w)", re.I)
S2 = re.compile(r"\b(?i:engineer|technician|administrator)\s+(I|II|1)\b")   # word any case; numeral exact ('i' is not a level)
S3_PATTERNS = [re.compile(r"(?<!\w)(\d{1,2})\s*\+\s*years?(?!\w)", re.I),
               re.compile(r"(?<!\w)(\d{1,2})\s+or\s+more\s+years?(?!\w)", re.I),
               re.compile(r"\bminimum\s+of\s+(\d{1,2})\s+years?(?!\w)", re.I)]
S5 = re.compile(r"(?<!\w)(new grad|entry[- ]level|early career|junior|associate|0\s*-\s*2 years)(?!\w)", re.I)

# ---------------------------------------------------------------- Gate 4
K2_REMOVE = [re.compile(r"https?://\S+", re.I), re.compile(r"\bcontext\s+switching\b", re.I),
             re.compile(r"\b(call|ticket|request)\s+routing\b", re.I)]


def _claim(label, quote=None, field=None, note=""):
    return {"label": label, "quote": quote, "field": field, "note": note}


def _words_between(text: str, a: int, b: int) -> int:
    return len(re.findall(r"\S+", text[a:b]))


def _negated(body: str, m: re.Match) -> bool:
    for n in NEGATOR.finditer(body):
        if n.end() <= m.start() and _words_between(body, n.end(), m.start()) <= NEGATION_WINDOW:
            return True
        if n.start() >= m.end() and _words_between(body, m.end(), n.start()) <= NEGATION_WINDOW:
            return True
    return False


_SENT_END = re.compile(r"\n|(?<=[a-z0-9)\]])[.!?;](?=\s|$)")   # a period after a capital (U.S., Sr.) does not end a sentence


def _sentence_around(text: str, start: int, end: int) -> str:
    """The sentence (or line) holding [start, end), as an exact substring of text."""
    left = 0
    for m in _SENT_END.finditer(text, 0, start):
        left = m.end()
    m = _SENT_END.search(text, end)
    right = m.end() if m else len(text)
    return text[left:right].strip()


def gate1(title: str, cfg: dict = V03):
    """-> (reject_gate or None, flags, title_claim)."""
    if not T1.search(title):
        return "T1", [], _claim("insufficient", None, "title", "no whole-word network in title")
    m = T2.search(title)
    if m:
        return "T2", [], _claim("contradicted", m.group(0), "title", "false friend")
    m = (T2A_ALWAYS.search(title) or (T2A_STRATEGY.search(title) if not ENGINEER_WORD.search(title) else None)) if cfg["t2a"] else None
    if m:
        return "T2a", [], _claim("contradicted", m.group(0), "title", "false friend")
    flags = []
    if T4.search(title):
        flags.append("T4")
    if T3.search(title):
        label = "insufficient" if flags else "supported"
        return None, flags, _claim(label, title, "title", "network role title" + ("; software title, human decides" if flags else ""))
    if cfg["t3a"] and T3A.search(title):
        return None, flags + ["T3a"], _claim("insufficient", title, "title", "technician/operations title, human decides")
    return None, flags + ["T5"], _claim("insufficient", title, "title", "network but no role word, human decides")


def gate2(body: str, cfg: dict = V03):
    """-> (reject_gate or None, flags, authorization_claim)."""
    guarded = None
    may_access = None
    groups = (("A1", A1_PHRASES), ("A6", A6_PHRASES)) if cfg["a6"] else (("A1", A1_PHRASES),)
    for gate, phrases in groups:
        for p in phrases:
            rx = _phrase_re(p) if cfg["ear_strict"] else ww(p)
            for m in rx.finditer(body):
                if cfg["a3_negation"] and _negated(body, m):
                    guarded = guarded or m
                elif (cfg["a7_may_access"] and p == "export control"
                      and A7_MAY_ACCESS.search(_sentence_around(body, m.start(), m.end()))):
                    may_access = may_access or m          # v0.2 change 2: ambiguous access sentence -> flag
                else:
                    return gate, [], _claim("contradicted", m.group(0), "body", f"{gate}: '{p}'")
    for p in A2_PHRASES:
        for m in ww(p).finditer(body):
            if (cfg["a2_export_license"] and p == "without sponsorship"
                    and A2_EXPORT_LICENSE.match(body, m.end())):
                may_access = may_access or m              # v0.3: export-license sponsorship, not visa -> A7 flag
                continue
            return "A2", [], _claim("contradicted", m.group(0), "body", f"A2 sponsorship refusal: '{p}'")
    if guarded or may_access:
        flags, first = [], None
        if guarded:
            flags.append("A3")
            first = guarded
        if may_access:
            flags.append("A7")
            first = first or may_access
        note = "; ".join(n for f_, n in (("A3", "A3: exclusion phrase appears negated"),
                                          ("A7", "A7: export-control access or export-license sentence, sponsorship unknown"))
                         if f_ in flags) + "; human decides"
        return None, flags, _claim("insufficient", _sentence_around(body, first.start(), first.end()), "body", note)
    m = A4.search(body)
    if m:
        return None, [], _claim("insufficient", _sentence_around(body, m.start(), m.end()), "body",
                                "A4: authorization stated, sponsorship unknown")
    return None, [], _claim("insufficient", None, None, "A5: posting is silent on authorization and sponsorship")


def min_years(body: str):
    """-> (smallest N with 'experience' nearby, its sentence) or (None, None)."""
    best = None
    exp = [m for m in re.finditer(r"(?<!\w)experience(?!\w)", body, re.I)]
    for pat in S3_PATTERNS:
        for m in pat.finditer(body):
            near = any((e.start() >= m.end() and _words_between(body, m.end(), e.start()) <= YEARS_EXPERIENCE_WINDOW) or
                       (e.end() <= m.start() and _words_between(body, e.end(), m.start()) <= YEARS_EXPERIENCE_WINDOW)
                       for e in exp)
            if near:
                n = int(m.group(1))
                if best is None or n < best[0]:
                    best = (n, _sentence_around(body, m.start(), m.end()))
    return best or (None, None)


def gate3(title: str, body: str):
    """-> (reject_gate or None, flags, seniority_claim, min_years)."""
    m = S1.search(title)
    if m:
        return "S1", [], _claim("contradicted", m.group(0), "title", f"S1: level word '{m.group(0)}' in title"), None
    n, sent = min_years(body)
    if n is not None:
        if n >= YEARS_REJECT_MIN:
            return "S3", [], _claim("contradicted", sent, "body", f"S3: smallest stated requirement {n} years"), n
        if n > YEARS_FIT_MAX:
            return None, ["S3"], _claim("insufficient", sent, "body", f"S3: {n} years is near the threshold, human decides"), n
        return None, [], _claim("supported", sent, "body", f"S3: smallest stated requirement {n} years"), n
    m = S2.search(title)
    if m:
        return None, [], _claim("supported", m.group(0), "title", "S2: entry level numeral"), None
    for field, text in (("title", title), ("body", body)):
        m = S5.search(text)
        if m:
            return None, [], _claim("supported", m.group(0) if field == "title" else _sentence_around(text, m.start(), m.end()),
                                    field, f"S5: '{m.group(0)}'"), None
    return None, [], _claim("insufficient", None, None, "S4: no years and no level word stated"), None


def gate4(body: str, resume: dict, cfg: dict = V03):
    threshold = cfg["skill_threshold"]
    text = body
    for rx in (K2_REMOVE if cfg["k2"] else []):
        text = rx.sub(" ", text)
    matched, quotes = [], []
    for term in resume["skills"]["networking"]:
        m = ww(term).search(text)
        if m:
            matched.append(term)
            quotes.append(m.group(0))
    if len(matched) >= threshold:
        # quote: the first matched term as it appears in the body (exact substring)
        return None, matched, _claim("supported", quotes[0], "body", f"K1: {len(matched)} networking terms: {', '.join(matched)}")
    return "K1", matched, _claim("insufficient", quotes[0] if quotes else None, "body" if quotes else None,
                                 f"K1: {len(matched)} of {threshold} networking terms")


def decide(rec: dict, resume: dict, cfg: dict = None) -> dict:
    cfg = V03 if cfg is None else cfg
    title = (rec.get("title") or "").strip()
    body = rec.get("body") or ""
    claims = {k: _claim("insufficient", None, None, "not reached") for k in ("title", "authorization", "seniority", "skills")}
    out = {"board": rec.get("board"), "id": rec.get("id"), "title": rec.get("title"), "outcome": None, "gate": None,
           "reason": "", "flags": [], "skills_matched": [], "min_years": None, "claims": claims}

    def done(outcome, gate, reason):
        out.update(outcome=outcome, gate=gate, reason=reason)
        return out

    if not title:
        return done("abstain", "2.4", "missing title")
    g, flags, claims["title"] = gate1(title, cfg)
    out["flags"] += flags
    if g:
        return done("reject", g, claims["title"]["note"])
    if len(body.strip()) < ABSTAIN_MIN_BODY:
        return done("abstain", "2.4", f"body shorter than {ABSTAIN_MIN_BODY} characters")
    g, flags, claims["authorization"] = gate2(body, cfg)
    out["flags"] += flags
    if g:
        return done("reject", g, claims["authorization"]["note"])
    if cfg["seniority"]:
        g, flags, claims["seniority"], out["min_years"] = gate3(title, body)
        out["flags"] += flags
        if g:
            return done("reject", g, claims["seniority"]["note"])
    else:
        claims["seniority"] = _claim("insufficient", None, None, "seniority gate switched off (score test)")
    g, out["skills_matched"], claims["skills"] = gate4(body, resume, cfg)
    if g:
        return done("reject", g, claims["skills"]["note"])
    if (cfg["abstain_rule2"] and claims["authorization"]["label"] == "insufficient"
            and claims["seniority"]["label"] == "insufficient" and not T3.search(title)):
        return done("abstain", "2.4", "no role word, and authorization and seniority both insufficient")
    for c in claims.values():          # FILTER section 2: a quote that cannot be found again becomes insufficient
        if c["quote"] is not None and c["quote"] not in (title if c["field"] == "title" else body):
            c.update(label="insufficient", note=c["note"] + "; quote not found again")
    if out["flags"]:
        return done("flag", None, "human decides: " + ", ".join(out["flags"]))
    return done("accept", None, "passed every gate")


def verify_quotes(decision: dict, rec: dict) -> list:
    errs = []
    for name, c in decision["claims"].items():
        if c["quote"] is None:
            continue
        src = (rec.get("title") or "") if c["field"] == "title" else (rec.get("body") or "")
        if c["quote"] not in src:
            errs.append(f"{name}: quote {c['quote']!r} not found in {c['field']}")
    return errs


def _date_key(v):
    if v is None or v == "":
        return None
    if isinstance(v, (int, float)):             # Lever createdAt, epoch milliseconds
        return datetime.datetime.fromtimestamp(v / 1000, datetime.timezone.utc).isoformat()
    return str(v)


def rank(pairs):
    """FILTER R1: seniority supported > insufficient > other; then more skills; then newest date; missing date last."""
    tier = {"supported": 0, "insufficient": 1}

    def key(p):
        rec_, dec = p
        dk = _date_key(rec_.get("date"))
        return (tier.get(dec["claims"]["seniority"]["label"], 2), -len(dec["skills_matched"]), dk is None,
                "".join(chr(0x10FFFF - ord(ch)) for ch in dk) if dk else "")
    return sorted(pairs, key=key)


def holdout_ids(path: Path = HOLDOUT_JSON) -> set:
    if not Path(path).exists():
        return set()
    return {(p["board"], p["id"]) for p in json.loads(Path(path).read_text(encoding="utf-8"))["postings"]}


def select_for_run(records, include_holdout=False, labels_path=None):
    held = holdout_ids()
    if include_holdout:
        if labels_path is None or not Path(labels_path).exists():
            raise HoldoutLocked("held-out postings stay locked until Prathamesh's labels file exists")
        return list(records)
    return [r for r in records if (r["board"], r["id"]) not in held]


def main(argv=None) -> int:
    ap = argparse.ArgumentParser()
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run")
    r.add_argument("--include-holdout", action="store_true")
    r.add_argument("--labels")
    r.add_argument("--out", default=str(HERE / "out" / "decisions.jsonl"))
    a = ap.parse_args(argv)
    resume = json.loads((HERE / "fixtures" / "resume.fictional.json").read_text(encoding="utf-8"))
    try:
        recs = select_for_run(postings.load_all(), a.include_holdout, a.labels)
    except HoldoutLocked as e:
        print(f"[refused] {e}")
        return 2
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    counts = {}
    with out.open("w", encoding="utf-8") as f:
        for rec_ in recs:
            dec = decide(rec_, resume)
            counts[dec["outcome"]] = counts.get(dec["outcome"], 0) + 1
            f.write(json.dumps(dec, ensure_ascii=False) + "\n")
    print(f"[filter] v0.3 postings={len(recs)} include_holdout={a.include_holdout} {counts} -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
