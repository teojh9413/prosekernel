from pathlib import Path

from humanprint.cli import main
from humanprint.engine import build_writing_brief, render_brief_report

ROOT = Path(__file__).resolve().parents[1]


def test_build_writing_brief_collects_examples_patterns_and_instructions():
    brief = build_writing_brief(ROOT, "write a launch email for Humanprint", limit=4)

    assert brief.task == "write a launch email for Humanprint"
    assert brief.retrieval_mode == "lexical"
    assert brief.recommended_categories[0] == "email-newsletters"
    assert len(brief.examples) == 4
    assert "PATTERN_EMAIL_001" in brief.pattern_ids
    assert brief.pattern_instructions
    assert any("Every [cadence]" in instruction for instruction in brief.pattern_instructions)
    assert brief.craft_moves
    assert "Do structure transfer, not phrase transfer." in brief.agent_prompt
    assert "Do not copy source phrases." in brief.agent_prompt
    assert "Score the draft before publishing" in brief.agent_prompt


def test_render_brief_report_is_agent_ready_and_api_free():
    brief = build_writing_brief(ROOT, "write a launch email for Humanprint", limit=3)
    report = render_brief_report(brief)

    for heading in [
        "# Humanprint Writing Brief",
        "## Retrieved examples",
        "## Patterns to apply",
        "## Craft moves",
        "## Agent drafting prompt",
        "## Quality gate",
    ]:
        assert heading in report
    assert "No model call was made" in report
    assert "Retrieval mode: lexical" in report
    assert "PATTERN_EMAIL_001" in report
    assert "humanprint scorecard" in report


def test_brief_can_use_hybrid_retrieval_mode():
    brief = build_writing_brief(
        ROOT,
        "write a customer trust update after a compromised credential scare",
        limit=3,
        mode="hybrid",
    )
    report = render_brief_report(brief)

    assert brief.retrieval_mode == "hybrid"
    assert brief.examples[0].category == "crisis-communications"
    assert "Retrieval mode: hybrid" in report


def test_cli_brief_writes_markdown_report(tmp_path):
    out = tmp_path / "brief.md"

    assert main([
        "brief",
        "write a launch email for Humanprint",
        "--root",
        str(ROOT),
        "--limit",
        "3",
        "--mode",
        "hybrid",
        "--output",
        str(out),
    ]) == 0

    text = out.read_text(encoding="utf-8")
    assert "# Humanprint Writing Brief" in text
    assert "No model call was made" in text
    assert "Retrieval mode: hybrid" in text
    assert "PATTERN_EMAIL_001" in text
