# TRANSCRIPT-CHECK.md

faster-whisper `small` (CPU, int8), language en. Compared word by word with `narration_text` after lower-casing, stripping punctuation and splitting hyphens.

| Beat | Match | Differences (expected → heard) | Heard |
|---|---|---|---|
| B00 | 95% | `prathamesh` → `prathymish` | I'm Prathymish Pathak, pitching Honest Shortlist for an Applied AI and Agent Engineering Role. This synthetic voice is reading my script. |
| B01 | 97% | `one` → `1` | A network engineering posting lists skills, city, sometimes pay. On sponsorship, it often says nothing. For the fictional F-1 student I'm designing for, that silence is the problem. |
| B02 | 98% | `ten` → `10` | Honest Shortlist will be a Python and Claude agent that watches public job boards and gives that student a short daily list of new postings, shipped as a GitHub repo with tests, a held out evaluation, and a 10-document packet. |
| B03 | 95% | `liveness` → `live ness` | Each claim, new location, sponsorship pay will be labeled supported, contradicted, or insufficient against the posting's own text. Live-ness will be checked by fetching the board again. |
| B04 | 100% | none | Why care? It will show its evidence and say the posting doesn't say, instead of guessing. I haven't examined alternatives yet. In my first job search assignment, I will compare LinkedIn job alerts and a chat assistant. |
| B05 | 100% | none | A hiring manager or engineer screening for that role will read the read me and sample output, then run one command, all within a minute. Each claim will link to its posting text, beside an evaluation table that shows the failures. |
| B06 | 100% | none | It will prove prompt contracts with a validator that rejects anything off schema, an agent loop with budgets, exits, and a stop the model doesn't control, and permissions enforced in code with boundary tests. |
| B07 | 94% | `m c p` → `mcp` | then source grounding with an MCP style tool, verification and versioned memory, a held out evaluation with five or more deliberate failures, and a human approval gate bound to the exact shortlist. |
| B08 | 94% | `log in` → `login` | Out by design, no LinkedIn or indeed scraping, only public greenhouse, lever, and Ashby data. And it will never apply email, message, or login. |
| B09 | 92% | `one` → `1`; `two` → `2`; `seeded` → `seated` | First, a one-board watch. Run 1 will set a baseline. Run 2 will report only new postings on a real second day or labeled seated. Anyone will be able to check the raw responses and the diff. |
| B10 | 93% | `payments` → `payment's`; `h one b` → `h1b` | The risk, keywords mislead. Visa can be the payment's company, authorized to work without the word sponsorship, answers neither question. So insufficient will be the default and public H1B employer data will stay a separate company signal, never a claim about the posting. |
| B11 | 100% | none | Writing Python myself, agent loops, policies in code, and evaluations that can say no are new to me. I already ran the Brutalist toolkit on Windows, diagnosed its failures, and reviewed and approved Claude's fixes. On my reallocation recipe, I chose the persona, rules, and dates while Claude drafted the code. |
| B12 | 100% | none | How often postings are silent, I don't know yet, I will measure it. Every claim here will be checkable, and that's the work I want to be hired for. |
| B13 | 91% | `1` → `one`; `thirty first` → `31st`; `twentieth` → `20th` | Today the toolkit has passed its smoke test, and my week one and recipe commits exist. Everything else is planned, the first watch by October 31st, and the full system, a stranger run and a demo by December 20th. |
| B14 | 100% | none | honest shortlist, every claim will carry its evidence, and silence will be called silence. |
