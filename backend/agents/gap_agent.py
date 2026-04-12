import logging

from agents.state import GraphState
from core.exceptions import LLMServiceError

logger = logging.getLogger(__name__)

_GAP_ANALYSIS_PROMPT = """
You are a career gap analysis expert.
Candidate profile: {profile_summary}
Target role: {target_role}
Market data: {market_data}

Return a JSON object with:
- missing_skills: list of skills the candidate lacks
- matching_skills: list of skills the candidate already has
- match_score: float between 0 and 1
"""


async def gap_node(state: GraphState, llm) -> dict:
    """Compares the candidate profile against market data to identify skill gaps.
    Owns: gap_analysis
    """
    from pydantic import BaseModel

    class GapOutput(BaseModel):
        missing_skills: list[str]
        matching_skills: list[str]
        match_score: float

    try:
        structured_llm = llm.with_structured_output(GapOutput)
        prompt = _GAP_ANALYSIS_PROMPT.format(
            profile_summary=state["profile_summary"],
            target_role=state["target_role"],
            market_data=state.get("gap_analysis", {}).get("market_results", []),
        )
        result: GapOutput = await structured_llm.ainvoke(prompt)
        return {"gap_analysis": result.model_dump()}
    except Exception as exc:
        logger.error("gap_node failed: %s", exc)
        raise LLMServiceError("Gap analysis agent LLM call failed") from exc
