"""Streamlit web interface.

Run with:  uv run streamlit run src/ui/streamlit_app.py

This is a skeleton: the layout and wiring are in place; the analysis/optimize
calls go through the same core logic as the CLI. It degrades gracefully if the
LLM backend isn't running yet so you can develop the UI independently.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Make `src` importable when launched via `streamlit run`.
ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.optimizer import WorkflowOptimizer  # noqa: E402
from src.core.process_analyzer import ProcessAnalyzer  # noqa: E402
from src.utils.validators import ValidationError, validate_process_description  # noqa: E402


st.set_page_config(
    page_title="Business Process Optimizer",
    page_icon="⚙️",
    layout="wide",
)


def _sidebar() -> None:
    with st.sidebar:
        st.header("About")
        st.write(
            "Generative AI assistant that analyzes IT team workflows and "
            "proposes optimized versions to improve operational efficiency."
        )
        st.caption("CAP 942 Capstone — open-source LLM via Ollama.")


def main() -> None:
    _sidebar()
    st.title("⚙️ Generative AI for Business Process Optimization")
    st.write(
        "Paste an IT process or workflow below. The app will analyze it for "
        "bottlenecks and generate an optimized version."
    )

    process_text = st.text_area(
        "IT Process Description",
        height=240,
        placeholder=(
            "Example: When a new employee joins, IT manually creates accounts "
            "in AD, email, and the ticketing system, then emails the manager..."
        ),
    )

    col1, col2 = st.columns(2)
    analyze_clicked = col1.button("Analyze", use_container_width=True)
    optimize_clicked = col2.button(
        "Analyze + Optimize", type="primary", use_container_width=True
    )

    if analyze_clicked or optimize_clicked:
        try:
            validate_process_description(process_text)
        except ValidationError as exc:
            st.error(str(exc))
            return

        try:
            with st.spinner("Analyzing process..."):
                analyzer = ProcessAnalyzer()
                analysis = analyzer.analyze(process_text)

            st.subheader("Analysis")
            st.markdown(analysis.analysis_text)

            if optimize_clicked:
                with st.spinner("Generating optimized workflow..."):
                    optimizer = WorkflowOptimizer()
                    optimization = optimizer.optimize(
                        process_text, analysis=analysis.analysis_text
                    )
                st.subheader("Optimized Workflow")
                st.markdown(optimization.optimized_workflow)

        except Exception as exc:  # noqa: BLE001 - surface errors in the UI
            st.error(f"Something went wrong: {exc}")
            st.info(
                "Make sure your LLM backend is running. For Ollama: "
                "`ollama serve` and `ollama pull llama3`."
            )


if __name__ == "__main__":
    main()
