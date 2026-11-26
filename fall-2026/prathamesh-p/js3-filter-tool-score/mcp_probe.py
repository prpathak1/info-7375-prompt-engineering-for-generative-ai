"""A tiny scripted MCP client used to probe a stdio tool server and keep the full transcript. Standard library only.

  python -I mcp_probe.py --probes probes/own.json --out transcripts/probe-own.jsonl -- python -I mcp_server.py
  python -I mcp_probe.py --probes probes/fs.json --out transcripts/probe-fs.jsonl -- npx -y @modelcontextprotocol/server-filesystem@2.2.0 <dir>

probes file: a JSON list of steps. A step is {"label": str, "send": <JSON value> | {"raw": "<text line>"},
"expect_reply": bool (default true)}. The client sends each step as one line, waits up to --timeout seconds for one
reply line, and logs both, with timestamps, to --out. Server stderr is logged too.
"""
import argparse
import datetime
import json
import queue
import subprocess
import sys
import threading
from pathlib import Path


def now():
    return datetime.datetime.now().astimezone().isoformat(timespec="milliseconds")


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--probes", required=True)
    ap.add_argument("--out", required=True)
    ap.add_argument("--timeout", type=float, default=20)
    ap.add_argument("cmd", nargs=argparse.REMAINDER)
    a = ap.parse_args()
    cmd = a.cmd[1:] if a.cmd and a.cmd[0] == "--" else a.cmd
    steps = json.loads(Path(a.probes).read_text(encoding="utf-8"))
    out = Path(a.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    log = out.open("w", encoding="utf-8")

    def w(kind, **kw):
        log.write(json.dumps({"t": now(), "kind": kind, **kw}, ensure_ascii=False) + "\n")
        log.flush()

    w("start", cmd=cmd)
    p = subprocess.Popen(cmd, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE,
                         shell=(sys.platform == "win32" and cmd[0] in ("npx", "npm")))
    lines = queue.Queue()
    threading.Thread(target=lambda: [lines.put(l) for l in iter(p.stdout.readline, b"")], daemon=True).start()
    errs = []
    threading.Thread(target=lambda: [errs.append(l.decode("utf-8", "replace").rstrip()) for l in iter(p.stderr.readline, b"")],
                     daemon=True).start()
    for st in steps:
        send = st["send"]
        raw = send["raw"] if isinstance(send, dict) and set(send) == {"raw"} else json.dumps(send)
        w("send", label=st["label"], line=raw if len(raw) < 2000 else raw[:200] + f"...<{len(raw)} bytes>")
        p.stdin.write(raw.encode("utf-8") + b"\n")
        p.stdin.flush()
        if st.get("expect_reply", True):
            try:
                reply = lines.get(timeout=a.timeout).decode("utf-8", "replace").strip()
                try:
                    w("recv", label=st["label"], msg=json.loads(reply))
                except json.JSONDecodeError:
                    w("recv", label=st["label"], raw=reply)
            except queue.Empty:
                w("no_reply", label=st["label"], timeout_s=a.timeout)
    p.stdin.close()
    try:
        p.wait(timeout=10)
    except subprocess.TimeoutExpired:
        p.kill()
    for e in errs:
        w("stderr", line=e)
    w("end", returncode=p.returncode)
    print(f"[probe] {len(steps)} steps -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
