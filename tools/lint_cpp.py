"""clang-format check (or fix) and optional clang-tidy for all C++ sources.

Usage:
    uv run python tools/lint_cpp.py            # check formatting
    uv run python tools/lint_cpp.py --fix      # rewrite files in place
    uv run python tools/lint_cpp.py --tidy build/debug   # also run clang-tidy

Templates are skipped: their {{PLACEHOLDERS}} are not valid C++ until rendered.
"""

from __future__ import annotations

import argparse
import shutil
import subprocess
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
DIRS = ("common/cpp", "problems")


def sources() -> list[Path]:
    files: list[Path] = []
    for d in DIRS:
        files += sorted((ROOT / d).rglob("*.[ch]pp"))
    return files


def tool(name: str) -> str:
    path = shutil.which(name)
    if path is None:
        print(f"{name} not found; run `uv sync` first", file=sys.stderr)
        raise SystemExit(2)
    return path


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--fix", action="store_true")
    parser.add_argument("--tidy", metavar="BUILD_DIR", help="dir with compile_commands.json")
    args = parser.parse_args(argv)

    files = [str(f) for f in sources()]
    fmt = [tool("clang-format"), *(["-i"] if args.fix else ["--dry-run", "--Werror"]), *files]
    rc = subprocess.run(fmt, cwd=ROOT, check=False).returncode

    if args.tidy:
        cpp_files = [f for f in files if f.endswith(".cpp")]
        # MSVC-only flags in compile_commands.json are not errors for clang-tidy.
        tidy = [tool("clang-tidy"), "-p", args.tidy, "--quiet"]
        tidy += ["--extra-arg=-Wno-unused-command-line-argument", *cpp_files]
        rc |= subprocess.run(tidy, cwd=ROOT, check=False).returncode

    print(f"C++ lint: {len(files)} file(s), {'ok' if rc == 0 else 'FAILED'}")
    return rc


if __name__ == "__main__":
    raise SystemExit(main())
