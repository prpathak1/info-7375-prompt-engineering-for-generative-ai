#!/usr/bin/env python3
"""transcribe_check.py: whisper-transcribe each beat's mp3 and diff it against narration_text.

Usage: python transcribe_check.py <film-folder> [model]   (local faster-whisper, CPU, int8)
Writes gate-reports/TRANSCRIPT-CHECK.md. Words are compared after lower-casing and stripping
punctuation; every word that differs is listed for a human to judge (mispronunciation vs. a
transcription artefact).
"""
import difflib, json, re, sys
from pathlib import Path

from faster_whisper import WhisperModel

sys.stdout.reconfigure(encoding="utf-8")  # `python -I` ignores PYTHONUTF8; Windows console is cp1252
reel = Path(sys.argv[1]); size = sys.argv[2] if len(sys.argv) > 2 else "small"
only = set(sys.argv[3:])  # optional beat ids: re-check only these (report goes to TRANSCRIPT-CHECK-<ids>.md)
sheet = json.loads((reel / "beat_sheet.json").read_text(encoding="utf-8"))
model = WhisperModel(size, device="cpu", compute_type="int8")
norm = lambda s: re.sub(r"[^a-z0-9' ]+", " ", s.lower().replace("-", " ")).split()

out = [f"# TRANSCRIPT-CHECK.md\n\nfaster-whisper `{size}` (CPU, int8), language en. Compared word by word "
       "with `narration_text` after lower-casing, stripping punctuation and splitting hyphens.\n",
       "| Beat | Match | Differences (expected → heard) | Heard |", "|---|---|---|---|"]
for b in sheet["beats"]:
    if only and b["beat_id"] not in only:
        continue
    mp3 = reel / b["audio_file"]
    segs, _ = model.transcribe(str(mp3), language="en", beam_size=5)
    heard = " ".join(s.text.strip() for s in segs)
    a, h = norm(b["narration_text"]), norm(heard)
    sm = difflib.SequenceMatcher(a=a, b=h, autojunk=False)
    diffs = [f"`{' '.join(a[i1:i2]) or '∅'}` → `{' '.join(h[j1:j2]) or '∅'}`"
             for tag, i1, i2, j1, j2 in sm.get_opcodes() if tag != "equal"]
    out.append(f"| {b['beat_id']} | {sm.ratio():.0%} | {'; '.join(diffs) or 'none'} | {heard} |")
    print(b["beat_id"], f"{sm.ratio():.0%}", "; ".join(diffs) or "none", flush=True)
(reel / "gate-reports").mkdir(exist_ok=True)
name = "TRANSCRIPT-CHECK.md" if not only else f"TRANSCRIPT-CHECK-{'-'.join(sorted(only))}.md"
(reel / "gate-reports" / name).write_text("\n".join(out) + "\n", encoding="utf-8")
