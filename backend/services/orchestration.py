from sqlalchemy.orm import Session

from agents.graph import build_graph
from agents.state import GraphState
from core.exceptions import GraphExecutionError
from models.schemas import AnalysisRequest, AnalysisResponse, GapAnalysis, RoadmapStep


class OrchestrationService:
    """Business logic layer — bridges API routers to the LangGraph execution engine."""

    def __init__(self, db: Session, llm) -> None:
        self._db = db
        self._llm = llm
        self._graph = build_graph(llm=llm, db=db)

    async def run(self, payload: AnalysisRequest) -> AnalysisResponse:
        initial_state: GraphState = {
            "resume_text": payload.resume_text,
            "github_url": str(payload.github_url),
            "target_role": payload.target_role,
            "profile_summary": None,
            "gap_analysis": None,
            "roadmap": None,
            "critic_feedback": None,
        }
        try:
            final_state: GraphState = await self._graph.ainvoke(initial_state)
        except Exception as exc:
            raise GraphExecutionError("LangGraph execution failed") from exc

        return AnalysisResponse(
            profile_summary=final_state["profile_summary"] or "",
            gap_analysis=final_state["gap_analysis"],
            roadmap=final_state["roadmap"] or [],
            critic_feedback=final_state["critic_feedback"] or "",
        )
