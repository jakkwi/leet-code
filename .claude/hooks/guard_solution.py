"""PreToolUse hook for Edit/Write: enforces "mentor, not solution generator".

Writing a problem's solution.hpp or solution.py turns into a permission prompt,
so Jakub sees and approves every such edit (for example, setting the shared
signature, or after he wrote "pokaż rozwiązanie").
"""

from __future__ import annotations

import json
import re
import sys

# Matched against the path with backslashes turned into slashes.
SOLUTION_RE = re.compile(r"problems/[^/]+/[^/]+/(cpp/solution\.hpp|python/solution\.py)$")


def main() -> int:
    data = json.load(sys.stdin)
    path = str(data.get("tool_input", {}).get("file_path", "")).replace("\\", "/")
    if not SOLUTION_RE.search(path):
        return 0
    print(
        json.dumps(
            {
                "hookSpecificOutput": {
                    "hookEventName": "PreToolUse",
                    "permissionDecision": "ask",
                    "permissionDecisionReason": (
                        "Solution file: Claude only edits it for infrastructure (signature, "
                        "variants list) or after 'pokaż rozwiązanie'."
                    ),
                }
            }
        )
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
