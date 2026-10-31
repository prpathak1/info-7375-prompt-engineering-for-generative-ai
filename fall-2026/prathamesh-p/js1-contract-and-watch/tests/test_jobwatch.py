"""Tests for JS1, written from CONTRACT.md (APPROVED 2026-10-30 18:21:29 EDT) before any implementation exists.

Interface these tests assume. The implementation must provide it in ../jobwatch.py:

    check_url(url) -> None                  raises HostRefused unless https://api.lever.co (default port, no userinfo)
    fetch(board, dest_dir, urlopen=...)      one GET; refuses an off-host final URL (redirect); writes nothing on refusal
    load_resume(path) -> dict               raises ResumeRefused unless fictional is True and email ends @example.com
    decide(posting, resume) -> record       {"label": "record", "verdict", "needs_human", "reason", "gate_results", "citations"}
    check_citations(citations, posting, resume) -> list[str]   error strings; empty list = every citation is grounded
    validate_judgment(raw_text, posting, resume) -> dict       raises JudgmentRejected on anything off-schema or uncited
    run(raw_path, state_path, out_path, resume, judge=None) -> report
        report = {"baseline": bool, "total": int, "new_count": int, "removed_count": int,
                  "new": [{"posting_id", "posting_title", "record", "judgment"}]}
        state file  = {"ids": [...]}; written only after a successful run

Field-path conventions (CONTRACT section 2):
  posting_field: "text", "descriptionPlain", "additionalPlain", "lists" (every lists[].content with tags stripped,
                 joined), or a dotted path such as "categories.location". posting_value must be a case-insensitive
                 substring of that field in the same posting.
  resume_field:  a dotted path into the résumé. If the value at the path is a list, resume_value must be an element of it
                 (case-insensitive). If it is a scalar, resume_value must equal it (strings: case-insensitive substring).

Run: python -I -m unittest discover -s tests -v   (from js1-contract-and-watch/)
"""
from __future__ import annotations

import copy
import json
import re
import sys
import tempfile
import types
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

import jobwatch  # noqa: E402  (does not exist yet: every test errors until it is implemented)

RESUME_PATH = ROOT / "fixtures" / "resume.fictional.json"
RAW_DAY1 = ROOT / "raw" / "2026-10-30" / "zoox.json"
HAND_LABELS = HERE / "hand_labels.json"


def posting(pid, title, description="", lists=None, additional=""):
    """Minimal Lever-shaped posting with only the fields the rule reads."""
    return {
        "id": pid,
        "text": title,
        "categories": {"location": "Foster City, CA", "team": "Test", "commitment": "Full-time"},
        "descriptionPlain": description,
        "lists": lists or [],
        "additionalPlain": additional,
    }


RELEVANT_DESC = "You will operate our BGP and OSPF backbone and manage firewall policy across sites."


class Base(unittest.TestCase):
    def setUp(self):
        self.resume = jobwatch.load_resume(RESUME_PATH)
        self.tmp = tempfile.TemporaryDirectory()
        self.dir = Path(self.tmp.name)

    def tearDown(self):
        self.tmp.cleanup()

    def write_raw(self, name, postings):
        p = self.dir / name
        p.write_text(json.dumps(postings), encoding="utf-8")
        return p

    def assert_grounded(self, citations, post):
        self.assertTrue(citations, "justification has no citations")
        self.assertTrue(any(c["resume_field"] for c in citations), "no résumé field cited")
        self.assertTrue(any(c["posting_field"] for c in citations), "no posting field cited")
        self.assertEqual(jobwatch.check_citations(citations, post, self.resume), [])


# ---------------------------------------------------------------- Refuses: allow-list (CONTRACT section 3)
class AllowList(unittest.TestCase):
    def test_accepts_lever_https(self):
        jobwatch.check_url("https://api.lever.co/v0/postings/zoox?mode=json")  # no exception

    def test_refuses_off_list_hosts(self):
        for url in [
            "https://boards-api.greenhouse.io/v1/boards/zoox/jobs",
            "https://jobs.lever.co/zoox",                       # Lever, but not the API host
            "https://api.lever.co.evil.example/v0/postings/zoox",  # lookalike suffix
            "https://evil.example/v0/postings/zoox?h=api.lever.co",
            "https://api.lever.co@evil.example/v0/postings/zoox",  # userinfo trick; real host is evil.example
            "https://API.LEVER.CO.evil.example/",
        ]:
            with self.subTest(url=url), self.assertRaises(jobwatch.HostRefused):
                jobwatch.check_url(url)

    def test_refuses_non_https_and_odd_ports(self):
        for url in ["http://api.lever.co/v0/postings/zoox?mode=json",
                    "ftp://api.lever.co/x",
                    "https://api.lever.co:8443/v0/postings/zoox"]:
            with self.subTest(url=url), self.assertRaises(jobwatch.HostRefused):
                jobwatch.check_url(url)

    def test_refuses_redirect_off_host_and_writes_nothing(self):
        class FakeResp:
            status = 200
            headers = {}
            def geturl(self): return "https://evil.example/landing"
            def read(self): return b"[]"
            def __enter__(self): return self
            def __exit__(self, *a): return False

        with tempfile.TemporaryDirectory() as d:
            with self.assertRaises(jobwatch.HostRefused):
                jobwatch.fetch("zoox", Path(d), urlopen=lambda *a, **k: FakeResp())
            self.assertEqual(list(Path(d).rglob("*")), [], "refused fetch must write no files")

    def test_source_has_one_get_and_no_send_paths(self):
        src = (ROOT / "jobwatch.py").read_text(encoding="utf-8")
        self.assertEqual(src.count("urlopen("), 1, "exactly one network call site")
        for forbidden in ("smtplib", '"POST"', "'POST'", "http.client", "import requests"):
            with self.subTest(forbidden=forbidden):
                self.assertNotIn(forbidden, src)


# ---------------------------------------------------------------- Refuses: real résumé (CONTRACT section 3)
class ResumeLoader(unittest.TestCase):
    def _write(self, d, data):
        p = Path(d) / "r.json"
        p.write_text(json.dumps(data), encoding="utf-8")
        return p

    def test_accepts_fictional_fixture(self):
        r = jobwatch.load_resume(RESUME_PATH)
        self.assertIs(r["fictional"], True)

    def test_refuses_without_fictional_true(self):
        base = json.loads(RESUME_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as d:
            for label, mutate in [
                ("missing", lambda r: r.pop("fictional")),
                ("false", lambda r: r.__setitem__("fictional", False)),
                ("string 'true'", lambda r: r.__setitem__("fictional", "true")),
                ("int 1", lambda r: r.__setitem__("fictional", 1)),
            ]:
                r = copy.deepcopy(base)
                mutate(r)
                with self.subTest(label), self.assertRaises(jobwatch.ResumeRefused):
                    jobwatch.load_resume(self._write(d, r))

    def test_refuses_non_example_email(self):
        base = json.loads(RESUME_PATH.read_text(encoding="utf-8"))
        with tempfile.TemporaryDirectory() as d:
            for email in ["someone@gmail.com", "x@example.com.evil.org", "", None]:
                r = copy.deepcopy(base)
                r["personal"]["email"] = email
                with self.subTest(email=email), self.assertRaises(jobwatch.ResumeRefused):
                    jobwatch.load_resume(self._write(d, r))


# ---------------------------------------------------------------- Rule: hand-predictable cases (CONTRACT section 4)
class Rule(Base):
    def verdict(self, post):
        return jobwatch.decide(post, self.resume)

    def test_road_network_tools_is_not_relevant_synthetic(self):
        r = self.verdict(posting("p1", "Software Engineer - Road Network Tools", RELEVANT_DESC))
        self.assertEqual(r["label"], "record")
        self.assertEqual(r["verdict"], "not_relevant")
        self.assertEqual(r["gate_results"]["title"]["decision"], "exclude")
        self.assertIn("road network", r["reason"].lower())
        self.assertFalse(r["needs_human"])

    def test_road_network_tools_is_not_relevant_in_real_day1_data(self):
        data = json.loads(RAW_DAY1.read_text(encoding="utf-8"))
        hits = [p for p in data if p["text"] == "Software Engineer - Road Network Tools"]
        self.assertEqual(len(hits), 1, "expected the real posting in raw/2026-10-30/zoox.json")
        r = self.verdict(hits[0])
        self.assertEqual(r["verdict"], "not_relevant")
        self.assertEqual(r["gate_results"]["title"]["decision"], "exclude")

    def test_other_false_friends_and_no_network(self):
        for title in ["Social Network Analyst", "Neural Network Research Scientist",
                      "Sales Network Manager", "Data Engineer", "Networked Systems Recruiter"]:
            with self.subTest(title=title):
                r = self.verdict(posting("p", title, RELEVANT_DESC))
                self.assertEqual(r["verdict"], "not_relevant")
                self.assertEqual(r["gate_results"]["title"]["decision"], "exclude")

    def test_include_title_with_two_skills_and_no_auth_text_is_relevant(self):
        post = posting("p2", "Senior Network Security Engineer", RELEVANT_DESC)
        r = self.verdict(post)
        self.assertEqual(r["verdict"], "relevant")
        self.assertFalse(r["needs_human"])
        self.assertEqual(r["gate_results"]["title"]["decision"], "include")
        self.assertGreaterEqual(len(r["gate_results"]["skills"]["matched"]), 2)
        self.assert_grounded(r["citations"], post)
        fields = {c["resume_field"] for c in r["citations"]}
        self.assertIn("skills.networking", fields)

    def test_flag_software_networking_is_not_relevant_with_needs_human(self):
        post = posting("p3", "Software Engineer, Networking & OS", RELEVANT_DESC)
        r = self.verdict(post)
        self.assertEqual(r["verdict"], "not_relevant")
        self.assertTrue(r["needs_human"])
        self.assertEqual(r["gate_results"]["title"]["decision"], "flag")
        self.assertTrue(r["reason"])
        # gates 2 and 3 are still evaluated and recorded for flagged postings
        self.assertIn("authorization", r["gate_results"])
        self.assertIn("skills", r["gate_results"])

    def test_flag_network_without_role_word(self):
        r = self.verdict(posting("p4", "Network Planner", RELEVANT_DESC))
        self.assertEqual(r["verdict"], "not_relevant")
        self.assertTrue(r["needs_human"])

    def test_verdict_is_two_valued(self):
        for title in ["Network Engineer", "Software Engineer, Networking", "Road Network Tools", "Chef"]:
            with self.subTest(title=title):
                self.assertIn(self.verdict(posting("p", title, RELEVANT_DESC))["verdict"],
                              {"relevant", "not_relevant"})

    def test_auth_gate_phrases_make_not_relevant_and_cite_visa(self):
        for field, text in [
            ("descriptionPlain", RELEVANT_DESC + " Applicants must be a U.S. citizen."),
            ("descriptionPlain", RELEVANT_DESC + " Requires an active security clearance."),
            ("additionalPlain", "This role is subject to ITAR."),
            ("lists", "<li>Must qualify as a <b>U.S. person</b> under export control rules</li>"),
        ]:
            with self.subTest(field=field, text=text):
                if field == "descriptionPlain":
                    post = posting("p5", "Network Engineer", text)
                elif field == "additionalPlain":
                    post = posting("p5", "Network Engineer", RELEVANT_DESC, additional=text)
                else:
                    post = posting("p5", "Network Engineer", RELEVANT_DESC,
                                   lists=[{"text": "Requirements", "content": text}])
                r = self.verdict(post)
                self.assertEqual(r["verdict"], "not_relevant")
                self.assertTrue(r["gate_results"]["authorization"]["hits"])
                self.assert_grounded(r["citations"], post)
                fields = {c["resume_field"] for c in r["citations"]}
                self.assertIn("visa.needs_sponsorship", fields)

    def test_auth_phrase_ear_is_whole_word(self):
        post = posting("p6", "Network Engineer", RELEVANT_DESC + " Linear growth; clear goals; yearly review.")
        r = self.verdict(post)
        self.assertEqual(r["gate_results"]["authorization"]["hits"], [])
        self.assertEqual(r["verdict"], "relevant")

    def test_auth_phrases_all_whole_word(self):
        # CONTRACT Gate 2 (amended 2026-10-30): every phrase is whole-word, case-insensitive, not only "EAR".
        # "military" must not trip ITAR; "years"/"dear" must not trip EAR; "US citizenry" must not trip "US citizen".
        post = posting("p6b", "Network Engineer",
                       RELEVANT_DESC + " 5+ years supporting military customers. Dear applicant: US citizenry welcome.")
        r = self.verdict(post)
        self.assertEqual(r["gate_results"]["authorization"]["hits"], [])
        self.assertEqual(r["verdict"], "relevant")

    def test_auth_phrases_allow_plural_s(self):
        # CONTRACT Gate 2 (amended 2026-10-30 18:38:50): a phrase may be followed by a single "s", as in Gate 3
        for extra, expect in [(" Applicants must be U.S. citizens.", "U.S. citizens"),
                              (" Candidates must hold security clearances.", "security clearances"),
                              (" Open only to U.S. persons.", "U.S. persons")]:
            with self.subTest(extra=extra):
                post = posting("p6d", "Network Engineer", RELEVANT_DESC + extra)
                r = self.verdict(post)
                self.assertEqual(r["verdict"], "not_relevant")
                self.assertIn(expect.lower(), [h["matched"].lower() for h in r["gate_results"]["authorization"]["hits"]])
                self.assert_grounded(r["citations"], post)

    def test_auth_sponsorship_refusal_phrases(self):
        # CONTRACT Gate 2 (amended 2026-10-31 14:16:58): sponsorship-refusal phrases, from Prathamesh's LinkedIn check
        pw = " Candidates must be authorized to work in the U.S. without sponsorship."  # Parallel Wireless wording
        cases = [pw, " We offer this role without visa sponsorship.", " No sponsorship is offered for this role.",
                 " Zoox will not sponsor work visas.", " We are unable to sponsor applicants.",
                 " The company cannot sponsor visas.", " Zoox does not sponsor H-1B.", " We do not sponsor visas."]
        for extra in cases:
            with self.subTest(extra=extra):
                post = posting("p6e", "Network Engineer", RELEVANT_DESC + extra)
                r = self.verdict(post)
                self.assertTrue(r["gate_results"]["authorization"]["hits"])
                self.assertEqual(r["verdict"], "not_relevant")
                self.assert_grounded(r["citations"], post)
                self.assertIn("visa.needs_sponsorship", {c["resume_field"] for c in r["citations"]})

    def test_sponsorship_available_is_not_a_hit(self):
        # a bare "sponsorship" is deliberately not a phrase
        for extra in [" Visa sponsorship available.", " We offer H-1B sponsorship.", " Sponsorship: yes."]:
            with self.subTest(extra=extra):
                r = self.verdict(posting("p6f", "Network Engineer", RELEVANT_DESC + extra))
                self.assertEqual(r["gate_results"]["authorization"]["hits"], [])
                self.assertEqual(r["verdict"], "relevant")

    def test_auth_phrase_hyphen_is_a_boundary(self):
        # whole word means no letter/digit/underscore on either side; a hyphen is a boundary
        post = posting("p6c", "Network Engineer", RELEVANT_DESC + " This work is ITAR-controlled.")
        r = self.verdict(post)
        self.assertTrue(r["gate_results"]["authorization"]["hits"])
        self.assertEqual(r["verdict"], "not_relevant")
        self.assert_grounded(r["citations"], post)

    def test_skills_threshold_is_two(self):
        one = posting("p7", "Network Engineer", "You will run our BGP edge.")
        two = posting("p8", "Network Engineer", "You will run our BGP edge and DNS.")
        self.assertEqual(self.verdict(one)["verdict"], "not_relevant")
        self.assertEqual(self.verdict(two)["verdict"], "relevant")

    def test_skills_match_whole_word_case_insensitive_plural_s(self):
        # CONTRACT Gate 3 (amended 2026-10-30): term or term+"s" as a whole word, case-insensitive.
        # "bgp" matches BGP; "firewalls" matches firewall.
        post = posting("p9", "Network Engineer", "bgp experience; manage firewalls.")
        r = self.verdict(post)
        self.assertEqual(sorted(m.lower() for m in r["gate_results"]["skills"]["matched"]), ["bgp", "firewall"])
        self.assertEqual(r["verdict"], "relevant")
        self.assert_grounded(r["citations"], post)
        values = {c["posting_value"].lower() for c in r["citations"] if c["resume_field"] == "skills.networking"}
        self.assertIn("firewalls", values)

    def test_skills_plural_rule_still_requires_whole_word(self):
        # only "s" is allowed after the term; other suffixes and prefixes do not match
        r = self.verdict(posting("p9b", "Network Engineer", "firewalling, BGPx, eBGP, DNSSEC, rerouting."))
        self.assertEqual(r["gate_results"]["skills"]["matched"], [])
        self.assertEqual(r["verdict"], "not_relevant")

    def test_skills_read_lists_content_with_tags_stripped(self):
        post = posting("p10", "Network Architect", "",
                       lists=[{"text": "Qualifications", "content": "<li><b>OSPF</b></li><li>VLAN design</li>"}])
        r = self.verdict(post)
        self.assertEqual(r["verdict"], "relevant")
        self.assert_grounded(r["citations"], post)

    def test_location_is_not_a_criterion(self):
        a = posting("p11", "Network Engineer", RELEVANT_DESC)
        b = copy.deepcopy(a)
        b["categories"]["location"] = "Remote - Antarctica"
        self.assertEqual(self.verdict(a)["verdict"], self.verdict(b)["verdict"])

    def test_hand_labels_if_present(self):
        if not HAND_LABELS.exists():
            self.skipTest("tests/hand_labels.json not written yet (Prathamesh hand-labels >= 5 real postings)")
        labels = json.loads(HAND_LABELS.read_text(encoding="utf-8"))
        data = {p["id"]: p for p in json.loads(RAW_DAY1.read_text(encoding="utf-8"))}
        self.assertGreaterEqual(len(labels), 5)
        for row in labels:
            with self.subTest(id=row["posting_id"]):
                self.assertEqual(self.verdict(data[row["posting_id"]])["verdict"], row["verdict"])


# ---------------------------------------------------------------- W1: uncited / fabricated justification
class W1UncitedJustification(Base):
    def test_every_record_citation_is_grounded(self):
        posts = [
            posting("a", "Network Engineer", RELEVANT_DESC),
            posting("b", "Network Engineer", RELEVANT_DESC + " Must be a US citizen."),
            posting("c", "Software Engineer - Road Network Tools", RELEVANT_DESC),
            posting("d", "Software Engineer, Networking", RELEVANT_DESC),
            posting("e", "Network Engineer", "Only BGP here."),
            posting("f", "Barista", ""),
        ]
        for p in posts:
            with self.subTest(id=p["id"]):
                self.assert_grounded(jobwatch.decide(p, self.resume)["citations"], p)

    def test_one_skill_posting_cites_exactly_that_one_term(self):
        post = posting("g", "Network Engineer", "You will own BGP peering.")
        r = jobwatch.decide(post, self.resume)
        self.assertEqual(r["verdict"], "not_relevant")
        skill_cites = [c for c in r["citations"] if c["resume_field"] == "skills.networking"]
        self.assertEqual([c["resume_value"] for c in skill_cites], ["BGP"])

    def test_check_citations_catches_fabrication(self):
        post = posting("h", "Network Engineer", "You will own BGP peering.")
        bad = [
            # posting never mentions OSPF
            {"resume_field": "skills.networking", "resume_value": "OSPF",
             "posting_field": "descriptionPlain", "posting_value": "OSPF"},
            # résumé has no MPLS under skills.networking
            {"resume_field": "skills.networking", "resume_value": "MPLS",
             "posting_field": "descriptionPlain", "posting_value": "BGP"},
            # path does not exist in résumé
            {"resume_field": "skills.telepathy", "resume_value": "BGP",
             "posting_field": "descriptionPlain", "posting_value": "BGP"},
            # posting field does not exist
            {"resume_field": "skills.networking", "resume_value": "BGP",
             "posting_field": "secretField", "posting_value": "BGP"},
        ]
        for c in bad:
            with self.subTest(c=c):
                self.assertNotEqual(jobwatch.check_citations([c], post, self.resume), [])


# ---------------------------------------------------------------- Validator: Claude judgment schema (CONTRACT sections 2-3)
class Validator(Base):
    def setUp(self):
        super().setUp()
        self.post = posting("v1", "Network Engineer", RELEVANT_DESC)
        self.good = {
            "posting_id": "v1",
            "verdict": "relevant",
            "citations": [{"resume_field": "skills.networking", "resume_value": "BGP",
                           "posting_field": "descriptionPlain", "posting_value": "BGP"}],
        }

    def test_accepts_good_output_and_labels_it_judgment(self):
        out = jobwatch.validate_judgment(json.dumps(self.good), self.post, self.resume)
        self.assertEqual(out["label"], "judgment")
        self.assertEqual(out["verdict"], "relevant")

    def test_rejects_off_schema(self):
        g = self.good
        cases = {
            "not json": "The posting looks relevant.",
            "json in prose": "Sure! " + json.dumps(g),
            "list not object": json.dumps([g]),
            "missing verdict": json.dumps({k: v for k, v in g.items() if k != "verdict"}),
            "missing citations": json.dumps({k: v for k, v in g.items() if k != "citations"}),
            "extra key": json.dumps({**g, "confidence": 0.9}),
            "third verdict value": json.dumps({**g, "verdict": "maybe"}),
            "verdict wrong case": json.dumps({**g, "verdict": "Relevant"}),
            "empty citations": json.dumps({**g, "citations": []}),
            "citations not list": json.dumps({**g, "citations": "BGP"}),
            "citation extra key": json.dumps({**g, "citations": [{**g["citations"][0], "note": "x"}]}),
            "citation missing key": json.dumps({**g, "citations": [{"resume_field": "skills.networking",
                                                                    "resume_value": "BGP"}]}),
            "wrong posting id": json.dumps({**g, "posting_id": "someone-else"}),
            "self-labeled record": json.dumps({**g, "label": "record"}),
        }
        for name, raw in cases.items():
            with self.subTest(name), self.assertRaises(jobwatch.JudgmentRejected):
                jobwatch.validate_judgment(raw, self.post, self.resume)

    def test_rejects_uncited_or_fabricated_justification(self):
        fabricated = {**self.good, "citations": [{"resume_field": "skills.networking", "resume_value": "VLAN",
                                                  "posting_field": "descriptionPlain", "posting_value": "VLAN"}]}
        with self.assertRaises(jobwatch.JudgmentRejected):
            jobwatch.validate_judgment(json.dumps(fabricated), self.post, self.resume)


# ---------------------------------------------------------------- Watch: baseline, new-only, W2, state safety (section 6)
class Watch(Base):
    def test_baseline_reports_zero_new_and_saves_state(self):
        raw = self.write_raw("d1.json", [posting("a", "Network Engineer", RELEVANT_DESC),
                                         posting("b", "Barista")])
        state = self.dir / "state" / "seen_ids.json"
        rep = jobwatch.run(raw, state, self.dir / "out1.json", self.resume)
        self.assertTrue(rep["baseline"])
        self.assertEqual(rep["new_count"], 0)
        self.assertEqual(rep["new"], [])
        self.assertTrue(state.exists())
        self.assertTrue({"a", "b"} <= set(json.loads(state.read_text(encoding="utf-8"))["ids"]))

    def test_baseline_on_real_day1_zoox_reports_zero_new(self):
        state = self.dir / "seen_ids.json"
        rep = jobwatch.run(RAW_DAY1, state, self.dir / "out.json", self.resume)
        self.assertEqual(rep["new_count"], 0)
        self.assertEqual(rep["total"], 227)

    def test_second_run_reports_only_unseen_ids(self):
        state = self.dir / "seen_ids.json"
        d1 = self.write_raw("d1.json", [posting("a", "Network Engineer", RELEVANT_DESC), posting("b", "Barista")])
        d2 = self.write_raw("d2.json", [posting("b", "Barista"),                 # still there: not new
                                        posting("c", "Network Architect", RELEVANT_DESC),  # new
                                        posting("d", "Chef")])                    # new
        jobwatch.run(d1, state, self.dir / "o1.json", self.resume)
        rep = jobwatch.run(d2, state, self.dir / "o2.json", self.resume)
        self.assertFalse(rep["baseline"])
        self.assertEqual(sorted(n["posting_id"] for n in rep["new"]), ["c", "d"])
        self.assertEqual(rep["new_count"], 2)
        self.assertEqual(rep["removed_count"], 1)  # "a" disappeared; logged as a count only

    def test_state_equals_exactly_current_run_ids(self):
        # CONTRACT section 6: state holds exactly the last successful run's ID set, not a union of runs
        state = self.dir / "seen_ids.json"
        jobwatch.run(self.write_raw("d1.json", [posting("a", "Chef"), posting("b", "Barista")]),
                     state, self.dir / "o1.json", self.resume)
        self.assertEqual(set(json.loads(state.read_text(encoding="utf-8"))["ids"]), {"a", "b"})
        jobwatch.run(self.write_raw("d2.json", [posting("b", "Barista"), posting("c", "Network Engineer")]),
                     state, self.dir / "o2.json", self.resume)
        ids = json.loads(state.read_text(encoding="utf-8"))["ids"]
        self.assertEqual(set(ids), {"b", "c"})
        self.assertEqual(len(ids), 2, "no duplicate IDs in state")

    def test_seeded_label_is_carried_in_report(self):
        # CONTRACT section 6: seeded output is labeled SEEDED in its header (the report itself), not only its filename
        state = self.dir / "s.json"
        jobwatch.run(self.write_raw("d1.json", []), state, self.dir / "o1.json", self.resume, label="SEEDED")
        rep = jobwatch.run(self.write_raw("d2.json", [posting("x", "Chef")]), state, self.dir / "o2.json",
                           self.resume, label="SEEDED")
        self.assertEqual(rep["label"], "SEEDED")
        self.assertEqual(json.loads((self.dir / "o2.json").read_text(encoding="utf-8"))["label"], "SEEDED")
        real = jobwatch.run(self.write_raw("d3.json", []), self.dir / "s3.json", self.dir / "o3.json", self.resume)
        self.assertNotIn("label", real)

    def test_rerun_same_day_reports_zero_new(self):
        state = self.dir / "seen_ids.json"
        d1 = self.write_raw("d1.json", [posting("a", "Network Engineer", RELEVANT_DESC)])
        jobwatch.run(d1, state, self.dir / "o1.json", self.resume)
        self.assertEqual(jobwatch.run(d1, state, self.dir / "o2.json", self.resume)["new_count"], 0)

    def test_failed_run_leaves_state_untouched(self):
        state = self.dir / "seen_ids.json"
        d1 = self.write_raw("d1.json", [posting("a", "Network Engineer", RELEVANT_DESC)])
        jobwatch.run(d1, state, self.dir / "o1.json", self.resume)
        before = state.read_bytes()
        broken = self.dir / "broken.json"
        broken.write_text("{not json", encoding="utf-8")
        with self.assertRaises(Exception):
            jobwatch.run(broken, state, self.dir / "o2.json", self.resume)
        self.assertEqual(state.read_bytes(), before)

    def test_W2_verdict_attached_to_correct_posting(self):
        state = self.dir / "seen_ids.json"
        relevant = posting("R", "Senior Network Security Engineer", RELEVANT_DESC)
        not_rel = posting("N", "Software Engineer - Road Network Tools", "Maps and lanes.")
        # day 1: only N exists. day 2: the old posting N comes FIRST and only R (second) is new, so a verdict
        # taken by list position from the unfiltered list would be N's. (Strengthened 2026-10-30: the earlier
        # order [R, N] put the new posting at index 0, and a positional mutant passed by coincidence.)
        jobwatch.run(self.write_raw("d1.json", [not_rel]), state, self.dir / "o1.json", self.resume)
        rep = jobwatch.run(self.write_raw("d2.json", [not_rel, relevant]), state, self.dir / "o2.json", self.resume)
        self.assertEqual(rep["new_count"], 1)
        item = rep["new"][0]
        self.assertEqual(item["posting_id"], "R")
        self.assertEqual(item["posting_title"], "Senior Network Security Engineer")
        self.assertEqual(item["record"]["verdict"], "relevant")
        self.assert_grounded(item["record"]["citations"], relevant)
        for c in item["record"]["citations"]:
            if c["posting_field"] == "text":
                self.assertNotIn("Road", c["posting_value"])

    def test_W2_many_new_postings_each_carry_their_own_verdict(self):
        state = self.dir / "seen_ids.json"
        jobwatch.run(self.write_raw("d1.json", [posting("z", "Chef")]), state, self.dir / "o1.json", self.resume)
        day2 = [posting("z", "Chef"),
                posting("n1", "Road Network Tools Engineer", RELEVANT_DESC),
                posting("r1", "Network Engineer", RELEVANT_DESC),
                posting("n2", "Barista"),
                posting("r2", "Network Architect", "OSPF and VPN design.")]
        rep = jobwatch.run(self.write_raw("d2.json", day2), state, self.dir / "o2.json", self.resume)
        by_id = {p["id"]: p for p in day2}
        expected = {"n1": "not_relevant", "r1": "relevant", "n2": "not_relevant", "r2": "relevant"}
        self.assertEqual({n["posting_id"]: n["record"]["verdict"] for n in rep["new"]}, expected)
        for n in rep["new"]:
            with self.subTest(id=n["posting_id"]):
                self.assertEqual(n["posting_title"], by_id[n["posting_id"]]["text"])
                self.assert_grounded(n["record"]["citations"], by_id[n["posting_id"]])

    def test_judgment_never_changes_record(self):
        def judge_as(v):
            return lambda p, r: json.dumps({"posting_id": p["id"], "verdict": v, "citations": [
                {"resume_field": "target.soc_code", "resume_value": "15-1241",
                 "posting_field": "text", "posting_value": p["text"][:3]}]})
        day2 = [posting("r1", "Network Engineer", RELEVANT_DESC), posting("n1", "Barista")]
        records = []
        for v in ("relevant", "not_relevant"):
            state = self.dir / f"s-{v}.json"
            jobwatch.run(self.write_raw(f"d1-{v}.json", []), state, self.dir / f"o1-{v}.json", self.resume)
            rep = jobwatch.run(self.write_raw(f"d2-{v}.json", day2), state, self.dir / f"o2-{v}.json",
                               self.resume, judge=judge_as(v))
            records.append(json.dumps([n["record"] for n in rep["new"]], sort_keys=True))
            for n in rep["new"]:
                self.assertEqual(n["record"]["label"], "record")
                self.assertEqual(n["judgment"]["label"], "judgment")
        self.assertEqual(records[0], records[1])

    def test_rejected_judgment_is_stored_as_rejected_not_repaired(self):
        state = self.dir / "seen_ids.json"
        jobwatch.run(self.write_raw("d1.json", []), state, self.dir / "o1.json", self.resume)
        rep = jobwatch.run(self.write_raw("d2.json", [posting("r1", "Network Engineer", RELEVANT_DESC)]),
                           state, self.dir / "o2.json", self.resume, judge=lambda p, r: "Looks relevant to me!")
        j = rep["new"][0]["judgment"]
        self.assertEqual(j["label"], "judgment")
        self.assertEqual(j["status"], "rejected")
        self.assertNotIn("verdict", j)
        self.assertEqual(rep["new"][0]["record"]["verdict"], "relevant")


# ---------------------------------------------------------------- Claude judge harness (offline: the CLI is faked)
class JudgeHarness(Base):
    """claude_judge(prompt_path, log_dir, runner=..., claude_bin=...) returns judge(posting, resume) for run().
    Each call is one fresh `claude -p --no-session-persistence` process. The raw output is saved before validation."""

    PROMPT = ROOT / "prompts" / "judge_v1.md"

    def fake_runner(self, result_text):
        calls = []

        def runner(cmd, **kw):
            calls.append((cmd, kw))
            sid = cmd[cmd.index("--session-id") + 1]
            env = {"type": "result", "is_error": False, "result": result_text, "session_id": sid,
                   "modelUsage": {"fake-model": {}}}
            return types.SimpleNamespace(returncode=0, stdout=json.dumps(env), stderr="")
        return runner, calls

    def run_with(self, result_text, post):
        runner, calls = self.fake_runner(result_text)
        judge = jobwatch.claude_judge(self.PROMPT, self.dir / "judge-log", runner=runner, claude_bin="claude")
        state = self.dir / "seen_ids.json"
        jobwatch.run(self.write_raw("d1.json", []), state, self.dir / "o1.json", self.resume)
        rep = jobwatch.run(self.write_raw("d2.json", [post]), state, self.dir / "o2.json", self.resume, judge=judge)
        return rep["new"][0], calls

    def test_prompt_contract_names_the_fixed_schema(self):
        text = self.PROMPT.read_text(encoding="utf-8")
        for needle in ("{{RESUME_JSON}}", "{{POSTING_JSON}}", "{{POSTING_ID}}", '"posting_id"', '"verdict"',
                       '"citations"', "resume_field", "resume_value", "posting_field", "posting_value"):
            self.assertIn(needle, text)

    def test_prompt_allowed_resume_paths_match_what_validator_resolves(self):
        # added 2026-10-31 after the SEEDED run: 4 rejections came from index/object paths the validator cannot follow.
        # The prompt's allowed list must be exactly the résumé paths the validator can resolve, and nothing is loosened.
        text = self.PROMPT.read_text(encoding="utf-8")
        block = text.split("It must be exactly one of", 1)[1].split("`resume_value`", 1)[0]
        listed = set(re.findall(r'"([^"]+)"', block))

        def resolvable(d, pre=""):
            for k, v in d.items():
                if isinstance(v, dict):
                    yield from resolvable(v, pre + k + ".")
                elif not (isinstance(v, list) and any(isinstance(x, (dict, list)) for x in v)):
                    yield pre + k
        self.assertEqual(listed, set(resolvable(self.resume)))
        self.assertFalse(jobwatch.resume_value_at(self.resume, "education.0.degree",
                                                  "MS, Computer Systems Networking and Telecommunications"))
        self.assertFalse(jobwatch.resume_value_at(self.resume, "experience", "Network Engineer"))

    def test_fresh_headless_call_and_raw_saved_with_session_id(self):
        post = posting("j1", "Network Engineer", RELEVANT_DESC)
        good = json.dumps({"posting_id": "j1", "verdict": "relevant", "citations": [
            {"resume_field": "skills.networking", "resume_value": "BGP",
             "posting_field": "descriptionPlain", "posting_value": "BGP"}]})
        item, calls = self.run_with(good, post)
        self.assertEqual(len(calls), 1)
        cmd, kw = calls[0]
        self.assertIn("-p", cmd)
        self.assertIn("--no-session-persistence", cmd)
        self.assertNotIn("--continue", cmd)
        self.assertNotIn("--resume", cmd)
        self.assertEqual(cmd[cmd.index("--tools") + 1], "", "tools disabled for the judge")
        j = item["judgment"]
        self.assertEqual((j["label"], j["status"], j["verdict"]), ("judgment", "accepted", "relevant"))
        self.assertTrue(j["session_id"])
        saved = json.loads(Path(j["raw_response_file"]).read_text(encoding="utf-8"))
        self.assertEqual(saved["session_id"], j["session_id"])
        # stdout is the CLI's JSON envelope; the model text inside it must be saved exactly
        self.assertEqual(json.loads(saved["stdout"])["result"], good)
        self.assertTrue(saved["requested_at"] and saved["finished_at"])
        self.assertEqual(item["record"], jobwatch.decide(post, self.resume))

    def test_fenced_output_is_rejected_and_kept_verbatim(self):
        post = posting("j2", "Network Engineer", RELEVANT_DESC)
        fenced = '```json\n{"posting_id": "j2", "verdict": "relevant", "citations": []}\n```'
        item, _ = self.run_with(fenced, post)
        j = item["judgment"]
        self.assertEqual(j["status"], "rejected")
        self.assertNotIn("verdict", j)
        self.assertEqual(j["raw_response"], fenced)
        self.assertTrue(Path(j["raw_response_file"]).exists())
        self.assertEqual(item["record"]["verdict"], "relevant")

    def test_each_call_gets_a_new_session_id(self):
        post = posting("j3", "Network Engineer", RELEVANT_DESC)
        runner, calls = self.fake_runner("not json")
        judge = jobwatch.claude_judge(self.PROMPT, self.dir / "log", runner=runner, claude_bin="claude")
        for _ in range(3):
            judge(post, self.resume)
        sids = [c[0][c[0].index("--session-id") + 1] for c in calls]
        self.assertEqual(len(set(sids)), 3)


if __name__ == "__main__":
    unittest.main()
