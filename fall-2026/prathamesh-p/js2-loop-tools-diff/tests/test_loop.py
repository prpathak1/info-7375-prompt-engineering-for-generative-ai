"""test_loop.py: tests for the JS2 bounded loop, written BEFORE any loop code, from GATE.md only.

GATE.md was APPROVED 2026-11-10 08:17:25 EST, with amendment A1 at 09:30:10 EST (`seeded/` readable).
Each test's docstring starts with EXPECTED, written before the test body and before any implementation exists.

Interface these tests fix (Claude Code's choice; GATE.md names no functions):

  adapters.py
    ALLOWED_HOSTS                         exactly {"api.lever.co", "boards-api.greenhouse.io", "api.ashbyhq.com"}  (GATE D-9)
    board_url(platform, slug) -> str      lever / greenhouse (?content=true) / ashby endpoints, as in GATE D-1
    parse(platform, body: bytes) -> list  one posting shape: {"id": str, "text": title, "descriptionPlain", "lists", "additionalPlain"}
    class FormatChanged(Exception)        raised for "200 but not JSON, or JSON without the platform's expected shape"

  loop.py
    MAX_BOARDS, MAX_REQUESTS, MAX_SECONDS, REQUEST_TIMEOUT, RETRY_DELAY, RETRY_AFTER_CAP   (GATE section 2 / section 4)
    EXIT_CODES = {"finished": 0, "error": 2, "incomplete": 3, "budget_exhausted": 4}
    Response(status, headers, body, final_url)                 what a transport returns
    class DNSFailure(OSError), class HostRefused(Exception)
    check_url(url)                                             3-host allow-list, https, port 443, no userinfo
    normalize_url(url) -> str                                  GATE D-7 normalization
    Ledger()  .permit(method, url, retry=False) -> bool, .sent, .refused   the repeat rule (GATE section 3)
    run_loop(boards, *, transport, raw_dir, state_dir, runs_dir, traces_dir, resume_path=..., max_boards=None,
             max_requests=None, max_seconds=None, approve=(), label=None, run_id=None, clock=..., sleep=...) -> report dict
    main(argv, transport=None) -> exit code
    transport(url, timeout) -> Response, or raises TimeoutError / ConnectionResetError / DNSFailure

  verify.py   (must not import jobwatch, loop, adapters or policy)
    python -I verify.py <run report>   exit 0 = PASS, 1 = FAIL, with reasons on stdout

Boards are written "platform:slug", for example "lever:zoox". The per-board key is "<platform>-<slug>", for example "lever-zoox".
"""
from __future__ import annotations

import json
import os
import re
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

GATE = (ROOT / "GATE.md").read_text(encoding="utf-8")


def _loop():
    import loop  # noqa: PLC0415   imported per test, so a missing module is reported per test
    return loop


def _adapters():
    import adapters  # noqa: PLC0415
    return adapters


# ---------------------------------------------------------------- fake bodies (constructed for tests; NOT real postings)
LEVER_BODY = json.dumps([
    {"id": "L1", "text": "Network Engineer", "descriptionPlain": "Operate BGP and OSPF; manage firewalls.", "lists": [], "additionalPlain": ""},
    {"id": "L2", "text": "Pastry Chef", "descriptionPlain": "Bake.", "lists": [], "additionalPlain": ""},
]).encode()
GH_BODY = json.dumps({"jobs": [
    {"id": 101, "title": "Senior Network Engineer", "content": "&lt;p&gt;Run BGP and OSPF.&lt;/p&gt;"},
    {"id": 102, "title": "Recruiter", "content": "&lt;p&gt;Hire people.&lt;/p&gt;"},
], "meta": {"total": 2}}).encode()
ASHBY_BODY = json.dumps({"jobs": [
    {"id": "a-1", "title": "Network Engineer", "descriptionPlain": "BGP, OSPF, VLAN."},
    {"id": "a-2", "title": "Designer", "descriptionPlain": "Figma."},
], "apiVersion": "1"}).encode()
ASHBY_EMPTY = json.dumps({"jobs": [], "apiVersion": "1"}).encode()

BOARDS3 = ["lever:zoox", "greenhouse:cloudflare", "ashby:openai"]
BAD = "greenhouse:cloudflare-js2-does-not-exist"


def url(board: str) -> str:
    platform, slug = board.split(":")
    return _adapters().board_url(platform, slug)


class FakeTransport:
    """script: {board: [Response | Exception | (status, headers, body[, final_url]), ...]}, consumed in order. It counts every call."""

    def __init__(self, script):
        self.script = {url(b): list(v) for b, v in script.items()}
        self.calls = []

    def __call__(self, u, timeout):
        self.calls.append(u)
        if u not in self.script or not self.script[u]:
            raise AssertionError(f"unexpected request {u}")
        item = self.script[u].pop(0)
        if isinstance(item, BaseException):
            raise item
        if isinstance(item, tuple):
            status, headers, body, *final = item
            return _loop().Response(status, headers, body, final[0] if final else u)
        return item


def ok(body):
    return (200, {}, body)


class Sandbox(unittest.TestCase):
    """Each test gets raw/state/runs/traces folders under ROOT/state/_test_tmp_<id>/ (writable and readable by GATE section 5); cleaned afterwards."""

    def setUp(self):
        (ROOT / "state").mkdir(exist_ok=True)
        self.box = Path(tempfile.mkdtemp(dir=ROOT / "state", prefix="_test_tmp_loop_"))
        self.dirs = {k: self.box / k for k in ("raw", "state", "runs", "traces")}
        for d in self.dirs.values():
            d.mkdir()
        self.sleeps = []

    def tearDown(self):
        shutil.rmtree(self.box, ignore_errors=True)
        try:
            (ROOT / "state").rmdir()
        except OSError:
            pass

    def run_loop(self, boards, transport, **kw):
        lp = _loop()
        kw.setdefault("sleep", self.sleeps.append)
        return lp.run_loop(boards, transport=transport, raw_dir=self.dirs["raw"], state_dir=self.dirs["state"],
                           runs_dir=self.dirs["runs"], traces_dir=self.dirs["traces"], **kw)

    def board(self, report, key):
        hits = [b for b in report["boards"] if b["board"] == key]
        self.assertEqual(len(hits), 1, f"{key} must appear once in report['boards']")
        return hits[0]

    def assert_no_invented_values(self, b):
        for k in ("posting_count", "new_count", "new_ids", "records"):
            self.assertNotIn(k, b, f"failed board {b['board']} must not report {k} (GATE section 4: no value is ever invented)")

    def saved_report(self, report):
        p = Path(report["report_file"])
        self.assertTrue(p.is_relative_to(self.dirs["runs"]), "report goes under runs/")
        self.assertRegex(p.name, rf"-{report['status']}\.json$", "GATE section 1: runs/<timestamp>-<status>.json")
        return json.loads(p.read_text(encoding="utf-8"))


# ================================================================ 1. Exits (GATE section 1)
class Exits(Sandbox):

    def test_E1_finished_exit_0_with_required_fields(self):
        """EXPECTED: three boards that answer 200 give status "finished", exit_code 0. Each board has outcome "ok", posting_count 2,
        new_count and records (a list); the report has requests_used 3, seconds_used (a number) and a verify reminder mentioning "verify.py".
        The saved runs/<...>-finished.json equals the returned report."""
        t = FakeTransport({"lever:zoox": [ok(LEVER_BODY)], "greenhouse:cloudflare": [ok(GH_BODY)], "ashby:openai": [ok(ASHBY_BODY)]})
        r = self.run_loop(BOARDS3, t)
        self.assertEqual((r["status"], r["exit_code"]), ("finished", 0))
        for key in ("lever-zoox", "greenhouse-cloudflare", "ashby-openai"):
            b = self.board(r, key)
            self.assertEqual(b["outcome"], "ok")
            self.assertEqual(b["posting_count"], 2)
            self.assertIn("new_count", b)
            self.assertIsInstance(b["records"], list)
        self.assertEqual(r["requests_used"], 3)
        self.assertIsInstance(r["seconds_used"], (int, float))
        self.assertIn("verify.py", r["verify_reminder"])
        self.assertEqual(self.saved_report(r), r)

    def test_E2_incomplete_exit_3_failed_board_fields_and_state_untouched(self):
        """EXPECTED: three ok boards plus the deliberate bad board answering 404 give "incomplete", exit 3 (W6: not "finished").
        The bad board has outcome "failed_http_404", error_type, http_status 404, attempts 1, and a why_stopped that mentions 404.
        It has NO posting_count, new_count, new_ids or records. Its pre-existing state file is byte-identical afterwards."""
        prev = self.dirs["state"] / "greenhouse-cloudflare-js2-does-not-exist.json"
        prev.write_text(json.dumps({"ids": ["keep-me"]}), encoding="utf-8")
        before = prev.read_bytes()
        t = FakeTransport({"lever:zoox": [ok(LEVER_BODY)], "greenhouse:cloudflare": [ok(GH_BODY)],
                           "ashby:openai": [ok(ASHBY_BODY)], BAD: [(404, {}, b'{"status":404,"error":"Job not found"}')]})
        r = self.run_loop(BOARDS3 + [BAD], t)
        self.assertEqual((r["status"], r["exit_code"]), ("incomplete", 3))
        b = self.board(r, "greenhouse-cloudflare-js2-does-not-exist")
        self.assertEqual(b["outcome"], "failed_http_404")
        self.assertEqual(b["http_status"], 404)
        self.assertEqual(b["attempts"], 1)
        self.assertIn("error_type", b)
        self.assertIn("404", b["why_stopped"])
        self.assert_no_invented_values(b)
        self.assertEqual(prev.read_bytes(), before, "the state of a failed board is untouched")
        self.assertEqual(self.saved_report(r)["status"], "incomplete")

    def test_E3_budget_exhausted_exit_4_names_budget_value_and_not_attempted(self):
        """EXPECTED: with max_requests=2 and three boards, the third request is not taken. Status "budget_exhausted", exit 4.
        budget == {"name": "requests", "value": 2}; not_attempted == ["ashby-openai"]; that board's outcome is "not_attempted",
        with no invented values; requests_used 2; the transport is called exactly 2 times."""
        t = FakeTransport({"lever:zoox": [ok(LEVER_BODY)], "greenhouse:cloudflare": [ok(GH_BODY)], "ashby:openai": [ok(ASHBY_BODY)]})
        r = self.run_loop(BOARDS3, t, max_requests=2)
        self.assertEqual((r["status"], r["exit_code"]), ("budget_exhausted", 4))
        self.assertEqual(r["budget"], {"name": "requests", "value": 2})
        self.assertEqual(r["not_attempted"], ["ashby-openai"])
        b = self.board(r, "ashby-openai")
        self.assertEqual(b["outcome"], "not_attempted")
        self.assert_no_invented_values(b)
        self.assertEqual((r["requests_used"], len(t.calls)), (2, 2))

    def test_E4_seconds_budget_checked_before_each_request(self):
        """EXPECTED: a fake clock that advances 70 s per request, with max_seconds=120. Request 1 happens at t=0 and request 2 at t=70.
        At t=140, before request 3, the seconds budget has run out: "budget_exhausted", budget name "seconds",
        not_attempted ["ashby-openai"], and exactly 2 calls."""
        now = [0.0]
        t = FakeTransport({"lever:zoox": [ok(LEVER_BODY)], "greenhouse:cloudflare": [ok(GH_BODY)], "ashby:openai": [ok(ASHBY_BODY)]})

        def slow(u, timeout):
            resp = t(u, timeout)
            now[0] += 70
            return resp
        r = self.run_loop(BOARDS3, slow, clock=lambda: now[0], max_seconds=120)
        self.assertEqual((r["status"], r["exit_code"]), ("budget_exhausted", 4))
        self.assertEqual(r["budget"]["name"], "seconds")
        self.assertEqual(r["not_attempted"], ["ashby-openai"])
        self.assertEqual(len(t.calls), 2)

    def test_E5_error_exit_2_off_host_final_url_stops_run_and_lists_written(self):
        """EXPECTED: board 1 is ok (its raw and state are written). Board 2's response has final_url https://evil.example/x (an off-host redirect).
        Status "error", exit 2. error.type "HostRefused"; error.step names "greenhouse-cloudflare"; error.written lists board 1's state file.
        Board 2 gets no state file. Board 3 is never requested (2 calls in total)."""
        t = FakeTransport({"lever:zoox": [ok(LEVER_BODY)], "greenhouse:cloudflare": [(200, {}, GH_BODY, "https://evil.example/x")],
                           "ashby:openai": [ok(ASHBY_BODY)]})
        r = self.run_loop(BOARDS3, t)
        self.assertEqual((r["status"], r["exit_code"]), ("error", 2))
        self.assertEqual(r["error"]["type"], "HostRefused")
        self.assertIn("greenhouse-cloudflare", r["error"]["step"])
        self.assertTrue(any(w.endswith("lever-zoox.json") for w in r["error"]["written"]), r["error"]["written"])
        self.assertFalse((self.dirs["state"] / "greenhouse-cloudflare.json").exists())
        self.assertEqual(len(t.calls), 2)

    def test_E6_error_exit_2_on_unexpected_exception(self):
        """EXPECTED: a transport raising ValueError("boom") (not a listed error type) gives "error", exit 2, error.type "ValueError",
        and error.message containing "boom". GATE section 4: any other exception means stop."""
        t = FakeTransport({"lever:zoox": [ValueError("boom")]})
        r = self.run_loop(["lever:zoox"], t)
        self.assertEqual((r["status"], r["exit_code"]), ("error", 2))
        self.assertEqual(r["error"]["type"], "ValueError")
        self.assertIn("boom", r["error"]["message"])

    def test_E7_ok_empty_counts_as_finished(self):
        """EXPECTED: a 200 with zero postings is outcome "ok_empty" with posting_count 0, and the run is "finished", exit 0.
        This is GATE D-4, on purpose: the agent does not second-guess it."""
        t = FakeTransport({"ashby:openai": [ok(ASHBY_EMPTY)]})
        r = self.run_loop(["ashby:openai"], t)
        self.assertEqual((r["status"], r["exit_code"]), ("finished", 0))
        b = self.board(r, "ashby-openai")
        self.assertEqual((b["outcome"], b["posting_count"]), ("ok_empty", 0))

    def test_E8_cli_prints_one_line_summary_and_returns_exit_code(self):
        """EXPECTED: loop.main([...]) with an injected transport returns 3 for the 404 case and prints one line containing "status=incomplete"."""
        import contextlib
        import io
        t = FakeTransport({BAD: [(404, {}, b"{}")]})
        buf = io.StringIO()
        with contextlib.redirect_stdout(buf):
            rc = _loop().main(["run", "--board", BAD, "--raw-dir", str(self.dirs["raw"]), "--state-dir", str(self.dirs["state"]),
                               "--runs-dir", str(self.dirs["runs"]), "--traces-dir", str(self.dirs["traces"])], transport=t)
        self.assertEqual(rc, 3)
        self.assertIn("status=incomplete", buf.getvalue())


# ================================================================ 2. Budgets (GATE section 2)
class Budgets(Sandbox):

    def test_B_1_constants_match_gate_table(self):
        """EXPECTED: the values parsed from the GATE section 2 table (boards 4, requests 6, seconds 120) and the per-request timeout (30 s),
        plus the section 4 retry delay (2 s) and Retry-After cap (10 s), equal loop's constants. If anyone changes either side alone, this fails (D-6)."""
        lp = _loop()
        def cell(label):
            m = re.search(rf"\|\s*{label}\s*\|\s*\*\*(\d+)\*\*", GATE)
            self.assertIsNotNone(m, f"GATE row {label!r} not found")
            return int(m.group(1))
        self.assertEqual(lp.MAX_BOARDS, cell("Max boards per run"))
        self.assertEqual(lp.MAX_REQUESTS, cell("Max HTTP requests per run"))
        self.assertEqual(lp.MAX_SECONDS, cell("Max wall-clock seconds per run"))
        self.assertEqual(lp.REQUEST_TIMEOUT, int(re.search(r"Per-request timeout is \*\*(\d+) s\*\*", GATE).group(1)))
        self.assertEqual(lp.RETRY_DELAY, 2)
        self.assertEqual(lp.RETRY_AFTER_CAP, 10)

    def test_B_2_more_than_max_boards_refused_before_any_request(self):
        """EXPECTED: five distinct boards (more than 4) give "error", exit 2, with zero transport calls."""
        boards = BOARDS3 + [BAD, "lever:another-board"]
        t = FakeTransport({})
        r = self.run_loop(boards, t)
        self.assertEqual((r["status"], r["exit_code"]), ("error", 2))
        self.assertEqual(t.calls, [])

    def test_B_3_cli_flag_cannot_raise_a_budget(self):
        """EXPECTED: --max-requests 7, --max-boards 5 or --max-seconds 121 (each above GATE) returns 2 with zero transport calls."""
        for flag, val in (("--max-requests", "7"), ("--max-boards", "5"), ("--max-seconds", "121")):
            t = FakeTransport({})
            with self.subTest(flag=flag):
                rc = _loop().main(["run", "--board", "lever:zoox", flag, val, "--raw-dir", str(self.dirs["raw"]),
                                   "--state-dir", str(self.dirs["state"]), "--runs-dir", str(self.dirs["runs"]),
                                   "--traces-dir", str(self.dirs["traces"])], transport=t)
                self.assertEqual(rc, 2)
                self.assertEqual(t.calls, [])

    def test_B_4_cli_flag_can_lower_a_budget(self):
        """EXPECTED: --max-requests 1 with two boards gives exit 4 (budget_exhausted) after exactly 1 call."""
        t = FakeTransport({"lever:zoox": [ok(LEVER_BODY)], "ashby:openai": [ok(ASHBY_BODY)]})
        rc = _loop().main(["run", "--board", "lever:zoox", "--board", "ashby:openai", "--max-requests", "1",
                           "--raw-dir", str(self.dirs["raw"]), "--state-dir", str(self.dirs["state"]),
                           "--runs-dir", str(self.dirs["runs"]), "--traces-dir", str(self.dirs["traces"])], transport=t)
        self.assertEqual(rc, 4)
        self.assertEqual(len(t.calls), 1)

    def test_B_5_default_boards_are_the_gate_four(self):
        """EXPECTED: with no --board, the CLI uses exactly the GATE D-1 boards plus the D-12 deliberate failure, in this order:
        lever:zoox, greenhouse:cloudflare, ashby:openai, greenhouse:cloudflare-js2-does-not-exist."""
        self.assertEqual(_loop().DEFAULT_BOARDS, BOARDS3 + [BAD])


# ================================================================ 3. Repeat rule (GATE section 3)
class RepeatRule(Sandbox):

    def test_R_1_normalize_url(self):
        """EXPECTED: scheme and host lower-cased, default port dropped, query parameters sorted, fragment removed. Every variant below
        normalizes to the same string as the canonical one."""
        lp = _loop()
        canon = lp.normalize_url("https://api.lever.co/v0/postings/zoox?a=1&mode=json")
        for v in ("HTTPS://API.LEVER.CO/v0/postings/zoox?mode=json&a=1", "https://api.lever.co:443/v0/postings/zoox?a=1&mode=json",
                  "https://api.lever.co/v0/postings/zoox?mode=json&a=1#frag"):
            with self.subTest(v=v):
                self.assertEqual(lp.normalize_url(v), canon)
        self.assertNotEqual(lp.normalize_url("https://api.lever.co/v0/postings/ZOOX?mode=json"), canon, "the path is not lower-cased")

    def test_R_2_ledger_refuses_repeat_allows_one_retry(self):
        """EXPECTED: permit(GET, u) gives True. A second permit of an equivalent URL without retry gives False, is recorded in .refused and not counted in .sent.
        permit(retry=True) gives True once; a second retry of the same action gives False. sent == 2 at the end."""
        lp = _loop()
        led = lp.Ledger()
        u = "https://api.lever.co/v0/postings/zoox?mode=json"
        self.assertTrue(led.permit("GET", u))
        self.assertFalse(led.permit("GET", "HTTPS://api.lever.co:443/v0/postings/zoox?mode=json"))
        self.assertEqual(len(led.refused), 1)
        self.assertTrue(led.permit("GET", u, retry=True))
        self.assertFalse(led.permit("GET", u, retry=True))
        self.assertEqual(led.sent, 2)

    def test_R_3_duplicate_board_collapsed_and_logged(self):
        """EXPECTED: boards ["lever:zoox", "LEVER:zoox"] are collapsed to one. There is exactly 1 call and 1 board in the report,
        and the trace has an observation of kind "collapsed"."""
        t = FakeTransport({"lever:zoox": [ok(LEVER_BODY)]})
        r = self.run_loop(["lever:zoox", "LEVER:zoox"], t)
        self.assertEqual(len(t.calls), 1)
        self.assertEqual(len(r["boards"]), 1)
        trace = [json.loads(x) for x in Path(r["trace_file"]).read_text(encoding="utf-8").splitlines()]
        self.assertTrue(any(o["kind"] == "collapsed" for o in trace))

    def test_R_4_trace_has_every_request_and_outcome(self):
        """EXPECTED: the trace (traces/<run_id>.jsonl, under traces_dir) is JSON lines. The number of "request" observations equals the transport
        call count (here 3: a 503, its retry, and one ok), and every board has one "board_outcome" observation."""
        t = FakeTransport({"lever:zoox": [(503, {}, b"busy"), ok(LEVER_BODY)], "ashby:openai": [ok(ASHBY_BODY)]})
        r = self.run_loop(["lever:zoox", "ashby:openai"], t)
        p = Path(r["trace_file"])
        self.assertTrue(p.is_relative_to(self.dirs["traces"]))
        trace = [json.loads(x) for x in p.read_text(encoding="utf-8").splitlines()]
        self.assertEqual(sum(o["kind"] == "request" for o in trace), len(t.calls))
        self.assertEqual(sorted(o["board"] for o in trace if o["kind"] == "board_outcome"), ["ashby-openai", "lever-zoox"])


# ================================================================ 4. Error policy (GATE section 4), W5
class ErrorPolicy(Sandbox):

    def outcome(self, script_items, board="lever:zoox"):
        t = FakeTransport({board: script_items})
        r = self.run_loop([board], t)
        return r, self.board(r, board.replace(":", "-")), t

    def test_P_1_404_no_retry(self):
        """EXPECTED (W5): 404 gives exactly 1 call, outcome failed_http_404, no sleep, run incomplete/3, no invented values."""
        r, b, t = self.outcome([(404, {}, b"{}")])
        self.assertEqual((len(t.calls), b["outcome"], r["exit_code"]), (1, "failed_http_404", 3))
        self.assertEqual(self.sleeps, [])
        self.assert_no_invented_values(b)

    def test_P_2_410_no_retry(self):
        """EXPECTED: 410 gives exactly 1 call and outcome failed_http_410 (D-3 names outcomes failed_http_<code>)."""
        r, b, t = self.outcome([(410, {}, b"{}")])
        self.assertEqual((len(t.calls), b["outcome"]), (1, "failed_http_410"))

    def test_P_3_5xx_one_retry_then_fail(self):
        """EXPECTED (W5): for each of 500, 502, 503 and 504, the code repeated twice gives exactly 2 calls, outcome failed_http_<code>,
        one sleep of 2 s, and attempts == 2."""
        for code in (500, 502, 503, 504):
            self.sleeps.clear()
            with self.subTest(code=code):
                r, b, t = self.outcome([(code, {}, b"x"), (code, {}, b"x")])
                self.assertEqual((len(t.calls), b["outcome"], b["attempts"]), (2, f"failed_http_{code}", 2))
                self.assertEqual(self.sleeps, [2])

    def test_P_4_503_then_ok_recovers(self):
        """EXPECTED: 503 followed by 200 gives 2 calls, outcome ok, and run finished/0."""
        r, b, t = self.outcome([(503, {}, b"x"), ok(LEVER_BODY)])
        self.assertEqual((len(t.calls), b["outcome"], r["exit_code"]), (2, "ok", 0))

    def test_P_5_429_retry_after_honoured_up_to_10s(self):
        """EXPECTED: 429 with Retry-After: 5, then 200, gives a sleep of 5 s and 2 calls. 429 with Retry-After: 30 (>10) gives NO retry,
        1 call, and outcome failed_http_429."""
        r, b, t = self.outcome([(429, {"Retry-After": "5"}, b"x"), ok(LEVER_BODY)])
        self.assertEqual((self.sleeps, len(t.calls), b["outcome"]), ([5], 2, "ok"))
        self.sleeps.clear()
        r, b, t = self.outcome([(429, {"Retry-After": "30"}, b"x")])
        self.assertEqual((self.sleeps, len(t.calls), b["outcome"]), ([], 1, "failed_http_429"))

    def test_P_6_timeout_and_reset_one_retry(self):
        """EXPECTED: TimeoutError twice gives 2 calls and failed_timeout. ConnectionResetError twice gives 2 calls and failed_network.
        A timeout then 200 gives ok. Every retry sleeps 2 s."""
        r, b, t = self.outcome([TimeoutError("t"), TimeoutError("t")])
        self.assertEqual((len(t.calls), b["outcome"]), (2, "failed_timeout"))
        r, b, t = self.outcome([ConnectionResetError("r"), ConnectionResetError("r")])
        self.assertEqual((len(t.calls), b["outcome"]), (2, "failed_network"))
        r, b, t = self.outcome([TimeoutError("t"), ok(LEVER_BODY)])
        self.assertEqual((len(t.calls), b["outcome"]), (2, "ok"))
        self.assertTrue(all(s == 2 for s in self.sleeps))

    def test_P_7_dns_no_retry(self):
        """EXPECTED: DNSFailure gives exactly 1 call and failed_network."""
        r, b, t = self.outcome([_loop().DNSFailure("no such host")])
        self.assertEqual((len(t.calls), b["outcome"]), (1, "failed_network"))

    def test_P_8_401_403_escalate_no_retry(self):
        """EXPECTED: 401 and 403 each give 1 call, outcome "escalated", and an entry in report["escalations"] naming the board,
        with an "evidence" path that exists. Run incomplete/3."""
        for code in (401, 403):
            with self.subTest(code=code):
                r, b, t = self.outcome([(code, {}, b"denied")])
                self.assertEqual((len(t.calls), b["outcome"], r["exit_code"]), (1, "escalated", 3))
                esc = [e for e in r["escalations"] if e["board"] == "lever-zoox"]
                self.assertEqual(len(esc), 1)
                self.assertTrue(Path(esc[0]["evidence"]).exists())

    def test_P_9_login_redirect_on_allowed_host_escalates(self):
        """EXPECTED: a 200 whose final_url is https://api.lever.co/login gives escalated, 1 call, and no posting_count."""
        r, b, t = self.outcome([(200, {}, b"<html>login</html>", "https://api.lever.co/login")])
        self.assertEqual((len(t.calls), b["outcome"]), (1, "escalated"))
        self.assert_no_invented_values(b)

    def test_P_10_format_change_escalates_and_raw_kept_unparsed(self):
        """EXPECTED: a 200 non-JSON body gives escalated, 1 call. The raw body is saved (the escalation's evidence file exists, holds
        exactly those bytes, and its name ends ".body", not ".json"), with no invented values. A 200 Greenhouse body that is a JSON list,
        not {"jobs": [...]}, also gives escalated."""
        r, b, t = self.outcome([(200, {}, b"<html>not json</html>")])
        self.assertEqual((len(t.calls), b["outcome"]), (1, "escalated"))
        ev = Path(r["escalations"][0]["evidence"])
        self.assertEqual(ev.read_bytes(), b"<html>not json</html>")
        self.assertTrue(ev.name.endswith(".body"))
        self.assert_no_invented_values(b)
        r, b, t = self.outcome([(200, {}, b"[]")], board="greenhouse:cloudflare")
        self.assertEqual(b["outcome"], "escalated")

    def test_P_11_request_budget_never_exceeded_by_retries(self):
        """EXPECTED (W5): four boards that each answer 503 twice would want 8 requests. Exactly 6 calls happen, then budget_exhausted/4,
        and requests_used == 6."""
        boards = BOARDS3 + [BAD]
        t = FakeTransport({b: [(503, {}, b"x"), (503, {}, b"x")] for b in boards})
        r = self.run_loop(boards, t)
        self.assertEqual((len(t.calls), r["requests_used"], r["status"]), (6, 6, "budget_exhausted"))

    def test_P_12_raw_saved_for_every_attempt_with_hash(self):
        """EXPECTED: each attempt's body is saved under raw_dir/<day>/ with a .fetch.txt holding http_status and a sha256 equal to the
        SHA-256 of the saved bytes. A 503 then 200 gives 2 bodies and 2 fetch.txt files."""
        import hashlib
        r, b, t = self.outcome([(503, {}, b"busy"), ok(LEVER_BODY)])
        metas = sorted(self.dirs["raw"].rglob("*.fetch.txt"))
        self.assertEqual(len(metas), 2)
        for m in metas:
            kv = dict(line.split("=", 1) for line in m.read_text(encoding="utf-8").splitlines() if "=" in line)
            body = m.with_name(kv["file"])
            self.assertEqual(hashlib.sha256(body.read_bytes()).hexdigest(), kv["sha256"])
            self.assertIn(kv["http_status"], ("503", "200"))


# ================================================================ 5. Permissions and hosts (GATE section 5), W3, W4, W8, B1, B2, B13
class Permissions(Sandbox):

    def test_H_1_allowed_hosts_exactly_gate(self):
        """EXPECTED: adapters.ALLOWED_HOSTS == {"api.lever.co", "boards-api.greenhouse.io", "api.ashbyhq.com"}, and the board URLs match GATE D-1."""
        a = _adapters()
        self.assertEqual(set(a.ALLOWED_HOSTS), {"api.lever.co", "boards-api.greenhouse.io", "api.ashbyhq.com"})
        self.assertEqual(a.board_url("lever", "zoox"), "https://api.lever.co/v0/postings/zoox?mode=json")
        self.assertEqual(a.board_url("greenhouse", "cloudflare"), "https://boards-api.greenhouse.io/v1/boards/cloudflare/jobs?content=true")
        self.assertEqual(a.board_url("ashby", "openai"), "https://api.ashbyhq.com/posting-api/job-board/openai")

    def test_H_2_B1_B2_check_url_refusals(self):
        """EXPECTED: HostRefused for example.com (B1), the lookalike api.lever.co.evil.example (B2), http://, userinfo, and port 8443.
        Each allowed host on https, with or without :443, passes."""
        lp = _loop()
        for bad in ("https://example.com/jobs", "https://api.lever.co.evil.example/v0/postings/zoox", "http://api.lever.co/v0/postings/zoox",
                    "https://user@api.lever.co/v0/postings/zoox", "https://api.lever.co:8443/v0/postings/zoox"):
            with self.subTest(bad=bad), self.assertRaises(lp.HostRefused):
                lp.check_url(bad)
        for good in ("https://api.lever.co/x", "https://boards-api.greenhouse.io:443/x", "https://api.ashbyhq.com/x"):
            lp.check_url(good)

    def test_H_3_W8_redirect_handler_refuses_off_host_for_all_three(self):
        """EXPECTED (W8): the real transport's redirect handler (loop._AllowListRedirects) raises HostRefused for a redirect from each
        allowed host to https://evil.example/, before following it."""
        import urllib.request
        lp = _loop()
        h = lp._AllowListRedirects()
        for host in ("api.lever.co", "boards-api.greenhouse.io", "api.ashbyhq.com"):
            req = urllib.request.Request(f"https://{host}/x", method="GET")
            with self.subTest(host=host), self.assertRaises(lp.HostRefused):
                h.redirect_request(req, None, 302, "Found", {}, "https://evil.example/")

    def test_H_4_W3_sibling_prefix_dir_refused_before_any_request(self):
        """EXPECTED (W3): state_dir = ROOT/state-evil (a sibling-prefix folder) gives "error", exit 2, with zero calls; the folder is not created."""
        t = FakeTransport({"lever:zoox": [ok(LEVER_BODY)]})
        lp = _loop()
        evil = ROOT / f"state-evil-{uuid.uuid4().hex[:6]}"
        r = lp.run_loop(["lever:zoox"], transport=t, raw_dir=self.dirs["raw"], state_dir=evil, runs_dir=self.dirs["runs"],
                        traces_dir=self.dirs["traces"], sleep=self.sleeps.append)
        self.assertEqual((r["status"], r["exit_code"], t.calls), ("error", 2, []))
        self.assertFalse(evil.exists())

    @unittest.skipUnless(os.name == "nt", "directory junctions are Windows-only")
    def test_H_5_W4_junction_raw_dir_refused_before_any_request(self):
        """EXPECTED (W4): raw_dir = a junction under the sandbox pointing outside ROOT gives "error", exit 2, zero calls, and an empty
        target. (A true symlink is not tested; it needs admin or Developer Mode here.)"""
        target = Path(tempfile.mkdtemp(prefix="js2-loop-junction-"))
        link = self.box / "rawlink"
        try:
            subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], check=True, capture_output=True)
            t = FakeTransport({"lever:zoox": [ok(LEVER_BODY)]})
            lp = _loop()
            r = lp.run_loop(["lever:zoox"], transport=t, raw_dir=link, state_dir=self.dirs["state"], runs_dir=self.dirs["runs"],
                            traces_dir=self.dirs["traces"], sleep=self.sleeps.append)
            self.assertEqual((r["status"], r["exit_code"], t.calls), ("error", 2, []))
            self.assertEqual(os.listdir(target), [])
        finally:
            if os.path.lexists(link):
                os.rmdir(link)
            shutil.rmtree(target, ignore_errors=True)

    def test_H_6_B13_static_no_send_paths(self):
        """EXPECTED (B13): loop.py and adapters.py contain no POST/PUT/PATCH/DELETE method, no Authorization or Cookie header, no smtplib,
        and no http.client. Every `method=` in loop.py is "GET". loop.py has exactly one `urlopen(` call site."""
        for name in ("loop.py", "adapters.py"):
            src = (ROOT / name).read_text(encoding="utf-8")
            for bad in ('"POST"', "'POST'", '"PUT"', '"PATCH"', '"DELETE"', "Authorization", "Cookie", "smtplib", "http.client"):
                with self.subTest(file=name, bad=bad):
                    self.assertNotIn(bad, src)
        src = (ROOT / "loop.py").read_text(encoding="utf-8")
        self.assertEqual(set(re.findall(r"method=['\"](\w+)['\"]", src)), {"GET"})
        self.assertEqual(src.count("urlopen("), 1)

    def test_H_7_reads_go_through_check_read(self):
        """EXPECTED (step-6 follow-up): resume_path = a fictional résumé copied OUTSIDE the project gives "error", exit 2, zero calls,
        and an error message containing "read refused"."""
        fd, name = tempfile.mkstemp(suffix=".json", prefix="js2-resume-outside-")
        os.close(fd)
        try:
            shutil.copyfile(ROOT / "fixtures" / "resume.fictional.json", name)
            t = FakeTransport({"lever:zoox": [ok(LEVER_BODY)]})
            r = self.run_loop(["lever:zoox"], t, resume_path=name)
            self.assertEqual((r["status"], r["exit_code"], t.calls), ("error", 2, []))
            self.assertIn("read refused", r["error"]["message"])
        finally:
            os.unlink(name)

    def test_H_8_approve_only_exact_path(self):
        """EXPECTED (step-6 follow-up; GATE B10/B11 at loop level): with a fixed run_id, the raw path for attempt 1 already exists under
        ROOT/raw/_test_tmp_*/. Without approve: "error", exit 2, zero calls, and the file is unchanged. With approve naming a DIFFERENT path:
        the same. With approve = the exact ROOT-relative path: the run proceeds (1 call) and the file is overwritten with the new body."""
        lp = _loop()
        rawbox = Path(tempfile.mkdtemp(dir=ROOT / "raw", prefix="_test_tmp_approve_"))
        try:
            rid = "TESTAPPROVE-" + uuid.uuid4().hex[:6]
            target = lp.raw_path(rawbox, lp.today(), "lever-zoox", rid, 1, ".json")
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_bytes(b"OLD")
            rel = target.resolve().relative_to(ROOT.resolve()).as_posix()
            for approve in ((), ("raw/some/other/file.json",)):
                t = FakeTransport({"lever:zoox": [ok(LEVER_BODY)]})
                r = lp.run_loop(["lever:zoox"], transport=t, raw_dir=rawbox, state_dir=self.dirs["state"], runs_dir=self.dirs["runs"],
                                traces_dir=self.dirs["traces"], run_id=rid, approve=approve, sleep=self.sleeps.append)
                with self.subTest(approve=approve):
                    self.assertEqual((r["status"], r["exit_code"], t.calls), ("error", 2, []))
                    self.assertEqual(target.read_bytes(), b"OLD")
            t = FakeTransport({"lever:zoox": [ok(LEVER_BODY)]})
            r = lp.run_loop(["lever:zoox"], transport=t, raw_dir=rawbox, state_dir=self.dirs["state"], runs_dir=self.dirs["runs"],
                            traces_dir=self.dirs["traces"], run_id=rid, approve=(rel,), sleep=self.sleeps.append)
            self.assertEqual(len(t.calls), 1)
            self.assertEqual(target.read_bytes(), LEVER_BODY)
        finally:
            shutil.rmtree(rawbox, ignore_errors=True)

    def test_H_9_seeded_folder_is_readable_not_writable(self):
        """EXPECTED (amendment A1): policy.check_read(ROOT/seeded/SEEDED-openai-empty.json) is allowed; check_write on the same path is refused."""
        import policy
        p = ROOT / "seeded" / "SEEDED-openai-empty.json"
        self.assertEqual(Path(policy.check_read(p)), p.resolve())
        with self.assertRaises(policy.PermissionRefused):
            policy.check_write(p)


# ================================================================ 6. Adapters, state and records
class AdaptersAndState(Sandbox):

    def test_A_1_parse_real_saved_raw_counts(self):
        """EXPECTED: parsing the REAL saved captures raw/2026-11-10/{zoox,cloudflare,openai}.json gives 234, 466 and 826 postings
        (FRICTIONAL F4). Every posting has a str id, a str text, and a str descriptionPlain."""
        a = _adapters()
        for platform, name, n in (("lever", "zoox", 234), ("greenhouse", "cloudflare", 466), ("ashby", "openai", 826)):
            posts = a.parse(platform, (ROOT / "raw" / "2026-11-10" / f"{name}.json").read_bytes())
            with self.subTest(name=name):
                self.assertEqual(len(posts), n)
                for p in posts:
                    self.assertIsInstance(p["id"], str)
                    self.assertIsInstance(p["text"], str)
                    self.assertIsInstance(p["descriptionPlain"], str)

    def test_A_2_greenhouse_content_unescaped_and_stripped(self):
        """EXPECTED: the Greenhouse content "&lt;p&gt;Run BGP and OSPF.&lt;/p&gt;" becomes descriptionPlain "Run BGP and OSPF." (no tags), and id 101 becomes "101"."""
        p = _adapters().parse("greenhouse", GH_BODY)[0]
        self.assertEqual((p["id"], p["descriptionPlain"]), ("101", "Run BGP and OSPF."))

    def test_A_3_format_changed(self):
        """EXPECTED: FormatChanged for non-JSON, for Greenhouse/Ashby bodies without a "jobs" list, for Lever bodies that are not a list,
        and for a posting without an id."""
        a = _adapters()
        for platform, body in (("lever", b"<html>"), ("lever", b"{}"), ("greenhouse", b"[]"), ("ashby", b'{"x": 1}'),
                               ("ashby", b'{"jobs": [{"title": "no id"}]}')):
            with self.subTest(platform=platform, body=body), self.assertRaises(a.FormatChanged):
                a.parse(platform, body)

    def test_A_4_baseline_then_new_ids_with_records(self):
        """EXPECTED: run 1 (no state) gives new_count 0 (baseline, as in JS1) and writes state with ids {L1, L2}. Run 2, whose body adds L3
        ("Senior Network Engineer", BGP and OSPF), gives new_ids ["L3"] and one record whose posting_id is "L3" and whose label is "record".
        previous_state_file points to a snapshot holding {L1, L2}."""
        body2 = json.dumps(json.loads(LEVER_BODY) + [{"id": "L3", "text": "Senior Network Engineer",
                                                      "descriptionPlain": "BGP and OSPF and firewalls.", "lists": [], "additionalPlain": ""}]).encode()
        t = FakeTransport({"lever:zoox": [ok(LEVER_BODY), ok(body2)]})
        r1 = self.run_loop(["lever:zoox"], t)
        b1 = self.board(r1, "lever-zoox")
        self.assertEqual(b1["new_count"], 0)
        self.assertEqual(set(json.loads((self.dirs["state"] / "lever-zoox.json").read_text(encoding="utf-8"))["ids"]), {"L1", "L2"})
        t.calls.clear()
        r2 = _loop().run_loop(["lever:zoox"], transport=t, raw_dir=self.dirs["raw"], state_dir=self.dirs["state"],
                              runs_dir=self.dirs["runs"], traces_dir=self.dirs["traces"], sleep=self.sleeps.append)
        b2 = self.board(r2, "lever-zoox")
        self.assertEqual(b2["new_ids"], ["L3"])
        self.assertEqual([x["posting_id"] for x in b2["records"]], ["L3"])
        self.assertEqual(b2["records"][0]["record"]["label"], "record")
        prev = json.loads(Path(b2["previous_state_file"]).read_text(encoding="utf-8"))
        self.assertEqual(set(prev["ids"]), {"L1", "L2"})

    def test_A_5_seeded_label_everywhere(self):
        """EXPECTED: label="SEEDED" puts "SEEDED" in report["label"], at the start of run_id, in the report filename, in every raw filename,
        and on every trace observation."""
        t = FakeTransport({"ashby:openai": [ok(ASHBY_EMPTY)]})
        r = self.run_loop(["ashby:openai"], t, label="SEEDED")
        self.assertEqual(r["label"], "SEEDED")
        self.assertTrue(r["run_id"].startswith("SEEDED"))
        self.assertIn("SEEDED", Path(r["report_file"]).name)
        self.assertTrue(all("SEEDED" in p.name for p in self.dirs["raw"].rglob("*") if p.is_file()))
        trace = [json.loads(x) for x in Path(r["trace_file"]).read_text(encoding="utf-8").splitlines()]
        self.assertTrue(trace and all(o.get("label") == "SEEDED" for o in trace))


# ================================================================ 7. verify.py (GATE section 7), W7
class Verify(Sandbox):

    def verify(self, report):
        return subprocess.run([sys.executable, "-I", str(ROOT / "verify.py"), report["report_file"]], cwd=ROOT,
                              capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120)

    def seed_state(self, key, ids):
        (self.dirs["state"] / f"{key}.json").write_text(json.dumps({"ids": ids}), encoding="utf-8")

    def test_V_1_static_independence(self):
        """EXPECTED: verify.py imports none of jobwatch, loop, adapters or policy."""
        src = (ROOT / "verify.py").read_text(encoding="utf-8")
        for mod in ("jobwatch", "loop", "adapters", "policy"):
            with self.subTest(mod=mod):
                self.assertIsNone(re.search(rf"^\s*(import|from)\s+{mod}\b", src, re.M))

    def test_V_2_W7_seeded_empty_finished_run_fails(self):
        """EXPECTED (W7): the previous snapshot has 3 openai ids, and the SEEDED day-2 run gets {"jobs": []}. The agent says finished/0
        with ok_empty, and verify.py exits 1 with stdout naming "ashby-openai", "0" and "3"."""
        self.seed_state("ashby-openai", ["a-1", "a-2", "a-3"])
        t = FakeTransport({"ashby:openai": [ok(ASHBY_EMPTY)]})
        r = self.run_loop(["ashby:openai"], t, label="SEEDED")
        self.assertEqual((r["status"], r["exit_code"]), ("finished", 0))
        v = self.verify(r)
        self.assertEqual(v.returncode, 1, v.stdout + v.stderr)
        self.assertIn("FAIL", v.stdout)
        self.assertIn("ashby-openai", v.stdout)
        self.assertRegex(v.stdout, r"\b0\b.*\b3\b|\b3\b.*\b0\b")

    def test_V_3_honest_run_passes(self):
        """EXPECTED: previous snapshot {a-1, a-2} and today's body {a-1, a-2} give finished, and verify.py exits 0 with "PASS"."""
        self.seed_state("ashby-openai", ["a-1", "a-2"])
        r = self.run_loop(["ashby:openai"], FakeTransport({"ashby:openai": [ok(ASHBY_BODY)]}))
        v = self.verify(r)
        self.assertEqual(v.returncode, 0, v.stdout + v.stderr)
        self.assertIn("PASS", v.stdout)

    def test_V_4_report_disagreeing_with_raw_fails(self):
        """EXPECTED: an honest run whose saved report is then edited (posting_count 2 changed to 5) makes verify.py exit 1 and name "posting_count"."""
        r = self.run_loop(["ashby:openai"], FakeTransport({"ashby:openai": [ok(ASHBY_BODY)]}))
        p = Path(r["report_file"])
        rep = json.loads(p.read_text(encoding="utf-8"))
        rep["boards"][0]["posting_count"] = 5
        p.write_text(json.dumps(rep), encoding="utf-8")
        v = self.verify(r)
        self.assertEqual(v.returncode, 1)
        self.assertIn("posting_count", v.stdout)

    def test_V_5_raw_hash_mismatch_fails(self):
        """EXPECTED: an honest run whose saved raw body is then altered makes verify.py exit 1 and name "sha256"."""
        r = self.run_loop(["ashby:openai"], FakeTransport({"ashby:openai": [ok(ASHBY_BODY)]}))
        body = next(p for p in self.dirs["raw"].rglob("*.json"))
        body.write_bytes(body.read_bytes() + b" ")
        v = self.verify(r)
        self.assertEqual(v.returncode, 1)
        self.assertIn("sha256", v.stdout)

    def test_V_6_drop_over_50_percent_fails(self):
        """EXPECTED: a previous snapshot of 5 ids and today's 2 postings (a 60% drop) make verify.py exit 1 and name "50%"."""
        self.seed_state("ashby-openai", ["a-1", "a-2", "x-3", "x-4", "x-5"])
        r = self.run_loop(["ashby:openai"], FakeTransport({"ashby:openai": [ok(ASHBY_BODY)]}))
        v = self.verify(r)
        self.assertEqual(v.returncode, 1)
        self.assertIn("50%", v.stdout)

    def test_V_7_invented_value_on_failed_board_fails(self):
        """EXPECTED: a 404 run whose report is edited to give the failed board a posting_count makes verify.py exit 1 and name "invented"."""
        r = self.run_loop([BAD], FakeTransport({BAD: [(404, {}, b"{}")]}))
        p = Path(r["report_file"])
        rep = json.loads(p.read_text(encoding="utf-8"))
        rep["boards"][0]["posting_count"] = 0
        p.write_text(json.dumps(rep), encoding="utf-8")
        v = self.verify(r)
        self.assertEqual(v.returncode, 1)
        self.assertIn("invented", v.stdout)


if __name__ == "__main__":
    unittest.main(verbosity=2)
