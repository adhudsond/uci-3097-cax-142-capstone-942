"""LLM initialization and management.

Provides a thin abstraction over the underlying LLM backend so the rest of the
app does not care whether it talks to Ollama, Hugging Face, etc. Swap backends
via the LLM_PROVIDER env var (see config.py).
"""

from __future__ import annotations

from typing import Protocol

from .config import settings
from .utils.logger import get_logger

logger = get_logger(__name__)


class LLMClient(Protocol):
    """Minimal interface any backend must implement."""

    def generate(self, prompt: str, system: str | None = None) -> str:
        """Return the model's text completion for a prompt."""
        ...


class OllamaClient:
    """Backend that talks to a local Ollama server."""

    def __init__(self) -> None:
        self.model = settings.llm_model
        self.host = settings.ollama_host
        self._client = None  # Lazily initialized.

    def _ensure_client(self):
        if self._client is None:
            try:
                import ollama

                self._client = ollama.Client(host=self.host)
            except ImportError as exc:  # pragma: no cover
                raise RuntimeError(
                    "The 'ollama' package is not installed. "
                    "Install it with: uv add ollama"
                ) from exc
        return self._client

    def generate(self, prompt: str, system: str | None = None) -> str:
        client = self._ensure_client()
        messages = []
        if system:
            messages.append({"role": "system", "content": system})
        messages.append({"role": "user", "content": prompt})

        logger.debug("Sending prompt to Ollama model=%s", self.model)
        response = client.chat(
            model=self.model,
            messages=messages,
            options={
                "temperature": settings.temperature,
                "num_predict": settings.max_tokens,
            },
        )
        return response["message"]["content"]


class HuggingFaceClient:
    """Backend that runs a Hugging Face text-generation pipeline locally.

    Placeholder implementation — wire up transformers in Phase 2.
    """

    def __init__(self) -> None:
        self.model = settings.llm_model
        self._pipe = None

    def _ensure_pipe(self):
        if self._pipe is None:
            try:
                from transformers import pipeline

                self._pipe = pipeline("text-generation", model=self.model)
            except ImportError as exc:  # pragma: no cover
                raise RuntimeError(
                    "The 'transformers' package is not installed. "
                    "Install it with: uv add transformers torch"
                ) from exc
        return self._pipe

    def generate(self, prompt: str, system: str | None = None) -> str:
        pipe = self._ensure_pipe()
        full_prompt = f"{system}\n\n{prompt}" if system else prompt
        result = pipe(
            full_prompt,
            max_new_tokens=settings.max_tokens,
            temperature=settings.temperature,
        )
        return result[0]["generated_text"]


def get_llm_client() -> LLMClient:
    """Factory that returns the configured LLM client."""
    provider = settings.llm_provider.lower()
    logger.info("Initializing LLM provider: %s", provider)

    if provider == "ollama":
        return OllamaClient()
    if provider == "huggingface":
        return HuggingFaceClient()

    raise ValueError(
        f"Unknown LLM_PROVIDER '{provider}'. Use 'ollama' or 'huggingface'."
    )
