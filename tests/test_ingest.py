from pathlib import Path
from humanprint.ingest import ExampleMetadata, example_path, render_example, slugify, validate_example_text, validate_library


def test_slugify():
    assert slugify("Apple iPod — 1,000 Songs in Your Pocket!") == "apple-ipod-1-000-songs-in-your-pocket"


def test_render_example_has_required_sections():
    meta = ExampleMetadata(
        title="Test Example",
        author="Author",
        source_url="https://example.com",
        date_published="2026",
        added="2026-04-28",
        category="viral-social",
        format="thread",
        rights="metadata-only",
        tags=["hook", "clarity"],
        quality_score=8,
        use_when="When testing.",
        pattern_ids=["PATTERN_HOOK_001"],
    )
    text = render_example(meta)
    assert validate_example_text(text) == []
    assert "pattern_ids: [PATTERN_HOOK_001]" in text
    assert example_path(Path("/repo"), meta) == Path("/repo/library/viral-social/examples/test-example.md")


def test_invalid_metadata_rejected():
    meta = ExampleMetadata(
        title="Bad",
        author="Author",
        source_url="",
        date_published="2026",
        added="2026-04-28",
        category="bad-category",
        format="thread",
        rights="unknown",
        tags=["one"],
        quality_score=99,
        use_when="Never.",
        pattern_ids=["PATTERN_FAKE_999"],
    )
    errors = meta.validate()
    assert "Unknown category: bad-category" in errors
    assert "Unknown rights value: unknown" in errors
    assert "quality_score must be 1-10" in errors
    assert "source_url is required" in errors
    assert "Unknown pattern_ids: PATTERN_FAKE_999" in errors


def test_current_library_validates():
    issues = validate_library(Path(__file__).resolve().parents[1])
    assert issues == {}
