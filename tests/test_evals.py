from pathlib import Path

from humanprint.cli import main
from humanprint.evals import evaluate_fixtures, score_text

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


def test_phase7a_fixtures_distinguish_weak_and_strong():
    results = evaluate_fixtures(ROOT)
    assert len(results) == 12
    assert all(result.passed for result in results)
    weak_scores = [r.scorecard.total for r in results if r.expected == "weak"]
    strong_scores = [r.scorecard.total for r in results if r.expected == "strong"]
    assert max(weak_scores) < min(strong_scores)
    assert min(strong_scores) >= 75
    assert max(weak_scores) < 75


def test_score_text_returns_feedback_dimensions():
    text = (ROOT / "evals" / "fixtures" / "strong" / "strategic-memo.md").read_text(encoding="utf-8")
    report = score_text(text, task="strategic memo evals before LLM adapter")
    assert report.total >= 75
    assert [d.name for d in report.dimensions] == REQUIRED_SCORECARD_DIMENSIONS
    assert report.metrics.proof_marker_count >= 2


def test_cli_scorecard_and_eval_commands(tmp_path):
    strong_path = ROOT / "evals" / "fixtures" / "strong" / "launch-email.md"
    score_out = tmp_path / "scorecard.md"
    assert main(["scorecard", str(strong_path), "--task", "launch email for Humanprint", "--output", str(score_out)]) == 0
    assert "Total score:" in score_out.read_text(encoding="utf-8")

    eval_out = tmp_path / "eval.md"
    assert main(["eval", "--root", str(ROOT), "--output", str(eval_out)]) == 0
    text = eval_out.read_text(encoding="utf-8")
    assert "Passed: 12/12" in text
