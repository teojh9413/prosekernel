from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
REQUIRED_SCORECARD_DIMENSIONS = [
    "Specificity",
    "Proof",
    "Structure",
    "Reader fit",
    "Memorability",
    "Non-genericness",
]
REQUIRED_TASKS = {
    "launch-email.md",
    "generic-social-rewrite.md",
    "incident-apology.md",
    "nontechnical-explanation.md",
    "strategic-memo.md",
    "onboarding-empty-state.md",
}


def test_phase7a_scorecard_matches_feedback_dimensions():
    text = (ROOT / "evals" / "writing-scorecard.md").read_text(encoding="utf-8")
    for dimension in REQUIRED_SCORECARD_DIMENSIONS:
        assert dimension in text
    for check in [
        "slop phrase count",
        "proof marker count",
        "weak opener detection",
        "abstract noun density",
        "long sentence count",
    ]:
        assert check in text


def test_phase7a_eval_tasks_exist_and_name_patterns():
    task_dir = ROOT / "evals" / "tasks"
    task_names = {path.name for path in task_dir.glob("*.md")}
    assert REQUIRED_TASKS <= task_names
    for path in task_dir.glob("*.md"):
        text = path.read_text(encoding="utf-8")
        for heading in ["## Task", "## Reader", "## Required pattern coverage", "## Must demonstrate", "## Failure modes"]:
            assert heading in text, f"{path.name} missing {heading}"
        assert "PATTERN_" in text
