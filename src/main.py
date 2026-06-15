"""Application entry point.

Routes to either the Streamlit UI or the CLI depending on how it's launched.
Streamlit apps are normally started with `streamlit run`, so for convenience
this module exposes a small dispatcher used by the CLI and tests.
"""

from __future__ import annotations

import argparse

from .core.optimizer import WorkflowOptimizer
from .core.process_analyzer import ProcessAnalyzer
from .utils.logger import get_logger

logger = get_logger(__name__)


def run_pipeline(process_description: str) -> dict[str, str]:
    """Run analyze -> optimize end to end and return both results.

    This is the single function the UI, CLI, and tests all call so behavior
    stays consistent across entry points.
    """
    analyzer = ProcessAnalyzer()
    optimizer = WorkflowOptimizer()

    analysis = analyzer.analyze(process_description)
    optimization = optimizer.optimize(
        process_description, analysis=analysis.analysis_text
    )
    return {
        "analysis": analysis.analysis_text,
        "optimized": optimization.optimized_workflow,
    }


def main() -> None:
    """CLI dispatcher kept minimal; full CLI lives in ui/cli.py."""
    parser = argparse.ArgumentParser(
        description="Business Process Optimization (AI)"
    )
    parser.add_argument(
        "process",
        nargs="?",
        help="Process description text to analyze and optimize.",
    )
    args = parser.parse_args()

    if not args.process:
        print(
            "No process provided.\n"
            "Run the web UI:  uv run streamlit run src/ui/streamlit_app.py\n"
            "Or the CLI:      uv run python -m src.ui.cli --help"
        )
        return

    results = run_pipeline(args.process)
    print("\n=== ANALYSIS ===\n", results["analysis"])
    print("\n=== OPTIMIZED WORKFLOW ===\n", results["optimized"])


if __name__ == "__main__":
    main()
