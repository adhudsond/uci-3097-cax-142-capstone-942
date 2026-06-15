"""Store and retrieve processes.

A higher-level repository that sits on top of the VectorStore and handles ID
generation and convenient save/retrieve operations for analyzed processes.
"""

from __future__ import annotations

import hashlib
from datetime import datetime, timezone
from typing import Any

from ..utils.logger import get_logger
from .vector_store import VectorStore

logger = get_logger(__name__)


def _make_id(text: str) -> str:
    """Deterministic short ID from the process text."""
    digest = hashlib.sha256(text.encode("utf-8")).hexdigest()
    return f"proc_{digest[:12]}"


class ProcessRepository:
    """CRUD-ish interface for stored processes."""

    def __init__(self, store: VectorStore | None = None) -> None:
        self.store = store or VectorStore()

    def save(
        self,
        process_text: str,
        optimized_text: str | None = None,
        tags: list[str] | None = None,
    ) -> str:
        """Persist a process (and optional optimization). Returns the doc id."""
        doc_id = _make_id(process_text)
        metadata: dict[str, Any] = {
            "created_at": datetime.now(timezone.utc).isoformat(),
            "has_optimization": optimized_text is not None,
            "tags": ",".join(tags or []),
        }
        if optimized_text:
            metadata["optimized"] = optimized_text
        self.store.add_process(doc_id, process_text, metadata)
        logger.info("Saved process id=%s", doc_id)
        return doc_id

    def find_similar(
        self, query: str, n_results: int = 3
    ) -> list[dict[str, Any]]:
        """Find previously stored processes similar to the query."""
        return self.store.search(query, n_results=n_results)
