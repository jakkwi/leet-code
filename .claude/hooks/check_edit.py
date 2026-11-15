"""PostToolUse hook for Edit/Write: no new long dashes, code formatted.

Only lines that are new compared to the last commit are checked for dashes,
so older text never blocks an edit. Exit 2 shows the problem to the agent.
Python files go through ruff format, C++ files through clang-format
(templates excluded: their placeholders are not C++ yet).
"""

from __future__ import annotations

import json
import shutil
import subprocess
import sys
from pathlib import Path

DASHES = (chr(0x2014), chr(0x2013))  # em dash, en dash
CPP_SUFFIXES = {".cpp", ".hpp", ".h", ".cc"}


def committed_lines(path: Path, root: Path) -> set[str]:
    try:
        rel = path.resolve().relative_to(root).as_posix()
    except ValueError:
        return set()
    old = subprocess.run(
        ["git", "show", f"HEAD:{rel}"],
        capture_output=True,
        text=True,
        encoding="utf-8",
        check=False,
        cwd=root,
    )
    return set(old.stdout.splitlines()) if old.returncode == 0 else set()


def find_tool(name: str, root: Path) -> str | None:
    for candidate in (root / ".venv" / "Scripts" / f"{name}.exe", root / ".venv" / "bin" / name):
        if candidate.is_file():
            return str(candidate)
    return shutil.which(name)


def main() -> int:
    data = json.load(sys.stdin)
    root = Path(data.get("cwd") or Path.cwd()).resolve()
    path = Path(data.get("tool_input", {}).get("file_path", ""))
    if not path.is_file():
        return 0
    try:
        text = path.read_text(encoding="utf-8")
    except (UnicodeDecodeError, OSError):
        return 0

    old = committed_lines(path, root)
    bad = [
        i + 1
        for i, line in enumerate(text.splitlines())
        if any(d in line for d in DASHES) and line not in old
    ]
    if bad:
        print(
            f"{path}: long dash on new line(s) {bad}. "
            "Use a comma, colon, parentheses or a plain hyphen.",
            file=sys.stderr,
        )
        return 2

    formatter: list[str] = []
    if path.suffix == ".py" and (ruff := find_tool("ruff", root)):
        formatter = [ruff, "format", "--quiet"]
    elif path.suffix in CPP_SUFFIXES and "templates" not in path.resolve().parts:
        cf = find_tool("clang-format", root)
        formatter = [cf, "-i"] if cf else []
    if formatter:
        subprocess.run([*formatter, str(path)], check=False, cwd=root)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
