"""Tests for WorkflowOptimizer using a fake LLM."""

from __future__ import annotations

from src.core.optimizer import WorkflowOptimizer


class FakeLLM:
    def generate(self, prompt: str, system: str | None = None) -> str:
        return "Optimized step-by-step workflow with automation."


SAMPLE = (
    "Provisioning a new server requires three separate manual approvals "
    "and a hand-written configuration checklist completed by two engineers."
)


def test_optimize_returns_result():
    optimizer = WorkflowOptimizer(llm=FakeLLM())
    result = optimizer.optimize(SAMPLE)
    assert result.process_description == SAMPLE
    assert "Optimized" in result.optimized_workflow


def test_optimize_with_analysis_context():
    optimizer = WorkflowOptimizer(llm=FakeLLM())
    result = optimizer.optimize(SAMPLE, analysis="Found 2 bottlenecks.")
    assert result.analysis_used == "Found 2 bottlenecks."


def test_compare():
    optimizer = WorkflowOptimizer(llm=FakeLLM())
    summary = optimizer.compare("old process here", "new process here")
    assert isinstance(summary, str)
