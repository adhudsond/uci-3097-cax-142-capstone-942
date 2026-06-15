"""Tests for ProcessAnalyzer using a fake LLM (no model required)."""

from __future__ import annotations

import pytest

from src.core.process_analyzer import ProcessAnalyzer
from src.utils.validators import ValidationError


class FakeLLM:
    """Returns a canned response and records the last prompt."""

    def __init__(self) -> None:
        self.last_prompt: str | None = None

    def generate(self, prompt: str, system: str | None = None) -> str:
        self.last_prompt = prompt
        return "1. Summary\n2. Bottlenecks\n3. Automatable steps"


SAMPLE = (
    "When a ticket is created, an engineer manually triages it, assigns it, "
    "and emails the requester for more details before starting work."
)


def test_analyze_returns_result():
    analyzer = ProcessAnalyzer(llm=FakeLLM())
    result = analyzer.analyze(SAMPLE)
    assert result.process_description == SAMPLE
    assert "Bottlenecks" in result.analysis_text


def test_analyze_rejects_short_input():
    analyzer = ProcessAnalyzer(llm=FakeLLM())
    with pytest.raises(ValidationError):
        analyzer.analyze("too short")
