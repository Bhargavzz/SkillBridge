import logging

from agents.state import GraphState
from core.exceptions import LLMServiceError

logger = logging.getLogger(__name__)

_CRITIC_PROMPT = """
You are a strict career roadmap critic. Review the following roadmap for realism,
completeness, and alignment with the target role. Provide concise, actionable feedback.

Target role: {target_role}
Roadmap: {roadmap}
"""


async def critic_node(state: GraphState, llm) -> dict:
    """Validates and critiques the generated roadmap for quality and realism.
    Owns: critic_feedback
    """
    try:
        prompt = _CRITIC_PROMPT.format(
            target_role=state["target_role"],
            roadmap=state.get("roadmap", []),
        )
        response = await llm.ainvoke(prompt)
        return {"critic_feedback": response.content}
    except Exception as exc:
        logger.error("critic_node failed: %s", exc)
        raise LLMServiceError("Critic agent LLM call failed") from exc
