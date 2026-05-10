"""BTLkiemthu test launcher.

This repository keeps implementation in `src/` and tests in `tests/`.
Run this file from the repo root to execute the full unittest suite.
"""

from __future__ import annotations

import sys
import unittest
from pathlib import Path


def main() -> int:
    repo_root = Path(__file__).resolve().parent
    tests_dir = repo_root / "tests"

    if not tests_dir.is_dir():
        print("ERROR: 'tests/' folder not found.", file=sys.stderr)
        print("Run from the repository root, e.g.:", file=sys.stderr)
        print("  python -m unittest discover -s tests -v", file=sys.stderr)
        return 2

    suite = unittest.defaultTestLoader.discover(
        start_dir=str(tests_dir),
        pattern="test*.py",
        top_level_dir=str(repo_root),
    )
    result = unittest.TextTestRunner(verbosity=2).run(suite)
    return 0 if result.wasSuccessful() else 1


if __name__ == "__main__":
    raise SystemExit(main())
