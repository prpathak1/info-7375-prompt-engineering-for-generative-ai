# FRICTIONAL.md: final project pitch film

One entry per meaningful step. Each entry records what was tried, what happened, and what changed.
Failures are recorded as they happened.

---

## Entry 1: 2026-10-14 15:49 EDT. Phase 1, toolkit clone and read

**Tried:** Cloned brutalist.art and read its README, CLAUDE.md, `setup`, `art`, `run.sh`,
`requirements.txt` and the show-tell SKILL.md.

**What happened:**
- A clone already existed at `C:\info7375\brutalist.art` (commit `cd4bf20`, from Week 1). It has
  4 locally modified files: the Week 1 Windows patches to `compile.py` and `remotion_scenes.py`,
  the `setup` guard patch, and `package-lock.json`. Upstream is 46 commits ahead, and a
  fast-forward is possible.
- To avoid overwriting those patches, Claude made a separate fresh clone at
  `C:\info7375\brutalist.art-latest` (HEAD `519fcbb`).
- Upstream now pins **Manim to 0.20.x** (`requirements.txt`). It says 0.18.x renders each scene one
  frame short, and that compile.py then refuses the film.
- show-tell defaults to the persona "Liam, in for Bear", a spoken @NikBearBrown outro, a Claude.ai
  composer for Your Turn, and Professor Bear portraits for any person. These conflict with the
  course rules on persona and impersonation found in Week 1 (week-01 FRICTIONAL Entry 6).

**What changed:** Nothing has been installed or patched. A second clone (about 1 GB) now exists.

---

## Entry 2: 2026-10-14 15:49 EDT. Phase 1, environment check

**Tried:** Checked each prerequisite from CMD and Git Bash. Ran the existing clone's `./setup` in
check mode (no `--install`) inside the Week 1 venv, with `PYTHONUTF8=1`.

**What happened:**
- Present: git 2.55, Python 3.13.1 (default) and 3.11.9 (`py -3.11`), Node 24.19 / npm 11.17,
  ffmpeg/ffprobe 9.0.2, MiKTeX pdflatex + dvisvgm, the Kokoro model (354 MB, old clone only),
  Remotion node_modules plus chrome-headless-shell (old clone only), and EB Garamond + Oswald
  installed per-user.
- Week 1 venv: manim **0.18.1**, ManimPango 0.5.0, **Pillow 10.4.0**, kokoro-onnx 0.6.1,
  faster-whisper 1.2.1, scipy 1.17.1. Upstream now requires manim 0.20.x and Pillow ≥ 11.
- `./setup` shows **all 7 rows green**. The green is misleading for the new toolkit: setup checks
  only `import manim`, not the version, and it ran against the old clone.
- PyPI shows win_amd64 cp311 wheels for manimpango 0.6.1 and Pillow 12. manim 0.20.1 is pure
  Python and needs Python ≥ 3.11, so the 3.11 venv qualifies. The upgrade itself has not been tried.
- Upstream still has three Week 1 Windows bugs: the raw-path `drawtext=fontfile=` (compile.py:795),
  bare `"npx"` in subprocess (remotion_scenes.py:90), and the ElevenLabs guard failing on the repo's
  own `youtube/` files (10 hits). The `_smoke` slug bug is fixed upstream.
- From CMD, `bash` resolves first to `C:\info7375\bin\bash.cmd`, which runs Git Bash. The next match
  on PATH is `WindowsApps\bash.exe`, the WSL launcher.
- iso_kit `professor_bear()` looks for `professor-bear/*.png`, which is not shipped in the repo, so it
  would fail on this clone.

**What changed:** Nothing has been installed. The fix list is waiting for Prathamesh's approval.

---

## Entry 3: 2026-10-14 15:49 EDT. Folder scaffold

**Tried:** Created `fall-2026/prathamesh-p/final-project-film/` with the six required files and a
`.gitignore`.

**What happened:** The files were created. `PROJECT-BRIEF.md` and `beat_sheet.json` are placeholders
until Prathamesh writes the seven answers. The course repo is checked out on branch
`prathamesh-p-week-01`. No git operations were run.

**What changed:** The folder exists. Nothing has been committed.

---

## Entry 4: 2026-10-14 16:03 EDT. Approval, film branch

**Tried:** Prathamesh approved Phase 2 with changes: build in `brutalist.art-latest` with a NEW venv,
leave the old clone and the Week 1 venv untouched, copy the model and node_modules (no downloads),
save the 4 patches as .diff files, prove the setup with `bash art smoke` from CMD, and stop after
about 45 minutes if smoke is failing.

**What happened:** Created branch `prathamesh-p-final-project-film` in the course repo, from the
current HEAD of `prathamesh-p-week-01`. Nothing has been committed.

**What changed:** All film commits will go on the new branch.

---

## Entry 5: 2026-10-14 16:04 EDT. New venv, model and node_modules copied

**Tried:** `py -3.11 -m venv C:\info7375\brutalist.art-latest\.venv`, with `python3.exe` copied from
`python.exe`, then `pip install "manim>=0.20,<0.21" "manimpango>=0.6.1,<0.7" "Pillow>=11,<13"
-r requirements.txt scipy`. Copied the Kokoro model and `runtime/remotion/node_modules` from the
old clone.

**What happened:**
- pip exit 0. Every package installed from a prebuilt Windows wheel: manim 0.20.1, ManimPango 0.6.1,
  Pillow 12.3.0, numpy 2.4.6, pycairo 1.29.2, av 18.1.0, onnxruntime 1.31.0, kokoro-onnx 0.6.1,
  faster-whisper 1.2.1, scipy 1.17.1.
- **scipy is not in requirements.txt.** Claude added it because GATE T (`art final`) is skipped
  without it.
- Kokoro model SHA-256 matches the old clone (onnx `7D5DF8EC…36A6C5`, voices `BCA610B8…1FBF7D`).
- node_modules: 132 entries in both. `package.json` is identical, and `npm ls --depth=0` shows no
  errors (remotion 4.0.486). robocopy took 5 s. Its exit code 1 means "files copied", not failure.

**What changed:** The new clone has a working toolchain. The old clone and its venv were not touched
(still `cd4bf20`, the same 4 modified files, manim 0.18.1). Correction: Phase 1 did run `git fetch`
on the old clone. That updated only its remote-tracking refs, not its files.

---

## Entry 6: 2026-10-14 16:05 EDT. The 4 Windows patches

**Tried:** Re-applied the Week 1 patches to the new code and saved each one as a .diff in
`toolkit-patches/`.

**What happened:** Claude's first attempt used a Python heredoc and `sed`. It applied patches 02
and 03, but **failed on 01 and 04** because of backslash escaping (an assertion error and a `sed`
"unterminated s command"), and wrote two empty .diff files. Claude redid 01 and 04 with exact text
edits and regenerated the diffs. On a stashed clean tree, `git apply --check` shows the cumulative
compile diff, 03 and 04 all apply cleanly to upstream `519fcbb`.

**What changed:** 3 toolkit files are modified locally and not committed. The diffs and a README are
in `toolkit-patches/`.

---

## Entry 7: 2026-10-14 16:06 EDT. `bash art smoke` from CMD

**Tried:** From CMD: `call .venv\Scripts\activate.bat`, then `set PYTHONUTF8=1 && bash art smoke`.

**What happened:**
- **Run 1 FAILED:** `Fatal Python error: preconfig_init_utf8_mode: invalid PYTHONUTF8 environment
  variable value`. In CMD, `set PYTHONUTF8=1 && …` stores the value as `"1 "`, with the space
  before `&&`. The run 1 wrapper also printed a misleading `EXIT=0`, because of how the echo was
  chained. Log: `logs/art_smoke_2026-10-14_run1.log`.
- **Run 2 PASSED** with the quoted form `set "PYTHONUTF8=1"`, from a .cmd file. Kokoro made B00 8.73 s
  and B01 5.12 s (af_bella, $0.00). GATE L clean. Compile with `drawtext: yes` (patch 01 works).
  GATE V `frames=4 BLOCKER=0 MAJOR=0` (patch 02 works). GATE SIZE 918,998 B, GATE TYPE video + audio,
  GATE AUDIO mean_volume −24.2 dB. Result: `SMOKE PASS`. Log: `logs/art_smoke_2026-10-14_run2.log`.
- Advisory line, expected for this fixture: `SKIN LINT: NO RENDERABLE BEATS`.
- **What smoke does NOT prove:** the fixture is two slates, so no Manim or Remotion scene was
  rendered. manim 0.20.1 and patch 03 (npx) have not been tested by a render yet.
- `bash setup` (check mode) on the new clone: 7/7 rows green. The ElevenLabs guard passes, so patch 04
  works. Log: `logs/setup_doctor_2026-10-14.log`.

**What changed:** The new setup is proven for the audio, compile and gate path. Every CMD command
will use `set "PYTHONUTF8=1"`. Smoke passed about 3 minutes after the start (16:03 → 16:06), well
inside the 45-minute limit.

---

## Entry 8: 2026-10-14 16:08 EDT. The MP4 must be committable

**Tried:** Removed `*.mp4` from this folder's `.gitignore`, because Prathamesh confirmed the rendered
film is a required deliverable for this assignment.

**What happened:** `git check-ignore` showed that **the course repo's root `.gitignore` (line 33,
`*.[mM][pP]4`) still ignores it**. Claude added `!final/*.mp4` to this folder's `.gitignore`.
Re-checked: `final/film.mp4` is not ignored, and `manim/B00.mp4` still is.

**What changed:** Only the master in `final/` can be committed. This overrides the instructor's
repo-wide rule for one folder. GitHub rejects files over 100 MB, so the master's size will be
checked before committing.

**Also noted:** the course `AGENTS.md` says course films go under `youtube/`. This folder follows
Prathamesh's instruction (`fall-2026/prathamesh-p/`), as Week 1 did.

---

## Entry 9: 2026-10-14 16:10 EDT. A failed doc update

**Tried:** Claude tried to append Entries 4 to 8 and update the other docs in one long shell command.

**What happened:** bash rejected it with a quote-parsing error (`unexpected EOF while looking for
matching '`), and nothing was written. Claude checked that no file was half-edited, then made the
edits with the file-edit tool instead.

**What changed:** Doc edits are now made with the editor, not shell heredocs.

---

## Entry 10: 2026-10-14 16:12 EDT. Decision: the MP4 stays out of GitHub

**Tried:** Prathamesh reviewed the `!final/*.mp4` override from Entry 8 and decided to revert it.

**What happened:** The reason given: the course repo's root `.gitignore` (`*.[mM][pP]4`) and the final
project brief both keep MP4s out of GitHub. The rendered MP4 will go in the Canvas ZIP. `README.md`
will record its filename, size, runtime and SHA-256, so the GitHub folder provably matches the ZIP.
Claude removed the override and put `*.mp4` back in this folder's `.gitignore`. `git check-ignore`
confirms `final/film.mp4` is ignored again.

**What changed:** Entry 8's override is undone. README.md now has a table for the MP4's record, to be
filled in after the final render. This is flagged as at risk in `RUBRIC-CHECK.md`: the pitch brief
lists "Rendered .mp4" under required submission, and some classmates' folders on `origin/main`
commit their MP4s.

---

## Entry 11: 2026-10-14 16:12 EDT. Folder path, voice, the official brief, RUBRIC-CHECK.md

**Tried:** Prathamesh confirmed the folder path and the voice, and sent the official pitch film brief
so that RUBRIC-CHECK.md could be built.

**What happened:**
- **Folder:** `fall-2026/prathamesh-p/final-project-film/` stays. The assignment brief names this path,
  and it overrides the `youtube/` convention in the course `AGENTS.md`.
- **Voice:** `af_bella`.
- **The brief did not arrive in the message.** The message held a template placeholder
  (`[paste the full contents of 01_final_project_pitch_film.md]`) instead of the text. Claude found
  the file at `<LOCAL>\Downloads\01_final_project_pitch_film\01_final_project_pitch_film.md`
  (5,861 B, SHA-256 prefix `aa82ba8e8c73a336`, dated 15:39 today) and used it. Prathamesh still has to
  confirm that it is the official version.
- The brief's requirements that are new since Phase 1: `README.md` must give name, working title,
  target role, runtime and rebuild instructions; "narrate as yourself"; gate reports must be included;
  and the canonical toolkit is `git clone https://github.com/nikbearbrown/brutalist.art`, which matches
  the setup.
- Created `RUBRIC-CHECK.md` with one row per requirement. Two rows are **at risk**: the synthetic voice
  vs "narrate as yourself", and the MP4 being in the ZIP only vs "matching GitHub folder".
- Rewrote `README.md` around the brief's required fields and added a `gate-reports/` slot.

**What changed:** The requirements are now tracked in one table, which will be updated at the end of
every phase.

---

## Entry 12: 2026-10-14 16:17 EDT. The brief is confirmed; the MP4 decision is reversed

**Tried:** Prathamesh confirmed that the Downloads copy of `01_final_project_pitch_film.md` is the
official brief, and reviewed the two at-risk rows.

**What happened:** **Reversal of Entry 10.** The rendered master WILL be committed. The reason: the
brief lists "Rendered .mp4" under required submission, and classmates' folders on `origin/main`
commit theirs. The method: when the master is final, check that it is under 100 MB, then force-add
ONLY that file (`git add -f final/<slug>.mp4`). The `.gitignore` stays as it is (`*.mp4` ignored), so
no intermediate render can be committed by accident. The SHA-256 table in README.md is also kept, so
the ZIP and the GitHub copy can be compared.

**What changed:** README.md and RUBRIC-CHECK.md are updated. Entry 10 is kept as written, because it
records the earlier decision.

---

## Entry 13: 2026-10-14 16:17 EDT. Prathamesh's reading of "narrate as yourself"

**Tried:** Decided how to treat the brief's line "Narrate as yourself; do not use the instructor's
name, persona, or credit line."

**What happened:** Prathamesh's reading, as summarised: "narrate as yourself" sits in the same
sentence as the instructor-persona ban, so it rules out impersonation. It does not require a recorded
human voice. Prathamesh's first-person script, read by a synthetic voice (Kokoro `af_bella`) and
disclosed on screen as synthetic, meets it.

**What changed:** The voice stays `af_bella`. RUBRIC-CHECK.md keeps the row as **at risk
(interpretation)**, because a grader could read the line differently.

---

## Entry 14: 2026-10-14 16:17 EDT. Seven-question interview starts

**Tried:** Started the interview: one question at a time. For each answer Claude shows a tightened
version, flags unverifiable claims, wrong tense and vagueness, and asks at most one rubric-required
follow-up. Claude does not write the answers.

**What happened:** To check answers against the course arc, Claude read the briefs in
`Downloads\01_final_project_pitch_film\`: 02 Reallocation Engine mode build (due Oct 21) and
03–07 JS1–JS5 (due Oct 31, Nov 10, Nov 23, Dec 1, Dec 13). In short: JS1 covers the contract, the
one-board watch, two labeled judges and the 10/10 held-out prompt experiment. JS2 covers the bounded
loop (exits, budgets), the permission policy in code (10 boundary cases) and the review packet. JS3
covers the filter, the reject audit, the source-grounded shortlist, the MCP-shaped tool and score
accountability. JS4 covers the plan, the evidence matrix, versioned memory and the stale-write
rejection. JS5 covers the approval gate with a fingerprint, the register, the controlled failure and
the ten-document packet.

**What changed:** `PROJECT-BRIEF.md` now has one section per question, filled in only as Prathamesh
approves each answer.

---

## Entry 15: 2026-10-14 16:24 EDT. The rule changes: Claude drafted the seven answers

**Tried:** Prathamesh changed the standing rule "I will write the answers to the seven pitch questions
myself." The seven answers were **drafted by Claude (claude.ai chat, Opus 5.5) on 2026-10-14, at
Prathamesh's request**. Prathamesh reviewed them, is responsible for defending them, and pasted them
here as the interview answers. This session tightens the wording, flags claims, and stops on every
`[CONFIRM]` item.

**What happened:**
- **The paste was cut off** mid-sentence at "Exists today: the toolkit setup with passing smoke
  (logs/), this film folder, and the Week 1 work (cite". The rest of "exists today" and the whole
  "will exist" list did not arrive.
- Claude checked what it could, without resolving any `[CONFIRM]` item:
  - **Week 1 commit:** `ce1a06ce9aef57db80de8c458aa0a09f45468235` (2026-09-27, author Prathamesh P), on
    `fork/prathamesh-p-week-01`. It is **not in `origin/main`**, so it is pushed to the fork but not
    merged.
  - **Week 1 patch files:** 5 `brutalist-*.diff` files in that commit.
  - **Week 1 authorship:** the week-01 `SOURCES.md:25` says `scenes.py`, `evidence/seed7_sequence.py`
    and `b08_your_turn_snippet.py` were "Written by Claude to my specification". Week 1 FRICTIONAL
    Entries 4 and 7 say Claude wrote the patches, and Prathamesh approved them.
  - **Possible existing evidence:** a Reallocation Engine recipe and prototype by Prathamesh,
    `prpathak1-network-eng-h1b-soc-15-1241` (Network Engineer, not data/ML). Commits `100a823`,
    `1a3e757` and `1b5a589` (2026-10-03, author prpathak1), on branch
    `contrib/2026fa-prpathak1-network-eng-h1b-soc-15-1241` of the fork. It is mostly Node
    (`run.mjs`, `test/run.test.mjs`) plus one Python file (`normalize_names.py`). Its authorship split
    is not stated in the files Claude read.
  - **H-1B data:** the Reallocation Engine has `data/80-days-to-stay/data/SEC_DOL_H1b_data_mapped-*`
    audits and `scripts/audit-sec-dol-h1b-data.py`.

**What changed:** The standing rule is updated in SOURCES.md. No answer goes into PROJECT-BRIEF.md
until its `[CONFIRM]` items are resolved and Prathamesh approves it.

---

## Entry 16: 2026-10-14, about 16:30 EDT (first logged as 16:42, a guessed time; corrected in Entry 17). CONFIRM answers, the brief, and the claim audit

**Tried:** Prathamesh answered the 8 CONFIRM items, accepted Claude's other corrections, and changed
the persona to an F-1 master's student targeting network engineering roles (SOC 15-1241), to match
the Reallocation recipe.

**What happened:**
- **5 of the 8 answers arrived as unfilled template text.** Items 1 (LinkedIn), 2 (chat assistant),
  4 (Python evidence and `normalize_names.py`), 6 (recipe authorship split) and 7 (the Q7 basis) still
  had `[fill in…]` / `[pick one…]` placeholders. Claude did not fill them in. They are marked
  `[PENDING]` in PROJECT-BRIEF.md.
- Resolved: 3 (target role kept), 5 (Brutalist wording approved, framed as debugging and
  verification), 8 (both lists resent in full).
- **H-1B data check:** the Reallocation Engine `data/80-days-to-stay/README.md` says it mapped SEC data
  against DOL LCA Disclosure Data and the USCIS H-1B Employer Data Hub. That is secondary, with no
  fiscal years and no dataset licence, and the CSV isn't in the clone. **Not verifiable, so the film
  will say only "public H-1B employer data."** Side finding: the CSV has `executive_officers`,
  `board_directors` and `phone` columns, which are real people's data. The agent will not use them.
- Verified that the 3 recipe commits are not in `origin/main` or `upstream/main` (after
  `git fetch upstream`). Claude's first verification loop printed `git merge-base` usage errors from a
  bad branch list (`origin/HEAD -> …`), but the valid comparisons gave the answer.
- Wrote PROJECT-BRIEF.md (about 935 words, which may exceed one printed page) and CLAIM-AUDIT.md
  (20 claims: 12 VERIFIED, 2 PARTIAL, 5 PENDING, plus design checks). Updated RUBRIC-CHECK.md:
  Q2, Q7, the one-page brief and two grading rows are **at risk** until the PENDING items are filled.

**What changed:** The brief exists with 6 `[PENDING]` slots. The beat sheet has not been started.

---

## Entry 17: 2026-10-14 16:36 EDT. Options sent unpicked; recipe records read; brief trimmed

**Tried:** Prathamesh sent a reply with (a)/(b) options for the 5 pending items, and asked for the
brief to be trimmed to about 550 words, the audit re-run, and RUBRIC-CHECK updated.

**What happened:**
- **No option was picked** for any of items 1–5. The `<…>` blanks were unfilled. Claude did not choose.
- Items 3 and 4 asked Claude to read the recipe's own records either way. Findings, from branch
  `contrib/2026fa-prpathak1-network-eng-h1b-soc-15-1241`:
  - The recipe's `SOURCES.md` has an AI-vs-student table. The AI "drafted all code and text". The
    student made the situation, data, rule, date and honesty decisions, and approved every commit.
  - **`normalize_names.py` was written by Claude Code:** FRICTIONAL F22 (line 337) lists it as an AI
    extra, and line 363 records the student accepting it.
  - **All 6 commits** on the branch (`ad7d728`, `100a823`, `1a3e757`, `1b5a589`, `25436c0`, `6471e2b`)
    carry `Co-Authored-By: Claude Opus 5.5`.
  - That recipe used the tracked `mapped_student_employment_targets_v3.csv`. Its README also gives no
    fiscal years or licence, so the H-1B wording stays generic.
- Trimmed PROJECT-BRIEF.md from about 935 to about 600 words, with Q4 at one line per topic. The pending
  items are merged into 4 `[PENDING]` slots (Q2 alternatives, Q7 Python, recipe split, Q7 basis).
- **Correction, a Claude error:** Entry 16, RUBRIC-CHECK and CLAIM-AUDIT carried timestamps of
  "16:42" and "16:40". These were guesses. `date` printed 16:34 at the start of this step, so that
  work happened at about 16:30. Corrected. From now on, every timestamp comes from `date`. The times
  in Entries 5–9 were also written without a `date` call. They fall between the real readings 16:03
  (Entry 4) and 16:12 (Entry 10), so they are approximate.

**What changed:** CLAIM-AUDIT has rows #3, #4 and #10 updated and #21–22 added. The brief is shorter.
Prathamesh still has to pick options for items 1–5.

---

## Entry 18: 2026-10-14 16:39 EDT. The brief is finalized

**Tried:** Prathamesh picked `1b 2b 3b 4 yes 5b` and dictated the Q2 wording.

**What happened:**
- **Q2:** no alternative was examined. Prathamesh's words go in verbatim: "I haven't examined
  alternatives yet. During JS1 I will compare against LinkedIn job alerts and against pasting a
  posting into a chat assistant, and record what I see in FRICTIONAL." **Kept at risk**, because the
  rubric asks for 1–2 real alternatives examined. *A commitment for JS1 (Oct 31): log both
  comparisons here.*
- **Q7:** Python moved to "New / will demonstrate". The recipe split was written from the recipe's
  own SOURCES table. The basis is "I will measure how often sponsorship wording is missing or
  ambiguous in my JS1 sample."
- **Audit re-run:** 0 `[PENDING]`, and no PENDING claim rows. The past-tense grep finds only verified
  statements (CLAIM-AUDIT #1, #3) plus "I haven't examined" (#6). There are no metric-like numbers.
- The brief is **684 words**, over the ~550 target, because the resolved Q7 text is longer than its
  placeholders. RUBRIC-CHECK marks the one-page row at risk. It has not been trimmed again without
  Prathamesh's say-so.

**What changed:** PROJECT-BRIEF.md is final. 4 RUBRIC-CHECK rows remain at risk. The beat sheet has
not been started.

---

## Entry 19: 2026-10-14 16:47 EDT. Brief trimmed; beat sheet drafted (not yet approved)

**Tried:** (1) Trim Q4 and "Will exist" to bring the brief to about 550 words. (2) Write
`beat_sheet.json` in the show-tell schema, with a runtime of 2:30–3:30, sized from af_bella's
measured rate.

**What happened:**
- **The trim stopped at 630 words, not 550.** Q4 and "Will exist" were 184 words together. Reaching 550
  meant cutting 134 of them, which would have removed Q4's planned-evidence column, and the rubric
  grades it. CLAIM-AUDIT "Trim re-run" lists what was removed. No claim was added.
- Read `skills/make/show-tell/reference/example-make_sheet.py` and one real reel,
  `youtube/show-tell-24-isometric-props/beat_sheet.json`, for the exact schema. Confirmed that
  `bookend_check.py` is not called by `run.sh`, `compile.py` or `art`, so dropping the house bookends
  will not block the build.
- **Rate:** smoke B00 is 23 words / 8.73 s and B01 is 12 words / 5.12 s, so 35 words / 13.85 s ≈
  **2.53 words/s (≈152 wpm)**. This matches the toolkit's own `words / 2.5` estimate.
- **Draft 1 was 18 beats, 743 words, an estimated 5:04, far over 3:30.** Claude cut it to **15 beats,
  495 words, an estimated 3:24**. That meant merging the Q1 artifact into B02, Q6's risk and
  mitigation into B10, and Q7's new and already-have into B11, and cutting secondary phrases.
  CLAIM-AUDIT lists every dropped phrase.
- **Beat IDs:** the request said "B02–B08: Q1 to Q7". Because some questions need two beats, the IDs
  run B00–B14 in sequence, and each beat carries a `pitch_question` field instead. Letter-suffixed IDs
  (e.g. `B02B`) are supported by newer Gate W code, but they were avoided to reduce pipeline risk.
- The generator is `make_sheet.py`, the toolkit's convention, so the sheet can be rebuilt.

**What changed:** `beat_sheet.json` holds 15 beats. **No audio has been generated and nothing has been
rendered.** It is waiting for Prathamesh's approval.

---

## Entry 20: 2026-10-14 16:50–17:00 EDT. Audio, transcription check, scenes, and the first `art run` attempt

**Tried:** Prathamesh approved the beats with these changes: a 4:00 hard limit (cut only if the audio
exceeds 3:50); spoken spellings "J S one", "M C P" and "read-me"; shared Manim components;
redacted real lines; and a fallback rule (two failed fixes per beat, or 21:00 EDT without a passing
review cut → plain slates).

**What happened:**
- Narration edits: "README" → "read-me" (B05), "MCP-style" → "M C P style" (B07). No "JS1" token is
  spoken anywhere in the narration. The B13 smoke line's fixture path was elided as "…". 498 words.
- Wrote the toolkit's GATE F paperwork: `FACTCHECK.md` (22 claims: 19 PASS, 1 CORRECTED, 2 EXEMPT),
  `SHOTLIST.md`, and `PROMPTS.md` ("no generation prompts").
- **Audio:** `generate_audio_kokoro.py`, af_bella, 15 beats, exit 0, $0.00. **Total 194.4 s ≈ 3:14**
  (`logs/audio_2026-10-14.log`). `make_sheet.py` now carries `audio_file` and `actual_duration_s`
  forward, so a re-run cannot wipe them.
- **Transcription check (faster-whisper `small`, local CPU):**
  - **Download, logged:** the model was not cached, so the first run downloaded
    `Systran/faster-whisper-small` (464 MB) from Hugging Face into `~/.cache/huggingface`. This is
    free; no key or account was used.
  - **Run 1 crashed** after B00 with `UnicodeEncodeError: 'charmap'`. Claude ran Python with `-I`,
    which ignores all `PYTHON*` variables, including `PYTHONUTF8`. Fix: `sys.stdout.reconfigure`.
  - Run 2: `gate-reports/TRANSCRIPT-CHECK.md`. **Flagged for Prathamesh to listen:** B00
    "Prathamesh" was heard as "prathymish", and B09 "seeded" was heard as "seated". The other
    differences are formatting artefacts ("one" → "1", "m c p" → "mcp", "log in" → "login",
    "h one b" → "h1b", "thirty first" → "31st").
- **Scenes:** `scenes.py`, with one shared component set (card, stamp, tag, block, box, arrow, panel,
  CONSTRUCTED label) and a `Pace` helper. Pace keeps every animation out of the clip-midpoint window
  that GATE T and Gate V sample, and ends each clip 0.06 s inside its audio.
- **Gate A pre-audit** (`static_scene_check.py` on a copy of `scenes.py` alone):
  - 13 of 15 passed first time.
  - **B00 fix 1:** a dot placed via `disc.width`, which the stub cannot measure. It landed at (−11.9).
    **B00 fix 2:** "shapes never change", the documented show-tell trap. Fixed by adding end dots late.
  - **B01 fix 1:** "?" outside the safe area, so explicit coordinates are now used.
  - All 15 are now clean.
- **Low-res stills contact sheet** (`manim -ql -s`), checked by eye. Fix 1 for each of:
  - B04: the "not yet examined" tag ran off the right edge, and "insufficient" overlapped the card.
  - B05: the cross sat on the table border.
  - B08: the arrow overlapped a board, and the "never" line touched the edge.
  - B11: a git line overflowed the panel, and the dots sat on the text.
  - Re-rendered and checked again.
- **`art run` attempt 1 FAILED at GATE A** on a scene named `BNN_Name`. `run.sh` finds scenes with the
  regex `class ([A-Z]…_\w+)\(Scene\)`, and it matched the example `class BNN_Name(Scene):` written in
  Claude's own docstring in `scenes.py`. **This is the trap the SKILL warns about, triggered by a
  comment.** The docstring was reworded, and the regex now finds exactly the 15 scenes. This was not a
  beat failure, so it does not count toward the two-attempt fallback rule.
  Log: `logs/art_run_2026-10-14_run1.log`.

**What changed:** Audio exists (3:14). `scenes.py` passes Gate A. `art run` attempt 2 started at
about 17:00 EDT.

---

## Entry 21: 2026-10-14 17:19–17:26 EDT. Orphaned run recovered; review cut passes every gate

**Tried:** The previous session ended while `art run` attempt 2 (2160p) was still running in the
background. Prathamesh asked for: a check of what had finished; re-runs in the FOREGROUND at
`--height 1080`; and the frame check.

**What happened:**
- **What attempt 2 had finished** (`logs/art_run_2026-10-14_run2.log`, last write 17:13):
  - All 15 scene clips rendered at 2160p, each ending 0.07–0.13 s inside its audio.
  - GATE L clean; GATE A 15/15 clean; GATE W 15/15 clean; GATE B (layout audit) CLEAN for every scene.
  - **It was killed during compile.** `.honest-shortlist-pitch-candidate-zkkygy_j/candidate.mp4`
    (9.7 MB, last write 17:17) is truncated ("moov atom not found"). `build-state.json` was stuck at
    "rendering". GATE V never ran, and no review cut existed. **Lesson:** a background render can
    be orphaned when a session ends. Renders now run in the foreground.
- **Pronunciation:** Prathamesh's reply still contained both unpicked options for B00 "Prathamesh" and
  B09 "seeded". **Nothing was changed. The audio is as generated at 16:53.** This is waiting for a
  choice.
- **Run 3** (1080p, foreground, 17:20:01–17:22:32): reused all 15 clips ("already filled") and wrote
  the review cut. **GATE V FAILED: 3 MAJOR `low-contrast`** (B02 at 50%: 0.24; B09 at 50%: 0.24;
  B09 at 85%: 0.25; floor 0.30). Both beats use the large pale kraft `box()` wall. Report kept in
  `gate-reports/gate-v-run3-1080/`.
- **Fix attempt 1 (B02, B09):** the box back wall became grey `BAR1`, following the SKILL's gate
  trap (3). Old clips moved to `_superseded/fix1/` (nothing deleted).
- **Run 4** (1080p, foreground, 17:23:05–17:25:42): B02 and B09 re-rendered and passed GATE A, W and B
  again. **GATE V passed: 30 frames, BLOCKER=0, MAJOR=0.** The run exited cleanly ("REVIEW built").
  B02 and B09 re-rendered at 2160p despite `--height 1080`, so all 15 clips are 4K.
- **Review cut:** `honest-shortlist-pitch-slate.mp4`, 1920×1080, video + audio, **194.708 s
  (3:14.7)** by ffprobe, 7,888,442 B, SHA-256 `198f911e…8c14` (`build-state.json`). It is a review
  cut with burned-in timecode and beat labels, not the master.
- Advisory SKIN LINT lines (expected under `bookend_exempt`): "B00 … COLD OPEN LAW wants
  ClaudeComposerAsk" and "B14 … OUTRO LAW wants ClaudeTitleOutro". These are ignored on purpose:
  those are the instructor-persona bookends the brief rules out.
- **Frame check:** `frame_check.py` produced 15 frames at 85% plus a contact sheet. Every row passes
  (`gate-reports/FRAME-CHECK.md`).
- **Fallback rule:** not triggered. No beat needed a second fix, and the review cut passed at 17:25,
  before 21:00.
- **Housekeeping:** `.gitignore` now ignores compile scratch dirs (`.*-candidate-*/`). Logs and
  gate reports contain local paths with the Windows username; this will be addressed in a scan
  before any commit.

**What changed:** A passing review cut exists. The final master has not been rendered; it is waiting
for Prathamesh's approval and the pronunciation choice.

---

## Entry 22: 2026-10-14 17:29–18:06 EDT. B06/B09 re-voiced; GATE T blocks the first final; B08 fixed twice

**Tried:** Prathamesh's final decisions:
- B00: keep the name as generated.
- B09: "on a real second day, or from a saved earlier response, clearly labeled".
- B06: "It will show I can build prompt contracts,".
- Keep the B11 subject line and B05's `$ run sample`.
- Redact local paths before any commit.
- Then re-voice B06 and B09, run the review, and render `art final` at 2160p.

**What happened:**
- **Re-voice (17:29):** `generate_audio_kokoro.py --only B06 B09`. B06 is now 14.42 s and B09 15.45 s;
  the total is 197.09 s. Transcription re-check (`gate-reports/TRANSCRIPT-CHECK-B06-B09.md`): B06 100%,
  B09 95% (only "one"/"two" written as digits). The "seeded" issue is gone with the word.
- Old B06 and B09 clips and their stale Manim cache were moved to `_superseded/fix2/`.
- **Review run 5** (17:31–17:35, foreground): B06 and B09 re-rendered at 2160p (clips 14.33 s and 15.37 s,
  inside their audio). GATE L/A/W/B clean, **GATE V 0/0**. Review cut 197.4 s.
- **`art final` attempt 1** (started 17:35:42, as a separate process): **GATE T BLOCKED** at 17:37.
  B08 "min-size §8.1: smallest text run 39px < floor 41px". No master was written.
  - Claude's wait loop watched for a completion marker that **never appeared**. The cause, found later:
    inside a `.cmd` file, calling `bash` (the `bash.cmd` shim) without `call` never returns, so the
    marker line was skipped.
  - At 17:57, Prathamesh asked for a status check. The process had already exited, and nothing was
    stuck. The watcher was stopped.
  - Report kept: `gate-reports/gate-t-final-run1-FAIL/`.
- **B08 fix attempt 1** (17:57): the "never: …" line went from size 32 to 36. Review run 6: GATE A/W/B/V
  clean. **GATE T still FAILED (39 px)**, because GATE T samples the clip midpoint and that line only
  appears at 62%. The wrong element was enlarged. Report: `gate-reports/gate-t-run2-FAIL-B08.md`.
- **B08 fix attempt 2** (18:02), the last attempt before the slate fallback: Claude extracted the
  midpoint frame and saw the CONSTRUCTED label, boards, label, posts and **a short arrow**. It removed
  the arrow, since `type_check.py`'s own notes say small arrowheads slip its filters. Review run 7:
  GATE L/A/W/B clean, V 0/0. **GATE T PASS** (18:06): 15 beats, 0 FAIL; B08's minimum is now 53 px.
  - The first attempt to run GATE T after run 7 never executed, because of the same `.cmd` `call` bug.
    It was re-run by itself.
- **Fallback rule:** not triggered. B08 passed on fix 2, and the time was 18:06, before 21:00.
- **`art final` attempt 2** started at 18:06:46, with `call bash …` so that the marker is written.

**What changed:** All gates pass on the review cut, and GATE T passes. B08 no longer has its arrow.
The final master is rendering.

---

## Entry 23: 2026-10-14 18:14–18:16 EDT. `art final` attempt 2 stopped on Prathamesh's instruction

**Tried:** After another session restart, Claude checked `art final` attempt 2 (started 18:06:46 as an
independent process). At 18:14 it was still running: all 15 beats were compiled, and ffmpeg was encoding
the 4K file (`candidate.mp4` at 0 bytes, last write 18:12). Prathamesh said: "dont keep it running.
stop it".

**What happened:** Claude checked the command lines first (`final.cmd` → `compile.py` → ffmpeg, all the
render), then ran `taskkill /PID 25744 /T /F` at 18:16. That terminated 8 processes in the tree. A
re-check found no render processes left. The partial output folder
`final/.honest-shortlist-pitch-candidate-93pkvpe7/` was moved to `_superseded/final-run2-stopped/`; it
was empty after the kill. `build-state.json` was left at `"verifying"`. **No master exists.** GATE T had
already passed by itself (18:06).

**What changed:** Nothing is running. The next render step is waiting for Prathamesh's instruction.

---

## Entry 24: 2026-10-14 18:17–18:24 EDT. Decision: 1080p master; master rendered; paths redacted

**Tried:** **Prathamesh's decision (received about 18:17 EDT): the final master will be 1080p, not
2160p.** Reasons, as given: the assignment does not require 4K; a smaller file stays safely under
GitHub's 100 MB limit; and the encode is faster.

**What happened:**
- **The 2160p run had already been stopped** at 18:16 (Entry 23), so it did not exit on its own.
  - A process check at 18:17:04 found no render processes; the only matches were the checking shell
    itself.
  - Its partial-output folder (empty after the kill) and a copy of its log were moved to
    `_superseded/final-2160p/`.
  - The empty `_superseded/final-run2-stopped/` folder Claude created at 18:16 was removed. Nothing
    else was deleted.
- **`art final` at 1080p** (foreground, `call bash …`, 18:17:18–18:21:18, **exit 0**):
  - It reused all 15 clips, with no scene re-rendered.
  - **GATE T PASS** on this run (`gate-reports/TYPECHECK-master-1080-PASS.md`: 15 beats, 0 FAIL).
  - It wrote **`final/honest-shortlist-pitch.mp4`**.
- **ffprobe on the master:**
  - **197.417 s (3:17.4)**, 1920×1080, 24 fps, H.264 + AAC.
  - **6,295,549 bytes**, well under GitHub's 104,857,600 limit.
  - **SHA-256 `142e91b8ae4b75f46f0515980e966474bca26f1b2df5fa6dc449731dce5bf405`**, matching
    `build-state.json` ("status": "ready").
  - Audio mean −23.9 dB, max −3.0 dB.
  - A frame at 0:30 shows no burned-in timecode or beat labels.
- **What `art final` does and doesn't check:** it runs only GATE T. GATE F/L/A/W/B/V last ran on review
  run 7 (18:02–18:04), built from the same 15 clips and the same audio, and all passed (V 0/0). They were
  not re-run on the master file itself.
- Frame check re-run on the final clips (B06, B08, B09 changed): all rows still pass.
- **README.md filled in:** working title, target role, runtime, and the MP4 table.
- **Redaction (`redact_paths.py`, logs/ + gate-reports/):**
  - Pass 1 replaced 340 paths. The grep proof then still found **663 wrapped path fragments**, where
    Manim's console splits a long path over indented lines such as `rative-ai\fall-2026\prath`, with no
    drive letter. Claude's first wrapped-line code was also muddled and was rewritten before running.
  - Pass 2 replaced 1,764 wrapped pieces. Final proof: **0 matches** for drive paths, `Users\`, the
    username and its 8.3 short form, `/c/`, `/tmp/` and the wrapped fragments.
- Also fixed outside those folders: FRICTIONAL Entry 11's Downloads path (it held the username), and
  `redact_paths.py`'s own patterns, which had the username written in. Left as is: the git author name
  in FRICTIONAL and CLAIM-AUDIT, which is not a path.
- **Still in committable files:** non-username local paths (`C:\info7375\…`) remain in BUILD-PROMPT.md,
  README.md, SOURCES.md, toolkit-patches, scenes.py (the toolkit font fallback), `build-state.json` and
  `final/honest-shortlist-pitch.verified.json`. These were outside the requested scope and are flagged
  to Prathamesh.

**What changed:** The master exists, and every gate passes. Nothing has been committed, pushed or
zipped.

---

## Entry 25: 2026-10-14 18:27 EDT. Final decisions, privacy scan, commit

**Tried:** Prathamesh's final decisions:
- **Leave** the `C:\info7375\…` paths. They contain no username and are needed to rebuild.
- **Keep** the git author name.
- **Accept** the remaining at-risk rows as logged: Q2's unexamined alternatives, the "narrate as
  yourself" interpretation, and the 630-word brief.
- **Prathamesh has watched the final master.**

Then: privacy scan, ignore check, commit, push to the fork, ZIP from the commit, Canvas text.

**What happened:**
- **Privacy scan** of all 87 committable text files (18:26):
  - Email addresses, phone patterns, API keys/tokens, and "résumé"/CV: 0 each. Claude's first
    "resume" grep used an unsupported `(?i)` flag, so its 0 meant nothing; it was re-run with `-i` and
    still found 0.
  - "@": 15 hits, none personal: `@NikBearBrown` in text explaining that the outro was dropped, `@@`
    diff hunk headers, and the ffmpeg colour `black@0.55`.
  - Windows-username pattern: 4 hits, none a path. Two are the git author name, one is a sentence
    about redaction, and one is the generic regex in `redact_paths.py`.
- **Ignore check:** `_superseded/`, `media/`, `manim/`, `mp3/`, `mp4/`, `clips/`, `_qc/`, the compile
  scratch folder, and both MP4s were already ignored, so `.gitignore` was unchanged.
- **Commit list:** 88 files, 10,873,289 bytes. None is over 10 MB; the largest is the master at
  6,295,549 B, which is force-added past the repo-wide `*.mp4` rule.
- **The commit hash will be given on Canvas.** It cannot be written into the commit that it
  identifies. It is also recorded in Claude's report to Prathamesh after the push.

**What changed:** This entry, SOURCES.md and RUBRIC-CHECK.md were written before the commit, so they
are included in it.
