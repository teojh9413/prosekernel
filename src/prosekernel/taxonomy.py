from __future__ import annotations

from dataclasses import dataclass
import re

CORE_CATEGORIES: tuple[str, ...] = (
    "viral-social",
    "persuasive-copywriting",
    "strategic-intelligent",
    "essays-literary",
    "technical-explanatory",
    "brand-positioning",
)

EXPANDED_CATEGORIES: tuple[str, ...] = (
    "email-newsletters",
    "speeches-oratory",
    "journalism-reportage",
    "ux-product-microcopy",
    "crisis-communications",
    "internal-ops-docs",
)

CATEGORIES: tuple[str, ...] = CORE_CATEGORIES + EXPANDED_CATEGORIES

CATEGORY_DESCRIPTIONS: dict[str, str] = {
    "viral-social": "Hooks, compression, rhythm, shareability, threads, short-form attention.",
    "persuasive-copywriting": "Landing pages, sales emails, desire, proof, objections, conversion.",
    "strategic-intelligent": "Memos, theses, investor logic, executive reasoning, tradeoffs.",
    "essays-literary": "Voice, clarity, scene, rhythm, argument, durable nonfiction craft.",
    "technical-explanatory": "Docs, tutorials, explainers, progressive disclosure, user education.",
    "brand-positioning": "Category framing, manifestos, memorable claims, worldview and identity.",
    "email-newsletters": "Launch emails, founder updates, lifecycle sequences, editorial newsletters.",
    "speeches-oratory": "Keynotes, public remarks, civic rhetoric, ceremonial and persuasive speech.",
    "journalism-reportage": "Profiles, interviews, reported narratives, investigations, field observation.",
    "ux-product-microcopy": "Onboarding, empty states, errors, labels, flows, support-adjacent product language.",
    "crisis-communications": "Apologies, incident notes, recalls, postmortems, trust repair under pressure.",
    "internal-ops-docs": "SOPs, decision records, internal memos, one-pagers, operating cadence docs.",
}

BLENDED_FORMATS: dict[str, tuple[str, ...]] = {
    "fundraising-investor-grants": ("strategic-intelligent", "persuasive-copywriting"),
    "customer-support-community-moderation": ("ux-product-microcopy", "crisis-communications"),
    "scripts-video-podcasts": ("essays-literary", "viral-social"),
    "academic-legal-policy": ("strategic-intelligent",),
    "sales-enablement-case-studies-whitepapers": ("persuasive-copywriting", "technical-explanatory"),
    "criticism-reviews-cultural-analysis": ("essays-literary", "journalism-reportage"),
}


CATEGORY_NEIGHBORS: dict[str, tuple[str, ...]] = {
    "email-newsletters": ("persuasive-copywriting", "brand-positioning", "essays-literary"),
    "speeches-oratory": ("essays-literary", "strategic-intelligent"),
    "journalism-reportage": ("essays-literary", "strategic-intelligent"),
    "ux-product-microcopy": ("technical-explanatory", "persuasive-copywriting"),
    "crisis-communications": ("strategic-intelligent", "technical-explanatory"),
    "internal-ops-docs": ("strategic-intelligent", "technical-explanatory"),
}

CATEGORY_KEYWORDS: dict[str, tuple[str, ...]] = {
    "viral-social": ("tweet", "thread", "viral", "post", "hook", "linkedin", "x ", "social", "share"),
    "persuasive-copywriting": ("landing", "sales", "conversion", "copy", "cta", "objection", "offer", "case study", "whitepaper"),
    "strategic-intelligent": ("memo", "strategy", "investor", "fundraising", "grant", "policy", "thesis", "market", "decision", "tradeoff"),
    "essays-literary": ("essay", "story", "narrative", "voice", "literary", "review", "criticism", "script", "podcast"),
    "technical-explanatory": ("docs", "documentation", "tutorial", "explain", "technical", "api", "guide", "whitepaper"),
    "brand-positioning": ("brand", "positioning", "tagline", "manifesto", "category", "slogan"),
    "email-newsletters": ("email", "newsletter", "lifecycle", "drip", "launch email", "founder update"),
    "speeches-oratory": ("speech", "keynote", "remarks", "talk", "oratory", "address"),
    "journalism-reportage": ("profile", "interview", "reported", "reportage", "journalism", "investigation", "feature"),
    "ux-product-microcopy": ("ux", "microcopy", "onboarding", "empty state", "error", "toast", "button", "tooltip", "support"),
    "crisis-communications": ("crisis", "apology", "incident", "outage", "postmortem", "recall", "trust", "moderation"),
    "internal-ops-docs": ("sop", "process", "internal", "ops", "operating", "decision record", "one-pager", "runbook"),
}

TOKEN_RE = re.compile(r"[a-z0-9]+")


def tokenize(text: str) -> set[str]:
    return set(TOKEN_RE.findall(text.lower()))


def category_score(task: str, category: str) -> int:
    haystack = f" {task.lower()} "
    score = 0
    for keyword in CATEGORY_KEYWORDS.get(category, ()): 
        if keyword in haystack:
            score += 3 if " " in keyword.strip() else 2
    # Also score direct token overlap with the category slug and description.
    task_tokens = tokenize(task)
    score += len(task_tokens & tokenize(category.replace("-", " ")))
    score += len(task_tokens & tokenize(CATEGORY_DESCRIPTIONS.get(category, "")))
    return score


def recommend_categories(task: str, limit: int = 3) -> list[str]:
    ranked = sorted(CATEGORIES, key=lambda c: (category_score(task, c), c), reverse=True)
    return [c for c in ranked if category_score(task, c) > 0][:limit] or ["essays-literary", "persuasive-copywriting", "technical-explanatory"][:limit]


def is_known_category(category: str) -> bool:
    return category in CATEGORIES


def expand_with_neighbors(categories: list[str] | tuple[str, ...]) -> tuple[str, ...]:
    expanded: list[str] = []
    for category in categories:
        if category not in expanded:
            expanded.append(category)
        for neighbor in CATEGORY_NEIGHBORS.get(category, ()):
            if neighbor not in expanded:
                expanded.append(neighbor)
    return tuple(expanded)
