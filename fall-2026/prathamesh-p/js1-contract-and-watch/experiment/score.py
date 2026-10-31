#!/usr/bin/env python3
"""score.py: compute the sampling and experiment numbers from the saved result files and experiment/labels.json.

Scoring: a call passes when it is accepted by the validator AND its verdict equals the label (fit -> relevant, not fit -> not_relevant).
A rejected call is counted as not passing, and is also reported separately. A false positive is an accepted `relevant` on a `not_fit` posting.
Writes experiment/results/summary.json and prints it.
"""
from __future__ import annotations

import json
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import jobwatch  # noqa: E402

RES = ROOT / "experiment" / "results"
labels = {r["posting_id"]: r for r in json.loads((ROOT / "experiment" / "labels.json").read_text(encoding="utf-8"))["labels"]}


def load(name):
    return json.loads((RES / name).read_text(encoding="utf-8"))


def score(calls):
    n = len(calls)
    passed = sum(c["status"] == "accepted" and c["verdict"] == labels[c["posting_id"]]["verdict"] for c in calls)
    fp = [c["posting_id"] for c in calls if c["status"] == "accepted" and c["verdict"] == "relevant"
          and labels[c["posting_id"]]["verdict"] == "not_relevant"]
    rejected = [c["posting_id"] for c in calls if c["status"] != "accepted"]
    trivial = sum(labels[c["posting_id"]]["verdict"] == "not_relevant" for c in calls)
    return {"n": n, "passed": passed, "false_positives": fp, "rejected": rejected,
            "trivial_always_not_relevant_passed": trivial}


def balance(split):
    rows = [r for r in labels.values() if r["split"] == split]
    return dict(Counter(r["label"] for r in rows)) | {"n": len(rows)}


summary = {"class_balance": {"dev": balance("dev"), "held_out": balance("held_out")}}

samp = load("sampling-v1-5x4.json")
per = {}
for c in samp["calls"]:
    d = per.setdefault(c["posting_id"], {"title": c["title"], "label": labels[c["posting_id"]]["label"], "verdicts": []})
    d["verdicts"].append(c["verdict"] if c["status"] == "accepted" else f"REJECTED")
for d in per.values():
    cnt = Counter(d["verdicts"])
    d["counts"] = dict(cnt)
    d["unanimous"] = len(cnt) == 1
    d["agrees_with_label"] = sum(v == ("relevant" if d["label"] == "fit" else "not_relevant") for v in d["verdicts"])
summary["sampling_v1"] = {"prompt_sha256": samp["prompt_sha256"], "window": [samp["started_at"], samp["finished_at"]], "per_posting": per}

for name in ("dev-v1.json", "dev-v2.json", "heldout-v2-ONCE.json"):
    r = load(name)
    summary[name] = {"prompt": r["prompt"], "prompt_sha256": r["prompt_sha256"],
                     "window": [r["started_at"], r["finished_at"]], **score(r["calls"])}

# the CONTRACT rule (record) on the same 20, for reference only (the record does not model seniority)
resume = jobwatch.load_resume(ROOT / "fixtures" / "resume.fictional.json")
by_id = {p["id"]: p for p in json.loads((ROOT / "raw" / "2026-10-30" / "zoox.json").read_bytes())}
rec = {pid: jobwatch.decide(by_id[pid], resume)["verdict"] for pid in labels}
summary["record_rule_on_20"] = {
    split: {"n": sum(1 for r in labels.values() if r["split"] == split),
            "agrees": sum(rec[p] == r["verdict"] for p, r in labels.items() if r["split"] == split),
            "false_positives": [p for p, r in labels.items() if r["split"] == split and rec[p] == "relevant" and r["verdict"] == "not_relevant"]}
    for split in ("dev", "held_out")}

(RES / "summary.json").write_text(json.dumps(summary, indent=2, ensure_ascii=False), encoding="utf-8")
print(json.dumps(summary, indent=2, ensure_ascii=False))
