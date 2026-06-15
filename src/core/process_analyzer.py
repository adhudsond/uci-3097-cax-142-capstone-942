"""Core analysis logic.

Takes a raw IT process description and uses the LLM to produce a structured
analysis (bottlenecks, manual steps, risks).
"""

from __future__ import annotations

from dataclasses import dataclass

from ..llm_provider import LLMClient, get_llm_client
from ..utils.logger import get_logger
from ..utils.validators import validate_process_description
from . import prompt_templates

logger = get_logger(__name__)


@dataclass
class AnalysisResult:
    """Structured output of an analysis run."""

    process_description: str
    analysis_text: str


class ProcessAnalyzer:
    """Analyzes IT processes using the configured LLM."""

    def __init__(self, llm: LLMClient | None = None) -> None:
        self.llm = llm or get_llm_client()

    def analyze(self, process_description: str) -> AnalysisResult:
        """Run analysis on a single process description."""
        validate_process_description(process_description)
        logger.info("Analyzing process (%d chars)", len(process_description))

        prompt = prompt_templates.analysis_prompt(process_description)
        text = self.llm.generate(
            prompt, system=prompt_templates.SYSTEM_PROMPT
        )
        return AnalysisResult(
            process_description=process_description,
            analysis_text=text,
        )
