"""Run mypy --strict on every Python tree.

Each problem has its own solution.py, and mypy refuses two modules with the
same name in one run, so problem folders are checked one at a time.
"""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SHARED = ["common/python", "tools", ".claude/hooks"]


def targets() -> list[list[str]]:
    runs = [SHARED]
    runs += [[p.relative_to(ROOT).as_posix()] for p in sorted(ROOT.glob("problems/*/*/python"))]
    return runs


def main() -> int:
    failed = 0
    for paths in targets():
        result = subprocess.run([sys.executable, "-m", "mypy", *paths], cwd=ROOT, check=False)
        failed += result.returncode != 0
    return 1 if failed else 0


if __name__ == "__main__":
    raise SystemExit(main())
