"""Workflow optimization logic.

Generates an optimized workflow from a process description, optionally using a
prior analysis as additional context.
"""

from __future__ import annotations

from dataclasses import dataclass

from ..llm_provider import LLMClient, get_llm_client
from ..utils.logger import get_logger
from ..utils.validators import validate_process_description
from . import prompt_templates

logger = get_logger(__name__)


@dataclass
class OptimizationResult:
    """Structured output of an optimization run."""

    process_description: str
    optimized_workflow: str
    analysis_used: str | None = None


class WorkflowOptimizer:
    """Produces optimized workflows using the configured LLM."""

    def __init__(self, llm: LLMClient | None = None) -> None:
        self.llm = llm or get_llm_client()

    def optimize(
        self, process_description: str, analysis: str | None = None
    ) -> OptimizationResult:
        """Generate an optimized workflow for the given process."""
        validate_process_description(process_description)
        logger.info("Optimizing process (%d chars)", len(process_description))

        prompt = prompt_templates.optimization_prompt(
            process_description, analysis=analysis
        )
        text = self.llm.generate(
            prompt, system=prompt_templates.SYSTEM_PROMPT
        )
        return OptimizationResult(
            process_description=process_description,
            optimized_workflow=text,
            analysis_used=analysis,
        )

    def compare(self, original: str, optimized: str) -> str:
        """Produce a before/after comparison summary."""
        prompt = prompt_templates.comparison_prompt(original, optimized)
        return self.llm.generate(prompt, system=prompt_templates.SYSTEM_PROMPT)
