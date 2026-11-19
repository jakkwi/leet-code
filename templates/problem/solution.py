"""{{NUMBER}}. {{TITLE}}: {{URL}}"""

from __future__ import annotations

from collections.abc import Callable

# ===== Your code: one function per variant. =====


# TODO: set the real signature here, in Solver below and in test_solution.py.
def brute_force(nums: list[int]) -> int:
    # TODO
    return 0


# ===== Registration: every variant listed here is tested against cases.json. =====

type Solver = Callable[[list[int]], int]

# Uncomment a line once its function is written; empty stubs stay out so the suite is green.
VARIANTS: dict[str, Solver] = {
    # "brute_force": brute_force,
}
