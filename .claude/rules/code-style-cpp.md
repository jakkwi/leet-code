---
paths:
  - "**/*.cpp"
  - "**/*.hpp"
---

# C++ style

Formatting is clang-format's job (`.clang-format`, Google based, 4 spaces, 100 columns). clang-tidy config: `.clang-tidy`.

## In code review, check
- Parameters: read-only containers by `const&` (or `std::span<const T>`), cheap types by value, sinks by value + `std::move`.
- `reserve` when the final size is known; no repeated reallocation in loops.
- Container choice and its cost: `vector` (contiguous, cache friendly) by default; `unordered_map` (average O(1), hashing and node allocation cost, iteration order unspecified) vs `map` (O(log n), ordered); `array` for fixed small sizes.
- UB: signed overflow (`a + b` on `int`), out of range indexing, iterator or reference invalidation after `push_back` / `insert` / `erase`, reading uninitialized values, dangling `string_view` / `span`.
- Signed vs unsigned: `size_t` loop indexes vs `int` values; `-Wsign-conversion` is on.
- `[[nodiscard]]` on pure functions, `const` everywhere it fits, no raw `new` / `delete` (lists and trees in tests use `ListArena` / `TreeArena`).
- Prefer `<algorithm>` and ranges when they say the intent more clearly than a loop.

## Conventions
- Namespace `lc::p<NNNN>_<slug>`; variants are free functions named after the idea (`brute_force`, `sort_two_pointers`, `hash_map_one_pass`).
- Every variant is registered in `variants()`; the shared signature is the `Solver` alias.
- Comments explain why, not what. English only.
