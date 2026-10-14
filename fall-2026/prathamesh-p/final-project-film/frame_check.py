#!/usr/bin/env python3
"""frame_check.py: extract one frame per beat (at 85% of its rendered clip) and build a contact sheet.

Usage: python frame_check.py <film-folder>
Writes gate-reports/frames/<BID>.png (1280x720) and gate-reports/FRAME-CHECK-contact.png. The per-beat
verdicts (CONSTRUCTED label, "fictional", disclosure, no path/email/logo/person) are judged by eye
from these frames and recorded in gate-reports/FRAME-CHECK.md.
"""
import json, subprocess, sys
from pathlib import Path
from PIL import Image, ImageDraw

reel = Path(sys.argv[1])
sheet = json.loads((reel / "beat_sheet.json").read_text(encoding="utf-8"))
out = reel / "gate-reports" / "frames"; out.mkdir(parents=True, exist_ok=True)
thumbs = []
for b in sheet["beats"]:
    bid = b["beat_id"]; clip = reel / "manim" / f"{bid}.mp4"
    dur = float(subprocess.run(["ffprobe", "-v", "error", "-show_entries", "format=duration", "-of", "csv=p=0", str(clip)],
                               capture_output=True, text=True).stdout.strip())
    png = out / f"{bid}.png"
    subprocess.run(["ffmpeg", "-y", "-v", "error", "-ss", f"{dur * 0.85:.3f}", "-i", str(clip), "-frames:v", "1",
                    "-vf", "scale=1280:720", str(png)], check=True)
    thumbs.append((bid, png, dur))
    print(bid, f"{dur:.2f}s", png.name)
w, h = 640, 360
cs = Image.new("RGB", (w * 3, (h + 30) * 5), "white"); d = ImageDraw.Draw(cs)
for i, (bid, png, dur) in enumerate(thumbs):
    x, y = (i % 3) * w, (i // 3) * (h + 30)
    cs.paste(Image.open(png).resize((w, h)), (x, y + 30)); d.text((x + 8, y + 8), f"{bid}  ({dur:.2f}s clip, frame at 85%)", fill="black")
cs.save(reel / "gate-reports" / "FRAME-CHECK-contact.png")
