from contextlib import asynccontextmanager

from fastapi import FastAPI

from app import models  # noqa: F401
from app.api.router import api_router
from app.core.config import get_settings
from app.core.error_handlers import register_exception_handlers

settings = get_settings()


@asynccontextmanager
async def lifespan(_: FastAPI):
    yield


app = FastAPI(
    title=settings.project_name,
    lifespan=lifespan,
)
register_exception_handlers(app)
app.include_router(api_router, prefix=settings.api_v1_prefix)


@app.get("/", tags=["health"])
async def read_root() -> dict[str, str]:
    return {"message": "FieldData weather alerts API"}
