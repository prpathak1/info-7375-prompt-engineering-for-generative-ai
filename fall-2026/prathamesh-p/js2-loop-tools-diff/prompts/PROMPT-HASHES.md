# Prompt versions and hashes

| File | sha256 | Status |
|---|---|---|
| `archive/judge_v1.PRE-FIX-used-2026-10-30-and-SEEDED-2026-10-31.md` | `3be1ef3b7a0752b002ca5d6395459f9daf1016b745dac188379f0725ac70bb98` | Pre-fix v1. Used for the 2026-10-30 smoke test and the 2026-10-31 SEEDED run (4 of 5 rejected for index/object résumé paths). Kept as evidence. |
| `judge_v1.md` | `f55c7c68cf04c36ecd3300c8dacd48b1243644fd47e051604557e5927f946272` | **Experiment baseline v1** (fixed 2026-10-31 13:53 EDT, before any sampling or experiment call). resume_field is limited to dictionary-key paths, with the exact allowed list given. |
| `judge_v2.md` | `99ff01260298a4d32e1392c0688ef6aa600fd6e8f2855f6bf3bc652752a245f7` | Experiment change (2026-10-31 14:21 EDT): v1 plus criterion 4 (seniority, matching experiment/LABELING-RULE.md). No other edit. |

Each raw judgment file also records `prompt_sha256`, the hash of the *filled* prompt (template plus résumé plus posting), not of the template file above.
