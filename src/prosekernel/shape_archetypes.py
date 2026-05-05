from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class StructureArchetype:
    name: str
    description: str
    shape: tuple[str, ...]
    best_for: tuple[str, ...]
    risk_if_misused: str


ARCHETYPES: tuple[StructureArchetype, ...] = (
    StructureArchetype(
        name="Direct Advisory Note",
        description="A senior, situated note for advising a decision maker without hiding the point.",
        shape=(
            "Why I am writing this",
            "What I think the real issue is",
            "What most people would do first",
            "Why I think that is not enough",
            "The path I would explore",
            "What we should decide in conversation",
        ),
        best_for=("business proposals", "strategic notes", "executive outreach", "advisory memos"),
        risk_if_misused="May sound too direct if the relationship is cold or formal.",
    ),
    StructureArchetype(
        name="Curiosity Proposal",
        description="A proposal that earns a meeting instead of trying to close the whole decision on paper.",
        shape=(
            "A quick observation",
            "The opportunity behind it",
            "Why this may matter for your company",
            "Three possible directions",
            "The one most worth discussing",
            "What I would like to explore with you",
        ),
        best_for=("founder outreach", "partnership proposals", "consulting introductions", "high-level business development"),
        risk_if_misused="Too little detail for a formal approval document.",
    ),
    StructureArchetype(
        name="Strategic Memo",
        description="A directional memo organized around leverage, options, tradeoffs, and recommendation.",
        shape=(
            "The core thesis",
            "The current constraint",
            "The leverage point",
            "The options",
            "The tradeoff",
            "The recommended move",
            "The open questions",
        ),
        best_for=("internal strategy", "investor memos", "product direction", "market thesis writing"),
        risk_if_misused="Can become too formal for a short note.",
    ),
    StructureArchetype(
        name="Founder Narrative",
        description="A build story that moves from frustration to insight to what changed.",
        shape=(
            "The frustration",
            "The thing I kept noticing",
            "The failed obvious solutions",
            "The sharper insight",
            "What I built",
            "What it changes",
            "Who should try it",
        ),
        best_for=("launch posts", "founder essays", "product storytelling", "open source announcements"),
        risk_if_misused="Can sound self-indulgent if it adds fake personal drama.",
    ),
    StructureArchetype(
        name="Decision Brief",
        description="A compact document for humans and agents that need to decide or act.",
        shape=(
            "Decision needed",
            "Recommendation",
            "Evidence",
            "Risks",
            "Rejected alternatives",
            "Next action",
        ),
        best_for=("agentic writing", "internal approvals", "ops decisions", "incident decisions", "product prioritization"),
        risk_if_misused="Too dry for public writing.",
    ),
    StructureArchetype(
        name="Market Thesis Note",
        description="A category argument that identifies a missed reading and who gains or loses power.",
        shape=(
            "The common reading",
            "What that reading misses",
            "The structural shift",
            "Who gains power",
            "Who loses power",
            "What to watch next",
        ),
        best_for=("Substack essays", "LinkedIn thought leadership", "investor analysis", "category commentary"),
        risk_if_misused="Can become too abstract without examples.",
    ),
    StructureArchetype(
        name="Technical Explainer with Judgment",
        description="A technical explainer that keeps a point of view instead of sounding like docs or marketing copy.",
        shape=(
            "The user problem",
            "The old way",
            "Why the old way breaks",
            "The new mechanism",
            "What changes in practice",
            "The limits",
            "Where to start",
        ),
        best_for=("developer tools", "AI infrastructure", "API products", "open source docs"),
        risk_if_misused="Can become too explanatory if there is no opinion.",
    ),
)


def archetype_by_name(name: str) -> StructureArchetype:
    for archetype in ARCHETYPES:
        if archetype.name == name:
            return archetype
    raise KeyError(name)


def recommend_archetypes(task: str = "", reader: str = "", intent: str = "", channel: str = "") -> tuple[StructureArchetype, ...]:
    """Recommend one or two situated structure archetypes from deterministic context clues."""
    haystack = " ".join([task, reader, intent, channel]).lower()
    selected: list[str] = []

    def add(name: str) -> None:
        if name not in selected:
            selected.append(name)

    if any(word in haystack for word in ("curiosity", "meeting", "conversation", "discuss", "outreach", "partnership")):
        add("Curiosity Proposal")
        if any(word in haystack for word in ("boss", "founder", "client", "executive", "senior", "company")):
            add("Direct Advisory Note")

    if any(word in haystack for word in ("boss", "founder", "client", "executive", "senior decision", "ceo")):
        add("Direct Advisory Note")

    if any(word in haystack for word in ("decide", "decision", "approval", "incident", "ops", "prioritization", "prioritize")):
        add("Decision Brief")
        add("Strategic Memo")

    if any(word in haystack for word in ("internal", "strategy", "strategic", "tradeoff", "direction", "memo")):
        add("Strategic Memo")

    if any(word in haystack for word in ("launch", "built", "founder narrative", "announcement", "open source")):
        add("Founder Narrative")

    if any(word in haystack for word in ("investor", "market thesis", "category", "trend", "structural shift", "power")):
        add("Market Thesis Note")

    if any(word in haystack for word in ("developer", "technical", "api", "tool", "infrastructure", "docs", "explain")):
        add("Technical Explainer with Judgment")

    if not selected:
        add("Strategic Memo")
        add("Direct Advisory Note")

    return tuple(archetype_by_name(name) for name in selected[:2])
