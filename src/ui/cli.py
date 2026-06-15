"""Command-line interface.

Run with:  uv run python -m src.ui.cli --help

Reads a process description from an argument, --file, or stdin, then prints the
analysis and optimized workflow.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ..core.optimizer import WorkflowOptimizer
from ..core.process_analyzer import ProcessAnalyzer
from ..utils.validators import ValidationError, validate_process_description


def _read_input(args: argparse.Namespace) -> str:
    if args.text:
        return args.text
    if args.file:
        return Path(args.file).read_text(encoding="utf-8")
    if not sys.stdin.isatty():
        return sys.stdin.read()
    raise SystemExit("No input. Provide TEXT, --file PATH, or pipe via stdin.")


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        prog="bpo-cli",
        description="Analyze and optimize an IT business process.",
    )
    parser.add_argument("text", nargs="?", help="Process description text.")
    parser.add_argument("--file", help="Read process description from a file.")
    parser.add_argument(
        "--analyze-only",
        action="store_true",
        help="Only run analysis, skip optimization.",
    )
    return parser


def main(argv: list[str] | None = None) -> int:
    args = build_parser().parse_args(argv)
    process_text = _read_input(args)

    try:
        validate_process_description(process_text)
    except ValidationError as exc:
        print(f"Error: {exc}", file=sys.stderr)
        return 1

    analyzer = ProcessAnalyzer()
    analysis = analyzer.analyze(process_text)
    print("\n=== ANALYSIS ===\n")
    print(analysis.analysis_text)

    if not args.analyze_only:
        optimizer = WorkflowOptimizer()
        optimization = optimizer.optimize(
            process_text, analysis=analysis.analysis_text
        )
        print("\n=== OPTIMIZED WORKFLOW ===\n")
        print(optimization.optimized_workflow)

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
