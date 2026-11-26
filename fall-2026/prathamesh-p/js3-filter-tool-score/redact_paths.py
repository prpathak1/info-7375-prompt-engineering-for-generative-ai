"""Redact the Windows user folder from text files in this folder (Prathamesh's decision, 2026-11-25).

  python -I redact_paths.py            scan only: list files and match counts (default, changes nothing)
  python -I redact_paths.py --apply    replace every match with <USER_HOME>

Matches, case-insensitive, in every escaped form:
  C:\\Users\\<name>, C:\\\\Users\\\\<name> (JSON-escaped, any number of backslashes), C:/Users/<name>, /c/Users/<name>
where <name> is the long folder name or its 8.3 short name. The separator after the name is kept, so JSON stays valid.
Binary files and __pycache__ are skipped. raw/ board captures are scanned too (they hold no local paths).
"""
import argparse
import re
import sys
from pathlib import Path

HERE = Path(__file__).resolve().parent
NAMES = ["Prathamesh P", "Prathamesh%20P", "PRATHA~1"]
RX = re.compile(r"(?:[A-Za-z]:|/[A-Za-z])?(?:\\+|/)Users(?:\\+|/)(?:" + "|".join(re.escape(n) for n in NAMES) + r")(?![\w~])",
                re.I)
TOKEN = "<USER_HOME>"


def files():
    for f in sorted(HERE.rglob("*")):
        if f.is_file() and "__pycache__" not in f.parts and f.name != Path(__file__).name:
            yield f


def main() -> int:
    ap = argparse.ArgumentParser()
    ap.add_argument("--apply", action="store_true")
    a = ap.parse_args()
    total = 0
    for f in files():
        raw = f.read_bytes()
        if b"\x00" in raw[:4096]:
            continue                                            # binary
        try:
            enc = "utf-8"
            text = raw.decode(enc)
        except UnicodeDecodeError:
            enc = "latin-1"                                     # cp1252 console logs: latin-1 round-trips every byte
            text = raw.decode(enc)
            print(f"[note] {f.relative_to(HERE)} is not UTF-8; scanned byte-for-byte as latin-1")
        n = len(RX.findall(text))
        if not n:
            continue
        total += n
        print(f"{n:5d}  {f.relative_to(HERE)}")
        if a.apply:
            f.write_bytes(RX.sub(TOKEN, text).encode(enc))       # same encoding, line endings untouched
    print(f"[redact] {'replaced' if a.apply else 'found'} {total} matches")
    return 0


if __name__ == "__main__":
    sys.exit(main())
