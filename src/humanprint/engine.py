from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from .evals import ScorecardReport, score_text
from .lint import LintReport, lint_text
from .patterns import PATTERN_FILES
from .retrieve import ExampleRecord, section_text, select_examples
from .taxonomy import recommend_categories

@dataclass
class WritingBrief:
    task: str
    recommended_categories: list[str]
    examples: list[ExampleRecord]
    pattern_ids: list[str]
    pattern_instructions: list[str]
    craft_moves: list[str]
    agent_prompt: str


@dataclass
class WritingDemoResult:
    task: str
    recommended_categories: list[str]
    examples: list[ExampleRecord]
    pattern_ids: list[str]
    craft_moves: list[str]
    draft: str
    initial_report: LintReport
    initial_scorecard: ScorecardReport
    rewrite: str
    final_report: LintReport
    final_scorecard: ScorecardReport


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


def pattern_agent_instructions(root: Path, pattern_ids: list[str]) -> list[str]:
    instructions: list[str] = []
    for pattern_id in pattern_ids:
        rel = PATTERN_FILES.get(pattern_id)
        if not rel:
            continue
        path = root / rel
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        instruction = section_text(text, "Agent instruction")
        if instruction:
            instructions.append(f"{pattern_id}: {instruction}")
    return instructions


def build_agent_prompt(task: str, examples: list[ExampleRecord], pattern_ids: list[str], pattern_instructions: list[str], craft_moves: list[str]) -> str:
    lines: list[str] = []
    lines.append("You are drafting with Humanprint, an open-source writing taste layer for AI agents.")
    lines.append("")
    lines.append(f"Task: {task}")
    lines.append("")
    lines.append("Operating rules:")
    lines.append("- Do structure transfer, not phrase transfer.")
    lines.append("- Do not copy source phrases.")
    lines.append("- Lead with the reader's concrete situation before polish.")
    lines.append("- Use specific proof: names, numbers, examples, mechanisms, scenes, or constraints.")
    lines.append("- Avoid generic AI slop, fake significance, and unsupported certainty.")
    lines.append("")
    lines.append("Retrieved examples to study:")
    for example in examples:
        lines.append(f"- {example.title} [{example.category}] — use when: {example.use_when}")
    lines.append("")
    lines.append("Patterns to apply:")
    if pattern_instructions:
        for instruction in pattern_instructions:
            lines.append(f"- {instruction}")
    else:
        for pattern_id in pattern_ids:
            lines.append(f"- {pattern_id}")
    lines.append("")
    lines.append("Craft moves to transfer:")
    for move in craft_moves:
        lines.append(f"- {move}")
    lines.append("")
    lines.append("Drafting sequence:")
    lines.append("1. Name the reader and their current moment.")
    lines.append("2. Choose one primary pattern and make the structure visible.")
    lines.append("3. Draft with concrete proof before claims of importance.")
    lines.append("4. Cut any sentence that could describe any other product, company, or topic.")
    lines.append("5. Score the draft before publishing with `humanprint scorecard draft.md --task \"...\"`.")
    return "\n".join(lines).rstrip()


def build_writing_brief(root: Path, task: str, limit: int = 5, category: str | None = None) -> WritingBrief:
    examples = select_examples(root, task, limit=limit, category=category)
    pattern_ids = collect_pattern_ids(examples)
    craft_moves = extract_craft_moves(examples)
    pattern_instructions = pattern_agent_instructions(root, pattern_ids)
    prompt = build_agent_prompt(task, examples, pattern_ids, pattern_instructions, craft_moves)
    return WritingBrief(
        task=task,
        recommended_categories=recommend_categories(task, limit=3),
        examples=examples,
        pattern_ids=pattern_ids,
        pattern_instructions=pattern_instructions,
        craft_moves=craft_moves,
        agent_prompt=prompt,
    )


def render_brief_report(brief: WritingBrief) -> str:
    lines: list[str] = []
    lines.append("# Humanprint Writing Brief")
    lines.append("")
    lines.append(f"Task: {brief.task}")
    lines.append("")
    lines.append("> Dry-run mode: No model call was made. This report is a provider-agnostic brief for any AI agent or LLM adapter.")
    lines.append("")
    lines.append("## Recommended categories")
    for category in brief.recommended_categories:
        lines.append(f"- {category}")
    lines.append("")
    lines.append("## Retrieved examples")
    for example in brief.examples:
        lines.append(f"- {example.title} — {example.category} — `{example.path}`")
        lines.append(f"  - Use when: {example.use_when}")
        lines.append(f"  - Patterns: {', '.join(example.pattern_ids)}")
    lines.append("")
    lines.append("## Patterns to apply")
    for pattern_id in brief.pattern_ids:
        lines.append(f"- `{pattern_id}`")
    if brief.pattern_instructions:
        lines.append("")
        lines.append("Agent instructions:")
        for instruction in brief.pattern_instructions:
            lines.append(f"- {instruction}")
    lines.append("")
    lines.append("## Craft moves")
    for move in brief.craft_moves:
        lines.append(f"- {move}")
    lines.append("")
    lines.append("## Agent drafting prompt")
    lines.append("```text")
    lines.append(brief.agent_prompt)
    lines.append("```")
    lines.append("")
    lines.append("## Quality gate")
    lines.append("- Run `humanprint lint draft.md`.")
    lines.append(f"- Run `humanprint scorecard draft.md --task \"{brief.task}\"`.")
    lines.append("- Revise until the draft has concrete proof, reader fit, and non-genericness.")
    return "\n".join(lines).rstrip() + "\n"


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
    initial_scorecard = score_text(draft, task=task)
    rewrite = rewrite_from_lint(draft, initial)
    final = lint_text(rewrite)
    final_scorecard = score_text(rewrite, task=task)
    return WritingDemoResult(
        task=task,
        recommended_categories=recommend_categories(task, limit=3),
        examples=examples,
        pattern_ids=pattern_ids,
        craft_moves=moves,
        draft=draft,
        initial_report=initial,
        initial_scorecard=initial_scorecard,
        rewrite=rewrite,
        final_report=final,
        final_scorecard=final_scorecard,
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
    lines.append(f"Initial lint score: {result.initial_report.score}/100")
    lines.append(f"Final lint score: {result.final_report.score}/100")
    lines.append("")
    lines.append("## Score improvement")
    lines.append(f"Initial scorecard: {result.initial_scorecard.total}/100")
    lines.append(f"Final scorecard: {result.final_scorecard.total}/100")
    delta = result.final_scorecard.total - result.initial_scorecard.total
    lines.append(f"Scorecard delta: {delta:+d}")
    lines.append("")
    lines.append("Dimension movement:")
    initial_dims = {dimension.name: dimension for dimension in result.initial_scorecard.dimensions}
    for final_dim in result.final_scorecard.dimensions:
        initial_dim = initial_dims[final_dim.name]
        lines.append(f"- {final_dim.name}: {initial_dim.score}/{initial_dim.max_score} → {final_dim.score}/{final_dim.max_score}")
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
