---
paths:
  - "problems/**"
  - "common/**"
  - "**/test*.py"
  - "**/test*.cpp"
---

# Testing

- `cases.json` is the single source of test cases for both languages: `{"cases": [{"name", "input", "expected", "note"?}]}`. `input` is an object keyed by parameter name. Case names are unique, snake_case, and say what they test (`negative_numbers`, `duplicates_form_answer`).
- Tests are parameterized: every variant x every case. Adding a variant must not require touching the test file.
- Edge cases to look for: empty and single-element input, duplicates, negatives and zero, extremes of the constraints (`INT_MIN`, `INT_MAX`, overflow in sums), answer at the first / last position, already sorted / reverse sorted input, all equal elements.
- When the answer is not unique or order does not matter, the test normalizes (for example sorts) before comparing, and `note` says so.
- Debug builds run with ASan (plus UBSan on Linux). A sanitizer report is a failing test, never noise.
- `tools/check_isolation.py` validates the `cases.json` shape.
