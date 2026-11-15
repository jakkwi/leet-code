# leetcode-cpp-python

Algorithms and data structures practice on LeetCode problems, in C++20 (main) and
Python 3.12+ (second). Every problem has several solutions of different complexity,
one shared set of test cases for both languages, and a write-up of the reasoning.

Progress and per-problem complexity: [PROGRESS.md](PROGRESS.md).

## Layout

| Path | Contents |
|---|---|
| `problems/<pattern>/<NNNN_slug>/` | One problem: `README.md`, `cases.json`, `cpp/`, `python/` |
| `problems/.../cases.json` | Test cases read by both the GoogleTest and the pytest suite |
| `problems/.../cpp/solution.hpp` | Every variant as a separate function, plus the `variants()` list |
| `problems/.../python/solution.py` | Same variants in Python, plus the `VARIANTS` dict |
| `common/cpp/include/lc/` | Header-only test harness, `ListNode`, `TreeNode` |
| `common/python/lccommon/` | Python counterpart of the above |
| `templates/problem/` | Skeleton used by `tools/new_problem.py` |
| `tools/` | Problem scaffolding, isolation check, lint and mypy runners |

Each problem is self-contained: it may use the standard library and `common/`, never
another problem. `tools/check_isolation.py` enforces this in CI.

## How the tests work

Each test is parameterized over variants x cases: adding a function to `variants()`
(C++) or `VARIANTS` (Python) runs it against every case in `cases.json` with no other
change. A failing test is named `<variant>__<case>`, so it points at both.

## Tooling

| Tool | Version / setting |
|---|---|
| C++ | C++20, CMake 3.28+, Ninja |
| Tests | GoogleTest 1.18.0, optional Google Benchmark 1.10.0 (pinned commits, SHA-256 checked) |
| Debug build | AddressSanitizer on MSVC; ASan + UBSan on GCC/Clang |
| C++ lint | clang-format and clang-tidy 19 (installed by uv) |
| Python | 3.12+, uv, pytest, ruff, mypy --strict |
| CI | GitHub Actions: Linux Clang (ASan + UBSan), Windows MSVC (ASan), Python, lint, gitleaks, pip-audit |

## Commands

On Windows run the C++ commands from a Developer PowerShell for VS 2022 (MSVC on PATH).

```bash
uv sync
```

```bash
cmake --preset debug
```

```bash
cmake --build --preset debug
```

```bash
ctest --preset debug
```

```bash
uv run pytest
```

```bash
uv run ruff check . && uv run ruff format --check . && uv run python tools/run_mypy.py
```

```bash
uv run python tools/lint_cpp.py
```

```bash
uv run python tools/check_isolation.py
```

New problem (then re-run `cmake --preset debug`):

```bash
uv run python tools/new_problem.py arrays_hashing 217 contains-duplicate
```
