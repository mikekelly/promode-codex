#!/usr/bin/env python3
"""Inject the Promode for Codex main-agent brief at SessionStart.

Codex command hooks receive a single JSON object on stdin. This hook is bundled
with the plugin, so PLUGIN_ROOT points at the installed plugin copy.
"""

from __future__ import annotations

import json
import os
from pathlib import Path
import sys


VALID_SOURCES = {"startup", "resume", "clear", "compact"}


def main() -> int:
    try:
        payload = json.load(sys.stdin)
    except json.JSONDecodeError:
        return 0

    if payload.get("hook_event_name") != "SessionStart":
        return 0
    if payload.get("source") not in VALID_SOURCES:
        return 0

    root = Path(os.environ.get("PLUGIN_ROOT") or Path(__file__).resolve().parents[1])
    candidates = [
        root / "standard" / "PROMODE_CODEX_MAIN.md",
        root / "PROMODE_CODEX_MAIN.md",
    ]
    brief = next((path for path in candidates if path.is_file()), None)
    if brief is None:
        return 0

    version = plugin_version(root)
    system_message = f"promode-codex{f' v{version}' if version else ''} active in this session"

    output = {
        "systemMessage": system_message,
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": brief.read_text(encoding="utf-8"),
        }
    }
    json.dump(output, sys.stdout)
    return 0


def plugin_version(root: Path) -> str:
    manifest = root / ".codex-plugin" / "plugin.json"
    if not manifest.is_file():
        return ""
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return ""
    version = data.get("version")
    return version if isinstance(version, str) else ""


if __name__ == "__main__":
    raise SystemExit(main())
