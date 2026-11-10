"""test_written_reset.py: the WRITTEN defect, a defect found in Prathamesh's accepted patch 6dc2abb (NOT-CHECKED item 8).
This test is written BEFORE the fix.

`jobwatch.WRITTEN` is the list printed as "files written before the refusal". It is process-wide and never reset, so a second
`jobwatch.main()` call in the same process reports files written by an EARLIER call. Requirement (Prathamesh, 2026-11-10):
two refusals in one process must each report only their own files. Fix: reset WRITTEN at the start of each main() call.

EXPECTED is stated in each docstring, with a prediction for the code as it is now (6dc2abb).
"""
from __future__ import annotations

import contextlib
import io
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

import jobwatch  # noqa: E402

RAW = str(ROOT / "raw" / "2026-11-10" / "zoox.json")


def _main(argv):
    err = io.StringIO()
    with contextlib.redirect_stderr(err), contextlib.redirect_stdout(io.StringIO()):
        rc = jobwatch.main(argv)
    return rc, err.getvalue()


class WrittenIsPerCall(unittest.TestCase):
    def setUp(self):
        (ROOT / "state").mkdir(exist_ok=True)
        self.inside = Path(tempfile.mkdtemp(dir=ROOT / "state", prefix="_test_tmp_written_"))
        self.outside = Path(tempfile.mkdtemp(prefix="js2-written-outside-"))

    def tearDown(self):
        shutil.rmtree(self.inside, ignore_errors=True)
        shutil.rmtree(self.outside, ignore_errors=True)
        try:
            (ROOT / "state").rmdir()
        except OSError:
            pass

    def test_W_1_two_refusals_after_a_writing_call_each_report_only_their_own_files(self):
        """EXPECTED: call A (a run fully inside state/) writes its out and state files and returns 0. Call B (--out outside) and then call C
        (--state outside) each return 2, and each prints "files written before the refusal: none", because neither wrote anything itself.
        Neither message names A's files.
        (Prediction now: B and C both list A's two files, so it FAILS.)"""
        a_out, a_state = self.inside / "a-out.json", self.inside / "a-state.json"
        rc, _ = _main(["run", "--raw", RAW, "--state", str(a_state), "--out", str(a_out)])
        self.assertEqual(rc, 0)
        self.assertTrue(a_out.exists() and a_state.exists())

        rc_b, err_b = _main(["run", "--raw", RAW, "--state", str(self.inside / "b-state.json"), "--out", str(self.outside / "b-out.json")])
        rc_c, err_c = _main(["run", "--raw", RAW, "--state", str(self.outside / "c-state.json"), "--out", str(self.inside / "c-out.json")])
        for name, rc, err in (("B", rc_b, err_b), ("C", rc_c, err_c)):
            with self.subTest(call=name):
                self.assertEqual(rc, 2)
                self.assertIn("files written before the refusal: none", err)
                self.assertNotIn("a-out.json", err)
                self.assertNotIn("a-state.json", err)


if __name__ == "__main__":
    unittest.main(verbosity=2)
