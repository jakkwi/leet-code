---
paths:
  - "problems/**"
  - "common/**"
  - "**/test*.py"
---

# Testing

- `cases.json` holds the test cases: `{"cases": [{"name", "input", "expected", "note"?}]}`. `input` is an object keyed by parameter name. Case names are unique, snake_case, and say what they test (`negative_numbers`, `duplicates_form_answer`).
- Tests are parameterized: every variant x every case. Adding a variant to `VARIANTS` must not require touching the test file.
- Edge cases to look for: empty and single-element input, duplicates, negatives and zero, extremes of the constraints, answer at the first / last position, already sorted / reverse sorted input, all equal elements, large input for the time limit.
- When the answer is not unique or order does not matter, the test normalizes (for example sorts) before comparing, and `note` says so.
- `tools/check_isolation.py` validates the `cases.json` shape.
