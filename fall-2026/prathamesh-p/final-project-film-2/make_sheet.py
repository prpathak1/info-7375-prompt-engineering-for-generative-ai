#!/usr/bin/env python3
"""make_sheet.py: writes beat_sheet.json for the Honest Shortlist final project film.

Narration is read from SCRIPT.md (approved by Prathamesh 2026-11-23), so the sheet cannot drift from it.
The schema follows the pitch film's make_sheet.py (show-tell: lane "manim", shot.manim.class, qc.sparse_by_design).
House bookends are dropped (no instructor persona, name, outro), the voice is disclosed in B00, every mock-up
says CONSTRUCTED, and the SEEDED demo says SEEDED. Measured audio fields are carried forward while a beat's
narration is unchanged (show-tell gate trap (4)).

Run: py -3.13 -I make_sheet.py
"""
import json
import re
from pathlib import Path

HERE = Path(__file__).resolve().parent
WPM = 154  # af_bella, measured on the pitch film (506 words / 197.09 s of generated audio)
VOICE = "af_bella"
narr = dict(re.findall(r'^\*\*(B\d\d)\.\*\* (.+)$', (HERE / "SCRIPT.md").read_text(encoding="utf-8"), re.M))
P1, P2, P3, P4 = "1 executive summary", "2 what others have done", "3 methods", "4 evaluation"
SPARSE = ("show-tell style: one drawn object or scene on a cream stage per beat, minimal labels, the voice carries "
          "the explanation. Only underfill and clustered are waived; edge-bleed, empty-frame and contrast still apply.")

# (beat, part, class, visual, on-screen labels, constructed?, file behind any real line)
V = [
    ("B00", P1, "B00_Title", "Title stack: 'Honest Shortlist', an ink rule, name, film line; the synthetic-voice disclosure lands last.",
     ["Honest Shortlist", "Prathamesh Pathak", "Final project film · INFO 7375 · 2026-11-23",
      "Narration: synthetic voice (Kokoro af_bella)", "reading my script"], False, None),
    ("B01", P1, "B01_Card", "One shortlist card: the 'sponsorship' row threads to a quoted-sentence slip; the last row gets the dash stamp 'posting doesn't say'.",
     ["CONSTRUCTED", "sponsorship", "the sentence it rests on", "posting doesn't say"], True, None),
    ("B02", P1, "B02_Tally", "Seven posting cards in a row; two get a cross (clearance required, inferred), five get a dash (silent); '0 offer sponsorship'.",
     ["7 network postings · 3 employers", "2 clearance required (inferred)", "5 silent", "0 offer sponsorship",
      "Reallocation mode run · 2026-10-20"], False, "Mode WORKED-RUN.md (run 20261020-1348)"),
    ("B03", P1, "B03_History", "'Zoox: 1,364 H-1B approvals' above a real console panel of its three silent network postings.",
     ["Zoox: 1,364 H-1B approvals", "80 Days to Stay · 2026-10-20", "silent  0 sentence(s)  zoox",
      "Senior Network Security Engineer", "Staff Network Security Architect",
      "Senior Manager, Network Engineering & …"], False, "Mode DOMAIN-JUSTIFICATION.md; WORKED-RUN.md Cmds 3-5"),
    ("B04", P2, "B04_Alerts", "Plain text, no logo or UI: one 'documented' line, then three dated notes from Prathamesh's own look.",
     ["LinkedIn alerts: documented, not tested by me", "what I saw · LinkedIn search · 2026-10-31",
      "match reasoning: behind a click", "'without sponsorship': not flagged", "closed postings: still listed"],
     False, "JS1 ALTERNATIVES.md (a), (b)"),
    ("B05", P2, "B05_Chat", "Two verdict columns on the same posting: chat 'Not relevant · 8+ years · silent on sponsorship' vs 'my agent v1: relevant'.",
     ["chat, pasted posting · 2026-10-31", "Not relevant", "8+ years", "sponsorship: posting is silent",
      "my agent v1 · same posting", "relevant", "Zoox · Senior Network Security Engineer"],
     False, "JS1 ACTION-SURFACES.md (a)"),
    ("B06", P2, "B06_Dropped", "Two real console lines, then two bars to scale: 22 vs 653; '631 dropped · no error'.",
     ["[lever] Shield AI: found 22 jobs", "[lever-full] shieldai: 653 postings", "22", "653",
      "631 dropped · no error", "real console · 2026-10-20"], False, "Mode WORKED-RUN.md Cmd 1 and Cmds 3-5"),
    ("B07", P2, "B07_Grid", "Three-by-three grid of stamps: rows LinkedIn alerts / chat assistant / Honest Shortlist (planned); columns watches / evidence / says silent.",
     ["CONSTRUCTED · my summary", "watches", "evidence", "says silent", "LinkedIn alerts", "chat assistant",
      "Honest Shortlist", "(planned)"], True, None),
    ("B08", P3, "B08_Pipeline", "Six blocks joined by arrows: fetch, new only, title rule, extract, label, re-fetch + approve; status above each: RAN / IN MODE / PLANNED.",
     ["CONSTRUCTED", "Greenhouse · Lever · Ashby (public)", "RAN", "IN MODE", "PLANNED", "fetch", "new only",
      "title rule", "extract", "label", "re-fetch", "approve", "never: apply · email · message · log in"], True, None),
    ("B09", P3, "B09_LiveRun", "Real terminal panel from the JS2 live run; a dot marks the 404 line.",
     ["real · JS2 live run · 2026-11-10 09:52 EST", "[loop] status=incomplete exit=3",
      "boards=4 requests=4/6 seconds=8.757/120", "lever-zoox  ok  postings=234 new=31",
      "...-js2-does-not-exist  failed_http_404", "attempts=1  no retry (GATE section 4)"],
     False, "JS2 demo/01-live-run.txt"),
    ("B10", P3, "B10_NewOnly", "The zoox line with 'new=31' ringed; below, the real false-friend test name.",
     ["lever-zoox  ok  postings=234 new=31", "new vs my 2026-10-31 state (227 IDs)",
      "Rule.test_road_network_tools_is_not_", "relevant_in_real_day1_data", "false friend: 'Road Network Tools'"],
     False, "JS2 demo/01-live-run.txt, README.md; JS1 README.md"),
    ("B11", P3, "B11_Extract", "Real extraction line tagged IN MODE; below, three planned label stamps.",
     ["IN MODE · 2026-10-20", "has-sentences  2 sentence(s)  shieldai", "Network Engineer (R4843)",
      "fields=additionalPlain,descriptionPlain,lists", "CONSTRUCTED · PLANNED", "supported", "contradicted",
      "insufficient (default)"], True, "Mode WORKED-RUN.md Cmds 3-5 (the console line only)"),
    ("B12", P3, "B12_Validator", "Real test name and 'Ran 50 tests, OK' tagged RAN; two grey planned blocks: re-fetch, my approval.",
     ["RAN · JS1 · 2026-10-31", "Validator.test_rejects_uncited_or_", "fabricated_justification", "Ran 50 tests, OK",
      "CONSTRUCTED · PLANNED", "re-fetch", "my approval"], True, "JS1 README.md (the panel only)"),
    ("B13", P3, "B13_Resources", "Checklist: three checked rows and one dash row.",
     ["boards: public, no account", "compute: my laptop · Python stdlib", "Claude: my Claude Code subscription",
      "50 judge calls in JS1 · 2026-10-31", "daily runs, many boards: not measured"],
     False, "JS1 experiment/REPORT.md, SAMPLING-REPORT.md, README.md"),
    ("B14", P4, "B14_Baseline", "Real result rows from the JS1 experiment; a cross stamp: 'pass rate alone proved nothing'.",
     ["real · JS1 experiment · 2026-10-31", "labels: 20 of 20 'not fit'", "always not_relevant: dev 10/10",
      "always not_relevant: held-out 10/10", "100%", "pass rate alone proved nothing"],
     False, "JS1 experiment/REPORT.md"),
    ("B15", P4, "B15_HeldOut", "Planned held-out tray of cards in three groups; two empty meters: false positives, false negatives.",
     ["CONSTRUCTED · PLANNED", "about 40 postings · more boards", "labelled by me before any output",
      "entry-level fits", "not fit", "false friends", "false positives", "false negatives"], True, None),
    ("B16", P4, "B16_Seeded", "Real SEEDED panel: agent 'finished exit=0', verify 'FAIL … 826 ids'; then the planned success bar.",
     ["SEEDED · constructed empty response · 2026-11-10", "[loop] *** SEEDED *** status=finished",
      "exit=0  ashby-openai  ok_empty  new=0", "verify.py [SEEDED]: FAIL", "posting count is 0 but the previous",
      "snapshot had 826 ids", "worked if (planned):", "most real fits found", "no clearance/citizen-only 'relevant'",
      "beats always-insufficient", "verify catches every planted failure"],
     False, "JS2 demo/02-seeded-finished-but-wrong.txt (criteria: Prathamesh's decision 2026-11-23)"),
    ("B17", P4, "B17_Close", "Failure bar and reported rate, then the close: 'Honest Shortlist' and the closing line.",
     ["zero tolerance: 'relevant' when sponsorship is ruled out", "missed real fits: a rate I report",
      "Honest Shortlist", "every claim carries its evidence"], False, None),
]

assert [v[0] for v in V] == sorted(narr), "SCRIPT.md beats and the visual plan differ"
B = []
for bid, part, cls, vis, labels, constructed, src in V:
    t = narr[bid]
    n = len(t.split())
    b = {"beat_id": bid, "act": "show-tell", "film_part": part, "lane": "manim", "proof_gate": "SHOW",
         "narration_text": t, "word_count": n, "estimated_duration_s": round(n / WPM * 60, 1),
         "voice": VOICE, "engine": "kokoro",
         "qc": {"sparse_by_design": True, "sparse_reason": SPARSE},
         "shot": {"type": "GRAPHIC", "source": "own", "visual_intent": vis, "motion_claim": vis,
                  "show": [{"at": 0.05, "event": "first element"}, {"at": 0.3, "event": "main element"},
                           {"at": 0.65, "event": "accent"}],
                  "manim": {"class": cls}, "on_screen_labels": labels, "constructed": constructed}}
    if src:
        b["shot"]["real_source"] = src
    B.append(b)

sheet = {"metadata": {
    "slug": "honest-shortlist-final", "title": "Honest Shortlist: Final Project Film", "topic": "FINAL PROJECT FILM",
    "skill": "show-tell", "style_preset": "show-tell", "channel": "student",
    "persona": "none: Prathamesh's own first-person script, synthetic voice, disclosed in B00",
    "voice": VOICE, "voice_kokoro": VOICE, "engine": "kokoro", "clock": "narration", "palette": "claude",
    "register": "Plain", "fps": 24, "aspect_ratio": "16:9", "width": 3840, "height": 2160, "caption_policy": "none",
    "bookend_exempt": ["cold-open", "bidea", "bdefs", "bhtf", "bvdt", "bout"],
    "bookend_exempt_reason": ("Student film: narrated as myself, with no instructor name, persona, credit line or outro "
                              "(same as the pitch film). B00 is a plain title with the synthetic-voice disclosure; "
                              "B17 is a short close."),
    "source_doc": "SCRIPT.md (approved 2026-11-23)", "playlist": "INFO 7375 Fall 2026", "chapter_number": 0,
    "tags": ["agentic AI", "job search agent", "source grounding", "evaluation", "INFO 7375"]},
    "beats": B}

if __name__ == "__main__":
    old = HERE / "beat_sheet.json"
    if old.exists():
        prev = {b["beat_id"]: b for b in json.loads(old.read_text(encoding="utf-8")).get("beats", [])}
        for b in B:
            p = prev.get(b["beat_id"])
            if p and p.get("narration_text") == b["narration_text"]:
                for k in ("audio_file", "actual_duration_s"):
                    if k in p:
                        b[k] = p[k]
    old.write_text(json.dumps(sheet, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    words = sum(b["word_count"] for b in B)
    est = sum(b["estimated_duration_s"] for b in B)
    print(f"{len(B)} beats; {words} words; est {est:.1f} s = {int(est // 60)}:{int(est % 60):02d}")
