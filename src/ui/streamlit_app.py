"""Streamlit web interface.

Run with:  uv run streamlit run src/ui/streamlit_app.py

Layout and wiring go through the same core logic as the CLI. After a run, the
generated analysis and optimized workflow can be downloaded as Markdown, plain
text, HTML, or Word (.docx) documents.
"""

from __future__ import annotations

import sys
from pathlib import Path

import streamlit as st

# Make `src` importable when launched via `streamlit run`.
ROOT = Path(__file__).resolve().parent.parent.parent
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

from src.core.exporter import (  # noqa: E402
    ExportPayload,
    to_docx,
    to_html,
    to_markdown,
    to_text,
)
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


def _download_section(payload: ExportPayload) -> None:
    """Render download buttons for each export format."""
    st.subheader("📄 Download report")
    st.caption("Save this analysis and optimized workflow as a document.")

    c1, c2, c3, c4 = st.columns(4)

    c1.download_button(
        "Markdown (.md)",
        data=to_markdown(payload),
        file_name="bpo_report.md",
        mime="text/markdown",
        use_container_width=True,
    )
    c2.download_button(
        "Text (.txt)",
        data=to_text(payload),
        file_name="bpo_report.txt",
        mime="text/plain",
        use_container_width=True,
    )
    c3.download_button(
        "HTML (.html)",
        data=to_html(payload),
        file_name="bpo_report.html",
        mime="text/html",
        use_container_width=True,
    )

    # .docx requires python-docx; offer it if available, else explain.
    try:
        docx_bytes = to_docx(payload)
        c4.download_button(
            "Word (.docx)",
            data=docx_bytes,
            file_name="bpo_report.docx",
            mime=(
                "application/vnd.openxmlformats-officedocument."
                "wordprocessingml.document"
            ),
            use_container_width=True,
        )
    except RuntimeError:
        c4.button(
            "Word (.docx)",
            disabled=True,
            help="Install python-docx to enable: uv sync --extra docs",
            use_container_width=True,
        )


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

            optimized_text = ""
            if optimize_clicked:
                with st.spinner("Generating optimized workflow..."):
                    optimizer = WorkflowOptimizer()
                    optimization = optimizer.optimize(
                        process_text, analysis=analysis.analysis_text
                    )
                optimized_text = optimization.optimized_workflow
                st.subheader("Optimized Workflow")
                st.markdown(optimized_text)

            # Offer downloads once we have results.
            st.divider()
            payload = ExportPayload(
                process_description=process_text,
                analysis=analysis.analysis_text,
                optimized=optimized_text or "(Not generated — ran analysis only.)",
            )
            _download_section(payload)

        except Exception as exc:  # noqa: BLE001 - surface errors in the UI
            st.error(f"Something went wrong: {exc}")
            st.info(
                "Make sure your LLM backend is running. For Ollama: "
                "start the server and `ollama pull llama3`."
            )


if __name__ == "__main__":
    main()
