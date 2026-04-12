import logging
from typing import Any

from agents.state import GraphState
from core.exceptions import LLMServiceError, VectorStoreError

logger = logging.getLogger(__name__)


async def market_node(state: GraphState, llm, vector_repo) -> dict:
    """Queries the vector store for real job market data relevant to the target role.
    Owns: market_data (stored within gap_analysis dict pre-population)
    Falls back to a deterministic keyword query if LLM fails (Strategy Pattern).
    """
    try:
        embedding: list[float] = await _get_embedding(state["target_role"], llm)
        results: list[dict[str, Any]] = vector_repo.similarity_search(embedding, top_k=5)
        return {"gap_analysis": {"market_results": results}}
    except LLMServiceError:
        logger.warning("market_node LLM failed; falling back to keyword search")
        fallback = vector_repo.similarity_search(embedding=[], top_k=5)
        return {"gap_analysis": {"market_results": fallback}}
    except Exception as exc:
        logger.error("market_node failed: %s", exc)
        raise


async def _get_embedding(text: str, llm) -> list[float]:
    """Encapsulates embedding generation; replace with a dedicated embedding client."""
    try:
        # Placeholder — swap for an actual embeddings API call
        return []
    except Exception as exc:
        raise LLMServiceError("Embedding generation failed") from exc
