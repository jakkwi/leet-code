"""0001. Two Sum: https://leetcode.com/problems/two-sum/"""

from __future__ import annotations

from collections.abc import Callable

# ===== Your code: one function per variant. =====


def brute_force(nums: list[int], target: int) -> list[int]:
    """Indices of the two numbers that add up to target, in any order."""
    # TODO
    return []


# ===== Registration: every variant listed here is tested against cases.json. =====

type Solver = Callable[[list[int], int], list[int]]

# Uncomment a line once its function is written; empty stubs stay out so the suite is green.
VARIANTS: dict[str, Solver] = {
    # "brute_force": brute_force,
}
