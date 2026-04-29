from pathlib import Path

from prosekernel.engine import render_demo_report, run_writing_demo

ROOT = Path(__file__).resolve().parents[1]


def test_writing_demo_runs_full_pipeline():
    result = run_writing_demo(ROOT, "write a launch email for ProseKernel", limit=4)
    assert result.retrieval_mode == "lexical"
    assert result.recommended_categories[0] == "email-newsletters"
    assert len(result.examples) == 4
    assert result.craft_moves
    assert result.pattern_ids
    assert "PATTERN_EMAIL_001" in result.pattern_ids
    assert result.final_report.passed


def test_render_demo_report_contains_contract_sections():
    result = run_writing_demo(ROOT, "write an outage apology", limit=3, mode="hybrid")
    report = render_demo_report(result)
    assert result.retrieval_mode == "hybrid"
    assert "Retrieval mode: hybrid" in report
    for heading in [
        "## Recommended categories",
        "## Retrieved examples",
        "## Patterns used",
        "## Craft moves to transfer",
        "## Lint result",
        "## Score improvement",
        "## Rewrite",
    ]:
        assert heading in report
