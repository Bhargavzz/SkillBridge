import uuid

from pydantic import BaseModel, ConfigDict, EmailStr, HttpUrl


# ==========================================
# Auth Schemas
# ==========================================


class UserCreate(BaseModel):
    email: EmailStr
    password: str


class UserRead(BaseModel):
    id: uuid.UUID
    email: EmailStr
    is_active: bool
    model_config = ConfigDict(from_attributes=True)


class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"


class TokenData(BaseModel):
    email: str | None = None


# ==========================================
# Analysis Schemas
# ==========================================


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
