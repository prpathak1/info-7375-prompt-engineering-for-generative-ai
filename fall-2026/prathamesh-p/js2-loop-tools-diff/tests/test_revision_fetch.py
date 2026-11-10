"""test_revision_fetch.py: review step 6 REVISE (Prathamesh, 2026-11-10). This test is written BEFORE the revision.

Requirement (review/06-decision.md): fetch() checks all three target paths with policy.check_write BEFORE the network request.
An outside --raw-dir must be refused with exit code 2 and make ZERO requests. A fake urlopen counts the calls.

Each docstring starts with EXPECTED, written before the revision, plus a prediction for the code as it is now (patch at review/03-patch.diff).
"""
from __future__ import annotations

import os
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

import jobwatch  # noqa: E402


class _CountingUrlopen:
    """Counts calls. If it is ever called, it answers like a real allowed Lever response, so that code which (wrongly) sends the
    request first gets as far as the write check, and the test then sees calls == 1 rather than some unrelated error."""

    def __init__(self):
        self.calls = 0

    def __call__(self, req, *a, **k):
        self.calls += 1
        url = req.full_url

        class _Resp:
            status = 200
            headers = {}
            def geturl(self): return url
            def read(self): return b"[]"
            def __enter__(self): return self
            def __exit__(self, *exc): return False

        return _Resp()


class FetchChecksPathsBeforeRequest(unittest.TestCase):
    def setUp(self):
        self.outside = Path(tempfile.mkdtemp(prefix="js2-fetch-outside-"))   # under %TEMP%, outside ROOT
        self.fake = _CountingUrlopen()

    def tearDown(self):
        shutil.rmtree(self.outside, ignore_errors=True)

    def test_V1_library_fetch_outside_raw_dir_makes_zero_requests(self):
        """EXPECTED: jobwatch.fetch("zoox", <outside>, urlopen=fake) raises policy.PermissionRefused, fake.calls == 0,
        and the outside folder stays empty. (Prediction now: PermissionRefused is raised, but fake.calls == 1, so it FAILS on the call count.)"""
        with self.assertRaises(jobwatch.policy.PermissionRefused):
            jobwatch.fetch("zoox", self.outside, urlopen=self.fake)
        self.assertEqual(self.fake.calls, 0, "the permission check must happen before the network request")
        self.assertEqual(os.listdir(self.outside), [])

    def test_V2_cli_fetch_outside_raw_dir_exit_2_zero_requests(self):
        """EXPECTED: jobwatch.main(["fetch", "--board", "zoox", "--raw-dir", <outside>]) returns 2, fake.calls == 0, and the outside folder stays empty.
        The CLI passes no urlopen, so the test swaps fetch()'s default urlopen for the fake and restores it afterwards. No real request is possible.
        (Prediction now: returns 2, but fake.calls == 1, so it FAILS on the call count.)"""
        saved = jobwatch.fetch.__defaults__
        self.assertEqual(len(saved), 1, "fetch() is expected to have exactly one default (urlopen)")
        jobwatch.fetch.__defaults__ = (self.fake,)
        try:
            rc = jobwatch.main(["fetch", "--board", "zoox", "--raw-dir", str(self.outside)])
        finally:
            jobwatch.fetch.__defaults__ = saved
        self.assertEqual(rc, 2)
        self.assertEqual(self.fake.calls, 0, "the permission check must happen before the network request")
        self.assertEqual(os.listdir(self.outside), [])

    def test_V3_control_inside_raw_dir_does_request(self):
        """EXPECTED: with an INSIDE folder (a temp folder under state/), the checks pass and fake.calls == 1. This is a control, so that a
        'never request' change cannot pass V1 and V2. The fake returns b"[]", so three files are written there, and they are removed afterwards.
        (Prediction now: PASSES.)"""
        (ROOT / "state").mkdir(exist_ok=True)
        inside = Path(tempfile.mkdtemp(dir=ROOT / "state", prefix="_test_tmp_fetch_"))
        try:
            jobwatch.fetch("zoox", inside, urlopen=self.fake)
            self.assertEqual(self.fake.calls, 1)
        finally:
            shutil.rmtree(inside, ignore_errors=True)
            try:
                (ROOT / "state").rmdir()     # only if this test left it empty
            except OSError:
                pass


if __name__ == "__main__":
    unittest.main(verbosity=2)
