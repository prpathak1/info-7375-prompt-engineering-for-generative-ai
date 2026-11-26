# Grounding: lexical relevance vs. entailment, and the abstention rule

- **Written by:** Claude Code (Opus 5.5), 2026-11-25 about 19:13 EST.
- **Sources:** FILTER v0.2 outputs in `out/decisions.all.v0.2.jsonl` and v0.3 outputs in `out/decisions.all.v0.3.jsonl`; the shortlist in `SHORTLIST.md` (v0.3; the v0.2 version is `out/SHORTLIST.v0.2.md`). Every quote is copied from the stored raw postings.
- **Held-out labels** are cited from `holdout/LABELS.json` (Claude-drafted, approved by Prathamesh).

## 1. Lexical relevance is not entailment (a real case)

**The posting text.** Nine Cloudflare network postings (8081027, 8083701, 8088046, 8088751, 8142261, 8159206, 8164724, 8188468, 8207864) contain this sentence:

> "Please note that any offer of employment may be conditioned on your authorization to receive software or technology controlled under these U.S. export laws without sponsorship for an export license."

**What the filter did.** Under v0.2, rule A2 matches the words `without sponsorship`, labels the authorization claim **contradicted**, and rejects all 9. The phrase is in the A2 list because, in a visa context, "without sponsorship" means "we won't sponsor your visa".

**What the sentence says.** It is about **sponsorship for an export license** (a license to receive controlled technology), not **visa sponsorship**. It doesn't say the employer refuses to sponsor work visas. Read against the evidence rules (FILTER section 2), the claim "nothing excludes an F-1 holder who needs sponsorship" is neither asserted nor denied: the right label is **insufficient**, not contradicted. The words are relevant; the meaning doesn't follow.

**The same pattern, three more times:**
- v0.1 A1 matched `EAR` in "We are the eyes and ears of Cloudflare" (fixed in v0.2).
- v0.1 A1 matched `export control` in "This position may require access to information protected under U.S. export control laws" (8 postings). "May require access" is not "excludes" (now A7 → flag).
- Held-out H26: S3 rejected it first, so its skills gate never ran in the filter run. Called on its own (`filter.gate4`, about 19:14 EST), the skills gate returns BGP, OSPF, routing and switching. The body contains "assisting with cable routing/termination", which is physical cabling, not IP routing (K2 excludes only call, ticket and request routing). The **first** `routing` match, the one the gate records, is that cabling sentence. A second match, "Familiarity with routing and switching concepts (BGP, OSPF, EVPN/VXLAN)", is genuine. So the count of 4 holds here, but the quoted evidence for `routing` would be the wrong sentence: a lexical match standing in for the real one.

**Status: changed in v0.3** (Prathamesh, 2026-11-25). When `without sponsorship` is directly followed by `for an export license`, it no longer counts as A2: the sentence now leaves the authorization claim **insufficient** and the posting is flagged A7, which matches the reading above.
- On the 1,964 non-held-out postings, 3 of the 9 now reach a human. The other 6 are rejected by a later rule (seniority or skills), with their own quotes (`demo/08-v02-to-v03-diff.txt`).
- The word match still exists. The rule now checks the words that follow it, which is a narrow patch for one sentence shape, not a general reading of meaning: a reworded export-license sentence would still be read as a visa refusal.

## 2. The abstention rule

FILTER section 2.4 abstains (no accept, no reject) when:
1. the body is missing or under 200 characters, or
2. authorization and seniority are both `insufficient` **and** the title has no T3 role word.

**What happened on the full runs (1,994 postings):** 0 abstains under v0.2, and 0 under v0.3 (1,986 reject, 5 flag, 3 accept).

## 3. Counterexamples that show the rule's limits

**(a) Unknown on what matters most, yet not abstained: H03.** OpenAI "Network Engineer", San Francisco, `9f78c41f-...`.
- Authorization is **insufficient** (posting is silent) and seniority is **insufficient** (no years stated, no level word).
- Rule 2 doesn't fire, because the title has a role word ("Engineer"). The filter accepts it, ranked #1.
- Prathamesh's held-out label is `fit` ("no years stated, silent on authorization and clearance"). Here the acceptance happens to agree with him.
- But the rule abstains on thin **titles**, not thin **evidence**: the two facts that decide the persona's case are both unknown, and the filter still says accept.

**(b) A fact the rule can't see: H08.** OpenAI "Network Engineer", **London, UK**, `a80e213f-...`.
- All four claims come out exactly as for H03, and the filter accepts it (#3 under v0.2 and v0.3).
- Prathamesh's label is `not_fit`: "UK role; persona needs US sponsorship."
- No FILTER rule reads location: JS1 CONTRACT made location "not a criterion" because `open_to_relocation: true`. So no claim is `insufficient` about it, and abstention can't fire on a fact the filter never checks.
- Abstention only protects against gaps the claim list already names.
