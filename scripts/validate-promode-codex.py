#!/usr/bin/env python3
"""Validate Promode for Codex repo assumptions."""

from __future__ import annotations

import json
import os
from pathlib import Path
import shutil
import shlex
import subprocess
import sys
import tempfile
import tomllib


ROOT = Path(__file__).resolve().parents[1]
AGENTS = {
    "promode_implementer",
    "promode_reviewer",
    "promode_debugger",
    "promode_verifier",
    "promode_environment_manager",
    "promode_product_designer",
    "promode_agent_analyzer",
}


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_file(path: Path) -> None:
    if not path.is_file():
        fail(f"missing file: {path.relative_to(ROOT)}")


def validate_manifest() -> None:
    path = ROOT / ".codex-plugin" / "plugin.json"
    check_file(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("name") != "promode-codex":
        fail("plugin name must be promode-codex")
    description = data.get("description", "")
    if not isinstance(description, str) or "Codex" not in description:
        fail("plugin description must be Codex-specific")
    if "Claude Code" in description:
        fail("plugin description must not mention Claude Code")
    if data.get("skills") != "./skills/":
        fail("plugin manifest must point skills to ./skills/")
    if "hooks" in data:
        fail("hooks field is intentionally omitted; Codex discovers hooks/hooks.json by default")


def validate_marketplace() -> None:
    path = ROOT / ".agents" / "plugins" / "marketplace.json"
    check_file(path)
    data = json.loads(path.read_text(encoding="utf-8"))
    if data.get("name") != "promode-codex":
        fail("marketplace name must be promode-codex")
    interface = data.get("interface")
    if not isinstance(interface, dict):
        fail("marketplace interface must be an object")
    if interface.get("displayName") != "Promode for Codex":
        fail("marketplace displayName must be Promode for Codex")
    plugins = data.get("plugins")
    if not isinstance(plugins, list) or len(plugins) != 1:
        fail("marketplace must contain exactly one plugin entry")
    plugin = plugins[0]
    if plugin.get("name") != "promode-codex":
        fail("marketplace plugin name must be promode-codex")
    if plugin.get("source") != {"source": "local", "path": "./"}:
        fail("marketplace plugin source must point at the repository root")
    if plugin.get("policy") != {
        "installation": "AVAILABLE",
        "authentication": "ON_INSTALL",
    }:
        fail("marketplace plugin policy is invalid")
    if plugin.get("category") != "Productivity":
        fail("marketplace plugin category must be Productivity")


def validate_hook() -> None:
    hooks_json = ROOT / "hooks" / "hooks.json"
    main_script = ROOT / "hooks" / "promode-main-context.py"
    drift_script = ROOT / "hooks" / "promode-agent-drift.py"
    check_file(hooks_json)
    check_file(main_script)
    check_file(drift_script)
    hook_config = json.loads(hooks_json.read_text(encoding="utf-8"))
    commands = {
        hook.get("command")
        for group in hook_config.get("hooks", {}).get("SessionStart", [])
        if isinstance(group, dict)
        for hook in group.get("hooks", [])
        if isinstance(hook, dict)
    }
    for command in (
        "python3 ${PLUGIN_ROOT}/hooks/promode-main-context.py",
        "python3 ${PLUGIN_ROOT}/hooks/promode-agent-drift.py",
    ):
        if command not in commands:
            fail(f"hooks.json missing command: {command}")

    sample = {
        "hook_event_name": "SessionStart",
        "source": "startup",
        "cwd": str(ROOT),
        "session_id": "test",
        "transcript_path": None,
        "model": "gpt-test",
        "permission_mode": "default",
    }
    proc = run_hook(main_script, sample)
    if not proc.stdout:
        fail("main hook produced no output")
    output = json.loads(proc.stdout)
    if "active in this session" not in output.get("systemMessage", ""):
        fail("main hook systemMessage should confirm Promode is active in this session")
    hook_output = output.get("hookSpecificOutput", {})
    if hook_output.get("hookEventName") != "SessionStart":
        fail("main hook output missing SessionStart hookEventName")
    context = hook_output.get("additionalContext", "")
    if "Promode for Codex" not in context:
        fail("main hook context does not include Promode for Codex brief")

    proc = run_hook(drift_script, sample)
    if proc.stdout.strip():
        fail("drift hook should be quiet when the repo has no project Promode artifacts")
    validate_drift_hook_clean_project(drift_script)
    validate_drift_hook_warning(drift_script)

    sample_project = ROOT / ".codex"
    project_main_hook = sample_project / "hooks" / "promode-main-context.py"
    project_drift_hook = sample_project / "hooks" / "promode-agent-drift.py"
    project_brief = sample_project / "PROMODE_CODEX_MAIN.md"
    if project_main_hook.exists() or project_drift_hook.exists() or project_brief.exists():
        fail("repo root must not contain installed project hook artifacts")


def validate_installer() -> None:
    with tempfile.TemporaryDirectory(prefix="promode-codex-install-") as tmp:
        project = Path(tmp)
        (project / ".git").mkdir()
        installer = ROOT / "scripts" / "install-project-agents.py"
        for _ in range(2):
            proc = subprocess.run(
                [sys.executable, str(installer), str(project)],
                text=True,
                capture_output=True,
                check=False,
            )
            if proc.returncode != 0:
                fail(f"installer exited {proc.returncode}: {proc.stderr}")

        hooks_json = project / ".codex" / "hooks.json"
        for path in (
            project / ".codex" / "PROMODE_CODEX_MAIN.md",
            project / ".codex" / "hooks" / "promode-main-context.py",
            project / ".codex" / "hooks" / "promode-agent-drift.py",
        ):
            if not path.is_file():
                fail(f"installer missing file: {path}")
        commands = [
            hook.get("command")
            for group in json.loads(hooks_json.read_text(encoding="utf-8"))["hooks"][
                "SessionStart"
            ]
            for hook in group.get("hooks", [])
        ]
        expected_main = 'python3 "$(git rev-parse --show-toplevel)/.codex/hooks/promode-main-context.py"'
        expected_drift = (
            f"PLUGIN_ROOT={shlex.quote(str(ROOT))} "
            'python3 "$(git rev-parse --show-toplevel)/.codex/hooks/promode-agent-drift.py"'
        )
        if commands.count(expected_main) != 1:
            fail("installer should write exactly one project main-context hook command")
        if commands.count(expected_drift) != 1:
            fail("installer should write exactly one project agent-drift hook command")
        if len(commands) != len(set(commands)):
            fail("installer should not duplicate hook commands on repeat runs")

        proc = run_hook(
            project / ".codex" / "hooks" / "promode-agent-drift.py",
            hook_sample(project),
        )
        if proc.stdout.strip():
            fail("installed project drift hook should be quiet for matching agents")


def run_hook(script: Path, sample: dict[str, object]) -> subprocess.CompletedProcess[str]:
    env = os.environ.copy()
    env["PLUGIN_ROOT"] = str(ROOT)
    proc = subprocess.run(
        [sys.executable, str(script)],
        input=json.dumps(sample),
        text=True,
        capture_output=True,
        env=env,
        check=False,
    )
    if proc.returncode != 0:
        try:
            script_label = script.relative_to(ROOT)
        except ValueError:
            script_label = script
        fail(f"{script_label} exited {proc.returncode}: {proc.stderr}")
    return proc


def hook_sample(cwd: Path) -> dict[str, object]:
    return {
        "hook_event_name": "SessionStart",
        "source": "startup",
        "cwd": str(cwd),
        "session_id": "test",
        "transcript_path": None,
        "model": "gpt-test",
        "permission_mode": "default",
    }


def copy_standard_agents(target: Path) -> list[Path]:
    target.mkdir(parents=True, exist_ok=True)
    sources = sorted((ROOT / "standard" / "agents").glob("promode_*.toml"))
    for source in sources:
        shutil.copy2(source, target / source.name)
    return sources


def validate_drift_hook_clean_project(script: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="promode-codex-clean-") as tmp:
        project = Path(tmp)
        (project / ".git").mkdir()
        copy_standard_agents(project / ".codex" / "agents")
        proc = run_hook(script, hook_sample(project))
        if proc.stdout.strip():
            fail("drift hook should be quiet when project agents match plugin agents")


def validate_drift_hook_warning(script: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="promode-codex-drift-") as tmp:
        project = Path(tmp)
        (project / ".git").mkdir()
        agents_dir = project / ".codex" / "agents"
        sources = copy_standard_agents(agents_dir)
        if len(sources) < 2:
            fail("drift validation needs at least two standard agent templates")

        missing_name = sources[0].name
        changed_name = sources[1].name
        (agents_dir / missing_name).unlink()
        with (agents_dir / changed_name).open("a", encoding="utf-8") as handle:
            handle.write("\n# drift validation edit\n")
        (agents_dir / "promode_removed.toml").write_text(
            "name = \"promode_removed\"\n",
            encoding="utf-8",
        )

        proc = run_hook(script, hook_sample(project))
        if not proc.stdout.strip():
            fail("drift hook should warn when project agents differ")
        output = json.loads(proc.stdout)
        if "project Promode agents need update" not in output.get("systemMessage", ""):
            fail("drift hook systemMessage should flag project agent drift")
        hook_output = output.get("hookSpecificOutput", {})
        if hook_output.get("hookEventName") != "SessionStart":
            fail("drift hook output missing SessionStart hookEventName")
        context = hook_output.get("additionalContext", "")
        for needle in (
            "Promode Codex project-agent drift detected.",
            f"Missing: {missing_name}.",
            f"Changed: {changed_name}.",
            "Extra: promode_removed.toml.",
            "`managing-promode-codex` update workflow",
        ):
            if needle not in context:
                fail(f"drift hook warning missing text: {needle}")


def validate_agents() -> None:
    root = ROOT / "standard" / "agents"
    check_file(root / "promode_implementer.toml")
    seen = set()
    for path in sorted(root.glob("promode_*.toml")):
        data = tomllib.loads(path.read_text(encoding="utf-8"))
        for key in ("name", "description", "developer_instructions"):
            if not data.get(key):
                fail(f"{path.name} missing {key}")
        seen.add(data["name"])
    missing = AGENTS - seen
    extra = seen - AGENTS
    if missing:
        fail(f"missing standard agents: {sorted(missing)}")
    if extra:
        fail(f"unexpected standard agents: {sorted(extra)}")


def validate_skills() -> None:
    skills_root = ROOT / "skills"
    for skill in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        skill_md = skill / "SKILL.md"
        check_file(skill_md)
        text = skill_md.read_text(encoding="utf-8")
        if not text.startswith("---\n"):
            fail(f"{skill.name} SKILL.md missing YAML frontmatter")
        frontmatter_end = text.find("\n---", 4)
        if frontmatter_end == -1:
            fail(f"{skill.name} SKILL.md frontmatter not closed")
        frontmatter = text[4:frontmatter_end]
        if "name:" not in frontmatter or "description:" not in frontmatter:
            fail(f"{skill.name} SKILL.md needs name and description")


def main() -> int:
    validate_manifest()
    validate_marketplace()
    validate_hook()
    validate_installer()
    validate_agents()
    validate_skills()
    print("PASS: promode-codex assumptions validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
