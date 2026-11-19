"""Architecture check: every problem folder is self-contained.

Rules (see .claude/rules/architecture.md):
- problems/<pattern>/<NNNN_slug>/ with a known pattern and a well-formed name;
- every problem has the full file set;
- Python imports only the standard library, lccommon and pytest, and never
  touches sys.path or another problem's files;
- cases.json is well formed and case names are unique.

Exit code 1 lists every violation.
"""

from __future__ import annotations

import ast
import json
import re
import sys
from pathlib import Path

if __package__ in (None, ""):
    sys.path.insert(0, str(Path(__file__).resolve().parent))

from patterns import PATTERNS

ROOT = Path(__file__).resolve().parents[1]
REQUIRED = ("README.md", "cases.json", "solution.py", "test_solution.py")
PROBLEM_RE = re.compile(r"^\d{4}_[a-z0-9]+(_[a-z0-9]+)*$")
ALLOWED_PY = {"lccommon", "pytest", "__future__"} | set(sys.stdlib_module_names)
FORBIDDEN_CALLS = {"sys.path.insert", "sys.path.append", "importlib.import_module"}


def _dotted(node: ast.expr) -> str:
    if isinstance(node, ast.Name):
        return node.id
    if isinstance(node, ast.Attribute):
        return f"{_dotted(node.value)}.{node.attr}"
    return ""


def check_python(problem: Path) -> list[str]:
    errors: list[str] = []
    for src in sorted(problem.glob("*.py")):
        tree = ast.parse(src.read_text(encoding="utf-8"), filename=str(src))
        for node in ast.walk(tree):
            if isinstance(node, ast.Import):
                roots = [alias.name.split(".")[0] for alias in node.names]
            elif isinstance(node, ast.ImportFrom):
                if node.level:
                    errors.append(f"{src}:{node.lineno}: relative imports are not allowed")
                    continue
                roots = [(node.module or "").split(".")[0]]
            elif isinstance(node, ast.Call) and _dotted(node.func) in FORBIDDEN_CALLS:
                errors.append(f"{src}:{node.lineno}: {_dotted(node.func)} is not allowed")
                continue
            else:
                continue
            errors.extend(
                f"{src}:{node.lineno}: import of {root!r} (allowed: stdlib, lccommon, pytest)"
                for root in roots
                if root not in ALLOWED_PY
            )
    return errors


def check_cases(problem: Path) -> list[str]:
    path = problem / "cases.json"
    try:
        data = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        return [f"{path}: invalid JSON: {exc}"]
    cases = data.get("cases") if isinstance(data, dict) else None
    if not isinstance(cases, list):
        return [f"{path}: top level must be an object with a 'cases' list"]
    errors: list[str] = []
    seen: set[str] = set()
    for i, case in enumerate(cases):
        if not isinstance(case, dict) or not {"name", "input", "expected"} <= case.keys():
            errors.append(f"{path}: case #{i} needs name, input, expected")
            continue
        if not isinstance(case["input"], dict):
            errors.append(f"{path}: case {case['name']!r}: input must be an object")
        if case["name"] in seen:
            errors.append(f"{path}: duplicate case name {case['name']!r}")
        seen.add(case["name"])
    return errors


def check(root: Path) -> list[str]:
    problems_dir = root / "problems"
    if not problems_dir.is_dir():
        return []
    errors: list[str] = []
    for pattern_dir in sorted(p for p in problems_dir.iterdir() if p.is_dir()):
        if pattern_dir.name not in PATTERNS:
            errors.append(f"{pattern_dir}: unknown pattern folder")
            continue
        for problem in sorted(p for p in pattern_dir.iterdir() if p.is_dir()):
            if not PROBLEM_RE.match(problem.name):
                errors.append(f"{problem}: folder name must look like 0001_two_sum")
                continue
            missing = [f for f in REQUIRED if not (problem / f).is_file()]
            if missing:
                errors.append(f"{problem}: missing {', '.join(missing)}")
                continue
            errors += check_python(problem) + check_cases(problem)
    return errors


def main() -> int:
    errors = check(ROOT)
    for err in errors:
        print(err, file=sys.stderr)
    count = sum(1 for _ in (ROOT / "problems").glob("*/*/")) if (ROOT / "problems").is_dir() else 0
    print(f"isolation check: {count} problem(s), {len(errors)} violation(s)")
    return 1 if errors else 0


if __name__ == "__main__":
    raise SystemExit(main())
