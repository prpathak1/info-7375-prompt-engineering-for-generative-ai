"""Tests for the JS3 filter, written from FILTER.md v0.1 (all 23 rules APPROVED by Prathamesh 2026-11-25 18:46:08 EST)
BEFORE filter.py exists. Each test name says its rule ID; each docstring states the expected result.

Held-out rule: no test reads any of the 30 postings in holdout/HOLDOUT.json. Real postings used here are checked
against that file first (test_real_fixture_is_not_held_out). All other cases are SYNTHETIC records written below.

Interface these tests assume (../filter.py):
    decide(rec, resume) -> {"outcome": accept|reject|flag|abstain, "gate": rule id that decided (or None for accept),
                            "reason": str, "flags": [rule ids], "skills_matched": [terms], "min_years": int|None,
                            "claims": {"title"|"authorization"|"seniority"|"skills":
                                       {"label": supported|contradicted|insufficient, "quote": str|None,
                                        "field": "title"|"body"|None, "note": str}}}
    rank(pairs) -> pairs sorted by FILTER R1; pairs = [(rec, decision)] of accepted postings
    verify_quotes(decision, rec) -> list[str]   empty = every quote is an exact substring of its field
    select_for_run(records, include_holdout=False, labels_path=None) -> records; raises HoldoutLocked when the
        held-out postings are requested before a labels file exists
Records are postings.normalize() shape: {"board","id","title","body","location","url","date",...}.

Run: python -I -m unittest tests.test_filter -v   (from js3-filter-tool-score/)
"""
import json
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(HERE))

import filter as flt  # noqa: E402
import postings  # noqa: E402

RESUME = json.loads((HERE / "fixtures" / "resume.fictional.json").read_text(encoding="utf-8"))
HOLDOUT = json.loads((HERE / "holdout" / "HOLDOUT.json").read_text(encoding="utf-8"))
HELD = {(p["board"], p["id"]) for p in HOLDOUT["postings"]}

# Neutral padding: no skill, authorization, seniority or years words. Gets a body over the 200-char abstain floor.
PAD = ("The team builds dependable systems for customers around the world and cares about clear writing, "
       "careful reviews and calm on-call habits. We value curiosity and kindness. ") * 2
TWO_SKILLS = " You will configure BGP and OSPF across our sites."


def rec(title="Network Engineer", body=PAD + TWO_SKILLS, date="2026-11-01T00:00:00Z", rid="syn-1"):
    return {"platform": "synthetic", "board": "synthetic", "id": rid, "title": title, "body": body,
            "location": "Boston, MA", "url": None, "date": date, "captured": "synthetic"}


def d(title="Network Engineer", body=PAD + TWO_SKILLS, **kw):
    return flt.decide(rec(title, body, **kw), RESUME)


class Gate1Title(unittest.TestCase):
    def test_T1_no_network_word_rejects(self):
        """'Product Manager' -> reject, gate T1."""
        r = d("Product Manager")
        self.assertEqual((r["outcome"], r["gate"]), ("reject", "T1"))

    def test_T1_networking_and_networks_count(self):
        """'Networking Engineer' and 'Networks Engineer' pass T1 -> accept with two skills."""
        for t in ("Networking Engineer", "Networks Engineer"):
            self.assertEqual(d(t)["outcome"], "accept", t)

    def test_T1_whole_word_only(self):
        """'Networkx Engineer' has no whole-word network -> reject T1."""
        self.assertEqual(d("Networkx Engineer")["gate"], "T1")

    def test_T2_false_friend_rejects(self):
        """'Social Network Engineer' -> reject, gate T2."""
        self.assertEqual((d("Social Network Engineer")["outcome"], d("Social Network Engineer")["gate"]), ("reject", "T2"))

    def test_T2a_new_false_friends_reject(self):
        """Champion network / network-on-chip / NoC / network strategy without an engineer word -> reject T2a."""
        for t in ("Champion Network Engineer", "RTL Engineer, Network-on-Chip", "Design Engineer, Networking / NoC",
                  "Network Strategy Analyst"):
            r = d(t)
            self.assertEqual((r["outcome"], r["gate"]), ("reject", "T2a"), t)

    def test_T2a_network_strategy_with_engineer_word_is_not_T2a(self):
        """'Network Strategy Engineer' has an engineer word -> T2a does not apply -> accept."""
        self.assertEqual(d("Network Strategy Engineer")["outcome"], "accept")

    def test_T3_role_word_accepts(self):
        """'Network Engineer' + 2 skills + silent body -> accept; title claim supported, quote 'Network Engineer'."""
        r = d("Network Engineer")
        self.assertEqual(r["outcome"], "accept")
        self.assertEqual(r["claims"]["title"]["label"], "supported")
        self.assertEqual(r["claims"]["title"]["field"], "title")

    def test_T3a_technician_without_role_word_flags(self):
        """'Network Technician' (no T3 role word) -> flag, T3a in flags."""
        r = d("Network Technician", PAD + TWO_SKILLS + " Entry level role.")
        self.assertEqual(r["outcome"], "flag")
        self.assertIn("T3a", r["flags"])

    def test_T3a_operations_with_engineer_word_accepts(self):
        """'Network Operations Engineer' has 'engineer' -> T3 applies, not T3a -> accept."""
        self.assertEqual(d("Network Operations Engineer")["outcome"], "accept")

    def test_T4_software_flags(self):
        """'Software Engineer, Network Platform' -> flag, T4 in flags."""
        r = d("Software Engineer, Network Platform")
        self.assertEqual(r["outcome"], "flag")
        self.assertIn("T4", r["flags"])

    def test_T5_no_role_word_flags_when_seniority_known(self):
        """'Network Coordinator' + '0-2 years' (S5 supported) -> flag with T5."""
        r = d("Network Coordinator", PAD + TWO_SKILLS + " 0-2 years of experience.")
        self.assertEqual(r["outcome"], "flag")
        self.assertIn("T5", r["flags"])


class Gate2Authorization(unittest.TestCase):
    def test_A1_citizen_rejects_with_contradicted_quote(self):
        """'Must be a U.S. citizen.' -> reject A1; authorization contradicted, quote 'U.S. citizen'."""
        r = d(body=PAD + TWO_SKILLS + " Must be a U.S. citizen.")
        self.assertEqual((r["outcome"], r["gate"]), ("reject", "A1"))
        self.assertEqual(r["claims"]["authorization"]["label"], "contradicted")
        self.assertEqual(r["claims"]["authorization"]["quote"].lower(), "u.s. citizen")

    def test_A1_plural(self):
        """'Open to U.S. citizens only.' -> reject A1."""
        self.assertEqual(d(body=PAD + TWO_SKILLS + " Open to U.S. citizens only.")["gate"], "A1")

    def test_W1_years_military_dear_do_not_trigger_A1(self):
        """W1: substring matching would fire 'EAR' in 'years' and 'ITAR' in 'military'. Whole word -> accept."""
        r = d(body=PAD + TWO_SKILLS + " Dear applicant, we spent years serving military and civic customers.")
        self.assertEqual(r["outcome"], "accept")

    def test_A1_searched_in_body_not_title(self):
        """A Gate-2 phrase only in the title is not searched -> no A1."""
        self.assertNotEqual(d("Network Engineer (ITAR program)")["gate"], "A1")

    def test_A2_sponsorship_refusal_rejects(self):
        """'We are unable to sponsor visas.' -> reject A2, authorization contradicted."""
        r = d(body=PAD + TWO_SKILLS + " We are unable to sponsor visas.")
        self.assertEqual((r["outcome"], r["gate"]), ("reject", "A2"))
        self.assertEqual(r["claims"]["authorization"]["label"], "contradicted")

    def test_W4_A3_negated_clearance_flags_not_rejects(self):
        """W4: 'Security clearance not required.' -> flag (A3), not reject."""
        r = d(body=PAD + TWO_SKILLS + " Security clearance not required.")
        self.assertEqual(r["outcome"], "flag")
        self.assertIn("A3", r["flags"])

    def test_A3_negator_before_phrase(self):
        """'No security clearance is needed.' -> flag (A3)."""
        r = d(body=PAD + TWO_SKILLS + " No security clearance is needed.")
        self.assertEqual(r["outcome"], "flag")
        self.assertIn("A3", r["flags"])

    def test_A3_negator_too_far_does_not_guard(self):
        """Negator more than 5 words away -> A1 still rejects."""
        body = PAD + TWO_SKILLS + " Travel is not expected often for this team, but an active security clearance is mandatory."
        self.assertEqual(d(body=body)["gate"], "A1")

    def test_A4_authorized_to_work_is_not_refusal(self):
        """'must be authorized to work in the U.S.' -> accept; authorization insufficient, note says sponsorship unknown."""
        r = d(body=PAD + TWO_SKILLS + " Candidates must be authorized to work in the U.S.")
        self.assertEqual(r["outcome"], "accept")
        self.assertEqual(r["claims"]["authorization"]["label"], "insufficient")
        self.assertIn("sponsorship unknown", r["claims"]["authorization"]["note"])

    def test_W5_A5_silent_is_insufficient_never_supported(self):
        """W5: no authorization text -> label insufficient, note 'posting is silent'."""
        r = d()
        self.assertEqual(r["claims"]["authorization"]["label"], "insufficient")
        self.assertIn("posting is silent", r["claims"]["authorization"]["note"])

    def test_A6_green_card_and_permanent_resident_reject(self):
        """'green card' / 'permanent resident' / 'U.S. persons only' -> reject A6."""
        for s in (" Green card holders only.", " Must be a permanent resident.", " U.S. persons only."):
            self.assertEqual(d(body=PAD + TWO_SKILLS + s)["outcome"], "reject", s)


class FilterV02(unittest.TestCase):
    """FILTER v0.2 (Prathamesh's decision after the audit, 2026-11-25). Written before the code change."""
    CF = ("This position may require access to information protected under U.S. export control laws, "
          "including the U.S. Export Administration Regulations.")

    def test_v02_1_EAR_does_not_match_ears(self):
        """'the eyes and ears of the team' -> no A1 (EAR is exact uppercase, no plural) -> accept."""
        r = d(body=PAD + TWO_SKILLS + " We are the eyes and ears of the team.")
        self.assertEqual(r["outcome"], "accept")

    def test_v02_1_EAR_lowercase_does_not_match(self):
        """'wear ear protection on the floor' -> lowercase 'ear' is not EAR -> accept."""
        self.assertEqual(d(body=PAD + TWO_SKILLS + " Wear ear protection on the floor.")["outcome"], "accept")

    def test_v02_1_EAR_uppercase_still_rejects(self):
        """'Items subject to the EAR.' -> reject A1, quote 'EAR'."""
        r = d(body=PAD + TWO_SKILLS + " Items are subject to the EAR.")
        self.assertEqual((r["outcome"], r["gate"], r["claims"]["authorization"]["quote"]), ("reject", "A1", "EAR"))

    def test_v02_2_may_require_access_export_control_flags(self):
        """The Cloudflare 'may require access ... export control' sentence alone -> flag A7, sponsorship unknown."""
        r = d(body=PAD + TWO_SKILLS + " " + self.CF)
        self.assertEqual(r["outcome"], "flag")
        self.assertIn("A7", r["flags"])
        self.assertEqual(r["claims"]["authorization"]["label"], "insufficient")
        self.assertIn("sponsorship unknown", r["claims"]["authorization"]["note"])

    def test_v02_2_explicit_exclusion_still_rejects(self):
        """The same sentence plus 'Must be a U.S. citizen.' -> reject A1."""
        r = d(body=PAD + TWO_SKILLS + " " + self.CF + " Must be a U.S. citizen.")
        self.assertEqual((r["outcome"], r["gate"]), ("reject", "A1"))


class FilterV03(unittest.TestCase):
    """FILTER v0.3 (Prathamesh's decision, 2026-11-25). Written before the code change."""
    LICENSE = ("Please note that any offer of employment may be conditioned on your authorization to receive software or "
               "technology controlled under these U.S. export laws without sponsorship for an export license.")

    def test_v03_export_license_sentence_alone_flags_A7(self):
        """The export-license sentence alone -> flag A7 (sponsorship unknown), not reject A2."""
        r = d(body=PAD + TWO_SKILLS + " " + self.LICENSE)
        self.assertEqual(r["outcome"], "flag")
        self.assertIn("A7", r["flags"])
        self.assertIn("sponsorship unknown", r["claims"]["authorization"]["note"])

    def test_v03_cloudflare_pair_flags_A7(self):
        """The real Cloudflare pair (may-require-access sentence + export-license sentence) -> flag A7."""
        r = d(body=PAD + TWO_SKILLS + " " + FilterV02.CF + " " + self.LICENSE)
        self.assertEqual(r["outcome"], "flag")
        self.assertIn("A7", r["flags"])

    def test_v03_visa_refusal_still_rejects_A2(self):
        """'We will not sponsor visas for this role.' -> reject A2."""
        r = d(body=PAD + TWO_SKILLS + " We will not sponsor visas for this role.")
        self.assertEqual((r["outcome"], r["gate"]), ("reject", "A2"))

    def test_v03_plain_without_sponsorship_still_rejects_A2(self):
        """'Candidates must be able to work without sponsorship.' -> reject A2 (no export-license continuation)."""
        r = d(body=PAD + TWO_SKILLS + " Candidates must be able to work without sponsorship.")
        self.assertEqual((r["outcome"], r["gate"]), ("reject", "A2"))


class Gate3Seniority(unittest.TestCase):
    def test_S1_title_levels_reject(self):
        """Senior / Sr. / Staff / Principal / Lead / Manager / Director / Head of / VP in title -> reject S1."""
        for t in ("Senior Network Engineer", "Sr. Network Engineer", "Staff Network Engineer", "Principal Network Architect",
                  "Network Infrastructure Lead", "Network Engineering Manager", "Director, Network Engineering",
                  "Head of Network Engineering", "VP Network Engineering"):
            r = d(t)
            self.assertEqual((r["outcome"], r["gate"]), ("reject", "S1"), t)
            self.assertEqual(r["claims"]["seniority"]["label"], "contradicted", t)

    def test_W2_S2_manager_I_is_not_entry_level(self):
        """W2: 'Manager I, Engineering - Zero Trust Networking' -> reject S1 (not entry level)."""
        r = d("Manager I, Engineering - Zero Trust Networking")
        self.assertEqual((r["outcome"], r["gate"]), ("reject", "S1"))

    def test_S2_engineer_I_is_entry_level(self):
        """'Network Engineer I' -> accept, seniority supported."""
        r = d("Network Engineer I")
        self.assertEqual(r["outcome"], "accept")
        self.assertEqual(r["claims"]["seniority"]["label"], "supported")

    def test_S3_five_plus_years_rejects(self):
        """'5+ years of experience' -> reject S3, min_years 5, quote contains '5+ years'."""
        r = d(body=PAD + TWO_SKILLS + " You have 5+ years of experience in networking.")
        self.assertEqual((r["outcome"], r["gate"], r["min_years"]), ("reject", "S3", 5))
        self.assertIn("5+ years", r["claims"]["seniority"]["quote"])

    def test_S3_three_or_four_years_flags(self):
        """'3+ years of professional experience' and '4 or more years of experience' -> flag, S3 in flags."""
        for s in (" 3+ years of professional experience.", " 4 or more years of experience."):
            r = d(body=PAD + TWO_SKILLS + s)
            self.assertEqual(r["outcome"], "flag", s)
            self.assertIn("S3", r["flags"], s)

    def test_S3_minimum_of_pattern(self):
        """'Minimum of 6 years of relevant experience' -> reject S3."""
        self.assertEqual(d(body=PAD + TWO_SKILLS + " Minimum of 6 years of relevant experience.")["gate"], "S3")

    def test_S3_two_years_supported(self):
        """'2+ years of experience' -> accept, seniority supported."""
        r = d(body=PAD + TWO_SKILLS + " 2+ years of experience.")
        self.assertEqual(r["outcome"], "accept")
        self.assertEqual(r["claims"]["seniority"]["label"], "supported")

    def test_S3_smallest_N_wins(self):
        """'1+ years of experience required; 7+ years of experience preferred' -> min_years 1 -> accept."""
        r = d(body=PAD + TWO_SKILLS + " 1+ years of experience required; 7+ years of experience preferred.")
        self.assertEqual((r["outcome"], r["min_years"]), ("accept", 1))

    def test_S3_years_without_experience_nearby_ignored(self):
        """'5+ years in business' and '2 years ago' (no 'experience' within 6 words) -> no years read -> accept."""
        r = d(body=PAD + TWO_SKILLS + " We have been in business 5+ years now and grew a lot. We moved offices 2 years ago.")
        self.assertEqual((r["outcome"], r["min_years"]), ("accept", None))

    def test_S4_no_years_is_insufficient_and_passes(self):
        """No years and no level word -> seniority insufficient; posting still accepted."""
        r = d()
        self.assertEqual(r["outcome"], "accept")
        self.assertEqual(r["claims"]["seniority"]["label"], "insufficient")

    def test_S5_entry_phrases_supported(self):
        """'new grad' in title or 'entry level' in body -> seniority supported."""
        self.assertEqual(d("Network Engineer, New Grad")["claims"]["seniority"]["label"], "supported")
        self.assertEqual(d(body=PAD + TWO_SKILLS + " This is an entry level role.")["claims"]["seniority"]["label"], "supported")


class Gate4Skills(unittest.TestCase):
    def test_K1_one_skill_rejects(self):
        """Only 'BGP' -> reject K1; skills claim insufficient."""
        r = d(body=PAD + " You will configure BGP.")
        self.assertEqual((r["outcome"], r["gate"]), ("reject", "K1"))
        self.assertEqual(r["claims"]["skills"]["label"], "insufficient")

    def test_K1_two_distinct_skills_accept_and_plural_counts(self):
        """'VLANs' (plural) + 'firewall' -> 2 distinct -> accept; skills supported."""
        r = d(body=PAD + " You will manage VLANs and a firewall.")
        self.assertEqual(r["outcome"], "accept")
        self.assertEqual(sorted(r["skills_matched"]), ["VLAN", "firewall"])
        self.assertEqual(r["claims"]["skills"]["label"], "supported")

    def test_K1_repeated_term_counts_once(self):
        """'BGP ... BGP' -> 1 distinct -> reject K1."""
        self.assertEqual(d(body=PAD + " BGP, more BGP, always BGP.")["gate"], "K1")

    def test_K2_lexical_false_friends_do_not_count(self):
        """'context switching', 'ticket routing', DNS inside a URL do not count -> 0 skills -> reject K1."""
        r = d(body=PAD + " Avoid context switching; we use ticket routing. See https://dns.example.com/help.")
        self.assertEqual((r["gate"], r["skills_matched"]), ("K1", []))

    def test_K3_other_skill_groups_do_not_count(self):
        """Python, Ansible, Azure, zero trust -> not skills.networking -> reject K1."""
        self.assertEqual(d(body=PAD + " Python, Ansible, Azure and zero trust.")["gate"], "K1")


class Abstain(unittest.TestCase):
    def test_short_body_abstains(self):
        """Body under 200 characters -> abstain."""
        r = d(body="Configure BGP and OSPF.")
        self.assertEqual(r["outcome"], "abstain")

    def test_missing_title_abstains(self):
        """No title -> abstain."""
        self.assertEqual(d(title=None)["outcome"], "abstain")

    def test_title_reject_wins_over_short_body(self):
        """Gate 1 runs on the title first: 'Road Network Engineer' with an empty body -> reject T2, not abstain."""
        self.assertEqual(d("Road Network Engineer", body="")["gate"], "T2")

    def test_rule2_no_role_word_and_both_insufficient_abstains(self):
        """'Network Coordinator', silent body (authorization and seniority both insufficient) -> abstain."""
        self.assertEqual(d("Network Coordinator")["outcome"], "abstain")


class Ranking(unittest.TestCase):
    def test_W3_entry_role_outranks_keyword_dense_role(self):
        """W3: a 2-skill posting with seniority supported ranks above a 9-skill posting with seniority insufficient."""
        entry = rec("Network Engineer", PAD + TWO_SKILLS + " 0-2 years of experience.", rid="entry")
        dense = rec("Network Engineer", PAD + " BGP OSPF TCP/IP VLAN VPN DNS firewall routing switching.", rid="dense")
        pairs = [(dense, flt.decide(dense, RESUME)), (entry, flt.decide(entry, RESUME))]
        self.assertTrue(all(p[1]["outcome"] == "accept" for p in pairs))
        self.assertEqual([p[0]["id"] for p in flt.rank(pairs)], ["entry", "dense"])

    def test_W3_staff_with_nine_skills_is_not_accepted(self):
        """A 9-skill 'Staff Network Engineer' is rejected by S1, so it never reaches the ranking."""
        r = d("Staff Network Engineer", PAD + " BGP OSPF TCP/IP VLAN VPN DNS firewall routing switching.")
        self.assertEqual(r["gate"], "S1")

    def test_R1_ties_break_by_newest_date_missing_last(self):
        """Same tier and skill count: newest first; a missing date ranks last."""
        a, b, c = rec(rid="old", date="2026-01-01T00:00:00Z"), rec(rid="new", date="2026-11-01T00:00:00Z"), rec(rid="none", date=None)
        pairs = [(x, flt.decide(x, RESUME)) for x in (a, c, b)]
        self.assertEqual([p[0]["id"] for p in flt.rank(pairs)], ["new", "old", "none"])


class Evidence(unittest.TestCase):
    def test_every_quote_is_found_again(self):
        """Every non-null quote in an accepted and a rejected decision is an exact substring of its field."""
        for r_ in (rec(body=PAD + TWO_SKILLS + " 2+ years of experience."), rec(body=PAD + TWO_SKILLS + " We cannot sponsor.")):
            self.assertEqual(flt.verify_quotes(flt.decide(r_, RESUME), r_), [])

    def test_tampered_quote_is_reported(self):
        """A quote that is not in the posting -> verify_quotes returns an error."""
        r_ = rec()
        dec = flt.decide(r_, RESUME)
        dec["claims"]["skills"]["quote"] = "EIGRP"
        self.assertTrue(flt.verify_quotes(dec, r_))


class HoldoutGuard(unittest.TestCase):
    def test_held_out_postings_excluded_by_default(self):
        """select_for_run drops all 30 held-out postings."""
        kept = flt.select_for_run(postings.load_all())
        self.assertFalse({(p["board"], p["id"]) for p in kept} & HELD)

    def test_held_out_locked_until_labels_exist(self):
        """include_holdout=True without an existing labels file -> HoldoutLocked."""
        with tempfile.TemporaryDirectory() as t:
            with self.assertRaises(flt.HoldoutLocked):
                flt.select_for_run(postings.load_all(), include_holdout=True, labels_path=Path(t) / "none.json")


class RealNonHeldOut(unittest.TestCase):
    """Real postings, each checked to be outside the held-out sample before the filter sees it."""

    @classmethod
    def setUpClass(cls):
        cls.by_title = {}
        for p in postings.load_all():
            cls.by_title.setdefault(p["title"].strip() if p["title"] else "", []).append(p)

    def get(self, title):
        ps = self.by_title.get(title, [])
        self.assertEqual(len(ps), 1, title)
        self.assertNotIn((ps[0]["board"], ps[0]["id"]), HELD, "test would read a held-out posting")
        return ps[0]

    def test_real_fixture_is_not_held_out(self):
        """The two real postings below are not in holdout/HOLDOUT.json."""
        self.get("Senior Network Security Engineer")
        self.get("Manager I, Engineering - Zero Trust Networking")

    def test_real_zoox_senior_network_security_engineer_rejected_S1(self):
        """JS1 accepted this posting (8+ years). v0.1 -> reject S1."""
        self.assertEqual(flt.decide(self.get("Senior Network Security Engineer"), RESUME)["gate"], "S1")

    def test_real_datadog_manager_I_rejected_S1(self):
        """W2 on the real Datadog title -> reject S1."""
        self.assertEqual(flt.decide(self.get("Manager I, Engineering - Zero Trust Networking"), RESUME)["gate"], "S1")


if __name__ == "__main__":
    unittest.main()
