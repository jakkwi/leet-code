# Git

- Conventional Commits: `feat(0001_two_sum): add hash map variant`, `test(0001_two_sum): add edge cases`, `docs: ...`, `build: ...`, `ci: ...`, `chore: ...`. Imperative, English, subject under 72 characters.
- Commit only when Jakub asks. Commits are GPG signed; never skip signing or hooks.
- Author is Jakub Kwiatkowski only. No Co-Authored-By trailers, no mention of Claude or AI in commits, PRs, code or docs.
- Never force push, never rewrite pushed history.
- Before a commit: pytest, ruff, mypy (`tools/run_mypy.py`), `tools/check_isolation.py` all green.
