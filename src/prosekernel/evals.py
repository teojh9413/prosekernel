from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re

from .lint import ABSTRACT_NOUNS, Finding, LintReport, SLOP_PHRASES, WEAK_OPENERS, lint_text
from .taxonomy import tokenize

SCORECARD_DIMENSIONS = (
    ("Specificity", 20),
    ("Proof", 20),
    ("Structure", 15),
    ("Reader fit", 15),
    ("Memorability", 15),
    ("Non-genericness", 15),
)

PROOF_MARKER_RE = re.compile(
    r"\b(\d+[\d,%$xkmb\.]*)\b|\b(for example|because|case study|customer|customers|user|users|source|data|test|tested|survey|observed|measured|found|shows|reported|according to|after|before)\b",
    re.I,
)
CONCRETE_MARKER_RE = re.compile(
    r"\b([A-Z][a-z]+(?:\s+[A-Z][a-z]+)*|\d+[\d,%$xkmb\.]*)\b"
)
READER_MARKER_RE = re.compile(r"\b(you|your|reader|customer|user|team|founder|operator|engineer|buyer|manager|maintainer)\b", re.I)
STRUCTURE_MARKER_RE = re.compile(r"(^#{1,3}\s+|^[-*]\s+|^\d+\.\s+|\b(first|second|third|then|next|finally|because|therefore|but|so)\b)", re.I | re.M)
MEMORABLE_MARKER_RE = re.compile(r"\b(not .* but|instead|versus|vs\.|tradeoff|rule|principle|bottom line|the point|remember|fingerprint)\b", re.I)


@dataclass(frozen=True)
class EvalMetrics:
    word_count: int
    sentence_count: int
    paragraph_count: int
    proof_marker_count: int
    concrete_marker_count: int
    abstract_noun_count: int
    slop_phrase_count: int
    weak_opener: bool
    long_sentence_count: int
    task_token_overlap: int


@dataclass(frozen=True)
class DimensionScore:
    name: str
    score: int
    max_score: int
    rationale: str


@dataclass(frozen=True)
class ScorecardReport:
    total: int
    dimensions: tuple[DimensionScore, ...]
    lint_report: LintReport
    metrics: EvalMetrics

    @property
    def passed(self) -> bool:
        return self.total >= 75 and self.lint_report.score >= 70 and not any(f.severity == "error" for f in self.lint_report.findings)


@dataclass(frozen=True)
class FixtureEvalResult:
    path: Path
    expected: str
    scorecard: ScorecardReport

    @property
    def passed(self) -> bool:
        if self.expected == "strong":
            return self.scorecard.total >= 75
        if self.expected == "weak":
            return self.scorecard.total < 75
        return False


def _sentences(text: str) -> list[str]:
    return [s.strip() for s in re.split(r"(?<=[.!?])\s+", text.strip()) if s.strip()]


def _paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]


def _cap(value: int, maximum: int) -> int:
    return max(0, min(maximum, value))


def collect_metrics(text: str, task: str = "") -> EvalMetrics:
    lowered = text.lower()
    sentences = _sentences(text)
    paragraphs = _paragraphs(text)
    words = re.findall(r"\b[\w'-]+\b", text)
    abstract_hits = sum(len(re.findall(rf"\b{re.escape(noun)}\b", lowered)) for noun in ABSTRACT_NOUNS)
    slop_hits = sum(lowered.count(phrase) for phrase in SLOP_PHRASES)
    first_paragraph = paragraphs[0].lower() if paragraphs else ""
    weak_opener = any(first_paragraph.startswith(opener) for opener in WEAK_OPENERS)
    long_sentences = [sentence for sentence in sentences if len(sentence.split()) > 32]
    task_overlap = len(tokenize(task) & tokenize(text)) if task else 0
    return EvalMetrics(
        word_count=len(words),
        sentence_count=len(sentences),
        paragraph_count=len(paragraphs),
        proof_marker_count=len(PROOF_MARKER_RE.findall(text)),
        concrete_marker_count=len(CONCRETE_MARKER_RE.findall(text)),
        abstract_noun_count=abstract_hits,
        slop_phrase_count=slop_hits,
        weak_opener=weak_opener,
        long_sentence_count=len(long_sentences),
        task_token_overlap=task_overlap,
    )


def score_text(text: str, task: str = "") -> ScorecardReport:
    lint = lint_text(text)
    metrics = collect_metrics(text, task)
    word_count = max(1, metrics.word_count)
    proof_density = metrics.proof_marker_count / max(1, word_count / 100)
    concrete_density = metrics.concrete_marker_count / max(1, word_count / 100)
    abstract_density = metrics.abstract_noun_count / max(1, word_count / 100)

    specificity = 7 + min(8, int(concrete_density * 1.2)) + min(5, metrics.proof_marker_count)
    specificity -= min(8, int(abstract_density))
    specificity -= 3 if metrics.slop_phrase_count else 0
    specificity = _cap(specificity, 20)

    if metrics.word_count < 80:
        # Microcopy and empty states cannot carry a full evidence chain, but they still need
        # at least one concrete constraint, example, or user-facing consequence.
        proof = 10 + min(7, metrics.proof_marker_count * 3)
    else:
        proof = 5 + min(12, int(proof_density * 4))
        proof += 3 if metrics.proof_marker_count >= 4 else 0
    if any(f.rule in {"no_proof", "smart_sounding_empty", "vague_attribution"} for f in lint.findings):
        proof -= 7
    proof = _cap(proof, 20)

    structure = 5 + min(5, metrics.paragraph_count * 2) + min(5, len(STRUCTURE_MARKER_RE.findall(text)) // 2)
    structure -= 4 if metrics.weak_opener else 0
    structure -= min(3, metrics.long_sentence_count)
    structure = _cap(structure, 15)

    reader_fit = 5 + min(5, len(READER_MARKER_RE.findall(text))) + min(5, metrics.task_token_overlap)
    if not task and len(READER_MARKER_RE.findall(text)) >= 2:
        reader_fit += 2
    if metrics.weak_opener:
        reader_fit -= 3
    reader_fit = _cap(reader_fit, 15)

    memorability = 4 + min(5, len(MEMORABLE_MARKER_RE.findall(text)) * 2) + min(3, text.count(":"))
    memorability += 3 if any(6 <= len(sentence.split()) <= 14 for sentence in _sentences(text)) else 0
    memorability += 3 if "Button:" in text else 0
    memorability -= 2 if metrics.slop_phrase_count else 0
    memorability = _cap(memorability, 15)

    non_generic = 7 + min(4, metrics.task_token_overlap) + min(4, metrics.proof_marker_count)
    non_generic -= min(8, metrics.slop_phrase_count * 2 + max(0, metrics.abstract_noun_count - 3))
    if any(f.rule == "smart_sounding_empty" for f in lint.findings):
        non_generic -= 6
    non_generic = _cap(non_generic, 15)

    dimensions = (
        DimensionScore("Specificity", specificity, 20, _specificity_rationale(metrics)),
        DimensionScore("Proof", proof, 20, _proof_rationale(metrics, lint.findings)),
        DimensionScore("Structure", structure, 15, _structure_rationale(metrics)),
        DimensionScore("Reader fit", reader_fit, 15, _reader_fit_rationale(metrics, bool(task))),
        DimensionScore("Memorability", memorability, 15, _memorability_rationale(text)),
        DimensionScore("Non-genericness", non_generic, 15, _non_generic_rationale(metrics, lint.findings)),
    )
    total = sum(d.score for d in dimensions)
    return ScorecardReport(total=total, dimensions=dimensions, lint_report=lint, metrics=metrics)


def _specificity_rationale(metrics: EvalMetrics) -> str:
    return f"{metrics.concrete_marker_count} concrete markers, {metrics.abstract_noun_count} abstract noun hits."


def _proof_rationale(metrics: EvalMetrics, findings: list[Finding]) -> str:
    penalties = [f.rule for f in findings if f.rule in {"no_proof", "smart_sounding_empty", "vague_attribution"}]
    suffix = f" Penalties: {', '.join(penalties)}." if penalties else ""
    return f"{metrics.proof_marker_count} proof markers found.{suffix}"


def _structure_rationale(metrics: EvalMetrics) -> str:
    opener = " weak opener" if metrics.weak_opener else " no weak opener"
    return f"{metrics.paragraph_count} paragraph(s), {metrics.long_sentence_count} long sentence(s),{opener}."


def _reader_fit_rationale(metrics: EvalMetrics, has_task: bool) -> str:
    task_note = f" task overlap {metrics.task_token_overlap}" if has_task else " no task supplied"
    return f"Reader markers plus{task_note}."


def _memorability_rationale(text: str) -> str:
    marker_count = len(MEMORABLE_MARKER_RE.findall(text))
    return f"{marker_count} contrast/rule/memory marker(s)."


def _non_generic_rationale(metrics: EvalMetrics, findings: list[Finding]) -> str:
    empty = any(f.rule == "smart_sounding_empty" for f in findings)
    return f"Task overlap {metrics.task_token_overlap}; slop phrases {metrics.slop_phrase_count}; smart-empty={empty}."


def render_scorecard_report(report: ScorecardReport, title: str = "ProseKernel Scorecard") -> str:
    lines = [f"# {title}", "", f"Total score: {report.total}/100", f"Lint score: {report.lint_report.score}/100", f"Status: {'PASS' if report.passed else 'REVISE'}", ""]
    lines.append("## Dimension scores")
    for dimension in report.dimensions:
        lines.append(f"- {dimension.name}: {dimension.score}/{dimension.max_score} — {dimension.rationale}")
    lines.append("")
    lines.append("## Automatic metrics")
    metrics = report.metrics
    lines.extend([
        f"- word count: {metrics.word_count}",
        f"- sentence count: {metrics.sentence_count}",
        f"- paragraph count: {metrics.paragraph_count}",
        f"- proof marker count: {metrics.proof_marker_count}",
        f"- abstract noun count: {metrics.abstract_noun_count}",
        f"- slop phrase count: {metrics.slop_phrase_count}",
        f"- long sentence count: {metrics.long_sentence_count}",
    ])
    lines.append("")
    lines.append("## Lint findings")
    if not report.lint_report.findings:
        lines.append("- None")
    else:
        for finding in report.lint_report.findings:
            lines.append(f"- {finding.severity}: {finding.rule} — {finding.message}")
    return "\n".join(lines).rstrip() + "\n"


def evaluate_fixtures(root: Path) -> list[FixtureEvalResult]:
    fixture_root = root / "evals" / "fixtures"
    results: list[FixtureEvalResult] = []
    for expected in ("weak", "strong"):
        for path in sorted((fixture_root / expected).glob("*.md")):
            task = path.stem.replace("-", " ")
            report = score_text(path.read_text(encoding="utf-8"), task=task)
            results.append(FixtureEvalResult(path=path, expected=expected, scorecard=report))
    return results


def render_fixture_eval_report(results: list[FixtureEvalResult], root: Path) -> str:
    lines = ["# ProseKernel Fixture Eval", ""]
    passed = sum(1 for result in results if result.passed)
    lines.append(f"Passed: {passed}/{len(results)}")
    lines.append("")
    for result in results:
        rel = result.path.relative_to(root) if result.path.is_relative_to(root) else result.path
        verdict = "PASS" if result.passed else "FAIL"
        lines.append(f"- {verdict} {rel} expected={result.expected} score={result.scorecard.total}/100 lint={result.scorecard.lint_report.score}/100")
    return "\n".join(lines).rstrip() + "\n"
