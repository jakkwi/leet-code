"""Loader for a problem's cases.json."""

from __future__ import annotations

import json
from collections.abc import Callable, Iterable
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any

import pytest


@dataclass(frozen=True, slots=True)
class Case:
    name: str
    input: dict[str, Any]
    expected: Any
    note: str = field(default="")


def load_cases(path: Path) -> list[Case]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    return [
        Case(
            name=item["name"],
            input=item["input"],
            expected=item["expected"],
            note=item.get("note", ""),
        )
        for item in raw["cases"]
    ]


def variant_case_params[F: Callable[..., Any]](
    variants: dict[str, F], cases: Iterable[Case]
) -> list[Any]:
    """Every variant x every case, as pytest params with readable ids."""
    cases = list(cases)
    return [
        pytest.param(fn, case, id=f"{name}-{case.name}")
        for name, fn in variants.items()
        for case in cases
    ]
