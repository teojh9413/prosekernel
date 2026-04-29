from humanprint.lint import lint_text


def test_slop_fails():
    report = lint_text("In today's fast-paced world, teams leverage cutting-edge solutions to unlock growth.")
    assert not report.passed
    assert any(f.rule == "slop_phrase" for f in report.findings)


def test_specific_draft_passes():
    text = "The onboarding form loses users at step three. In a 42-user test, 18 people stopped when we asked for company size before showing value. Move that field after activation."
    report = lint_text(text)
    assert report.score >= 80


def test_legacy_inflation_fails():
    report = lint_text("The update stands as a testament to innovation and marks a pivotal moment in the evolving landscape.")
    assert not report.passed
    assert any(f.rule == "legacy_inflation" for f in report.findings)


def test_vague_attribution_warns():
    report = lint_text("Many experts believe this improves productivity, but the draft names no source.")
    assert any(f.rule == "vague_attribution" for f in report.findings)


def test_smart_sounding_empty_fails():
    text = " ".join([
        "This platform improves productivity, quality, growth, and value across the ecosystem.",
        "The experience creates a solution that supports innovation and success for modern teams.",
        "It gives organizations a better journey, a stronger impact, and a clearer way to operate.",
        "The approach is flexible enough for different workflows while remaining useful for every stakeholder.",
        "Overall, it helps teams move faster and communicate better without unnecessary complexity."
    ])
    report = lint_text(text)
    assert not report.passed
    assert any(f.rule == "smart_sounding_empty" for f in report.findings)
