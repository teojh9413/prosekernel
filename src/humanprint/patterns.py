from __future__ import annotations

PATTERN_FILES: dict[str, str] = {
    "PATTERN_PROOF_001": "patterns/PATTERN_PROOF_001-specific-proof-ladder.md",
    "PATTERN_HOOK_001": "patterns/PATTERN_HOOK_001-portable-distinction.md",
    "PATTERN_EMAIL_001": "patterns/PATTERN_EMAIL_001-promised-cadence.md",
    "PATTERN_CRISIS_001": "patterns/PATTERN_CRISIS_001-impact-timeline-cause-prevention.md",
    "PATTERN_UX_001": "patterns/PATTERN_UX_001-actionable-recovery-microcopy.md",
    "PATTERN_STRATEGY_001": "patterns/PATTERN_STRATEGY_001-decision-grade-principles.md",
    "PATTERN_BRAND_001": "patterns/PATTERN_BRAND_001-worldview-positioning.md",
    "PATTERN_EXPLAIN_001": "patterns/PATTERN_EXPLAIN_001-progressive-disclosure.md",
    "PATTERN_SPEECH_001": "patterns/PATTERN_SPEECH_001-shared-principle-renewed-duty.md",
    "PATTERN_REPORTAGE_001": "patterns/PATTERN_REPORTAGE_001-scene-to-system-accountability.md",
    "PATTERN_INTERNAL_001": "patterns/PATTERN_INTERNAL_001-explicit-ownership-operating-doc.md",
    "PATTERN_PERSUASION_001": "patterns/PATTERN_PERSUASION_001-awareness-matched-argument.md",
}

KNOWN_PATTERN_IDS: tuple[str, ...] = tuple(PATTERN_FILES)

CATEGORY_DEFAULT_PATTERN_IDS: dict[str, tuple[str, ...]] = {
    "viral-social": ("PATTERN_HOOK_001",),
    "persuasive-copywriting": ("PATTERN_PERSUASION_001",),
    "strategic-intelligent": ("PATTERN_STRATEGY_001",),
    "essays-literary": ("PATTERN_EXPLAIN_001",),
    "technical-explanatory": ("PATTERN_EXPLAIN_001",),
    "brand-positioning": ("PATTERN_BRAND_001",),
    "email-newsletters": ("PATTERN_EMAIL_001",),
    "speeches-oratory": ("PATTERN_SPEECH_001",),
    "journalism-reportage": ("PATTERN_REPORTAGE_001",),
    "ux-product-microcopy": ("PATTERN_UX_001",),
    "crisis-communications": ("PATTERN_CRISIS_001",),
    "internal-ops-docs": ("PATTERN_INTERNAL_001",),
}

TAG_PATTERN_HINTS: tuple[tuple[tuple[str, ...], str], ...] = (
    (("proof", "specificity", "evidence", "data", "measurement", "case study"), "PATTERN_PROOF_001"),
    (("hook", "hooks", "distinction", "compression", "memorable-frame", "contrast"), "PATTERN_HOOK_001"),
    (("awareness", "sales", "offer", "cta", "direct-response", "problem-aware"), "PATTERN_PERSUASION_001"),
    (("newsletter", "welcome-email", "cadence", "briefing", "lifecycle"), "PATTERN_EMAIL_001"),
    (("incident", "outage", "postmortem", "trust-repair", "apology"), "PATTERN_CRISIS_001"),
    (("ux-writing", "microcopy", "error-message", "validation", "onboarding", "user-action"), "PATTERN_UX_001"),
    (("strategy", "tradeoffs", "decision-making", "principles", "memo", "market-thesis"), "PATTERN_STRATEGY_001"),
    (("brand", "positioning", "worldview", "category", "mission", "identity"), "PATTERN_BRAND_001"),
    (("docs", "documentation", "tutorial", "examples", "plain-language", "mental-model", "explanation"), "PATTERN_EXPLAIN_001"),
    (("speech", "rhetoric", "moral-argument", "cadence", "moral-frame"), "PATTERN_SPEECH_001"),
    (("reported-narrative", "immersion", "scene", "institutional-accountability"), "PATTERN_REPORTAGE_001"),
    (("dri", "ownership", "operating-system", "process"), "PATTERN_INTERNAL_001"),
)


def normalize_pattern_ids(raw: object) -> tuple[str, ...]:
    if raw is None:
        return ()
    if isinstance(raw, str):
        items = [item.strip().strip('"\'') for item in raw.split(",")]
    else:
        items = [str(item).strip().strip('"\'') for item in raw]  # type: ignore[arg-type]
    seen: list[str] = []
    for item in items:
        if item and item not in seen:
            seen.append(item)
    return tuple(seen)


def infer_pattern_ids(category: str, tags: list[str] | tuple[str, ...], text: str = "") -> tuple[str, ...]:
    """Return stable strict-pattern IDs for an example.

    Frontmatter can specify exact `pattern_ids`; this fallback keeps older
    examples retrievable while preserving deterministic, inspectable behavior.
    """
    selected: list[str] = list(CATEGORY_DEFAULT_PATTERN_IDS.get(category, ()))
    haystack = " ".join([category, " ".join(tags)]).lower()
    for needles, pattern_id in TAG_PATTERN_HINTS:
        if any(needle in haystack for needle in needles) and pattern_id not in selected:
            selected.append(pattern_id)
    return tuple(selected)
