from __future__ import annotations

import os
from pathlib import Path


class RootResolutionError(ValueError):
    """Raised when ProseKernel cannot find its repo/data root."""


_REQUIRED_MARKERS = (
    "pyproject.toml",
    "library",
    "patterns",
    "src/prosekernel",
)


def _is_prosekernel_root(path: Path) -> bool:
    return all((path / marker).exists() for marker in _REQUIRED_MARKERS)


def _human_root_error(start: Path, attempted: Path | None = None) -> str:
    attempted_line = f"\nChecked root candidate: {attempted}" if attempted else f"\nSearched upward from: {start}"
    return (
        "ProseKernel needs access to its repo/data root."
        f"{attempted_line}\n"
        "Expected to find pyproject.toml, library/, patterns/, and src/prosekernel.\n"
        "Please run from the repo root, pass --root /path/to/prosekernel, "
        "or set PROSEKERNEL_ROOT=/path/to/prosekernel."
    )


def resolve_root(explicit_root: Path | str | None = None) -> Path:
    """Resolve the ProseKernel repo/data root for installed and repo-local CLI use.

    Precedence:
    1. Explicit --root argument.
    2. PROSEKERNEL_ROOT environment variable.
    3. Search upward from the current working directory for repo/data markers.

    Raises RootResolutionError with a human-readable fix when no valid root exists.
    """

    cwd = Path.cwd().resolve()

    if explicit_root is not None:
        candidate = Path(explicit_root).expanduser().resolve()
        if _is_prosekernel_root(candidate):
            return candidate
        raise RootResolutionError(_human_root_error(cwd, attempted=candidate))

    env_root = os.environ.get("PROSEKERNEL_ROOT")
    if env_root:
        candidate = Path(env_root).expanduser().resolve()
        if _is_prosekernel_root(candidate):
            return candidate
        raise RootResolutionError(_human_root_error(cwd, attempted=candidate))

    for candidate in (cwd, *cwd.parents):
        if _is_prosekernel_root(candidate):
            return candidate

    raise RootResolutionError(_human_root_error(cwd))
