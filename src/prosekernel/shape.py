from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path

from .shape_archetypes import StructureArchetype, recommend_archetypes
from .shape_rules import ShapeFinding, ShapeRuleAnalysis, analyze_shape_rules


@dataclass(frozen=True)
class ShapeDimensionScore:
    name: str
    score: int
    max_score: int
    rationale: str


@dataclass(frozen=True)
class ShapeScorecard:
    total: int
    dimensions: tuple[ShapeDimensionScore, ...]


@dataclass(frozen=True)
class ShapeReport:
    path: Path
    task: str
    reader: str
    intent: str
    channel: str
    analysis: ShapeRuleAnalysis
    score: ShapeScorecard
    ai_structure_risk: str
    recommended_archetypes: tuple[StructureArchetype, ...]
    rewrite_instructions: tuple[str, ...]


def _cap(value: int, maximum: int) -> int:
    return max(0, min(maximum, value))


def _severity_penalty(findings: tuple[ShapeFinding, ...], rules: set[str]) -> int:
    penalty = 0
    for finding in findings:
        if finding.rule not in rules:
            continue
        if finding.severity in {"severe", "high"}:
            penalty += 6
        elif finding.severity == "medium":
            penalty += 4
        else:
            penalty += 2
    return penalty


def _has_rule(analysis: ShapeRuleAnalysis, rule: str) -> bool:
    return any(finding.rule == rule for finding in analysis.findings)


def score_shape(analysis: ShapeRuleAnalysis, task: str = "", reader: str = "", intent: str = "") -> ShapeScorecard:
    findings = analysis.findings
    metrics = analysis.metrics

    reader_fit = 10 if reader else 8
    if _has_rule(analysis, "lack_of_situated_reader"):
        reader_fit -= 5
    if reader and any(term.lower() in " ".join(analysis.headings).lower() for term in reader.split() if len(term) > 3):
        reader_fit += 2
    reader_fit = _cap(reader_fit, 15)

    intent_fit = 10 if intent else 8
    if _has_rule(analysis, "fake_completeness"):
        intent_fit -= 4
    if intent and "meeting" in intent.lower() and any("conversation" in heading.lower() or "discuss" in heading.lower() for heading in analysis.headings):
        intent_fit += 3
    intent_fit = _cap(intent_fit, 15)

    structure_originality = 13
    structure_originality -= _severity_penalty(findings, {"generic_section_ladder", "heading_as_container"})
    if metrics.heading_count and metrics.generic_heading_count == 0:
        structure_originality += 2
    structure_originality = _cap(structure_originality, 15)

    judgment = 12
    judgment -= _severity_penalty(findings, {"symmetrical_section_rhythm", "fake_completeness", "generic_section_ladder"})
    if any(word in " ".join(analysis.headings).lower() for word in ("not build", "tradeoff", "decide", "worth", "risk", "constraint")):
        judgment += 3
    judgment = _cap(judgment, 15)

    rhythm = 8
    rhythm -= _severity_penalty(findings, {"one_sentence_paragraph_overuse", "em_dash_overuse", "repeated_contrast_formula"})
    if metrics.paragraph_count >= 3 and metrics.one_sentence_paragraph_pct < 40:
        rhythm += 2
    rhythm = _cap(rhythm, 10)

    heading_quality = 8
    heading_quality -= _severity_penalty(findings, {"heading_as_container", "generic_section_ladder"})
    if metrics.heading_count and metrics.generic_heading_count == 0:
        heading_quality += 2
    heading_quality = _cap(heading_quality, 10)

    ending_strength = 7
    if _has_rule(analysis, "weak_ending"):
        ending_strength -= 5
    if any(word in (analysis.headings[-1].lower() if analysis.headings else "") for word in ("decide", "conversation", "next", "question", "consequence")):
        ending_strength += 3
    ending_strength = _cap(ending_strength, 10)

    template_risk_reversed = 10
    template_risk_reversed -= _severity_penalty(findings, {"generic_section_ladder", "generic_signposting", "fake_completeness", "weak_ending"})
    template_risk_reversed = _cap(template_risk_reversed, 10)

    dimensions = (
        ShapeDimensionScore("Reader fit", reader_fit, 15, "Checks whether the structure feels written to a real reader and situation."),
        ShapeDimensionScore("Intent fit", intent_fit, 15, "Checks whether the document shape fits what the piece is trying to cause."),
        ShapeDimensionScore("Structure originality", structure_originality, 15, "Penalizes inherited article/proposal ladders and generic containers."),
        ShapeDimensionScore("Judgment and prioritization", judgment, 15, "Rewards selective emphasis and penalizes fake completeness or equal-weight thinking."),
        ShapeDimensionScore("Rhythm naturalness", rhythm, 10, "Checks one-sentence paragraph rhythm, em dashes, and repeated formulas."),
        ShapeDimensionScore("Heading quality", heading_quality, 10, "Checks whether headings are situated moves rather than topic labels."),
        ShapeDimensionScore("Ending strength", ending_strength, 10, "Checks whether the ending creates a next step, decision, risk, question, or judgment."),
        ShapeDimensionScore("AI template risk", template_risk_reversed, 10, "Reversed score: higher means lower template risk."),
    )
    return ShapeScorecard(total=sum(d.score for d in dimensions), dimensions=dimensions)


def classify_ai_structure_risk(score: ShapeScorecard, analysis: ShapeRuleAnalysis) -> str:
    if any(f.rule == "generic_section_ladder" and f.severity == "high" for f in analysis.findings):
        return "High"
    if score.total >= 85:
        return "Low"
    if score.total >= 70:
        return "Low" if not any(f.severity in {"high", "severe"} for f in analysis.findings) else "Medium"
    if score.total >= 55:
        return "Medium"
    return "High"


def build_rewrite_instructions(report: ShapeReport) -> tuple[str, ...]:
    primary = report.recommended_archetypes[0]
    instructions = [
        f"Restructure the piece as a {primary.name}.",
        "Do not simply rename headings. Change the order, emphasis, and what is left unsaid.",
    ]
    lower_intent = report.intent.lower()
    if "curiosity" in lower_intent or "meeting" in lower_intent:
        instructions.extend([
            "Open with the specific observation, not market background or an executive summary.",
            "Collapse broad opportunity and transformation sections into one commercial tension.",
            "Do not close with a summary. Close with what the first conversation should decide.",
        ])
    if any(f.rule == "one_sentence_paragraph_overuse" for f in report.analysis.findings):
        instructions.append("Use one-sentence paragraphs only for real emphasis, not as the default rhythm.")
    if any(f.rule == "em_dash_overuse" for f in report.analysis.findings):
        instructions.append("Reduce decorative em dashes; prefer cleaner sentences, colons, commas, or full stops.")
    if any(f.rule == "repeated_contrast_formula" for f in report.analysis.findings):
        instructions.append("Use contrast formulas at most once; replace repeated not-X/but-Y turns with concrete judgment.")
    instructions.append("Keep the tone direct, senior, and specific. Frame the work as better editorial judgment and structure, not deception or AI-undetectability.")
    return tuple(instructions)


def run_shape(path: str | Path, task: str, reader: str = "", intent: str = "", channel: str = "") -> ShapeReport:
    draft_path = Path(path)
    text = draft_path.read_text(encoding="utf-8")
    analysis = analyze_shape_rules(text, task=task, reader=reader, intent=intent, channel=channel)
    score = score_shape(analysis, task=task, reader=reader, intent=intent)
    risk = classify_ai_structure_risk(score, analysis)
    archetypes = recommend_archetypes(task=task, reader=reader, intent=intent, channel=channel)
    placeholder = ShapeReport(
        path=draft_path,
        task=task,
        reader=reader,
        intent=intent,
        channel=channel,
        analysis=analysis,
        score=score,
        ai_structure_risk=risk,
        recommended_archetypes=archetypes,
        rewrite_instructions=(),
    )
    return ShapeReport(
        path=draft_path,
        task=task,
        reader=reader,
        intent=intent,
        channel=channel,
        analysis=analysis,
        score=score,
        ai_structure_risk=risk,
        recommended_archetypes=archetypes,
        rewrite_instructions=build_rewrite_instructions(placeholder),
    )


def _score_interpretation(total: int) -> str:
    if total >= 85:
        return "strong human architecture"
    if total >= 70:
        return "usable with minor structure polish"
    if total >= 55:
        return "clear but template like"
    if total >= 40:
        return "high AI structure risk"
    return "default AI document shape"


def render_shape_report(report: ShapeReport) -> str:
    lines: list[str] = ["# ProseKernel Shape Report", ""]
    lines.append("## Overall diagnosis")
    lines.append("")
    lines.append(f"AI structure risk: {report.ai_structure_risk}")
    lines.append(f"Shape score: {report.score.total}/100 — {_score_interpretation(report.score.total)}")
    if not report.reader or not report.intent:
        lines.append("Diagnosis certainty: lower because reader or intent was not supplied.")
    lines.append("")
    if report.ai_structure_risk == "High":
        lines.append("The draft is clear in places, but its architecture looks assembled from a default AI template. The issue is the document shape before sentence polish, not only the headings.")
    elif report.ai_structure_risk == "Medium":
        lines.append("The draft has usable material, but parts of the sequence and emphasis still feel template-like.")
    else:
        lines.append("The draft has a more situated shape: reader, intent, sequence, and emphasis are doing visible work.")
    lines.append("")

    lines.append("## Shape scorecard")
    for dimension in report.score.dimensions:
        lines.append(f"- {dimension.name}: {dimension.score}/{dimension.max_score} — {dimension.rationale}")
    lines.append("")

    lines.append("## Detected issues")
    if report.analysis.findings:
        for index, finding in enumerate(report.analysis.findings, start=1):
            evidence = f" Evidence: {finding.evidence}." if finding.evidence else ""
            lines.append(f"{index}. {finding.message} Severity: {finding.severity}.{evidence}")
    else:
        lines.append("- None")
    lines.append("")

    metrics = report.analysis.metrics
    lines.append("## Automatic metrics")
    lines.extend([
        f"- word count: {metrics.word_count}",
        f"- heading count: {metrics.heading_count}",
        f"- generic heading count: {metrics.generic_heading_count}",
        f"- paragraph count: {metrics.paragraph_count}",
        f"- one-sentence paragraph share: {metrics.one_sentence_paragraph_pct}%",
        f"- em dash count: {metrics.em_dash_count}",
        f"- repeated contrast formula count: {metrics.contrast_formula_count}",
        f"- generic signpost count: {metrics.signpost_count}",
    ])
    lines.append("")

    lines.append("## Recommended structure")
    primary = report.recommended_archetypes[0]
    lines.append("")
    lines.append(f"Use {primary.name}.")
    lines.append("")
    for index, step in enumerate(primary.shape, start=1):
        lines.append(f"{index}. {step}")
    if len(report.recommended_archetypes) > 1:
        alternatives = ", ".join(a.name for a in report.recommended_archetypes[1:])
        lines.append("")
        lines.append(f"Secondary option: {alternatives}.")
    lines.append("")

    lines.append("## Rewrite instructions for the agent")
    lines.append("")
    for instruction in report.rewrite_instructions:
        lines.append(f"- {instruction}")
    lines.append("")
    lines.append("No model call was made. This is a deterministic editorial architecture diagnostic, not a hard quality gate.")
    return "\n".join(lines).rstrip() + "\n"
