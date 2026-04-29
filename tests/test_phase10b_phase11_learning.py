from pathlib import Path

from prosekernel.cli import main
from prosekernel.learning import validate_learning_note_text

ROOT = Path(__file__).resolve().parents[1]

SLOPPY_DRAFT = """In today's fast-paced digital landscape, ProseKernel is a transformative solution that leverages robust technology to unlock seamless writing excellence.

This innovative platform underscores the importance of quality and helps users elevate content with powerful insights.
"""

PRIVATE_SOURCE_SENTENCE = "PRIVATE_SOURCE_SENTENCE_DO_NOT_STORE: the internal refund queue waits 5 business days before escalation."


def test_cli_rewrite_writes_standalone_rewrite_output(tmp_path, capsys):
    draft_path = tmp_path / "draft.md"
    report_path = tmp_path / "rewrite-report.md"
    rewritten_path = tmp_path / "rewritten.md"
    draft_path.write_text(SLOPPY_DRAFT, encoding="utf-8")

    exit_code = main([
        "rewrite",
        str(draft_path),
        "--root",
        str(ROOT),
        "--task",
        "write a launch email for ProseKernel",
        "--output",
        str(report_path),
        "--rewrite-output",
        str(rewritten_path),
    ])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert str(report_path) in captured.out
    assert str(rewritten_path) in captured.out
    assert report_path.exists()
    assert rewritten_path.exists()
    report = report_path.read_text(encoding="utf-8")
    rewritten = rewritten_path.read_text(encoding="utf-8")
    assert report.startswith("# ProseKernel Rewrite Report")
    assert "## Quality delta" in report
    assert rewritten.startswith("# Rewritten draft")
    assert "# ProseKernel Rewrite Report" not in rewritten
    assert "## Quality delta" not in rewritten


def test_cli_learn_writes_metadata_only_lesson_without_source_text(tmp_path, capsys):
    draft_path = tmp_path / "source-draft.md"
    lesson_path = tmp_path / "lesson.md"
    draft_path.write_text(PRIVATE_SOURCE_SENTENCE, encoding="utf-8")

    exit_code = main([
        "learn",
        str(draft_path),
        "--root",
        str(ROOT),
        "--task",
        "rewrite help center copy for delayed refunds",
        "--source-title",
        "Refund workflow draft",
        "--source-author",
        "Support Team",
        "--source-url",
        "https://example.com/refund-workflow",
        "--rights",
        "metadata-only",
        "--category",
        "ux-product-microcopy",
        "--tags",
        "refunds, support",
        "--output",
        str(lesson_path),
    ])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert str(lesson_path) in captured.out
    text = lesson_path.read_text(encoding="utf-8")
    assert text.startswith("---\n")
    assert 'source_title: "Refund workflow draft"' in text
    assert 'source_author: "Support Team"' in text
    assert 'rights: "metadata-only"' in text
    assert "source_text_stored: false" in text
    assert "source_text_sha256:" in text
    assert 'promotion_status: "metadata-only-review"' in text
    assert "## Reusable lesson" in text
    assert "## Promotion gate" in text
    assert PRIVATE_SOURCE_SENTENCE not in text
    assert "5 business days" not in text
    assert validate_learning_note_text(text) == []


def test_learn_refuses_promotion_without_explicit_approval(tmp_path):
    draft_path = tmp_path / "source-draft.md"
    output_path = tmp_path / "lesson.md"
    draft_path.write_text("User-provided copy about a checkout error.", encoding="utf-8")

    exit_code = main([
        "learn",
        str(draft_path),
        "--source-title",
        "Checkout error copy",
        "--source-author",
        "Product Team",
        "--source-url",
        "https://example.com/checkout-error",
        "--rights",
        "user-provided",
        "--category",
        "ux-product-microcopy",
        "--tags",
        "checkout, error",
        "--promote",
        "--output",
        str(output_path),
    ])

    assert exit_code == 2
    assert not output_path.exists()


def test_learn_refuses_promotion_for_metadata_only_sources_even_when_approved(tmp_path):
    draft_path = tmp_path / "source-draft.md"
    output_path = tmp_path / "lesson.md"
    draft_path.write_text("Modern article draft that must not be promoted as a library example.", encoding="utf-8")

    exit_code = main([
        "learn",
        str(draft_path),
        "--source-title",
        "Modern article",
        "--source-author",
        "Modern Publication",
        "--source-url",
        "https://example.com/modern-article",
        "--rights",
        "metadata-only",
        "--category",
        "essays-literary",
        "--tags",
        "essay, craft",
        "--promote",
        "--approved",
        "--output",
        str(output_path),
    ])

    assert exit_code == 2
    assert not output_path.exists()


def test_validate_learning_note_rejects_stored_source_text():
    unsafe = """---
source_title: "Unsafe note"
source_author: "Example"
source_url: "https://example.com"
rights: "metadata-only"
source_text_stored: true
promotion_status: "metadata-only-review"
---

## Source text
Copied source text appears here.
"""

    errors = validate_learning_note_text(unsafe)

    assert "source_text_stored must be false" in errors
    assert "learning notes must not include source-text sections" in errors


def test_rewrite_refuses_same_report_and_standalone_output_path(tmp_path):
    draft_path = tmp_path / "draft.md"
    output_path = tmp_path / "rewrite.md"
    draft_path.write_text(SLOPPY_DRAFT, encoding="utf-8")

    exit_code = main([
        "rewrite",
        str(draft_path),
        "--root",
        str(ROOT),
        "--task",
        "write a launch email for ProseKernel",
        "--output",
        str(output_path),
        "--rewrite-output",
        str(output_path),
    ])

    assert exit_code == 2
    assert not output_path.exists()


def test_learn_refuses_to_overwrite_existing_note_without_force(tmp_path):
    draft_path = tmp_path / "source-draft.md"
    output_path = tmp_path / "lesson.md"
    draft_path.write_text("User-provided checkout error copy.", encoding="utf-8")
    output_path.write_text("existing audit record", encoding="utf-8")

    exit_code = main([
        "learn",
        str(draft_path),
        "--source-title",
        "Checkout error copy",
        "--source-author",
        "Product Team",
        "--source-url",
        "https://example.com/checkout-error",
        "--rights",
        "user-provided",
        "--category",
        "ux-product-microcopy",
        "--tags",
        "checkout, error",
        "--output",
        str(output_path),
    ])

    assert exit_code == 1
    assert output_path.read_text(encoding="utf-8") == "existing audit record"


def test_validate_learning_note_rejects_unsafe_promotion_status():
    unsafe = """---
source_title: "Unsafe promotion"
source_author: "Example"
source_url: "https://example.com"
rights: "metadata-only"
source_text_stored: false
source_text_sha256: "abc123"
promotion_status: "ready-for-human-review"
approved: true
---

## Reusable lesson
- A lesson.

## Promotion gate
- Status: ready-for-human-review
"""

    errors = validate_learning_note_text(unsafe)

    assert "ready-for-human-review requires safe rights" in errors


def test_validate_learning_note_requires_metadata_in_frontmatter():
    unsafe = """---
source_text_stored: false
source_text_sha256: "abc123"
promotion_status: "lesson-only"
---

source_title: "Only in body"
source_author: "Only in body"
source_url: "https://example.com"
rights: "user-provided"

## Reusable lesson
- A lesson.

## Promotion gate
- Status: lesson-only
"""

    errors = validate_learning_note_text(unsafe)

    assert "missing frontmatter: source_title" in errors
    assert "missing frontmatter: rights" in errors


def test_validate_learning_note_rejects_source_text_heading_variants():
    unsafe = """---
source_title: "Unsafe note"
source_author: "Example"
source_url: "https://example.com"
rights: "user-provided"
source_text_stored: false
source_text_sha256: "abc123"
promotion_status: "lesson-only"
---

### Original draft
Copied draft appears here.

## Reusable lesson
- A lesson.

## Promotion gate
- Status: lesson-only
"""

    errors = validate_learning_note_text(unsafe)

    assert "learning notes must not include source-text sections" in errors


def test_learn_rejects_multiline_metadata_to_prevent_frontmatter_injection(tmp_path):
    draft_path = tmp_path / "source-draft.md"
    output_path = tmp_path / "lesson.md"
    draft_path.write_text("User-provided checkout error copy.", encoding="utf-8")

    exit_code = main([
        "learn",
        str(draft_path),
        "--source-title",
        "Checkout error\nsource_text_stored: true",
        "--source-author",
        "Product Team",
        "--source-url",
        "https://example.com/checkout-error",
        "--rights",
        "user-provided",
        "--category",
        "ux-product-microcopy",
        "--tags",
        "checkout, error",
        "--output",
        str(output_path),
    ])

    assert exit_code == 2
    assert not output_path.exists()
