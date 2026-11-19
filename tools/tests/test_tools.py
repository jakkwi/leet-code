from __future__ import annotations

import sys
from pathlib import Path

import pytest

TOOLS = Path(__file__).resolve().parents[1]
sys.path.insert(0, str(TOOLS))

import check_isolation  # noqa: E402
import new_problem  # noqa: E402


@pytest.fixture
def repo(tmp_path: Path) -> Path:
    return tmp_path


def test_new_problem_renders_all_placeholders(repo: Path) -> None:
    path = new_problem.create(repo, "arrays_hashing", 1, "two-sum")
    assert path == repo / "problems" / "arrays_hashing" / "0001_two_sum"
    assert "0001. Two Sum" in (path / "solution.py").read_text(encoding="utf-8")
    assert "# 0001. Two Sum" in (path / "README.md").read_text(encoding="utf-8")
    assert b"\r\n" not in (path / "solution.py").read_bytes()
    assert check_isolation.check(repo) == []


def test_new_problem_rejects_bad_input(repo: Path) -> None:
    with pytest.raises(ValueError, match="pattern"):
        new_problem.create(repo, "nope", 1, "two-sum")
    with pytest.raises(ValueError, match="slug"):
        new_problem.create(repo, "arrays_hashing", 1, "Two_Sum")
    new_problem.create(repo, "arrays_hashing", 1, "two-sum")
    with pytest.raises(FileExistsError):
        new_problem.create(repo, "arrays_hashing", 1, "two-sum")


def test_isolation_flags_cross_problem_access(repo: Path) -> None:
    path = new_problem.create(repo, "arrays_hashing", 1, "two-sum")
    (path / "solution.py").write_text(
        "import sys\nimport numpy\nfrom . import other\nsys.path.insert(0, '..')\n",
        encoding="utf-8",
    )
    errors = "\n".join(check_isolation.check(repo))
    assert "'numpy'" in errors
    assert "relative imports" in errors
    assert "sys.path.insert" in errors


def test_isolation_flags_bad_cases(repo: Path) -> None:
    path = new_problem.create(repo, "arrays_hashing", 1, "two-sum")
    (path / "cases.json").write_text(
        '{"cases": [{"name": "a", "input": {}, "expected": 1},'
        ' {"name": "a", "input": {}, "expected": 2}, {"name": "b"}]}',
        encoding="utf-8",
    )
    errors = "\n".join(check_isolation.check(repo))
    assert "duplicate" in errors
    assert "needs name, input, expected" in errors


def test_isolation_flags_missing_files(repo: Path) -> None:
    path = new_problem.create(repo, "arrays_hashing", 1, "two-sum")
    (path / "test_solution.py").unlink()
    assert "missing test_solution.py" in "\n".join(check_isolation.check(repo))
