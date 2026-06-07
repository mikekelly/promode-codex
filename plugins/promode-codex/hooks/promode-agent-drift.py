#!/usr/bin/env python3
"""Warn when project-installed Promode agents drift from the plugin copy."""

from __future__ import annotations

from hashlib import sha256
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

    plugin_root = Path(os.environ.get("PLUGIN_ROOT") or Path(__file__).resolve().parents[1])
    warning = project_agent_drift_warning(plugin_root, payload.get("cwd"))
    if not warning:
        return 0

    output = {
        "systemMessage": "promode-codex project Promode agents need update",
        "hookSpecificOutput": {
            "hookEventName": "SessionStart",
            "additionalContext": warning,
        },
    }
    json.dump(output, sys.stdout)
    return 0


def project_agent_drift_warning(plugin_root: Path, cwd_value: object) -> str:
    standard = agent_shas(plugin_root / "standard" / "agents")
    if not standard:
        return ""

    project_root = find_project_root(cwd_value)
    codex_dir = project_root / ".codex"
    project = agent_shas(codex_dir / "agents")

    if not project and not has_project_promode_artifact(codex_dir):
        return ""

    missing = sorted(set(standard) - set(project))
    extra = sorted(set(project) - set(standard))
    changed = sorted(
        name
        for name in set(standard) & set(project)
        if standard[name] != project[name]
    )
    if not missing and not extra and not changed:
        return ""

    lines = [
        "Promode Codex project-agent drift detected.",
        "Project `.codex/agents/promode_*.toml` does not match this Promode plugin version.",
    ]
    if missing:
        lines.append(f"Missing: {', '.join(missing)}.")
    if changed:
        lines.append(f"Changed: {', '.join(changed)}.")
    if extra:
        lines.append(f"Extra: {', '.join(extra)}.")
    lines.append(
        "Before relying on delegated Promode agents, run the "
        "`managing-promode-codex` update workflow."
    )
    return "\n".join(lines)


def agent_shas(directory: Path) -> dict[str, str]:
    if not directory.is_dir():
        return {}
    return {
        path.name: sha_file(path)
        for path in sorted(directory.glob("promode_*.toml"))
        if path.is_file()
    }


def sha_file(path: Path) -> str:
    digest = sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def find_project_root(cwd_value: object) -> Path:
    cwd = Path(cwd_value) if isinstance(cwd_value, str) and cwd_value else Path.cwd()
    try:
        current = cwd.resolve()
    except OSError:
        current = cwd.absolute()
    if current.is_file():
        current = current.parent
    for candidate in (current, *current.parents):
        if (candidate / ".git").exists():
            return candidate
    return current


def has_project_promode_artifact(codex_dir: Path) -> bool:
    project_agents = codex_dir / "agents"
    if project_agents.is_dir() and any(project_agents.glob("promode_*.toml")):
        return True
    if any(
        path.exists()
        for path in (
            codex_dir / "PROMODE_CODEX_MAIN.md",
            codex_dir / "hooks" / "promode-main-context.py",
            codex_dir / "hooks" / "promode-agent-drift.py",
        )
    ):
        return True
    return hooks_json_mentions_promode(codex_dir / "hooks.json")


def hooks_json_mentions_promode(path: Path) -> bool:
    if not path.is_file():
        return False
    try:
        return "promode" in path.read_text(encoding="utf-8").lower()
    except OSError:
        return False


if __name__ == "__main__":
    raise SystemExit(main())
