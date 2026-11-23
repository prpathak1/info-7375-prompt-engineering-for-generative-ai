# FRICTIONAL: final project film

These are facts with timestamps (EST, from `date` on this machine). Entries marked *(Claude Code)* were written by Claude Code (Opus 5.5).
A "My take:" line appears only where Prathamesh made a decision. None has been made yet in this folder.

## F1. Toolkit smoke test (2026-11-23, log written 10:40:54 EST) *(Claude Code)*
- From CMD: `cd /d C:\info7375\brutalist.art-latest`, `call .venv\Scripts\activate.bat`, `set "PYTHONUTF8=1"`, `bash art smoke`.
- Toolkit HEAD `519fcbb`, with three locally modified files (`runtime/scripts/compile.py`, `runtime/scripts/remotion_scenes.py`, `setup`). These are the Windows patches from the pitch film.
- Result: **`SMOKE PASS`**, exit 0. Kokoro made 2 beats with `af_bella` (8.73 s, 5.12 s, cost $0.00). GATE V gave BLOCKER=0 MAJOR=0. GATE SIZE passed (918,998 bytes), and so did GATE TYPE (video and audio decode) and GATE AUDIO (mean −24.2 dB).
- The log also shows `SKIN LINT: NO RENDERABLE BEATS`. The smoke example is slate-only by design, so this is not a failure.
- Full log: `logs/art_smoke_2026-11-23.log`.

## F2. Branch and folder (2026-11-23 10:42 EST) *(Claude Code)*
- In the course repo, `git checkout -b prathamesh-p-final-project-film-2` from `f8a7af8` (JS2 head, the latest commit).
- Created `fall-2026/prathamesh-p/final-project-film-2/`. Nothing is committed.
- The untracked pitch-media folder `fall-2026/prathamesh-p/final-project-film/` carried into the working tree untouched.
- The repo's `AGENTS.md` says course films go under `youtube/`. This folder follows Prathamesh's instruction and the location of the earlier films, so it is not under `youtube/`.

## F3. Fact gathering (2026-11-23 ~10:20–10:45 EST) *(Claude Code)*
- Read the pitch (`65ff4a0`), JS1 (`a4f7165`), JS2 (`f8a7af8`) and the Reallocation mode branch (`f4eab3a`, PR #59 per its FRICTIONAL Entry 9).
- **JS3 does not exist.** There is no folder and no branch. The pitch brief had planned it for 2026-11-23.
- `gh` is not installed, so PR #59's live state was not checked. Its number and URL come from the mode's FRICTIONAL.md.
- af_bella rate measured from the pitch beat sheet: 506 words / 197.09 s = **154 wpm**.

## F4. Script draft 1 (2026-11-23 ~10:50 EST) *(Claude Code)*
- The first draft ran 615 words, about 4:00 at 154 wpm, which is over the target. It was trimmed to 577 words (about 3:45).
- To make the trim, Claude Code cut the opinion line in B03 and shortened B04, B09, B11, B12, B13, B14 and B16.
- One correction came from the source: ALTERNATIVES.md (b) says Prathamesh looked at LinkedIn **search results, not a saved alert**, and B04 now says so.
- Open flags are listed in SCRIPT.md: one UNBACKED line (B13), three DECISION lines (B15–B17) and one MY TAKE (B07).
- No audio was generated and nothing was rendered.

## F5. Script decisions (2026-11-23, Prathamesh) *(recorded by Claude Code)*
- Prathamesh decided B13, B15, B16 and B17. Claude (claude.ai chat) drafted the wording at Prathamesh's request, and Prathamesh reviewed it and edited it where they disagreed.
- Prathamesh read the whole SCRIPT.md: "it says what I'd say."
- B07: the message gave no replacement line, so B07 stays as drafted.
- Placement (Claude Code): B13 and B17 replace only the flagged sentences. B13 keeps "boards need no account / stdlib Python", and B17 keeps the closing line. B15 keeps "false positives … and false negatives" before the new held-out sentence.
- Result: 593 words. Estimated at 154 wpm: 230.9 s (3:50).

## F6. Audio and transcription check (2026-11-23 ~10:52–10:58 EST) *(Claude Code)*
- `generate_audio_kokoro.py` made 18 beats, af_bella, $0.00, exit 0. **Measured total 233.41 s (3:53)**, under 4:00 (`logs/audio_2026-11-23.log`).
- `transcribe_check.py` (faster-whisper small) found mostly number formatting (`twentieth` → `20th`, `six hundred thirty one` → `631`). The full table is in `gate-reports/TRANSCRIPT-CHECK.md`.
- Items worth a listen:
  - B00 `Prathamesh` → `prathamish`. The pitch film heard the same.
  - B05 `paste` → `pasted`.
  - B09 `one four oh four` → `1404`. This is probably formatting.
  - B03 and B10: `Zoox` → `zooks`. That is the company's own pronunciation, so it is correct.

## F7. Scenes and stills (2026-11-23 ~10:55–11:05 EST) *(Claude Code)*
- `scenes.py`: 18 classes, using the pitch film's shared components unchanged.
- Low-res last-frame stills found four layout problems: B08 status labels collided, the B11 console line overflowed its panel, the B05 footer was crowded, and B17 lines were misaligned. A second pass found B08 "Greenhouse…" colliding with CONSTRUCTED.
- All were fixed and re-checked by eye. `fit()` now keeps the left edge when it shrinks a line.
- Gate F files written: FACTCHECK.md, SHOTLIST.md, PROMPTS.md.

## F8. Review cut, run 1: Gate B stopped at B02 (2026-11-23 ~11:05 EST) *(Claude Code)*
- `art run --height 1080` (CMD, venv, `PYTHONUTF8=1`). Gates F, L, A and W were clean. **GATE B (strict)** refused B02: the label "2 clearance required (inferred)" reached x = −6.5, outside the ±6.3 safe area. Exit 2.
- Fix: label centre moved from x −4.0 to −3.4. Audit kept in `gate-reports/run1-FAIL-B02/`.
- A layout audit of all 18 scenes in a scratch copy then found one more warning: the B10 ring crossed the console text. It was replaced by an underline, and the re-audit came back clean.

## F9. Review cut, run 2: all gates pass (2026-11-23 ~11:10–11:20 EST) *(Claude Code)*
- 18/18 beats filled (MANIM). Gate F passed (silent). Gate L clean; Gate A 18/18 clean; Gate W 18/18 clean; Gate B layout audit 0 errors, 0 warnings.
- **Gate V: 36 frames, BLOCKER 0, MAJOR 0.**
- Review cut `honest-shortlist-final-slate.mp4`: **233.833 s (3:53.8)**, 1920×1080, H.264 + AAC.
- SKIN LINT notes that B00 and B17 aren't the house cold open or outro. That is expected, because those bookends were dropped on purpose (same as the pitch).
- Frame check (`gate-reports/FRAME-CHECK.md`):
  - CONSTRUCTED appears on all 6 mock-up beats, and SEEDED on B16.
  - B00 shows the disclosure.
  - No frame shows a path, email, logo or person.
- `redact_paths.py logs gate-reports`: 1,799 replacements.
- The final master has **not** been rendered, as instructed.

## F10. B09 wording fix (2026-11-23 ~11:25–11:32 EST) *(Claude Code, at Prathamesh's request)*
- SCRIPT.md B09: "got one four oh four" became "got **a four-oh-four error**". The script is now 592 words.
- `make_sheet.py` dropped the audio fields for B09 only. `generate_audio_kokoro.py --only B09` gave 13.97 s (was 13.55 s), $0.00.
- Transcription check on B09: `four oh four` → `404` (formatting only; heard "a 404 error"). The other differences are `one` → `1` and `tenth` → `10th`. Report: `gate-reports/TRANSCRIPT-CHECK-B09.md`.
- The old clip was moved to `_superseded/B09.run2.mp4`. In `art run` run 3, only B09 was re-rendered and the other 17 clips were reused unchanged from run 2.
- Gate results:
  - On B09: Gate A clean, Gate W clean, Gate B layout audit 0 errors and 0 warnings.
  - On the whole film: Gate F pass, Gate L clean, Gate V 36 frames with BLOCKER 0 and MAJOR 0. Exit 0.
- Review cut: **234.250 s (3:54.3)**, 18/18 filled. The new B09 frame was checked by eye: no path, logo or person.
- The final master has still not been rendered.

## F11. Final master (2026-11-23 11:33–11:39 EST) *(Claude Code)*
- Prathamesh watched and approved the review cut, and confirmed that B07 stays as drafted.
- `call bash art final "<film>" --height 1080 --out "<film>\final"` (CMD, venv, `PYTHONUTF8=1`). **GATE T: PASS** (18 beats, 0 FAILs). Exit 0. Log: `logs/art_final_2026-11-23_1080.log`.
- `final/honest-shortlist-final.mp4`: 234.250 s, 1920×1080, 24 fps, H.264 + AAC, 9,624,963 bytes.
- SHA-256 `256600048bff4c6fc1c23990645766944b5b9c4e5408fbbe2261513ad1c9eb3c`. `sha256sum` and `certutil` agree.
- Frames from the master at 2 s and 120 s were checked by eye. There is no review overlay (timecode or beat label), no path, no logo and no person, and the B00 disclosure is fading in at 2 s.
- The MP4 is not committed (root `.gitignore`). README.md records its hash.
