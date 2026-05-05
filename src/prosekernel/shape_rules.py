from __future__ import annotations

from dataclasses import dataclass
import re


GENERIC_HEADINGS = {
    "introduction",
    "overview",
    "executive summary",
    "background",
    "market opportunity",
    "problem statement",
    "solution",
    "proposed solution",
    "proposed solutions",
    "key benefits",
    "benefits",
    "challenges",
    "implementation roadmap",
    "roadmap",
    "future outlook",
    "conclusion",
    "key takeaways",
}

GENERIC_SIGNPOSTS = (
    "in today's rapidly evolving landscape",
    "it is important to note that",
    "this highlights the importance of",
    "there are several key",
    "in conclusion",
    "ultimately",
    "furthermore",
    "moreover",
    "additionally",
    "this underscores",
    "this represents a significant opportunity",
)

WEAK_ENDING_PHRASES = (
    "in conclusion",
    "to summarize",
    "overall",
    "ultimately, this shows",
    "the future of",
    "is bright",
    "by embracing",
    "companies can",
    "position themselves for the future",
)

SITUATION_MARKERS = (
    "you",
    "your",
    "company",
    "team",
    "reader",
    "decision",
    "meeting",
    "conversation",
    "merchant",
    "customer",
    "client",
    "founder",
    "boss",
    "operator",
    "current business",
    "now",
    "first conversation",
)


@dataclass(frozen=True)
class ShapeFinding:
    rule: str
    severity: str
    message: str
    evidence: str = ""


@dataclass(frozen=True)
class ShapeMetrics:
    word_count: int
    heading_count: int
    generic_heading_count: int
    paragraph_count: int
    one_sentence_paragraph_count: int
    one_sentence_paragraph_pct: int
    em_dash_count: int
    contrast_formula_count: int
    signpost_count: int
    section_word_counts: tuple[int, ...]


@dataclass(frozen=True)
class ShapeRuleAnalysis:
    findings: tuple[ShapeFinding, ...]
    metrics: ShapeMetrics
    headings: tuple[str, ...]


def extract_headings(text: str) -> tuple[str, ...]:
    headings: list[str] = []
    for line in text.splitlines():
        match = re.match(r"^#{1,3}\s+(.+?)\s*$", line)
        if match:
            heading = re.sub(r"\s+#+\s*$", "", match.group(1)).strip()
            headings.append(heading)
    return tuple(headings)


def normalize_heading(heading: str) -> str:
    heading = heading.strip().lower()
    heading = re.sub(r"[^a-z0-9\s?]", "", heading)
    heading = re.sub(r"\s+", " ", heading)
    return heading.strip()


def _paragraphs(text: str) -> list[str]:
    raw = [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]
    return [p for p in raw if not p.lstrip().startswith("#") and not p.lstrip().startswith("```")]


def _sentences(paragraph: str) -> list[str]:
    cleaned = re.sub(r"\s+", " ", paragraph.strip())
    if not cleaned:
        return []
    parts = [s.strip() for s in re.split(r"(?<=[.!?])\s+", cleaned) if s.strip()]
    return parts or [cleaned]


def _section_word_counts(text: str) -> tuple[int, ...]:
    sections: list[list[str]] = []
    current: list[str] = []
    for line in text.splitlines():
        if re.match(r"^#{1,3}\s+", line):
            if current:
                sections.append(current)
            current = []
            continue
        current.append(line)
    if current:
        sections.append(current)
    counts = []
    for section in sections:
        body = "\n".join(section)
        word_count = len(re.findall(r"\b[\w'-]+\b", body))
        if word_count:
            counts.append(word_count)
    return tuple(counts)


def _count_contrast_formulas(text: str) -> int:
    patterns = (
        r"\bnot\b[^.!?]{0,80}\bbut\b",
        r"\bnot\b[^.!?]{0,80}\.\s*\b(it|this)\s+is\b",
        r"\bnot\s+about\b[^.!?]{0,80}\.\s*\b(it|this)\s+is\s+about\b",
        r"\bthe\s+question\s+is\s+not\b[^.!?]{0,120}\.\s*\bthe\s+question\s+is\b",
    )
    lowered = text.lower()
    return sum(len(re.findall(pattern, lowered, flags=re.I | re.S)) for pattern in patterns)


def _generic_heading_hits(headings: tuple[str, ...]) -> list[str]:
    hits: list[str] = []
    for heading in headings:
        normalized = normalize_heading(heading)
        if normalized in GENERIC_HEADINGS or normalized.startswith("what is ") or normalized.startswith("why ") and normalized.endswith(" matters"):
            hits.append(heading)
    return hits


def analyze_shape_rules(text: str, task: str = "", reader: str = "", intent: str = "", channel: str = "") -> ShapeRuleAnalysis:
    headings = extract_headings(text)
    generic_hits = _generic_heading_hits(headings)
    paragraphs = _paragraphs(text)
    one_sentence = [p for p in paragraphs if len(_sentences(p)) == 1]
    one_sentence_pct = round((len(one_sentence) / len(paragraphs)) * 100) if paragraphs else 0
    em_dash_count = text.count("—")
    contrast_count = _count_contrast_formulas(text)
    lowered = text.lower()
    signpost_hits = [phrase for phrase in GENERIC_SIGNPOSTS if phrase in lowered]
    section_counts = _section_word_counts(text)
    findings: list[ShapeFinding] = []

    if generic_hits:
        if len(generic_hits) >= 5:
            severity = "high"
        elif len(generic_hits) >= 3:
            severity = "medium"
        else:
            severity = "low"
        proposal_markers = {"Executive Summary", "Market Opportunity", "Proposed Solutions", "Implementation Roadmap"}
        ladder_type = "generic proposal ladder" if proposal_markers & set(generic_hits) else "generic article ladder"
        findings.append(ShapeFinding(
            rule="generic_section_ladder",
            severity=severity,
            message=f"Detected a {ladder_type}: {', '.join(generic_hits)}. The issue is the default AI document shape, not only the heading names.",
            evidence=", ".join(generic_hits),
        ))

    if len(section_counts) >= 4:
        nonzero = [count for count in section_counts if count > 0]
        if len(nonzero) >= 4:
            medianish = sorted(nonzero)[len(nonzero) // 2]
            narrow = [count for count in nonzero if abs(count - medianish) <= max(20, int(medianish * 0.35))]
            if len(narrow) >= 4:
                findings.append(ShapeFinding(
                    rule="symmetrical_section_rhythm",
                    severity="warning",
                    message="The sections have unusually even weight. Human writing usually varies emphasis based on judgment.",
                    evidence=", ".join(str(count) for count in section_counts),
                ))

    if one_sentence_pct >= 40:
        if one_sentence_pct >= 75:
            severity = "severe"
        elif one_sentence_pct >= 60:
            severity = "high"
        else:
            severity = "warning"
        findings.append(ShapeFinding(
            rule="one_sentence_paragraph_overuse",
            severity=severity,
            message="Too many one sentence paragraphs. This creates the default AI dramatic rhythm.",
            evidence=f"{len(one_sentence)}/{len(paragraphs)} paragraphs ({one_sentence_pct}%)",
        ))

    if em_dash_count > 3:
        if em_dash_count > 10:
            severity = "severe"
        elif em_dash_count > 6:
            severity = "high"
        else:
            severity = "warning"
        findings.append(ShapeFinding(
            rule="em_dash_overuse",
            severity=severity,
            message="Frequent em dashes can make the prose feel AI polished rather than naturally written.",
            evidence=str(em_dash_count),
        ))

    if contrast_count > 1:
        findings.append(ShapeFinding(
            rule="repeated_contrast_formula",
            severity="warning",
            message="Repeated not-X/but-Y contrast formulas become obvious AI writing when reused.",
            evidence=str(contrast_count),
        ))

    if signpost_hits:
        findings.append(ShapeFinding(
            rule="generic_signposting",
            severity="warning" if len(signpost_hits) < 3 else "high",
            message="Generic signposting makes the piece sound assembled instead of situated.",
            evidence=", ".join(signpost_hits),
        ))

    if intent and "curiosity" in intent.lower() and len(headings) > 7:
        findings.append(ShapeFinding(
            rule="fake_completeness",
            severity="warning",
            message="The draft may be trying to close the entire argument on paper. For this intent, leave more for the conversation.",
            evidence=f"{len(headings)} major headings",
        ))

    ending_source = "\n\n".join(paragraphs[-2:]).lower() if paragraphs else lowered[-500:]
    if any(phrase in ending_source for phrase in WEAK_ENDING_PHRASES):
        findings.append(ShapeFinding(
            rule="weak_ending",
            severity="warning",
            message="The ending mostly summarizes or gestures at a generic future. Strong endings create a decision, next step, consequence, question, or sharper judgment.",
            evidence=ending_source[:180].replace("\n", " "),
        ))

    container_hits = [heading for heading in headings if normalize_heading(heading) in GENERIC_HEADINGS]
    if container_hits:
        findings.append(ShapeFinding(
            rule="heading_as_container",
            severity="warning",
            message="Several headings are containers rather than situated claims. Do not simply rewrite them as thesis sentences; ask whether each section belongs in that position.",
            evidence=", ".join(container_hits),
        ))

    context_terms = set(re.findall(r"\b[a-z][a-z0-9'-]+\b", " ".join([reader, task, intent]).lower()))
    useful_context_terms = {term for term in context_terms if len(term) > 3 and term not in {"create", "proposal", "meeting", "intent", "task"}}
    situated_hits = [marker for marker in SITUATION_MARKERS if re.search(rf"\b{re.escape(marker)}\b", lowered)]
    if useful_context_terms:
        situated_hits.extend(term for term in useful_context_terms if re.search(rf"\b{re.escape(term)}\b", lowered))
    if not situated_hits:
        findings.append(ShapeFinding(
            rule="lack_of_situated_reader",
            severity="warning",
            message="The piece does not feel written to a specific situation. It may read like a generic AI article.",
            evidence="No reader, company, scenario, decision, or context marker found.",
        ))

    metrics = ShapeMetrics(
        word_count=len(re.findall(r"\b[\w'-]+\b", text)),
        heading_count=len(headings),
        generic_heading_count=len(generic_hits),
        paragraph_count=len(paragraphs),
        one_sentence_paragraph_count=len(one_sentence),
        one_sentence_paragraph_pct=one_sentence_pct,
        em_dash_count=em_dash_count,
        contrast_formula_count=contrast_count,
        signpost_count=len(signpost_hits),
        section_word_counts=section_counts,
    )
    return ShapeRuleAnalysis(findings=tuple(findings), metrics=metrics, headings=headings)
