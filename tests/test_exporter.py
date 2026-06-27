"""Tests for the document exporter.

Markdown/text/HTML are dependency-free and always tested. The .docx test is
skipped automatically if python-docx isn't installed.
"""

from __future__ import annotations

import pytest

from src.core.exporter import (
    ExportPayload,
    to_html,
    to_markdown,
    to_text,
)

PAYLOAD = ExportPayload(
    process_description="Engineers manually reset passwords over email.",
    analysis="Bottleneck: no self-service. Risk: plain-text passwords.",
    optimized="1. Add self-service portal.\n2. Enforce MFA.",
    comparison="- Removed manual email step\n- Added MFA",
)


def test_markdown_contains_sections():
    md = to_markdown(PAYLOAD)
    assert "# Business Process Optimization Report" in md
    assert "## Analysis" in md
    assert "## Optimized Workflow" in md
    assert "## Before / After Comparison" in md


def test_text_contains_sections():
    txt = to_text(PAYLOAD)
    assert "ORIGINAL PROCESS" in txt
    assert "ANALYSIS" in txt
    assert "OPTIMIZED WORKFLOW" in txt


def test_html_is_escaped_and_structured():
    payload = ExportPayload(
        process_description="Uses <script> & weird chars",
        analysis="a",
        optimized="b",
    )
    html = to_html(payload)
    assert "<!DOCTYPE html>" in html
    assert "&lt;script&gt;" in html  # escaped
    assert "<script>" not in html.split("<style>")[1]  # not raw in body


def test_docx_generates_bytes_or_skips():
    docx = pytest.importorskip("docx")  # noqa: F841
    from src.core.exporter import to_docx

    data = to_docx(PAYLOAD)
    assert isinstance(data, bytes)
    assert data[:2] == b"PK"  # .docx is a zip archive
