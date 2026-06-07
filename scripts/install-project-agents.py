#!/usr/bin/env python3
"""Install Promode for Codex project artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import shlex
import shutil
import sys


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
AGENT_SOURCE = PLUGIN_ROOT / "standard" / "agents"
BRIEF_SOURCE = PLUGIN_ROOT / "standard" / "PROMODE_CODEX_MAIN.md"
MAIN_HOOK_SOURCE = PLUGIN_ROOT / "hooks" / "promode-main-context.py"
DRIFT_HOOK_SOURCE = PLUGIN_ROOT / "hooks" / "promode-agent-drift.py"
MAIN_HOOK_COMMAND = 'python3 "$(git rev-parse --show-toplevel)/.codex/hooks/promode-main-context.py"'
DRIFT_HOOK_COMMAND = (
    f"PLUGIN_ROOT={shlex.quote(str(PLUGIN_ROOT))} "
    'python3 "$(git rev-parse --show-toplevel)/.codex/hooks/promode-agent-drift.py"'
)
HOOK_MATCHER = "startup|resume|clear|compact"
PROMODE_HOOK_NAMES = ("promode-main-context.py", "promode-agent-drift.py")
HOOKS = [
    {
        "type": "command",
        "command": MAIN_HOOK_COMMAND,
        "statusMessage": "Loading Promode for Codex",
    },
    {
        "type": "command",
        "command": DRIFT_HOOK_COMMAND,
        "statusMessage": "Checking Promode project agents",
    },
]
HOOK_SOURCES = [MAIN_HOOK_SOURCE, DRIFT_HOOK_SOURCE]


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", default=".", help="Project directory")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument(
        "--agents-only",
        action="store_true",
        help="Install only .codex/agents templates; skip hook and brief",
    )
    return parser.parse_args()


def main() -> int:
    args = parse_args()
    project = Path(args.project).resolve()
    if not project.is_dir():
        print(f"not a directory: {project}", file=sys.stderr)
        return 2

    codex_dir = project / ".codex"
    target = codex_dir / "agents"
    hook_target_dir = codex_dir / "hooks"
    hooks_json = codex_dir / "hooks.json"
    agent_files = sorted(AGENT_SOURCE.glob("promode_*.toml"))
    if not agent_files:
        print(f"no agent templates found in {AGENT_SOURCE}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(f"would create {target}")
        for source in agent_files:
            print(f"would copy {source.name} -> {target / source.name}")
        if not args.agents_only:
            print(f"would copy {BRIEF_SOURCE.name} -> {codex_dir / BRIEF_SOURCE.name}")
            for source in HOOK_SOURCES:
                print(f"would copy {source.name} -> {hook_target_dir / source.name}")
            print(f"would merge SessionStart hook into {hooks_json}")
        return 0

    target.mkdir(parents=True, exist_ok=True)
    for source in agent_files:
        shutil.copy2(source, target / source.name)
        print(f"installed {target / source.name}")

    if not args.agents_only:
        codex_dir.mkdir(parents=True, exist_ok=True)
        hook_target_dir.mkdir(parents=True, exist_ok=True)
        shutil.copy2(BRIEF_SOURCE, codex_dir / BRIEF_SOURCE.name)
        for source in HOOK_SOURCES:
            shutil.copy2(source, hook_target_dir / source.name)
        merge_hooks_json(hooks_json)
        print(f"installed {codex_dir / BRIEF_SOURCE.name}")
        for source in HOOK_SOURCES:
            print(f"installed {hook_target_dir / source.name}")
        print(f"merged SessionStart hook into {hooks_json}")

    return 0


def merge_hooks_json(path: Path) -> None:
    if path.exists():
        try:
            payload = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            raise SystemExit(f"invalid JSON in {path}: {exc}") from exc
        if not isinstance(payload, dict):
            raise SystemExit(f"{path} must contain a JSON object")
    else:
        payload = {}

    hooks = payload.setdefault("hooks", {})
    if not isinstance(hooks, dict):
        raise SystemExit(f"{path} field 'hooks' must be an object")
    session_start = hooks.setdefault("SessionStart", [])
    if not isinstance(session_start, list):
        raise SystemExit(f"{path} field 'hooks.SessionStart' must be a list")

    cleaned_session_start = []
    for group in session_start:
        if not isinstance(group, dict):
            cleaned_session_start.append(group)
            continue
        group_hooks = group.get("hooks", [])
        if not isinstance(group_hooks, list):
            cleaned_session_start.append(group)
            continue
        kept_hooks = [
            hook
            for hook in group_hooks
            if not (
                isinstance(hook, dict)
                and is_promode_hook_command(hook.get("command"))
            )
        ]
        if kept_hooks or len(kept_hooks) == len(group_hooks):
            group = group.copy()
            group["hooks"] = kept_hooks
            cleaned_session_start.append(group)

    cleaned_session_start.append(
        {"matcher": HOOK_MATCHER, "hooks": [hook.copy() for hook in HOOKS]}
    )
    hooks["SessionStart"] = cleaned_session_start

    path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")


def is_promode_hook_command(command: object) -> bool:
    return isinstance(command, str) and any(name in command for name in PROMODE_HOOK_NAMES)


if __name__ == "__main__":
    raise SystemExit(main())
