"""Application configuration.

Loads settings from environment variables (see .env.example) with sensible
defaults so the app runs out of the box against a local Ollama instance.
"""

from __future__ import annotations

import os
from dataclasses import dataclass, field
from pathlib import Path

# Load .env if python-dotenv is installed (optional dependency).
try:
    from dotenv import load_dotenv

    load_dotenv()
except ImportError:  # pragma: no cover - dotenv is optional
    pass


# Project paths
BASE_DIR = Path(__file__).resolve().parent.parent
DATA_DIR = BASE_DIR / "data"
SAMPLE_PROCESSES_DIR = DATA_DIR / "sample_processes"
SAMPLE_OUTPUT_DIR = DATA_DIR / "sample_output"


@dataclass
class Settings:
    """Central settings object. Values come from env vars with defaults."""

    # --- LLM provider ---
    # Provider backend: "ollama" (default) or "huggingface".
    llm_provider: str = field(
        default_factory=lambda: os.getenv("LLM_PROVIDER", "ollama")
    )
    # Model name/tag. For Ollama, e.g. "llama3", "mistral", "gemma".
    llm_model: str = field(
        default_factory=lambda: os.getenv("LLM_MODEL", "llama3")
    )
    # Ollama server host.
    ollama_host: str = field(
        default_factory=lambda: os.getenv("OLLAMA_HOST", "http://localhost:11434")
    )
    # Generation controls.
    temperature: float = field(
        default_factory=lambda: float(os.getenv("LLM_TEMPERATURE", "0.4"))
    )
    max_tokens: int = field(
        default_factory=lambda: int(os.getenv("LLM_MAX_TOKENS", "1024"))
    )

    # --- Vector store (ChromaDB) ---
    vector_db_path: str = field(
        default_factory=lambda: os.getenv(
            "VECTOR_DB_PATH", str(DATA_DIR / "chroma_db")
        )
    )
    embedding_model: str = field(
        default_factory=lambda: os.getenv(
            "EMBEDDING_MODEL", "all-MiniLM-L6-v2"
        )
    )
    collection_name: str = field(
        default_factory=lambda: os.getenv("COLLECTION_NAME", "it_processes")
    )

    # --- Logging ---
    log_level: str = field(
        default_factory=lambda: os.getenv("LOG_LEVEL", "INFO")
    )


# Singleton-style settings instance imported across the app.
settings = Settings()
