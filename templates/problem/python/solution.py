"""{{NUMBER}}. {{TITLE}}: {{URL}}"""

from __future__ import annotations

from collections.abc import Callable

# TODO: set the signature every variant shares (and the call in test_solution.py).
type Solver = Callable[[list[int]], int]


# Variants go here, one function each.


# Every variant listed here is run against every case in cases.json.
VARIANTS: dict[str, Solver] = {
    # "brute_force": brute_force,
}
