# Build prompt and commands

## Phase 1: environment check (2026-10-14)

The prompt is the Phase 1 request in this session: clone the toolkit, read its README and skills
(especially show-tell), list the prerequisites, check what is installed, and report what will break
on Windows. Nothing was installed.

Read-only commands that were run (PowerShell or Git Bash):

```
git clone https://github.com/nikbearbrown/brutalist.art C:\info7375\brutalist.art-latest
git -C C:\info7375\brutalist.art fetch origin
where bash python python3 py node npx ffmpeg pdflatex dvisvgm git
C:\info7375\brutalist.art\.venv\Scripts\python.exe -m pip list
# Git Bash, existing clone, existing venv, check mode (no --install):
source .venv/Scripts/activate; export PYTHONUTF8=1; ./setup
```

## Phase 2: new toolkit setup (2026-10-14)

CMD:

```
py -3.11 -m venv C:\info7375\brutalist.art-latest\.venv
copy C:\info7375\brutalist.art-latest\.venv\Scripts\python.exe C:\info7375\brutalist.art-latest\.venv\Scripts\python3.exe
C:\info7375\brutalist.art-latest\.venv\Scripts\python3.exe -m pip install "manim>=0.20,<0.21" "manimpango>=0.6.1,<0.7" "Pillow>=11,<13" -r C:\info7375\brutalist.art-latest\requirements.txt scipy
copy C:\info7375\brutalist.art\runtime\models\kokoro\*  C:\info7375\brutalist.art-latest\runtime\models\kokoro\
robocopy C:\info7375\brutalist.art\runtime\remotion\node_modules C:\info7375\brutalist.art-latest\runtime\remotion\node_modules /E /MT:16
```

Patches: see `toolkit-patches/README.md`.

Every toolkit command from CMD. Note the QUOTED `set`: unquoted `set X=1 && ...` stores `"1 "`.

```
cd /d C:\info7375\brutalist.art-latest
call .venv\Scripts\activate.bat
set "PYTHONUTF8=1"
bash art smoke
```

Result: SMOKE PASS (`logs/art_smoke_2026-10-14_run2.log`).

## Phase 3: brief → beats → audio → review cut (2026-10-14)

Prompts (Claude Code session, summarised): the seven answers were drafted in a claude.ai chat and
pasted in. Claude Code tightened them, and Prathamesh resolved every [CONFIRM] item (FRICTIONAL
15–18). Then: "write beat_sheet.json from PROJECT-BRIEF.md … follow the show-tell schema exactly …
runtime 2:30–3:30 … CONSTRUCTED on every mock-up … real lines dated … no person, logo or instructor
persona". After approval: "shared Manim components … generate Kokoro audio … transcription check …
art run … save every gate report … one frame per beat". Full requests are in FRICTIONAL 19–20.

Commands (Windows CMD), from the film folder `fall-2026\prathamesh-p\final-project-film`:

```
:: 1. beat sheet (keeps measured audio fields when the narration is unchanged)
py -3.13 -I make_sheet.py

:: 2. narration audio (Kokoro af_bella) and the transcription check
cd /d C:\info7375\brutalist.art-latest
call .venv\Scripts\activate.bat
set "PYTHONUTF8=1"
python runtime\scripts\generate_audio_kokoro.py "<film folder>"
python -I "<film folder>\transcribe_check.py" "<film folder>" small

:: 3. review cut: GATE F/L/A/W/B/V, renders manim\B*.mp4, compiles the review mp4.
::    Run it in the FOREGROUND. A background run was orphaned when a session ended (FRICTIONAL 21).
::    Already-rendered clips are reused; to re-render a beat, move manim\<BID>.mp4 to _superseded\ first.
bash art run "<film folder>" --height 1080

:: 4. one frame per beat + contact sheet (gate-reports\frames\, FRAME-CHECK-contact.png)
python -I "<film folder>\frame_check.py" "<film folder>"
```

Result (2026-10-14 17:25 EDT): review cut `honest-shortlist-pitch-slate.mp4`, 194.708 s, with GATE
L/A/W/B/V all passing (V after one fix).

Gate A pre-audit, as the SKILL recommends (Git Bash, from a scratch folder holding ONLY a copy of
`scenes.py`):

```
python runtime/qc/static_scene_check.py scenes.py --class <Class> --quiet
```

## Phase 4: final master (2026-10-14, 1080p by Prathamesh's decision)

Prompt (summarised): "the final master will be 1080p … `art final` at --height 1080, in the
FOREGROUND (use `call bash ...` so the script returns) … GATE T must run on this master."

CMD, as a `.cmd` file. **`call` is required**: without it, a `.cmd` that runs the `bash.cmd` shim never
returns to its next line (FRICTIONAL 22).

```
cd /d C:\info7375\brutalist.art-latest
call .venv\Scripts\activate.bat
set "PYTHONUTF8=1"
call bash art final "<film folder>" --height 1080 --out "<film folder>\final"
```

Result: `final/honest-shortlist-pitch.mp4`, 197.417 s, 1920×1080, 6,295,549 B, SHA-256
`142e91b8ae4b75f46f0515980e966474bca26f1b2df5fa6dc449731dce5bf405`; GATE T PASS.

GATE T by itself (it is also run inside `art final`): `python runtime\scripts\type_check.py "<film folder>"`.

Before committing, redact local paths in logs and reports:
`python -I redact_paths.py logs gate-reports`.
