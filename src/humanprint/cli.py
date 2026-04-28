from __future__ import annotations

import argparse
from pathlib import Path
from .lint import lint_file


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(prog="humanprint", description="Lint writing for AI slop.")
    sub = parser.add_subparsers(dest="command", required=True)

    lint_p = sub.add_parser("lint", help="Score a draft for AI-slop markers")
    lint_p.add_argument("path", type=Path)

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

    return 2


if __name__ == "__main__":
    raise SystemExit(main())
