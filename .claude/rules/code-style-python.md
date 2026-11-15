---
paths:
  - "**/*.py"
---

# Python style

- ruff (config in `pyproject.toml`) for lint and format, mypy `--strict` via `tools/run_mypy.py`.
- Type hints everywhere; builtin generics (`list[int]`, `dict[str, int]`), `X | None`, PEP 695 `type` aliases.
- Variants are module-level functions registered in `VARIANTS`.
- Idioms to point out in review: `enumerate` over `range(len(...))`, dict / set comprehensions, `collections` (`Counter`, `defaultdict`, `deque`), `heapq`, `bisect`, slicing costs a copy, `in` on a list is O(n) but on a set / dict average O(1).
- When comparing with C++, name what Python hides: arbitrary precision ints (no overflow), objects behind every list slot (no contiguous ints), hash randomization, amortized list growth, recursion limit.
- Standard library only inside `problems/`.
