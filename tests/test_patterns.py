from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SECTIONS = [
    "## Use when",
    "## Reader situation",
    "## Structure",
    "## Why it works",
    "## Examples",
    "## Anti-patterns",
    "## Agent instruction",
]


def strict_pattern_files():
    return sorted((ROOT / "patterns").glob("PATTERN_*.md"))


def test_phase5_strict_pattern_files_exist():
    pattern_names = {path.name for path in strict_pattern_files()}
    assert "PATTERN_PROOF_001-specific-proof-ladder.md" in pattern_names
    assert "PATTERN_HOOK_001-portable-distinction.md" in pattern_names
    assert "PATTERN_EMAIL_001-promised-cadence.md" in pattern_names
    assert "PATTERN_CRISIS_001-impact-timeline-cause-prevention.md" in pattern_names
    assert "PATTERN_UX_001-actionable-recovery-microcopy.md" in pattern_names
    assert "PATTERN_STRATEGY_001-decision-grade-principles.md" in pattern_names
    assert "PATTERN_BRAND_001-worldview-positioning.md" in pattern_names
    assert "PATTERN_EXPLAIN_001-progressive-disclosure.md" in pattern_names
    assert "PATTERN_SPEECH_001-shared-principle-renewed-duty.md" in pattern_names
    assert "PATTERN_REPORTAGE_001-scene-to-system-accountability.md" in pattern_names
    assert "PATTERN_INTERNAL_001-explicit-ownership-operating-doc.md" in pattern_names
    assert "PATTERN_PERSUASION_001-awareness-matched-argument.md" in pattern_names


def test_strict_patterns_follow_schema():
    for path in strict_pattern_files():
        text = path.read_text(encoding="utf-8")
        assert text.startswith("# PATTERN_")
        for section in REQUIRED_SECTIONS:
            assert section in text, f"{path.name} missing {section}"
        assert "library/" in text
