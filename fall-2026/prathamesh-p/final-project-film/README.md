# Final project pitch film

INFO 7375, Fall 2026. A 2 to 4 minute pitch film. It will be built with the free, local Brutalist
toolkit (https://github.com/nikbearbrown/brutalist.art), on native Windows.

| Field (required by the brief) | Value |
|---|---|
| Name | Prathamesh Pathak (`prathamesh-p`) |
| Working title | Honest Shortlist |
| Target role | AI / agent engineer (applied AI) |
| Runtime | 3:17.4 (197.417 s, ffprobe on the final master) |
| Rebuild instructions | `BUILD-PROMPT.md` (see also "Rebuild" below) |

## Status

**Final master rendered (2026-10-14 18:21 EDT):** `final/honest-shortlist-pitch.mp4`, 1080p. Every
toolkit gate passes: GATE T on the master; GATE F/L/A/W/B/V on the review cut built from the same
clips. Reports are in `gate-reports/`. Not yet committed or zipped.

Narration will be a neutral Kokoro voice (`af_bella`) reading Prathamesh's first-person script,
disclosed on screen as synthetic. There will be no instructor name, persona, outro, portraits, or
person beats.

## The rendered film (in GitHub and in the Canvas ZIP)

The brief requires the rendered MP4. The course repo's root `.gitignore` ignores `*.mp4`, so only the
final master is force-added (`git add -f final/<slug>.mp4`), after checking that it is under GitHub's
100 MB limit. The same file goes in `Pathak_Prathamesh_INFO7375_FinalProjectFilm.zip`. These values
prove the two copies are identical:

| Filename | Size (bytes) | Runtime | SHA-256 |
|---|---|---|---|
| `final/honest-shortlist-pitch.mp4` | 6,295,549 (6.0 MB; GitHub limit 104,857,600) | 3:17.4 (197.417 s) · 1920×1080 · 24 fps · H.264 + AAC | `142e91b8ae4b75f46f0515980e966474bca26f1b2df5fa6dc449731dce5bf405` |

Check: `certutil -hashfile <filename>.mp4 SHA256` (CMD) must print the SHA-256 above.

## Files

| File | Purpose |
|---|---|
| `PROJECT-BRIEF.md` | The project being pitched: the seven answers, written by Prathamesh |
| `beat_sheet.json` | Narration and visual plan (will be written in Phase 3) |
| `BUILD-PROMPT.md` | The exact commands and prompts that rebuild the film |
| `SOURCES.md` | Sources, what Prathamesh wrote, what Claude contributed, third-party licences |
| `FRICTIONAL.md` | A dated work log, including failures |
| `RUBRIC-CHECK.md` | Every requirement in the brief, where it is met, and its status |
| `toolkit-patches/` | The 4 local Windows patches to brutalist.art, as .diff files |
| `logs/` | Raw logs of setup and smoke runs |
| `gate-reports/` | Toolkit quality-gate reports for the film (will be produced in Phase 3) |

## Rebuild

From CMD, after the setup in `BUILD-PROMPT.md` Phase 2:

```
cd /d C:\info7375\brutalist.art-latest
call .venv\Scripts\activate.bat
set "PYTHONUTF8=1"
```

```
py -3.13 -I make_sheet.py                                         (from this folder)
python runtime\scripts\generate_audio_kokoro.py "<this folder>"
bash art run "<this folder>" --height 1080                         (review cut + gates)
call bash art final "<this folder>" --height 1080 --out "<this folder>\final"
```

Full commands, prompts and the fix history are in `BUILD-PROMPT.md` and `FRICTIONAL.md`.

## Rules for this folder

- Everything runs on the free local pipeline. No API keys, no paid generation, no uploads.
- Renders, audio, caches, credentials and private data are not committed (see `.gitignore`).
- Anything mocked up will be labeled CONSTRUCTED on screen.
