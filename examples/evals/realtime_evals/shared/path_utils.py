from pathlib import Path
import os
import re
from typing import Iterable

"""Path utilities to prevent path traversal in realtime eval harnesses.

This module provides:
- validate_example_id: fail-fast validation for example_id/simulation_id values.
- safe_join: join relative path parts onto a base directory, resolve, and ensure
  the final path is contained within the base directory. Rejects absolute paths
  and user/variable expansions.

Note: This mitigates the common path-traversal cases used by the realtime eval
harnesses. It does not fully eliminate TOCTOU/symlink races if untrusted
processes can manipulate the filesystem between the check and a subsequent open()
or write(). For deployments that require complete protection against that class of
attacks, consider opening files with dirfds + O_NOFOLLOW or running harnesses in
isolated containers.
"""

_SAFE_ID_RE = re.compile(r"^[A-Za-z0-9_.-]+$")


def validate_example_id(example_id: str) -> None:
    """
    Raise ValueError if example_id contains path separators, parent refs, or other unsafe chars.
    Accepts only letters, digits, underscore, dot, and hyphen.
    """
    if not isinstance(example_id, str) or not example_id.strip():
        raise ValueError(f"invalid example_id: {example_id!r}")
    if not _SAFE_ID_RE.match(example_id):
        raise ValueError(f"invalid example_id: {example_id!r}")


def _normalize_no_user_expansion(p: str) -> str:
    # Disallow ~ and environment expansion on input strings for safety:
    if p.startswith("~") or "${" in p or p.startswith("$"):
        raise ValueError(f"disallowed path expansion in: {p!r}")
    return p


def safe_join(base: Path, *parts: Iterable[str]) -> Path:
    """
    Join parts onto base, resolve to an absolute path, and check the result is inside base.
    Raises ValueError if the resulting path escapes the base directory.
    """
    base = Path(base).resolve()
    candidate = base
    for part in parts:
        if not isinstance(part, str):
            raise ValueError("path parts must be strings")
        part = _normalize_no_user_expansion(part)
        p = Path(part)
        if p.is_absolute():
            # Absolute paths are not allowed
            raise ValueError(f"absolute paths are not allowed: {part!r}")
        candidate = candidate.joinpath(p)
    # Resolve final path to eliminate ../ and symlinks
    candidate_resolved = candidate.resolve()
    # os.path.commonpath raises ValueError if drives differ on Windows
    try:
        common = os.path.commonpath([str(base), str(candidate_resolved)])
    except ValueError:
        raise ValueError(f"Path {candidate_resolved} is not in base {base}")
    if common != str(base):
        raise ValueError(f"Path {candidate_resolved} escapes base directory {base}")
    return candidate_resolved
