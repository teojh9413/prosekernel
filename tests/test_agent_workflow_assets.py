from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]

REQUIRED_AGENT_FILES = [
    "SKILL.md",
    "prompts/agent-workflow.md",
    "prompts/writing-brief.md",
    "prompts/critique.md",
    "prompts/rewrite.md",
    "docs/editorial-architecture.md",
    "docs/phase-9-agent-workflow.md",
]


def read_rel(path: str) -> str:
    return (ROOT / path).read_text(encoding="utf-8")


def test_phase9_agent_workflow_files_exist():
    missing = [path for path in REQUIRED_AGENT_FILES if not (ROOT / path).exists()]

    assert missing == []


def test_repo_skill_is_agent_ready_and_public_safe():
    text = read_rel("SKILL.md")

    for required in [
        "name: prosekernel",
        "ProseKernel is an open-source taste engine for AI writing agents.",
        "prosekernel brief",
        "prosekernel shape",
        "prosekernel lint",
        "prosekernel scorecard",
        "Do structure transfer, not phrase transfer.",
        "Do not copy source phrases.",
        "Do not auto-save private user writing",
    ]:
        assert required in text


def test_agent_workflow_prompt_is_end_to_end_and_command_grounded():
    text = read_rel("prompts/agent-workflow.md")

    for required in [
        "classify → retrieve → patterns → brief → draft → shape → lint/score → revise → explain",
        "prosekernel search-examples",
        "prosekernel brief",
        "prosekernel shape",
        "prosekernel lint",
        "prosekernel scorecard",
        "explain what changed",
        "No model/API call is required until the explicit drafting step",
    ]:
        assert required in text


def test_prompt_templates_cover_brief_critique_and_rewrite_contracts():
    brief = read_rel("prompts/writing-brief.md")
    critique = read_rel("prompts/critique.md")
    rewrite = read_rel("prompts/rewrite.md")

    for required in [
        "Reader",
        "Goal",
        "Awareness stage",
        "Retrieved examples",
        "Patterns to apply",
        "Quality gate",
    ]:
        assert required in brief

    for required in [
        "diagnose generic AI slop",
        "specificity",
        "proof",
        "reader fit",
        "non-genericness",
        "line-level fixes",
    ]:
        assert required in critique

    for required in [
        "preserve the intended meaning",
        "structure transfer, not phrase transfer",
        "What changed",
        "prosekernel lint",
        "prosekernel scorecard",
    ]:
        assert required in rewrite


def test_docs_and_readme_link_phase9_agent_workflow():
    phase_doc = read_rel("docs/phase-9-agent-workflow.md")
    agent_doc = read_rel("docs/agent-workflow.md")
    readme = read_rel("README.md")
    roadmap = read_rel("ROADMAP.md")

    for required in [
        "Phase 9",
        "Codex",
        "Claude Code",
        "Cursor",
        "OpenCode",
        "Hermes",
        "classify → retrieve → patterns → brief → draft → shape → lint/score → revise → explain",
        "prosekernel shape",
    ]:
        assert required in phase_doc

    assert "docs/phase-9-agent-workflow.md" in readme
    assert "prompts/agent-workflow.md" in agent_doc
    assert "Phase 9 — Agent workflow integration" in roadmap
    assert "Status: implemented." in roadmap
