from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from api.dependencies import get_db_session, get_llm_client
from models.schemas import AnalysisRequest, AnalysisResponse
from services.orchestration import OrchestrationService

router = APIRouter(prefix="/analysis", tags=["analysis"])


@router.post("/", response_model=AnalysisResponse)
async def run_analysis(
    payload: AnalysisRequest,
    db: Session = Depends(get_db_session),
    llm=Depends(get_llm_client),
) -> AnalysisResponse:
    service = OrchestrationService(db=db, llm=llm)
    return await service.run(payload)
