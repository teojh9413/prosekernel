from pathlib import Path

from prosekernel.cli import main

ROOT = Path(__file__).resolve().parents[1]

APPROVED_LESSON = """---
title: "Learning lesson — Checkout recovery copy"
task: "rewrite checkout recovery microcopy"
source_title: "Checkout recovery copy"
source_author: "Product Team"
source_url: "https://example.com/checkout-recovery"
rights: "user-provided"
category: "ux-product-microcopy"
tags: ["checkout", "error", "microcopy"]
pattern_ids: ["PATTERN_UX_001"]
source_text_stored: false
source_text_sha256: "abc123"
source_word_count: 42
lint_score: 88
scorecard_total: 82
promotion_status: "ready-for-human-review"
approved: true
---

# Learning lesson — Checkout recovery copy

## Source metadata
- Title: Checkout recovery copy
- Author/company: Product Team
- URL: https://example.com/checkout-recovery
- Rights: user-provided
- Source text stored: no

## Reusable lesson
- Name the failed action, explain what remains safe, and give one recovery action.
- Keep structure transfer only: metadata, critique, score deltas, and original analysis are allowed; copied source prose is not.

## Safe learning record
- Task: rewrite checkout recovery microcopy
- Category: ux-product-microcopy
- Tags: checkout, error, microcopy
- Pattern IDs: PATTERN_UX_001
- Lint score at import: 88/100
- Scorecard at import: 82/100
- Stored content: metadata, hash, metrics, and original analysis only.

## Promotion gate
- Status: ready-for-human-review
- Do not promote this note into a library example or pattern unless rights are reviewed and a human explicitly approves.
"""

UNSAFE_LESSON = APPROVED_LESSON.replace('rights: "user-provided"', 'rights: "metadata-only"')

PRIVATE_SENTENCE = "PRIVATE_SOURCE_SENTENCE_DO_NOT_COPY"


def test_propose_example_creates_reviewable_example_proposal_without_source_text(tmp_path, capsys):
    lesson_path = tmp_path / "lesson.md"
    proposal_path = tmp_path / "proposal.md"
    lesson_path.write_text(APPROVED_LESSON + f"\n<!-- {PRIVATE_SENTENCE} -->\n", encoding="utf-8")

    exit_code = main([
        "propose-example",
        str(lesson_path),
        "--root",
        str(ROOT),
        "--output",
        str(proposal_path),
    ])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert str(proposal_path) in captured.out
    text = proposal_path.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert 'title: "Checkout recovery copy"' in text
    assert 'rights: "user-provided"' in text
    assert "pattern_ids: [PATTERN_UX_001]" in text
    assert "## Why this is good" in text
    assert "## Excerpt or summary" in text
    assert "Source text was not stored" in text
    assert "Human review required before moving this proposal into `library/`" in text
    assert PRIVATE_SENTENCE not in text


def test_propose_pattern_creates_pattern_proposal_from_approved_lesson(tmp_path):
    lesson_path = tmp_path / "lesson.md"
    proposal_path = tmp_path / "pattern-proposal.md"
    lesson_path.write_text(APPROVED_LESSON, encoding="utf-8")

    exit_code = main([
        "propose-pattern",
        str(lesson_path),
        "--root",
        str(ROOT),
        "--pattern-id",
        "PATTERN_UX_002",
        "--output",
        str(proposal_path),
    ])

    assert exit_code == 0
    text = proposal_path.read_text(encoding="utf-8")
    assert text.startswith("# PATTERN_UX_002 — Checkout recovery copy")
    for section in ["## Use when", "## Reader situation", "## Structure", "## Why it works", "## Examples", "## Anti-patterns", "## Agent instruction"]:
        assert section in text
    assert "Derived from approved learning note" in text
    assert "Source text was not stored" in text


def test_proposal_bridge_refuses_metadata_only_learning_notes(tmp_path):
    lesson_path = tmp_path / "lesson.md"
    output_path = tmp_path / "proposal.md"
    lesson_path.write_text(UNSAFE_LESSON, encoding="utf-8")

    exit_code = main([
        "propose-example",
        str(lesson_path),
        "--root",
        str(ROOT),
        "--output",
        str(output_path),
    ])

    assert exit_code == 2
    assert not output_path.exists()


def test_proposal_bridge_refuses_notes_not_ready_for_human_review(tmp_path):
    lesson_path = tmp_path / "lesson.md"
    output_path = tmp_path / "proposal.md"
    lesson_path.write_text(APPROVED_LESSON.replace('promotion_status: "ready-for-human-review"', 'promotion_status: "lesson-only"'), encoding="utf-8")

    exit_code = main([
        "propose-pattern",
        str(lesson_path),
        "--root",
        str(ROOT),
        "--pattern-id",
        "PATTERN_UX_002",
        "--output",
        str(output_path),
    ])

    assert exit_code == 2
    assert not output_path.exists()


def test_proposal_bridge_refuses_to_overwrite_without_force(tmp_path):
    lesson_path = tmp_path / "lesson.md"
    output_path = tmp_path / "proposal.md"
    lesson_path.write_text(APPROVED_LESSON, encoding="utf-8")
    output_path.write_text("existing proposal", encoding="utf-8")

    exit_code = main([
        "propose-example",
        str(lesson_path),
        "--root",
        str(ROOT),
        "--output",
        str(output_path),
    ])

    assert exit_code == 1
    assert output_path.read_text(encoding="utf-8") == "existing proposal"


def test_render_example_proposal_signature_has_no_unused_output_path_parameter():
    import inspect
    from prosekernel.learning import render_example_proposal

    assert "output_path" not in inspect.signature(render_example_proposal).parameters


def test_propose_pattern_rejects_existing_known_pattern_id(tmp_path, capsys):
    lesson_path = tmp_path / "lesson.md"
    output_path = tmp_path / "pattern-proposal.md"
    lesson_path.write_text(APPROVED_LESSON, encoding="utf-8")

    exit_code = main([
        "propose-pattern",
        str(lesson_path),
        "--root",
        str(ROOT),
        "--pattern-id",
        "PATTERN_UX_001",
        "--output",
        str(output_path),
    ])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert not output_path.exists()
    assert "pattern ID already exists" in captured.err
    assert "should not be proposed as new" in captured.err


def test_propose_pattern_keeps_pattern_id_format_validation(tmp_path, capsys):
    lesson_path = tmp_path / "lesson.md"
    output_path = tmp_path / "pattern-proposal.md"
    lesson_path.write_text(APPROVED_LESSON, encoding="utf-8")

    exit_code = main([
        "propose-pattern",
        str(lesson_path),
        "--root",
        str(ROOT),
        "--pattern-id",
        "not-a-pattern-id",
        "--output",
        str(output_path),
    ])

    captured = capsys.readouterr()
    assert exit_code == 2
    assert not output_path.exists()
    assert "pattern_id must look like PATTERN_DOMAIN_001" in captured.err
