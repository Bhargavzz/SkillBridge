from contextlib import asynccontextmanager

from fastapi import Depends, FastAPI, Request
from fastapi.responses import JSONResponse

from api.dependencies import get_current_user
from api.routers import analysis, health
from api.routers import auth
from core.exceptions import SkillBridgeAPIException


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="SkillBridge AI",
    version="0.1.0",
    lifespan=lifespan,
)


@app.exception_handler(SkillBridgeAPIException)
async def skillbridge_exception_handler(request: Request, exc: SkillBridgeAPIException) -> JSONResponse:
    payload = exc.to_response_dict(endpoint=str(request.url.path))
    return JSONResponse(status_code=exc.status_code, content=payload)


app.include_router(health.router, prefix="/api/v1")
app.include_router(auth.router, prefix="/api/v1")
app.include_router(
    analysis.router,
    prefix="/api/v1",
    dependencies=[Depends(get_current_user)],
)
