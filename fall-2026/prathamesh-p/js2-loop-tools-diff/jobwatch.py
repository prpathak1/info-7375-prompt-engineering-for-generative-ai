#!/usr/bin/env python3
"""jobwatch.py: JS1 watch for one public Lever board, one fictional résumé, new postings only.

Implements CONTRACT.md (APPROVED 2026-10-30). Python standard library only.

  record   = the deterministic rule verdict (CONTRACT section 4). Anyone can recompute it.
  judgment = a Claude verdict, accepted only through validate_judgment(). It never changes a record.

The program makes one HTTPS GET to api.lever.co per fetch. It never applies, sends, posts, or logs in.

Usage (from js1-contract-and-watch/):
    python -I jobwatch.py fetch --board zoox --raw-dir raw
    python -I jobwatch.py run --raw raw/2026-10-30/zoox.json --state state/seen_ids.json \
        --out runs/2026-10-30-run1.json --resume fixtures/resume.fictional.json [--judge claude]
    python -I jobwatch.py judge --raw raw/2026-10-30/zoox.json --posting-id <id>   (one posting; no state change)
"""
from __future__ import annotations

import argparse
import hashlib
import html
import importlib.util
import json
import os
import re
import subprocess
import sys
import tempfile
import time
import urllib.parse
import urllib.request
import uuid
from pathlib import Path


def _load_policy():
    """policy.py beside this file. It is loaded by path because `python -I` does not put the script's folder on sys.path.
    It is registered as module `policy`, so the tests' `import policy` and this module share one set of classes."""
    here = Path(__file__).resolve().with_name("policy.py")
    mod = sys.modules.get("policy")
    if mod is not None and Path(getattr(mod, "__file__", "")).resolve() == here:
        return mod
    spec = importlib.util.spec_from_file_location("policy", here)
    mod = importlib.util.module_from_spec(spec)
    sys.modules["policy"] = mod
    spec.loader.exec_module(mod)
    return mod


policy = _load_policy()
WRITTEN: list[str] = []   # every file this process wrote, in order; reported if a later write is refused (GATE section 1)


def _write(path: Path, data) -> None:
    """The single non-atomic write path. policy.check_write runs first; nothing is created if it refuses.
    bytes are written unmodified (raw evidence); str is written as UTF-8 text, as JS1 did."""
    target = policy.check_write(path)
    target.parent.mkdir(parents=True, exist_ok=True)
    if isinstance(data, bytes):
        target.write_bytes(data)
    else:
        target.write_text(data, encoding="utf-8")
    WRITTEN.append(str(target))

ALLOWED_HOST = "api.lever.co"
BOARD_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
VERDICTS = ("relevant", "not_relevant")
CITATION_KEYS = {"resume_field", "resume_value", "posting_field", "posting_value"}
JUDGMENT_KEYS = {"posting_id", "verdict", "citations"}
TEXT_FIELDS = ("descriptionPlain", "lists", "additionalPlain")
SKILL_THRESHOLD = 2


class HostRefused(Exception):
    pass


class ResumeRefused(Exception):
    pass


class JudgmentRejected(Exception):
    pass


# ---------------------------------------------------------------- allow-list and fetch (CONTRACT section 3)
def check_url(url: str) -> None:
    try:
        u = urllib.parse.urlsplit(url)
        port = u.port
    except ValueError as e:
        raise HostRefused(f"unparseable URL: {url!r}") from e
    if u.scheme != "https":
        raise HostRefused(f"scheme {u.scheme!r} refused; only https")
    if "@" in u.netloc:
        raise HostRefused("userinfo in URL refused")
    if port not in (None, 443):
        raise HostRefused(f"port {port} refused")
    if (u.hostname or "").lower() != ALLOWED_HOST:
        raise HostRefused(f"host {u.hostname!r} is not on the allow-list ({ALLOWED_HOST})")


class _AllowListRedirects(urllib.request.HTTPRedirectHandler):
    """Refuse a redirect before following it if it leaves the allow-list."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(_AllowListRedirects)


def board_url(board: str) -> str:
    if not BOARD_RE.match(board):
        raise HostRefused(f"board slug {board!r} refused")
    return f"https://{ALLOWED_HOST}/v0/postings/{board}?mode=json"


def sha256_bytes(b: bytes) -> str:
    return hashlib.sha256(b).hexdigest()


def fetch(board: str, dest_dir: Path, urlopen=_OPENER.open) -> Path:
    """One GET. The raw body is saved unmodified as dest_dir/<local date>/<board>.json, along with headers and fetch metadata.
    Files are written only after the final URL has passed the allow-list."""
    url = board_url(board)
    check_url(url)
    day = Path(dest_dir) / time.strftime("%Y-%m-%d")
    raw = day / f"{board}.json"
    for target in (raw, day / f"{board}.headers.txt", day / f"{board}.fetch.txt"):
        policy.check_write(target)            # step-6 revision: all three are checked BEFORE the network request
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "info7375-js1-watch"})
    with urlopen(req, timeout=60) as resp:
        final = resp.geturl()
        check_url(final)
        body = resp.read()
        status = getattr(resp, "status", None)
        headers = "".join(f"{k}: {v}\n" for k, v in dict(resp.headers).items())
    if status != 200:
        raise RuntimeError(f"HTTP {status} from {final}")
    json.loads(body)  # must be JSON before anything is written
    if raw.exists():
        raise FileExistsError(f"{raw} already exists; refusing to overwrite evidence")
    _write(raw, body)
    _write(day / f"{board}.headers.txt", headers)
    meta = {
        "board": board, "url": url, "final_url": final,
        "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "fetched_local": time.strftime("%a %b %d %H:%M:%S %Z %Y"),
        "http_status": status, "bytes": len(body), "sha256": sha256_bytes(body),
    }
    _write(day / f"{board}.fetch.txt", "".join(f"{k}={v}\n" for k, v in meta.items()))
    return raw


# ---------------------------------------------------------------- résumé loader (CONTRACT section 3)
def load_resume(path) -> dict:
    data = json.loads(Path(path).read_text(encoding="utf-8"))
    if not isinstance(data, dict) or data.get("fictional") is not True:
        raise ResumeRefused('résumé must contain "fictional": true')
    email = (data.get("personal") or {}).get("email")
    if not isinstance(email, str) or email.count("@") != 1 or not email.lower().endswith("@example.com"):
        raise ResumeRefused("résumé email must be an @example.com address")
    return data


# ---------------------------------------------------------------- field access and citation checks (CONTRACT section 2)
def strip_tags(s: str) -> str:
    return re.sub(r"[ \t]+", " ", html.unescape(re.sub(r"<[^>]+>", " ", s or ""))).strip()


def posting_field_text(posting: dict, field: str):
    if field == "lists":
        return "\n".join(strip_tags(item.get("content", "")) for item in posting.get("lists") or [])
    cur = posting
    for part in field.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return None
        cur = cur[part]
    return cur if isinstance(cur, str) else None


def resume_value_at(resume: dict, path: str, value) -> bool:
    cur = resume
    for part in path.split("."):
        if not isinstance(cur, dict) or part not in cur:
            return False
        cur = cur[part]
    if isinstance(cur, list):
        return any(not isinstance(x, (dict, list)) and str(x).lower() == str(value).lower() for x in cur)
    if isinstance(cur, str):
        return isinstance(value, str) and value != "" and value.lower() in cur.lower()
    if isinstance(cur, dict):
        return False
    return str(cur).lower() == str(value).lower()  # bool / number / null


def check_citations(citations, posting: dict, resume: dict) -> list[str]:
    errors = []
    if not isinstance(citations, list) or not citations:
        return ["citations must be a non-empty list"]
    for i, c in enumerate(citations):
        if not isinstance(c, dict) or set(c) != CITATION_KEYS:
            errors.append(f"citation {i}: keys must be exactly {sorted(CITATION_KEYS)}")
            continue
        rf, pf, pv = c["resume_field"], c["posting_field"], c["posting_value"]
        if not isinstance(rf, str) or not rf or not resume_value_at(resume, rf, c["resume_value"]):
            errors.append(f"citation {i}: résumé has no {c['resume_value']!r} at {rf!r}")
        text = posting_field_text(posting, pf) if isinstance(pf, str) and pf else None
        if text is None:
            errors.append(f"citation {i}: posting has no text field {pf!r}")
        elif not isinstance(pv, str) or not pv or pv.lower() not in text.lower():
            errors.append(f"citation {i}: {pv!r} not found in posting {pf!r}")
    return errors


def cite(resume_field, resume_value, posting_field, posting_value) -> dict:
    return {"resume_field": resume_field, "resume_value": resume_value,
            "posting_field": posting_field, "posting_value": posting_value}


# ---------------------------------------------------------------- the rule (CONTRACT section 4)
# Gate 1 reuses decide() from prpathak1/the-reallocation-engine
# scripts/contrib/2026fa/prpathak1-network-sponsorship-text/filter_titles.py (commit f3ea8b7), unchanged.
NETWORK = re.compile(r"\bnetwork(s|ing)?\b", re.I)
FALSE_FRIEND = re.compile(r"\b(road|social|neural|sales|partner|retail|distribution)\s+network", re.I)
ROLE = re.compile(r"\b(engineer|engineering|architect|administrator|admin|security|infrastructure)\b", re.I)
SOFTWARE = re.compile(r"\bsoftware\b", re.I)


def title_decision(title: str) -> tuple[str, str]:
    if not NETWORK.search(title):
        return "exclude", "no 'network' in title"
    if FALSE_FRIEND.search(title):
        return "exclude", f"false friend: '{FALSE_FRIEND.search(title).group(0)}'"
    if SOFTWARE.search(title):
        return "flag", "software-engineering title mentioning network; may be SOC 15-1252, human decides"
    if ROLE.search(title):
        return "include", "network role title"
    return "flag", "mentions network but no recognised role word; human decides"


def whole_word(term: str, plural: bool = False) -> re.Pattern:
    return re.compile(r"(?<!\w)" + re.escape(term) + (r"s?" if plural else "") + r"(?!\w)", re.I)


# Gate 2: each phrase is whole-word (optionally + "s"), case-insensitive, and maps to the constraints.excluded entry it violates.
CITIZEN = "roles requiring U.S. citizenship"
CLEARANCE = "roles requiring an active or obtainable security clearance"
EXPORT = "roles restricted to U.S. persons under ITAR/EAR export control"
AUTH_PHRASES = [
    ("U.S. citizen", CITIZEN), ("US citizen", CITIZEN), ("U.S. citizenship", CITIZEN),
    ("U.S. person", EXPORT), ("security clearance", CLEARANCE), ("active clearance", CLEARANCE),
    ("ITAR", EXPORT), ("EAR", EXPORT), ("export control", EXPORT),
    # sponsorship refusal (amended 2026-10-31); no constraints.excluded entry names it, so None = cite visa.type instead
    ("without sponsorship", None), ("without visa sponsorship", None), ("no sponsorship", None),
    ("not sponsor", None), ("will not sponsor", None), ("unable to sponsor", None),
    ("cannot sponsor", None), ("does not sponsor", None),
]
AUTH_PATTERNS = [(p, whole_word(p, plural=True), excl) for p, excl in AUTH_PHRASES]


def decide(posting: dict, resume: dict) -> dict:
    title = posting.get("text") or ""
    t_dec, t_reason = title_decision(title)
    citations = [cite("target.soc_code", resume["target"]["soc_code"], "text", title)] if title else []

    hits = []
    for phrase, pat, excluded in AUTH_PATTERNS:
        for field in TEXT_FIELDS:
            text = posting_field_text(posting, field) or ""
            m = pat.search(text)
            if m:
                hits.append({"phrase": phrase, "field": field, "matched": m.group(0)})
                citations.append(cite("visa.needs_sponsorship", resume["visa"]["needs_sponsorship"], field, m.group(0)))
                if excluded is None:
                    citations.append(cite("visa.type", resume["visa"]["type"], field, m.group(0)))
                else:
                    citations.append(cite("constraints.excluded", excluded, field, m.group(0)))
                if excluded == EXPORT:
                    citations.append(cite("visa.us_person_for_itar", resume["visa"]["us_person_for_itar"], field, m.group(0)))
                break  # first field with this phrase is enough

    matched = []
    for term in resume["skills"]["networking"]:
        pat = whole_word(term, plural=True)
        for field in TEXT_FIELDS:
            m = pat.search(posting_field_text(posting, field) or "")
            if m:
                matched.append(term)
                citations.append(cite("skills.networking", term, field, m.group(0)))
                break

    if t_dec != "include":
        reason = f"Gate 1 (title) {t_dec}: {t_reason}"
    elif hits:
        reason = "Gate 2 (authorization): " + ", ".join(f"'{h['matched']}' in {h['field']}" for h in hits)
    elif len(matched) < SKILL_THRESHOLD:
        reason = f"Gate 3 (skills): {len(matched)} of {SKILL_THRESHOLD} required skills.networking terms matched"
    else:
        reason = f"all gates pass; skills matched: {', '.join(matched)}"
    relevant = t_dec == "include" and not hits and len(matched) >= SKILL_THRESHOLD
    return {
        "label": "record",
        "verdict": "relevant" if relevant else "not_relevant",
        "needs_human": t_dec == "flag",
        "reason": reason,
        "gate_results": {
            "title": {"decision": t_dec, "reason": t_reason},
            "authorization": {"hits": hits},
            "skills": {"matched": matched, "threshold": SKILL_THRESHOLD},
        },
        "citations": citations,
    }


# ---------------------------------------------------------------- judgment validator (CONTRACT sections 2-3)
def validate_judgment(raw_text: str, posting: dict, resume: dict) -> dict:
    try:
        obj = json.loads(raw_text)
    except (TypeError, ValueError) as e:
        raise JudgmentRejected(f"not a JSON document: {e}") from e
    if not isinstance(obj, dict):
        raise JudgmentRejected("top level must be a JSON object")
    if set(obj) != JUDGMENT_KEYS:
        raise JudgmentRejected(f"keys must be exactly {sorted(JUDGMENT_KEYS)}, got {sorted(obj)}")
    if obj["posting_id"] != posting.get("id"):
        raise JudgmentRejected(f"posting_id {obj['posting_id']!r} does not match {posting.get('id')!r}")
    if obj["verdict"] not in VERDICTS:
        raise JudgmentRejected(f"verdict must be one of {VERDICTS}")
    errors = check_citations(obj["citations"], posting, resume)
    if errors:
        raise JudgmentRejected("; ".join(errors))
    return {"label": "judgment", "status": "accepted", "posting_id": obj["posting_id"],
            "verdict": obj["verdict"], "citations": obj["citations"]}


def judge_posting(judge, posting: dict, resume: dict) -> dict:
    """A judge returns the model's text, or {"text": ..., "meta": {...}} with provenance (claude_judge does this)."""
    if judge is None:
        return {"label": "judgment", "status": "not_run"}
    raw, meta = None, {}
    try:
        got = judge(posting, resume)
        raw, meta = (got["text"], got.get("meta", {})) if isinstance(got, dict) else (got, {})
        out = validate_judgment(raw, posting, resume)
    except JudgmentRejected as e:
        return {"label": "judgment", "status": "rejected", "errors": [str(e)], "raw_response": raw, **meta}
    except Exception as e:  # a judge failure is a judgment failure, never a record failure
        return {"label": "judgment", "status": "error", "errors": [repr(e)], "raw_response": raw, **meta}
    out["obtained_at"] = meta.get("finished_at") or time.strftime("%Y-%m-%dT%H:%M:%S%z")
    return {**out, **meta}


# ---------------------------------------------------------------- Claude judge via headless Claude Code
def posting_view(posting: dict) -> dict:
    """The posting as Claude sees it. Every field is the same text that check_citations() validates against."""
    cats = posting.get("categories") or {}
    return {"id": posting.get("id"), "text": posting.get("text", ""),
            "categories": {k: cats.get(k) for k in ("location", "team", "commitment")},
            "descriptionPlain": posting.get("descriptionPlain", ""),
            "lists": posting_field_text(posting, "lists"),
            "additionalPlain": posting.get("additionalPlain", "")}


def build_judge_prompt(template: str, posting: dict, resume: dict) -> str:
    return (template.replace("{{RESUME_JSON}}", json.dumps(resume, indent=2, ensure_ascii=False))
                    .replace("{{POSTING_JSON}}", json.dumps(posting_view(posting), indent=2, ensure_ascii=False))
                    .replace("{{POSTING_ID}}", str(posting.get("id"))))


def claude_judge(prompt_path, log_dir, runner=subprocess.run, claude_bin="claude", model=None, timeout=300):
    """Return judge(posting, resume). Each call is a new `claude -p` process with a new session ID, no session
    persistence, no tools, and an empty working directory. The full raw output is saved before validation."""
    prompt_path, log_dir = Path(prompt_path), Path(log_dir)
    policy.check_write(log_dir / "_write-check")   # refuse an unwritable log folder before any `claude -p` call; nothing is created
    template = prompt_path.read_text(encoding="utf-8")

    def judge(posting: dict, resume: dict) -> dict:
        session = str(uuid.uuid4())
        prompt = build_judge_prompt(template, posting, resume)
        cmd = [claude_bin, "-p", "--no-session-persistence", "--session-id", session,
               "--output-format", "json", "--tools", "", "--strict-mcp-config"]
        if model:
            cmd += ["--model", model]
        requested = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        with tempfile.TemporaryDirectory() as cwd:
            proc = runner(cmd, input=prompt, capture_output=True, text=True, encoding="utf-8",
                          timeout=timeout, cwd=cwd)
        finished = time.strftime("%Y-%m-%dT%H:%M:%S%z")
        try:
            envelope = json.loads(proc.stdout)
        except (TypeError, ValueError):
            envelope = None
        env = envelope if isinstance(envelope, dict) else {}
        text = env["result"] if isinstance(env.get("result"), str) else proc.stdout
        meta = {"session_id": env.get("session_id") or session, "session_id_requested": session,
                "model": sorted(env.get("modelUsage") or {}) or None,
                "requested_at": requested, "finished_at": finished}
        out = log_dir / f"{time.strftime('%Y%m%dT%H%M%S')}-{posting.get('id')}-{session}.json"
        _write(out, json.dumps({
            **meta, "label": "judgment (raw Claude response)", "posting_id": posting.get("id"),
            "prompt_file": prompt_path.as_posix(), "prompt_sha256": sha256_bytes(prompt.encode("utf-8")),
            "cmd": cmd, "returncode": proc.returncode, "stdout": proc.stdout, "stderr": proc.stderr,
        }, indent=2, ensure_ascii=False))
        meta["raw_response_file"] = out.as_posix()
        return {"text": text, "meta": meta}

    return judge


# ---------------------------------------------------------------- the watch (CONTRACT section 6)
def _write_atomic(path: Path, text: str) -> None:
    target = policy.check_write(path)
    tmp = policy.check_write(path.with_name(path.name + ".tmp"))
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(text, encoding="utf-8")
    os.replace(tmp, target)
    WRITTEN.append(str(target))


def run(raw_path, state_path, out_path, resume: dict, judge=None, label=None) -> dict:
    """label (e.g. "SEEDED") is written at the top of the report; real runs carry no label."""
    raw_path, state_path, out_path = Path(raw_path), Path(state_path), Path(out_path)
    policy.check_write(out_path)       # GATE section 5: both outputs are checked before anything is read or written
    policy.check_write(state_path)
    raw_bytes = raw_path.read_bytes()
    data = json.loads(raw_bytes)
    if not isinstance(data, list) or not all(isinstance(p, dict) and isinstance(p.get("id"), str) for p in data):
        raise ValueError(f"{raw_path}: expected a JSON list of postings with string ids")

    baseline = not state_path.exists()
    prev = set() if baseline else set(json.loads(state_path.read_text(encoding="utf-8"))["ids"])
    today = [p["id"] for p in data]
    new = [] if baseline else [
        {"posting_id": p["id"], "posting_title": p.get("text", ""),
         "record": decide(p, resume), "judgment": judge_posting(judge, p, resume)}
        for p in data if p["id"] not in prev
    ]
    report = {
        **({"label": label} if label else {}),
        "run_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"),
        "raw_file": raw_path.as_posix(), "raw_sha256": sha256_bytes(raw_bytes),
        "baseline": baseline, "total": len(data), "new_count": len(new),
        "removed_count": 0 if baseline else len(prev - set(today)),
        "new": new,
    }
    _write_atomic(out_path, json.dumps(report, indent=2, ensure_ascii=False))
    _write_atomic(state_path, json.dumps({"ids": sorted(set(today))}, indent=2))  # state last
    return report


# ---------------------------------------------------------------- CLI
def main(argv=None) -> int:
    WRITTEN.clear()   # per call, not per process: a refusal reports only this call's own writes (defect in 6dc2abb, FRICTIONAL F34)
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    f = sub.add_parser("fetch", help="one GET of the board; saves raw evidence")
    f.add_argument("--board", required=True)
    f.add_argument("--raw-dir", default="raw")
    r = sub.add_parser("run", help="diff a saved raw response against state; verdicts for new postings")
    r.add_argument("--raw", required=True)
    r.add_argument("--state", default="state/seen_ids.json")
    r.add_argument("--out", required=True)
    r.add_argument("--resume", default="fixtures/resume.fictional.json")
    r.add_argument("--judge", choices=["none", "claude"], default="none")
    r.add_argument("--label", help='e.g. SEEDED; written into the report and printed on every line')
    j = sub.add_parser("judge", help="Claude judgment for ONE saved posting; never touches state")
    j.add_argument("--raw", required=True)
    j.add_argument("--posting-id", required=True)
    j.add_argument("--resume", default="fixtures/resume.fictional.json")
    for q in (r, j):
        q.add_argument("--prompt", default="prompts/judge_v1.md")
        q.add_argument("--judge-log", default="traces/judgments")
        q.add_argument("--model")
    a = ap.parse_args(argv)
    try:
        return _dispatch(a)
    except policy.PermissionRefused as e:
        print(f"[error] {e}", file=sys.stderr)
        print(f"[error] status=error step={a.cmd}; files written before the refusal: {WRITTEN or 'none'}", file=sys.stderr)
        return 2


def _dispatch(a) -> int:
    if a.cmd == "fetch":
        path = fetch(a.board, Path(a.raw_dir))
        print(f"[fetch] saved {path}")
        print((path.parent / f"{a.board}.fetch.txt").read_text(encoding="utf-8"), end="")
        return 0

    resume = load_resume(a.resume)
    if a.cmd == "judge":
        post = next(p for p in json.loads(Path(a.raw).read_bytes()) if p.get("id") == a.posting_id)
        result = {"posting_id": a.posting_id, "posting_title": post.get("text", ""),
                  "record": decide(post, resume),
                  "judgment": judge_posting(claude_judge(a.prompt, a.judge_log, model=a.model), post, resume)}
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0
    judge = claude_judge(a.prompt, a.judge_log, model=a.model) if a.judge == "claude" else None
    rep = run(a.raw, a.state, a.out, resume, judge=judge, label=a.label)
    if a.label:
        print(f"[run] *** {a.label} *** (not a real board change)")
    print(f"[run] raw={rep['raw_file']} sha256={rep['raw_sha256']}")
    print(f"[run] baseline={rep['baseline']} total={rep['total']} new={rep['new_count']} removed={rep['removed_count']}")
    for n in rep["new"]:
        rec = n["record"]
        flag = " needs_human" if rec["needs_human"] else ""
        print(f"  RECORD {rec['verdict']:12}{flag} {n['posting_id']} {n['posting_title']}  [{rec['reason']}]")
        print(f"  JUDGMENT status={n['judgment']['status']} verdict={n['judgment'].get('verdict', '-')}")
    print(f"[run] report -> {a.out}; state -> {a.state}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
