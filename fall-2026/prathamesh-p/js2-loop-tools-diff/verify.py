#!/usr/bin/env python3
"""verify.py: the independent check of one loop run (GATE.md section 7; W7).

It deliberately does NOT import jobwatch, loop, adapters or policy, and it does not take any count or verdict from the run report as truth.
It uses the report only for two things: (a) as the CLAIM under test, and (b) as a list of which saved files belong to this run.
Every number it compares is recomputed from those saved files with its own small ID extractor:

  1. per board, recompute the posting count and the new-ID count from the saved raw body and the previous state snapshot,
     and FAIL if the report disagrees;
  2. FAIL any board whose posting count is 0 while the previous snapshot had at least 1, or whose count fell by more than 50%;
  3. FAIL if any saved raw body's SHA-256 does not match its .fetch.txt.
  Also (beyond GATE section 7): FAIL if a board that did not end ok/ok_empty carries a count, IDs or records (an invented value),
  and FAIL if the report says "finished" while some board failed or escalated.

Exit 0 = PASS, 1 = FAIL (the reasons are printed), 2 = the report could not be read.
Usage:  python -I verify.py runs/<run_id>-<status>.json
Read-only: it writes nothing. Python standard library only.
"""
from __future__ import annotations

import hashlib
import json
import sys
from pathlib import Path

DROP_LIMIT = 0.50
COUNT_KEYS = ("posting_count", "new_count", "new_ids", "records")


def extract_ids(platform: str, body: bytes) -> list[str]:
    """Independent of adapters.py on purpose: the minimum needed to list posting IDs for each platform."""
    data = json.loads(body)
    items = data if platform == "lever" else data["jobs"]
    return [str(item["id"]) for item in items]


def read_meta(path: Path) -> dict:
    return dict(line.split("=", 1) for line in path.read_text(encoding="utf-8").splitlines() if "=" in line)


def check(report: dict) -> list[str]:
    fails: list[str] = []
    boards = report.get("boards") or []
    for b in boards:
        key, outcome = b.get("board"), b.get("outcome")
        # 3. every saved body against its .fetch.txt
        for a in b.get("attempt_log") or []:
            if "raw_file" not in a:
                continue
            body_p, meta_p = Path(a["raw_file"]), Path(a["fetch_file"])
            if not body_p.exists() or not meta_p.exists():
                fails.append(f"{key}: attempt {a.get('n')}: saved body or .fetch.txt is missing ({body_p.name})")
                continue
            meta = read_meta(meta_p)
            actual = hashlib.sha256(body_p.read_bytes()).hexdigest()
            if meta.get("sha256") != actual:
                fails.append(f"{key}: attempt {a.get('n')}: sha256 of {body_p.name} is {actual[:12]}..., "
                             f"but its .fetch.txt says {str(meta.get('sha256'))[:12]}...")
        if outcome not in ("ok", "ok_empty"):
            invented = [k for k in COUNT_KEYS if k in b]
            if invented:
                fails.append(f"{key}: outcome {outcome} but the report gives {invented}: invented value(s) for a board with no usable response")
            continue
        # 1. recompute counts from the saved raw body and the previous snapshot
        raw = Path(b.get("raw_file", ""))
        if not raw.is_file():
            fails.append(f"{key}: outcome {outcome} but its raw file is missing: {raw}")
            continue
        try:
            today = extract_ids(b.get("platform"), raw.read_bytes())
        except (ValueError, KeyError, TypeError) as e:
            fails.append(f"{key}: the saved raw body does not parse for platform {b.get('platform')!r} ({type(e).__name__})")
            continue
        count = len(today)
        if b.get("posting_count") != count:
            fails.append(f"{key}: report posting_count={b.get('posting_count')} but the saved raw body has {count} postings")
        prev_file = b.get("previous_state_file")
        prev = None
        if prev_file:
            p = Path(prev_file)
            if not p.is_file():
                fails.append(f"{key}: previous state snapshot is missing: {p}")
            else:
                prev = set(json.loads(p.read_text(encoding="utf-8"))["ids"])
        expected_new = 0 if prev is None else len([i for i in dict.fromkeys(today) if i not in prev])
        if b.get("new_count") != expected_new:
            fails.append(f"{key}: report new_count={b.get('new_count')} but recomputed new IDs = {expected_new}")
        # 2. an empty or collapsed board is suspicious, however cleanly it finished
        if prev is not None and len(prev) >= 1:
            if count == 0:
                fails.append(f"{key}: posting count is 0 but the previous snapshot had {len(prev)} ids: "
                             f"an empty board after a non-empty one is treated as an outage or format change, not as 'no new jobs'")
            elif (len(prev) - count) / len(prev) > DROP_LIMIT:
                fails.append(f"{key}: posting count fell from {len(prev)} to {count} "
                             f"({(len(prev) - count) / len(prev):.0%}), more than the 50% limit")
    if report.get("status") == "finished":
        bad = [b.get("board") for b in boards if b.get("outcome") not in ("ok", "ok_empty")]
        if bad:
            fails.append(f"report status is 'finished' but these boards did not end ok/ok_empty: {bad}")
    return fails


def main(argv=None) -> int:
    argv = sys.argv[1:] if argv is None else argv
    if len(argv) != 1:
        print("usage: python -I verify.py runs/<run_id>-<status>.json", file=sys.stderr)
        return 2
    try:
        report = json.loads(Path(argv[0]).read_text(encoding="utf-8"))
    except (OSError, ValueError) as e:
        print(f"verify.py: cannot read report {argv[0]}: {e}", file=sys.stderr)
        return 2
    label = f" [{report.get('label')}]" if report.get("label") else ""
    fails = check(report)
    print(f"verify.py{label}: run {report.get('run_id')}  agent status={report.get('status')} exit={report.get('exit_code')}")
    if fails:
        print(f"verify.py{label}: FAIL ({len(fails)} reason(s))")
        for f in fails:
            print(f"  FAIL  {f}")
        return 1
    print(f"verify.py{label}: PASS (counts recomputed from raw, no suspicious drop, hashes match)")
    return 0


if __name__ == "__main__":
    sys.exit(main())
