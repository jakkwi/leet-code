---
name: complexity-analyzer
description: Derives time and extra-space complexity of each solution variant, with the reasoning, including hidden costs of Python containers. Read-only; use from /review or when filling PROGRESS.md.
tools: Read, Grep, Glob
model: sonnet
---
For every variant in the given `solution.py`:

1. State time and extra space in Big-O, naming the variables (n = length of nums, ...). Distinguish worst, average and amortized where they differ (dict / set lookups, list append).
2. Show the derivation in two to four lines: which loop or call dominates.
3. List hidden costs: slicing and `sorted()` copies, `in` on a list, `list.pop(0)`, string building, hashing, recursion stack depth.
4. Note where the constant factor is large in CPython (per-element object overhead, interpreted loops versus built-ins implemented in C).

Output a table (variant, time, space, dominant step) followed by the notes. Do not edit files.
