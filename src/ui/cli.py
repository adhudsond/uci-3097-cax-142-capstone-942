"""Command-line interface.

Run with:  uv run python -m src.ui.cli --help

Reads a process description from an argument, --file, or stdin, then prints the
analysis and optimized workflow. Optionally saves a report document with
--save / --format.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from ..core.exporter import FORMATS, ExportPayload
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
    parser.add_argument(
        "--save",
        metavar="PATH",
        help="Save a report document to PATH (e.g. report.md, report.docx).",
    )
    parser.add_argument(
        "--format",
        choices=sorted(FORMATS.keys()),
        help="Report format. Inferred from --save extension if omitted.",
    )
    return parser


def _infer_format(save_path: str, explicit: str | None) -> str:
    if explicit:
        return explicit
    ext = Path(save_path).suffix.lstrip(".").lower()
    ext_map = {fmt[1]: name for name, fmt in FORMATS.items()}
    if ext in ext_map:
        return ext_map[ext]
    raise SystemExit(
        f"Could not infer format from '{save_path}'. "
        f"Use --format with one of: {', '.join(sorted(FORMATS))}."
    )


def _save_report(
    save_path: str,
    fmt_name: str,
    payload: ExportPayload,
) -> None:
    renderer, _ext, is_binary = FORMATS[fmt_name]
    content = renderer(payload)
    path = Path(save_path)
    if is_binary:
        path.write_bytes(content)
    else:
        path.write_text(content, encoding="utf-8")
    print(f"\nSaved {fmt_name} report to: {path.resolve()}")


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

    optimized_text = ""
    if not args.analyze_only:
        optimizer = WorkflowOptimizer()
        optimization = optimizer.optimize(
            process_text, analysis=analysis.analysis_text
        )
        optimized_text = optimization.optimized_workflow
        print("\n=== OPTIMIZED WORKFLOW ===\n")
        print(optimized_text)

    if args.save:
        fmt_name = _infer_format(args.save, args.format)
        payload = ExportPayload(
            process_description=process_text,
            analysis=analysis.analysis_text,
            optimized=optimized_text or "(Not generated — ran analysis only.)",
        )
        try:
            _save_report(args.save, fmt_name, payload)
        except RuntimeError as exc:
            print(f"\nError saving report: {exc}", file=sys.stderr)
            return 1

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
