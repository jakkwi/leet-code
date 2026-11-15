---
description: Review Jakub's solution code (correctness, complexity, C++/Python style)
argument-hint: [problem folder, defaults to uncommitted changes]
---
Review `$ARGUMENTS` (or, if empty, the uncommitted changes from `git diff` and untracked files under `problems/`).

1. Build and run the tests (`cmake --build --preset debug`, `ctest --preset debug`, `uv run pytest`). Report failures and sanitizer output first.
2. Use the code-reviewer agent for correctness, UB and style, and the complexity-analyzer agent for time and space of each variant.
3. Answer in Polish: Blocking / Should fix / Nice to have, each with `file:line`, the problem and why it matters. Explain fixes in words; write fixed code only for infrastructure, never for solution bodies unless Jakub wrote "pokaż rozwiązanie".
4. Ask Jakub what complexity he thinks each variant has before stating yours, if he has not said it yet.
