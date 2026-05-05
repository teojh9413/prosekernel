from __future__ import annotations

import argparse
import sys
from pathlib import Path
from .lint import lint_file
from .ingest import ExampleMetadata, example_path, render_example, validate_library
from .engine import (
    build_writing_brief,
    render_brief_report,
    render_critique_report,
    render_demo_report,
    render_provider_write_report,
    render_rewrite_report,
    run_critique,
    run_provider_write,
    run_rewrite,
    run_writing_demo,
)
from .evals import evaluate_fixtures, render_fixture_eval_report, render_scorecard_report, score_text
from .learning import (
    build_learning_lesson,
    default_example_proposal_path,
    default_learning_path,
    default_pattern_proposal_path,
    load_learning_note,
    render_example_proposal,
    render_learning_lesson,
    render_pattern_proposal,
    validate_learning_directory,
)
from .paths import RootResolutionError, resolve_root
from .patterns import infer_pattern_ids
from .providers import ProviderCallError, ProviderError, provider_adapter_from_env
from .retrieve import rank_examples, select_examples
from .shape import render_shape_report, run_shape
from .taxonomy import recommend_categories


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="prosekernel", description="ProseKernel writing library tools.")
    sub = parser.add_subparsers(dest="command", required=True)

    lint_p = sub.add_parser("lint", help="Score a draft for AI-slop markers")
    lint_p.add_argument("path", type=Path)

    new_p = sub.add_parser("new-example", help="Create a new annotated example skeleton")
    new_p.add_argument("--root", type=Path)
    new_p.add_argument("--title", required=True)
    new_p.add_argument("--author", required=True)
    new_p.add_argument("--source-url", required=True)
    new_p.add_argument("--date-published", default="unknown")
    new_p.add_argument("--added", required=True)
    new_p.add_argument("--category", required=True)
    new_p.add_argument("--format", required=True)
    new_p.add_argument("--rights", required=True)
    new_p.add_argument("--tags", required=True, help="Comma-separated tags")
    new_p.add_argument("--quality-score", type=int, default=8)
    new_p.add_argument("--use-when", required=True)
    new_p.add_argument("--pattern-ids", default="", help="Optional comma-separated strict pattern IDs")
    new_p.add_argument("--force", action="store_true")

    val_p = sub.add_parser("validate-library", help="Validate library example structure")
    val_p.add_argument("--root", type=Path)

    search_p = sub.add_parser("search-examples", aliases=["examples"], help="Select ProseKernel examples for a writing task")
    search_p.add_argument("task")
    search_p.add_argument("--root", type=Path)
    search_p.add_argument("--limit", type=int, default=5)
    search_p.add_argument("--category")
    search_p.add_argument("--mode", choices=("lexical", "semantic", "hybrid"), default="lexical", help="Retrieval scorer to use; default preserves deterministic lexical/category behavior")
    search_p.add_argument("--explain", action="store_true", help="Print score breakdown for each retrieved example")

    brief_p = sub.add_parser("brief", help="Build a provider-agnostic dry-run writing brief")
    brief_p.add_argument("task")
    brief_p.add_argument("--root", type=Path)
    brief_p.add_argument("--limit", type=int, default=5)
    brief_p.add_argument("--category")
    brief_p.add_argument("--mode", choices=("lexical", "semantic", "hybrid"), default="lexical", help="Retrieval scorer to use; default preserves deterministic lexical/category behavior")
    brief_p.add_argument("--output", type=Path, help="Optional markdown report path")

    write_p = sub.add_parser("write", help="Draft with an explicit LLM provider and ProseKernel quality report")
    write_p.add_argument("task")
    write_p.add_argument("--root", type=Path)
    write_p.add_argument("--limit", type=int, default=5)
    write_p.add_argument("--category")
    write_p.add_argument("--mode", choices=("lexical", "semantic", "hybrid"), default="lexical", help="Retrieval scorer to use; default preserves deterministic lexical/category behavior")
    write_p.add_argument("--provider", help="Explicit provider: openai, anthropic, or openrouter")
    write_p.add_argument("--model", help="Explicit provider model name")
    write_p.add_argument("--api-key", help="Optional explicit API key; otherwise provider env var is used")
    write_p.add_argument("--timeout", type=int, default=60)
    write_p.add_argument("--output", type=Path, help="Optional markdown report path")

    critique_p = sub.add_parser("critique", help="Critique a draft with deterministic lint, scorecard, retrieval, and revision guidance")
    critique_p.add_argument("path", type=Path)
    critique_p.add_argument("--root", type=Path)
    critique_p.add_argument("--task", default="", help="Optional writing task for reader-fit and retrieval context")
    critique_p.add_argument("--limit", type=int, default=5)
    critique_p.add_argument("--category")
    critique_p.add_argument("--mode", choices=("lexical", "semantic", "hybrid"), default="lexical", help="Retrieval scorer to use for reference examples")
    critique_p.add_argument("--output", type=Path, help="Optional markdown report path")

    rewrite_p = sub.add_parser("rewrite", help="Rewrite a draft deterministically using ProseKernel critique guidance")
    rewrite_p.add_argument("path", type=Path)
    rewrite_p.add_argument("--root", type=Path)
    rewrite_p.add_argument("--task", default="", help="Optional writing task for reader-fit and retrieval context")
    rewrite_p.add_argument("--limit", type=int, default=5)
    rewrite_p.add_argument("--category")
    rewrite_p.add_argument("--mode", choices=("lexical", "semantic", "hybrid"), default="lexical", help="Retrieval scorer to use for reference examples")
    rewrite_p.add_argument("--output", type=Path, help="Optional markdown report path")
    rewrite_p.add_argument("--rewrite-output", type=Path, help="Optional path for the standalone rewritten draft only")

    shape_p = sub.add_parser("shape", help="Diagnose document architecture before sentence polish")
    shape_p.add_argument("path", type=Path)
    shape_p.add_argument("--root", type=Path)
    shape_p.add_argument("--task", required=True, help="Writing task or situation the draft is meant to serve")
    shape_p.add_argument("--reader", default="", help="Intended reader; recommended for situated diagnosis")
    shape_p.add_argument("--intent", default="", help="Desired reaction, decision, or next action; recommended")
    shape_p.add_argument("--channel", default="", help="Optional channel or format context")
    shape_p.add_argument("--output", type=Path, help="Optional markdown report path")

    learn_p = sub.add_parser("learn", help="Create a public-safe metadata-only learning note from a draft")
    learn_p.add_argument("path", type=Path)
    learn_p.add_argument("--root", type=Path)
    learn_p.add_argument("--task", default="", help="Writing task or reason this source is being studied")
    learn_p.add_argument("--source-title", required=True)
    learn_p.add_argument("--source-author", required=True)
    learn_p.add_argument("--source-url", required=True)
    learn_p.add_argument("--rights", required=True, help="Rights value: public-domain, open-license, short-excerpt, metadata-only, or user-provided")
    learn_p.add_argument("--category", required=True)
    learn_p.add_argument("--tags", required=True, help="Comma-separated tags")
    learn_p.add_argument("--pattern-ids", default="", help="Optional comma-separated strict pattern IDs; inferred from category/tags when omitted")
    learn_p.add_argument("--output", type=Path, help="Optional learning note path; defaults to learning/lessons/<source-title>.md")
    learn_p.add_argument("--force", action="store_true", help="Overwrite an existing learning note")
    learn_p.add_argument("--promote", action="store_true", help="Mark as a candidate for promotion after rights checks")
    learn_p.add_argument("--approved", action="store_true", help="Human approval flag required for promotion")

    learn_val_p = sub.add_parser("validate-learning", help="Validate public-safe learning notes")
    learn_val_p.add_argument("--root", type=Path)

    propose_example_p = sub.add_parser("propose-example", help="Create a review-required library example proposal from an approved learning note")
    propose_example_p.add_argument("path", type=Path)
    propose_example_p.add_argument("--root", type=Path)
    propose_example_p.add_argument("--format", default="learned-example")
    propose_example_p.add_argument("--output", type=Path, help="Optional proposal path; defaults to proposals/examples/<category>/<source-title>.md")
    propose_example_p.add_argument("--force", action="store_true", help="Overwrite an existing proposal")

    propose_pattern_p = sub.add_parser("propose-pattern", help="Create a review-required strict-pattern proposal from an approved learning note")
    propose_pattern_p.add_argument("path", type=Path)
    propose_pattern_p.add_argument("--root", type=Path)
    propose_pattern_p.add_argument("--pattern-id", required=True, help="New proposed pattern ID, e.g. PATTERN_UX_002")
    propose_pattern_p.add_argument("--output", type=Path, help="Optional proposal path; defaults to proposals/patterns/<pattern-id>-<source-title>.md")
    propose_pattern_p.add_argument("--force", action="store_true", help="Overwrite an existing proposal")

    demo_p = sub.add_parser("write-demo", aliases=["demo"], help="Run deterministic retrieval + draft + lint + rewrite demo")
    demo_p.add_argument("task")
    demo_p.add_argument("--root", type=Path)
    demo_p.add_argument("--limit", type=int, default=5)
    demo_p.add_argument("--category")
    demo_p.add_argument("--mode", choices=("lexical", "semantic", "hybrid"), default="lexical", help="Retrieval scorer to use; default preserves deterministic lexical/category behavior")
    demo_p.add_argument("--output", type=Path, help="Optional markdown report path")

    score_p = sub.add_parser("scorecard", aliases=["score"], help="Score a draft with the Phase 7A ProseKernel scorecard")
    score_p.add_argument("path", type=Path)
    score_p.add_argument("--task", default="", help="Optional writing task for reader-fit/non-genericness scoring")
    score_p.add_argument("--output", type=Path, help="Optional markdown report path")

    eval_p = sub.add_parser("eval", help="Run built-in weak/strong fixture evals")
    eval_p.add_argument("--root", type=Path)
    eval_p.add_argument("--output", type=Path, help="Optional markdown report path")

    args = parser.parse_args(argv)

    commands_requiring_root = {
        "new-example",
        "validate-library",
        "search-examples",
        "examples",
        "brief",
        "write",
        "critique",
        "rewrite",
        "shape",
        "learn",
        "validate-learning",
        "propose-example",
        "propose-pattern",
        "write-demo",
        "demo",
        "eval",
    }
    if args.command in commands_requiring_root:
        try:
            args.root = resolve_root(args.root)
        except RootResolutionError as exc:
            print(str(exc), file=sys.stderr)
            return 2

    if args.command == "lint":
        report = lint_file(args.path)
        status = "PASS" if report.passed else "FAIL"
        print(f"ProseKernel score: {report.score}/100 — {status}")
        if not report.findings:
            print("No slop markers found. Now read it aloud and cut 15%.")
            return 0
        for finding in report.findings:
            loc = f":{finding.line}" if finding.line else ""
            print(f"- [{finding.severity.upper()}] {finding.rule}{loc}: {finding.message}")
        return 0 if report.passed else 1

    if args.command == "new-example":
        tags = [t.strip() for t in args.tags.split(",") if t.strip()]
        pattern_ids = [p.strip() for p in args.pattern_ids.split(",") if p.strip()]
        if not pattern_ids:
            pattern_ids = list(infer_pattern_ids(args.category, tuple(tags)))
        meta = ExampleMetadata(
            title=args.title,
            author=args.author,
            source_url=args.source_url,
            date_published=args.date_published,
            added=args.added,
            category=args.category,
            format=args.format,
            rights=args.rights,
            tags=tags,
            quality_score=args.quality_score,
            use_when=args.use_when,
            pattern_ids=pattern_ids,
        )
        path = example_path(args.root, meta)
        if path.exists() and not args.force:
            print(f"Refusing to overwrite existing file: {path}")
            return 1
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_text(render_example(meta), encoding="utf-8")
        print(path)
        return 0

    if args.command == "validate-library":
        issues = validate_library(args.root)
        if not issues:
            print("Library validation passed.")
            return 0
        print("Library validation failed:")
        for path, errors in issues.items():
            print(f"- {path}")
            for error in errors:
                print(f"  - {error}")
        return 1

    if args.command in {"search-examples", "examples"}:
        categories = recommend_categories(args.task, limit=3)
        print("Recommended categories: " + ", ".join(categories))
        if args.explain:
            print(f"Retrieval mode: {args.mode}")
            matches = rank_examples(args.root, args.task, limit=args.limit, category=args.category, mode=args.mode)
            for match in matches:
                example = match.example
                rel = example.path.relative_to(args.root) if example.path.is_relative_to(args.root) else example.path
                patterns = ", ".join(example.pattern_ids)
                print(
                    f"- {example.title} [{example.category}] patterns: {patterns} {rel} "
                    f"lexical={match.lexical_score} semantic={match.semantic_score} hybrid={match.hybrid_score}"
                )
        else:
            for example in select_examples(args.root, args.task, limit=args.limit, category=args.category, mode=args.mode):
                rel = example.path.relative_to(args.root) if example.path.is_relative_to(args.root) else example.path
                patterns = ", ".join(example.pattern_ids)
                print(f"- {example.title} [{example.category}] patterns: {patterns} {rel}")
        return 0

    if args.command == "brief":
        brief = build_writing_brief(args.root, args.task, limit=args.limit, category=args.category, mode=args.mode)
        report = render_brief_report(brief)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding="utf-8")
            print(args.output)
        else:
            print(report)
        return 0

    if args.command == "write":
        if not args.provider or not args.model:
            print(
                "No default provider is configured. ProseKernel will not choose a paid provider for you. "
                "Use `prosekernel brief` for a no-credential dry run, or pass --provider and --model explicitly.",
                file=sys.stderr,
            )
            return 2
        try:
            provider_adapter = provider_adapter_from_env(
                args.provider,
                args.model,
                api_key=args.api_key,
                timeout=args.timeout,
            )
            result = run_provider_write(
                args.root,
                args.task,
                provider_adapter=provider_adapter,
                limit=args.limit,
                category=args.category,
                mode=args.mode,
            )
        except ProviderCallError as exc:
            print(f"Provider call failed: {exc}", file=sys.stderr)
            return 1
        except ProviderError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        report = render_provider_write_report(result)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding="utf-8")
            print(args.output)
        else:
            print(report)
        return 0

    if args.command == "critique":
        result = run_critique(
            args.root,
            args.path,
            task=args.task,
            limit=args.limit,
            category=args.category,
            mode=args.mode,
        )
        report = render_critique_report(result)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding="utf-8")
            print(args.output)
        else:
            print(report)
        return 0 if result.scorecard.passed else 1

    if args.command == "rewrite":
        if args.output and args.rewrite_output and args.output.resolve() == args.rewrite_output.resolve():
            print("Refusing to write report and standalone rewrite to the same path.", file=sys.stderr)
            return 2
        result = run_rewrite(
            args.root,
            args.path,
            task=args.task,
            limit=args.limit,
            category=args.category,
            mode=args.mode,
        )
        report = render_rewrite_report(result)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding="utf-8")
            print(args.output)
        else:
            print(report)
        if args.rewrite_output:
            args.rewrite_output.parent.mkdir(parents=True, exist_ok=True)
            args.rewrite_output.write_text(result.rewritten_text.strip() + "\n", encoding="utf-8")
            print(args.rewrite_output)
        return 0 if result.final_scorecard.total >= result.initial_scorecard.total else 1

    if args.command == "shape":
        draft_path = args.path
        if not draft_path.exists() and not draft_path.is_absolute():
            rooted_path = args.root / draft_path
            if rooted_path.exists():
                draft_path = rooted_path
        if not draft_path.exists():
            print(f"Draft not found: {args.path}", file=sys.stderr)
            return 2
        result = run_shape(
            draft_path,
            task=args.task,
            reader=args.reader,
            intent=args.intent,
            channel=args.channel,
        )
        report = render_shape_report(result)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding="utf-8")
            print(args.output)
        else:
            print(report)
        return 0

    if args.command == "learn":
        tags = [tag.strip() for tag in args.tags.split(",") if tag.strip()]
        pattern_ids = [pattern_id.strip() for pattern_id in args.pattern_ids.split(",") if pattern_id.strip()]
        try:
            lesson = build_learning_lesson(
                args.path,
                task=args.task or args.source_title,
                source_title=args.source_title,
                source_author=args.source_author,
                source_url=args.source_url,
                rights=args.rights,
                category=args.category,
                tags=tags,
                pattern_ids=pattern_ids or None,
                promote=args.promote,
                approved=args.approved,
            )
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        report = render_learning_lesson(lesson)
        output_path = args.output or default_learning_path(args.root, lesson)
        if output_path.exists() and not args.force:
            print(f"Refusing to overwrite existing learning note: {output_path}", file=sys.stderr)
            return 1
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        print(output_path)
        return 0

    if args.command == "validate-learning":
        issues = validate_learning_directory(args.root)
        if not issues:
            print("Learning validation passed.")
            return 0
        print("Learning validation failed:")
        for path, errors in issues.items():
            print(f"- {path}")
            for error in errors:
                print(f"  - {error}")
        return 1

    if args.command == "propose-example":
        try:
            note = load_learning_note(args.path)
            report = render_example_proposal(note, format_name=args.format)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        output_path = args.output or default_example_proposal_path(args.root, note)
        if output_path.exists() and not args.force:
            print(f"Refusing to overwrite existing proposal: {output_path}", file=sys.stderr)
            return 1
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        print(output_path)
        return 0

    if args.command == "propose-pattern":
        try:
            note = load_learning_note(args.path)
            report = render_pattern_proposal(note, pattern_id=args.pattern_id)
        except ValueError as exc:
            print(str(exc), file=sys.stderr)
            return 2
        output_path = args.output or default_pattern_proposal_path(args.root, note, args.pattern_id)
        if output_path.exists() and not args.force:
            print(f"Refusing to overwrite existing proposal: {output_path}", file=sys.stderr)
            return 1
        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(report, encoding="utf-8")
        print(output_path)
        return 0

    if args.command in {"write-demo", "demo"}:
        result = run_writing_demo(args.root, args.task, limit=args.limit, category=args.category, mode=args.mode)
        report = render_demo_report(result)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding="utf-8")
            print(args.output)
        else:
            print(report)
        return 0 if result.final_report.passed else 1

    if args.command in {"scorecard", "score"}:
        scorecard = score_text(args.path.read_text(encoding="utf-8"), task=args.task)
        report = render_scorecard_report(
            scorecard,
            title=f"ProseKernel Scorecard — {args.path.name}",
        )
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding="utf-8")
            print(args.output)
        else:
            print(report)
        return 0 if scorecard.passed else 1

    if args.command == "eval":
        results = evaluate_fixtures(args.root)
        report = render_fixture_eval_report(results, args.root)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding="utf-8")
            print(args.output)
        else:
            print(report)
        return 0 if results and all(result.passed for result in results) else 1

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
