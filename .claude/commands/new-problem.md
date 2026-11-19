---
description: Scaffold a LeetCode problem and start the mentoring workflow
argument-hint: <pattern> <number> <leetcode-slug>
---
Create the problem folder: `uv run python tools/new_problem.py $ARGUMENTS`.

Then:
1. Set the shared signature: the `brute_force` stub and `Solver` alias in `solution.py`, and the call in `test_solution.py`. If the answer order does not matter, normalize in the test. Add LeetCode's official examples to `cases.json`. Nothing else: the stub body stays `# TODO`.
2. Run `uv run pytest` on the new folder: the examples fail against the stub, which is expected.
3. Present the problem to Jakub in Polish: statement in your own words, constraints, one example. Ask for his intuition and what brute force he would write. Do not hint at the optimal approach.

If this is the first problem of its pattern, follow the full workflow from CLAUDE.md; otherwise move faster.
