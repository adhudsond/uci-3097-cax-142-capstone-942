"""ChromaDB vector store management.

Wraps a persistent ChromaDB collection used to store IT process descriptions
and their optimizations so similar past processes can be retrieved (RAG).
Chroma is an optional dependency; methods raise a clear error if it's missing.
"""

from __future__ import annotations

from typing import Any

from ..config import settings
from ..utils.logger import get_logger

logger = get_logger(__name__)


class VectorStore:
    """Thin wrapper around a persistent ChromaDB collection."""

    def __init__(self) -> None:
        self._client = None
        self._collection = None

    def _ensure_collection(self):
        if self._collection is None:
            try:
                import chromadb
                from chromadb.utils import embedding_functions
            except ImportError as exc:  # pragma: no cover
                raise RuntimeError(
                    "ChromaDB is not installed. Install it with: "
                    "uv add chromadb sentence-transformers"
                ) from exc

            self._client = chromadb.PersistentClient(
                path=settings.vector_db_path
            )
            embed_fn = embedding_functions.SentenceTransformerEmbeddingFunction(
                model_name=settings.embedding_model
            )
            self._collection = self._client.get_or_create_collection(
                name=settings.collection_name,
                embedding_function=embed_fn,
            )
            logger.info(
                "Vector collection '%s' ready at %s",
                settings.collection_name,
                settings.vector_db_path,
            )
        return self._collection

    def add_process(
        self, doc_id: str, text: str, metadata: dict[str, Any] | None = None
    ) -> None:
        """Add or upsert a process document."""
        collection = self._ensure_collection()
        collection.upsert(
            ids=[doc_id],
            documents=[text],
            metadatas=[metadata or {}],
        )
        logger.debug("Upserted process id=%s", doc_id)

    def search(self, query: str, n_results: int = 3) -> list[dict[str, Any]]:
        """Return the most similar stored processes to a query."""
        collection = self._ensure_collection()
        results = collection.query(query_texts=[query], n_results=n_results)

        hits: list[dict[str, Any]] = []
        documents = results.get("documents", [[]])[0]
        ids = results.get("ids", [[]])[0]
        metadatas = results.get("metadatas", [[]])[0]
        for doc_id, doc, meta in zip(ids, documents, metadatas):
            hits.append({"id": doc_id, "document": doc, "metadata": meta})
        return hits
