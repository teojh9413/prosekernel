from pathlib import Path

from prosekernel.cli import main
from prosekernel.engine import (
    render_critique_report,
    render_rewrite_report,
    run_critique,
    run_rewrite,
)

ROOT = Path(__file__).resolve().parents[1]

SLOPPY_DRAFT = """In today's fast-paced digital landscape, ProseKernel is a transformative solution that leverages robust technology to unlock seamless writing excellence.

This innovative platform underscores the importance of quality and helps users elevate content with powerful insights.
"""


def test_run_critique_scores_draft_and_builds_revision_plan(tmp_path):
    draft_path = tmp_path / "draft.md"
    draft_path.write_text(SLOPPY_DRAFT, encoding="utf-8")

    result = run_critique(
        ROOT,
        draft_path,
        task="write a launch email for ProseKernel",
        limit=3,
        mode="hybrid",
    )

    assert result.path == draft_path
    assert result.task == "write a launch email for ProseKernel"
    assert result.retrieval_mode == "hybrid"
    assert result.lint_report.score < 100
    assert result.scorecard.total < 75
    assert result.recommended_categories[0] == "email-newsletters"
    assert result.examples
    assert result.pattern_ids
    assert result.revision_plan
    assert any("specific" in item.lower() or "proof" in item.lower() for item in result.revision_plan)


def test_render_critique_report_is_productized_markdown(tmp_path):
    draft_path = tmp_path / "draft.md"
    draft_path.write_text(SLOPPY_DRAFT, encoding="utf-8")

    report = render_critique_report(
        run_critique(ROOT, draft_path, task="write a launch email for ProseKernel", limit=2)
    )

    assert report.startswith("# ProseKernel Critique Report")
    for heading in [
        "## Verdict",
        "## Scorecard",
        "## Lint findings",
        "## Revision plan",
        "## Retrieved examples",
        "## Patterns to apply",
        "## Next command",
    ]:
        assert heading in report
    assert "prosekernel rewrite" in report
    assert "No model call was made" in report


def test_run_rewrite_returns_revised_draft_and_quality_delta(tmp_path):
    draft_path = tmp_path / "draft.md"
    draft_path.write_text(SLOPPY_DRAFT, encoding="utf-8")

    result = run_rewrite(
        ROOT,
        draft_path,
        task="write a launch email for ProseKernel",
        limit=3,
        mode="hybrid",
    )

    assert result.path == draft_path
    assert result.task == "write a launch email for ProseKernel"
    assert result.rewritten_text != result.original_text
    assert "transformative solution" not in result.rewritten_text.lower()
    assert result.final_scorecard.total >= result.initial_scorecard.total
    assert result.final_lint_report.score >= result.initial_lint_report.score
    assert result.examples
    assert result.pattern_ids


def test_render_rewrite_report_is_productized_markdown(tmp_path):
    draft_path = tmp_path / "draft.md"
    draft_path.write_text(SLOPPY_DRAFT, encoding="utf-8")

    report = render_rewrite_report(
        run_rewrite(ROOT, draft_path, task="write a launch email for ProseKernel", limit=2)
    )

    assert report.startswith("# ProseKernel Rewrite Report")
    for heading in [
        "## Quality delta",
        "## Revision plan used",
        "## Rewritten draft",
        "## Retrieved examples",
        "## Patterns applied",
        "## Quality gate",
    ]:
        assert heading in report
    assert "No model call was made" in report
    assert "prosekernel scorecard" in report


def test_run_rewrite_preserves_non_prosekernel_topic(tmp_path):
    draft_path = tmp_path / "refund draft.md"
    draft_path.write_text(
        "Customers need clarity when a refund is delayed. Explain the 5 business day review window, the email receipt, and the support escalation path.",
        encoding="utf-8",
    )

    result = run_rewrite(
        ROOT,
        draft_path,
        task="rewrite help center copy for a refund workflow",
        limit=3,
        mode="hybrid",
    )

    assert "refund" in result.rewritten_text.lower()
    assert "5 business day" in result.rewritten_text.lower()
    assert "support escalation" in result.rewritten_text.lower()
    assert "ProseKernel" not in result.rewritten_text
    assert "AI writing agent" not in result.rewritten_text


def test_critique_next_command_quotes_paths_and_tasks(tmp_path):
    draft_path = tmp_path / "draft with spaces.md"
    draft_path.write_text(SLOPPY_DRAFT, encoding="utf-8")
    task = 'rewrite launch email for "agent teams"'

    report = render_critique_report(run_critique(ROOT, draft_path, task=task, limit=1))

    assert "## Next command" in report
    assert "'" in report
    assert str(draft_path) in report
    assert '--task \'rewrite launch email for "agent teams"\'' in report


def test_rewrite_quality_gate_quotes_task(tmp_path):
    draft_path = tmp_path / "draft.md"
    draft_path.write_text(SLOPPY_DRAFT, encoding="utf-8")
    task = 'rewrite launch email for "agent teams"'

    report = render_rewrite_report(run_rewrite(ROOT, draft_path, task=task, limit=1))

    assert "## Quality gate" in report
    assert "prosekernel scorecard rewritten.md --task" in report
    assert '--task \'rewrite launch email for "agent teams"\'' in report


def test_cli_critique_and_rewrite_write_markdown_reports(tmp_path, capsys):
    draft_path = tmp_path / "draft.md"
    critique_path = tmp_path / "critique.md"
    rewrite_path = tmp_path / "rewrite.md"
    draft_path.write_text(SLOPPY_DRAFT, encoding="utf-8")

    critique_exit = main([
        "critique",
        str(draft_path),
        "--root",
        str(ROOT),
        "--task",
        "write a launch email for ProseKernel",
        "--mode",
        "hybrid",
        "--output",
        str(critique_path),
    ])
    rewrite_exit = main([
        "rewrite",
        str(draft_path),
        "--root",
        str(ROOT),
        "--task",
        "write a launch email for ProseKernel",
        "--mode",
        "hybrid",
        "--output",
        str(rewrite_path),
    ])

    captured = capsys.readouterr()
    assert critique_exit == 1
    assert rewrite_exit == 0
    assert str(critique_path) in captured.out
    assert str(rewrite_path) in captured.out
    assert "# ProseKernel Critique Report" in critique_path.read_text(encoding="utf-8")
    assert "# ProseKernel Rewrite Report" in rewrite_path.read_text(encoding="utf-8")


def test_friendlier_cli_aliases_preserve_existing_commands(capsys):
    examples_exit = main(["examples", "write a launch email for ProseKernel", "--root", str(ROOT), "--limit", "1"])
    demo_exit = main(["demo", "write a launch email for ProseKernel", "--root", str(ROOT), "--limit", "1"])
    score_exit = main(["score", str(ROOT / "evals" / "fixtures" / "strong" / "launch-email.md")])

    captured = capsys.readouterr()
    assert examples_exit == 0
    assert demo_exit == 0
    assert score_exit == 0
    assert "Recommended categories" in captured.out
    assert "# ProseKernel Retrieval + Writing Demo" in captured.out
    assert "# ProseKernel Scorecard" in captured.out
