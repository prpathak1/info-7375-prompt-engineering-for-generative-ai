# Provenance of `hand_labels.json`

- **Recorded:** Fri Oct 30 18:33:42 EDT 2026 (from `date`). Claude Code saved the verdicts and notes unedited, as Prathamesh supplied them in chat.
- **How the predictions were made:** Claude (claude.ai chat) drafted them at Prathamesh's request by applying the CONTRACT rule by hand to the
  titles and to the text extracted into `tests/rows2-3-text.txt`. Prathamesh reviewed and approved them **before any implementation
  (`jobwatch.py`) existed**.
- **What they are:** hand applications of the CONTRACT rule. They are **not** Prathamesh's independent judgment of fit.
- **Contract version applied:** CONTRACT §4 as of 2026-10-30, with Gate 3 plurals counting and Gate 2 whole-word matching for every phrase.
- **Format note:** The file is a plain JSON list so that `test_hand_labels_if_present` can read it. This provenance note sits beside it because JSON has no comments.
