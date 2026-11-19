# leetcode-python

Algorithms and data structures practice on LeetCode problems in Python. Every problem
has several solutions of different complexity, a set of test cases run against all of
them, and a write-up of the reasoning.

Progress and per-problem complexity: [PROGRESS.md](PROGRESS.md).

## Layout

| Path | Contents |
|---|---|
| `problems/<pattern>/<NNNN_slug>/` | One problem: `README.md`, `cases.json`, `solution.py`, `test_solution.py` |
| `problems/.../solution.py` | Every variant as a separate function, plus the `VARIANTS` dict |
| `problems/.../cases.json` | Test cases, run against every variant |
| `common/lccommon/` | Test harness, `ListNode`, `TreeNode` |
| `templates/problem/` | Skeleton used by `tools/new_problem.py` |
| `tools/` | Problem scaffolding, isolation check, mypy runner |

Each problem is self-contained: it may use the standard library and `lccommon`, never
another problem. `tools/check_isolation.py` enforces this in CI.

## How the tests work

Each test is parameterized over variants x cases: adding a function to `VARIANTS` runs it
against every case in `cases.json` with no other change. A failing test is named
`<variant>-<case>`, so it points at both.

## Tooling

| Tool | Setting |
|---|---|
| Python | 3.12+, managed by uv |
| Tests | pytest |
| Lint and format | ruff |
| Types | mypy --strict |
| CI | GitHub Actions: tests, lint, types, isolation check, gitleaks, pip-audit |

## Commands

```bash
uv sync
```

```bash
uv run pytest
```

```bash
uv run ruff check . && uv run ruff format --check . && uv run python tools/run_mypy.py
```

```bash
uv run python tools/check_isolation.py
```

New problem:

```bash
uv run python tools/new_problem.py arrays_hashing 217 contains-duplicate
```
