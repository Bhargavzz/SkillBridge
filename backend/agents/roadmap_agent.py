import logging

from agents.state import GraphState
from core.exceptions import LLMServiceError

logger = logging.getLogger(__name__)

_ROADMAP_PROMPT = """
You are a learning roadmap architect.
Target role: {target_role}
Missing skills: {missing_skills}

Return a JSON array of roadmap steps. Each step must have:
- title: string
- description: string
- duration_weeks: integer
- resources: list of strings (URLs or book titles)
"""


async def roadmap_node(state: GraphState, llm) -> dict:
    """Generates a time-boxed learning roadmap for the identified skill gaps.
    Owns: roadmap
    """
    from pydantic import BaseModel

    class RoadmapStep(BaseModel):
        title: str
        description: str
        duration_weeks: int
        resources: list[str]

    class RoadmapOutput(BaseModel):
        steps: list[RoadmapStep]

    try:
        structured_llm = llm.with_structured_output(RoadmapOutput)
        gap = state.get("gap_analysis") or {}
        prompt = _ROADMAP_PROMPT.format(
            target_role=state["target_role"],
            missing_skills=gap.get("missing_skills", []),
        )
        result: RoadmapOutput = await structured_llm.ainvoke(prompt)
        return {"roadmap": [step.model_dump() for step in result.steps]}
    except Exception as exc:
        logger.error("roadmap_node failed: %s", exc)
        raise LLMServiceError("Roadmap agent LLM call failed") from exc
