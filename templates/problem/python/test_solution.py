from __future__ import annotations

from pathlib import Path
from typing import Any

import pytest

from lccommon.cases import Case, load_cases, variant_case_params
from lccommon.loader import load_sibling

solution = load_sibling(__file__)
CASES = load_cases(Path(__file__).resolve().parents[1] / "cases.json")


@pytest.mark.parametrize(("fn", "case"), variant_case_params(solution.VARIANTS, CASES))
def test_matches_expected(fn: Any, case: Case) -> None:
    # TODO: adapt to the problem's signature.
    assert fn(case.input["nums"]) == case.expected, case.note
