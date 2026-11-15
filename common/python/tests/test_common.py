"""Self-test of the shared Python harness."""

from __future__ import annotations

from collections.abc import Callable
from pathlib import Path

import pytest

from lccommon.cases import Case, load_cases, variant_case_params
from lccommon.list_node import ListNode, from_list, to_list
from lccommon.tree_node import from_level_order, to_level_order

SAMPLE = Path(__file__).resolve().parents[2] / "testdata" / "sample_cases.json"

VARIANTS: dict[str, Callable[[int, int], int]] = {
    "add": lambda a, b: a + b,
    "add_reversed": lambda a, b: b + a,
}


def test_load_cases_reads_all_fields() -> None:
    cases = load_cases(SAMPLE)
    assert [c.name for c in cases] == ["sum_basic", "sum negative"]
    assert cases[0].input == {"a": 2, "b": 3}
    assert cases[0].expected == 5
    assert cases[0].note == ""
    assert cases[1].note


def test_variant_case_params_is_cartesian_product() -> None:
    assert len(variant_case_params(VARIANTS, load_cases(SAMPLE))) == 4


@pytest.mark.parametrize(("fn", "case"), variant_case_params(VARIANTS, load_cases(SAMPLE)))
def test_sample_matches_expected(fn: Callable[[int, int], int], case: Case) -> None:
    assert fn(case.input["a"], case.input["b"]) == case.expected, case.note


def test_list_round_trip() -> None:
    assert to_list(from_list([1, 2, 3])) == [1, 2, 3]
    assert from_list([]) is None


def test_list_cycle_detected() -> None:
    head = from_list([1, 2])
    assert head is not None
    assert head.next is not None
    head.next.next = head
    with pytest.raises(ValueError, match="cycle"):
        to_list(head, max_nodes=10)


def test_list_node_repr() -> None:
    assert repr(ListNode(1, ListNode(2))) == "ListNode([1, 2])"


@pytest.mark.parametrize(
    "values",
    [[3, 9, 20, None, None, 15, 7], [1, None, 2], [1], []],
)
def test_tree_round_trip(values: list[int | None]) -> None:
    assert to_level_order(from_level_order(values)) == values


def test_tree_trailing_nulls_trimmed() -> None:
    assert to_level_order(from_level_order([1, None, 2, None, None])) == [1, None, 2]
