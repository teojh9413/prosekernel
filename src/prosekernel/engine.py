from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
import re
import shlex
from .evals import ScorecardReport, score_text
from .lint import LintReport, lint_text
from .patterns import PATTERN_FILES
from .providers import ProviderAdapter
from .retrieve import ExampleRecord, section_text, select_examples
from .taxonomy import recommend_categories

@dataclass
class WritingBrief:
    task: str
    retrieval_mode: str
    recommended_categories: list[str]
    examples: list[ExampleRecord]
    pattern_ids: list[str]
    pattern_instructions: list[str]
    craft_moves: list[str]
    agent_prompt: str


@dataclass
class WritingDemoResult:
    task: str
    retrieval_mode: str
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


@dataclass
class ProviderWriteResult:
    task: str
    provider: str
    model: str
    brief: WritingBrief
    draft: str
    lint_report: LintReport
    scorecard: ScorecardReport


@dataclass
class CritiqueResult:
    path: Path
    task: str
    retrieval_mode: str
    original_text: str
    recommended_categories: list[str]
    examples: list[ExampleRecord]
    pattern_ids: list[str]
    craft_moves: list[str]
    lint_report: LintReport
    scorecard: ScorecardReport
    revision_plan: list[str]


@dataclass
class RewriteResult:
    path: Path
    task: str
    retrieval_mode: str
    original_text: str
    rewritten_text: str
    recommended_categories: list[str]
    examples: list[ExampleRecord]
    pattern_ids: list[str]
    craft_moves: list[str]
    revision_plan: list[str]
    initial_lint_report: LintReport
    final_lint_report: LintReport
    initial_scorecard: ScorecardReport
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
    lines.append("You are drafting with ProseKernel, an open-source writing taste layer for AI agents.")
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
    lines.append("5. Score the draft before publishing with `prosekernel scorecard draft.md --task \"...\"`.")
    return "\n".join(lines).rstrip()


def build_writing_brief(root: Path, task: str, limit: int = 5, category: str | None = None, mode: str = "lexical") -> WritingBrief:
    examples = select_examples(root, task, limit=limit, category=category, mode=mode)
    pattern_ids = collect_pattern_ids(examples)
    craft_moves = extract_craft_moves(examples)
    pattern_instructions = pattern_agent_instructions(root, pattern_ids)
    prompt = build_agent_prompt(task, examples, pattern_ids, pattern_instructions, craft_moves)
    return WritingBrief(
        task=task,
        retrieval_mode=mode,
        recommended_categories=recommend_categories(task, limit=3),
        examples=examples,
        pattern_ids=pattern_ids,
        pattern_instructions=pattern_instructions,
        craft_moves=craft_moves,
        agent_prompt=prompt,
    )


def render_brief_report(brief: WritingBrief) -> str:
    lines: list[str] = []
    lines.append("# ProseKernel Writing Brief")
    lines.append("")
    lines.append(f"Task: {brief.task}")
    lines.append(f"Retrieval mode: {brief.retrieval_mode}")
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
    lines.append("- Run `prosekernel lint draft.md`.")
    lines.append(f"- Run `prosekernel scorecard draft.md --task \"{brief.task}\"`.")
    lines.append("- Revise until the draft has concrete proof, reader fit, and non-genericness.")
    return "\n".join(lines).rstrip() + "\n"


def revision_plan_from_reports(lint_report: LintReport, scorecard: ScorecardReport) -> list[str]:
    plan: list[str] = []
    weak_dimensions = [dimension for dimension in scorecard.dimensions if dimension.score / dimension.max_score < 0.65]
    for dimension in weak_dimensions:
        if dimension.name == "Specificity":
            plan.append("Replace abstract claims with concrete nouns, named situations, numbers, or constraints.")
        elif dimension.name == "Proof":
            plan.append("Add proof before importance claims: example, user consequence, observed behavior, number, or mechanism.")
        elif dimension.name == "Structure":
            plan.append("Make the structure visible with a reader problem, claim, proof, tradeoff, and next action.")
        elif dimension.name == "Reader fit":
            plan.append("Name the reader and their current moment before explaining the product or idea.")
        elif dimension.name == "Memorability":
            plan.append("Add one contrast, rule, or bottom-line sentence the reader can repeat.")
        elif dimension.name == "Non-genericness":
            plan.append("Cut sentences that could describe any other product, company, or topic.")
    for finding in lint_report.findings:
        if finding.rule == "slop_phrase":
            plan.append("Replace flagged AI-slop phrases with plain, testable language.")
        elif finding.rule in {"no_proof", "smart_sounding_empty", "vague_attribution"}:
            plan.append("Remove unsupported authority signals and add verifiable proof.")
        elif finding.rule == "weak_lead":
            plan.append("Rewrite the opener around the reader's concrete situation, not a generic trend.")
    if not plan:
        plan.append("Automated checks are acceptable; do a human pass for rhythm, compression, and source-safe originality.")
    deduped: list[str] = []
    seen: set[str] = set()
    for item in plan:
        if item not in seen:
            deduped.append(item)
            seen.add(item)
    return deduped[:7]


def run_critique(
    root: Path,
    path: Path,
    *,
    task: str = "",
    limit: int = 5,
    category: str | None = None,
    mode: str = "lexical",
) -> CritiqueResult:
    text = path.read_text(encoding="utf-8")
    examples = select_examples(root, task or text[:240], limit=limit, category=category, mode=mode)
    pattern_ids = collect_pattern_ids(examples)
    craft_moves = extract_craft_moves(examples)
    lint_report = lint_text(text)
    scorecard = score_text(text, task=task)
    return CritiqueResult(
        path=path,
        task=task,
        retrieval_mode=mode,
        original_text=text,
        recommended_categories=recommend_categories(task or text[:240], limit=3),
        examples=examples,
        pattern_ids=pattern_ids,
        craft_moves=craft_moves,
        lint_report=lint_report,
        scorecard=scorecard,
        revision_plan=revision_plan_from_reports(lint_report, scorecard),
    )


def render_critique_report(result: CritiqueResult) -> str:
    lines: list[str] = []
    lines.append("# ProseKernel Critique Report")
    lines.append("")
    lines.append(f"Draft: `{result.path}`")
    if result.task:
        lines.append(f"Task: {result.task}")
    lines.append(f"Retrieval mode: {result.retrieval_mode}")
    lines.append("")
    lines.append("> No model call was made. This critique uses deterministic ProseKernel lint, scorecard, retrieval, and pattern guidance.")
    lines.append("")
    lines.append("## Verdict")
    status = "PASS" if result.scorecard.passed else "REVISE"
    lines.append(f"Status: {status}")
    lines.append(f"Scorecard: {result.scorecard.total}/100")
    lines.append(f"Lint: {result.lint_report.score}/100")
    lines.append("")
    lines.append("## Scorecard")
    for dimension in result.scorecard.dimensions:
        lines.append(f"- {dimension.name}: {dimension.score}/{dimension.max_score} — {dimension.rationale}")
    lines.append("")
    lines.append("## Lint findings")
    if result.lint_report.findings:
        for finding in result.lint_report.findings:
            loc = f":{finding.line}" if finding.line else ""
            lines.append(f"- [{finding.severity.upper()}] {finding.rule}{loc}: {finding.message}")
    else:
        lines.append("- None")
    lines.append("")
    lines.append("## Revision plan")
    for item in result.revision_plan:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Retrieved examples")
    for example in result.examples:
        lines.append(f"- {example.title} — {example.category} — `{example.path}`")
        lines.append(f"  - Use when: {example.use_when}")
    lines.append("")
    lines.append("## Patterns to apply")
    for pattern_id in result.pattern_ids:
        lines.append(f"- `{pattern_id}`")
    if result.craft_moves:
        lines.append("")
        lines.append("Craft moves:")
        for move in result.craft_moves[:5]:
            lines.append(f"- {move}")
    lines.append("")
    lines.append("## Next command")
    command_parts = ["prosekernel", "rewrite", str(result.path)]
    if result.task:
        command_parts.extend(["--task", result.task])
    command_parts.extend(["--output", "rewrite.md"])
    lines.append(f"`{shlex.join(command_parts)}`")
    return "\n".join(lines).rstrip() + "\n"


def _compact_source_fact(text: str, limit: int = 180) -> str:
    clean = " ".join(text.strip().split())
    if not clean:
        return "Add one concrete fact from the source draft before publishing."
    sentence = re.split(r"(?<=[.!?])\s+", clean)[0]
    if len(sentence) < 80 and len(clean) > len(sentence):
        sentence = clean
    if len(sentence) <= limit:
        return sentence
    return sentence[: limit - 3].rstrip() + "..."


def rewrite_draft_deterministically(task: str, original_text: str, examples: list[ExampleRecord], craft_moves: list[str], revision_plan: list[str]) -> str:
    subject = _task_subject(task or "revise this draft")
    example_hint = examples[0].title if examples else "the strongest matching ProseKernel example"
    first_move = craft_moves[0] if craft_moves else "Lead with the reader's concrete problem."
    second_move = craft_moves[1] if len(craft_moves) > 1 else "Use proof before claims of importance."
    source_fact = _compact_source_fact(original_text)
    is_prosekernel_task = "prosekernel" in original_text.lower() or "prosekernel" in subject.lower()
    if is_prosekernel_task:
        claim = "ProseKernel gives an AI writing agent a visible editing loop: retrieve examples, apply named patterns, then score the draft before it ships."
        proof = "In a 3-step workflow, the agent can compare the draft against retrieved examples, cut flagged phrases, and revise weak sections around reader fit, proof, structure, and non-genericness."
    else:
        claim = f"For this task, the draft should give the reader a clear path through {subject}, not a polished generality."
        proof = f"Use the source fact as the anchor: {source_fact}"
    return f"""# Rewritten draft

Reader: you need the piece to answer the practical question before it tries to sound finished.

Problem: {subject} fails if it opens with generic importance. The reader needs the concrete situation, the constraint, and the next action.

Claim: {claim}

Proof: {proof}

Tradeoff: this is slower than instant polish, but it prevents the common failure mode: confident copy that could describe any product, policy, or workflow.

Next action: fix the highest-penalty line first, preserve the source facts, then publish only after the scorecard and human read-aloud pass.

Craft transfer:
- {first_move}
- {second_move}

Source pattern studied: {example_hint}
"""


def run_rewrite(
    root: Path,
    path: Path,
    *,
    task: str = "",
    limit: int = 5,
    category: str | None = None,
    mode: str = "lexical",
) -> RewriteResult:
    critique = run_critique(root, path, task=task, limit=limit, category=category, mode=mode)
    rewritten = rewrite_draft_deterministically(task, critique.original_text, critique.examples, critique.craft_moves, critique.revision_plan)
    final_lint = lint_text(rewritten)
    final_scorecard = score_text(rewritten, task=task)
    return RewriteResult(
        path=path,
        task=task,
        retrieval_mode=mode,
        original_text=critique.original_text,
        rewritten_text=rewritten,
        recommended_categories=critique.recommended_categories,
        examples=critique.examples,
        pattern_ids=critique.pattern_ids,
        craft_moves=critique.craft_moves,
        revision_plan=critique.revision_plan,
        initial_lint_report=critique.lint_report,
        final_lint_report=final_lint,
        initial_scorecard=critique.scorecard,
        final_scorecard=final_scorecard,
    )


def render_rewrite_report(result: RewriteResult) -> str:
    lines: list[str] = []
    lines.append("# ProseKernel Rewrite Report")
    lines.append("")
    lines.append(f"Source draft: `{result.path}`")
    if result.task:
        lines.append(f"Task: {result.task}")
    lines.append(f"Retrieval mode: {result.retrieval_mode}")
    lines.append("")
    lines.append("> No model call was made. This rewrite is deterministic and should be treated as a source-safe working draft, not final copy.")
    lines.append("")
    lines.append("## Quality delta")
    score_delta = result.final_scorecard.total - result.initial_scorecard.total
    lint_delta = result.final_lint_report.score - result.initial_lint_report.score
    lines.append(f"Scorecard: {result.initial_scorecard.total}/100 → {result.final_scorecard.total}/100 ({score_delta:+d})")
    lines.append(f"Lint: {result.initial_lint_report.score}/100 → {result.final_lint_report.score}/100 ({lint_delta:+d})")
    lines.append("")
    lines.append("## Revision plan used")
    for item in result.revision_plan:
        lines.append(f"- {item}")
    lines.append("")
    lines.append("## Rewritten draft")
    lines.append(result.rewritten_text.strip())
    lines.append("")
    lines.append("## Retrieved examples")
    for example in result.examples:
        lines.append(f"- {example.title} — {example.category} — `{example.path}`")
    lines.append("")
    lines.append("## Patterns applied")
    for pattern_id in result.pattern_ids:
        lines.append(f"- `{pattern_id}`")
    lines.append("")
    lines.append("## Quality gate")
    scorecard_command = ["prosekernel", "scorecard", "rewritten.md"]
    if result.task:
        scorecard_command.extend(["--task", result.task])
    lines.append(f"- Run `{shlex.join(scorecard_command)}`.")
    lines.append(f"- Run `{shlex.join(['prosekernel', 'lint', 'rewritten.md'])}`.")
    lines.append("- Do a human read-aloud pass for rhythm, compression, and factual proof.")
    return "\n".join(lines).rstrip() + "\n"


def run_provider_write(
    root: Path,
    task: str,
    *,
    provider_adapter: ProviderAdapter,
    limit: int = 5,
    category: str | None = None,
    mode: str = "lexical",
) -> ProviderWriteResult:
    brief = build_writing_brief(root, task, limit=limit, category=category, mode=mode)
    draft = provider_adapter.generate(brief.agent_prompt).strip()
    lint_report = lint_text(draft)
    scorecard = score_text(draft, task=task)
    return ProviderWriteResult(
        task=task,
        provider=provider_adapter.provider,
        model=provider_adapter.model,
        brief=brief,
        draft=draft,
        lint_report=lint_report,
        scorecard=scorecard,
    )


def render_provider_write_report(result: ProviderWriteResult) -> str:
    lines: list[str] = []
    lines.append("# ProseKernel Write Report")
    lines.append("")
    lines.append(f"Task: {result.task}")
    lines.append(f"Retrieval mode: {result.brief.retrieval_mode}")
    lines.append(f"Provider: {result.provider}")
    lines.append(f"Model: {result.model}")
    lines.append("")
    lines.append("> Model call completed only because an explicit provider and model were supplied.")
    lines.append("")
    lines.append("## Recommended categories")
    for category in result.brief.recommended_categories:
        lines.append(f"- {category}")
    lines.append("")
    lines.append("## Retrieved examples")
    for example in result.brief.examples:
        lines.append(f"- {example.title} — {example.category} — `{example.path}`")
    lines.append("")
    lines.append("## Patterns used")
    for pattern_id in result.brief.pattern_ids:
        lines.append(f"- `{pattern_id}`")
    lines.append("")
    lines.append("## Craft moves")
    for move in result.brief.craft_moves:
        lines.append(f"- {move}")
    lines.append("")
    lines.append("## Draft")
    lines.append(result.draft)
    lines.append("")
    lines.append("## Lint result")
    status = "PASS" if result.lint_report.passed else "FAIL"
    lines.append(f"ProseKernel lint score: {result.lint_report.score}/100 — {status}")
    if result.lint_report.findings:
        for finding in result.lint_report.findings:
            loc = f":{finding.line}" if finding.line else ""
            lines.append(f"- [{finding.severity.upper()}] {finding.rule}{loc}: {finding.message}")
    else:
        lines.append("No automated slop markers found.")
    lines.append("")
    lines.append("## Scorecard")
    lines.append(f"Total: {result.scorecard.total}/100")
    for dimension in result.scorecard.dimensions:
        lines.append(f"- {dimension.name}: {dimension.score}/{dimension.max_score} — {dimension.rationale}")
    lines.append("")
    lines.append("## Quality gate")
    lines.append("- If lint or scorecard is weak, revise before publishing.")
    lines.append("- Keep structure transfer; do not copy source phrases.")
    lines.append("- Add real proof before claims of importance.")
    return "\n".join(lines).rstrip() + "\n"


def draft_from_task(task: str, examples: list[ExampleRecord], craft_moves: list[str]) -> str:
    subject = _task_subject(task)
    first_move = craft_moves[0] if craft_moves else "Lead with the reader's concrete problem."
    second_move = craft_moves[1] if len(craft_moves) > 1 else "Make the structure visible before details."
    third_move = craft_moves[2] if len(craft_moves) > 2 else "Use one specific proof point before asking for action."
    source_line = "; ".join(f"{e.title} ({e.category})" for e in examples[:3])
    return f"""# ProseKernel demo draft

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


def run_writing_demo(root: Path, task: str, limit: int = 5, category: str | None = None, mode: str = "lexical") -> WritingDemoResult:
    examples = select_examples(root, task, limit=limit, category=category, mode=mode)
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
        retrieval_mode=mode,
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
    lines.append("# ProseKernel Retrieval + Writing Demo")
    lines.append("")
    lines.append(f"Task: {result.task}")
    lines.append(f"Retrieval mode: {result.retrieval_mode}")
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
