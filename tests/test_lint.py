from humanprint.lint import lint_text


def test_slop_fails():
    report = lint_text("In today's fast-paced world, teams leverage cutting-edge solutions to unlock growth.")
    assert not report.passed
    assert any(f.rule == "slop_phrase" for f in report.findings)


def test_specific_draft_passes():
    text = "The onboarding form loses users at step three. In a 42-user test, 18 people stopped when we asked for company size before showing value. Move that field after activation."
    report = lint_text(text)
    assert report.score >= 80
