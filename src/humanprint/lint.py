from __future__ import annotations

from dataclasses import dataclass
import re
from pathlib import Path

SLOP_PHRASES = [
    "in today's fast-paced world",
    "ever-evolving landscape",
    "delve into",
    "unlock",
    "unleash",
    "leverage",
    "game-changer",
    "seamless",
    "robust",
    "cutting-edge",
    "revolutionary",
    "transformative",
    "at the end of the day",
    "low-hanging fruit",
    "synergy",
    "paradigm shift",
    "it is important to note",
    "needless to say",
    "in conclusion",
    "this article explores",
    "whether you're a beginner or an expert",
]

LEGACY_INFLATION = [
    "stands as",
    "serves as",
    "a testament to",
    "pivotal moment",
    "crucial role",
    "significant role",
    "key role",
    "underscores its importance",
    "reflects broader",
    "enduring legacy",
    "lasting legacy",
    "marking a shift",
    "shaping the future",
    "indelible mark",
]

SUPERFICIAL_ANALYSIS = [
    "highlighting",
    "underscoring",
    "emphasizing",
    "reflecting",
    "symbolizing",
    "contributing to",
    "fostering",
    "cultivating",
    "encompassing",
    "resonates with",
]

VAGUE_ATTRIBUTION_PATTERNS = [
    r"\bmany (experts|people|observers|critics) (believe|argue|say|suggest)\b",
    r"\bsome (experts|people|observers|critics) (believe|argue|say|suggest)\b",
    r"\bit is widely (believed|regarded|recognized)\b",
    r"\bresearch shows\b",
]

HEDGES = [
    "may", "might", "could", "perhaps", "arguably", "somewhat", "fairly",
    "rather", "quite", "very", "really", "basically", "generally", "typically",
]

WEAK_OPENERS = [
    "in this", "this article", "this post", "today we", "when it comes to",
    "as we all know", "in the realm of", "in an era", "with the rise of",
]

ABSTRACT_NOUNS = [
    "innovation", "efficiency", "productivity", "growth", "success", "quality",
    "value", "impact", "solution", "experience", "journey", "ecosystem",
]

@dataclass
class Finding:
    rule: str
    severity: str
    message: str
    line: int | None = None

@dataclass
class LintReport:
    score: int
    findings: list[Finding]

    @property
    def passed(self) -> bool:
        return self.score >= 80 and not any(f.severity == "error" for f in self.findings)


def _line_number(text: str, needle: str) -> int | None:
    idx = text.lower().find(needle.lower())
    if idx < 0:
        return None
    return text[:idx].count("\n") + 1


def lint_text(text: str) -> LintReport:
    findings: list[Finding] = []
    lowered = text.lower()

    for phrase in SLOP_PHRASES:
        if phrase in lowered:
            findings.append(Finding(
                rule="slop_phrase",
                severity="error",
                message=f"Banned AI-slop phrase: '{phrase}'. Replace with concrete language.",
                line=_line_number(text, phrase),
            ))

    for phrase in LEGACY_INFLATION:
        if phrase in lowered:
            findings.append(Finding(
                rule="legacy_inflation",
                severity="error",
                message=f"Unsupported significance/legacy phrase: '{phrase}'. Prove it or cut it.",
                line=_line_number(text, phrase),
            ))

    superficial_hits = [p for p in SUPERFICIAL_ANALYSIS if p in lowered]
    if len(superficial_hits) >= 3:
        findings.append(Finding(
            rule="superficial_analysis",
            severity="warning",
            message="Multiple vague analysis markers: " + ", ".join(superficial_hits[:8]) + ". Replace with mechanism or evidence.",
        ))

    for pat in VAGUE_ATTRIBUTION_PATTERNS:
        m = re.search(pat, lowered)
        if m:
            findings.append(Finding(
                rule="vague_attribution",
                severity="warning",
                message=f"Vague attribution: '{m.group(0)}'. Name who says it or remove the claim.",
                line=text[:m.start()].count("\n") + 1,
            ))

    paragraphs = [p.strip() for p in re.split(r"\n\s*\n", text) if p.strip()]
    if paragraphs:
        first = paragraphs[0].lower()
        if any(first.startswith(w) for w in WEAK_OPENERS):
            findings.append(Finding(
                rule="weak_lead",
                severity="error",
                message="Weak opener. Lead with the point, tension, proof, or a concrete scene.",
                line=1,
            ))
        if len(paragraphs[0].split()) > 80:
            findings.append(Finding(
                rule="bloated_lead",
                severity="warning",
                message="Opening paragraph is long. Make the lead sharper.",
                line=1,
            ))

    sentences = re.split(r"(?<=[.!?])\s+", text.strip()) if text.strip() else []
    long_sentences = [s for s in sentences if len(s.split()) > 32]
    if long_sentences:
        findings.append(Finding(
            rule="long_sentences",
            severity="warning",
            message=f"{len(long_sentences)} sentence(s) exceed 32 words. Split or cut.",
        ))

    hedge_count = sum(len(re.findall(rf"\b{re.escape(h)}\b", lowered)) for h in HEDGES)
    if hedge_count >= 8:
        findings.append(Finding(
            rule="hedging",
            severity="warning",
            message=f"Heavy hedging detected ({hedge_count} hedge words). Make claims or remove them.",
        ))

    abstract_hits = [a for a in ABSTRACT_NOUNS if re.search(rf"\b{re.escape(a)}\b", lowered)]
    if len(abstract_hits) >= 5:
        findings.append(Finding(
            rule="abstract_language",
            severity="warning",
            message="Too many abstract nouns: " + ", ".join(sorted(set(abstract_hits))) + ". Add examples, numbers, names, or scenes.",
        ))

    passive_matches = re.findall(r"\b(is|are|was|were|be|been|being)\s+\w+ed\b", lowered)
    if len(passive_matches) >= 5:
        findings.append(Finding(
            rule="passive_voice",
            severity="warning",
            message=f"Possible passive voice cluster ({len(passive_matches)} hits). Make agency explicit.",
        ))

    proof_markers = re.findall(r"\b\d+[\d,%$xkmb\.]*\b|for example|because|case study|customer|user|source|data", lowered)
    if len(text.split()) > 250 and len(proof_markers) < 2:
        findings.append(Finding(
            rule="no_proof",
            severity="error",
            message="Long draft with almost no proof markers. Add numbers, examples, names, or evidence.",
        ))

    score = 100
    for f in findings:
        score -= 15 if f.severity == "error" else 7
    score = max(0, score)
    return LintReport(score=score, findings=findings)


def lint_file(path: str | Path) -> LintReport:
    return lint_text(Path(path).read_text(encoding="utf-8"))
