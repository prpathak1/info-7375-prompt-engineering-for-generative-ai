#!/usr/bin/env python3
"""redact_paths.py: replace local filesystem paths with <LOCAL> in text files under the given folders.

Usage: python redact_paths.py <dir> [<dir> ...]
Rewrites .log/.md/.txt/.json/.csv files in place and prints a count per file. Any Windows user folder
path (whose account name may contain a space) is matched first, then any remaining drive-letter path,
Git Bash /c/... path, or /tmp/... path is replaced to the end of its token. Indented single-token
continuation lines in .log files (paths wrapped by Manim's console) are replaced as well.
"""
import re, sys
from pathlib import Path

PATTERNS = [
    # any user folder (the account name may contain a space, so match up to the next separator)
    re.compile(r"(?i)[A-Za-z]:[\\/]+Users[\\/]+[^\\/\r\n]+?(?=[\\/])[^\s'\"|<>()\]\[,;`]*"),
    re.compile(r"(?i)/[a-z]/Users/[^/\r\n]+?(?=/)[^\s'\"|<>()\]\[,;`]*"),
    re.compile(r"(?i)(?<![\w<])[A-Za-z]:[\\/]{1,2}[^\s'\"|<>()\]\[,;`]+"),
    re.compile(r"(?<![\w.<])/(?:c|tmp)/[^\s'\"|<>()\]\[,;`]+"),
]
# Manim's rich console wraps a long path into heavily indented single-token continuation lines
# (e.g. "      rative-ai\fall-2026\prath"). Those carry no drive letter, so they get their own pass.
WRAPPED = re.compile(r"(?m)^(\s{20,})(\S+)(\s*)$")
EXT = {".log", ".md", ".txt", ".json", ".csv"}

total = 0
for root in sys.argv[1:]:
    for p in sorted(Path(root).rglob("*")):
        if not p.is_file() or p.suffix.lower() not in EXT:
            continue
        s = p.read_text(encoding="utf-8", errors="replace")
        n = 0
        for pat in PATTERNS:
            s, k = pat.subn("<LOCAL>", s)
            n += k
        if p.suffix.lower() == ".log":
            hits = [0]

            def _wrap(m):
                tok = m.group(2)
                if tok == "<LOCAL>" or not re.search(r"[\\/'_.-]", tok):
                    return m.group(0)          # already redacted, or a plain word: leave it
                hits[0] += 1
                return f"{m.group(1)}<LOCAL>{m.group(3)}"

            s = WRAPPED.sub(_wrap, s)
            n += hits[0]
        if n:
            p.write_text(s, encoding="utf-8")
            print(f"{n:5d}  {p}")
            total += n
print(f"total replacements: {total}")
