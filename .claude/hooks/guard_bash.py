"""PreToolUse hook for Bash and PowerShell: blocks unsafe commands and AI attribution.

Exit code 2 blocks the call and sends stderr back to the agent.
Standard library only, runs on Windows, Linux and macOS.
"""

from __future__ import annotations

import json
import re
import sys

BLOCKED: list[tuple[str, str]] = [
    # destructive
    (
        r"\brm\s+-[a-zA-Z]*r[a-zA-Z]*f|\brm\s+-[a-zA-Z]*f[a-zA-Z]*r",
        "Recursive force delete is blocked. Delete specific files instead.",
    ),
    (
        r"Remove-Item\b.*-Recurse\b.*-Force|Remove-Item\b.*-Force\b.*-Recurse",
        "Recursive force delete is blocked.",
    ),
    (r"\b(rd|rmdir)\s+/s\b", "Recursive directory delete is blocked."),
    (r"\bgit\s+push\b.*(--force\b|--force-with-lease\b|\s-f\b)", "Force push is blocked."),
    (r"\bgit\s+reset\s+--hard\b", "git reset --hard is blocked. Ask the user first."),
    (r"\bgit\s+clean\s+-[a-zA-Z]*f", "git clean -f is blocked. Ask the user first."),
    (r"\bgit\s+(rebase|commit\s+--amend|filter-branch)\b", "Rewriting history is blocked."),
    (
        r"--no-verify\b|--no-gpg-sign\b|commit\.gpgsign=false",
        "Skipping hooks or signing is blocked. Fix what failed instead.",
    ),
    # remote code execution / supply chain
    (
        r"\b(curl|wget|iwr|irm|Invoke-WebRequest|Invoke-RestMethod)\b[^|]*\|\s*"
        r"(sh|bash|zsh|python3?|pwsh|powershell|iex)\b",
        "Piping downloaded content into a shell is blocked.",
    ),
    (r"\b(iex|Invoke-Expression)\b", "Invoke-Expression is blocked."),
    (
        r"--index-url|--extra-index-url|--default-index|\s--index[= ]|--registry[= ]",
        "Custom package indexes or registries are blocked.",
    ),
    # secrets
    (
        r"(cat|type|Get-Content|gc|less|more|head|tail|bat)\s+[^|;&]*\.env(?![\w.]*example)\b",
        "Reading .env files is blocked.",
    ),
    (
        r"(cat|type|Get-Content|gc|less|more|head|tail)\s+[^|;&]*"
        r"(id_rsa|id_ed25519|\.pem\b|\.key\b|credentials|\.gnupg|secring)",
        "Reading key or credential files is blocked.",
    ),
    (
        r"\$env:[A-Z_]*(KEY|TOKEN|SECRET|PASSWORD)|echo\s+\$\{?[A-Z_]*(KEY|TOKEN|SECRET|PASSWORD)",
        "Printing secrets from the environment is blocked.",
    ),
    # attribution
    (r"Co-Authored-By", "Do not add Co-Authored-By trailers or any AI attribution."),
    (r"Generated with \[?Claude", "Do not add AI attribution to commits or PRs."),
]


def check(cmd: str) -> str | None:
    for pattern, msg in BLOCKED:
        if re.search(pattern, cmd, re.IGNORECASE):
            return msg
    return None


def main() -> int:
    data = json.load(sys.stdin)
    cmd = data.get("tool_input", {}).get("command", "")
    if not isinstance(cmd, str):
        cmd = " ".join(map(str, cmd))
    msg = check(cmd)
    if msg:
        print(msg, file=sys.stderr)
        return 2
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
