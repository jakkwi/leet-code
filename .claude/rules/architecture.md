---
paths:
  - "problems/**"
  - "common/**"
  - "templates/**"
  - "tools/**"
---

# Architecture: problem isolation

Layers would be overkill here. The one structural rule is that every problem is self-contained.

- A problem lives in `problems/<pattern>/<NNNN_slug>/` with `README.md`, `cases.json`, `solution.py`, `test_solution.py`. Pattern folders are the keys of `tools/patterns.py`.
- A problem may use the standard library, pytest and `lccommon` (in `common/`). Never another problem's files.
- Code moves into `common/` only when at least two problems need it and it is not part of any solution (test harness, `ListNode`, `TreeNode`). Algorithms never go into `common/`.
- `solution.py` is loaded by path (`lccommon.loader.load_sibling`), never via `sys.path` changes or relative imports.
- `tools/check_isolation.py` enforces all of this in CI. Create problems with `tools/new_problem.py`, not by hand.
