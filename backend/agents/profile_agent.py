import logging

from agents.state import GraphState
from core.exceptions import LLMServiceError

logger = logging.getLogger(__name__)


async def profile_node(state: GraphState, llm) -> dict:
    """Parses the resume and GitHub URL into a structured profile summary.
    Owns: profile_summary
    """
    try:
        response = await llm.ainvoke(
            f"Summarize this resume for a {state['target_role']} role:\n{state['resume_text']}"
        )
        return {"profile_summary": response.content}
    except Exception as exc:
        logger.error("profile_node failed: %s", exc)
        raise LLMServiceError("Profile agent LLM call failed") from exc
