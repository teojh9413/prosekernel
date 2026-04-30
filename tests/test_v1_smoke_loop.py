from pathlib import Path

from prosekernel.cli import main

ROOT = Path(__file__).resolve().parents[1]
PRIVATE_SOURCE_PROSE = "PRIVATE_SMOKE_SOURCE_PROSE_DO_NOT_COPY"


def test_v1_cli_smoke_loop_generates_safe_learning_and_review_proposals(tmp_path, capsys):
    draft_path = tmp_path / "draft.md"
    brief_path = tmp_path / "brief.md"
    critique_path = tmp_path / "critique.md"
    rewrite_report_path = tmp_path / "rewrite-report.md"
    rewritten_path = tmp_path / "rewritten.md"
    lesson_path = tmp_path / "lesson.md"
    example_proposal_path = tmp_path / "example-proposal.md"
    pattern_proposal_path = tmp_path / "pattern-proposal.md"

    draft_path.write_text(
        f"{PRIVATE_SOURCE_PROSE}: checkout failed after card validation. Tell the user the cart is safe and the next action is retrying payment.",
        encoding="utf-8",
    )

    assert main([
        "brief",
        "rewrite checkout recovery microcopy",
        "--root",
        str(ROOT),
        "--output",
        str(brief_path),
    ]) == 0
    assert brief_path.exists()

    critique_exit = main([
        "critique",
        str(draft_path),
        "--root",
        str(ROOT),
        "--task",
        "rewrite checkout recovery microcopy",
        "--output",
        str(critique_path),
    ])
    assert critique_exit in {0, 1}
    assert critique_path.exists()

    assert main([
        "rewrite",
        str(draft_path),
        "--root",
        str(ROOT),
        "--task",
        "rewrite checkout recovery microcopy",
        "--output",
        str(rewrite_report_path),
        "--rewrite-output",
        str(rewritten_path),
    ]) == 0
    assert rewrite_report_path.exists()
    assert rewritten_path.exists()

    assert main([
        "learn",
        str(draft_path),
        "--root",
        str(ROOT),
        "--task",
        "rewrite checkout recovery microcopy",
        "--source-title",
        "Smoke checkout recovery draft",
        "--source-author",
        "Product Team",
        "--source-url",
        "https://example.com/smoke-checkout-recovery",
        "--rights",
        "user-provided",
        "--category",
        "ux-product-microcopy",
        "--tags",
        "checkout, microcopy",
        "--promote",
        "--approved",
        "--output",
        str(lesson_path),
    ]) == 0
    assert lesson_path.exists()
    lesson = lesson_path.read_text(encoding="utf-8")
    assert PRIVATE_SOURCE_PROSE not in lesson
    assert "source_text_stored: false" in lesson
    assert 'promotion_status: "ready-for-human-review"' in lesson

    temp_validation_root = tmp_path / "validation-root"
    (temp_validation_root / "library").mkdir(parents=True)
    (temp_validation_root / "patterns").mkdir(parents=True)
    (temp_validation_root / "src" / "prosekernel").mkdir(parents=True)
    (temp_validation_root / "pyproject.toml").write_text("[project]\nname = \"prosekernel-smoke\"\n", encoding="utf-8")
    (temp_validation_root / "learning" / "lessons").mkdir(parents=True)
    (temp_validation_root / "learning" / "lessons" / "lesson.md").write_text(lesson, encoding="utf-8")
    assert main(["validate-learning", "--root", str(temp_validation_root)]) == 0

    assert main([
        "propose-example",
        str(lesson_path),
        "--root",
        str(ROOT),
        "--output",
        str(example_proposal_path),
    ]) == 0
    assert example_proposal_path.exists()
    example_proposal = example_proposal_path.read_text(encoding="utf-8")
    assert PRIVATE_SOURCE_PROSE not in example_proposal
    assert "proposal_status: review-required" in example_proposal
    assert "source_text_stored: false" in example_proposal

    assert main([
        "propose-pattern",
        str(lesson_path),
        "--root",
        str(ROOT),
        "--pattern-id",
        "PATTERN_UX_999",
        "--output",
        str(pattern_proposal_path),
    ]) == 0
    assert pattern_proposal_path.exists()
    pattern_proposal = pattern_proposal_path.read_text(encoding="utf-8")
    assert PRIVATE_SOURCE_PROSE not in pattern_proposal
    assert "Proposal status: review-required" in pattern_proposal
    assert "Source text was not stored" in pattern_proposal

    assert main(["validate-library", "--root", str(ROOT)]) == 0
    assert main(["eval", "--root", str(ROOT)]) == 0

    captured = capsys.readouterr()
    assert str(brief_path) in captured.out
    assert str(lesson_path) in captured.out
