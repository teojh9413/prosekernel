from __future__ import annotations

from dataclasses import dataclass
from hashlib import sha256
from pathlib import Path
import re

from .evals import score_text
from .ingest import RIGHTS, slugify
from .lint import lint_text
from .patterns import KNOWN_PATTERN_IDS, infer_pattern_ids
from .taxonomy import CATEGORIES

PROMOTION_SAFE_RIGHTS = {"public-domain", "open-license", "user-provided"}
FRONTMATTER_RE = re.compile(r"\A---\n(.*?)\n---\n", re.S)
SOURCE_TEXT_HEADING_RE = re.compile(
    r"^#{1,6}\s+(source text|full source|original draft|source draft|original text|copied source)\b",
    re.M | re.I,
)
CONTROL_RE = re.compile(r"[\r\n\t\x00-\x08\x0b\x0c\x0e-\x1f]")


@dataclass(frozen=True)
class LearningLesson:
    task: str
    source_title: str
    source_author: str
    source_url: str
    rights: str
    category: str
    tags: list[str]
    pattern_ids: list[str]
    source_text_sha256: str
    source_word_count: int
    lint_score: int
    scorecard_total: int
    revision_lessons: list[str]
    promotion_status: str
    approved: bool = False


def _quote(value: str) -> str:
    return value.replace("\\", "\\\\").replace('"', '\\"')


def _yaml_list(values: list[str]) -> str:
    return "[" + ", ".join(f'"{_quote(value)}"' for value in values) + "]"


def _frontmatter_fields(text: str) -> dict[str, str]:
    match = FRONTMATTER_RE.match(text)
    if not match:
        return {}
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        if not line.strip() or ":" not in line:
            continue
        key, raw = line.split(":", 1)
        value = raw.strip()
        if value.startswith('"') and value.endswith('"'):
            value = value[1:-1].replace('\\"', '"').replace('\\\\', '\\')
        fields[key.strip()] = value
    return fields


def _validate_single_line(name: str, value: str, errors: list[str], max_len: int = 500) -> None:
    if not value.strip():
        errors.append(f"{name} is required")
    if CONTROL_RE.search(value):
        errors.append(f"{name} must be a single line")
    if len(value) > max_len:
        errors.append(f"{name} is too long")


def _word_count(text: str) -> int:
    return len(re.findall(r"\b[\w'-]+\b", text))


def _promotion_status(rights: str, approved: bool, promote: bool) -> str:
    if promote and approved and rights in PROMOTION_SAFE_RIGHTS:
        return "ready-for-human-review"
    if rights == "metadata-only":
        return "metadata-only-review"
    if rights == "short-excerpt":
        return "excerpt-review-required"
    return "lesson-only"


def validate_learning_request(
    *,
    source_title: str,
    source_author: str,
    source_url: str,
    rights: str,
    category: str,
    tags: list[str],
    pattern_ids: list[str],
    task: str = "",
    promote: bool = False,
    approved: bool = False,
) -> list[str]:
    errors: list[str] = []
    _validate_single_line("source_title", source_title, errors, max_len=240)
    _validate_single_line("source_author", source_author, errors, max_len=180)
    _validate_single_line("source_url", source_url, errors, max_len=500)
    if task:
        _validate_single_line("task", task, errors, max_len=500)
    for tag in tags:
        _validate_single_line("tag", tag, errors, max_len=80)
    for pattern_id in pattern_ids:
        _validate_single_line("pattern_id", pattern_id, errors, max_len=80)
    if rights not in RIGHTS:
        errors.append(f"unknown rights value: {rights}")
    if category not in CATEGORIES:
        errors.append(f"unknown category: {category}")
    if len(tags) < 2:
        errors.append("at least two tags are required")
    unknown_patterns = [pattern_id for pattern_id in pattern_ids if pattern_id not in KNOWN_PATTERN_IDS]
    if unknown_patterns:
        errors.append("unknown pattern_ids: " + ", ".join(unknown_patterns))
    if promote and not approved:
        errors.append("refusing promotion without --approved")
    if promote and approved and rights not in PROMOTION_SAFE_RIGHTS:
        errors.append("refusing promotion because rights are not public-domain, open-license, or user-provided")
    return errors


def build_learning_lesson(
    source_path: Path,
    *,
    task: str,
    source_title: str,
    source_author: str,
    source_url: str,
    rights: str,
    category: str,
    tags: list[str],
    pattern_ids: list[str] | None = None,
    promote: bool = False,
    approved: bool = False,
) -> LearningLesson:
    source_text = source_path.read_text(encoding="utf-8")
    selected_patterns = pattern_ids or list(infer_pattern_ids(category, tuple(tags), source_text))
    errors = validate_learning_request(
        source_title=source_title,
        source_author=source_author,
        source_url=source_url,
        rights=rights,
        category=category,
        tags=tags,
        pattern_ids=selected_patterns,
        task=task,
        promote=promote,
        approved=approved,
    )
    if errors:
        raise ValueError("; ".join(errors))

    lint_report = lint_text(source_text)
    scorecard = score_text(source_text, task=task)
    weak_dimensions = [dimension.name for dimension in scorecard.dimensions if dimension.score / dimension.max_score < 0.65]
    lessons: list[str] = []
    if weak_dimensions:
        lessons.append("Use this source as a diagnostic case for weak dimensions: " + ", ".join(weak_dimensions) + ".")
    if lint_report.findings:
        rules = []
        for finding in lint_report.findings:
            if finding.rule not in rules:
                rules.append(finding.rule)
        lessons.append("Convert flagged lint rules into reusable edits: " + ", ".join(rules[:5]) + ".")
    if not lessons:
        lessons.append("Preserve the structural lesson and verify it against future drafts without storing the source text.")
    lessons.append("Keep structure transfer only: metadata, critique, score deltas, and original analysis are allowed; copied source prose is not.")

    return LearningLesson(
        task=task,
        source_title=source_title,
        source_author=source_author,
        source_url=source_url,
        rights=rights,
        category=category,
        tags=tags,
        pattern_ids=selected_patterns,
        source_text_sha256=sha256(source_text.encode("utf-8")).hexdigest(),
        source_word_count=_word_count(source_text),
        lint_score=lint_report.score,
        scorecard_total=scorecard.total,
        revision_lessons=lessons,
        promotion_status=_promotion_status(rights, approved, promote),
        approved=approved,
    )


def render_learning_lesson(lesson: LearningLesson) -> str:
    tag_list = _yaml_list(lesson.tags)
    pattern_list = _yaml_list(lesson.pattern_ids)
    lines: list[str] = [
        "---",
        f'title: "Learning lesson — {_quote(lesson.source_title)}"',
        f'task: "{_quote(lesson.task)}"',
        f'source_title: "{_quote(lesson.source_title)}"',
        f'source_author: "{_quote(lesson.source_author)}"',
        f'source_url: "{_quote(lesson.source_url)}"',
        f'rights: "{_quote(lesson.rights)}"',
        f'category: "{_quote(lesson.category)}"',
        f"tags: {tag_list}",
        f"pattern_ids: {pattern_list}",
        "source_text_stored: false",
        f'source_text_sha256: "{lesson.source_text_sha256}"',
        f"source_word_count: {lesson.source_word_count}",
        f"lint_score: {lesson.lint_score}",
        f"scorecard_total: {lesson.scorecard_total}",
        f'promotion_status: "{lesson.promotion_status}"',
        f"approved: {str(lesson.approved).lower()}",
        "---",
        "",
        f"# Learning lesson — {lesson.source_title}",
        "",
        "## Source metadata",
        f"- Title: {lesson.source_title}",
        f"- Author/company: {lesson.source_author}",
        f"- URL: {lesson.source_url}",
        f"- Rights: {lesson.rights}",
        "- Source text stored: no",
        "",
        "## Reusable lesson",
    ]
    for item in lesson.revision_lessons:
        lines.append(f"- {item}")
    lines.extend([
        "",
        "## Safe learning record",
        f"- Task: {lesson.task}",
        f"- Category: {lesson.category}",
        f"- Tags: {', '.join(lesson.tags)}",
        f"- Pattern IDs: {', '.join(lesson.pattern_ids)}",
        f"- Lint score at import: {lesson.lint_score}/100",
        f"- Scorecard at import: {lesson.scorecard_total}/100",
        "- Stored content: metadata, hash, metrics, and original analysis only.",
        "",
        "## Promotion gate",
        f"- Status: {lesson.promotion_status}",
        "- Do not promote this note into a library example or pattern unless rights are reviewed and a human explicitly approves.",
        "- For modern copyrighted sources, promote only metadata, craft analysis, and structure maps; do not copy source prose.",
        "- If promoted to a pattern, write the pattern as an original abstraction and link back to source metadata.",
    ])
    return "\n".join(lines).rstrip() + "\n"


def default_learning_path(root: Path, lesson: LearningLesson) -> Path:
    return root / "learning" / "lessons" / f"{slugify(lesson.source_title)}.md"


def validate_learning_note_text(text: str) -> list[str]:
    errors: list[str] = []
    frontmatter = _frontmatter_fields(text)
    if not frontmatter:
        errors.append("missing YAML frontmatter")

    stored = frontmatter.get("source_text_stored")
    if stored and stored.lower() == "true":
        errors.append("source_text_stored must be false")
    if stored is None or stored.lower() != "false":
        errors.append("missing source_text_stored: false")

    for required in ("source_title", "source_author", "source_url", "rights", "promotion_status", "source_text_sha256"):
        if required not in frontmatter:
            errors.append(f"missing frontmatter: {required}")

    rights = frontmatter.get("rights", "").strip('"\'')
    promotion_status = frontmatter.get("promotion_status", "").strip('"\'')
    approved = frontmatter.get("approved", "false").strip('"\'').lower() == "true"
    if promotion_status == "ready-for-human-review":
        if rights not in PROMOTION_SAFE_RIGHTS:
            errors.append("ready-for-human-review requires safe rights")
        if not approved:
            errors.append("ready-for-human-review requires approved: true")

    if SOURCE_TEXT_HEADING_RE.search(text):
        errors.append("learning notes must not include source-text sections")
    if "## Promotion gate" not in text:
        errors.append("missing section: Promotion gate")
    if "## Reusable lesson" not in text:
        errors.append("missing section: Reusable lesson")
    return errors


def validate_learning_directory(root: Path) -> dict[str, list[str]]:
    issues: dict[str, list[str]] = {}
    for path in sorted((root / "learning" / "lessons").glob("*.md")):
        errors = validate_learning_note_text(path.read_text(encoding="utf-8"))
        if errors:
            issues[str(path.relative_to(root))] = errors
    return issues
