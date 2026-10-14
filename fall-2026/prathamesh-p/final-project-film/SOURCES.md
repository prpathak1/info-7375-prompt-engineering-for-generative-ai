# Sources

## Tools used

| Source | Version / commit | Licence / note |
|---|---|---|
| Brutalist toolkit, https://github.com/nikbearbrown/brutalist.art | upstream HEAD `519fcbb96e9e1898d374c8794117cab494ffc5cb` (fresh clone, 2026-10-14); existing local clone at `cd4bf20904be4e7d63babd9622b17963c2361b27` | free, local |
| Course final-project briefs, `assignments/assignment-final-project.md` and `assignment-final-project-update-1.md` | course repo `origin/main` `0a0376b`, read 2026-10-14 | read for the submission rules (e.g. MP4s stay out of GitHub) |
| Assignment brief "Final Project Pitch Film - Show What You Will Build", local file `Downloads\01_final_project_pitch_film\01_final_project_pitch_film.md` | SHA-256 prefix `aa82ba8e8c73a336`, read 2026-10-14 | the official requirements; Prathamesh still has to confirm the version |
| The Reallocation Engine (Prathamesh's fork, https://github.com/prpathak1/the-reallocation-engine), `data/80-days-to-stay/README.md` and `data/80-days-to-stay/data/SEC_DOL_H1b_data_mapped-audit.md` | local clone `6471e2b` (2026-10-03); audit dated 2026-05-28 | repo MIT (© 2026 Nik Bear Brown). It names DOL LCA Disclosure Data and the USCIS H-1B Employer Data Hub as sources, but gives no fiscal years and no dataset licence, and the CSV is not in the clone. **Unverified, so the film says only "public H-1B employer data"** |
| Prathamesh's Reallocation recipe `prpathak1-network-eng-h1b-soc-15-1241` | commits `100a823`, `1a3e757`, `1b5a589` (2026-10-03), fork branch, not merged | cited as existing evidence; authorship split PENDING |
| Week 1 film, `fall-2026/prathamesh-p/week-01-video/` | commit `ce1a06ce9aef57db80de8c458aa0a09f45468235` (2026-09-27), fork branch, not merged | evidence for debugging and verification; its Python was written by Claude (week-01 `SOURCES.md:25`) |
| PyPI JSON API (wheel lists for manim 0.20.1, manimpango 0.6.1, pillow 12.0.0) | queried 2026-10-14 | metadata only, nothing installed |

## What Prathamesh wrote

- The task, its standing rules, and the Phase 1 request.
- The decisions recorded in FRICTIONAL (voice, MP4 handling, folder path, reading of "narrate as
  yourself").

## The seven pitch answers: drafted by Claude (chat), owned by Prathamesh

**Change to the standing rules (2026-10-14 16:24 EDT):** the seven answers were **drafted by Claude
(claude.ai chat, model Opus 5.5) on 2026-10-14, at Prathamesh's request**. They were not written by
Prathamesh. Prathamesh reviewed them and is responsible for defending them. Claude Code (this session)
then tightened the wording and flagged unverifiable claims. Items marked `[CONFIRM]` were resolved by
Prathamesh, not by Claude. Sources: the claude.ai chat of 2026-10-14 (a private conversation, not
included) and this session.

Claude Code's part (2026-10-14 16:24–16:42 EDT): tightened the wording of all 7 answers; rewrote the
persona to F-1 network engineering, as Prathamesh decided; checked commits, authorship notes and the
H-1B data; wrote `PROJECT-BRIEF.md` and `CLAIM-AUDIT.md`; updated `RUBRIC-CHECK.md`. Claude left the 6
`[PENDING]` slots for Prathamesh.

**2026-10-14 18:26–18:27 EDT, submission (Claude Code):** ran the privacy scan, checked the ignore
rules, wrote FRICTIONAL Entry 25, committed, pushed to Prathamesh's fork, and built the Canvas ZIP from
the commit with `git archive`. Prathamesh watched the final master and made every submission
decision.

**2026-10-14 17:29–18:24 EDT, master (Claude Code):** applied Prathamesh's B06/B09 wording and
re-voiced only those beats; made two B08 fixes for GATE T (larger text, then removing the arrow);
stopped the 2160p run on instruction; rendered the 1080p master with `art final`; wrote
`redact_paths.py` and redacted logs/ and gate-reports/; filled in README.md. The decisions (1080p,
wording, keeping the B11 subject line and B05's `$ run sample`) were Prathamesh's.

**2026-10-14 17:19–17:26 EDT, review cut (Claude Code):** recovered the orphaned run; made one GATE V
fix (grey box wall in `scenes.py`); ran `art run` twice in the foreground; wrote `frame_check.py` and
`gate-reports/FRAME-CHECK.md` (the frame verdicts are Claude's, judged by eye). Copied the toolkit's
gate reports into `gate-reports/`.

**2026-10-14 16:50–17:00 EDT, build (Claude Code):** wrote `scenes.py` (all drawings: original,
flat, in the show-tell Claude palette; colors copied from the toolkit's `iso_kit.py`), `FACTCHECK.md`,
`SHOTLIST.md`, `PROMPTS.md`, and `transcribe_check.py`. Generated the narration with Kokoro-82M
(af_bella, local) and ran the transcription check with faster-whisper `small` (Systran model, MIT,
downloaded once from Hugging Face). Fonts: EB Garamond (SIL OFL, bundled with the toolkit) and
PT Mono (SIL OFL, bundled with the toolkit, registered from file). Third-party assets in the film:
none. No images, logos, music or stock footage.

**2026-10-14 16:47 EDT, beat sheet (Claude Code):** trimmed Q4 and "Will exist" as Prathamesh
approved; wrote `make_sheet.py` and generated `beat_sheet.json` (15 beats). **The narration was drafted
by Claude Code from PROJECT-BRIEF.md** and is waiting for Prathamesh's approval. The schema follows the
toolkit's show-tell `reference/example-make_sheet.py`. Real on-screen text is quoted from
`logs/art_smoke_2026-10-14_run2.log` and `git log` (hash, date, subject only).

Finalized at 16:39 EDT from Prathamesh's choices (`1b 2b 3b 4 yes 5b`). The Q2 sentence is
Prathamesh's own wording, verbatim. The Q7 recipe split was condensed by Claude Code from the
recipe's own SOURCES.md, with Prathamesh's approval.

## What Claude (Claude Code, model Opus 5.5) contributed

**2026-10-14, Phase 1:**
- Made a fresh clone of brutalist.art at `C:\info7375\brutalist.art-latest`. The existing clone at
  `C:\info7375\brutalist.art`, with its local Windows patches, was not modified.
- Read the README, CLAUDE.md, `setup`, `art`, `runtime/scripts/run.sh`, `requirements.txt`, and
  `skills/make/show-tell/SKILL.md` in full, plus parts of `iso_kit.py`.
- Checked the installed prerequisites, ran `./setup` in check mode, grepped for Unix assumptions,
  and wrote the Phase 1 report.
- Created this folder: `README.md`, `PROJECT-BRIEF.md` (placeholder), `beat_sheet.json`
  (placeholder), `BUILD-PROMPT.md`, `SOURCES.md`, `FRICTIONAL.md`, and `.gitignore`.

**2026-10-14, Phase 2 setup (approved by Prathamesh, with changes):**
- Created git branch `prathamesh-p-final-project-film` in the course repo.
- Created a new venv `C:\info7375\brutalist.art-latest\.venv` (Python 3.11.9) and installed the
  pinned requirements, plus scipy (Claude's addition, for GATE T).
- Copied the Kokoro model and Remotion node_modules from the old clone (verified by hash and count).
- Re-applied the 4 Week 1 Windows patches and saved them in `toolkit-patches/`. Claude wrote them in
  Week 1, and Prathamesh approved them then and again now.
- Ran `bash art smoke` and `bash setup` from CMD. Logs are in `logs/`.
- Edited `.gitignore` so that only `final/*.mp4` can be committed.
- Wrote FRICTIONAL Entries 4–9 and updated `README.md` and `BUILD-PROMPT.md`.

**2026-10-14, Phase 2 wrap-up (Prathamesh's decisions):**
- Reverted the `!final/*.mp4` `.gitignore` override, as Prathamesh decided.
- Found the pitch brief in Downloads, because the message held a placeholder, and built
  `RUBRIC-CHECK.md` from it.
- Rewrote `README.md` around the brief's required fields, and wrote FRICTIONAL Entries 10–11.

Installed from PyPI (free): manim 0.20.1, ManimPango 0.6.1, Pillow 12.3.0, kokoro-onnx 0.6.1,
faster-whisper 1.2.1, scipy 1.17.1, and their dependencies. The Kokoro-82M model files come from
github.com/thewh1teagle/kokoro-onnx releases `model-files-v1.0`. They were copied locally from the
Week 1 download, not downloaded again.
