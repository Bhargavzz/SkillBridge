from contextlib import asynccontextmanager
from fastapi import FastAPI

from api.routers import analysis, health


@asynccontextmanager
async def lifespan(app: FastAPI):
    yield


app = FastAPI(
    title="SkillBridge AI",
    version="0.1.0",
    lifespan=lifespan,
)

app.include_router(health.router, prefix="/api/v1")
app.include_router(analysis.router, prefix="/api/v1")
