#!/usr/bin/env python3
"""Sync Promode for Codex project agents and doctrine artifacts."""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import re
import shutil
import subprocess
import sys
import urllib.error
import urllib.request


PLUGIN_ROOT = Path(__file__).resolve().parents[1]
AGENT_SOURCE = PLUGIN_ROOT / "standard" / "agents"
DOC_SOURCE = PLUGIN_ROOT / "standard" / "docs"
UPSTREAM_GIT_URL = "https://github.com/mikekelly/promode-codex.git"
UPSTREAM_MANIFEST_URL = (
    "https://raw.githubusercontent.com/mikekelly/promode-codex/main/"
    "plugins/promode-codex/.codex-plugin/plugin.json"
)
UPGRADE_CHECK_TIMEOUT_SECONDS = 5
SEMVER_RE = re.compile(r"^v?(\d+)\.(\d+)\.(\d+)$")
PROMODE_HOOK_NAMES = ("promode-main-context.py", "promode-agent-drift.py")
STALE_PROJECT_PATHS = (
    Path(".codex") / "PROMODE_CODEX_MAIN.md",
    Path(".codex") / "hooks" / "promode-main-context.py",
    Path(".codex") / "hooks" / "promode-agent-drift.py",
)
SESSION_REFRESH_MESSAGE = (
    "Restart or resume Codex in this project so newly installed Promode "
    "custom-agent roles and project-local doctrine are discovered. Run "
    "`$promode-codex:activate` at the start of each session to load the Promode "
    "main-agent brief."
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("project", nargs="?", default=".", help="Project directory")
    parser.add_argument("--dry-run", action="store_true", help="Show changes without writing")
    parser.add_argument(
        "--agents-only",
        action="store_true",
        help="Deprecated compatibility flag; sync now installs all Promode project files",
    )
    parser.add_argument(
        "--skip-upgrade-check",
        action="store_true",
        help="Skip the best-effort GitHub check for a newer Promode plugin version",
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
    docs_target = codex_dir / "promode" / "docs"
    hooks_json = codex_dir / "hooks.json"
    agent_files = sorted(AGENT_SOURCE.glob("promode_*.toml"))
    if not agent_files:
        print(f"no agent templates found in {AGENT_SOURCE}", file=sys.stderr)
        return 2
    doctrine_files = doctrine_source_files()
    if not doctrine_files:
        print(f"no doctrine docs found in {DOC_SOURCE}", file=sys.stderr)
        return 2

    if args.dry_run:
        print(f"would create {target}")
        for source in agent_files:
            print(f"would copy {source.name} -> {target / source.name}")
        print(f"would create {docs_target}")
        for source in doctrine_files:
            relative = source.relative_to(DOC_SOURCE)
            print(f"would copy {relative} -> {docs_target / relative}")
        for stale in stale_doctrine_files(docs_target, doctrine_files):
            print(f"would remove stale {stale}")
        for relative in STALE_PROJECT_PATHS:
            stale = project / relative
            if stale.exists():
                print(f"would remove stale {stale}")
        if hooks_json.exists():
            print(f"would remove legacy Promode hook entries from {hooks_json}")
        return 0

    target.mkdir(parents=True, exist_ok=True)
    for source in agent_files:
        shutil.copy2(source, target / source.name)
        print(f"installed {target / source.name}")

    sync_doctrine_docs(docs_target, doctrine_files)
    cleanup_legacy_promode_hooks(project)

    print(SESSION_REFRESH_MESSAGE)
    if not args.skip_upgrade_check:
        warn_if_upgrade_available()
    return 0


def cleanup_legacy_promode_hooks(project: Path) -> None:
    for relative in STALE_PROJECT_PATHS:
        stale = project / relative
        if stale.exists():
            stale.unlink()
            print(f"removed stale {stale}")

    hooks_json = project / ".codex" / "hooks.json"
    if remove_promode_hook_entries(hooks_json):
        print(f"removed legacy Promode hook entries from {hooks_json}")


def remove_promode_hook_entries(path: Path) -> bool:
    if not path.exists():
        return False

    try:
        payload = json.loads(path.read_text(encoding="utf-8"))
    except json.JSONDecodeError as exc:
        raise SystemExit(f"invalid JSON in {path}: {exc}") from exc
    if not isinstance(payload, dict):
        raise SystemExit(f"{path} must contain a JSON object")

    hooks = payload.get("hooks")
    if not isinstance(hooks, dict):
        return False

    changed = False
    for event_name in list(hooks):
        groups = hooks[event_name]
        if not isinstance(groups, list):
            continue

        cleaned_groups = []
        for group in groups:
            if not isinstance(group, dict):
                cleaned_groups.append(group)
                continue
            group_hooks = group.get("hooks")
            if not isinstance(group_hooks, list):
                cleaned_groups.append(group)
                continue

            kept_hooks = [
                hook
                for hook in group_hooks
                if not (
                    isinstance(hook, dict)
                    and is_promode_hook_command(hook.get("command"))
                )
            ]
            if len(kept_hooks) != len(group_hooks):
                changed = True
            if kept_hooks:
                group = group.copy()
                group["hooks"] = kept_hooks
                cleaned_groups.append(group)

        if cleaned_groups:
            hooks[event_name] = cleaned_groups
        else:
            del hooks[event_name]
            changed = True

    if changed:
        path.write_text(json.dumps(payload, indent=2) + "\n", encoding="utf-8")
    return changed


def is_promode_hook_command(command: object) -> bool:
    return isinstance(command, str) and any(name in command for name in PROMODE_HOOK_NAMES)


def doctrine_source_files() -> list[Path]:
    if not DOC_SOURCE.is_dir():
        return []
    return sorted(path for path in DOC_SOURCE.rglob("*") if path.is_file())


def sync_doctrine_docs(target: Path, source_files: list[Path]) -> None:
    target.mkdir(parents=True, exist_ok=True)
    for source in source_files:
        relative = source.relative_to(DOC_SOURCE)
        destination = target / relative
        destination.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, destination)
        print(f"installed {destination}")

    for stale in stale_doctrine_files(target, source_files):
        stale.unlink()
        print(f"removed stale {stale}")
    prune_empty_dirs(target)


def stale_doctrine_files(target: Path, source_files: list[Path]) -> list[Path]:
    if not target.is_dir():
        return []
    expected = {source.relative_to(DOC_SOURCE) for source in source_files}
    return sorted(
        (
            path
            for path in target.rglob("*")
            if path.is_file() and path.relative_to(target) not in expected
        ),
        reverse=True,
    )


def prune_empty_dirs(root: Path) -> None:
    if not root.is_dir():
        return
    for path in sorted((path for path in root.rglob("*") if path.is_dir()), reverse=True):
        try:
            path.rmdir()
        except OSError:
            pass


def warn_if_upgrade_available() -> None:
    try:
        current = current_plugin_version()
        latest = latest_available_version()
    except Exception:
        return
    if current is None or latest is None or not is_newer_version(latest, current):
        return

    print(
        f"WARNING: Promode for Codex {latest} is available; "
        f"this plugin copy is {current}."
    )
    print(
        "Run `codex plugin marketplace upgrade promode-codex` "
        "(or omit the name to upgrade all marketplaces), then restart or resume Codex."
    )


def current_plugin_version() -> str | None:
    manifest = PLUGIN_ROOT / ".codex-plugin" / "plugin.json"
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None

    version = data.get("version")
    return version if isinstance(version, str) and parse_semver(version) else None


def latest_available_version(timeout: int = UPGRADE_CHECK_TIMEOUT_SECONDS) -> str | None:
    versions = []
    tag_version = latest_remote_tag_version(timeout=timeout)
    manifest_version = latest_manifest_version(timeout=timeout)
    for version in (tag_version, manifest_version):
        if version is not None:
            versions.append(version)
    if not versions:
        return None
    return max(versions, key=lambda version: parse_semver(version) or (0, 0, 0))


def latest_remote_tag_version(timeout: int = UPGRADE_CHECK_TIMEOUT_SECONDS) -> str | None:
    try:
        proc = subprocess.run(
            ["git", "ls-remote", "--tags", UPSTREAM_GIT_URL],
            text=True,
            capture_output=True,
            check=False,
            timeout=timeout,
        )
    except (OSError, subprocess.SubprocessError):
        return None
    if proc.returncode != 0:
        return None
    return latest_version_from_ls_remote(proc.stdout)


def latest_manifest_version(timeout: int = UPGRADE_CHECK_TIMEOUT_SECONDS) -> str | None:
    try:
        with urllib.request.urlopen(UPSTREAM_MANIFEST_URL, timeout=timeout) as response:
            text = response.read().decode("utf-8")
    except (OSError, TimeoutError, UnicodeDecodeError, urllib.error.URLError):
        return None

    try:
        data = json.loads(text)
    except json.JSONDecodeError:
        return None
    version = data.get("version")
    return version if isinstance(version, str) and parse_semver(version) else None


def latest_version_from_ls_remote(output: str) -> str | None:
    versions = []
    for line in output.splitlines():
        fields = line.split()
        if len(fields) != 2:
            continue
        ref = fields[1]
        if ref.endswith("^{}"):
            continue
        if not ref.startswith("refs/tags/"):
            continue
        version = ref.removeprefix("refs/tags/")
        parsed = parse_semver(version)
        if parsed is not None:
            versions.append(normalize_semver(version))
    if not versions:
        return None
    return max(versions, key=lambda version: parse_semver(version) or (0, 0, 0))


def is_newer_version(candidate: str, current: str) -> bool:
    candidate_semver = parse_semver(candidate)
    current_semver = parse_semver(current)
    if candidate_semver is None or current_semver is None:
        return False
    return candidate_semver > current_semver


def normalize_semver(version: str) -> str:
    parsed = parse_semver(version)
    if parsed is None:
        return version
    return ".".join(str(part) for part in parsed)


def parse_semver(version: str) -> tuple[int, int, int] | None:
    match = SEMVER_RE.fullmatch(version.strip())
    if not match:
        return None
    return tuple(int(part) for part in match.groups())


if __name__ == "__main__":
    raise SystemExit(main())
