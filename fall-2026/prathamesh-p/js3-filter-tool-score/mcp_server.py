"""A from-scratch, read-only MCP-style tool server (JS3, Chapter 8). Python standard library only.

Transport: newline-delimited JSON-RPC 2.0 over stdio (one JSON object per line; stdout carries protocol only,
diagnostics go to stderr). Methods: initialize, notifications/initialized, ping, tools/list, tools/call.

One capability: score_posting(board, posting_id). It returns the FILTER v0.3 decision and the 4 evidence-labelled
claims for ONE posting already stored under raw/. It makes no network calls, and it never writes except its own
transcript under transcripts/ in this folder. It never applies, emails, messages or logs in.

  python -I mcp_server.py            (a client starts it; it reads stdin until EOF)
"""
import datetime
import json
import os
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
sys.path.insert(0, str(HERE))
import filter as flt  # noqa: E402
import postings  # noqa: E402

SERVER_INFO = {"name": "js3-score-posting", "version": "0.3.0"}   # transcripts of 2026-11-25 19:14 were captured at 0.2.0 (FILTER v0.2)
PROTOCOL_VERSIONS = ["2025-11-25", "2025-06-18", "2025-03-26", "2024-11-05"]   # newest first
MAX_LINE = 64 * 1024
BOARD_RE = re.compile(r"^[a-z0-9][a-z0-9-]{0,63}$")
ID_RE = re.compile(r"^[A-Za-z0-9][A-Za-z0-9-]{0,63}$")
TOOL = {
    "name": "score_posting",
    "title": "Score one stored job posting",
    "description": ("Read-only. Returns the JS3 filter (FILTER.md v0.3) decision for ONE job posting already saved on disk: "
                    "outcome (accept/reject/flag/abstain), the deciding rule, and four claims (title, authorization, "
                    "seniority, skills) each labelled supported/contradicted/insufficient with an exact quote. "
                    "No network access. The only write is the server's own message log in its transcripts/ folder; it "
                    "changes no posting, file or account. The decision is evidence, not advice to apply."),
    "inputSchema": {"type": "object", "additionalProperties": False, "required": ["board", "posting_id"],
                    "properties": {"board": {"type": "string", "pattern": BOARD_RE.pattern,
                                             "description": "board slug, e.g. openai, cloudflare, zoox"},
                                   "posting_id": {"type": "string", "pattern": ID_RE.pattern,
                                                  "description": "the posting id as stored by the board"}}},
    "annotations": {"readOnlyHint": True, "destructiveHint": False, "idempotentHint": True, "openWorldHint": False},
}


class Transcript:
    def __init__(self):
        d = HERE / "transcripts"
        d.mkdir(exist_ok=True)
        ts = datetime.datetime.now().strftime("%Y%m%dT%H%M%S")
        self.path = d / f"server-{ts}-{os.getpid()}.jsonl"
        self.f = self.path.open("a", encoding="utf-8")

    def log(self, direction, payload):
        self.f.write(json.dumps({"t": datetime.datetime.now().astimezone().isoformat(timespec="milliseconds"),
                                 "dir": direction, "msg": payload}, ensure_ascii=False) + "\n")
        self.f.flush()


_INDEX = None


def index():
    global _INDEX
    if _INDEX is None:
        _INDEX = {(r["board"], r["id"]): r for r in postings.load_all()}
    return _INDEX


def error(id_, code, message):
    return {"jsonrpc": "2.0", "id": id_, "error": {"code": code, "message": message}}


def result(id_, res):
    return {"jsonrpc": "2.0", "id": id_, "result": res}


def call_tool(id_, params):
    if not isinstance(params, dict) or params.get("name") != "score_posting":
        return error(id_, -32602, f"unknown tool: {params.get('name') if isinstance(params, dict) else params!r}")
    args = params.get("arguments")
    if not isinstance(args, dict) or set(args) != {"board", "posting_id"}:
        return error(id_, -32602, "arguments must be exactly {board, posting_id}")
    board, pid = args["board"], args["posting_id"]
    if not (isinstance(board, str) and BOARD_RE.match(board) and isinstance(pid, str) and ID_RE.match(pid)):
        return error(id_, -32602, "board or posting_id does not match its pattern")
    rec = index().get((board, pid))
    if rec is None:
        return result(id_, {"isError": True, "content": [{"type": "text", "text": f"no stored posting {board}/{pid}"}]})
    resume = json.loads((HERE / "fixtures" / "resume.fictional.json").read_text(encoding="utf-8"))
    dec = flt.decide(rec, resume)
    out = {"filter_version": "v0.3", "board": board, "posting_id": pid, "title": rec["title"], "location": rec["location"],
           "captured": rec["captured"], "outcome": dec["outcome"], "deciding_rule": dec["gate"], "reason": dec["reason"],
           "flags": dec["flags"], "claims": dec["claims"], "quote_check_errors": flt.verify_quotes(dec, rec),
           "note": "Evidence only. Whether this posting is worth the candidate's time is a human decision."}
    return result(id_, {"content": [{"type": "text", "text": json.dumps(out, ensure_ascii=False)}],
                        "structuredContent": out, "isError": False})


def handle(msg):
    """Return a response dict, or None for a notification."""
    if isinstance(msg, list):
        return error(None, -32600, "batch requests are not supported")
    if not isinstance(msg, dict) or msg.get("jsonrpc") != "2.0" or not isinstance(msg.get("method"), str):
        return error(msg.get("id") if isinstance(msg, dict) else None, -32600, "invalid request")
    method, id_, params = msg["method"], msg.get("id"), msg.get("params") or {}
    is_note = "id" not in msg
    if method == "notifications/initialized" or (is_note and method.startswith("notifications/")):
        return None
    if is_note:
        return None
    if method == "initialize":
        asked = params.get("protocolVersion") if isinstance(params, dict) else None
        ver = asked if asked in PROTOCOL_VERSIONS else PROTOCOL_VERSIONS[0]
        return result(id_, {"protocolVersion": ver, "capabilities": {"tools": {"listChanged": False}},
                            "serverInfo": SERVER_INFO,
                            "instructions": "One read-only tool: score_posting. It reads stored postings only."})
    if method == "ping":
        return result(id_, {})
    if method == "tools/list":
        return result(id_, {"tools": [TOOL]})
    if method == "tools/call":
        return call_tool(id_, params)
    return error(id_, -32601, f"method not found: {method}")


def main() -> int:
    tr = Transcript()
    print(f"[js3-mcp] transcript: {tr.path}", file=sys.stderr)
    stdin, stdout = sys.stdin.buffer, sys.stdout.buffer
    while True:
        line = stdin.readline(MAX_LINE + 1)
        if not line:
            break
        if len(line) > MAX_LINE and not line.endswith(b"\n"):
            while True:                                  # discard the rest of the oversized line
                more = stdin.readline(MAX_LINE)
                if not more or more.endswith(b"\n"):
                    break
            tr.log("in", {"oversized_line_bytes_at_least": len(line)})
            resp = error(None, -32600, f"message larger than {MAX_LINE} bytes")
        else:
            text = line.decode("utf-8", errors="replace").strip()
            if not text:
                continue
            try:
                msg = json.loads(text)
                tr.log("in", msg)
            except json.JSONDecodeError:
                tr.log("in", {"unparseable": text[:500]})
                msg = None
                resp = error(None, -32700, "parse error")
            if msg is not None:
                try:
                    resp = handle(msg)
                except Exception as e:                   # never crash the session on one bad call
                    resp = error(msg.get("id") if isinstance(msg, dict) else None, -32603, f"internal error: {type(e).__name__}")
        if resp is not None:
            tr.log("out", resp)
            stdout.write((json.dumps(resp, ensure_ascii=False) + "\n").encode("utf-8"))
            stdout.flush()
    tr.log("eof", {})
    return 0


if __name__ == "__main__":
    sys.exit(main())
