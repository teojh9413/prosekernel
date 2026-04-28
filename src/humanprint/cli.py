from __future__ import annotations

import argparse
from pathlib import Path
from .lint import lint_file
from .ingest import ExampleMetadata, example_path, render_example, validate_library


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
    new_p.add_argument("--force", action="store_true")

    val_p = sub.add_parser("validate-library", help="Validate library example structure")
    val_p.add_argument("--root", type=Path, default=Path.cwd())

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
        meta = ExampleMetadata(
            title=args.title,
            author=args.author,
            source_url=args.source_url,
            date_published=args.date_published,
            added=args.added,
            category=args.category,
            format=args.format,
            rights=args.rights,
            tags=[t.strip() for t in args.tags.split(",") if t.strip()],
            quality_score=args.quality_score,
            use_when=args.use_when,
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

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
