from sqlalchemy.ext.asyncio import AsyncSession

from app.modules.weather.models.models import WeatherForecast
from app.modules.weather.repository.repository import WeatherForecastRepository
from app.modules.weather.schemas.schemas import WeatherForecastCreate


class WeatherForecastService:
    def __init__(self, repository: WeatherForecastRepository | None = None) -> None:
        self.repository = repository or WeatherForecastRepository()

    async def list_forecasts(self, session: AsyncSession) -> list[WeatherForecast]:
        return await self.repository.list_all(session)

    async def create_forecast(
        self,
        session: AsyncSession,
        payload: WeatherForecastCreate,
    ) -> WeatherForecast:
        return await self.repository.create(session, payload)

