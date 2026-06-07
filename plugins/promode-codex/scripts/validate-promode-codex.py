#!/usr/bin/env python3
"""Validate Promode for Codex repo assumptions."""

from __future__ import annotations

import argparse
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
AGENT_CONTRACT_PHRASES = {
    "promode_agent_analyzer": [
        "without assuming transcript stability",
        "Do not parse entire large transcript files",
        "not crystallised into deterministic checks",
    ],
    "promode_debugger": [
        "Default to diagnose-and-report",
        "Generate 3-5 ranked, falsifiable hypotheses",
        "Do not debug in slow system tests",
    ],
    "promode_environment_manager": [
        "Orient through AGENTS.md",
        "reliable\narrange/reset/isolation",
        "runbook linked from RUNBOOKS.md",
    ],
    "promode_implementer": [
        "You implement code using TDD",
        "Write or identify one failing behavioral test",
        "Do not revert unrelated edits",
    ],
    "promode_product_designer": [
        "Default stance: skeptical",
        "Report a concrete recommendation",
        "Do not make code changes unless",
    ],
    "promode_reviewer": [
        "Lead with a verdict: APPROVED or REWORK",
        "Tests are missing, superficial",
        "Behavioral authority order",
    ],
    "promode_verifier": [
        "PASS or FAIL",
        "You verify behavior from the outside",
        "Do not fix failures",
    ],
}
READ_ONLY_AGENTS = {
    "promode_agent_analyzer",
    "promode_reviewer",
    "promode_verifier",
}


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--mode",
        choices=("auto", "source", "package"),
        default="auto",
        help=(
            "auto detects source-repo vs installed-plugin layout; source also "
            "requires marketplace/repo policy files; package validates only the "
            "plugin payload and project installer behavior"
        ),
    )
    return parser.parse_args()


def detect_source_repo_root() -> Path | None:
    """Return the marketplace repo root when ROOT is plugins/promode-codex."""
    if ROOT.parent.name != "plugins":
        return None
    candidate = ROOT.parent.parent
    marketplace = candidate / ".agents" / "plugins" / "marketplace.json"
    plugin_root = candidate / "plugins" / "promode-codex"
    if marketplace.is_file() and plugin_root.resolve() == ROOT.resolve():
        return candidate
    return None


def fail(message: str) -> None:
    print(f"FAIL: {message}", file=sys.stderr)
    raise SystemExit(1)


def check_file(path: Path) -> None:
    if not path.is_file():
        try:
            label = path.relative_to(ROOT)
        except ValueError:
            label = path
        fail(f"missing file: {label}")


def plugin_version(root: Path, fallback: str = "test") -> str:
    manifest = root / ".codex-plugin" / "plugin.json"
    if not manifest.is_file():
        return fallback
    try:
        data = json.loads(manifest.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return fallback
    version = data.get("version")
    return version if isinstance(version, str) and version else fallback


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


def validate_marketplace(source_root: Path) -> None:
    path = source_root / ".agents" / "plugins" / "marketplace.json"
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
    if plugin.get("source") != {"source": "local", "path": "./plugins/promode-codex"}:
        fail("marketplace plugin source must point at ./plugins/promode-codex")
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
        stale_brief = project / ".codex" / "PROMODE_CODEX_MAIN.md"
        stale_brief.parent.mkdir()
        stale_brief.write_text("stale project brief\n", encoding="utf-8")
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
            if "Restart or resume Codex" not in proc.stdout:
                fail("installer should advise restarting or resuming Codex")

        hooks_json = project / ".codex" / "hooks.json"
        for path in (
            project / ".codex" / "hooks" / "promode-main-context.py",
            project / ".codex" / "hooks" / "promode-agent-drift.py",
        ):
            if not path.is_file():
                fail(f"installer missing file: {path}")
        if (project / ".codex" / "PROMODE_CODEX_MAIN.md").exists():
            fail("installer should not copy PROMODE_CODEX_MAIN.md into the project")
        commands = [
            hook.get("command")
            for group in json.loads(hooks_json.read_text(encoding="utf-8"))["hooks"][
                "SessionStart"
            ]
            for hook in group.get("hooks", [])
        ]
        expected_main = (
            f"PLUGIN_ROOT={shlex.quote(str(ROOT))} "
            'python3 "$(git rev-parse --show-toplevel)/.codex/hooks/promode-main-context.py"'
        )
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


def validate_repository_policy(source_root: Path) -> None:
    check_file(source_root / "scripts" / "check")
    if not os.access(source_root / "scripts" / "check", os.X_OK):
        fail("scripts/check must be executable")
    check_text = (source_root / "scripts" / "check").read_text(encoding="utf-8")
    if "validate-promode-codex.py --mode source" not in check_text:
        fail("scripts/check must run validate-promode-codex.py --mode source")

    for path in (
        source_root / "docs" / "PROJECT_FRAMING.md",
        source_root / "docs" / "DECISIONS.md",
        source_root / "docs" / "TRACEABILITY.md",
    ):
        check_file(path)

    gitignore = source_root / ".gitignore"
    check_file(gitignore)
    gitignore_text = gitignore.read_text(encoding="utf-8")
    if "/.codex/" not in gitignore_text:
        fail(".gitignore must ignore root /.codex/ generated setup state")
    if "Do not generalize" not in gitignore_text:
        fail(".gitignore must state that root /.codex/ ignore is repo-specific")

    agents_md = source_root / "AGENTS.md"
    check_file(agents_md)
    agents_text = agents_md.read_text(encoding="utf-8")
    for needle in (
        "scripts/check",
        "docs/PROJECT_FRAMING.md",
        "docs/DECISIONS.md",
        "docs/TRACEABILITY.md",
        "Do not generalize that to user projects",
    ):
        if needle not in agents_text:
            fail(f"AGENTS.md missing guidance: {needle}")


def validate_no_stale_setup_artifacts(source_root: Path) -> None:
    stale_paths = (
        source_root / ".codex" / "PROMODE_CODEX_MAIN.md",
        source_root / ".claude" / "PROMODE_MAIN_AGENT.md",
        source_root / ".claude" / "hooks" / "promode-main-context.sh",
    )
    for path in stale_paths:
        if path.exists():
            fail(f"stale setup artifact should be absent: {path}")

    claude_settings = source_root / ".claude" / "settings.json"
    if claude_settings.is_file():
        try:
            text = claude_settings.read_text(encoding="utf-8").lower()
        except OSError as exc:
            fail(f"could not read {claude_settings}: {exc}")
        if "promode" in text:
            fail(".claude/settings.json must not contain Promode hook entries")


def validate_installed_cache_layout() -> None:
    """The installed plugin payload has no marketplace repo wrapper."""
    with tempfile.TemporaryDirectory(prefix="promode-codex-cache-layout-") as tmp:
        cache_root = (
            Path(tmp)
            / "promode-codex"
            / "promode-codex"
            / plugin_version(ROOT, fallback="test")
        )
        shutil.copytree(
            ROOT,
            cache_root,
            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"),
        )
        proc = subprocess.run(
            [sys.executable, str(cache_root / "scripts" / "validate-promode-codex.py")],
            text=True,
            capture_output=True,
            check=False,
        )
        if proc.returncode != 0:
            fail(
                "installed cache layout validation failed: "
                f"stdout={proc.stdout!r} stderr={proc.stderr!r}"
            )


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
        name = data["name"]
        seen.add(name)
        if name in READ_ONLY_AGENTS and data.get("sandbox_mode") != "read-only":
            fail(f"{path.name} must be read-only")
        instructions = data["developer_instructions"]
        for phrase in AGENT_CONTRACT_PHRASES.get(name, []):
            if phrase not in instructions:
                fail(f"{path.name} missing contract phrase: {phrase}")
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


def validate_package() -> None:
    validate_manifest()
    validate_hook()
    validate_installer()
    validate_agents()
    validate_skills()


def validate_source(source_root: Path) -> None:
    validate_marketplace(source_root)
    validate_repository_policy(source_root)
    validate_no_stale_setup_artifacts(source_root)
    validate_installed_cache_layout()


def main() -> int:
    args = parse_args()
    source_root = detect_source_repo_root()

    if args.mode == "source" and source_root is None:
        fail(
            "source validation requires the marketplace repo layout "
            "`<repo>/.agents/plugins/marketplace.json` plus "
            "`<repo>/plugins/promode-codex/`"
        )

    validate_package()
    if args.mode == "source" or (args.mode == "auto" and source_root is not None):
        assert source_root is not None
        validate_source(source_root)

    print("PASS: promode-codex assumptions validated")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
