from pydantic import BaseModel, HttpUrl


class AnalysisRequest(BaseModel):
    resume_text: str
    github_url: HttpUrl
    target_role: str


class RoadmapStep(BaseModel):
    title: str
    description: str
    duration_weeks: int
    resources: list[str]


class GapAnalysis(BaseModel):
    missing_skills: list[str]
    matching_skills: list[str]
    match_score: float


class AnalysisResponse(BaseModel):
    profile_summary: str
    gap_analysis: GapAnalysis
    roadmap: list[RoadmapStep]
    critic_feedback: str
