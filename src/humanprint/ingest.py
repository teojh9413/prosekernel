from __future__ import annotations

from dataclasses import dataclass, asdict
from pathlib import Path
import re

CATEGORIES = {
    "viral-social",
    "persuasive-copywriting",
    "strategic-intelligent",
    "essays-literary",
    "technical-explanatory",
    "brand-positioning",
}

RIGHTS = {"public-domain", "open-license", "short-excerpt", "metadata-only", "user-provided"}

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


def validate_example_text(text: str) -> list[str]:
    errors: list[str] = []
    if not text.startswith("---\n"):
        errors.append("missing YAML frontmatter")
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
