from __future__ import annotations

from dataclasses import dataclass
from functools import lru_cache
from pathlib import Path
import re
from .patterns import infer_pattern_ids, normalize_pattern_ids
from .taxonomy import CATEGORY_DESCRIPTIONS, CATEGORIES, expand_with_neighbors, recommend_categories, tokenize

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)

_RETRIEVAL_MODES = {"lexical", "semantic", "hybrid"}

# Phase 8 keeps retrieval stdlib/offline: these aliases approximate semantic intent
# without adding paid APIs, external embedding services, or heavyweight model deps.
CONCEPT_ALIASES: dict[str, tuple[str, ...]] = {
    "trust": ("confidence", "credibility", "reassurance", "belief", "safety", "rebuild", "repair"),
    "security": ("credential", "credentials", "compromise", "compromised", "breach", "attack", "incident", "risk", "host", "key"),
    "crisis": ("outage", "incident", "failure", "recall", "apology", "response", "postmortem", "remediation"),
    "decision": ("approve", "approver", "ownership", "accountability", "responsible", "roles", "alignment", "tradeoff"),
    "internal": ("ops", "process", "operating", "runbook", "handbook", "team", "workflow", "coordination"),
    "speech": ("address", "remarks", "oratory", "keynote", "public", "civic", "audience", "duty"),
    "journalism": ("reported", "reportage", "investigation", "profile", "scene", "witness", "accountability"),
    "email": ("newsletter", "digest", "cadence", "inbox", "subscriber", "update", "launch"),
    "ux": ("microcopy", "onboarding", "empty", "state", "error", "button", "interface", "flow"),
    "proof": ("evidence", "specific", "numbers", "examples", "mechanism", "facts", "documents"),
    "brand": ("positioning", "worldview", "category", "identity", "manifesto", "promise"),
    "technical": ("docs", "documentation", "api", "tutorial", "guide", "explain", "developer"),
}

CATEGORY_CONCEPTS: dict[str, tuple[str, ...]] = {
    "crisis-communications": ("crisis", "trust", "security", "proof"),
    "internal-ops-docs": ("internal", "decision", "proof"),
    "speeches-oratory": ("speech", "trust"),
    "journalism-reportage": ("journalism", "proof"),
    "email-newsletters": ("email",),
    "ux-product-microcopy": ("ux", "technical"),
    "brand-positioning": ("brand",),
    "technical-explanatory": ("technical", "proof"),
    "strategic-intelligent": ("decision", "proof"),
    "persuasive-copywriting": ("proof", "brand"),
    "viral-social": ("brand", "speech"),
    "essays-literary": ("speech", "journalism"),
}


@dataclass(frozen=True)
class ExampleRecord:
    path: Path
    title: str
    author: str
    source_url: str
    category: str
    format: str
    rights: str
    tags: tuple[str, ...]
    quality_score: int
    use_when: str
    pattern_ids: tuple[str, ...]
    craft_moves: tuple[str, ...]
    summary: str

    @property
    def search_text(self) -> str:
        return " ".join([
            self.title, self.author, self.category, self.format, self.use_when,
            " ".join(self.tags), " ".join(self.pattern_ids), " ".join(self.craft_moves), self.summary,
        ])


@dataclass(frozen=True)
class RetrievalMatch:
    example: ExampleRecord
    retrieval_mode: str
    lexical_score: int
    semantic_score: int
    hybrid_score: int
    preferred_categories: tuple[str, ...]


def _parse_value(raw: str):
    raw = raw.strip()
    if raw.startswith('"') and raw.endswith('"'):
        return raw[1:-1]
    if raw.startswith("[") and raw.endswith("]"):
        inner = raw[1:-1].strip()
        if not inner:
            return []
        return [item.strip().strip('"\'') for item in inner.split(",")]
    if raw.isdigit():
        return int(raw)
    return raw


def parse_frontmatter(text: str) -> dict[str, object]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    data: dict[str, object] = {}
    for line in match.group(1).splitlines():
        if ":" not in line:
            continue
        key, raw = line.split(":", 1)
        data[key.strip()] = _parse_value(raw)
    return data


def section_text(text: str, heading: str) -> str:
    matches = list(HEADING_RE.finditer(text))
    for idx, match in enumerate(matches):
        if match.group(1).strip().lower() == heading.lower():
            start = match.end()
            end = matches[idx + 1].start() if idx + 1 < len(matches) else len(text)
            return text[start:end].strip()
    return ""


def _bullets(section: str, limit: int = 5) -> tuple[str, ...]:
    lines: list[str] = []
    for line in section.splitlines():
        stripped = line.strip()
        if stripped.startswith("- "):
            lines.append(stripped[2:].strip())
        elif re.match(r"^\d+\.\s+", stripped):
            lines.append(re.sub(r"^\d+\.\s+", "", stripped).strip())
    if not lines and section:
        lines = [s.strip() for s in re.split(r"(?<=[.!?])\s+", section) if s.strip()]
    return tuple(lines[:limit])


def load_examples(root: Path) -> list[ExampleRecord]:
    examples: list[ExampleRecord] = []
    for path in sorted((root / "library").glob("*/examples/*.md")):
        text = path.read_text(encoding="utf-8")
        fm = parse_frontmatter(text)
        if not fm:
            continue
        craft = _bullets(section_text(text, "Craft moves"))
        summary = section_text(text, "Excerpt or summary") or section_text(text, "Why this is good")
        tags = fm.get("tags") or []
        if isinstance(tags, str):
            tags = [tags]
        pattern_ids = normalize_pattern_ids(fm.get("pattern_ids"))
        if not pattern_ids:
            pattern_ids = infer_pattern_ids(str(fm.get("category", path.parent.parent.name)), tuple(str(t) for t in tags), text)
        examples.append(ExampleRecord(
            path=path,
            title=str(fm.get("title", path.stem)),
            author=str(fm.get("author", "unknown")),
            source_url=str(fm.get("source_url", "")),
            category=str(fm.get("category", path.parent.parent.name)),
            format=str(fm.get("format", "unknown")),
            rights=str(fm.get("rights", "metadata-only")),
            tags=tuple(str(t) for t in tags),
            quality_score=int(fm.get("quality_score", 8)),
            use_when=str(fm.get("use_when", "")),
            pattern_ids=pattern_ids,
            craft_moves=craft,
            summary=summary[:800],
        ))
    return examples


def score_example(task: str, example: ExampleRecord, preferred_categories: tuple[str, ...] = ()) -> int:
    task_tokens = tokenize(task)
    example_tokens = tokenize(example.search_text)
    score = len(task_tokens & example_tokens) * 4
    if example.category in preferred_categories:
        category_rank = preferred_categories.index(example.category)
        # Prefer exact category hits strongly; neighbors are fallbacks, not replacements.
        score += 30 if category_rank == 0 else max(6, 18 - (category_rank * 2))
    score += example.quality_score
    if task_tokens & tokenize(" ".join(example.pattern_ids).replace("_", " ")):
        score += 3
    # Nudge generally useful examples upward when direct overlap is sparse.
    if {"clarity", "specificity", "proof", "structure"} & set(example.tags):
        score += 2
    return score


def _stem_token(token: str) -> str:
    for suffix in ("ications", "ication", "ments", "ing", "ers", "ies", "ed", "s"):
        if len(token) > len(suffix) + 3 and token.endswith(suffix):
            return token[: -len(suffix)]
    return token


@lru_cache(maxsize=2048)
def _semantic_token_tuple(text: str, category: str | None = None) -> tuple[str, ...]:
    base = tokenize(text)
    expanded = set(base)
    expanded.update(_stem_token(token) for token in base)
    lowered = f" {text.lower()} "

    for concept, aliases in CONCEPT_ALIASES.items():
        alias_tokens = {concept, *aliases}
        if base & tokenize(" ".join(alias_tokens)) or any(f" {alias.lower()} " in lowered for alias in aliases if " " in alias):
            expanded.add(concept)
            expanded.update(alias_tokens)

    if category:
        expanded.update(tokenize(category.replace("-", " ")))
        expanded.update(tokenize(CATEGORY_DESCRIPTIONS.get(category, "")))
        for concept in CATEGORY_CONCEPTS.get(category, ()):
            expanded.add(concept)
            expanded.update(CONCEPT_ALIASES.get(concept, ()))
    return tuple(sorted(expanded))


def semantic_tokens(text: str, category: str | None = None) -> set[str]:
    """Return cached lightweight expanded concept tokens for offline semantic matching."""
    return set(_semantic_token_tuple(text, category))


def semantic_score_example(task: str, example: ExampleRecord, preferred_categories: tuple[str, ...] = ()) -> int:
    task_tokens = semantic_tokens(task)
    example_tokens = semantic_tokens(example.search_text, category=example.category)
    overlap = task_tokens & example_tokens
    score = len(overlap) * 3

    # Reward concept/category alignment separately from raw lexical overlap.
    task_concepts = set(CONCEPT_ALIASES) & task_tokens
    example_concepts = set(CATEGORY_CONCEPTS.get(example.category, ())) | (set(CONCEPT_ALIASES) & example_tokens)
    score += len(task_concepts & example_concepts) * 8

    if example.category in preferred_categories:
        category_rank = preferred_categories.index(example.category)
        score += 12 if category_rank == 0 else max(3, 8 - category_rank)
    score += max(0, example.quality_score - 7)
    return score


def _validate_mode(mode: str) -> str:
    if mode not in _RETRIEVAL_MODES:
        raise ValueError(f"Unknown retrieval mode: {mode}. Expected one of: {', '.join(sorted(_RETRIEVAL_MODES))}")
    return mode


def rank_examples(
    root: Path,
    task: str,
    limit: int = 5,
    category: str | None = None,
    mode: str = "lexical",
) -> list[RetrievalMatch]:
    mode = _validate_mode(mode)
    examples = load_examples(root)
    if category:
        examples = [e for e in examples if e.category == category]
        preferred = (category,)
    else:
        preferred = expand_with_neighbors(recommend_categories(task, limit=3))

    matches: list[RetrievalMatch] = []
    for example in examples:
        lexical = score_example(task, example, preferred)
        semantic = semantic_score_example(task, example, preferred)
        hybrid = lexical + semantic
        matches.append(RetrievalMatch(
            example=example,
            retrieval_mode=mode,
            lexical_score=lexical,
            semantic_score=semantic,
            hybrid_score=hybrid,
            preferred_categories=preferred,
        ))

    if mode == "semantic":
        key = lambda match: (match.semantic_score, match.lexical_score, match.example.quality_score, match.example.title)
    elif mode == "hybrid":
        key = lambda match: (match.hybrid_score, match.lexical_score, match.semantic_score, match.example.quality_score, match.example.title)
    else:
        key = lambda match: (match.lexical_score, match.example.quality_score, match.example.title)
    return sorted(matches, key=key, reverse=True)[:limit]


def select_examples(
    root: Path,
    task: str,
    limit: int = 5,
    category: str | None = None,
    mode: str = "lexical",
) -> list[ExampleRecord]:
    return [match.example for match in rank_examples(root, task, limit=limit, category=category, mode=mode)]
