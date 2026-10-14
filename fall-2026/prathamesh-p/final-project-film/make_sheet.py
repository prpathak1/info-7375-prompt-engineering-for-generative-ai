#!/usr/bin/env python3
"""make_sheet.py: writes beat_sheet.json for the Honest Shortlist pitch film.

Schema follows brutalist.art skills/make/show-tell/reference/example-make_sheet.py (beat(), lane
"manim", shot.type GRAPHIC, shot.manim.class, qc.sparse_by_design). Departures from the skill, as
Prathamesh decided (FRICTIONAL Entries 6/13 of Week 1 and this folder):
  * no BIDEA hesitant writer, no BDEFS terms card, no BHTF Claude composer, no BOUT
    @NikBearBrown outro. No instructor name, persona, credit line, portraits or person beats.
  * narration is Prathamesh's first-person script in Kokoro af_bella, disclosed on screen in B00.
  * every drawing of the proposed system, a shortlist or an interface carries "CONSTRUCTED";
    the persona is labeled "fictional"; real visuals are real log/git lines with their dates.
Source of every claim: PROJECT-BRIEF.md (final, 2026-10-14).
"""
import json
from pathlib import Path

HERE = Path(__file__).resolve().parent
SLUG = "honest-shortlist-pitch"
TITLE = "Honest Shortlist: Final Project Pitch"
VOICE = "af_bella"
WPS = 2.53  # af_bella, measured from logs/art_smoke_2026-10-14_run2.log: 35 words / 13.85 s

SPARSE = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal labels, "
          "the voice carries the explanation. Only underfill and clustered are waived; edge-bleed, "
          "empty-frame and contrast still apply.")


def beat(bid, q, narration, cls, image, show, constructed, labels, real=None):
    b = {"beat_id": bid, "act": "show-tell", "lane": "manim", "proof_gate": "SHOW",
         "pitch_question": q,
         "narration_text": narration,
         "estimated_duration_s": round(len(narration.split()) / WPS + 0.6, 1),
         "voice": VOICE, "engine": "kokoro",
         "qc": {"sparse_by_design": True, "sparse_reason": SPARSE},
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": image, "motion_claim": image,
                  "show": show, "manim": {"class": cls},
                  "on_screen_labels": labels,
                  "constructed": constructed}}
    if real:
        b["shot"]["real_source"] = real
    return b


B = [
 beat("B00", "title",
      "I'm Prathamesh Pathak, pitching Honest Shortlist for an applied AI and agent engineering role. "
      "This synthetic voice is reading my script.",
      "B00_Title",
      "Title stack on the cream stage: 'Honest Shortlist', name, target role; an ink rule draws under the title; "
      "the disclosure line lands last.",
      [{"at": 0.05, "event": "title"}, {"at": 0.3, "event": "rule draws"}, {"at": 0.4, "event": "name + role"},
       {"at": 0.6, "event": "disclosure line"}],
      False,
      ["Honest Shortlist", "Prathamesh Pathak", "Target role: AI / agent engineer (applied AI)",
       "Narration: synthetic voice (Kokoro) reading my script"]),
 beat("B01", "problem (Q6)",
      "A network engineering posting lists skills, city, sometimes pay. On sponsorship, it often says nothing. "
      "For the fictional F one student I'm designing for, that silence is the problem.",
      "B01_Silence",
      "One kraft posting page; three scribble rows fill in (skills, city, pay); the fourth row, 'sponsorship', "
      "stays empty and a ghost question mark grows beside it. Tag: 'fictional F-1 student'.",
      [{"at": 0.1, "event": "page lands"}, {"at": 0.3, "event": "rows fill"}, {"at": 0.6, "event": "empty sponsorship row + ?"}],
      True, ["CONSTRUCTED", "sponsorship", "fictional F-1 student"]),
 beat("B02", "Q1",
      "Honest Shortlist will be a Python and Claude agent that watches public job boards and gives that student "
      "a short daily list of new postings, shipped as a GitHub repo with tests, a held-out evaluation, and a "
      "ten-document packet.",
      "B02_Watch",
      "Three board stacks on the left; postings slide through a narrow gate into a short-list tray; the tray "
      "sits inside an open box tagged 'GitHub repo' with a test page, an eval sheet and a ten-page stack.",
      [{"at": 0.1, "event": "boards"}, {"at": 0.3, "event": "postings flow through gate"}, {"at": 0.6, "event": "repo box + parts"}],
      True, ["CONSTRUCTED", "job boards", "GitHub repo"]),
 beat("B03", "Q1",
      "Each claim, new, location, sponsorship, pay, will be labeled supported, contradicted, or insufficient "
      "against the posting's own text. Liveness will be checked by fetching the board again.",
      "B03_Labels",
      "One shortlist card with four claim rows; a stamp lands on each row (check, cross, dash); a refresh arrow "
      "loops from the card back to a board stack.",
      [{"at": 0.15, "event": "card"}, {"at": 0.35, "event": "stamps land"}, {"at": 0.75, "event": "refresh arrow to board"}],
      True, ["CONSTRUCTED", "supported", "contradicted", "insufficient"]),
 beat("B04", "Q2",
      "Why care? It will show its evidence and say the posting doesn't say, instead of guessing. I haven't "
      "examined alternatives yet. In my first job-search assignment, I will compare LinkedIn job alerts and a "
      "chat assistant.",
      "B04_NotYet",
      "Left: the posting page's empty row stamped 'insufficient'. Right: two plain-text tags, 'LinkedIn job "
      "alerts' and 'chat assistant', under a tag 'not yet examined · JS1, Oct 31'. No logos.",
      [{"at": 0.1, "event": "insufficient stamp"}, {"at": 0.45, "event": "two plain-text tags"}, {"at": 0.7, "event": "not yet · JS1"}],
      True, ["CONSTRUCTED", "insufficient", "LinkedIn job alerts", "chat assistant", "not yet examined · JS1, Oct 31"]),
 beat("B05", "Q3",
      "A hiring manager or engineer screening for that role will read the read-me and sample output, then run "
      "one command, all within a minute. Each claim will link to its posting text, beside an evaluation table "
      "that shows the failures.",
      "B05_SixtySeconds",
      "A 60-second dial; a README page, then one terminal line, then the shortlist card whose claims draw "
      "leader lines to posting text; an eval table beside it with one failure row marked.",
      [{"at": 0.1, "event": "dial starts"}, {"at": 0.3, "event": "README"}, {"at": 0.42, "event": "one command"},
       {"at": 0.6, "event": "claims link to text; eval table with failure row"}],
      True, ["CONSTRUCTED", "60 s", "README", "failures"]),
 beat("B06", "Q4",
      "It will show I can build prompt contracts, with a validator that rejects anything off-schema; an agent loop with "
      "budgets, exits, and a stop the model doesn't control; and permissions enforced in code, with boundary tests.",
      "B06_Skills1",
      "Three blocks rise in a row, each with a small evidence page: contract (a schema slot rejecting a bent "
      "card), loop (a ring with an exit gate), permissions (a fence with an allow-list tag).",
      [{"at": 0.15, "event": "contract block"}, {"at": 0.4, "event": "loop block"}, {"at": 0.7, "event": "permissions block"}],
      True, ["CONSTRUCTED", "contract · JS1", "loop · JS2", "permissions · JS2"]),
 beat("B07", "Q4",
      "Then source grounding with an M C P style tool, verification and versioned memory, a held-out evaluation "
      "with five or more deliberate failures, and a human approval gate bound to the exact shortlist.",
      "B07_Skills2",
      "The row continues: four more blocks rise (grounding, memory, evaluation, gate); the gate block closes "
      "on the shortlist card with a fingerprint seal.",
      [{"at": 0.1, "event": "grounding"}, {"at": 0.3, "event": "memory"}, {"at": 0.5, "event": "evaluation"},
       {"at": 0.72, "event": "gate seals the shortlist"}],
      True, ["CONSTRUCTED", "grounding · JS3", "memory · JS4", "evaluation", "human gate · JS5"]),
 beat("B08", "Q5",
      "Out, by design: no LinkedIn or Indeed scraping, only public Greenhouse, Lever, and Ashby data. And it "
      "will never apply, email, message, or log in.",
      "B08_Fence",
      "A fence with one gate: three board blocks (plain-text names) pass through; four action tags (apply, "
      "email, message, log in) bump the fence and drop away.",
      [{"at": 0.15, "event": "fence"}, {"at": 0.35, "event": "boards pass"}, {"at": 0.65, "event": "actions blocked"}],
      True, ["CONSTRUCTED", "Greenhouse · Lever · Ashby", "never: apply · email · message · log in"]),
 beat("B09", "Q5",
      "First, a one-board watch. Run one will set a baseline. Run two will report only new postings, on a real "
      "second day, or from a saved earlier response, clearly labeled. Anyone will be able to check the raw responses and the diff.",
      "B09_Baseline",
      "Two run trays side by side: run 1 fills a state page and shows '0 new'; run 2 adds two cards that glow; "
      "a diff page between them draws two marked lines.",
      [{"at": 0.15, "event": "run 1 · 0 new"}, {"at": 0.4, "event": "run 2 · new cards"}, {"at": 0.7, "event": "diff draws"}],
      True, ["CONSTRUCTED", "run 1: 0 new", "run 2", "SEEDED if not day 2"]),
 beat("B10", "Q6",
      "The risk: keywords mislead. Visa can be the payments company; authorized to work, without the word "
      "sponsorship, answers neither question. So insufficient will be the default, and public H one B employer "
      "data will stay a separate company signal, never a claim about the posting.",
      "B10_FalseFriends",
      "Two plain-text keyword tags drop onto the posting page: 'Visa' and 'authorized to work'; a ghost check "
      "and cross hover, then an 'insufficient' stamp lands; a company block slides apart, tagged 'employer data'.",
      [{"at": 0.12, "event": "'Visa' tag"}, {"at": 0.3, "event": "'authorized to work' tag"},
       {"at": 0.6, "event": "insufficient stamp"}, {"at": 0.8, "event": "company block set apart"}],
      True, ["CONSTRUCTED", "Visa", "authorized to work", "insufficient", "public H-1B employer data"]),
 beat("B11", "Q7",
      "Writing Python myself, agent loops, policies in code, and evaluations that can say no are new to me. I "
      "already ran the Brutalist toolkit on Windows, diagnosed its failures, and reviewed and approved Claude's "
      "fixes. On my Reallocation recipe, I chose the persona, rules, and dates, while Claude drafted the code.",
      "B11_Have",
      "Left: four outlined, unfilled tool tags ('new to me'). Right, REAL: two dated git log lines typed in a "
      "dark panel (hash, date, subject only; no author, email or paths), captioned 'real · git log'.",
      [{"at": 0.1, "event": "new-to-me tags"}, {"at": 0.4, "event": "panel"}, {"at": 0.55, "event": "line 1"},
       {"at": 0.75, "event": "line 2"}],
      False, ["new to me", "real · git log", "ce1a06c  2026-09-27", "1b5a589  2026-10-03"],
      real={"what": "git log --format='%h %cs %s' (subjects shown as committed)",
            "lines": ["ce1a06c 2026-09-27 Week 01 video: expected vs observed (prathamesh-p)",
                      "1b5a589 2026-10-03 Final sample run + recipe 0.1.2 (DRAFT, sample run passing)"],
            "repos": ["info-7375-prompt-engineering-for-generative-ai (fork)", "the-reallocation-engine (fork)"]}),
 beat("B12", "Q7",
      "How often postings are silent, I don't know yet; I will measure it. Every claim here will be checkable, "
      "and that's the work I want to be hired for.",
      "B12_Measure",
      "The empty-row posting page with a tally sheet beside it; the tally stays blank with a 'to measure · JS1' tag.",
      [{"at": 0.15, "event": "page + blank tally"}, {"at": 0.55, "event": "'to measure' tag"}],
      True, ["CONSTRUCTED", "to measure · JS1"]),
 beat("B13", "exists vs will",
      "Today, the toolkit has passed its smoke test, and my Week 1 and recipe commits exist. Everything else is "
      "planned: the first watch by October thirty-first, and the full system, a stranger run, and a demo by "
      "December twentieth.",
      "B13_ExistsWill",
      "Split stage. Left 'exists today': REAL smoke log lines in a dark panel, dated 2026-10-14. Right 'will "
      "exist': an ink timeline with seven ticks, Oct 21 to Dec 20; hollow dots appear in order (planned).",
      [{"at": 0.1, "event": "left panel: real log lines"}, {"at": 0.4, "event": "right: timeline draws"},
       {"at": 0.7, "event": "Dec 20 tick"}],
      False, ["exists today", "will exist (planned)", "2026-10-14", "Oct 21 · Oct 31 · Nov 10 · Nov 23 · Dec 1 · Dec 13 · Dec 20"],
      real={"what": "logs/art_smoke_2026-10-14_run2.log (verbatim lines; the fixture path in the SMOKE PASS line is elided as …)",
            "lines": ["[smoke] GATE TYPE passed — video + audio streams both decode",
                      "[smoke] GATE AUDIO passed — mean_volume -24.2 dB (floor -40 dB)",
                      "[smoke] SMOKE PASS — … built a real, watchable slate cut end to end."]}),
 beat("B14", "close",
      "Honest Shortlist: every claim will carry its evidence, and silence will be called silence.",
      "B14_Close",
      "The shortlist card settles centre; its sponsorship row shows the 'insufficient' stamp; the title draws beneath.",
      [{"at": 0.1, "event": "card settles"}, {"at": 0.45, "event": "title"}],
      True, ["CONSTRUCTED", "Honest Shortlist"]),
]

sheet = {"metadata": {
    "slug": SLUG, "title": TITLE, "topic": "FINAL PROJECT PITCH", "skill": "show-tell", "style_preset": "show-tell",
    "channel": "student", "persona": "none: Prathamesh's own first-person script, synthetic voice, disclosed in B00",
    "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro", "clock": "narration", "palette": "claude",
    "register": "Plain", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160, "caption_policy": "none",
    "bookend_exempt": ["cold-open", "bidea", "bdefs", "bhtf", "bvdt", "bout"],
    "bookend_exempt_reason": ("Student pitch film: the brief says to narrate as yourself and not to use the instructor's "
                              "name, persona or credit line, so every house bookend is dropped (hesitant writer, terms "
                              "card, Claude composer, @NikBearBrown outro). B00 is a plain title with the synthetic-voice "
                              "disclosure; B14 is a short close."),
    "source_doc": "PROJECT-BRIEF.md (final, 2026-10-14)",
    "playlist": "INFO 7375 Fall 2026", "chapter_number": 0,
    "tags": ["agentic AI", "job search agent", "source grounding", "evaluation", "INFO 7375"]},
    "beats": B}

if __name__ == "__main__":
    # Carry measured audio forward when a beat's narration is unchanged (show-tell gate trap (4):
    # make_sheet.py must keep audio_file + actual_duration_s, or `art run` refuses).
    old = HERE / "beat_sheet.json"
    if old.exists():
        prev = {b["beat_id"]: b for b in json.loads(old.read_text(encoding="utf-8")).get("beats", [])}
        for b in B:
            p = prev.get(b["beat_id"])
            if p and p.get("narration_text") == b["narration_text"]:
                for k in ("audio_file", "actual_duration_s"):
                    if k in p:
                        b[k] = p[k]
    (HERE / "beat_sheet.json").write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    words = sum(len(b["narration_text"].split()) for b in B)
    est = sum(b["estimated_duration_s"] for b in B)
    print(f"{len(B)} beats; {words} words; est {est:.1f} s = {int(est // 60)}:{int(est % 60):02d}")
    for b in B:
        print(f'{b["beat_id"]}\t{b["pitch_question"]}\t{len(b["narration_text"].split())}w\t{b["estimated_duration_s"]}s\t'
              f'{"CONSTRUCTED" if b["shot"]["constructed"] else "real/plain"}')
