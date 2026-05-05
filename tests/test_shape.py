from pathlib import Path

from prosekernel.cli import main
from prosekernel.shape import render_shape_report, run_shape
from prosekernel.shape_archetypes import recommend_archetypes
from prosekernel.shape_rules import analyze_shape_rules

ROOT = Path(__file__).resolve().parents[1]

GENERIC_PROPOSAL = """# Executive Summary

In today's rapidly evolving landscape, payments companies face a significant opportunity.

# Market Opportunity

The market is changing.

# AI Transformation

This is not just automation, but transformation.

# Proposed Solutions

There are several key initiatives.

# Implementation Roadmap

Additionally, the roadmap can proceed in phases.

# Conclusion

In conclusion, by embracing AI, companies can position themselves for the future.
"""

GENERIC_ARTICLE = """# Introduction

This article explores the topic.

# What is Agentic Writing?

Agentic writing is important.

# Why Agentic Writing Matters

It matters for teams.

# Key Benefits

There are several key benefits.

# Challenges

There are challenges.

# Future Outlook

The future of agentic writing is bright.

# Conclusion

Ultimately, this shows the importance of the topic.
"""

ONE_SENTENCE_PARAGRAPHS = """# Note

This is one sentence.

This is another sentence.

This is a third sentence.

This paragraph has two sentences. It is less theatrical.

This is a fifth sentence.
"""

SITUATED_STRUCTURE = """# Why I am writing this now

Your payments business already has the merchant relationship, the transaction context, and the operational trust most AI vendors lack. That combination is why I think this is worth discussing now.

# What I noticed in the current business

The obvious AI upgrade is support automation. I would not start there. It saves cost, but it does not change how the company is understood by merchants.

# The part I would not build first

I would avoid a broad AI platform pitch. It asks the organization to believe too much before there is a specific commercial wedge.

# The commercial path worth testing

The sharper test is an agent layer around merchant cashflow: reconciliation, invoice follow up, and short term financing signals. It uses data the company already sees and creates a reason for merchants to return between payments events.

# What the first conversation should decide

The useful meeting is not to approve a roadmap. It is to decide whether this wedge is worth a 30 day discovery sprint with one merchant segment.
"""


def _rules(text: str):
    return analyze_shape_rules(text, task="proposal to payments company", reader="company boss", intent="create curiosity for a meeting")


def _finding_rules(text: str) -> set[str]:
    return {finding.rule for finding in _rules(text).findings}


def test_generic_proposal_ladder_is_flagged():
    analysis = _rules(GENERIC_PROPOSAL)

    finding = next(f for f in analysis.findings if f.rule == "generic_section_ladder")
    assert finding.severity == "high"
    assert "generic proposal" in finding.message.lower() or "default ai" in finding.message.lower()


def test_generic_article_ladder_is_flagged():
    rules = _finding_rules(GENERIC_ARTICLE)

    assert "generic_section_ladder" in rules
    assert "heading_as_container" in rules


def test_one_sentence_paragraph_overuse_is_flagged():
    rules = _finding_rules(ONE_SENTENCE_PARAGRAPHS)

    assert "one_sentence_paragraph_overuse" in rules


def test_em_dash_overuse_is_flagged():
    text = "# Note\n\nThis needs care — not drama — because rhythm matters — and defaults leak — when every turn uses decoration. Another line — with one more."

    rules = _finding_rules(text)

    assert "em_dash_overuse" in rules


def test_repeated_contrast_formula_is_flagged():
    text = "# Note\n\nIt is not a tool, but a workflow. The question is not whether AI writes. The question is whether the structure has judgment."

    rules = _finding_rules(text)

    assert "repeated_contrast_formula" in rules


def test_generic_signposting_is_flagged():
    text = "# Note\n\nIt is important to note that this represents a significant opportunity. Moreover, this underscores the importance of the initiative."

    rules = _finding_rules(text)

    assert "generic_signposting" in rules


def test_weak_conclusion_is_flagged():
    rules = _finding_rules(GENERIC_ARTICLE)

    assert "weak_ending" in rules


def test_specific_situated_structure_scores_better_than_generic_structure(tmp_path):
    bad_path = tmp_path / "bad.md"
    good_path = tmp_path / "good.md"
    bad_path.write_text(GENERIC_PROPOSAL, encoding="utf-8")
    good_path.write_text(SITUATED_STRUCTURE, encoding="utf-8")

    bad = run_shape(bad_path, task="proposal to payments company", reader="company boss", intent="create curiosity for a meeting")
    good = run_shape(good_path, task="proposal to payments company", reader="company boss", intent="create curiosity for a meeting")

    assert good.score.total > bad.score.total
    assert good.ai_structure_risk in {"Low", "Medium"}
    assert bad.ai_structure_risk == "High"


def test_shape_report_includes_recommended_archetype_and_rewrite_instructions(tmp_path):
    path = tmp_path / "draft.md"
    path.write_text(GENERIC_PROPOSAL, encoding="utf-8")

    report = render_shape_report(run_shape(path, task="proposal to payments company", reader="company boss", intent="create curiosity for a meeting"))

    assert report.startswith("# ProseKernel Shape Report")
    assert "AI structure risk: High" in report
    assert "## Recommended structure" in report
    assert "Curiosity Proposal" in report
    assert "## Rewrite instructions for the agent" in report
    assert "Do not simply rename headings" in report
    assert "No model call was made" in report


def test_archetype_selector_maps_reader_intent_to_curiosity_proposal():
    recs = recommend_archetypes(task="proposal to payments company", reader="company boss", intent="create curiosity for a meeting", channel="")

    assert recs[0].name == "Curiosity Proposal"
    assert any(rec.name == "Direct Advisory Note" for rec in recs)


def test_cli_shape_writes_output_file(tmp_path, capsys):
    draft_path = tmp_path / "draft.md"
    output_path = tmp_path / "shape-report.md"
    draft_path.write_text(GENERIC_PROPOSAL, encoding="utf-8")

    exit_code = main([
        "shape",
        str(draft_path),
        "--root",
        str(ROOT),
        "--task",
        "proposal to payments company",
        "--reader",
        "company boss",
        "--intent",
        "create curiosity for a meeting",
        "--output",
        str(output_path),
    ])

    captured = capsys.readouterr()
    assert exit_code == 0
    assert str(output_path) in captured.out
    assert "# ProseKernel Shape Report" in output_path.read_text(encoding="utf-8")


def test_cli_shape_works_from_repo_root_and_with_root(monkeypatch, tmp_path, capsys):
    repo_output = tmp_path / "repo-output.md"
    root_output = tmp_path / "root-output.md"
    draft_path = ROOT / "examples" / "ai-structure-sample.md"

    monkeypatch.chdir(ROOT)
    repo_exit = main([
        "shape",
        str(draft_path),
        "--task",
        "proposal to payments company",
        "--reader",
        "company boss",
        "--intent",
        "create curiosity for a meeting",
        "--output",
        str(repo_output),
    ])

    monkeypatch.chdir(tmp_path)
    root_exit = main([
        "shape",
        str(draft_path),
        "--root",
        str(ROOT),
        "--task",
        "proposal to payments company",
        "--reader",
        "company boss",
        "--intent",
        "create curiosity for a meeting",
        "--output",
        str(root_output),
    ])

    capsys.readouterr()
    assert repo_exit == 0
    assert root_exit == 0
    assert repo_output.is_file()
    assert root_output.is_file()


def test_shape_docs_examples_and_sample_report_exist_without_old_brand():
    expected = [
        ROOT / "docs" / "editorial-architecture.md",
        ROOT / "examples" / "ai-structure-sample.md",
        ROOT / "examples" / "human-structure-sample.md",
        ROOT / "examples" / "reports" / "shape-report.md",
    ]

    for path in expected:
        assert path.is_file(), path
        text = path.read_text(encoding="utf-8")
        assert "ProseKernel" in text
        assert ("Human" + "print") not in text
        assert ("human" + "print") not in text
