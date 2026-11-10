"""policy.py: the JS2 permission policy for file paths, enforced in code (GATE.md section 5, D-10 and D-11; APPROVED 2026-11-10 08:17:25 EST).

  read   allowed under ROOT/{fixtures, raw, state, prompts} and the file ROOT/GATE.md
  write  allowed under ROOT/{raw, state, runs, traces}
         overwriting an EXISTING file under raw/ (evidence) needs approval: approve=("raw/<...>",), with exact ROOT-relative paths
  everything else is refused, including every path outside the project folder.

How a path is checked (D-11): resolve it fully with os.path.realpath, which follows symlinks and junctions on every existing component
and appends the rest, then compare path COMPONENTS after os.path.normcase. String prefixes are never compared, so `raw-evil/` is not `raw/`
and `js2-loop-tools-diff-evil/` is not the project folder. A relative path is taken relative to the current working directory,
exactly as the OS would interpret it.

Python standard library only. This module only answers questions: it never reads, writes or creates anything.
"""
from __future__ import annotations

import os
from pathlib import Path, PurePosixPath

ROOT = Path(os.path.realpath(Path(__file__).resolve().parent))
READ_DIRS = ("fixtures", "raw", "state", "prompts")
READ_FILES = ("GATE.md",)
WRITE_DIRS = ("raw", "state", "runs", "traces")
APPROVAL_DIRS = ("raw",)


class PermissionRefused(Exception):
    """A read or write the policy does not allow. GATE section 4: it stops the whole run, with no retry."""


class ApprovalRequired(PermissionRefused):
    """A write the policy allows only with Prathamesh's explicit, per-path approval."""


def _resolve(path) -> Path:
    return Path(os.path.realpath(os.fspath(path)))


def _relative_parts(resolved: Path) -> tuple[str, ...] | None:
    """The normcased components of `resolved` below ROOT, or None if it is not inside ROOT (component comparison)."""
    r = Path(os.path.normcase(resolved))
    root = Path(os.path.normcase(ROOT))
    if r != root and root not in r.parents:
        return None
    return r.relative_to(root).parts


def _norm(names) -> set[str]:
    return {os.path.normcase(n) for n in names}


def check_read(path) -> Path:
    """Return the fully resolved path if reading it is allowed, otherwise raise PermissionRefused."""
    resolved = _resolve(path)
    parts = _relative_parts(resolved)
    if parts is None:
        raise PermissionRefused(f"read refused: {path} resolves to {resolved}, outside the project folder {ROOT}")
    if len(parts) == 1 and parts[0] in _norm(READ_FILES):
        return resolved
    if len(parts) >= 2 and parts[0] in _norm(READ_DIRS):
        return resolved
    raise PermissionRefused(f"read refused: {path} is not under a readable folder {READ_DIRS} or file {READ_FILES}")


def check_write(path, approve=()) -> Path:
    """Return the fully resolved path if writing it is allowed, otherwise raise PermissionRefused (or ApprovalRequired)."""
    resolved = _resolve(path)
    parts = _relative_parts(resolved)
    if parts is None:
        raise PermissionRefused(f"write refused: {path} resolves to {resolved}, outside the project folder {ROOT}")
    if len(parts) < 2 or parts[0] not in _norm(WRITE_DIRS):
        raise PermissionRefused(f"write refused: {path} is not under a writable folder {WRITE_DIRS}")
    if parts[0] in _norm(APPROVAL_DIRS) and resolved.exists():
        rel = PurePosixPath(*parts).as_posix()
        # both sides normalized the same way: normcase (on Windows: lower case AND "/" -> "\\"), then split into components
        approved = {PurePosixPath(*Path(os.path.normcase(a)).parts).as_posix() for a in approve}
        if rel not in approved:
            raise ApprovalRequired(f"write refused: {path} would overwrite existing evidence; "
                                   f"it needs Prathamesh's approval (--approve {rel})")
    return resolved
