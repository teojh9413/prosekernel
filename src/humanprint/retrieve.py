from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
from .taxonomy import CATEGORIES, expand_with_neighbors, recommend_categories, tokenize

FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
HEADING_RE = re.compile(r"^##\s+(.+?)\s*$", re.M)

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
    craft_moves: tuple[str, ...]
    summary: str

    @property
    def search_text(self) -> str:
        return " ".join([
            self.title, self.author, self.category, self.format, self.use_when,
            " ".join(self.tags), " ".join(self.craft_moves), self.summary,
        ])


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
        score += max(6, 18 - (category_rank * 2))
    score += example.quality_score
    # Nudge generally useful examples upward when direct overlap is sparse.
    if {"clarity", "specificity", "proof", "structure"} & set(example.tags):
        score += 2
    return score


def select_examples(root: Path, task: str, limit: int = 5, category: str | None = None) -> list[ExampleRecord]:
    examples = load_examples(root)
    if category:
        examples = [e for e in examples if e.category == category]
        preferred = (category,)
    else:
        preferred = expand_with_neighbors(recommend_categories(task, limit=3))
    ranked = sorted(examples, key=lambda e: (score_example(task, e, preferred), e.quality_score, e.title), reverse=True)
    return ranked[:limit]
