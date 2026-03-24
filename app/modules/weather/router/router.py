from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession

from app.core.database import get_db_session
from app.modules.weather.schemas.schemas import WeatherForecastRead
from app.modules.weather.service.service import WeatherForecastService

router = APIRouter(prefix="/weather-forecasts", tags=["weather-forecasts"])
service = WeatherForecastService()


@router.get("/", response_model=list[WeatherForecastRead])
async def list_weather_forecasts(
    session: AsyncSession = Depends(get_db_session),
) -> list[WeatherForecastRead]:
    return await service.list_forecasts(session)

