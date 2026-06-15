"""Integration test for the end-to-end pipeline using a fake LLM.

Patches the LLM factory so the full run_pipeline path is exercised without a
running model.
"""

from __future__ import annotations

import src.core.optimizer as optimizer_mod
import src.core.process_analyzer as analyzer_mod
from src.main import run_pipeline


class FakeLLM:
    def generate(self, prompt: str, system: str | None = None) -> str:
        if "optimized version" in prompt.lower():
            return "OPTIMIZED OUTPUT"
        return "ANALYSIS OUTPUT"


SAMPLE = (
    "The on-call rotation is tracked in a spreadsheet that someone updates "
    "manually each week and then pastes into a chat channel by hand."
)


def test_run_pipeline(monkeypatch):
    monkeypatch.setattr(analyzer_mod, "get_llm_client", lambda: FakeLLM())
    monkeypatch.setattr(optimizer_mod, "get_llm_client", lambda: FakeLLM())

    results = run_pipeline(SAMPLE)
    assert results["analysis"] == "ANALYSIS OUTPUT"
    assert results["optimized"] == "OPTIMIZED OUTPUT"
