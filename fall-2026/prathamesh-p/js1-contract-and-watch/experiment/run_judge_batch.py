#!/usr/bin/env python3
"""run_judge_batch.py: run the Claude judge (jobwatch.claude_judge + validate_judgment) on experiment postings.

Every call is a fresh `claude -p --no-session-persistence` process with its own session ID. The raw output is saved under --log-dir
before validation, and rejected outputs are stored as rejected. The results file is never overwritten, so a held-out run cannot be repeated by accident.

Usage (from js1-contract-and-watch/):
    python -I experiment/run_judge_batch.py --prompt prompts/judge_v1.md --split dev --out experiment/results/dev-v1.json
    python -I experiment/run_judge_batch.py --prompt prompts/judge_v1.md --ids ID1,ID2 --repeats 4 --out experiment/results/sampling.json
"""
from __future__ import annotations

import argparse
import hashlib
import json
import sys
import time
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import jobwatch  # noqa: E402

RAW = ROOT / "raw" / "2026-10-30" / "zoox.json"
CANDIDATES = ROOT / "experiment" / "candidates.json"


def main(argv=None) -> int:
    ap = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    ap.add_argument("--prompt", required=True)
    g = ap.add_mutually_exclusive_group(required=True)
    g.add_argument("--split", choices=["dev", "held_out"])
    g.add_argument("--ids", help="comma-separated posting IDs (must be experiment candidates)")
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--out", required=True)
    ap.add_argument("--log-dir", default="experiment/raw-judgments")
    ap.add_argument("--resume", default="fixtures/resume.fictional.json")
    ap.add_argument("--workers", type=int, default=4)
    a = ap.parse_args(argv)

    out = Path(a.out)
    if out.exists():
        print(f"refusing: {out} exists (runs are never repeated or overwritten)", file=sys.stderr)
        return 2
    cands = json.loads(CANDIDATES.read_text(encoding="utf-8"))["candidates"]
    ids = [c["posting_id"] for c in cands if c["split"] == a.split] if a.split else a.ids.split(",")
    allowed = {c["posting_id"] for c in cands}
    if not set(ids) <= allowed:
        print("refusing: every posting must be an experiment candidate", file=sys.stderr)
        return 2
    by_id = {p["id"]: p for p in json.loads(RAW.read_bytes())}
    resume = jobwatch.load_resume(a.resume)
    judge = jobwatch.claude_judge(a.prompt, a.log_dir)
    jobs = [(pid, k) for pid in ids for k in range(1, a.repeats + 1)]

    def one(job):
        pid, k = job
        j = jobwatch.judge_posting(judge, by_id[pid], resume)
        return {"posting_id": pid, "title": by_id[pid]["text"], "repeat": k, "status": j["status"],
                "verdict": j.get("verdict"), "session_id": j.get("session_id"), "model": j.get("model"),
                "requested_at": j.get("requested_at"), "finished_at": j.get("finished_at"),
                "raw_response_file": j.get("raw_response_file"), "errors": j.get("errors", [])}

    started = time.strftime("%Y-%m-%dT%H:%M:%S%z")
    with ThreadPoolExecutor(max_workers=a.workers) as ex:
        calls = list(ex.map(one, jobs))
    report = {"label": "judgment (Claude responses; not fact)", "prompt": a.prompt,
              "prompt_sha256": hashlib.sha256(Path(a.prompt).read_bytes()).hexdigest(),
              "split": a.split, "ids": ids, "repeats": a.repeats,
              "started_at": started, "finished_at": time.strftime("%Y-%m-%dT%H:%M:%S%z"), "calls": calls}
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(json.dumps(report, indent=2, ensure_ascii=False), encoding="utf-8")
    for c in calls:
        print(f"{c['status']:9} {str(c['verdict']):12} r{c['repeat']} {c['session_id']} {c['title']}")
    print(f"[batch] {len(calls)} calls -> {out}")
    return 0


if __name__ == "__main__":
    sys.exit(main())
