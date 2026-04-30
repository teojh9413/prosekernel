from pathlib import Path
import subprocess

ROOT = Path(__file__).resolve().parents[1]


def _read(relative: str) -> str:
    return (ROOT / relative).read_text(encoding="utf-8")


def test_readme_links_public_launch_assets():
    readme = _read("README.md")

    assert "Taste infrastructure for AI writing agents." in readme
    assert "## What ProseKernel does" in readme
    assert "## Who it is for" in readme
    assert "## 60-second demo" in readme
    assert "docs/install.md" in readme
    assert "examples/reports/launch-email-brief.md" in readme
    assert "examples/reports/slop-critique-report.md" in readme
    assert "examples/reports/rewrite-report.md" in readme
    assert "scripts/public_demo.sh" in readme


def test_readme_keeps_demo_first_public_polish():
    readme = _read("README.md")

    assert "ProseKernel is a local writing-quality layer for AI agents." in readme
    assert "sounds finished before it has judgment" in readme
    assert "retrieve examples → apply patterns → draft → lint → score → critique → rewrite → learn safely" in readme
    assert 'prosekernel lint examples/ai-slop-sample.md || true' in readme
    assert "The lint command intentionally flags the sample draft; that is the point of the demo." in readme
    assert "## Common commands" in readme
    assert "## Quick CLI" not in readme
    assert "Track C public launch prep is implemented" in readme
    assert "Track C public launch prep is in progress" not in readme


def test_public_launch_assets_exist_and_describe_v1_release():
    expected_paths = [
        "scripts/public_demo.sh",
        "CHANGELOG.md",
        "docs/release-process.md",
        "docs/github-release-settings.md",
        "docs/public-release-checklist.md",
        "examples/reports/launch-email-brief.md",
        "examples/reports/slop-critique-report.md",
        "examples/reports/rewrite-report.md",
    ]

    for relative in expected_paths:
        assert (ROOT / relative).is_file(), relative

    changelog = _read("CHANGELOG.md")
    assert "## 0.1.0 — Public v1" in changelog
    assert "Completed Phase 12 Writing OS loop" in changelog

    release_process = _read("docs/release-process.md")
    for command in (
        "python -m pytest -q",
        "prosekernel validate-library --root .",
        "prosekernel validate-learning --root .",
        "prosekernel eval --root .",
        "bash scripts/public_demo.sh",
        "git diff --check",
        "git tag v0.1.0",
        "git push origin v0.1.0",
    ):
        assert command in release_process

    github_settings = _read("docs/github-release-settings.md")
    assert "Taste infrastructure for AI writing agents." in github_settings
    for topic in (
        "ai-agents",
        "writing",
        "cli",
        "evals",
        "llm",
        "developer-tools",
        "open-source",
        "prompt-engineering",
    ):
        assert topic in github_settings


def test_sample_reports_are_public_safe_and_reviewable():
    banned_private_markers = [
        "PRIVATE_",
        "DO_NOT_COPY",
        "copyrighted full source",
    ]
    for relative in (
        "examples/reports/launch-email-brief.md",
        "examples/reports/slop-critique-report.md",
        "examples/reports/rewrite-report.md",
    ):
        text = _read(relative)
        assert "ProseKernel" in text
        assert len(text.strip()) > 400
        for marker in banned_private_markers:
            assert marker not in text


def test_public_demo_script_contains_expected_commands():
    script = _read("scripts/public_demo.sh")
    assert script.startswith("#!/usr/bin/env bash\nset -euo pipefail")
    for command in (
        "python -m pip install -e .",
        'prosekernel brief "write a launch email for an AI writing tool" --root . --output /tmp/prosekernel-brief.md',
        'prosekernel search-examples "write a launch email for an AI writing tool" --root . --limit 3',
        'prosekernel lint examples/ai-slop-sample.md',
        'prosekernel scorecard examples/ai-slop-sample.md --task "write a launch email for an AI writing tool"',
        "prosekernel eval --root .",
    ):
        assert command in script


def test_public_release_assets_do_not_reintroduce_old_brand():
    result = subprocess.run(
        ["git", "ls-files"],
        cwd=ROOT,
        check=True,
        text=True,
        capture_output=True,
    )
    offenders: list[str] = []
    banned_tokens = ("Human" + "print", "human" + "print", "src/" + "human" + "print")
    skip_parts = {".git", ".venv", "__pycache__", ".pytest_cache", "build", "dist"}
    for raw in result.stdout.splitlines():
        path = ROOT / raw
        if not path.is_file():
            continue
        relative = path.relative_to(ROOT)
        if set(relative.parts) & skip_parts:
            continue
        if any(part.endswith(".egg-info") for part in relative.parts):
            continue
        try:
            text = path.read_text(encoding="utf-8")
        except UnicodeDecodeError:
            continue
        for token in banned_tokens:
            if token in text:
                offenders.append(raw)
                break

    assert offenders == []
