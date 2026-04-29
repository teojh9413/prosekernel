from __future__ import annotations

import argparse
import sys
from pathlib import Path
from .lint import lint_file
from .ingest import ExampleMetadata, example_path, render_example, validate_library
from .engine import (
    build_writing_brief,
    render_brief_report,
    render_demo_report,
    render_provider_write_report,
    run_provider_write,
    run_writing_demo,
)
from .evals import evaluate_fixtures, render_fixture_eval_report, render_scorecard_report, score_text
from .patterns import infer_pattern_ids
from .providers import ProviderCallError, ProviderError, provider_adapter_from_env
from .retrieve import rank_examples, select_examples
from .taxonomy import recommend_categories


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="humanprint", description="Humanprint writing library tools.")
    sub = parser.add_subparsers(dest="command", required=True)

    lint_p = sub.add_parser("lint", help="Score a draft for AI-slop markers")
    lint_p.add_argument("path", type=Path)

    new_p = sub.add_parser("new-example", help="Create a new annotated example skeleton")
    new_p.add_argument("--root", type=Path, default=Path.cwd())
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
    val_p.add_argument("--root", type=Path, default=Path.cwd())

    search_p = sub.add_parser("search-examples", help="Select Humanprint examples for a writing task")
    search_p.add_argument("task")
    search_p.add_argument("--root", type=Path, default=Path.cwd())
    search_p.add_argument("--limit", type=int, default=5)
    search_p.add_argument("--category")
    search_p.add_argument("--mode", choices=("lexical", "semantic", "hybrid"), default="lexical", help="Retrieval scorer to use; default preserves deterministic lexical/category behavior")
    search_p.add_argument("--explain", action="store_true", help="Print score breakdown for each retrieved example")

    brief_p = sub.add_parser("brief", help="Build a provider-agnostic dry-run writing brief")
    brief_p.add_argument("task")
    brief_p.add_argument("--root", type=Path, default=Path.cwd())
    brief_p.add_argument("--limit", type=int, default=5)
    brief_p.add_argument("--category")
    brief_p.add_argument("--mode", choices=("lexical", "semantic", "hybrid"), default="lexical", help="Retrieval scorer to use; default preserves deterministic lexical/category behavior")
    brief_p.add_argument("--output", type=Path, help="Optional markdown report path")

    write_p = sub.add_parser("write", help="Draft with an explicit LLM provider and Humanprint quality report")
    write_p.add_argument("task")
    write_p.add_argument("--root", type=Path, default=Path.cwd())
    write_p.add_argument("--limit", type=int, default=5)
    write_p.add_argument("--category")
    write_p.add_argument("--mode", choices=("lexical", "semantic", "hybrid"), default="lexical", help="Retrieval scorer to use; default preserves deterministic lexical/category behavior")
    write_p.add_argument("--provider", help="Explicit provider: openai, anthropic, or openrouter")
    write_p.add_argument("--model", help="Explicit provider model name")
    write_p.add_argument("--api-key", help="Optional explicit API key; otherwise provider env var is used")
    write_p.add_argument("--timeout", type=int, default=60)
    write_p.add_argument("--output", type=Path, help="Optional markdown report path")

    demo_p = sub.add_parser("write-demo", help="Run deterministic retrieval + draft + lint + rewrite demo")
    demo_p.add_argument("task")
    demo_p.add_argument("--root", type=Path, default=Path.cwd())
    demo_p.add_argument("--limit", type=int, default=5)
    demo_p.add_argument("--category")
    demo_p.add_argument("--mode", choices=("lexical", "semantic", "hybrid"), default="lexical", help="Retrieval scorer to use; default preserves deterministic lexical/category behavior")
    demo_p.add_argument("--output", type=Path, help="Optional markdown report path")

    score_p = sub.add_parser("scorecard", help="Score a draft with the Phase 7A Humanprint scorecard")
    score_p.add_argument("path", type=Path)
    score_p.add_argument("--task", default="", help="Optional writing task for reader-fit/non-genericness scoring")
    score_p.add_argument("--output", type=Path, help="Optional markdown report path")

    eval_p = sub.add_parser("eval", help="Run built-in weak/strong fixture evals")
    eval_p.add_argument("--root", type=Path, default=Path.cwd())
    eval_p.add_argument("--output", type=Path, help="Optional markdown report path")

    args = parser.parse_args(argv)

    if args.command == "lint":
        report = lint_file(args.path)
        status = "PASS" if report.passed else "FAIL"
        print(f"Humanprint score: {report.score}/100 — {status}")
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

    if args.command == "search-examples":
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
                "No default provider is configured. Humanprint will not choose a paid provider for you. "
                "Use `humanprint brief` for a no-credential dry run, or pass --provider and --model explicitly.",
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

    if args.command == "write-demo":
        result = run_writing_demo(args.root, args.task, limit=args.limit, category=args.category, mode=args.mode)
        report = render_demo_report(result)
        if args.output:
            args.output.parent.mkdir(parents=True, exist_ok=True)
            args.output.write_text(report, encoding="utf-8")
            print(args.output)
        else:
            print(report)
        return 0 if result.final_report.passed else 1

    if args.command == "scorecard":
        scorecard = score_text(args.path.read_text(encoding="utf-8"), task=args.task)
        report = render_scorecard_report(
            scorecard,
            title=f"Humanprint Scorecard — {args.path.name}",
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
