---
description: Scaffold a LeetCode problem and start the mentoring workflow
argument-hint: <pattern> <number> <leetcode-slug>
---
Create the problem folder: `uv run python tools/new_problem.py $ARGUMENTS`.

Then:
1. Set the shared signature: the `Solver` alias in `cpp/solution.hpp`, the call in `cpp/test.cpp`, the `Solver` type and call in `python/`. If the answer order does not matter, normalize in the tests. Add LeetCode's official examples to `cases.json`. Nothing else: no variant bodies.
2. Re-run `cmake --preset debug`, build, and confirm ctest and pytest pass (zero variants is valid).
3. Present the problem to Jakub in Polish: statement in your own words, constraints, one example. Ask for his intuition and what brute force he would write. Do not hint at the optimal approach.

If this is the first problem of its pattern, follow the full workflow from CLAUDE.md; otherwise move faster.
