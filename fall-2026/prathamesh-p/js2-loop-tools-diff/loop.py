#!/usr/bin/env python3
"""loop.py: the JS2 bounded agent loop over several public job boards (GATE.md, APPROVED 2026-11-10 08:17:25 EST; amendment A1).

One run:
  - takes a fixed board list (default: the GATE D-1 boards plus the D-12 deliberate failure) and collapses duplicates;
  - checks budgets BEFORE each request (boards 4, requests 6, seconds 120);
  - makes one GET per board, plus at most one retry, and only for a timeout, a connection reset, 429 or 5xx;
  - saves every response body unmodified, with a .fetch.txt (status, bytes, SHA-256), under raw/<day>/;
  - computes new IDs against per-board state and, for new postings, the JS1 record (jobwatch.decide). There is no Claude judge (D-2);
  - writes one trace line per observation under traces/, and one report runs/<run_id>-<status>.json;
  - ends in exactly one status: finished 0 / error 2 / incomplete 3 / budget_exhausted 4. "finished" is not "correct": run verify.py.

Every file read and write goes through policy.py (GATE section 5), and every permission check comes BEFORE the action it guards.
The only network method is GET, only to the three allowed hosts. The agent never applies, sends messages, posts or logs in.
Python standard library only.

Usage (from js2-loop-tools-diff/):
    python -I loop.py run                                   # the four GATE boards, live
    python -I loop.py run --board lever:zoox --max-requests 2
    python -I loop.py seed-state --board ashby:openai --from-raw raw/2026-11-10/openai.json --state-dir state/SEEDED --label SEEDED
    python -I loop.py run --board ashby:openai --replay ashby:openai=seeded/SEEDED-openai-empty.json --state-dir state/SEEDED --label SEEDED
"""
from __future__ import annotations

import argparse
import hashlib
import importlib.util
import json
import re
import socket
import sys
import time
import urllib.error
import urllib.parse
import urllib.request
import uuid
from dataclasses import dataclass
from pathlib import Path

HERE = Path(__file__).resolve().parent


def _load(name: str):
    """Load a sibling module by path (`python -I` puts no script folder on sys.path), sharing it with a normal `import name`."""
    path = HERE / f"{name}.py"
    mod = sys.modules.get(name)
    if mod is not None and Path(getattr(mod, "__file__", "")).resolve() == path:
        return mod
    spec = importlib.util.spec_from_file_location(name, path)
    mod = importlib.util.module_from_spec(spec)
    sys.modules[name] = mod
    spec.loader.exec_module(mod)
    return mod


policy = _load("policy")
adapters = _load("adapters")
jobwatch = _load("jobwatch")

# ---------------------------------------------------------------- GATE section 2 and section 4 values. A test checks these against GATE.md (D-6).
MAX_BOARDS = 4
MAX_REQUESTS = 6
MAX_SECONDS = 120
REQUEST_TIMEOUT = 30
RETRY_DELAY = 2
RETRY_AFTER_CAP = 10

EXIT_CODES = {"finished": 0, "error": 2, "incomplete": 3, "budget_exhausted": 4}
DEFAULT_BOARDS = ["lever:zoox", "greenhouse:cloudflare", "ashby:openai", "greenhouse:cloudflare-js2-does-not-exist"]
RETRY_STATUSES = {429, 500, 502, 503, 504}
ESCALATE_STATUSES = {401, 403}
NO_RETRY_FAIL_STATUSES = {404, 410}
LOGIN_PATH_RE = re.compile(r"/(login|log-in|signin|sign-in|sign_in|sso|oauth|auth)(/|$|\?)", re.I)
VERIFY_REMINDER = ("verify.py has NOT run. 'finished' only means every board reached a terminal outcome inside budget; "
                   "it does not mean the result is right (GATE section 1). Run: python -I verify.py <this report>")


class HostRefused(Exception):
    pass


class DNSFailure(OSError):
    pass


class ConfigRefused(Exception):
    """A run configuration GATE does not allow: a budget raised above GATE, too many boards, or an unknown board."""


class _BudgetOut(Exception):
    def __init__(self, name, value):
        super().__init__(f"{name} budget exhausted at {value}")
        self.name, self.value = name, value


@dataclass
class Response:
    status: int
    headers: dict
    body: bytes
    final_url: str


# ---------------------------------------------------------------- hosts, URLs and the repeat rule (GATE section 3 and section 5)
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
    if (u.hostname or "").lower() not in adapters.ALLOWED_HOSTS:
        raise HostRefused(f"host {u.hostname!r} is not on the allow-list {adapters.ALLOWED_HOSTS}")


def normalize_url(url: str) -> str:
    u = urllib.parse.urlsplit(url)
    scheme = u.scheme.lower()
    host = (u.hostname or "").lower()
    default = {"https": 443, "http": 80}.get(scheme)
    netloc = host if u.port in (None, default) else f"{host}:{u.port}"
    query = urllib.parse.urlencode(sorted(urllib.parse.parse_qsl(u.query, keep_blank_values=True)))
    return urllib.parse.urlunsplit((scheme, netloc, u.path or "/", query, ""))


class Ledger:
    """The repeat rule: an action is (method, normalized URL). The first send is permitted, one explicit retry is permitted,
    and anything else is refused and NOT sent. A refused repeat is recorded but not counted in `sent`."""

    def __init__(self):
        self.sent = 0
        self.refused: list[dict] = []
        self._count: dict[tuple, int] = {}

    def permit(self, method: str, url: str, retry: bool = False) -> bool:
        key = (method.upper(), normalize_url(url))
        n = self._count.get(key, 0)
        if (n == 0 and not retry) or (n == 1 and retry):
            self._count[key] = n + 1
            self.sent += 1
            return True
        self.refused.append({"method": key[0], "url": key[1], "retry": retry, "already_sent": n})
        return False


class _AllowListRedirects(urllib.request.HTTPRedirectHandler):
    """Refuse a redirect before following it if it leaves the allow-list (GATE section 5, W8)."""

    def redirect_request(self, req, fp, code, msg, headers, newurl):
        check_url(newurl)
        return super().redirect_request(req, fp, code, msg, headers, newurl)


_OPENER = urllib.request.build_opener(_AllowListRedirects)


def urllib_transport(url: str, timeout: float) -> Response:
    """The only network code. One GET; HTTP error statuses come back as a Response; timeouts, resets and DNS failures are raised."""
    check_url(url)
    req = urllib.request.Request(url, method="GET", headers={"User-Agent": "info7375-js2-loop"})
    urlopen = _OPENER.open
    try:
        with urlopen(req, timeout=timeout) as resp:
            return Response(resp.status, dict(resp.headers), resp.read(), resp.geturl())
    except urllib.error.HTTPError as e:
        body = e.read() if e.fp is not None else b""
        return Response(e.code, dict(e.headers or {}), body, e.geturl() or url)
    except urllib.error.URLError as e:
        reason = e.reason
        if isinstance(reason, socket.gaierror):
            raise DNSFailure(str(reason)) from e
        if isinstance(reason, TimeoutError):
            raise TimeoutError(str(reason)) from e
        if isinstance(reason, ConnectionResetError):
            raise reason from e
        raise


def replay_transport(mapping: dict[str, Path]) -> callable:
    """Offline transport for SEEDED or replayed runs: serves files (read through policy.check_read) instead of the network."""
    def transport(url: str, timeout: float) -> Response:
        key = normalize_url(url)
        if key not in mapping:
            raise ConfigRefused(f"replay transport has no file for {url}; no network is used in replay mode")
        return Response(200, {}, policy.check_read(mapping[key]).read_bytes(), url)
    return transport


# ---------------------------------------------------------------- paths
def today() -> str:
    return time.strftime("%Y-%m-%d")


def raw_path(raw_dir, day: str, key: str, run_id: str, attempt: int, ext: str) -> Path:
    return Path(raw_dir) / day / f"{key}.{run_id}.a{attempt}{ext}"


def meta_path(raw_dir, day: str, key: str, run_id: str, attempt: int) -> Path:
    return Path(raw_dir) / day / f"{key}.{run_id}.a{attempt}.fetch.txt"


def parse_board(spec: str) -> tuple[str, str, str]:
    if ":" not in spec:
        raise ConfigRefused(f"board {spec!r} must be written platform:slug, for example lever:zoox")
    platform, slug = (x.strip().lower() for x in spec.split(":", 1))
    try:
        adapters.board_url(platform, slug)
    except ValueError as e:
        raise ConfigRefused(str(e)) from e
    return platform, slug, f"{platform}-{slug}"


# ---------------------------------------------------------------- one run
class _Run:
    def __init__(self, run_id, label, traces_dir, approve):
        self.run_id, self.label, self.approve = run_id, label, tuple(approve)
        self.trace = Path(traces_dir) / f"{run_id}.jsonl"
        self.written: list[str] = []
        self.step = "start"

    def write(self, path, data) -> Path:
        target = policy.check_write(path, approve=self.approve)
        target.parent.mkdir(parents=True, exist_ok=True)
        if isinstance(data, bytes):
            target.write_bytes(data)
        else:
            target.write_text(data, encoding="utf-8")
        self.written.append(str(target))
        return target

    def read(self, path) -> bytes:
        return policy.check_read(path).read_bytes()

    def observe(self, kind: str, **fields) -> None:
        line = {"t": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "run_id": self.run_id, "label": self.label, "kind": kind, **fields}
        target = policy.check_write(self.trace)
        target.parent.mkdir(parents=True, exist_ok=True)
        new = not target.exists()
        with target.open("a", encoding="utf-8") as f:
            f.write(json.dumps(line, ensure_ascii=False) + "\n")
        if new:
            self.written.append(str(target))


def _budgets(max_boards, max_requests, max_seconds) -> dict:
    out = {}
    for name, given, cap in (("boards", max_boards, MAX_BOARDS), ("requests", max_requests, MAX_REQUESTS),
                             ("seconds", max_seconds, MAX_SECONDS)):
        if given is None:
            out[name] = cap
        elif not (1 <= given <= cap):
            raise ConfigRefused(f"--max-{name} {given} refused: a flag can only lower a GATE budget (1..{cap}); "
                                f"raising it needs a dated GATE.md amendment by Prathamesh")
        else:
            out[name] = given
    return out


def _header(headers: dict, name: str):
    for k, v in (headers or {}).items():
        if k.lower() == name.lower():
            return v
    return None


def run_loop(boards, *, transport=None, raw_dir=HERE / "raw", state_dir=HERE / "state", runs_dir=HERE / "runs",
             traces_dir=HERE / "traces", resume_path=HERE / "fixtures" / "resume.fictional.json", max_boards=None,
             max_requests=None, max_seconds=None, approve=(), label=None, run_id=None, clock=time.monotonic,
             sleep=time.sleep) -> dict:
    transport = transport or urllib_transport
    start = clock()
    run_id = run_id or f"{label + '-' if label else ''}{time.strftime('%Y%m%dT%H%M%S')}-{uuid.uuid4().hex[:6]}"
    ctx = _Run(run_id, label, traces_dir, approve)
    ledger = Ledger()
    report = {"run_id": run_id, "label": label, "started_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "status": None,
              "exit_code": None, "budgets": None, "boards": [], "escalations": [], "not_attempted": [],
              "requests_used": 0, "seconds_used": 0, "verify_reminder": VERIFY_REMINDER,
              "trace_file": str(ctx.trace), "report_file": None}
    keys: list[tuple] = []
    try:
        ctx.step = "configuration"
        budgets = report["budgets"] = _budgets(max_boards, max_requests, max_seconds)
        seen, collapsed = {}, []
        for spec in boards:
            platform, slug, key = parse_board(spec)
            if key in seen:
                collapsed.append({"spec": spec, "same_as": seen[key]})
                continue
            seen[key] = spec
            keys.append((platform, slug, key))
        if len(keys) > budgets["boards"]:
            raise ConfigRefused(f"{len(keys)} boards refused: the board budget is {budgets['boards']} (GATE section 2)")

        ctx.step = "permission pre-checks"           # every folder and the résumé are checked before any request
        for d in (raw_dir, state_dir, runs_dir, traces_dir):
            policy.check_write(Path(d) / "_write-check")
        policy.check_read(Path(state_dir) / "_read-check")
        resume = jobwatch.load_resume(policy.check_read(resume_path))

        ctx.observe("run_start", boards=[k for *_, k in keys], budgets=budgets, approve=list(ctx.approve))
        for c in collapsed:
            ctx.observe("collapsed", **c)
        for i, (platform, slug, key) in enumerate(keys):
            ctx.step = f"board {key}"
            _do_board(ctx, report, ledger, budgets, transport, sleep, clock, start, platform, slug, key,
                      Path(raw_dir), Path(state_dir), resume)
        report["status"] = ("incomplete" if any(b["outcome"].startswith("failed_") or b["outcome"] == "escalated"
                                                for b in report["boards"]) else "finished")
    except _BudgetOut as b:
        report["status"] = "budget_exhausted"
        report["budget"] = {"name": b.name, "value": b.value}
        done = {x["board"] for x in report["boards"]}
        for platform, slug, key in keys:
            if key not in done:
                report["boards"].append({"board": key, "platform": platform, "url": adapters.board_url(platform, slug),
                                         "outcome": "not_attempted", "attempts": 0})
        report["not_attempted"] = [x["board"] for x in report["boards"] if x["outcome"] == "not_attempted"]
        _safe_observe(ctx, "budget_exhausted", budget=b.name, value=b.value, not_attempted=report["not_attempted"])
    except Exception as e:  # noqa: BLE001  GATE section 4: a refusal or any other fault stops the run
        report["status"] = "error"
        report["error"] = {"type": type(e).__name__, "message": str(e), "step": ctx.step, "written": list(ctx.written)}
        done = {x["board"] for x in report["boards"]}
        report["not_attempted"] = [key for *_, key in keys if key not in done]
        _safe_observe(ctx, "error", type=type(e).__name__, message=str(e), step=ctx.step)

    report["exit_code"] = EXIT_CODES[report["status"]]
    report["requests_used"] = ledger.sent
    report["refused_repeats"] = ledger.refused
    report["seconds_used"] = round(clock() - start, 3)
    report["ended_at"] = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    _safe_observe(ctx, "run_end", status=report["status"], exit_code=report["exit_code"],
                  requests_used=report["requests_used"], seconds_used=report["seconds_used"])
    out = Path(runs_dir) / f"{run_id}-{report['status']}.json"
    try:
        report["report_file"] = str(policy.check_write(out))
        ctx.write(out, json.dumps(report, indent=2, ensure_ascii=False))
    except Exception as e:  # noqa: BLE001  the report itself could not be written; say so, do not hide it
        report["report_file"] = None
        report["report_write_error"] = f"{type(e).__name__}: {e}"
    return report


def _safe_observe(ctx, kind, **fields):
    try:
        ctx.observe(kind, **fields)
    except Exception:  # noqa: BLE001  a refused trace write must not mask the original status
        pass


def _do_board(ctx, report, ledger, budgets, transport, sleep, clock, start, platform, slug, key, raw_dir, state_dir, resume):
    url = adapters.board_url(platform, slug)
    check_url(url)
    b = {"board": key, "platform": platform, "url": url, "outcome": None, "attempts": 0, "attempt_log": []}
    report["boards"].append(b)
    day = today()
    attempt, retry, pending = 1, False, None

    def finish_failed(outcome, error_type, why, http_status=None):
        b.update({"outcome": outcome, "error_type": error_type, "why_stopped": why})
        if http_status is not None:
            b["http_status"] = http_status
        ctx.observe("board_outcome", board=key, outcome=outcome, why=why)

    while True:
        # 1. permission checks for every file this attempt could write, BEFORE the request (step-6 rule)
        paths = {ext: raw_path(raw_dir, day, key, ctx.run_id, attempt, ext) for ext in (".json", ".body")}
        meta = meta_path(raw_dir, day, key, ctx.run_id, attempt)
        for p in (*paths.values(), meta):
            policy.check_write(p, approve=ctx.approve)
        # 2. budgets, checked before the request
        elapsed = clock() - start
        try:
            if ledger.sent + 1 > budgets["requests"]:
                raise _BudgetOut("requests", ledger.sent)
            if elapsed >= budgets["seconds"]:
                raise _BudgetOut("seconds", round(elapsed, 3))
        except _BudgetOut as out:
            if pending:
                finish_failed(*pending[:2], f"{pending[2]}; the retry was not taken because the {out.name} budget ran out",
                              pending[3])
            else:
                b["outcome"] = "not_attempted"
                ctx.observe("board_outcome", board=key, outcome="not_attempted", why=str(out))
            raise
        # 3. the repeat rule
        if not ledger.permit("GET", url, retry=retry):
            ctx.observe("repeat_refused", board=key, url=url, attempt=attempt)
            raise RuntimeError(f"repeat rule refused attempt {attempt} for {url}; internal fault")
        ctx.observe("request", board=key, url=url, attempt=attempt, retry=retry, requests_used=ledger.sent)
        b["attempts"] = attempt

        # 4. the request
        try:
            resp = transport(url, REQUEST_TIMEOUT)
        except (TimeoutError, ConnectionResetError, DNSFailure) as e:
            kind = "dns" if isinstance(e, DNSFailure) else "timeout" if isinstance(e, TimeoutError) else "reset"
            outcome = "failed_timeout" if kind == "timeout" else "failed_network"
            b["attempt_log"].append({"n": attempt, "error": type(e).__name__, "message": str(e)})
            ctx.observe("response", board=key, attempt=attempt, error=type(e).__name__, message=str(e))
            if kind in ("timeout", "reset") and attempt == 1:
                pending = (outcome, kind, f"{type(e).__name__} on attempt 1 (GATE section 4: one retry for timeout/reset)", None)
                ctx.observe("retry_wait", board=key, seconds=RETRY_DELAY, reason=kind)
                sleep(RETRY_DELAY)
                attempt, retry = 2, True
                continue
            why = ("DNS failure: no retry (GATE section 4)" if kind == "dns"
                   else f"{type(e).__name__} on attempt {attempt}; one retry already used (GATE section 4)")
            finish_failed(outcome, kind, why)
            return

        # 5. allow-list on the final URL before anything is saved (W8); then save the evidence
        check_url(resp.final_url)
        status = int(resp.status)
        login = status == 200 and bool(LOGIN_PATH_RE.search(urllib.parse.urlsplit(resp.final_url).path))
        parsed, fmt_err = None, None
        if status == 200 and not login:
            try:
                parsed = adapters.parse(platform, resp.body)
            except adapters.FormatChanged as e:
                fmt_err = e
        body_path = ctx.write(paths[".json"] if parsed is not None else paths[".body"], resp.body)
        sha = hashlib.sha256(resp.body).hexdigest()
        meta_lines = {"file": body_path.name, "board": key, "platform": platform, "url": url, "final_url": resp.final_url,
                      "attempt": attempt, "http_status": status, "bytes": len(resp.body), "sha256": sha,
                      "parsed": "yes" if parsed is not None else "no (unparsed)",
                      "fetched_utc": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
                      "fetched_local": time.strftime("%a %b %d %H:%M:%S %Z %Y"), "run_id": ctx.run_id, "label": ctx.label}
        ctx.write(meta, "".join(f"{k}={v}\n" for k, v in meta_lines.items()))
        b["attempt_log"].append({"n": attempt, "http_status": status, "final_url": resp.final_url, "raw_file": str(body_path),
                                 "fetch_file": str(meta.resolve()), "sha256": sha, "bytes": len(resp.body)})
        ctx.observe("response", board=key, attempt=attempt, http_status=status, raw_file=str(body_path), sha256=sha,
                    bytes=len(resp.body))

        # 6. classify (GATE section 4)
        if status == 200 and (login or fmt_err):
            reason = (f"redirected to a login page ({resp.final_url}); the agent never logs in" if login
                      else f"format changed: {fmt_err}")
            b.update({"outcome": "escalated", "error_type": "login_redirect" if login else "format_changed",
                      "http_status": status, "why_stopped": f"{reason} (GATE section 4: no retry, human escalation)"})
            report["escalations"].append({"board": key, "reason": reason, "evidence": str(body_path)})
            ctx.observe("board_outcome", board=key, outcome="escalated", why=reason)
            return
        if status == 200:
            _finish_ok(ctx, b, key, parsed, state_dir, resume, body_path)
            return
        if status in RETRY_STATUSES:
            ra = _header(resp.headers, "Retry-After")
            if attempt == 1:
                if ra is not None and str(ra).strip().isdigit() and int(str(ra).strip()) > RETRY_AFTER_CAP:
                    finish_failed(f"failed_http_{status}", f"http_{status}",
                                  f"HTTP {status} with Retry-After {ra} s > {RETRY_AFTER_CAP} s: no retry (GATE section 4)", status)
                    return
                delay = int(str(ra).strip()) if ra is not None and str(ra).strip().isdigit() else RETRY_DELAY
                pending = (f"failed_http_{status}", f"http_{status}", f"HTTP {status} on attempt 1", status)
                ctx.observe("retry_wait", board=key, seconds=delay, reason=f"http_{status}")
                sleep(delay)
                attempt, retry = 2, True
                continue
            finish_failed(f"failed_http_{status}", f"http_{status}",
                          f"HTTP {status} on attempt 2; one retry already used (GATE section 4)", status)
            return
        if status in ESCALATE_STATUSES:
            reason = f"HTTP {status}: the board may now need a login; the agent never logs in"
            b.update({"outcome": "escalated", "error_type": f"http_{status}", "http_status": status,
                      "why_stopped": f"{reason} (GATE section 4: no retry, human escalation)"})
            report["escalations"].append({"board": key, "reason": reason, "evidence": str(body_path)})
            ctx.observe("board_outcome", board=key, outcome="escalated", why=reason)
            return
        if status in NO_RETRY_FAIL_STATUSES:
            finish_failed(f"failed_http_{status}", f"http_{status}",
                          f"HTTP {status}: bad board name or removed board; no retry (GATE section 4)", status)
            return
        finish_failed(f"failed_http_{status}", f"http_{status}",
                      f"HTTP {status} is not in the GATE section 4 retry list; no retry", status)
        return


def _finish_ok(ctx, b, key, posts, state_dir, resume, body_path):
    ids, seen_today = [], set()
    for p in posts:
        if p["id"] not in seen_today:
            seen_today.add(p["id"])
            ids.append(p["id"])
    state_file = state_dir / f"{key}.json"
    previous_state_file = None
    if policy.check_read(state_file).exists():
        prev_bytes = ctx.read(state_file)
        prev = set(json.loads(prev_bytes)["ids"])
        hist = ctx.write(state_dir / "history" / f"{key}.before-{ctx.run_id}.json", prev_bytes)
        previous_state_file = str(hist)
        new_ids = [i for i in ids if i not in prev]
    else:
        new_ids = []                                   # baseline: the first run reports nothing as new (as in JS1)
    by_id = {p["id"]: p for p in posts}
    records = [{"posting_id": i, "posting_title": by_id[i].get("text", ""), "record": jobwatch.decide(by_id[i], resume)}
               for i in new_ids]
    state = {"ids": sorted(seen_today), "board": key, "run_id": ctx.run_id, "label": ctx.label,
             "written_at": time.strftime("%Y-%m-%dT%H:%M:%S%z")}
    target = policy.check_write(state_file)
    tmp = policy.check_write(state_file.with_name(state_file.name + ".tmp"))
    target.parent.mkdir(parents=True, exist_ok=True)
    tmp.write_text(json.dumps(state, indent=2), encoding="utf-8")
    tmp.replace(target)
    ctx.written.append(str(target))
    outcome = "ok" if posts else "ok_empty"
    b.update({"outcome": outcome, "posting_count": len(posts), "new_count": len(new_ids), "new_ids": new_ids,
              "records": records, "previous_state_file": previous_state_file, "state_file": str(target),
              "raw_file": str(body_path), "baseline": previous_state_file is None})
    ctx.observe("board_outcome", board=key, outcome=outcome, posting_count=len(posts), new_count=len(new_ids),
                state_file=str(target), previous_state_file=previous_state_file)


# ---------------------------------------------------------------- CLI
def _seed_state(a) -> int:
    """SEEDED set-up for the GATE section 7 demo: a state snapshot whose IDs come from a saved raw file. No network."""
    platform, slug, key = parse_board(a.board)
    src = policy.check_read(a.from_raw)
    body = src.read_bytes()
    ids = sorted({p["id"] for p in adapters.parse(platform, body)})
    out = Path(a.state_dir) / f"{key}.json"
    target = policy.check_write(out)
    target.parent.mkdir(parents=True, exist_ok=True)
    target.write_text(json.dumps({"ids": ids, "board": key, "label": a.label,
                                  "seeded_from": {"file": str(src), "sha256": hashlib.sha256(body).hexdigest()}}, indent=2),
                      encoding="utf-8")
    print(f"[seed-state] {a.label or ''} {key}: {len(ids)} ids from {src} -> {target}".replace("  ", " "))
    return 0


def main(argv=None, transport=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    sub = ap.add_subparsers(dest="cmd", required=True)
    r = sub.add_parser("run", help="one bounded run over the boards")
    r.add_argument("--board", action="append", help="platform:slug; repeatable. Default: the four GATE boards")
    for name in ("boards", "requests", "seconds"):
        r.add_argument(f"--max-{name}", type=int, help=f"lower the {name} budget (it cannot be raised)")
    r.add_argument("--approve", action="append", default=[], help="exact ROOT-relative path an overwrite is approved for")
    r.add_argument("--label", help="e.g. SEEDED; carried into the run id, filenames, trace and report")
    r.add_argument("--run-id")
    r.add_argument("--replay", action="append", default=[], help="platform:slug=PATH; serve this file instead of the network")
    for d in ("raw", "state", "runs", "traces"):
        r.add_argument(f"--{d}-dir", default=str(HERE / d))
    r.add_argument("--resume", default=str(HERE / "fixtures" / "resume.fictional.json"))
    s = sub.add_parser("seed-state", help="SEEDED: write a state snapshot from a saved raw file (no network)")
    s.add_argument("--board", required=True)
    s.add_argument("--from-raw", required=True)
    s.add_argument("--state-dir", required=True)
    s.add_argument("--label", default="SEEDED")
    a = ap.parse_args(argv)

    if a.cmd == "seed-state":
        try:
            return _seed_state(a)
        except (policy.PermissionRefused, ConfigRefused, adapters.FormatChanged) as e:
            print(f"[error] {e}", file=sys.stderr)
            return 2

    if a.replay:
        mapping = {}
        for item in a.replay:
            spec, _, path = item.partition("=")
            platform, slug, _key = parse_board(spec)
            mapping[normalize_url(adapters.board_url(platform, slug))] = Path(path)
        transport = replay_transport(mapping)
    rep = run_loop(a.board or DEFAULT_BOARDS, transport=transport, raw_dir=a.raw_dir, state_dir=a.state_dir,
                   runs_dir=a.runs_dir, traces_dir=a.traces_dir, resume_path=a.resume, max_boards=a.max_boards,
                   max_requests=a.max_requests, max_seconds=a.max_seconds, approve=a.approve, label=a.label, run_id=a.run_id)
    bud = rep.get("budgets") or {}
    tag = f"*** {rep['label']} *** " if rep.get("label") else ""
    print(f"[loop] {tag}status={rep['status']} exit={rep['exit_code']} boards={len(rep['boards'])} "
          f"requests={rep['requests_used']}/{bud.get('requests', MAX_REQUESTS)} seconds={rep['seconds_used']}/{bud.get('seconds', MAX_SECONDS)} "
          f"report={rep['report_file']}")
    for b in rep["boards"]:
        extra = (f"postings={b['posting_count']} new={b['new_count']}" if "posting_count" in b
                 else f"why={b.get('why_stopped', '-')}")
        print(f"  [board] {b['board']:45} {b['outcome'] or '-':16} attempts={b.get('attempts', 0)} {extra}")
    if rep.get("error"):
        print(f"[error] {rep['error']['type']}: {rep['error']['message']} (step: {rep['error']['step']})", file=sys.stderr)
    for e in rep["escalations"]:
        print(f"[escalation] {e['board']}: {e['reason']} evidence={e['evidence']}")
    if rep["status"] == "finished":
        print("[loop] finished is not 'correct': run  python -I verify.py " + str(rep["report_file"]))
    return rep["exit_code"]


if __name__ == "__main__":
    sys.exit(main())
