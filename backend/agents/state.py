from typing import Optional, TypedDict


class GraphState(TypedDict):
    """Strict, immutable-by-convention LangGraph state definition.
    Each agent node must only return the keys it owns.
    """
    resume_text: str
    github_url: str
    target_role: str
    profile_summary: Optional[str]
    gap_analysis: Optional[dict]
    roadmap: Optional[list]
    critic_feedback: Optional[str]
