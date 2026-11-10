"""07_hardlink_demo.py: review step 7, a case the tests still miss: an NTFS HARD LINK inside a writable folder that points to a file OUTSIDE the project.

Why it slips through: os.path.realpath follows symlinks and junctions, but a hard link is not a link to a path. It is a second
directory entry for the same file, so it "resolves" to itself, inside state/, and policy.check_write allows it. Writing through it
changes the outside file. No admin rights are needed (os.link / mklink /H), only that both are on the same volume.

Safe by construction: the "victim" is a throwaway file created by this script in a new %TEMP% folder. The hard link is created under
state/ with a random name. Both are removed in `finally`. Nothing else is touched. No network.
Run from the project folder:  python -I review/07_hardlink_demo.py
"""
import os
import shutil
import sys
import tempfile
import time
import uuid
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
import jobwatch            # noqa: E402  (loads policy.py beside it)
policy = jobwatch.policy

print("started", time.strftime("%a %b %d %H:%M:%S %Y"), "| ROOT =", ROOT)
outside = Path(tempfile.mkdtemp(prefix="js2-hardlink-victim-"))
(ROOT / "state").mkdir(exist_ok=True)
links = []
try:
    for case, writer in (("A: jobwatch._write (plain write, used by fetch and claude_judge)", "plain"),
                         ("B: jobwatch._write_atomic (tmp + os.replace, used by run)", "atomic")):
        victim = outside / f"victim-{writer}.txt"
        victim.write_text("ORIGINAL outside content\n", encoding="utf-8")
        link = ROOT / "state" / f"_demo_hardlink_{writer}_{uuid.uuid4().hex[:8]}.json"
        os.link(victim, link)
        links.append(link)
        print(f"\n== case {case}")
        print("victim (outside):", victim)
        print("link   (inside): ", link, "| st_nlink =", os.stat(link).st_nlink,
              "| same file:", os.path.samefile(victim, link))
        try:
            got = policy.check_write(link)
            print("policy.check_write(link) -> ALLOWED:", got)
        except policy.PermissionRefused as e:
            print("policy.check_write(link) -> REFUSED:", e)
            continue
        if writer == "plain":
            jobwatch._write(link, "OVERWRITTEN through state/ hard link\n")
        else:
            jobwatch._write_atomic(link, "OVERWRITTEN through state/ hard link\n")
        print("victim content now:", repr(victim.read_text(encoding="utf-8")))
        print("victim changed:", victim.read_text(encoding="utf-8").startswith("OVERWRITTEN"),
              "| link still same file as victim:", os.path.samefile(victim, link))
finally:
    for link in links:
        if os.path.lexists(link):
            os.unlink(link)
    shutil.rmtree(outside, ignore_errors=True)
    try:
        (ROOT / "state").rmdir()
    except OSError:
        pass
    print("\ncleanup: links removed:", all(not os.path.lexists(l) for l in links), "| victim folder removed:", not outside.exists())
    print("ended", time.strftime("%a %b %d %H:%M:%S %Y"))
