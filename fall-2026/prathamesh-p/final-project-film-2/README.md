# Final project film: Honest Shortlist

INFO 7375, Fall 2026. Due 2026-11-23 23:30 ET (25 points). A 3 to 4 minute film in Professor Bear's four parts, in order:
(1) executive summary, (2) what others have done, (3) methods, (4) evaluation.

| Field | Value |
|---|---|
| Name | Prathamesh Pathak (`prathamesh-p`) |
| Project | Honest Shortlist (pitched 2026-10-14, `65ff4a0`) |
| Branch | `prathamesh-p-final-project-film-2`, from `f8a7af8` (JS2 head) |
| Runtime | 3:54.3 (234.250 s, ffprobe on the final master) |
| Rebuild instructions | "Rebuild" below; the full log is in `FRICTIONAL.md` |

## Status

- **Script.** Prathamesh approved it on 2026-11-23.
- **Review cut.** Prathamesh watched and approved it on 2026-11-23. Every toolkit gate passed on it: F, L, A, W, B, and V (36 frames, 0 BLOCKER, 0 MAJOR).
- **Final master.** Rendered on 2026-11-23 at 11:38 EST with `art final --height 1080`, and **GATE T passed** (18 beats, 0 FAILs; `TYPECHECK.md`).
- **Submission.** The master was submitted to Canvas as a file upload.

## The rendered film

The MP4 is **not in GitHub**: the course repo's root `.gitignore` ignores `*.mp4`. The SHA-256 below shows which file was submitted to Canvas.

| Filename | Size (bytes) | Runtime | Format | SHA-256 |
|---|---|---|---|---|
| `final/honest-shortlist-final.mp4` | 9,624,963 (9.2 MB) | 3:54.3 (234.250 s) | 1920×1080 · 24 fps · H.264 + AAC | `256600048bff4c6fc1c23990645766944b5b9c4e5408fbbe2261513ad1c9eb3c` |

To check a copy, run `certutil -hashfile <filename>.mp4 SHA256` in CMD. It must print the SHA-256 above.
`final/honest-shortlist-final.verified.json` is the toolkit's own record of the verified master.

## Toolkit (same setup as the pitch film)

- brutalist.art at `C:\info7375\brutalist.art-latest` (`519fcbb`), with its `.venv` and Prathamesh's Windows patches (pitch `toolkit-patches/`).
- `bash art smoke` passed on 2026-11-23 (`logs/art_smoke_2026-11-23.log`).
- Voice: Kokoro `af_bella`, local and free ($0.00). No instructor persona, name or outro.
- The synthetic voice is **disclosed on screen** in B00.
- Every mock-up carries the on-screen label **CONSTRUCTED**, and the SEEDED demo is labeled **SEEDED**. The frame check is in `gate-reports/FRAME-CHECK.md`.

## Files

| File | Purpose |
|---|---|
| `SCRIPT.md` | The approved narration in the four parts, with a source tag on every line |
| `beat_sheet.json` | One picture and one idea per beat, with measured audio durations. `make_sheet.py` generates it from SCRIPT.md |
| `scenes.py` | The 18 Manim scenes, reusing the pitch film's shared components |
| `SOURCES.md` | Every fact used, with its file and commit, and who did what |
| `FACTCHECK.md`, `SHOTLIST.md`, `PROMPTS.md` | The toolkit's paperwork set (Gate F) |
| `FRICTIONAL.md` | A dated log of every step, including the failed runs |
| `TYPECHECK.md` | GATE T report on the final master |
| `gate-reports/` | Gate V, layout audit, transcription check, frame check (frames included) |
| `logs/` | Raw toolkit logs, with local paths redacted |
| `transcribe_check.py`, `frame_check.py`, `redact_paths.py` | Check helpers, carried over from the pitch film |

## Rebuild

From CMD:

```bat
cd /d C:\info7375\brutalist.art-latest
call .venv\Scripts\activate.bat
set "PYTHONUTF8=1"
```

Then:

```bat
py -3.13 -I make_sheet.py                                          (from this folder)
python runtime\scripts\generate_audio_kokoro.py "<this folder>"
python -I "<this folder>\transcribe_check.py" "<this folder>" small
call bash art run "<this folder>" --height 1080                    (review cut + gates)
call bash art final "<this folder>" --height 1080 --out "<this folder>\final"
```

## Rules for this folder

- Free local pipeline only: no API keys, no paid generation, no uploads by the toolkit.
- Renders, audio and caches are not committed (`.gitignore` here and at the repo root).
- Past tense is used only for things that exist and ran. The film makes no JS3 claim, because JS3 did not exist on 2026-11-23.
