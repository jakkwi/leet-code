---
paths:
  - "**/*.py"
---

# Python style

- ruff (config in `pyproject.toml`) for lint and format, mypy `--strict` via `tools/run_mypy.py`.
- Type hints everywhere; builtin generics (`list[int]`, `dict[str, int]`), `X | None`, PEP 695 `type` aliases.
- Variants are module-level functions named after the idea (`brute_force`, `sort_two_pointers`, `hash_map_one_pass`), registered in `VARIANTS`.
- Standard library only inside `problems/`.

## In code review, check
- Hidden costs: `x in list` is O(n) but O(1) average on a `set` / `dict`; slicing and `sorted()` copy; `list.pop(0)` and `insert(0, ...)` are O(n) (use `collections.deque`); string `+=` in a loop is quadratic (use `"".join`).
- Container choice: `list`, `dict`, `set`, `Counter`, `defaultdict`, `deque`, `heapq`, `bisect`, and why.
- Mutating the input when the caller does not expect it (for example sorting `nums` in place).
- Idioms: `enumerate` over `range(len(...))`, comprehensions, unpacking, `zip`, early `return`.
- Recursion depth (default limit about 1000) for deep trees or DFS.
- What is under the hood: every list slot is a pointer to an int object, ints never overflow, `dict` keeps insertion order, hashing has a cost.
- Comments explain why, not what. English only.
