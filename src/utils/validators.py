"""Input validation helpers."""

from __future__ import annotations

MIN_PROCESS_LENGTH = 20
MAX_PROCESS_LENGTH = 20_000


class ValidationError(ValueError):
    """Raised when user input fails validation."""


def validate_process_description(text: str) -> str:
    """Validate a process description. Returns the cleaned text."""
    if text is None:
        raise ValidationError("Process description cannot be None.")

    cleaned = text.strip()
    if len(cleaned) < MIN_PROCESS_LENGTH:
        raise ValidationError(
            f"Process description is too short "
            f"(min {MIN_PROCESS_LENGTH} characters)."
        )
    if len(cleaned) > MAX_PROCESS_LENGTH:
        raise ValidationError(
            f"Process description is too long "
            f"(max {MAX_PROCESS_LENGTH} characters)."
        )
    return cleaned
