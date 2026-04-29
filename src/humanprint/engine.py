from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from .lint import LintReport, lint_text
from .retrieve import ExampleRecord, select_examples
from .taxonomy import recommend_categories

@dataclass
class WritingDemoResult:
    task: str
    recommended_categories: list[str]
    examples: list[ExampleRecord]
    pattern_ids: list[str]
    craft_moves: list[str]
    draft: str
    initial_report: LintReport
    rewrite: str
    final_report: LintReport


def extract_craft_moves(examples: list[ExampleRecord], limit: int = 7) -> list[str]:
    moves: list[str] = []
    seen: set[str] = set()
    for example in examples:
        for move in example.craft_moves:
            key = move.lower()
            if key not in seen:
                moves.append(move)
                seen.add(key)
            if len(moves) >= limit:
                return moves
    return moves


def collect_pattern_ids(examples: list[ExampleRecord], limit: int = 6) -> list[str]:
    pattern_ids: list[str] = []
    for example in examples:
        for pattern_id in example.pattern_ids:
            if pattern_id not in pattern_ids:
                pattern_ids.append(pattern_id)
            if len(pattern_ids) >= limit:
                return pattern_ids
    return pattern_ids


def _task_subject(task: str) -> str:
    clean = " ".join(task.strip().split())
    if len(clean) <= 90:
        return clean
    return clean[:87].rstrip() + "..."


def draft_from_task(task: str, examples: list[ExampleRecord], craft_moves: list[str]) -> str:
    subject = _task_subject(task)
    first_move = craft_moves[0] if craft_moves else "Lead with the reader's concrete problem."
    second_move = craft_moves[1] if len(craft_moves) > 1 else "Make the structure visible before details."
    third_move = craft_moves[2] if len(craft_moves) > 2 else "Use one specific proof point before asking for action."
    source_line = "; ".join(f"{e.title} ({e.category})" for e in examples[:3])
    return f"""# Humanprint demo draft

Task: {subject}

Reader problem: The reader needs a useful answer before they need polish. Start with the friction, name the decision, and show what changes next.

Draft:
You do not need more words for this piece. You need a sharper path.

Open with the specific tension: what is broken, delayed, misunderstood, or newly possible. Then make one claim the reader can test. If the piece asks for action, put the ask after the proof, not before it.

Use this structure:
1. Name the reader and the moment they are in.
2. State the concrete problem in one sentence.
3. Give one example, number, scene, or constraint.
4. Explain the tradeoff.
5. End with the next action.

Craft transfer:
- {first_move}
- {second_move}
- {third_move}

Source examples studied: {source_line}
"""


def rewrite_from_lint(draft: str, report: LintReport) -> str:
    if report.passed:
        return draft + "\nRevision note: passed automated anti-slop screen. Next edit: cut 10% and add real proof.\n"
    revised = draft
    replacements = {
        "leverage": "use",
        "unlock": "make possible",
        "seamless": "clear",
        "robust": "reliable",
        "transformative": "specific",
        "in conclusion": "Bottom line",
    }
    for old, new in replacements.items():
        revised = revised.replace(old, new).replace(old.title(), new.title())
    revised += "\nRevision note: removed flagged generic language; add named evidence before publishing.\n"
    return revised


def run_writing_demo(root: Path, task: str, limit: int = 5, category: str | None = None) -> WritingDemoResult:
    examples = select_examples(root, task, limit=limit, category=category)
    moves = extract_craft_moves(examples)
    pattern_ids = collect_pattern_ids(examples)
    draft = draft_from_task(task, examples, moves)
    initial = lint_text(draft)
    rewrite = rewrite_from_lint(draft, initial)
    final = lint_text(rewrite)
    return WritingDemoResult(
        task=task,
        recommended_categories=recommend_categories(task, limit=3),
        examples=examples,
        pattern_ids=pattern_ids,
        craft_moves=moves,
        draft=draft,
        initial_report=initial,
        rewrite=rewrite,
        final_report=final,
    )


def render_demo_report(result: WritingDemoResult) -> str:
    lines: list[str] = []
    lines.append("# Humanprint Retrieval + Writing Demo")
    lines.append("")
    lines.append(f"Task: {result.task}")
    lines.append("")
    lines.append("## Recommended categories")
    for category in result.recommended_categories:
        lines.append(f"- {category}")
    lines.append("")
    lines.append("## Retrieved examples")
    for example in result.examples:
        lines.append(f"- {example.title} — {example.category} — `{example.path}`")
    lines.append("")
    lines.append("## Patterns used")
    for pattern_id in result.pattern_ids:
        lines.append(f"- `{pattern_id}`")
    lines.append("")
    lines.append("## Craft moves to transfer")
    for move in result.craft_moves:
        lines.append(f"- {move}")
    lines.append("")
    lines.append("## Draft")
    lines.append(result.draft)
    lines.append("")
    lines.append("## Lint result")
    lines.append(f"Initial score: {result.initial_report.score}/100")
    lines.append(f"Final score: {result.final_report.score}/100")
    lines.append("")
    if result.final_report.findings:
        lines.append("Findings:")
        for finding in result.final_report.findings:
            lines.append(f"- {finding.severity}: {finding.rule} — {finding.message}")
    else:
        lines.append("No automated slop markers in final rewrite.")
    lines.append("")
    lines.append("## Rewrite")
    lines.append(result.rewrite)
    return "\n".join(lines).rstrip() + "\n"
