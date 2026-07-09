#!/usr/bin/env python3
"""Validate Promode for Codex repo assumptions."""

from __future__ import annotations

import argparse
import importlib.util
import json
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile
import tomllib


ROOT = Path(__file__).resolve().parents[1]
AGENTS = {
    "promode_agent_analyzer",
    "promode_auditor",
    "promode_chief_technology_officer",
    "promode_code_reviewer",
    "promode_constraint_reinforcer",
    "promode_debugger",
    "promode_environment_manager",
    "promode_fast_worker",
    "promode_product_design_expert",
    "promode_senior_engineer",
    "promode_verifier",
}
AGENT_CONTRACT_PHRASES = {
    "promode_agent_analyzer": [
        "without assuming transcript stability",
        "Do not parse entire large transcript files",
        "Recovery process",
        "not crystallised into deterministic checks",
    ],
    "promode_auditor": [
        "Promode methodology audits for Codex",
        "Setup pre-flight",
        "Prioritised action plan",
    ],
    "promode_chief_technology_officer": [
        "hard-to-reverse architecture",
        "GPT-5.6 Sol",
        "high reasoning",
        "do not make code changes",
        "Delegation-ready task breakdown",
    ],
    "promode_code_reviewer": [
        "Lead with a verdict: APPROVED or REWORK",
        "Failing-test-first evidence",
        "Behavioral authority order",
    ],
    "promode_constraint_reinforcer": [
        "A crucial constraint",
        "A plain link alone does not carry a critical rule",
        "Do not put Promode methodology itself into AGENTS.md",
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
    "promode_fast_worker": [
        "the mechanical execution tier",
        "Know your lane",
        "selector-based actions, never hardcoded coordinates",
    ],
    "promode_product_design_expert": [
        "Default stance: skeptical",
        "Report a concrete recommendation",
        "Do not make code changes unless",
    ],
    "promode_senior_engineer": [
        "the deep-reasoning implementation tier",
        "Write or identify one failing behavioral test",
        "Do not revert unrelated edits",
    ],
    "promode_verifier": [
        "PASS or FAIL",
        "You verify behavior from the outside",
        "Do not fix failures",
    ],
}
EXPECTED_AGENT_MODELS = {
    "promode_agent_analyzer": "gpt-5.5",
    "promode_auditor": "gpt-5.5",
    "promode_chief_technology_officer": "gpt-5.6-sol",
    "promode_code_reviewer": "gpt-5.5",
    "promode_constraint_reinforcer": "gpt-5.5",
    "promode_debugger": "gpt-5.5",
    "promode_environment_manager": "gpt-5.5",
    "promode_fast_worker": "gpt-5.4-mini",
    "promode_product_design_expert": "gpt-5.5",
    "promode_senior_engineer": "gpt-5.5",
    "promode_verifier": "gpt-5.5",
}
EXPECTED_AGENT_REASONING_EFFORT = {
    "promode_chief_technology_officer": "high",
}
READ_ONLY_AGENTS = {
    "promode_agent_analyzer",
    "promode_auditor",
    "promode_chief_technology_officer",
    "promode_code_reviewer",
    "promode_verifier",
}
REQUIRED_SKILLS = {
    "activate",
    "sync",
    "promode-audit",
    "handoff",
}
FORBIDDEN_EXPOSED_SKILLS = {
    "managing-promode-codex",
    "recovering-subagents",
    "discovery-to-determinism",
}
PROMODE_HOOK_NAMES = ("promode-main-context.py", "promode-agent-drift.py")
DOCTRINE_DOCS = {
    "agent-knowledge-wiki.md",
    "codex-assumptions.md",
    "discovery-to-determinism.md",
    "index.md",
    "main-agent-delivery.md",
    "opinion-register.md",
    "operator-seam-and-agent-tools.md",
    "ui-state-graph-edt.md",
}
DOCTRINE_REGISTER_RELATIVE = Path(".codex") / "promode" / "docs" / "opinion-register.md"
COMMON_AGENT_CONTRACT_PHRASES = (
    ".codex/promode/docs/opinion-register.md",
    "git rev-parse --show-toplevel",
    "$promode-codex:sync",
)


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
        fail("hooks field must be omitted; Promode Codex uses explicit activation")
    for stale in (
        ROOT / "hooks" / "hooks.json",
        ROOT / "hooks" / "promode-main-context.py",
        ROOT / "hooks" / "promode-agent-drift.py",
    ):
        if stale.exists():
            fail(f"plugin must not ship legacy hook artifact: {stale.relative_to(ROOT)}")


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


def validate_activation_flow() -> None:
    activate = ROOT / "skills" / "activate" / "SKILL.md"
    activate_metadata = ROOT / "skills" / "activate" / "agents" / "openai.yaml"
    sync = ROOT / "skills" / "sync" / "SKILL.md"
    sync_metadata = ROOT / "skills" / "sync" / "agents" / "openai.yaml"
    check_file(activate)
    check_file(activate_metadata)
    check_file(sync)
    check_file(sync_metadata)
    if (ROOT / "standard" / "PROMODE_CODEX_MAIN.md").exists():
        fail("main brief must live in skills/activate/SKILL.md, not standard/")

    activate_text = activate.read_text(encoding="utf-8")
    for needle in (
        "Promode for Codex main-agent brief",
        "Main-agent-only activation",
        "not intended for subagents",
        "<role>",
        "<codex-runtime-contract>",
        "<promode-doctrine>",
        "<delegation-map>",
        "<activation-scope>",
        ".codex/promode/docs/opinion-register.md",
        "opinion IDs",
        "$promode-codex:sync",
        "Activation is not persistent",
    ):
        if needle not in activate_text:
            fail(f"activate skill missing activation contract text: {needle}")
    for needle in (
        "promode_chief_technology_officer",
        "promode_senior_engineer",
        "promode_fast_worker",
        "promode_code_reviewer",
        "promode_product_design_expert",
        "promode_auditor",
        "promode_constraint_reinforcer",
        ".codex/promode/docs/discovery-to-determinism.md",
        "GPT-5.6 Sol",
        "gpt-5.6-sol",
        "high\n  reasoning effort",
        "GPT-5.5",
        "GPT-5.4-mini",
        "Protect the main-agent context",
        "Default to planning for delegation on non-trivial tasks",
        "Aggressively split independent sidecar tasks",
    ):
        if needle not in activate_text:
            fail(f"activate skill missing mirrored Promode surface: {needle}")
    for stale in (
        "promode_implementer",
        "promode_reviewer",
        "promode_product_designer",
        "Use the `discovery-to-determinism` skill",
    ):
        if stale in activate_text:
            fail(f"activate skill contains stale surface: {stale}")

    for path in (activate_metadata, sync_metadata):
        metadata_text = path.read_text(encoding="utf-8")
        if "allow_implicit_invocation: false" not in metadata_text:
            fail(f"{path.parent.parent.name} skill must disable implicit invocation")

    sync_text = sync.read_text(encoding="utf-8")
    for needle in (
        "Explicit user-invoked",
        "install-project-agents.py",
        "hook-based Promode artifacts",
        ".codex/promode/docs/",
        ".codex/agents/promode_*.toml",
        "GitHub check",
        "--skip-upgrade-check",
        "$promode-codex:activate",
        ".codex/agents/",
        "eleven",
    ):
        if needle not in sync_text:
            fail(f"sync skill missing contract text: {needle}")


def validate_doctrine_bundle() -> None:
    docs_root = ROOT / "standard" / "docs"
    for name in DOCTRINE_DOCS:
        check_file(docs_root / name)

    register = (docs_root / "opinion-register.md").read_text(encoding="utf-8")
    for needle in (
        "Promode for Codex opinion register",
        "no-plugin-cache-coupling",
        "tdd-non-negotiable",
        "operator-seam-bulk-below-ui",
        "sync-skill",
        "main-context-for-orchestration",
        ".codex/promode/docs/opinion-register.md",
    ):
        if needle not in register:
            fail(f"opinion register missing doctrine text: {needle}")
    if "Claude" in register or "claude" in register:
        fail("opinion register must stay decoupled from Claude-specific wording")

    discovery = (docs_root / "discovery-to-determinism.md").read_text(encoding="utf-8")
    for needle in (
        "Discovery to determinism",
        "./ui-state-graph-edt.md",
        "./operator-seam-and-agent-tools.md",
        "This document teaches",
    ):
        if needle not in discovery:
            fail(f"discovery-to-determinism doc missing doctrine text: {needle}")
    if "name: discovery-to-determinism" in discovery or "references/" in discovery:
        fail("discovery-to-determinism doc must not retain skill-local metadata")

    codex_assumptions = (docs_root / "codex-assumptions.md").read_text(
        encoding="utf-8"
    )
    for needle in (
        "Explicit activation",
        "Project-local doctrine bundle",
        "Custom agents",
        "Upgrade awareness",
        "gpt-5.6-sol",
        "high reasoning effort",
        "gpt-5.5",
        "gpt-5.4-mini",
    ):
        if needle not in codex_assumptions:
            fail(f"codex assumptions doc missing runtime text: {needle}")


def validate_installer() -> None:
    with tempfile.TemporaryDirectory(prefix="promode-codex-install-") as tmp:
        project = Path(tmp)
        (project / ".git").mkdir()
        codex_dir = project / ".codex"
        agents_dir = codex_dir / "agents"
        hooks_dir = codex_dir / "hooks"
        doctrine_dir = codex_dir / "promode" / "docs"
        stale_brief = codex_dir / "PROMODE_CODEX_MAIN.md"
        stale_main_hook = hooks_dir / "promode-main-context.py"
        stale_drift_hook = hooks_dir / "promode-agent-drift.py"
        stale_doctrine = doctrine_dir / "stale-doctrine.md"
        stale_agent = agents_dir / "promode_implementer.toml"
        unrelated_agent = agents_dir / "keep_me.toml"
        unrelated_promode_file = codex_dir / "promode" / "keep.txt"
        unrelated_hook = hooks_dir / "keep-me.py"
        hooks_json = codex_dir / "hooks.json"

        agents_dir.mkdir(parents=True)
        hooks_dir.mkdir(parents=True)
        doctrine_dir.mkdir(parents=True)
        stale_agent.write_text("stale promode agent\n", encoding="utf-8")
        unrelated_agent.write_text("preserve me\n", encoding="utf-8")
        stale_brief.write_text("stale project brief\n", encoding="utf-8")
        stale_main_hook.write_text("legacy main hook\n", encoding="utf-8")
        stale_drift_hook.write_text("legacy drift hook\n", encoding="utf-8")
        stale_doctrine.write_text("stale generated doctrine\n", encoding="utf-8")
        unrelated_promode_file.write_text("preserve me\n", encoding="utf-8")
        unrelated_hook.write_text("unrelated hook\n", encoding="utf-8")
        hooks_json.write_text(
            json.dumps(
                {
                    "hooks": {
                        "SessionStart": [
                            {
                                "matcher": "startup|resume",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": "python3 .codex/hooks/keep-me.py",
                                    },
                                    {
                                        "type": "command",
                                        "command": (
                                            "python3 .codex/hooks/"
                                            "promode-main-context.py"
                                        ),
                                    },
                                ],
                            },
                            {
                                "matcher": "compact",
                                "hooks": [
                                    {
                                        "type": "command",
                                        "command": (
                                            "python3 .codex/hooks/"
                                            "promode-agent-drift.py"
                                        ),
                                    }
                                ],
                            },
                        ]
                    }
                },
                indent=2,
            )
            + "\n",
            encoding="utf-8",
        )
        installer = ROOT / "scripts" / "install-project-agents.py"
        for _ in range(2):
            proc = subprocess.run(
                [sys.executable, str(installer), "--skip-upgrade-check", str(project)],
                text=True,
                capture_output=True,
                check=False,
            )
            if proc.returncode != 0:
                fail(f"installer exited {proc.returncode}: {proc.stderr}")
            if "Restart or resume Codex" not in proc.stdout:
                fail("installer should advise restarting or resuming Codex")
            if "$promode-codex:activate" not in proc.stdout:
                fail("installer should advise explicit Promode activation")

        for agent in AGENTS:
            if not (project / ".codex" / "agents" / f"{agent}.toml").is_file():
                fail(f"installer missing agent: {agent}")
        if not (project / DOCTRINE_REGISTER_RELATIVE).is_file():
            fail("installer should sync project-local opinion register")
        if stale_doctrine.exists():
            fail("installer should remove stale generated doctrine files")
        if stale_agent.exists():
            fail("installer should remove stale Promode agent files")
        if not unrelated_agent.is_file():
            fail("installer should preserve non-Promode agent files")
        if not unrelated_promode_file.is_file():
            fail("installer should preserve non-doc files under .codex/promode")
        for path in (stale_brief, stale_main_hook, stale_drift_hook):
            if path.exists():
                fail(f"installer should remove legacy artifact: {path}")
        if not unrelated_hook.is_file():
            fail("installer should preserve unrelated hook files")

        hooks_payload = json.loads(hooks_json.read_text(encoding="utf-8"))
        commands = [
            hook.get("command")
            for groups in hooks_payload.get("hooks", {}).values()
            if isinstance(groups, list)
            for group in groups
            if isinstance(group, dict)
            for hook in group.get("hooks", [])
            if isinstance(hook, dict)
        ]
        if "python3 .codex/hooks/keep-me.py" not in commands:
            fail("installer should preserve unrelated hook commands")
        for command in commands:
            if is_promode_hook_command(command):
                fail("installer should remove Promode hook commands")


def validate_upgrade_check_parsing() -> None:
    installer = load_installer_module()
    ls_remote = "\n".join(
        (
            "1111111111111111111111111111111111111111\trefs/tags/v2.9.4",
            "2222222222222222222222222222222222222222\trefs/tags/2.10.0",
            "3333333333333333333333333333333333333333\trefs/tags/v2.10.0^{}",
            "4444444444444444444444444444444444444444\trefs/tags/2.10.0-beta",
            "5555555555555555555555555555555555555555\trefs/heads/main",
        )
    )
    if installer.latest_version_from_ls_remote(ls_remote) != "2.10.0":
        fail("installer should parse the latest stable semver tag from ls-remote")
    if installer.parse_semver("v2.10.0") != (2, 10, 0):
        fail("installer should parse v-prefixed semver")
    if installer.parse_semver("2.10.0-beta") is not None:
        fail("installer should ignore prerelease versions for upgrade warnings")
    if not installer.is_newer_version("2.10.1", "2.10.0"):
        fail("installer should detect newer patch versions")
    if installer.is_newer_version("2.9.9", "2.10.0"):
        fail("installer should not downgrade users")


def load_installer_module():
    path = ROOT / "scripts" / "install-project-agents.py"
    spec = importlib.util.spec_from_file_location("install_project_agents", path)
    if spec is None or spec.loader is None:
        fail("could not load install-project-agents.py for validation")
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module


def validate_repository_policy(source_root: Path) -> None:
    check_file(source_root / "scripts" / "check")
    if not os.access(source_root / "scripts" / "check", os.X_OK):
        fail("scripts/check must be executable")
    check_text = (source_root / "scripts" / "check").read_text(encoding="utf-8")
    if "validate-promode-codex.py --mode source" not in check_text:
        fail("scripts/check must run validate-promode-codex.py --mode source")
    if "scripts/check-local-validators" not in check_text:
        fail("scripts/check must run scripts/check-local-validators")
    local_validator_check = source_root / "scripts" / "check-local-validators"
    check_file(local_validator_check)
    if not os.access(local_validator_check, os.X_OK):
        fail("scripts/check-local-validators must be executable")
    validate_local_validator_dispatch(source_root, local_validator_check)

    ci_workflow = source_root / ".github" / "workflows" / "check.yml"
    check_file(ci_workflow)
    ci_text = ci_workflow.read_text(encoding="utf-8")
    for needle in (
        "actions/checkout",
        "actions/setup-python",
        "pull_request:",
        "push:",
        "scripts/check",
    ):
        if needle not in ci_text:
            fail(f"CI workflow must run repository checks: {needle}")

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
        "standard/docs/",
        "Do not generalize that to user projects",
    ):
        if needle not in agents_text:
            fail(f"AGENTS.md missing guidance: {needle}")


def validate_local_validator_dispatch(source_root: Path, script: Path) -> None:
    with tempfile.TemporaryDirectory(prefix="promode-codex-local-validators-") as tmp:
        tmp_path = Path(tmp)

        missing_plugin = tmp_path / "missing-plugin-validator.py"
        missing_skills = tmp_path / "missing-skills-validator.rb"
        missing_env = {
            **os.environ,
            "CODEX_PLUGIN_VALIDATOR": str(missing_plugin),
            "DEVELOPING_SKILLS_VALIDATOR": str(missing_skills),
        }
        missing_proc = subprocess.run(
            [str(script)],
            cwd=source_root,
            text=True,
            capture_output=True,
            check=False,
            env=missing_env,
        )
        if missing_proc.returncode != 0:
            fail(
                "scripts/check-local-validators should pass when local validators "
                f"are absent: stdout={missing_proc.stdout!r} stderr={missing_proc.stderr!r}"
            )
        for expected in (
            f"SKIP: Codex plugin validator not found at {missing_plugin}",
            f"SKIP: developing-skills validator not found at {missing_skills}",
        ):
            if expected not in missing_proc.stdout:
                fail(f"missing local-validator skip evidence: {expected}")

        stub = (
            "from pathlib import Path\n"
            "import os\n"
            "import sys\n"
            "log = Path(os.environ['PROMODE_VALIDATOR_STUB_LOG'])\n"
            "with log.open('a', encoding='utf-8') as handle:\n"
            "    handle.write(Path(sys.argv[0]).name + ':' + ' '.join(sys.argv[1:]) + '\\n')\n"
        )
        plugin_stub = tmp_path / "plugin-validator.py"
        skills_stub = tmp_path / "skills-validator.py"
        log_path = tmp_path / "stub.log"
        plugin_stub.write_text(stub, encoding="utf-8")
        skills_stub.write_text(stub, encoding="utf-8")
        present_env = {
            **os.environ,
            "CODEX_PLUGIN_VALIDATOR": str(plugin_stub),
            "CODEX_PLUGIN_VALIDATOR_RUNNER": sys.executable,
            "DEVELOPING_SKILLS_VALIDATOR": str(skills_stub),
            "DEVELOPING_SKILLS_VALIDATOR_RUNNER": sys.executable,
            "PROMODE_VALIDATOR_STUB_LOG": str(log_path),
        }
        present_proc = subprocess.run(
            [str(script)],
            cwd=source_root,
            text=True,
            capture_output=True,
            check=False,
            env=present_env,
        )
        if present_proc.returncode != 0:
            fail(
                "scripts/check-local-validators should run present validators: "
                f"stdout={present_proc.stdout!r} stderr={present_proc.stderr!r}"
            )
        log_text = log_path.read_text(encoding="utf-8")
        for expected in (
            "plugin-validator.py:plugins/promode-codex",
            "skills-validator.py:.",
        ):
            if expected not in log_text:
                fail(f"local validator dispatch missing invocation: {expected}")


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


def is_promode_hook_command(command: object) -> bool:
    return isinstance(command, str) and any(name in command for name in PROMODE_HOOK_NAMES)


def validate_agents() -> None:
    root = ROOT / "standard" / "agents"
    check_file(root / "promode_senior_engineer.toml")
    for stale in (
        root / "promode_implementer.toml",
        root / "promode_reviewer.toml",
        root / "promode_product_designer.toml",
    ):
        if stale.exists():
            fail(f"stale compressed agent file must be absent: {stale.name}")
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
        expected_model = EXPECTED_AGENT_MODELS.get(name)
        if expected_model is not None and data.get("model") != expected_model:
            fail(f"{path.name} must pin model {expected_model}")
        expected_reasoning_effort = EXPECTED_AGENT_REASONING_EFFORT.get(name)
        if (
            expected_reasoning_effort is not None
            and data.get("model_reasoning_effort") != expected_reasoning_effort
        ):
            fail(
                f"{path.name} must pin reasoning effort "
                f"{expected_reasoning_effort}"
            )
        instructions = data["developer_instructions"]
        if "Hook-provided transcript paths" in instructions:
            fail(f"{path.name} contains stale hook-era transcript wording")
        for phrase in COMMON_AGENT_CONTRACT_PHRASES:
            if phrase not in instructions:
                fail(f"{path.name} missing shared doctrine phrase: {phrase}")
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
    seen = set()
    for skill in sorted(path for path in skills_root.iterdir() if path.is_dir()):
        if skill.name in FORBIDDEN_EXPOSED_SKILLS:
            fail(f"skill should not be exposed in Codex plugin: {skill.name}")
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
        name = skill_frontmatter_name(frontmatter)
        if name:
            seen.add(name)
    missing = REQUIRED_SKILLS - seen
    if missing:
        fail(f"missing required skills: {sorted(missing)}")
    extra = seen - REQUIRED_SKILLS
    if extra:
        fail(f"unexpected exposed skills: {sorted(extra)}")


def skill_frontmatter_name(frontmatter: str) -> str:
    for line in frontmatter.splitlines():
        if line.startswith("name:"):
            return line.split(":", 1)[1].strip().strip("\"'")
    return ""


def validate_package() -> None:
    validate_manifest()
    validate_activation_flow()
    validate_doctrine_bundle()
    validate_installer()
    validate_upgrade_check_parsing()
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
