"""Create a problem folder from templates/problem.

Usage:
    uv run python tools/new_problem.py <pattern> <number> <leetcode-slug> [--title "Two Sum"]

Example:
    uv run python tools/new_problem.py arrays_hashing 1 two-sum
"""

from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from patterns import PATTERNS

ROOT = Path(__file__).resolve().parents[1]
TEMPLATE = ROOT / "templates" / "problem"
SLUG_RE = re.compile(r"^[a-z0-9]+(-[a-z0-9]+)*$")


def placeholders(pattern: str, number: int, slug: str, title: str) -> dict[str, str]:
    snake = slug.replace("-", "_")
    return {
        "NUMBER": f"{number:04d}",
        "TITLE": title,
        "URL": f"https://leetcode.com/problems/{slug}/",
        "PATTERN_TITLE": PATTERNS[pattern],
        "NAMESPACE": f"p{number:04d}_{snake}",
        "SUITE": "".join(part.capitalize() for part in slug.split("-")),
    }


def render(text: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        text = text.replace("{{" + key + "}}", value)
    leftover = re.search(r"\{\{[A-Z_]+\}\}", text)
    if leftover:
        msg = f"unknown placeholder {leftover.group(0)}"
        raise ValueError(msg)
    return text


def create(root: Path, pattern: str, number: int, slug: str, title: str | None = None) -> Path:
    if pattern not in PATTERNS:
        msg = f"unknown pattern {pattern!r}, expected one of: {', '.join(PATTERNS)}"
        raise ValueError(msg)
    if not SLUG_RE.match(slug):
        msg = f"slug must look like 'two-sum', got {slug!r}"
        raise ValueError(msg)
    if not 1 <= number <= 9999:
        msg = "number must be 1..9999"
        raise ValueError(msg)

    title = title or " ".join(word.capitalize() for word in slug.split("-"))
    target = root / "problems" / pattern / f"{number:04d}_{slug.replace('-', '_')}"
    if target.exists():
        msg = f"{target} already exists"
        raise FileExistsError(msg)

    values = placeholders(pattern, number, slug, title)
    for src in sorted(TEMPLATE.rglob("*")):
        if src.is_dir():
            continue
        dst = target / src.relative_to(TEMPLATE)
        dst.parent.mkdir(parents=True, exist_ok=True)
        dst.write_text(render(src.read_text(encoding="utf-8"), values), encoding="utf-8")
    return target


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__.splitlines()[0] if __doc__ else None)
    parser.add_argument("pattern", choices=PATTERNS)
    parser.add_argument("number", type=int)
    parser.add_argument("slug", help="LeetCode URL slug, e.g. two-sum")
    parser.add_argument("--title")
    args = parser.parse_args(argv)
    try:
        path = create(ROOT, args.pattern, args.number, args.slug, args.title)
    except (ValueError, FileExistsError) as exc:
        print(f"error: {exc}", file=sys.stderr)
        return 1
    print(f"created {path.relative_to(ROOT).as_posix()}")
    print("re-run CMake configure so the new test target is picked up")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
