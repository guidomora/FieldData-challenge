from fastapi import APIRouter

from app.modules.alerts.router.router import router as alerts_router
from app.modules.notifications.router.router import router as notifications_router
from app.modules.weather.router.router import router as weather_router

api_router = APIRouter()


@api_router.get("/health", tags=["health"])
async def healthcheck() -> dict[str, str]:
    return {"status": "ok"}


api_router.include_router(alerts_router)
api_router.include_router(weather_router)
api_router.include_router(notifications_router)
