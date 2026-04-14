from typing import Any

from sqlalchemy import select
from sqlalchemy.orm import Session

from core.exceptions import VectorStoreError
from models.orm import JobEmbedding, JobPosting


class VectorRepository:
    """Isolates all pgvector DB operations from the LangGraph layer (Repository Pattern)."""

    def __init__(self, db: Session) -> None:
        self._db = db

    def similarity_search(
        self, embedding: list[float], top_k: int = 5
    ) -> list[dict[str, Any]]:
        try:
            rows = self._db.execute(
                select(JobPosting.job_title, JobPosting.company, JobPosting.raw_content)
                .join(JobEmbedding, JobEmbedding.job_id == JobPosting.id)
                .order_by(JobEmbedding.embedding.cosine_distance(embedding))
                .limit(top_k)
            ).mappings().all()
            return [dict(row) for row in rows]
        except Exception as exc:
            raise VectorStoreError("Similarity search failed") from exc

    def upsert_document(self, content: str, embedding: list[float]) -> None:
        try:
            # Full upsert logic will be implemented in the data-ingestion pipeline.
            pass
        except Exception as exc:
            raise VectorStoreError("Document upsert failed") from exc
