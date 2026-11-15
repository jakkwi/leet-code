"""0001. Two Sum: https://leetcode.com/problems/two-sum/"""

from __future__ import annotations

from collections.abc import Callable

# (nums, target) -> indices of the two numbers that add up to target, in any order.
type Solver = Callable[[list[int], int], list[int]]


# Variants go here, one function each.


# Every variant listed here is run against every case in cases.json.
VARIANTS: dict[str, Solver] = {
    # "brute_force": brute_force,
}
