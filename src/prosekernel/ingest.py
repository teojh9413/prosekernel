from __future__ import annotations

from dataclasses import dataclass, asdict, field
from pathlib import Path
import re
from .patterns import KNOWN_PATTERN_IDS
from .taxonomy import CATEGORIES

RIGHTS = {"public-domain", "open-license", "short-excerpt", "metadata-only", "user-provided"}
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)

REQUIRED_SECTIONS = [
    "Source",
    "Why this is good",
    "Craft moves",
    "Structure map",
    "Excerpt or summary",
    "Reusable pattern",
    "Imitation prompt",
    "Anti-patterns to avoid",
]

@dataclass
class ExampleMetadata:
    title: str
    author: str
    source_url: str
    date_published: str
    added: str
    category: str
    format: str
    rights: str
    tags: list[str]
    quality_score: int
    use_when: str
    pattern_ids: list[str] = field(default_factory=list)

    def validate(self) -> list[str]:
        errors: list[str] = []
        if self.category not in CATEGORIES:
            errors.append(f"Unknown category: {self.category}")
        if self.rights not in RIGHTS:
            errors.append(f"Unknown rights value: {self.rights}")
        if not 1 <= int(self.quality_score) <= 10:
            errors.append("quality_score must be 1-10")
        if not self.source_url:
            errors.append("source_url is required")
        if len(self.tags) < 2:
            errors.append("at least two tags are required")
        if not self.pattern_ids:
            errors.append("at least one pattern_id is required")
        unknown_patterns = [pattern_id for pattern_id in self.pattern_ids if pattern_id not in KNOWN_PATTERN_IDS]
        if unknown_patterns:
            errors.append("Unknown pattern_ids: " + ", ".join(unknown_patterns))
        return errors


def slugify(text: str) -> str:
    text = text.lower().strip()
    text = re.sub(r"[^a-z0-9]+", "-", text)
    text = re.sub(r"-+", "-", text).strip("-")
    return text or "untitled"


def render_frontmatter(meta: ExampleMetadata) -> str:
    tags = "[" + ", ".join(meta.tags) + "]"
    lines = ["---"]
    data = asdict(meta)
    for key in ["title", "author", "source_url", "date_published", "added", "category", "format", "rights"]:
        lines.append(f'{key}: "{data[key]}"')
    lines.append(f"tags: {tags}")
    lines.append(f"quality_score: {meta.quality_score}")
    lines.append(f'use_when: "{meta.use_when}"')
    if meta.pattern_ids:
        lines.append("pattern_ids: [" + ", ".join(meta.pattern_ids) + "]")
    lines.append("---")
    return "\n".join(lines) + "\n\n"


def render_example(meta: ExampleMetadata) -> str:
    errors = meta.validate()
    if errors:
        raise ValueError("; ".join(errors))
    return render_frontmatter(meta) + f"""# {meta.title}

## Source
- Author: {meta.author}
- URL: {meta.source_url}
- Rights note: TODO

## Why this is good
TODO: Explain the specific craft value.

## Craft moves
- TODO: Move 1.
- TODO: Move 2.
- TODO: Move 3.

## Structure map
1. TODO
2. TODO
3. TODO

## Excerpt or summary
TODO: Store full text only when legally safe. Otherwise summarize.

## Reusable pattern
TODO: Generalize the move.

## Imitation prompt
TODO: Prompt an agent to transfer structure without copying wording.

## Anti-patterns to avoid
- TODO
"""


def example_path(root: Path, meta: ExampleMetadata) -> Path:
    return root / "library" / meta.category / "examples" / f"{slugify(meta.title)}.md"


def _frontmatter_pattern_ids(text: str) -> list[str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return []
    for line in match.group(1).splitlines():
        if line.startswith("pattern_ids:"):
            raw = line.split(":", 1)[1].strip()
            if raw.startswith("[") and raw.endswith("]"):
                return [item.strip().strip('"\'') for item in raw[1:-1].split(",") if item.strip()]
    return []


def validate_example_text(text: str) -> list[str]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        errors.append("missing YAML frontmatter")
    pattern_ids = _frontmatter_pattern_ids(text)
    if not pattern_ids:
        errors.append("missing frontmatter: pattern_ids")
    else:
        unknown_patterns = [pattern_id for pattern_id in pattern_ids if pattern_id not in KNOWN_PATTERN_IDS]
        if unknown_patterns:
            errors.append("unknown pattern_ids: " + ", ".join(unknown_patterns))
    for section in REQUIRED_SECTIONS:
        if f"## {section}" not in text:
            errors.append(f"missing section: {section}")
    return errors


def validate_library(root: Path) -> dict[str, list[str]]:
    issues: dict[str, list[str]] = {}
    for path in sorted((root / "library").glob("*/*/*.md")):
        errors = validate_example_text(path.read_text(encoding="utf-8"))
        if errors:
            issues[str(path.relative_to(root))] = errors
    return issues
