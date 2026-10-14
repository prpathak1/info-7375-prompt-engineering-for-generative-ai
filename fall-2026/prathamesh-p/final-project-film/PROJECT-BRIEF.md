# Project brief: Honest Shortlist (working title)

_Drafted by Claude (claude.ai chat, Opus 5.5), 2026-10-14, at my request; reviewed and owned by me
(SOURCES.md). Final: 2026-10-14._

**1. What is it?** Honest Shortlist will be a Python + Claude agent that watches public job boards and
gives a fictional F-1 master's student a short daily list of new network engineering postings (SOC
15-1241). Each claim (new, location, sponsorship or work-authorization wording, pay) will be labeled
supported, contradicted, or insufficient against the posting's text. Liveness will be checked by a
fresh fetch. **Artifact:** a GitHub repo with the agent, tests, a held-out evaluation, and the
ten-document packet.

**2. Why would anyone care?** It will show its evidence and say "the posting doesn't say" instead of
guessing. That matters most for sponsorship, where postings are often silent.
I haven't examined alternatives yet. During JS1 I will compare against LinkedIn job alerts and against
pasting a posting into a chat assistant, and record what I see in FRICTIONAL.

**3. Who opens it?** Target role: AI / agent engineer (applied AI). A hiring manager or engineer will read
the README and committed sample output, then run one command, all within 60 seconds. They will see claims
linked to the posting text they rest on, beside an evaluation table that includes the failures.

**4. What does it prove about me?**
- Prompt contracts (JS1): fixed-schema verdicts → validator tests.
- Agent loops (JS2): budgets, exits, a model-independent stop → saved traces.
- Permissions in code (JS2): allow-list, folder limits → 10+ boundary tests.
- Grounding (JS3): three labels, abstention, MCP-style tool → labeled shortlist, transcript.
- Verification, memory (JS4): evidence matrix, versioned state → planted-mismatch catch, two-day diff.
- Evaluation (JS1, JS5, final): held-out set, 5+ failure cases → pass rates with sample limits.
- Human gate (JS5): fingerprinted approval, controlled failure → rejection test, failure record.

**5. In, out, first.** **Out, by design:** no LinkedIn or Indeed scraping; public Greenhouse/Lever/Ashby
JSON only. It will never apply, email, message, or log in (a course rule). **First:** a one-board watch
(JS1): a baseline run, then a run reporting only new postings. That will be a real second day, or a
response labeled **SEEDED**. **Verify:** the raw responses plus the state diff, which anyone can
recompute.

**6. What could sink it?** Sponsorship wording is often missing or ambiguous, and keywords mislead.
"Visa" can be the payments company, and "authorized to work" without "sponsorship" answers neither
question. **Mitigation:** "insufficient" will be the default. Public H-1B employer data will be a
company-level signal, never a claim about the posting. False friends will go into the held-out set.

**7. Why this project?** **New / will demonstrate:** writing Python myself, loops with exits and
budgets, policies in code, MCP-style tools, and evaluations that can say no.
**Already have:**
- Debugging and verification: I ran the Brutalist toolkit on native Windows, diagnosed its failures,
  and reviewed and approved fixes that Claude wrote (`ce1a06c`, 2026-09-27).
- Sponsorship-history triage: my Reallocation recipe `network-eng-h1b` (`100a823`, `1a3e757`,
  `1b5a589`, 2026-10-03). I chose the persona, SOC code, rules and dates, decided the data and honesty
  calls, and approved every commit. Claude Code drafted all the code, tests and text.

**Why:** I don't know yet how common the problem is. I will measure how often sponsorship wording is
missing or ambiguous in my JS1 sample. Every claim will be checkable, and that is the work I want to
be hired to do.

**Exists today:** passing toolkit smoke (2026-10-14); this folder; commits `ce1a06c` (Week 1) and
`100a823`, `1a3e757`, `1b5a589` (recipe), on fork branches, not merged.

**Will exist:** Reallocation mode (Oct 21) · JS1 watch, judges, held-out test (Oct 31) · JS2 loop,
permissions (Nov 10) · JS3 grounding, MCP tool (Nov 23) · JS4 evidence, memory (Dec 1) · JS5 gate,
packet (Dec 13) · final system, stranger run, demo ≤5 min (Dec 20).
