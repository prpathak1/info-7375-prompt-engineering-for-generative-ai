"""test_policy.py: review packet step 2. The test is written BEFORE any patch, from GATE.md only.

Defect under test: JS1 NOT-CHECKED item 7, "writes not confined". `jobwatch.py run` writes wherever --state and --out point.

GATE.md (APPROVED 2026-11-10 08:17:25 EST) requirements this file checks:
  section 5 / D-10  Write only under ROOT/{raw,state,runs,traces}. Writes outside the project folder are refused. So are
                    writes inside it but outside those folders. Read only from fixtures/, raw/, state/, prompts/, GATE.md.
                    Overwriting an existing file under raw/ needs --approve <exact relative path>.
  section 5 / D-11  Full resolution (junctions and symlinks followed) and component comparison, never string prefixes.
  section 4 / D-8   A path or permission refusal stops the whole run, with no retry.
  section 1         Status `error` = exit code 2. The report names the refused action.

Interface these tests fix for the patch (named in review/PLAN.md; GATE.md names no functions):
  policy.py beside jobwatch.py, providing
    ROOT                                   the project folder, resolved
    class PermissionRefused(Exception)
    class ApprovalRequired(PermissionRefused)
    check_read(path) -> Path               the resolved path, or raises PermissionRefused
    check_write(path, approve=()) -> Path  the resolved path, or raises PermissionRefused / ApprovalRequired.
                                           `approve` holds ROOT-relative POSIX paths, such as "raw/2026-11-10/zoox.json".
  jobwatch.py run, when a write is refused: exit code 2, and stderr contains "refused" and the refused file's name.

Each test's docstring starts with EXPECTED, written before the test body and before any patch.
The prediction for the UNPATCHED code is in the docstring too.
"""
from __future__ import annotations

import os
import shutil
import subprocess
import sys
import tempfile
import unittest
import uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
sys.path.insert(0, str(ROOT))

RAW_TODAY = "raw/2026-11-10/zoox.json"   # real Lever capture, approved evidence (GATE D-1)


def _policy():
    """Imported inside each test, so a missing policy.py is reported once per test, not as one import error."""
    import policy  # noqa: PLC0415
    return policy


def _run_cli(state: Path, out: Path) -> subprocess.CompletedProcess:
    return subprocess.run(
        [sys.executable, "-I", str(ROOT / "jobwatch.py"), "run",
         "--raw", RAW_TODAY, "--state", str(state), "--out", str(out)],
        cwd=ROOT, capture_output=True, text=True, encoding="utf-8", errors="replace", timeout=120,
    )


class CliWritesOutsideProject(unittest.TestCase):
    """End-to-end through the real CLI. This is the defect from review/01-reproduce.txt, as a test."""

    def setUp(self):
        self.outside = Path(tempfile.mkdtemp(prefix="js2-outside-"))   # under %TEMP%, outside ROOT
        self.tag = uuid.uuid4().hex[:8]
        self.inside = []                                               # inside-ROOT files to clean up

    def tearDown(self):
        shutil.rmtree(self.outside, ignore_errors=True)
        for p in self.inside:
            for q in (p, p.with_name(p.name + ".tmp")):
                if q.exists():
                    q.unlink()
            try:
                p.parent.rmdir()          # only succeeds if this test left the folder empty
            except OSError:
                pass

    def _in(self, folder: str, name: str) -> Path:
        p = ROOT / folder / f"_test_{self.tag}_{name}"
        self.inside.append(p)
        return p

    def _assert_refused(self, cp, refused_name: str):
        self.assertEqual(cp.returncode, 2, f"exit code\nstdout:\n{cp.stdout}\nstderr:\n{cp.stderr}")
        self.assertIn("refused", cp.stderr.lower(), f"stderr must say 'refused'\nstderr:\n{cp.stderr}")
        self.assertIn(refused_name, cp.stderr, "stderr must name the refused file")

    def test_C1_state_and_out_both_outside(self):
        """EXPECTED: exit 2; stderr contains "refused" and "o.json" (the first write, --out, as in JS1 run());
        the outside folder stays EMPTY. (Unpatched prediction: exit 0, and s.json and o.json are written outside, so it FAILS.)"""
        cp = _run_cli(self.outside / "s.json", self.outside / "o.json")
        self._assert_refused(cp, "o.json")
        self.assertEqual(sorted(os.listdir(self.outside)), [], "nothing may be written outside the project")

    def test_C2_out_outside_state_inside(self):
        """EXPECTED: exit 2; stderr names "o.json"; the outside folder stays empty; the inside state file is NOT created
        (the refusal stops the run before the state write, GATE section 4, and state is written last as in JS1).
        (Unpatched prediction: exit 0, both files written, so it FAILS.)"""
        state = self._in("state", "seen.json")
        cp = _run_cli(state, self.outside / "o.json")
        self._assert_refused(cp, "o.json")
        self.assertEqual(sorted(os.listdir(self.outside)), [])
        self.assertFalse(state.exists(), "state must not be written after a refusal")

    def test_C3_state_outside_out_inside(self):
        """EXPECTED: exit 2; stderr names "s.json"; no file outside. Whether runs/... was written before the refusal is
        NOT asserted (GATE section 1 allows a partial write if the report names it). (Unpatched prediction: exit 0, s.json written outside, so it FAILS.)"""
        out = self._in("runs", "o.json")
        cp = _run_cli(self.outside / "s.json", out)
        self._assert_refused(cp, "s.json")
        self.assertEqual(sorted(os.listdir(self.outside)), [])

    def test_C4_control_both_inside_allowed(self):
        """EXPECTED: exit 0, and both files are created under state/ and runs/. This is a control, so that a "refuse everything"
        patch cannot pass. (Unpatched prediction: PASSES.)"""
        state, out = self._in("state", "seen.json"), self._in("runs", "o.json")
        cp = _run_cli(state, out)
        self.assertEqual(cp.returncode, 0, cp.stderr)
        self.assertTrue(state.exists() and out.exists())


class PolicyWriteBoundaries(unittest.TestCase):
    """Calls policy.check_write directly. (Unpatched prediction for every test here: ERROR, ModuleNotFoundError 'policy'.)"""

    def test_P1_B3_sibling_prefix_root(self):
        """EXPECTED: PermissionRefused for ../js2-loop-tools-diff-evil/x.json (a string-prefix check would accept it; that is wrong version W3)."""
        pol = _policy()
        with self.assertRaises(pol.PermissionRefused):
            pol.check_write(ROOT.parent / (ROOT.name + "-evil") / "x.json")

    def test_P2_B4_sibling_prefix_folder(self):
        """EXPECTED: PermissionRefused for ROOT/raw-evil/x.json (it starts with "raw" but is not raw/; W3)."""
        pol = _policy()
        with self.assertRaises(pol.PermissionRefused):
            pol.check_write(ROOT / "raw-evil" / "x.json")

    def test_P3_B6_dotdot_escape(self):
        """EXPECTED: PermissionRefused for ROOT/raw/../../js1-contract-and-watch/x.json (it resolves into the JS1 folder)."""
        pol = _policy()
        with self.assertRaises(pol.PermissionRefused):
            pol.check_write(ROOT / "raw" / ".." / ".." / "js1-contract-and-watch" / "x.json")

    def test_P4_B12_absolute_outside_temp(self):
        """EXPECTED: PermissionRefused for <%TEMP%>/x.json (absolute, outside the project)."""
        pol = _policy()
        with self.assertRaises(pol.PermissionRefused):
            pol.check_write(Path(tempfile.gettempdir()) / "x.json")

    def test_P5_B12_absolute_outside_system(self):
        """EXPECTED: PermissionRefused for C:/Windows/js2-x.txt (or /etc/js2-x.txt on POSIX). The file is never created."""
        pol = _policy()
        target = Path("C:/Windows/js2-x.txt") if os.name == "nt" else Path("/etc/js2-x.txt")
        with self.assertRaises(pol.PermissionRefused):
            pol.check_write(target)

    @unittest.skipUnless(os.name == "nt", "directory junctions are Windows-only")
    def test_P6_B5_junction_escape(self):
        """EXPECTED: PermissionRefused for ROOT/raw/<junction>/escape.json, where <junction> is an mklink /J pointing to a folder outside ROOT
        (a lexical check would accept it; that is W4). A true symlink is NOT tested: it needs admin or Developer Mode here (FRICTIONAL F8)."""
        pol = _policy()                                  # imported first: unpatched, nothing gets created
        target = Path(tempfile.mkdtemp(prefix="js2-junction-target-"))
        link = ROOT / "raw" / f"_test_junction_{uuid.uuid4().hex[:8]}"
        try:
            mk = subprocess.run(["cmd", "/c", "mklink", "/J", str(link), str(target)], capture_output=True, text=True)
            self.assertEqual(mk.returncode, 0, f"could not create junction: {mk.stdout}{mk.stderr}")
            with self.assertRaises(pol.PermissionRefused):
                pol.check_write(link / "escape.json")
            self.assertEqual(os.listdir(target), [], "nothing may land in the junction target")
        finally:
            if link.exists() or os.path.lexists(link):
                os.rmdir(link)                           # removes the junction only, not the target
            shutil.rmtree(target, ignore_errors=True)

    def test_P7_B8_inside_project_not_writable(self):
        """EXPECTED: PermissionRefused for fixtures/resume.fictional.json, GATE.md and jobwatch.py (inside ROOT, but not writable)."""
        pol = _policy()
        for rel in ("fixtures/resume.fictional.json", "GATE.md", "jobwatch.py"):
            with self.subTest(rel=rel), self.assertRaises(pol.PermissionRefused):
                pol.check_write(ROOT / rel)

    def test_P8_B10_overwrite_evidence_needs_approval(self):
        """EXPECTED: ApprovalRequired (a subclass of PermissionRefused) for the existing raw/2026-11-10/zoox.json with no approve list.
        Only the check runs; the file is not touched."""
        pol = _policy()
        self.assertTrue((ROOT / RAW_TODAY).exists())
        with self.assertRaises(pol.ApprovalRequired):
            pol.check_write(ROOT / RAW_TODAY)
        self.assertTrue(issubclass(pol.ApprovalRequired, pol.PermissionRefused))

    def test_P9_B11_overwrite_with_exact_approval(self):
        """EXPECTED: allowed with approve=("raw/2026-11-10/zoox.json",); it returns the resolved path. Approving a DIFFERENT
        path (raw/2026-11-10/openai.json) still raises ApprovalRequired for zoox.json. Only the check runs; nothing is written."""
        pol = _policy()
        got = pol.check_write(ROOT / RAW_TODAY, approve=(RAW_TODAY,))
        self.assertEqual(Path(got), (ROOT / RAW_TODAY).resolve())
        with self.assertRaises(pol.ApprovalRequired):
            pol.check_write(ROOT / RAW_TODAY, approve=("raw/2026-11-10/openai.json",))

    def test_P10_B9_new_file_in_writable_folders_allowed(self):
        """EXPECTED: allowed (returns the path inside ROOT) for a NEW file in each of raw/, state/, runs/, traces/. Nothing is written."""
        pol = _policy()
        for folder in ("raw", "state", "runs", "traces"):
            p = ROOT / folder / f"_never_written_{uuid.uuid4().hex[:8]}.json"
            with self.subTest(folder=folder):
                got = Path(pol.check_write(p))
                self.assertTrue(got.is_relative_to(ROOT.resolve()))
                self.assertFalse(p.exists())


class PolicyReadBoundaries(unittest.TestCase):
    """Read is not write (GATE D-10). (Unpatched prediction: ERROR, ModuleNotFoundError 'policy'.)"""

    def test_R1_B7_read_fixture_allowed(self):
        """EXPECTED: check_read(fixtures/resume.fictional.json) returns its resolved path (readable, although P7 shows it is not writable)."""
        pol = _policy()
        got = pol.check_read(ROOT / "fixtures" / "resume.fictional.json")
        self.assertEqual(Path(got), (ROOT / "fixtures" / "resume.fictional.json").resolve())

    def test_R2_read_outside_refused(self):
        """EXPECTED: PermissionRefused for check_read of a real file outside ROOT (a temp file)."""
        pol = _policy()
        fd, name = tempfile.mkstemp(prefix="js2-read-")
        os.close(fd)
        try:
            with self.assertRaises(pol.PermissionRefused):
                pol.check_read(name)
        finally:
            os.unlink(name)


if __name__ == "__main__":
    unittest.main(verbosity=2)
