"""Prompt templates for analyzing and optimizing IT business processes.

Keeping prompts in one place makes prompt engineering iterative and testable.
Each template is a function returning a formatted string so inputs are explicit.
"""

from __future__ import annotations

SYSTEM_PROMPT = (
    "You are an IT operations and business process optimization assistant. "
    "You analyze workflows used by IT teams and suggest concrete, practical "
    "improvements focused on efficiency, automation, and reduced manual effort. "
    "Be specific and actionable. Avoid generic advice."
)


def analysis_prompt(process_description: str) -> str:
    """Prompt asking the model to analyze an existing process."""
    return f"""Analyze the following IT business process.

PROCESS:
{process_description}

Provide:
1. A short summary of what the process does.
2. Identified bottlenecks or inefficiencies.
3. Manual steps that could be automated.
4. Any risks or single points of failure.

Respond in clear, structured sections.
"""


def optimization_prompt(
    process_description: str, analysis: str | None = None
) -> str:
    """Prompt asking the model to produce an optimized workflow."""
    context = f"\n\nPRIOR ANALYSIS:\n{analysis}" if analysis else ""
    return f"""Produce an optimized version of the following IT process.

ORIGINAL PROCESS:
{process_description}{context}

Provide:
1. An optimized step-by-step workflow.
2. Which steps were combined, removed, or automated and why.
3. Suggested tools or integrations (e.g., ticketing, CI/CD, monitoring).
4. Expected efficiency gains.

Keep it practical for a mid-sized IT team.
"""


def comparison_prompt(original: str, optimized: str) -> str:
    """Prompt for a before/after comparison summary."""
    return f"""Compare these two versions of an IT process and summarize the
key improvements in a concise bullet list.

ORIGINAL:
{original}

OPTIMIZED:
{optimized}
"""
