from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from lccommon.cases import Case, load_cases, variant_case_params
from lccommon.loader import load_sibling

solution = load_sibling(__file__)
CASES = load_cases(Path(__file__).resolve().parent / "cases.json")


@pytest.mark.parametrize(("fn", "case"), variant_case_params(solution.VARIANTS, CASES))
def test_matches_expected(fn: Any, case: Case) -> None:
    got = fn(case.input["nums"], case.input["target"])
    # Any order is accepted, so compare sorted index pairs.
    assert sorted(got) == sorted(case.expected), case.note
